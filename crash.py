def is_collision(obj1, obj2):
    # 두 객체 간의 충돌 여부 확인
    box1 = obj1.get_bounding_box()
    box2 = obj2.get_bounding_box()

    # 충돌 감지 로직 (여기에서는 간단히 박스의 겹침 여부를 확인)
    if (
        box1[0] < box2[2] and
        box1[2] > box2[0] and
        box1[1] < box2[3] and
        box1[3] > box2[1]
    ):
        print(f"Collision detected: {box1} and {box2}")
        return True
    else:
        print(f"No collision: {box1} and {box2}")
        return False