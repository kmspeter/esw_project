def is_collision(object1, object2):
    box1 = object1.get_bounding_box()
    box2 = object2.get_bounding_box()

    if (
        box1[0] < box2[2] and
        box1[2] > box2[0] and
        box1[1] < box2[3] and
        box1[3] > box2[1]
    ):
        return True
    else:
        return False