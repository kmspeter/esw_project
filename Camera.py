class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0

    def follow_character(self, character):
        # 카메라의 위치를 캐릭터의 위치에 맞추기
        self.offset_x = character.position[0] - self.width // 2
        self.offset_y = character.position[1] - self.height // 2

        # 화면을 캐릭터의 일정 범위 안에서 이동
        if character.position[0] < self.offset_x + self.width * 0.2:
            self.offset_x = max(0, character.position[0] - self.width * 0.2)
        elif character.position[0] > self.offset_x + self.width * 0.8:
            self.offset_x = min(character.width - self.width, character.position[0] - self.width * 0.8)

        if character.position[1] < self.offset_y + self.height * 0.2:
            self.offset_y = max(0, character.position[1] - self.height * 0.2)
        elif character.position[1] > self.offset_y + self.height * 0.8:
            self.offset_y = min(character.height - self.height, character.position[1] - self.height * 0.8)