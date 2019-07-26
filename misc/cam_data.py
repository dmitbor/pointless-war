
class Camera_Data:
    # Standard Zoom Level of 1
    zoom_level = 1

    # User's Screen Size
    display_width = 640
    display_height = 480

    # Camera Offsets
    camera_offset_mod_x = 0
    camera_offset_mod_y = 0

    def __init__(self, viewport):
        self.display_width = viewport[0]
        self.display_height = viewport[1]
        self.camera_offset_mod_x = 0 - self.get_zoom_padding()[0]
        self.camera_offset_mod_y = 0 - self.get_zoom_padding()[1]

    def add_zoom(self):
        if self.zoom_level < 4:
            self.zoom_level = self.zoom_level + 1
        return self.zoom_level

    def red_zoom(self):
        if self.zoom_level > 0:
            self.zoom_level = self.zoom_level - 1
        return self.zoom_level

    # Return Zoom Level Modifier
    def get_zoom_mod(self):
        if self.zoom_level == 0:
            return 0.5
        elif self.zoom_level == 1:
            return 1
        elif self.zoom_level == 2:
            return 2
        elif self.zoom_level == 3:
            return 5
        elif self.zoom_level == 4:
            return 10

    def get_zoom_padding(self):
        return self.display_width / 2 * self.get_zoom_mod(), self.display_height / 2 * self.get_zoom_mod()

    def go_direction(self, dir, shift):
        # Left or Up (Positive)
        # Right or Down (Negativev)
        dir_val = 1
        cam_trvl = 5

        if dir == "right" or dir == "down":
            dir_val = -1

        if shift is True:
            cam_trvl = 25

        if dir == "right" or dir == "left":
            self.camera_offset_mod_x += dir_val * int(self.get_zoom_mod() * cam_trvl)
        else:
            self.camera_offset_mod_y += dir_val * int(self.get_zoom_mod() * cam_trvl)

    def ret_cam_offset(self):
        return self.camera_offset_mod_x, self.camera_offset_mod_y
