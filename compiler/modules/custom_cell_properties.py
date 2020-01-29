# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class _MirrorAxis:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class _Bitcell:
    def __init__(self, mirror):
        self.mirror = mirror

class CellProperties():
    """
    TODO
    """
    def __init__(self):
        self.names = {}
        self._bitcell = _Bitcell(_MirrorAxis(True, False))

    @property
    def bitcell(self):
        return self._bitcell
