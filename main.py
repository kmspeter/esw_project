from PIL import Image, ImageDraw, ImageFont
import time
import random
from Character import Character
from Joystick import Joystick
from fireball import Fireball
from Enemy import Enemy
from crash import is_collision
from Power import Power
from Coin import Coin


def show_game_over_screen(joystick):
    game_over_image = Image.open('/home/kau-esw/esw/esw_project/images/gameover.png').convert('RGBA')
    continue_image = Image.open('/home/kau-esw/esw/esw_project/images/continue.png').convert('RGBA')

    game_over_screen = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))

    game_over_x = (joystick.width - game_over_image.width) // 2
    game_over_y = (joystick.height - game_over_image.height) // 2
    continue_x = (joystick.width - continue_image.width) // 2
    continue_y = game_over_y + game_over_image.height

    game_over_screen.paste(game_over_image, (game_over_x, game_over_y), game_over_image)
    game_over_screen.paste(continue_image, (continue_x, continue_y), continue_image)

    joystick.disp.image(game_over_screen)
    

def show_game_clear_screen(joystick):
    clear_image = Image.open('/home/kau-esw/esw/esw_project/images/clear.png').convert('RGBA')

    clear_screen = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))
    draw = ImageDraw.Draw(clear_screen)

    clear_x = (joystick.width - clear_image.width) // 2
    clear_y = (joystick.height - clear_image.height) // 2
    clear_screen.paste(clear_image, (clear_x, clear_y), clear_image)
    
    font_size = 20
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    
    text = "Congratulations!"
    text_width, text_height = draw.textsize(text, font)
    text_x = (joystick.width - text_width) // 2
    text_y = clear_y - text_height - 20
    draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
    
    restart_text = "Press B to Restart"
    restart_width, restart_height = draw.textsize(restart_text, font)
    restart_x = (joystick.width - restart_width) // 2
    restart_y = clear_y + clear_image.height + 20
    draw.text((restart_x, restart_y), restart_text, fill=(0, 0, 0), font=font)

    joystick.disp.image(clear_screen)
    

def main():
    joystick = Joystick()
    character = Character(joystick.width, joystick.height)
    fireballs = []
    enemies = []
    power = Power()
    coins = [Coin(joystick.width // 2, joystick.height // 2) for _ in range(3)]

    
    enemies_killed = 0
    coin_c = 0
    start_time = time.time()
    
    font_size = 15
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    
    background_image = Image.open('/home/kau-esw/esw/esw_project/images/back.png').convert('RGBA')


    while True:
        if not character.is_alive:
            show_game_over_screen(joystick)
            while True:
                if not joystick.button_B.value:
                    time.sleep(0.1)
                    break
                time.sleep(0.1)
            # 게임재시작
            character.is_alive = True
            character = Character(joystick.width, joystick.height)
            fireballs = []
            enemies = []
            coins = [Coin(joystick.width // 2, joystick.height // 2) for _ in range(3)]
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

        my_image = background_image.copy()
        draw = ImageDraw.Draw(my_image)
        
        if power.is_active():
            power.update_animation_frame()
            my_image.paste(power.get_current_animation_frame(), (joystick.width // 2 - 70, joystick.height // 2 - 70), power.get_current_animation_frame())

        my_image.paste(character.current_image, (display_x, display_y), character.current_image)

        # 화염구를 생성
        if command['attack']:
            new_fireball = Fireball(character)
            fireballs.append(new_fireball)
            new_fireball.update_initial_position()

        # 화염구 위치 업데이트
        for fireball in fireballs.copy():
            fireball.update_position()
            my_image.paste(fireball.image, (fireball.position[0], fireball.position[1]), fireball.image)

            # 적과 충돌 체크
            for enemy in enemies.copy():
                if enemy.is_alive and is_collision(fireball, enemy):
                    enemies_killed += 1
                    fireball.should_disappear()
                    enemy.hit_by_fireball()
                    # 적을 제거
                    enemies.remove(enemy)

        # 적 위치 업데이트 및 충돌 체크
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
                # Power로 모든 적 제거
                enemies = []
            
            if is_collision(character, enemy):
                #캐릭터 사망
                character.is_alive = False

        # 일정 확률로 적 생성
        if random.randint(0, 100) < 10:
            new_enemy = Enemy(
                character.position[0] + 200,
                random.randint(0, joystick.height - 50)
            )
            enemies.append(new_enemy)
            
        for coin in coins:
            coin.update_image()
            my_image.paste(coin.image, (coin.position[0], coin.position[1]), coin.image)

        for coin in coins.copy():
            coin.update_image()
            my_image.paste(coin.image, (coin.position[0], coin.position[1]), coin.image)

            # 캐릭터와 동전 충돌 체크
            if is_collision(character, coin):
                coin_c += 1
                coins.remove(coin)
        
        if random.randint(0, 100) < 1:
            new_coin = Coin(
                random.randint(0, joystick.width//2),
                random.randint(50, joystick.height-50)
            )
            coins.append(new_coin)
        
        top_text = f"Score: {enemies_killed*200 + coin_c*500 + int(time.time() - start_time)*20} | Time: {int(time.time() - start_time)}s"
        next_text = f"Clear: {20000 - (enemies_killed*200 + coin_c*500 + int(time.time() - start_time)*20)}"
        power_text = f"Power: {power.available_usages}"
        draw.text((10, 10), top_text, fill=(0, 0, 0), font=font)
        draw.text((10, 25), next_text, fill=(0, 0, 0), font=font)
        draw.text((10, 40), power_text, fill=(0, 0, 0), font=font)

        # 화면 업데이트
        joystick.disp.image(my_image)
        time.sleep(0.1)
        
        #게임 클리어
        if enemies_killed*200 + coin_c*500 >= 500:
            show_game_clear_screen(joystick)
            # 게임 클리어 후 대기
            while True:
                if not joystick.button_B.value:
                    time.sleep(0.1)
                    break
                time.sleep(0.1)
            # 게임 리셋
            character.is_alive = True
            character = Character(joystick.width, joystick.height)
            fireballs = []
            enemies = []
            coins = [Coin(joystick.width // 2, joystick.height // 2) for _ in range(3)]
            power.reactivate()
            enemies_killed = 0
            coin_c = 0
            start_time = time.time()

if __name__ == '__main__':
    main()