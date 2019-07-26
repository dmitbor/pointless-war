class Data_Store:
    Factions = None
    Objectives = None
    Soldiers = None
    Squads = None
    sqd_rspw_tmr = 0

    def __init__(self):
        self.Factions = []
        self.Objectives = []
        self.Soldiers = []
        self.Squads = []

    def ret_facts(self):
        return self.Factions

    def ret_objs(self):
        return self.Objectives

    def ret_solds(self):
        return self.Soldiers

    def ret_squads(self):
        return self.Squads

    def ret_rspw_tmr(self):
        return self.sqd_rspw_tmr

    def set_rspw_tmr(self, value):
        self.sqd_rspw_tmr = value
