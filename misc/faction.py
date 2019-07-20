class Faction():
    faction_name = ""
    faction_color = []

    def __init__(self, fname, colors):
        self.faction_name = fname
        self.faction_color = colors

    def get_fac_color(self):
        return self.faction_color

    def get_fac_color_caps(self):
        cap_color = []
        for color in self.faction_color:
            cur_color = color + 50
            if cur_color > 255:
                cur_color = 255 - 50
            elif cur_color < 0:
                cur_color = 50
            cap_color.append(cur_color)
        return cap_color
