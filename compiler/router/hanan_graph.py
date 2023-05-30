# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import heapq
from copy import deepcopy
from openram import debug
from openram.base.pin_layout import pin_layout
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from .direction import direction
from .hanan_node import hanan_node
from .hanan_utils import *


class hanan_graph:
    """ This is the Hanan graph created from the blockages. """

    def __init__(self, router):

        # This is the Hanan router that uses this graph
        self.router = router


    def is_on_same_layer(self, point, shape):
        """ Return if the point is on the same layer as the shape. """

        return point.z == self.router.get_zindex(shape.lpp)


    def create_graph(self, layout_source, layout_target):
        """ Create the Hanan graph to run routing on later. """
        debug.info(0, "Creating the Hanan graph for source '{0}' and target'{1}'.".format(layout_source, layout_target))

        # Find the region to be routed and only include objects inside that region
        region = deepcopy(layout_source)
        region.bbox([layout_source, layout_target])
        debug.info(0, "Routing region is {}".format(region.rect))

        # Find the blockages that are in the routing area
        self.graph_blockages = []
        for blockage in self.router.blockages:
            if region.overlaps(blockage):
                self.graph_blockages.append(blockage)
        debug.info(0, "Number of blockages detected in the routing region: {}".format(len(self.graph_blockages)))

        # Obtain the x and y values for Hanan grid
        x_values = set()
        y_values = set()
        offset = max(self.router.horiz_track_width, self.router.vert_track_width) / 2
        # Add the source and target pins first
        for shape in [layout_source, layout_target]:
            aspect_ratio = shape.width() / shape.height()
            # If the pin is tall or fat, add two points on the ends
            if aspect_ratio <= 0.5: # Tall pin
                uc = shape.uc()
                bc = shape.bc()
                points = [vector(uc.x, uc.y - offset),
                          vector(bc.x, bc.y + offset)]
            elif aspect_ratio >= 2: # Fat pin
                lc = shape.lc()
                rc = shape.rc()
                points = [vector(lc.x + offset, lc.y),
                          vector(rc.x - offset, rc.y)]
            else: # Square-like pin
                center = shape.center()
                x_values.add(center.x)
                y_values.add(center.y)
                continue
            for p in points:
                x_values.add(p.x)
                y_values.add(p.y)
        # Add corners for blockages
        for blockage in self.graph_blockages:
            ll, ur = blockage.rect
            x_values.update([ll.x - offset, ur.x + offset])
            y_values.update([ll.y - offset, ur.y + offset])

        # Sort x and y values
        x_values = list(x_values)
        y_values = list(y_values)
        x_values.sort()
        y_values.sort()

        # Generate Hanan points here (cartesian product of all x and y values)
        y_len = len(y_values)
        self.nodes = []
        for x in x_values:
            for y in y_values:
                below_node = hanan_node([x, y, 0])
                above_node = hanan_node([x, y, 1])
                # Connect these two neighbors
                below_node.add_neighbor(above_node)
                # Connect down and left nodes
                count = len(self.nodes) // 2
                if count % y_len: # Down
                    below_node.add_neighbor(self.nodes[-2])
                    above_node.add_neighbor(self.nodes[-1])
                if count >= y_len: # Left
                    below_node.add_neighbor(self.nodes[-(y_len * 2)])
                    above_node.add_neighbor(self.nodes[-(y_len * 2) + 1])
                self.nodes.append(below_node)
                self.nodes.append(above_node)

        # Remove blocked points
        for node in self.nodes.copy():
            point = node.center
            for blockage in self.graph_blockages:
                if self.is_on_same_layer(point, blockage) and is_in_region(point, blockage):
                    node.remove_all_neighbors()
                    self.nodes.remove(node)
                    break
        debug.info(0, "Number of nodes in the routing graph: {}".format(len(self.nodes)))


    def find_shortest_path(self, source, target):
        """
        Find the shortest path from the source node to target node using the
        A* algorithm.
        """

        # Find source and target nodes
        sources = []
        targets = []
        for node in self.nodes:
            if self.is_on_same_layer(node.center, source) and is_in_region(node.center, source):
                sources.append(node)
            elif self.is_on_same_layer(node.center, target) and is_in_region(node.center, target):
                targets.append(node)

        # Heuristic function to calculate the scores
        def h(node):
            """ Return the estimated distance to closest target. """
            min_dist = float("inf")
            for t in targets:
                dist = t.center.distance(node.center) + abs(t.center.z - node.center.z)
                if dist < min_dist:
                    min_dist = dist
            return min_dist

        # Initialize data structures to be used for A* search
        queue = []
        close_set = set()
        came_from = {}
        g_scores = {}
        f_scores = {}

        # Initialize score values for the source nodes
        for node in sources:
            g_scores[node.id] = 0
            f_scores[node.id] = h(node)
            heapq.heappush(queue, (f_scores[node.id], node.id, node))

        # Run the A* algorithm
        while len(queue) > 0:
            # Get the closest node from the queue
            current = heapq.heappop(queue)[2]

            # Return if already discovered
            if current in close_set:
                continue
            close_set.add(current)

            # Check if we've reached the target
            if current in targets:
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
