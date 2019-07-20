import random
from units.unit import Unit
from misc.var_calcs import two_point_distance


class Soldier(Unit):
    full_name = []
    rotation_speed = 25.0
    my_squad = None
    # Perception: Governs Ranged Accuracy
    stat_per = 50
    # Agility: Governs Speed, Rotation Speed, Melee Accuracy
    stat_agi = 50
    # Endurance: Governs Ability to Resist Shock from Damage, Running Endurance
    stat_end = 50
    # Intelegence: Governs Ability to Capture Points (Temporary), Leadership Bonus
    stat_int = 50
    speed = 5
    energy = 50
    health = 50
    cap_power = 5

    def __init__(self, namer, squad):
        self.full_name = namer.get_random_name()
        self.my_squad = squad
        print(self.full_name[0].get_name() + " " + self.full_name[1].get_name())
        self.gen_stats()

    def gen_stats(self):
        self.stat_per = random.randint(35, 65)
        self.stat_agi = random.randint(35, 65)
        self.stat_end = random.randint(35, 65)
        self.stat_int = random.randint(35, 65)
        self.speed = int(self.stat_agi / 10)
        self.rotation_speed = int(self.stat_agi / 2)
        self.energy = int(self.stat_end)
        self.health = int(self.stat_end)
        self.cap_power = int(self.stat_int / 10)

    def next_action(self):
        self.recover_end()
        for action in self.my_squad.get_cur_mission().get_mission_orders():
            if action == "NCO_PROX":
                if self.get_distance_to_officer() > 50.0:
                    self.target = self.my_squad.squad_leader
                    self.move_to_target("Run")
                    break
            elif action == "OBJ_PROX":
                if self.get_distance_to_objective() > 10.0:
                    self.target = self.my_squad.get_cur_mission().get_miss_trgt()
                    self.move_to_target()
                    break
            elif action == "OBJ_CAPT":
                # Set immediate target to objective
                self.target = self.my_squad.get_cur_mission().get_miss_trgt()
                self.target.cap_the_point(self.my_squad.squad_faction, self.cap_power)
                # print("Capturing|" + str(self.target.owner_points) + "|" + str(self.my_squad.squad_faction.faction_name))

    def get_distance_to_officer(self):
        leader_x = self.my_squad.squad_leader.x
        leader_y = self.my_squad.squad_leader.y
        return two_point_distance(self.x, self.y, leader_x, leader_y)

    def get_distance_to_objective(self):
        objective_x = self.my_squad.get_cur_mission().get_miss_trgt().map_x
        objective_y = self.my_squad.get_cur_mission().get_miss_trgt().map_y
        return two_point_distance(self.x, self.y, objective_x, objective_y)

    def move_to_target(self, movement="Walk"):
        if self.angle_2_target() is True:
            movement = self.set_tired(movement)
            # Completely exhausted units don't get to move
            if movement == "Stand":
                return None
            new_loc = self.calculate_next_loc(movement)
            self.x = new_loc[0]
            self.y = new_loc[1]

    def recover_end(self):
        self.energy += self.stat_end
        if self.energy > self.stat_end:
            self.energy = self.stat_end

    def set_tired(self, mov_type):
        if self.energy > 0:
            if mov_type == "Run":
                if self.energy >= self.speed * 2:
                    self.energy -= self.speed * 2
                    return "Run"
                else:
                    mov_type = "Walk"
            if mov_type == "Walk":
                if self.energy >= self.speed:
                    self.energy -= self.speed
                    return "Walk"
                else:
                    return "Stand"
        else:
            return "Stand"
