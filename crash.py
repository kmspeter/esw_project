def is_collision(obj1, obj2):
    # 두 객체 간의 충돌 여부 확인
    box1 = obj1.get_bounding_box()
    box2 = obj2.get_bounding_box()

    # 충돌 감지 로직
    if (
        box1[0] < box2[2] and
        box1[2] > box2[0] and
        box1[1] < box2[3] and
        box1[3] > box2[1]
    ):
        return True
    else:
        return False