# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#

class navigation_node:
    """ This class represents a node on the navigation graph. """

    def __init__(self, position):

        self.position = position
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
