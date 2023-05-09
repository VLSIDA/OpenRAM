# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.base.vector import vector
from openram.base.vector3d import vector3d


class navigation_node:
    """ This class represents a node on the navigation graph. """

    # This is used to assign unique ids to nodes
    next_id = 0

    def __init__(self, center, offset=None, horizontal=1, vertical=1):

        self.id = navigation_node.next_id
        navigation_node.next_id += 1
        if isinstance(center, vector):
            self.center = vector3d(center[0], center[1], 0)
        elif isinstance(center, vector3d):
            self.center = center
        else:
            self.center = vector3d(center)
        if offset:
            self.center += vector3d(offset * horizontal, offset * vertical, 0)
        self.neighbors = []


    def add_neighbor(self, node):
        """ Connect two nodes. """

        self.neighbors.append(node)
        node.neighbors.append(self)


    def remove_neighbor(self, node):
        """ Disconnect two nodes. """

        if node in self.neighbors:
            self.neighbors.remove(node)
            node.neighbors.remove(self)


    def get_edge_cost(self, node):
        """ Return the cost of going to node. """

        if node in self.neighbors:
            return self.center.distance(node.center)
        else:
            return float("inf")
