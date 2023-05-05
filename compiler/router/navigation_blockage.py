# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.vector import vector
from .navigation_node import navigation_node


class navigation_blockage:
    """ This class represents a blockage on the navigation graph. """

    def __init__(self, ll, ur):

        self.ll = ll
        self.ur = ur


    def create_corner_nodes(self):
        """ Create nodes on all 4 corners of this blockage. """

        corners = []
        corners.append(navigation_node(vector(self.ll[0], self.ll[1])))
        corners.append(navigation_node(vector(self.ll[0], self.ur[1])))
        corners.append(navigation_node(vector(self.ur[0], self.ll[1])))
        corners.append(navigation_node(vector(self.ur[0], self.ur[1])))
        corners[0].add_neighbor(corners[1])
        corners[0].add_neighbor(corners[2])
        corners[3].add_neighbor(corners[1])
        corners[3].add_neighbor(corners[2])
        return corners
