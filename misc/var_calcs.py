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


def get_closest_enemy(search_squads, my_loc, my_fac, max_range=0):
    to_return = None
    cur_dist = -1

    for squad in search_squads:
        if squad.squad_faction is not my_fac:
            sqd_ld_loc = squad.squad_leader.get_xy()
            distance = two_point_distance(my_loc[0], my_loc[1], sqd_ld_loc[0], sqd_ld_loc[1])
            if max_range == 0 or distance <= max_range:
                if cur_dist == -1 or distance < cur_dist:
                    for soldier in squad.squad_members:
                        if soldier.is_alive():
                            distance = two_point_distance(my_loc[0], my_loc[1], soldier.get_x(), soldier.get_y())
                            if (cur_dist == -1 or distance < cur_dist) and (max_range == 0 or distance <= max_range):
                                to_return = soldier
                                cur_dist = distance
    return to_return
