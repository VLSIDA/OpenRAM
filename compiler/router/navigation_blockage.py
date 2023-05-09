# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from .navigation_node import navigation_node


class navigation_blockage:
    """ This class represents a blockage on the navigation graph. """

    def __init__(self, ll, ur, layer=0):

        self.ll = ll
        self.ur = ur
        self.layer = layer


    @property
    def rect(self):
        """  """

        return self.ll, self.ur


    def create_corner_nodes(self, offset):
        """ Create nodes on all 4 corners of this blockage. """

        self.corners = []
        self.corners.append(navigation_node([self.ll[0], self.ll[1], self.layer], offset, -1, -1))
        self.corners.append(navigation_node([self.ll[0], self.ur[1], self.layer], offset, -1, 1))
        self.corners.append(navigation_node([self.ur[0], self.ll[1], self.layer], offset, 1, -1))
        self.corners.append(navigation_node([self.ur[0], self.ur[1], self.layer], offset, 1, 1))
        self.corners[0].add_neighbor(self.corners[1])
        self.corners[0].add_neighbor(self.corners[2])
        self.corners[3].add_neighbor(self.corners[1])
        self.corners[3].add_neighbor(self.corners[2])
