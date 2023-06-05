# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class grid_cell:
    """
    A single cell that can be occupied in a given layer, blocked,
    visited, etc.
    """
    def __init__(self):
        self.path = False
        self.blocked = False
        self.source = False
        self.target = False
        # -1 means it isn't visited yet
        self.min_cost = -1

    def reset(self):
        """
        Reset the dynamic info about routing.
        """
        self.min_cost=-1
        self.min_path=None
        self.blocked=False
        self.source=False
        self.target=False

    def get_cost(self):
        # We can display the cost of the frontier
        if self.min_cost > 0:
            return self.min_cost

    def get_type(self):
        type_string = ""

        if self.blocked:
            type_string += "X"

        if self.source:
            type_string += "S"

        if self.target:
            type_string += "T"

        if self.path:
            type_string += "P"

        return type_string
