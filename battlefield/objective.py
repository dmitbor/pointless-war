import random


class Objective:
    map_x = 0
    map_y = 0
    obj_size = 50
    owner_faction = None
    owner_points = 0

    def set_random_location(self, map_size_x, map_size_y):
        self.map_x = random.randint(self.obj_size, map_size_x - self.obj_size)
        self.map_y = random.randint(self.obj_size, map_size_y - self.obj_size)

    def set_location(self, given_x, given_y):
        self.map_x = given_x
        self.map_y = given_y

    def get_x(self):
        return self.get_obj_x()

    def get_y(self):
        return self.get_obj_y()

    def get_obj_x(self):
        return self.map_x

    def get_obj_y(self):
        return self.map_y

    def get_obj_size(self):
        return self.obj_size

    def get_owner(self):
        return self.owner_faction

    def cap_the_point(self, caping_faction):
        # Neutral Point
        if self.owner_faction is None:
            self.owner_points = 1
            self.owner_faction = caping_faction
        # Enemy-Held Point
        elif self.owner_faction is not caping_faction:
            self.owner_points -= 1
            if self.owner_points <= 0:
                self.owner_faction = None
                self.owner_points = 0
        # Ongoing Capture/Recapture
        elif self.owner_faction is caping_faction:
            if self.owner_points < 100:
                self.owner_points += 1
            elif self.owner_points > 100:
                self.owner_points = 100
