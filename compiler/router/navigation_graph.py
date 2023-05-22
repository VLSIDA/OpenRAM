# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import heapq
from openram import debug
from openram.base.vector3d import vector3d
from .direction import direction
from .navigation_node import navigation_node
from .navigation_utils import *


class navigation_graph:
    """ This is the navigation graph created from the blockages. """

    def __init__(self, router):

        self.router = router


    def create_graph(self, layout_source, layout_target):
        """  """
        debug.info(0, "Creating the navigation graph for source '{0}' and target'{1}'.".format(layout_source, layout_target))

        # Find the region to be routed and only include objects inside that region
        s_ll, s_ur = layout_source.rect
        t_ll, t_ur = layout_target.rect
        region = (s_ll.min(t_ll), s_ur.min(t_ur))
        debug.info(0, "Routing region is ll: '{0}' ur: '{1}'".format(region[0], region[1]))

        # Find the blockages that are in the routing area
        self.graph_blockages = []
        for blockage in self.router.blockages:
            ll, ur = blockage.rect
            if is_in_region(ll, region) or is_in_region(ur, region):
                self.graph_blockages.append(blockage)
        debug.info(0, "Number of blockages detected in the routing region: {}".format(len(self.graph_blockages)))

        # Obtain the x and y points for Hanan grid
        x_values = []
        y_values = []
        offset = max(self.router.horiz_track_width, self.router.vert_track_width) / 2
        for shape in [layout_source, layout_target]:
            center = shape.center()
            x_values.append(center.x)
            y_values.append(center.y)
        for blockage in self.graph_blockages:
            ll, ur = blockage.rect
            x_values.extend([ll.x - offset, ur.x + offset])
            y_values.extend([ll.y - offset, ur.y + offset])

        # Generate Hanan points here (cartesian product of all x and y values)
        hanan_points = []
        for x in x_values:
            for y in y_values:
                hanan_points.append(vector3d(x, y, 0))
                hanan_points.append(vector3d(x, y, 1))

        # Remove blocked points
        for point in hanan_points.copy():
            for blockage in self.graph_blockages:
                ll, ur = blockage.rect
                if self.router.get_zindex(blockage.lpp) == point.z and is_in_region(point, blockage.rect):
                    hanan_points.remove(point)
                    break

        # Create graph nodes from Hanan points
        self.nodes = []
        for point in hanan_points:
            self.nodes.append(navigation_node(point))

        # Connect closest points avoiding blockages
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            for d in direction.cardinal_offsets():
                min_dist = float("inf")
                min_neighbor = None
                for j in range(i + 1, len(self.nodes)):
                    neighbor = self.nodes[j]
                    if node.center.z != neighbor.center.z:
                        continue
                    distance_vector = neighbor.center - node.center
                    distance = node.center.distance(neighbor.center)
                    if (distance_vector.x or (distance_vector.y * d.y <= 0)) and \
                       (distance_vector.y or (distance_vector.x * d.x <= 0)):
                        continue
                    if distance < min_dist:
                        min_dist = distance
                        min_neighbor = neighbor
                if min_neighbor:
                    node.add_neighbor(min_neighbor)

        # Connect nodes that are on top of each other
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            for j in range(i + 1, len(self.nodes)):
                neighbor = self.nodes[j]
                if node.center.x == neighbor.center.x and \
                   node.center.y == neighbor.center.y and \
                   node.center.z != neighbor.center.z:
                    node.add_neighbor(neighbor)
        debug.info(0, "Number of nodes in the routing graph: {}".format(len(self.nodes)))


    def find_shortest_path(self, source, target):
        """
        Find the shortest path from the source node to target node using the
        A* algorithm.
        """

        # Find source and target nodes
        source_center = source.center()
        source_center = vector3d(source_center.x, source_center.y, self.router.get_zindex(source.lpp))
        target_center = target.center()
        target_center = vector3d(target_center.x, target_center.y, self.router.get_zindex(target.lpp))
        for node in self.nodes:
            if node.center == source_center:
                source = node
            if node.center == target_center:
                target = node

        # Heuristic function to calculate the scores
        h = lambda node: target.center.distance(node.center) + abs(target.center.z - node.center.z)

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
                tentative_score = self.get_edge_cost(current, node) + g_scores[current.id]
                if node.id not in g_scores or tentative_score < g_scores[node.id]:
                    came_from[node.id] = current
                    g_scores[node.id] = tentative_score
                    f_scores[node.id] = tentative_score + h(node)
                    heapq.heappush(queue, (f_scores[node.id], node.id, node))

        # Return None if not connected
        return None


    def get_edge_cost(self, source, target):
        """  """

        if target in source.neighbors:
            is_vertical = source.center.x == target.center.x
            layer_dist = source.center.distance(target.center)
            if is_vertical != bool(source.center.z):
                layer_dist *= 2
            via_dist = abs(source.center.z - target.center.z) * 2
            return layer_dist + via_dist
        return float("inf")
