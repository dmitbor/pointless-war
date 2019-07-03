import math


def two_point_distance(x1, y1, x2, y2):
    """
    Calculates distance between two given points.

    x1 - X Value of Point 1
    y1 - Y Value of Point 1
    x2 - X Value of Point 2
    y2 - Y Value of Point 2
    """

    return math.fabs(math.hypot(x2 - x1, y2 - y1))
