# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from enum import Enum
from openram import debug
from openram.base.vector3d import vector3d


class direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    UP = 5
    DOWN = 6
    NORTHEAST = 7
    NORTHWEST = 8
    SOUTHEAST = 9
    SOUTHWEST = 10

    def get_offset(direct):
        """
        Returns the vector offset for a given direction.
        """
        if direct==direction.NORTH:
            offset = vector3d(0, 1, 0)
        elif direct==direction.SOUTH:
            offset = vector3d(0, -1 ,0)
        elif direct==direction.EAST:
            offset = vector3d(1, 0, 0)
        elif direct==direction.WEST:
            offset = vector3d(-1, 0, 0)
        elif direct==direction.UP:
            offset = vector3d(0, 0, 1)
        elif direct==direction.DOWN:
            offset = vector3d(0, 0, -1)
        elif direct==direction.NORTHEAST:
            offset = vector3d(1, 1, 0)
        elif direct==direction.NORTHWEST:
            offset = vector3d(-1, 1, 0)
        elif direct==direction.SOUTHEAST:
            offset = vector3d(1, -1, 0)
        elif direct==direction.SOUTHWEST:
            offset = vector3d(-1, -1, 0)
        else:
            debug.error("Invalid direction {}".format(direct))

        return offset

    def cardinal_directions(up_down_too=False):
        temp_dirs = [direction.NORTH, direction.EAST, direction.SOUTH, direction.WEST]
        if up_down_too:
            temp_dirs.extend([direction.UP, direction.DOWN])
        return temp_dirs

    def cardinal_offsets(up_down_too=False):
        return [direction.get_offset(d) for d in direction.cardinal_directions(up_down_too)]

    def all_directions():
        return [direction.NORTH, direction.EAST, direction.SOUTH, direction.WEST,
                direction.NORTHEAST, direction.NORTHWEST, direction.SOUTHEAST, direction.SOUTHWEST]

    def all_offsets():
        return [direction.get_offset(d) for d in direction.all_directions()]

    def all_neighbors(cell):
        return [cell + x for x in direction.all_offsets()]

    def cardinal_neighbors(cell):
        return [cell + x for x in direction.cardinal_offsets()]

