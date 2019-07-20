import random
import pygame


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

    def cap_the_point(self, caping_faction, cap_power=1):
        # For funsies, randomize capping power.
        cap_power = random.randint(1, cap_power)
        # Neutral Point
        if self.owner_faction is None:
            self.owner_points = cap_power
            self.owner_faction = caping_faction
        # Enemy-Held Point
        elif self.owner_faction is not caping_faction:
            self.owner_points -= cap_power
            if self.owner_points <= 0:
                self.owner_faction = None
                self.owner_points = 0
        # Ongoing Capture/Recapture
        elif self.owner_faction is caping_faction:
            if self.owner_points < 100:
                self.owner_points += cap_power
            elif self.owner_points > 100:
                self.owner_points = 100

    def draw(self, draw_screen, zl, cam_mod):
        # Do not draw neutral self if we're not getting capped
        if (self.owner_points != 100):
            neut_color = (200, 200, 200)
            pygame.draw.rect(draw_screen, neut_color, ((self.map_x - self.obj_size / 2 + cam_mod[0]) / zl, (self.map_y - self.obj_size / 2 + cam_mod[1]) / zl, self.obj_size / zl, self.obj_size / zl))

        if self.owner_faction is not None:
            color = self.owner_faction.get_fac_color_caps()
            pygame.draw.rect(draw_screen, color, ((self.map_x - self.obj_size / 2 + cam_mod[0]) / zl, (self.map_y - self.obj_size / 2 + cam_mod[1]) / zl, (self.obj_size / 100 * self.owner_points) / zl, self.obj_size / zl))
