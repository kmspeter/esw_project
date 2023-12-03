from PIL import Image, ImageDraw
import time
import random
import numpy as np

class Character:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = [width // 2 - 70, height // 2]
        self.idle_image = Image.open('/home/kau-esw/esw/esw_project/images/mario.png').convert('RGBA')
        self.move_images = [
            Image.open('/home/kau-esw/esw/esw_project/images/mario_move0.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/mario_move1.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/mario_move2.png').convert('RGBA')
        ]
        self.current_image = self.idle_image
        self.current_move_index = 0
        self.is_alive = True

    def move(self, command):
        if not self.is_alive:
            return
        if command['move']:
            # 움직이는 상태일 때 순서대로 이미지 변경
            self.current_image = self.move_images[self.current_move_index]
            self.current_move_index = (self.current_move_index + 1) % len(self.move_images)
            
            
            if command['left_pressed']:
                self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
                
            if command['up_pressed']:
                self.position[1] -= 10
            if command['down_pressed']:
                self.position[1] += 10
            if command['left_pressed']:
                self.position[0] -= 10
            if command['right_pressed']:
                self.position[0] += 10
        else:
            # 정지 상태일 때 idle 이미지 사용
            self.current_image = self.idle_image
            
    def get_bounding_box(self):
        return (
            self.position[0] - 5,
            self.position[1] - 5,
            self.position[0] + 5,
            self.position[1] + 5
        )