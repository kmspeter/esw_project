from PIL import Image

class Fireball:
    def __init__(self, character, camera_offset_x, camera_offset_y):
        self.image = Image.open('/home/kau-esw/esw/esw_project/images/fireball.png').convert('RGBA')
        # 캐릭터의 현재 위치를 사용하여 초기 위치 설정
        self.character = character
        self.camera_offset_x = camera_offset_x
        self.camera_offset_y = camera_offset_y
        self.update_initial_position()

    def update_initial_position(self):
        # 초기 위치를 character의 현재 위치로 설정
        self.initial_position = [self.character.position[0] - self.camera_offset_x, self.character.position[1] - self.camera_offset_y]
        self.position = self.initial_position.copy()  # 새로운 리스트를 만들어서 참조 문제 해결

    def update_position(self):
        # 화염구를 초기 위치를 기준으로 오른쪽으로만 이동
        self.position[0] += 20

    def should_disappear(self):
        # 일정 조건을 충족하면 True를 반환하여 화염구를 사라지게 만들기
        max_distance = 100
        distance_moved = abs(self.position[0] - self.initial_position[0])

        return distance_moved > max_distance
    
    def get_bounding_box(self):
        # 화염구의 경계 상자 정보 반환
        return (
            self.position[0],
            self.position[1],
            self.position[0] + self.image.width,
            self.position[1] + self.image.height
        )