# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.vector import vector
from openram.base.vector3d import vector3d


class hanan_node:
    """ This class represents a node on the Hanan graph. """

    # This is used to assign unique ids to nodes
    next_id = 0

    def __init__(self, center):

        self.id = hanan_node.next_id
        hanan_node.next_id += 1
        if isinstance(center, vector3d):
            self.center = center
        else:
            self.center = vector3d(center)
        self.neighbors = []


    def __lt__(self, other):
        """ Override the default less than behavior. """

        return self.center < other.center


    def add_neighbor(self, other):
        """ Connect two nodes. """

        if other not in self.neighbors:
            self.neighbors.append(other)
            other.neighbors.append(self)


    def remove_neighbor(self, other):
        """ Disconnect two nodes. """

        if other in self.neighbors:
            self.neighbors.remove(other)
            other.neighbors.remove(self)


    def get_edge_cost(self, other):
        """ Get the cost of going from this node to the other node. """

        if other in self.neighbors:
            is_vertical = self.center.x == other.center.x
            layer_dist = self.center.distance(other.center)
            if is_vertical != bool(self.center.z):
                layer_dist *= 2
            via_dist = abs(self.center.z - other.center.z) * 2
            return layer_dist + via_dist
        return float("inf")
