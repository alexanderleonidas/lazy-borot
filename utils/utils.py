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
    return tuple_length(subtract_tuples(point1, point2))


def subtract_tuples(t1, t2):
    return t1[0] - t2[0], t1[1] - t2[1]


def tuple_length(t):
    return math.sqrt(t[0] ** 2 + t[1] ** 2)


def vector_length_squared(vector: tuple) -> float:
    return vector[0] ** 2 + vector[1] ** 2


def vector_length(vector: tuple) -> float:
    return math.sqrt(vector_length_squared(vector))


def vector_normalize(vector: tuple) -> tuple:
    length = vector_length(vector)

    if length != 0:
        return vector[0] / length, vector[1] / length

    raise ValueError("Cannot normalize a zero-length vector")


def clipline(obstacle, start_pos, end_pos):
    left, top, width, height = obstacle
    right = left + width
    bottom = top + height
    x1, y1 = start_pos
    x2, y2 = end_pos

    def line_intersection(p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None  # Lines are parallel

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if 0 <= t <= 1 and 0 <= u <= 1:
            return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        else:
            return None

    intersections = []
    edges = [
        ((left, top), (right, top)),
        ((right, top), (right, bottom)),
        ((right, bottom), (left, bottom)),
        ((left, bottom), (left, top))
    ]

    for edge_start, edge_end in edges:
        intersect_point = line_intersection(start_pos, end_pos, edge_start, edge_end)
        if intersect_point:
            intersections.append(intersect_point)

    if len(intersections) == 2:
        return tuple(intersections)
    elif len(intersections) > 2:
        # When there are more than two intersections, it returns the points that are on the segment
        return tuple(sorted(intersections, key=lambda point: (point[0] - x1)**2 + (point[1] - y1)**2)[:2])
    return ()


