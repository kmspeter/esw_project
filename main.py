from PIL import Image, ImageDraw, ImageFont
import time
import random
import numpy as np
from colorsys import hsv_to_rgb
from Character import Character
from Joystick import Joystick

def main():
    joystick = Joystick()
    character = Character(joystick.width, joystick.height)

    while True:
        command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

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

        character.move(command)

        # Create a new image with a white background
        my_image = Image.new("RGB", (joystick.width, joystick.height), (255, 255, 255))
        draw = ImageDraw.Draw(my_image)

        # Paste the current character image onto the new image at the character's position
        my_image.paste(character.current_image, (character.position[0], character.position[1]), character.current_image)

        joystick.disp.image(my_image)
        time.sleep(0.1)

if __name__ == '__main__':
    main()