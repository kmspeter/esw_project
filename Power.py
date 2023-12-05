from PIL import Image

class Power:
    def __init__(self):
        self.active = False
        self.animation_frames = [
            Image.open('/home/kau-esw/esw/esw_project/images/firework0.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/firework1.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/firework2.png').convert('RGBA')
        ]
        self.current_animation_frame_index = 0
        self.max_usages = 3
        self.available_usages = self.max_usages

    def activate(self):
        self.active = True
        self.available_usages -= 1
        self.current_animation_frame_index = 0

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def update_animation_frame(self):
        if self.active:
            self.current_animation_frame_index = (self.current_animation_frame_index + 1) % len(self.animation_frames)
            if self.current_animation_frame_index == len(self.animation_frames) - 1:
                self.deactivate()

    def get_current_animation_frame(self):
        return self.animation_frames[self.current_animation_frame_index]

    def reactivate(self):
        self.available_usages = self.max_usages