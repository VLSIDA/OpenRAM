# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import heapq
from openram import debug
from .navigation_node import navigation_node
from .navigation_blockage import navigation_blockage


class navigation_graph:
    """ This is the navigation graph created from the blockages. """

    def __init__(self, track_width):

        self.track_width = track_width


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
        s_ll, s_ur = layout_source.rect
        t_ll, t_ur = layout_target.rect
        region = (s_ll.min(t_ll), s_ur.min(t_ur))
        debug.info(0, "Routing region is ll: '{0}' ur: '{1}'".format(region[0], region[1]))

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
            blockage.create_corner_nodes(self.track_width / 2)

        # These nodes will be connected to create the final graph
        connect_objs = []
        connect_objs.extend(self.nodes)
        connect_objs.extend(self.nav_blockages)

        # Create intersection nodes
        # NOTE: Intersection nodes are used to connect boundaries of blockages
        # perpendicularly.
        debug.info(0, "Number of objects: {}".format(len(connect_objs)))
        for i in range(len(connect_objs)):
            obj1 = connect_objs[i]
            for j in range(i + 1, len(connect_objs)):
                obj2 = connect_objs[j]
                node1, node2 = get_closest_nodes(obj1, obj2)
                # Try two different corners
                for k in [0, 1]:
                    # Create a node at the perpendicular corner of these two nodes
                    x_node = node1 if k else node2
                    y_node = node2 if k else node1
                    corner = navigation_node([x_node.center[0], y_node.center[1], 0])
                    # Skip this corner if the perpendicular connection is blocked
                    if self.is_probe_blocked(corner.center, node1.center) or self.is_probe_blocked(corner.center, node2.center):
                        continue
                    # Check if this new node stands on an existing connection
                    self.remove_intersected_neighbors(node1, corner, k)
                    self.remove_intersected_neighbors(node2, corner, not(k))
                    # Add this new node to the graph
                    corner.add_neighbor(node1)
                    corner.add_neighbor(node2)
                    self.nodes.append(corner)

        # Add corner nodes from blockages after intersections
        for blockage in self.nav_blockages:
            self.nodes.extend(blockage.corners)
        debug.info(0, "Number of nodes after corners: {}".format(len(self.nodes)))


    def remove_intersected_neighbors(self, node, corner, axis):
        """  """

        a = node.center
        mid = corner.center
        for neighbor in node.neighbors:
            b = neighbor.center
            if a[not(axis)] == b[not(axis)] and is_between(a[axis], b[axis], mid[axis]):
                neighbor.remove_neighbor(node)
                neighbor.add_neighbor(corner)


    def find_shortest_path(self, source, target):
        """
        Find the shortest path from the source node to target node using the
        A* algorithm.
        """

        source = self.nodes[0]
        target = self.nodes[1]

        # Heuristic function to calculate the scores
        h = lambda node: target.center.distance(node.center)

        queue = []
        close_set = set()
        came_from = {}
        g_scores = {}
        f_scores = {}

        # Initialize score values for the source node
        g_scores[source.id] = 0
        f_scores[source.id] = h(source)

        heapq.heappush(queue, (f_scores[source.id], source.id, source))

        # Run the A* algorithm
        while len(queue) > 0:
            # Get the closest node from the queue
            current = heapq.heappop(queue)[2]

            # Return if already discovered
            if current in close_set:
                continue
            close_set.add(current)

            # Check if we've reached the target
            if current == target:
                path = []
                while current.id in came_from:
                    path.append(current)
                    current = came_from[current.id]
                path.append(current)
                return path

            # Update neighbor scores
            for node in current.neighbors:
                tentative_score = current.get_edge_cost(node) + g_scores[current.id]
                if node.id not in g_scores or tentative_score < g_scores[node.id]:
                    came_from[node.id] = current
                    g_scores[node.id] = tentative_score
                    f_scores[node.id] = tentative_score + h(node)
                    heapq.heappush(queue, (f_scores[node.id], node.id, node))

        # Return None if not connected
        return None


def is_between(a, b, mid):
    """ Return if 'mid' is between 'a' and 'b'. """

    return (a < mid and mid < b) or (b < mid and mid < a)


def get_closest_nodes(a, b):
    """  """

    if isinstance(a, navigation_node) and isinstance(b, navigation_node):
        return a, b
    if isinstance(a, navigation_blockage) and isinstance(b, navigation_blockage):
        min_dist = float("inf")
        min_a = None
        min_b = None
        for node_a in a.corners:
            for node_b in b.corners:
                dist = node_a.center.distance(node_b.center)
                if dist < min_dist:
                    min_dist = dist
                    min_a = node_a
                    min_b = node_b
        return min_a, min_b
    if isinstance(a, navigation_node):
        min_dist = float("inf")
        min_a = None
        min_b = None
        for node_b in b.corners:
            dist = a.center.distance(node_b.center)
            if dist < min_dist:
                min_dist = dist
                min_a = a
                min_b = node_b
        return min_a, min_b
    if isinstance(b, navigation_node):
        min_dist = float("inf")
        min_a = None
        min_b = None
        for node_a in a.corners:
            dist = b.center.distance(node_a.center)
            if dist < min_dist:
                min_dist = dist
                min_a = node_a
                min_b = b
        return min_a, min_b
