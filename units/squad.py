from misc.var_calcs import two_point_distance
from misc.mission import Mission


class Squad():
    squad_name = ""
    squad_leader = None
    squad_members = []
    squad_faction = None
    squad_missions = None
    ref_objs = None
    ref_squads = None

    def __init__(self):
        self.squad_name = ""
        self.squad_leader = None
        self.squad_members = []
        self.squad_faction = None
        self.squad_missions = []
        self.ref_objs = None
        self.ref_squads = None

    def assign_squad_name(self, given_name):
        self.squad_name = given_name

    def set_first_as_lead(self):
        self.squad_leader = self.squad_members[0]

    def set_new_leader(self):
        sldr_chosen = None
        sldr_int = 0
        for soldier in self.squad_members:
            if soldier.is_alive():
                if soldier.stat_int > sldr_int:
                    sldr_chosen = soldier
        if sldr_chosen is not None:
            self.squad_leader = sldr_chosen

    def assign_to_squad(self, unit_or_list):
        for unit in unit_or_list:
            self.squad_members.append(unit)

    def set_faction(self, faction):
        self.squad_faction = faction

    def set_new_target(self, ref_objs, trgt_type):
        if trgt_type == "objective":
            cur_choice = None
            cur_distance = 0

            # Find closest objective to capture.
            for target in ref_objs:
                if target.get_owner() is not self.squad_faction:
                    trgt_x = target.get_x()
                    trgt_y = target.get_y()
                    sqd_x = self.squad_leader.get_x()
                    sqd_y = self.squad_leader.get_y()
                    trgt_distance = two_point_distance(sqd_x, sqd_y, trgt_x, trgt_y)

                    print(trgt_distance)
                    if trgt_distance < cur_distance or cur_distance == 0:
                        cur_choice = target
                        cur_distance = trgt_distance

            if cur_choice is not None:
                new_mission = Mission()
                new_mission.set_obj_capture(cur_choice)
                self.squad_missions.append(new_mission)
                # self.set_members_to_objctv()
            else:
                print("We got all points! Victory!")

    def find_objective(self):
        self.set_new_target(self.ref_objs, "objective")

    def get_cur_mission(self):
        return self.squad_missions[len(self.squad_missions) - 1]

    def clear_completed_mission(self):
        if self.get_cur_mission().completed is True:
            self.remove_latest_mission()
            self.find_objective()

    def remove_latest_mission(self):
        self.squad_missions.pop(len(self.squad_missions) - 1)

    # def set_members_to_objctv(self):
    #     for member in self.squad_members:
    #         member.set_target(self.get_cur_mission().target)

    def give_ref_obj(self, obj_list):
        self.ref_objs = obj_list
