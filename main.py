from PIL import Image, ImageDraw, ImageFont
import time
import random
from Character import Character
from Joystick import Joystick
from fireball import Fireball
from Enemy import Enemy
from crash import is_collision
from Power import Power


def show_game_over_screen(joystick):
    # Load game over and restart images
    game_over_image = Image.open('/home/kau-esw/esw/esw_project/images/gameover.png').convert('RGBA')
    continue_image = Image.open('/home/kau-esw/esw/esw_project/images/continue.png').convert('RGBA')

    # Create a blank image for drawing
    game_over_screen = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))
    draw = ImageDraw.Draw(game_over_screen)

    # Calculate center positions for images
    game_over_x = (joystick.width - game_over_image.width) // 2
    game_over_y = (joystick.height - game_over_image.height) // 2
    continue_x = (joystick.width - continue_image.width) // 2
    continue_y = game_over_y + game_over_image.height

    # Paste images onto the blank image
    game_over_screen.paste(game_over_image, (game_over_x, game_over_y), game_over_image)
    game_over_screen.paste(continue_image, (continue_x, continue_y), continue_image)

    # Display the game over screen
    joystick.disp.image(game_over_screen)

def main():
    joystick = Joystick()
    character = Character(joystick.width, joystick.height)
    fireballs = []
    enemies = []
    power = Power()
    
    enemies_killed = 0
    coin_c = 0
    start_time = time.time()
    
    font_size = 15
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

    while True:
        if not character.is_alive:
            show_game_over_screen(joystick)
            # Wait for "R" key to be pressed for restart
            while True:
                if any([not joystick.button_U.value, not joystick.button_D.value,
                        not joystick.button_L.value, not joystick.button_R.value,
                        not joystick.button_A.value]):
                    break
                time.sleep(0.1)
            # Reset the game
            character.is_alive = True
            character = Character(joystick.width, joystick.height)
            fireballs = []
            enemies = []
            power.reactivate()
            enemies_killed = 0
            coin_c = 0
            start_time = time.time()
            
        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'attack': False, 'power': False}

        if not joystick.button_U.value:
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:
            command['right_pressed'] = True
            command['move'] = True

        if not joystick.button_A.value:
            command['attack'] = True
            
        if not joystick.button_B.value:
            command['power'] = True

        if command['power']:
            if power.available_usages > 0:
                power.activate()

        character.move(command)

        display_x = character.position[0]
        display_y = character.position[1]

        my_image = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))
        draw = ImageDraw.Draw(my_image)
        
        if power.is_active():
            # Power가 활성화된 경우에는 애니메이션 업데이트
            power.update_animation_frame()
            # 애니메이션 프레임을 현재 위치에 표시
            my_image.paste(power.get_current_animation_frame(), (joystick.width // 2 - 70, joystick.height // 2 - 70), power.get_current_animation_frame())

        my_image.paste(character.current_image, (display_x, display_y), character.current_image)

        # 화염구를 생성하고 my_image에 paste
        if command['attack']:
            new_fireball = Fireball(character)
            fireballs.append(new_fireball)
            new_fireball.update_initial_position()

        # 모든 화염구에 대해 위치 업데이트 및 화면에 표시
        for fireball in fireballs.copy():
            fireball.update_position()
            my_image.paste(fireball.image, (fireball.position[0], fireball.position[1]), fireball.image)

            # 적과의 충돌 체크
            for enemy in enemies.copy():
                if enemy.is_alive and is_collision(fireball, enemy):
                    enemies_killed += 1
                    fireball.should_disappear()
                    enemy.hit_by_fireball()
                    # 적을 리스트에서 제거
                    enemies.remove(enemy)

        # 모든 적에 대해 위치 업데이트, 충돌 체크 및 화면에 표시
        for enemy in enemies:
            enemy.move()

            for fireball in fireballs:
                if fireball.should_disappear() or not enemy.is_alive:
                    continue

                if is_collision(fireball, enemy):
                    enemies_killed += 1
                    fireball.should_disappear()
                    enemy.hit_by_fireball()

            enemies = [e for e in enemies if e.is_alive]

            enemy_display_x = enemy.position[0]
            enemy_display_y = enemy.position[1]
            my_image.paste(enemy.current_image, (enemy_display_x, enemy_display_y), enemy.current_image)
            
            if power.is_active():
                # 활성화된 Power 상태에서는 모든 적을 제거
                enemies = []
            
            if is_collision(character, enemy):
                character.is_alive = False

        # 일정 확률로 새로운 적 생성
        if random.randint(0, 100) < 10:
            new_enemy = Enemy(
                character.position[0] + 200,
                random.randint(0, joystick.height - 50)
            )
            enemies.append(new_enemy)

        top_text = f"Score: {enemies_killed*200 + coin_c*500 + int(time.time() - start_time)*20} | Time: {int(time.time() - start_time)}s"
        next_text = f"Boss appears: {10000 - enemies_killed*200 + coin_c*500}"
        power_text = f"Power: {power.available_usages}"
        draw.text((10, 10), top_text, fill=(0, 0, 0), font=font)
        draw.text((10, 25), next_text, fill=(0, 0, 0), font=font)
        draw.text((10, 40), power_text, fill=(0, 0, 0), font=font)

        # 화면 업데이트
        joystick.disp.image(my_image)
        time.sleep(0.1)

if __name__ == '__main__':
    main()