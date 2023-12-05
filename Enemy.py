from PIL import Image

class Enemy:
    def __init__(self, x, y):
        self.position = [x, y]
        self.initial_position = [x, y]  # 초기 위치
        self.images = [
            Image.open('/home/kau-esw/esw/esw_project/images/koopa_0.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/koopa_1.png').convert('RGBA')
        ]
        self.current_image_index = 0
        self.current_image = self.images[self.current_image_index]
        self.is_alive = True

    def move(self):
        self.position[0] -= 5

        if self.position[0] + self.current_image.width <= 0:
            self.position[0] = 800

        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.current_image = self.images[self.current_image_index]

    def hit_by_fireball(self):
        self.is_alive = False
        
    def should_disappear(self):
        max_distance = 200
        distance_moved = abs(self.position[0] - self.initial_position[0])

        if distance_moved > max_distance:
            self.is_alive = False
            return True
        return False
    
    def get_bounding_box(self):
        return (
            self.position[0] - 20,
            self.position[1] - 20,
            self.position[0] + 20,
            self.position[1] + 20
        )