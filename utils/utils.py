import math
from typing import Optional


def intersects(item: tuple, other: tuple) -> bool:
    x1, y1, w1, h1 = item
    x2, y2, w2, h2 = other

    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2


def intersects_closest_point(item: tuple, other: tuple) -> tuple:
    x1, y1, w1, h1 = item
    x2, y2, w2, h2 = other

    closest_x = max(x1, x2)
    closest_y = max(y1, y2)

    return closest_x, closest_y


def distance_between_points(point1: tuple, point2: tuple) -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def vector_length_squared(vector: tuple) -> float:
    return vector[0] ** 2 + vector[1] ** 2


def vector_length(vector: tuple) -> float:
    return math.sqrt(vector_length_squared(vector))


def vector_normalize(vector: tuple) -> tuple:
    length = vector_length(vector)

    if length != 0:
        return vector[0] / length, vector[1] / length

    raise ValueError("Cannot normalize a zero-length vector")


def clipline(item: tuple, other: tuple) -> Optional[tuple]:
    itemX1, itemY1, itemX2, itemY2 = item
    otherX1, otherY1, otherX2, otherY2 = other

    # Define constants for Cohen-Sutherland
    INSIDE = 0  # 0000
    LEFT = 1  # 0001
    RIGHT = 2  # 0010
    BOTTOM = 4  # 0100
    TOP = 8  # 1000

    # Helper function to calculate the region code
    def _compute_code(x, y):
        code = INSIDE
        if x < itemX1:  # to the left of rectangle
            code |= LEFT
        elif x > itemX2:  # to the right of rectangle
            code |= RIGHT
        if y < itemY1:  # below the rectangle
            code |= BOTTOM
        elif y > itemY2:  # above the rectangle
            code |= TOP
        return code

    code1 = _compute_code(otherX1, otherY1)
    code2 = _compute_code(otherX2, otherY2)
    accept = False

    while True:
        if not (code1 | code2):
            # Bitwise OR is 0, implying both points are inside
            accept = True
            break
        elif code1 & code2:
            # Bitwise AND is not 0, implying both points are outside
            break
        else:
            # Some segment of line lies within the rectangle
            x = y = None
            # At least one endpoint is outside the rectangle; pick it.
            out_code = code1 if code1 else code2

            # Find intersection point using formulae:
            # y = y1 + slope * (x - x1), x = x1 + (1/slope) * (y - y1)
            if out_code & TOP:
                # point is above the clip rectangle
                x = otherX1 + (otherX2 - otherX1) * (itemY2 - otherY1) / (otherY2 - otherY1)
                y = itemY2
            elif out_code & BOTTOM:
                # point is below the rectangle
                x = otherX1 + (otherX2 - otherX1) * (itemY1 - otherY1) / (otherY2 - otherY1)
                y = itemY1
            elif out_code & RIGHT:
                # point is to the right of rectangle
                y = otherY1 + (otherY2 - otherY1) * (itemX2 - otherX1) / (otherX2 - otherX1)
                x = itemX2
            elif out_code & LEFT:
                # point is to the left of rectangle
                y = otherY1 + (otherY2 - otherY1) * (itemX1 - otherX1) / (otherX2 - otherX1)
                x = itemX1

            # Now move outside point to intersection point to clip
            if out_code == code1:
                otherX1, otherY1 = x, y
                code1 = _compute_code(otherX1, otherY1)
            else:
                otherX2, otherY2 = x, y
                code2 = _compute_code(otherX2, otherY2)

    if accept:
        return (otherX1, otherY1), (otherX2, otherY2)
    else:
        return None
