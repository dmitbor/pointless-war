import math


class Unit:
    # Location
    x = 50
    y = 50
    face_angle = 0.0
    rotation_speed = 15.0

    speed = 0

    movement_target = None
    combat_target = None

    def get_xy(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_location(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        # print("New Location: " + str(self.x) + "/" + str(self.y))

    def get_angle(self):
        return self.face_angle

    def set_move_target(self, given_target):
        self.movement_target = given_target
        return self.movement_target

    def set_comb_target(self, given_target):
        self.combat_target = given_target
        return self.combat_target

    def get_move_target(self):
        return self.movement_target

    def get_comb_target(self):
        return self.combat_target

    def __angle_overflow_handling(self, targ_angle, negative=False):
        if negative is False:
            if (self.face_angle > 180.0):
                # Get overflow and add it to -180 to get new location
                self.face_angle = -180.0 + (self.face_angle - 180.0)
                # If new location overshots target, change facing to target
                if (self.face_angle > targ_angle):
                    self.face_angle = targ_angle
                    return True
            return False
        else:
            if (self.face_angle < -180.0):
                # Get our overflow and subtract it from 180 to get new location
                self.face_angle = 180.0 - abs(self.face_angle + 180.0)
                # If new location overshots target, change facing to target
                if (self.face_angle < targ_angle):
                    self.face_angle = targ_angle
                    return True
            return False

    def angle_2_target(self, target):
        targ_angle = self.calc_angle_2_target(target)

        # Exceptional handling
        # T: Bottom Left. F: Upper Left
        if (self.face_angle < -90.0 and targ_angle > 90.0):
            # Change Facing
            self.face_angle = self.face_angle - self.rotation_speed
            # print(self.face_angle)
            # If we eactually end up over 180 horizon, we're in positives now
            return self.__angle_overflow_handling(targ_angle, True)

        # T: Upper Left. F: Bottom Left
        if (self.face_angle > 90.0 and targ_angle < -90.0):
            # Change Facing
            self.face_angle = self.face_angle + self.rotation_speed
            # print(self.face_angle)
            # If we eactually end up over 180 horizon, we're in negatives now
            return self.__angle_overflow_handling(targ_angle)

        # Normal Angle Handling
        if (self.face_angle == targ_angle):
            return True
        elif (self.face_angle > targ_angle):
            self.face_angle = self.face_angle - self.rotation_speed
            if (self.face_angle < targ_angle):
                self.face_angle = targ_angle
                return True
        elif (self.face_angle < targ_angle):
            self.face_angle = self.face_angle + self.rotation_speed
            if (self.face_angle > targ_angle):
                self.face_angle = targ_angle
                return True
        return False

    def calc_angle_2_target(self, target):
        t_angle = math.atan2(target.get_y() - self.y, target.get_x() - self.x)
        return math.degrees(t_angle)

    def calculate_next_loc(self, movement="Walk"):
        cur_speed = self.speed
        if movement == "Run":
            cur_speed *= 2
        new_x = self.x + (cur_speed * math.cos(math.radians(self.face_angle)))
        new_y = self.y + (cur_speed * math.sin(math.radians(self.face_angle)))
        return new_x, new_y
