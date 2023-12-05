from PIL import Image

class Coin:
    def __init__(self, x, y):
        self.position = [x, y]
        self.image = Image.open('/home/kau-esw/esw/esw_project/images/coin_an0.png').convert('RGBA')
        self.images = [
            Image.open('/home/kau-esw/esw/esw_project/images/coin_an0.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/coin_an1.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/coin_an2.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/coin_an3.png').convert('RGBA')
        ]
        self.image_index = 0
        
    def update_image(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
    
            
    def get_bounding_box(self):
        return (
            self.position[0] - 15,
            self.position[1] - 15,
            self.position[0] + 15,
            self.position[1] + 15
        )