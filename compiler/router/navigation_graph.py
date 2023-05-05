# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from .navigation_node import navigation_node
from .navigation_blockage import navigation_blockage


class navigation_graph:
    """ This is the navigation graph created from the blockages. """

    def __init__(self):
        pass


    def is_probe_blocked(self, p1, p2):
        """
        Return if a probe sent from p1 to p2 encounters a blockage.
        The probe must be sent vertically or horizontally.
        This method assumes that blockages are rectangular.
        """

        # Check if any blockage blocks this probe
        for blockage in self.nav_blockages:
            right_x = blockage.ur[0]
            upper_y = blockage.ur[1]
            left_x = blockage.ll[0]
            lower_y = blockage.ll[1]
            # Check if blocked vertically
            if is_between(left_x, right_x, p1.x) and (is_between(p1.y, p2.y, upper_y) or is_between(p1.y, p2.y, lower_y)):
                return True
            # Check if blocked horizontally
            if is_between(upper_y, lower_y, p1.y) and (is_between(p1.x, p2.x, left_x) or is_between(p1.x, p2.x, right_x)):
                return True
        return False


    def create_graph(self, layout_source, layout_target, layout_blockages):
        """  """
        debug.info(0, "Creating the navigation graph for source '{0}' and target'{1}'.".format(layout_source, layout_target))

        # Find the region to be routed and only include objects inside that region
        s_ll, sou_ur = layout_source.rect
        t_ll, tar_ur = layout_target.rect
        ll = vector(min(s_ll.x, t_ll.x), max(s_ll.y, t_ll.y))
        ur = vector(max(sou_ur.x, tar_ur.x), min(sou_ur.y, tar_ur.y))
        region = (ll, ur)

        # Instantiate "navigation blockage" objects from layout blockages
        self.nav_blockages = []
        for layout_blockage in layout_blockages:
            ll, ur = layout_blockage.rect
            if (is_between(region[0].x, region[1].x, ll.x) and is_between(region[0].y, region[1].y, ll.y)) or \
               (is_between(region[0].x, region[1].x, ur.x) and is_between(region[0].y, region[1].y, ur.y)):
                self.nav_blockages.append(navigation_blockage(ll, ur))

        self.nodes = []

        # Add source and target for this graph
        self.nodes.append(navigation_node(layout_source.center()))
        self.nodes.append(navigation_node(layout_target.center()))

        # Create the corner nodes
        for blockage in self.nav_blockages:
            self.nodes.extend(blockage.create_corner_nodes())

        # Create intersection nodes
        # NOTE: Intersection nodes are used to connect boundaries of blockages
        # perpendicularly.
        new_nodes = []
        debug.info(0, "Number of blockages: {}".format(len(self.nav_blockages)))
        debug.info(0, "Number of nodes: {}".format(len(self.nodes)))
        for i in range(len(self.nodes)):
            debug.info(3, "Creating intersections for node #{}".format(i))
            node1 = self.nodes[i]
            for j in range(i + 1, len(self.nodes)):
                node2 = self.nodes[j]
                # Skip if the nodes are already connected
                if node1 in node2.neighbors:
                    continue
                # Try two different corners
                for k in [0, 1]:
                    # Create a node at the perpendicular corner of these two nodes
                    corner = navigation_node(vector(node1.position[k], node2.position[int(not k)]))
                    # Skip this corner if the perpendicular connection is blocked
                    if self.is_probe_blocked(corner.position, node1.position) or self.is_probe_blocked(corner.position, node2.position):
                        continue
                    corner.add_neighbor(node1)
                    corner.add_neighbor(node2)
                    new_nodes.append(corner)
        self.nodes.extend(new_nodes)
        debug.info(0, "Number of nodes after intersections: {}".format(len(self.nodes)))


def is_between(a, b, mid):
    """ Return if 'mid' is between 'a' and 'b'. """

    return (a < mid and mid < b) or (b < mid and mid < a)
