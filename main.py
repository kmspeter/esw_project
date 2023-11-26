from PIL import Image, ImageDraw, ImageFont
import time
import random
from Character import Character
from Joystick import Joystick
from Camera import Camera
from fireball import Fireball
from Enemy import Enemy
from crash import is_collision

def main():
    joystick = Joystick()
    character = Character(joystick.width, joystick.height)
    camera = Camera(joystick.width, joystick.height)
    fireballs = []
    enemies = []

    while True:
        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'attack': False}

        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        if not joystick.button_A.value:  # attack pressed
            command['attack'] = True

        character.move(command)
        camera.follow_character(character)
        
        display_x = character.position[0] - camera.offset_x
        display_y = character.position[1] - camera.offset_y

        # Create a new image with a white background
        my_image = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))
        draw = ImageDraw.Draw(my_image)

        # Paste the current character image onto the new image at the character's position
        my_image.paste(character.current_image, (display_x, display_y), character.current_image)

        # 화염구를 생성한 후에 my_image에 paste
        if command['attack']:
            # 화염구 객체 생성 (character를 전달하여 초기 위치를 설정)
            new_fireball = Fireball(character, camera.offset_x, camera.offset_y)
            fireballs.append(new_fireball)

            # 업데이트된 초기 위치로 화염구의 시작 위치 설정
            new_fireball.update_initial_position()

        # 모든 화염구에 대해 위치 업데이트
        for fireball in fireballs:
            fireball.update_position()
            my_image.paste(fireball.image, (fireball.position[0], fireball.position[1]), fireball.image)

            # 적과의 충돌 체크
            for enemy in enemies:
                if enemy.is_alive and is_collision(fireball, enemy):
                    # 화염구가 적에게 맞았을 때
                    fireball.should_disappear()
                    enemy.hit_by_fireball()
                    
       # 적 객체를 화면에 추가하고, 적 이동 및 화염구에 맞았는지 확인
        for enemy in enemies:
            enemy.move()
            my_image.paste(enemy.current_image, (enemy.position[0] - camera.offset_x, enemy.position[1] - camera.offset_y), enemy.current_image)

        # 적이 화염구에 맞아 죽으면 리스트에서 제거
        enemies = [enemy for enemy in enemies if enemy.is_alive]
        
        if random.randint(0, 100) < 5:
        # 캐릭터의 위치를 기준으로 오른쪽에 나타나도록 설정
            new_enemy = Enemy(
                character.position[0] + 200,  # 예시로 200의 간격을 두었습니다. 원하는 값으로 조절해주세요.
                random.randint(0, joystick.height - 50)
            )
            enemies.append(new_enemy)

        # 화면 업데이트
        joystick.disp.image(my_image)
        time.sleep(0.1)

if __name__ == '__main__':
    main()