class Mission():
    target = None
    objectives = []
    # Mission Types:
    # 1 - Objective
    # 2 - Assasination
    type = 0
    completed = False

    def __init__(self):
        self.target = None
        self.objectives = []
        self.type = 0
        self.completed = False

    def set_obj_capture(self, trgt_point):
        self.type = 1
        self.target = trgt_point
        self.objectives = []
        self.objectives.append("NCO_PROX")
        self.objectives.append("OBJ_PROX")
        self.objectives.append("OBJ_CAPT")
        self.completed = False

    def get_miss_type(self):
        return self.type

    def get_miss_trgt(self):
        return self.target

    def get_mission_orders(self):
        return self.objectives

    def check_completion(self, my_squad):
        if self.type == 1:
            if self.target.owner_faction is my_squad.squad_faction and self.target.owner_points == 100:
                self.completed = True
