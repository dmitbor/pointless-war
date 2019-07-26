import random
from units.unit import Unit
from misc.var_calcs import two_point_distance, get_closest_enemy


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
    # Strength: Governs Melee Damage, Carry Weight
    stat_str = 50
    # WIP Melee Damage value
    melee_damage = 5
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
        self.stat_str = random.randint(35, 65)
        self.speed = int(self.stat_agi / 10)
        self.rotation_speed = int(self.stat_agi / 2)
        self.energy = int(self.stat_end)
        self.health = int(self.stat_end)
        self.cap_power = int(self.stat_int / 10)
        self.melee_damage = int(self.stat_str / 10)

    def next_action(self, data_handler):
        self.recover_end()
        for action in self.my_squad.get_cur_mission().get_mission_orders():
            if action == "NCO_PROX":
                if self.get_distance_to_officer() > 50.0:
                    self.movement_target = self.my_squad.squad_leader
                    self.move_to_target("Run")
                    break
            elif action == "OBJ_PROX":
                if self.get_distance_to_objective() > 5.0:
                    self.movement_target = self.my_squad.get_cur_mission().get_miss_trgt()
                    self.move_to_target()
                    break
            elif action == "OBJ_CAPT":
                # Set immediate target to objective
                self.movement_target = self.my_squad.get_cur_mission().get_miss_trgt()
                self.movement_target.cap_the_point(self.my_squad.squad_faction, self.cap_power)
                # Punch enemies in proximity
                if (self.combat_target is not None and self.combat_target.is_alive() and self.in_combat_range(10)):
                    self.WIP_punch_enemy()
                # Find enemy to punch
                else:
                    self.combat_target = get_closest_enemy(data_handler.ret_squads(), self.get_xy(), self.my_squad.squad_faction, 10)
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
        if self.angle_2_target(self.get_move_target()) is True:
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

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    # Punch enemy within range
    def WIP_punch_enemy(self):
        print("Punch!")
        if random.randint(0, 100) <= self.stat_agi:
            self.combat_target.get_hurt(self.melee_damage)

    def get_hurt(self, damage):
        rand_val = random.randint(0, 100)
        if rand_val > self.stat_end:
            self.health -= damage
            print("OW!" + str(damage))
        else:
            dmg = int((self.stat_end - rand_val) / 10)
            self.health -= dmg
            print("OW!" + str(dmg))

        # Set a new leader if we are dead officer
        if self.health <= 0 and self.my_squad.squad_leader == self:
            self.my_squad.set_new_leader()

    def in_combat_range(self, range):
        distance = two_point_distance(self.get_x(), self.get_y(), self.combat_target.get_x(), self.combat_target.get_y())
        if distance > range:
            return False
        else:
            return True
