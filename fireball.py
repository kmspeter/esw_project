from PIL import Image

class Fireball:
    def __init__(self, character):
        self.image = Image.open('/home/kau-esw/esw/esw_project/images/fireball_00.png').convert('RGBA')
        self.images = [
            Image.open('/home/kau-esw/esw/esw_project/images/fireball_00.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/fireball_01.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/fireball_02.png').convert('RGBA'),
            Image.open('/home/kau-esw/esw/esw_project/images/fireball_03.png').convert('RGBA')
        ]
        # 캐릭터의 현재 위치를 사용하여 초기 위치 설정
        self.character = character
        self.update_initial_position()
        self.image_index = 0
        self.is_alive = True

    def update_initial_position(self):
        # 초기 위치를 character의 현재 위치로 설정
        self.initial_position = [self.character.position[0], self.character.position[1]]
        self.position = self.initial_position.copy()  # 새로운 리스트를 만들어서 참조 문제 해결

    def update_position(self):
        # 화염구를 초기 위치를 기준으로 오른쪽으로만 이동
        self.position[0] += 20
        self.update_image()
        
    def update_image(self):
        # 이미지 인덱스 업데이트
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        
    def should_disappear(self):
        # 일정 조건을 충족하면 True를 반환하여 화염구를 사라지게 만들기
        max_distance = 100
        distance_moved = abs(self.position[0] - self.initial_position[0])

        if distance_moved > max_distance:
            self.is_alive = False
    
    def get_bounding_box(self):
        return (
            self.position[0] - 10,
            self.position[1] - 10,
            self.position[0] + 10,
            self.position[1] + 10
        )