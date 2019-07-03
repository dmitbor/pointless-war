from units.unit import Unit
from misc.var_calcs import two_point_distance


class Soldier(Unit):
    full_name = []
    speed = 5
    rotation_speed = 30.0
    my_squad = None
    stat_agi = 50
    stat_end = 50

    def __init__(self, namer, squad):
        self.full_name = namer.get_random_name()
        self.my_squad = squad
        print(self.full_name[0].get_name() + " " + self.full_name[1].get_name())

    def next_action(self):
        for action in self.my_squad.get_cur_mission().get_mission_orders():
            if action == "NCO_PROX":
                if self.get_distance_to_officer() > 50.0:
                    self.target = self.my_squad.squad_leader
                    self.move_to_target()
                    break
            elif action == "OBJ_PROX":
                if self.get_distance_to_objective() > 10.0:
                    self.target = self.my_squad.get_cur_mission().get_miss_trgt()
                    self.move_to_target()
                    break
            elif action == "OBJ_CAPT":
                self.target.cap_the_point(self.my_squad.squad_faction)
                print("Capturing|" + str(self.target.owner_points) + "|" + str(self.my_squad.squad_faction.faction_name))

    def get_distance_to_officer(self):
        leader_x = self.my_squad.squad_leader.x
        leader_y = self.my_squad.squad_leader.y
        return two_point_distance(self.x, self.y, leader_x, leader_y)

    def get_distance_to_objective(self):
        objective_x = self.my_squad.get_cur_mission().get_miss_trgt().map_x
        objective_y = self.my_squad.get_cur_mission().get_miss_trgt().map_y
        return two_point_distance(self.x, self.y, objective_x, objective_y)

    def move_to_target(self):
        if self.angle_2_target() is True:
            new_loc = self.calculate_next_loc()
            self.x = new_loc[0]
            self.y = new_loc[1]
