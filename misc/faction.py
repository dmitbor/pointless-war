class Faction():
    faction_name = ""
    faction_color = []

    def __init__(self, fname, colors):
        self.faction_name = fname
        self.faction_color = colors

    def get_fac_color(self):
        return self.faction_color
