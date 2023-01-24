#! /usr/bin/python3

import enum

class Directions(enum.Enum):
    """
    Positions are defined by (row_index_offset, column_index_offset)
    """
    UP         = (-1,  0)
    UP_RIGHT   = (-1,  1)
    RIGHT      = ( 0,  1)
    DOWN_RIGHT = ( 1,  1)
    DOWN       = ( 1,  0)
    DOWN_LEFT  = ( 1, -1)
    LEFT       = ( 0, -1)
    UP_LEFT    = (-1, -1)

    def is_valid(self, pos: tuple, img_size: tuple):
        """
        pos should be (row_index, column_index)
        img_size should be (row_number, column_number)
        Returns True when the tile is inside the image -> edge cases are removed
        """
        if pos[0] + self.value[0] >= 0 and pos[0] + self.value[0] <= img_size[0] - 1:
            if pos[1] + self.value[1] >= 0 and pos[1] + self.value[1] <= img_size[1] - 1:
                return True
        return False

    def negate(self):
        """
        Returns the direction pointing in the exact opposite direction of <self>
        """
        return [direction for direction in Directions if direction.value[0] == -self.value[0] and direction.value[1] == -self.value[1]][0]
