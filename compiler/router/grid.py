# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base.vector3d import vector3d
from .grid_cell import grid_cell


class grid:
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """
    # costs are relative to a unit grid
    # non-preferred cost allows an off-direction jog of 1 grid
    # rather than 2 vias + preferred direction (cost 5)
    VIA_COST = 2
    NONPREFERRED_COST = 4
    PREFERRED_COST = 1

    def __init__(self, ll, ur, track_width):
        """ Initialize the map and define the costs. """

        # list of the source/target grid coordinates
        self.source = set()
        self.target = set()

        self.track_width = track_width
        self.track_widths = [self.track_width, self.track_width, 1.0]
        self.track_factor = [1 / self.track_width, 1 / self.track_width, 1.0]

        # The bounds are in grids for this
        # This is really lower left bottom layer and upper right top layer in 3D.
        self.ll = vector3d(ll.x, ll.y, 0).scale(self.track_factor).round()
        self.ur = vector3d(ur.x, ur.y, 0).scale(self.track_factor).round()
        debug.info(1, "BBOX coords: ll=" + str(ll) + " ur=" + str(ur))
        debug.info(1, "BBOX grids: ll=" + str(self.ll) + " ur=" + str(self.ur))

        # let's leave the map sparse, cells are created on demand to reduce memory
        self.map={}

    def add_all_grids(self):
        for x in range(self.ll.x, self.ur.x, 1):
            for y in range(self.ll.y, self.ur.y, 1):
                self.add_map(vector3d(x, y, 0))
                self.add_map(vector3d(x, y, 1))

    def set_blocked(self, n, value=True):
        if not isinstance(n, vector3d):
            for item in n:
                self.set_blocked(item, value)
        else:
            self.add_map(n)
            self.map[n].blocked=value

    def is_blocked(self, n):
        if not isinstance(n, vector3d):
            for item in n:
                if self.is_blocked(item):
                    return True
            else:
                return False
        else:
            self.add_map(n)
            return self.map[n].blocked

    def is_inside(self, n):
        if not isinstance(n, vector3d):
            for item in n:
                if self.is_inside(item):
                    return True
            else:
                return False
        else:
            return n.x >= self.ll.x and n.x <= self.ur.x and n.y >= self.ll.y and n.y <= self.ur.y

    def set_path(self, n, value=True):
        if isinstance(n, (list, tuple, set, frozenset)):
            for item in n:
                self.set_path(item, value)
        else:
            self.add_map(n)
            self.map[n].path=value

    def clear_blockages(self):
        for k in self.map:
            self.map[k].blocked=False

    def clear_source(self):
        for k in self.map:
            self.map[k].source=False
        self.source = set()

    def set_source(self, n):
        if not isinstance(n, vector3d):
            for item in n:
                self.set_source(item)
        else:
            self.add_map(n)
            self.map[n].source=True
            self.map[n].blocked=False
            self.source.add(n)

    def clear_target(self):
        for k in self.map:
            self.map[k].target=False
        self.target = set()

    def set_target(self, n):
        if not isinstance(n, vector3d):
            for item in n:
                self.set_target(item)
        else:
            self.add_map(n)
            self.map[n].target=True
            self.map[n].blocked=False
            self.target.add(n)

    def add_source(self, track_list):
        debug.info(3, "Adding source list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(4, "Adding source ={0}".format(str(n)))
            self.set_source(n)
            # self.set_blocked(n, False)

    def add_target(self, track_list):
        debug.info(3, "Adding target list={0}".format(str(track_list)))
        for n in track_list:
            debug.info(4, "Adding target ={0}".format(str(n)))
            self.set_target(n)
            # self.set_blocked(n, False)

    def get_perimeter_list(self, side="left", layers=[0, 1], width=1, margin=0, offset=0):
        """
        Side specifies which side.
        Layer specifies horizontal (0) or vertical (1)
        Width specifies how wide the perimeter "stripe" should be.
        Works from the inside out from the bbox (ll, ur)
        """
        if "ring" in side:
            ring_width = width
        else:
            ring_width = 0

        if "ring" in side:
            ring_offset = offset
        else:
            ring_offset = 0

        perimeter_list = []
        # Add the left/right columns
        if side=="all" or "left" in side:
            for x in range(self.ll.x - offset, self.ll.x - width - offset, -1):
                for y in range(self.ll.y - ring_offset - margin - ring_width + 1, self.ur.y + ring_offset + margin + ring_width, 1):
                    for layer in layers:
                        perimeter_list.append(vector3d(x, y, layer))

        if side=="all" or "right" in side:
            for x in range(self.ur.x + offset, self.ur.x + width + offset, 1):
                for y in range(self.ll.y - ring_offset - margin - ring_width + 1, self.ur.y + ring_offset + margin + ring_width, 1):
                    for layer in layers:
                        perimeter_list.append(vector3d(x, y, layer))

        if side=="all" or "bottom" in side:
            for y in range(self.ll.y - offset, self.ll.y - width - offset, -1):
                for x in range(self.ll.x - ring_offset - margin - ring_width + 1, self.ur.x + ring_offset + margin + ring_width, 1):
                    for layer in layers:
                        perimeter_list.append(vector3d(x, y, layer))

        if side=="all" or "top" in side:
            for y in range(self.ur.y + offset, self.ur.y + width + offset, 1):
                for x in range(self.ll.x - ring_offset - margin - ring_width + 1, self.ur.x + ring_offset + margin + ring_width, 1):
                    for layer in layers:
                        perimeter_list.append(vector3d(x, y, layer))

        # Add them all to the map
        self.add_map(perimeter_list)

        return perimeter_list

    def add_perimeter_target(self, side="all", layers=[0, 1]):
        debug.info(3, "Adding perimeter target")

        perimeter_list = self.get_perimeter_list(side, layers)

        self.set_target(perimeter_list)

    def is_target(self, point):
        """
        Point is in the target set, so we are done.
        """
        return point in self.target

    def add_map(self, n):
        """
        Add a point to the map if it doesn't exist.
        """
        if not isinstance(n, vector3d):
            for item in n:
                self.add_map(item)
        else:
            if n not in self.map:
                self.map[n]=grid_cell()

    def block_path(self, path):
        """
        Mark the path in the routing grid as blocked.
        Also unsets the path flag.
        """
        path.set_path(False)
        path.set_blocked(True)
