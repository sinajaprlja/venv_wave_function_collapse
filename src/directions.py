#! /usr/bin/python3

import enum

class Directions(enum.Enum):
    UP         = ( 0, -1)
    UP_RIGHT   = ( 1, -1)
    RIGHT      = ( 1,  0)
    DOWN_RIGHT = ( 1,  1)
    DOWN       = ( 0,  1)
    DOWN_LEFT  = (-1,  1)
    LEFT       = (-1,  0)
    UP_LEFT    = (-1, -1)

    # Returns True when the tile is inside the image -> edge cases are removed
    def is_valid(self, pos, img_size):
        if pos[0] + self.value[0] >= 0 and pos[0] + self.value[0] < img_size[0] - 1:
            if pos[1] + self.value[1] >= 0 and pos[1] + self.value[1] < img_size[1] - 1:
                return True
        return False
