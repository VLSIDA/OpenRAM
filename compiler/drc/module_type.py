# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class module_type():
    """
    This is a class that maps cell names to python classes implementing them.
    """
    def __init__(self):
        self.names = {}

    def __setitem__(self, b, c):
        self.names[b] = c

    def is_overridden(self, b):
        return (b in self.names.keys())

    def __getitem__(self, b):
        if b not in self.names.keys():
            raise KeyError

        return self.names[b]
