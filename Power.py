from PIL import Image

class Power:
    def __init__(self):
        # Power가 활성화되었는지 여부 및 애니메이션 관련 변수들 추가
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
        # Power 활성화 시 초기화
        self.active = True
        self.available_usages -= 1
        self.current_animation_frame_index = 0

    def deactivate(self):
        # Power 비활성화 시 초기화
        self.active = False

    def is_active(self):
        return self.active

    def update_animation_frame(self):
        # Power 애니메이션 업데이트
        if self.active:
            self.current_animation_frame_index = (self.current_animation_frame_index + 1) % len(self.animation_frames)
            if self.current_animation_frame_index == len(self.animation_frames) - 1:
                # 마지막 프레임까지 도달하면 자동으로 비활성화
                self.deactivate()

    def get_current_animation_frame(self):
        # 현재 애니메이션 프레임 반환
        return self.animation_frames[self.current_animation_frame_index]

    def reactivate(self):
        # Power 재활성화
        self.available_usages = self.max_usages