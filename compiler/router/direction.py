from enum import Enum
from vector3d import vector3d

class direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    UP = 5
    DOWN = 6


    def get_offset(direct):
        """ 
        Returns the vector offset for a given direction.
        """
        if direct==direction.NORTH:
            offset = vector3d(0,1,0)
        elif direct==direction.SOUTH:
            offset = vector3d(0,-1,0)
        elif direct==direction.EAST:
            offset = vector3d(1,0,0)
        elif direct==direction.WEST:
            offset = vector3d(-1,0,0)
        elif direct==direction.UP:
            offset = vector3d(0,0,1)
        elif direct==direction.DOWN:
            offset = vector3d(0,0,-1)
        else:
            debug.error("Invalid direction {}".format(dirct))

        return offset
