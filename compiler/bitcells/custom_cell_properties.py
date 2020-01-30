# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _mirror_axis:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class _bitcell:
    def __init__(self, mirror, split_wl):
        self.mirror = mirror
        self.split_wl = split_wl

class cell_properties():
    """
    TODO
    """
    def __init__(self):
        self.names = {}
        self._bitcell = _bitcell(mirror = _mirror_axis(True, False),
                                 split_wl = False)

    @property
    def bitcell(self):
        return self._bitcell
