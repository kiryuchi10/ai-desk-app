# utils.py
def estimate_distance(object_width, finger_width, arm_length):
    """
    거리 R = (물체 실제 너비 × 팔 길이) / 손가락 너비
    """
    try:
        distance = (object_width * arm_length) / finger_width
        return round(distance, 2)
    except ZeroDivisionError:
        return None
