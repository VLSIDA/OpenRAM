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
from .navigation_node import navigation_node
from .navigation_utils import *


class navigation_graph:
    """ This is the navigation graph created from the blockages. """

    def __init__(self, router):

        self.router = router


    def is_on_same_layer(self, point, shape):
        """ Return if the point is on the same layer as the shape. """

        return point.z == self.router.get_zindex(shape.lpp)


    def create_graph(self, layout_source, layout_target):
        """ Create the Hanan graph to run routing on later. """
        debug.info(0, "Creating the navigation graph for source '{0}' and target'{1}'.".format(layout_source, layout_target))

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
        x_values = []
        y_values = []
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
                for p in points:
                    x_values.append(p.x)
                    y_values.append(p.y)
            elif aspect_ratio >= 2: # Fat pin
                lc = shape.lc()
                rc = shape.rc()
                points = [vector(lc.x + offset, lc.y),
                          vector(rc.x - offset, rc.y)]
                for p in points:
                    x_values.append(p.x)
                    y_values.append(p.y)
            else: # Square-like pin
                center = shape.center()
                x_values.append(center.x)
                y_values.append(center.y)
        # Add corners for blockages
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
                if self.is_on_same_layer(point, blockage) and is_in_region(point, blockage):
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
                    # Skip if not on the same layer
                    if node.center.z != neighbor.center.z:
                        continue
                    # Calculate the distance vector and distance value
                    distance_vector = neighbor.center - node.center
                    distance = node.center.distance(neighbor.center)
                    # Skip if not connected rectilinearly
                    if (distance_vector.x or (distance_vector.y * d.y <= 0)) and \
                       (distance_vector.y or (distance_vector.x * d.x <= 0)):
                        continue
                    # Skip if this connection is blocked by a blockage
                    if is_probe_blocked(node.center, neighbor.center, self.graph_blockages):
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
        sources = []
        for node in self.nodes:
            if self.is_on_same_layer(node.center, source) and is_in_region(node.center, source):
                sources.append(node)
        targets = []
        for node in self.nodes:
            if self.is_on_same_layer(node.center, target) and is_in_region(node.center, target):
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
