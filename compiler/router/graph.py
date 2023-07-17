# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import heapq
from copy import deepcopy
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.tech import drc
from .direction import direction
from .graph_node import graph_node
from .graph_probe import graph_probe


class graph:
    """ This is the graph created from the blockages. """

    def __init__(self, router):

        # This is the graph router that uses this graph
        self.router = router
        self.source_nodes = []
        self.target_nodes = []


    def is_routable(self, shape):
        """ Return if a shape is routable in this graph. """

        return shape.name == self.source.name


    def inside_shape(self, point, shape):
        """ Return if the point is inside the shape. """

        # Check if they're on the same layer
        if point.z != self.router.get_zindex(shape.lpp):
            return False
        # Check if the point is inside the shape
        ll, ur = shape.rect
        return shape.on_segment(ll, point, ur)


    def is_probe_blocked(self, p1, p2):
        """
        Return if a probe sent from p1 to p2 encounters a blockage.
        The probe must be sent vertically or horizontally.
        This function assumes that p1 and p2 are on the same layer.
        """

        probe_shape = graph_probe(p1, p2, self.router.vert_lpp if p1.z else self.router.horiz_lpp)
        # Check if any blockage blocks this probe
        for blockage in self.graph_blockages:
            # Check if two shapes overlap
            if blockage.overlaps(probe_shape):
                # Probe is blocked if the shape isn't routable
                if not self.is_routable(blockage):
                    return True
                elif blockage.inflated_from is None:
                    continue
                elif blockage.inflated_from.overlaps(probe_shape):
                    continue
                else:
                    return True
        return False


    def is_node_blocked(self, node):
        """ Return if a node is blocked by a blockage. """

        for blockage in self.graph_blockages:
            # Check if two shapes overlap
            if self.inside_shape(node.center, blockage):
                if not self.is_routable(blockage):
                    return True
                elif blockage.inflated_from is None:
                    return False
                elif self.inside_shape(node.center, blockage.inflated_from):
                    return False
                else:
                    return True
        return False


    def is_via_blocked(self, point):
        """ Return if a via on the given point is blocked by another via. """

        for via in self.graph_vias:
            ll, ur = via.rect
            center = via.center()
            if via.on_segment(ll, point, ur) and \
               (center.x != point.x or center.y != point.y):
                return True
        return False


    def create_graph(self, source, target):
        """ Create the graph to run routing on later. """
        debug.info(2, "Creating the graph for source '{}' and target'{}'.".format(source, target))

        # Save source and target information
        self.source = source
        self.target = target

        # Find the region to be routed and only include objects inside that region
        region = deepcopy(source)
        region.bbox([target])
        region = region.inflated_pin(spacing=self.router.track_space,
                                     multiple=1)
        debug.info(3, "Routing region is {}".format(region.rect))

        # Find the blockages that are in the routing area
        self.graph_blockages = []
        for blockage in self.router.blockages:
            # Set the region's lpp to current blockage's lpp so that the
            # overlaps method works
            region.lpp = blockage.lpp
            if region.overlaps(blockage):
                self.graph_blockages.append(blockage)
        for shape in [source, target]:
            if shape not in self.graph_blockages:
                self.graph_blockages.append(shape)

        # Find the vias that are in the routing area
        self.graph_vias = []
        for via in self.router.vias:
            # Set the regions's lpp to current via's lpp so that the
            # overlaps method works
            region.lpp = via.lpp
            if region.overlaps(via):
                self.graph_vias.append(via)
        debug.info(3, "Number of blockages detected in the routing region: {}".format(len(self.graph_blockages)))
        debug.info(3, "Number of vias detected in the routing region: {}".format(len(self.graph_vias)))

        # Create the graph
        x_values, y_values = self.generate_cartesian_values()
        self.generate_graph_nodes(x_values, y_values)
        self.save_end_nodes()
        debug.info(3, "Number of nodes in the routing graph: {}".format(len(self.nodes)))


    def generate_cartesian_values(self):
        """
        Generate x and y values from all the corners of the shapes in the
        routing region.
        """

        x_values = set()
        y_values = set()

        # Add inner values for blockages of the routed type
        x_offset = vector(self.router.offset, 0)
        y_offset = vector(0, self.router.offset)
        for shape in self.graph_blockages:
            if not self.is_routable(shape):
                continue
            aspect_ratio = shape.width() / shape.height()
            # FIXME: Aspect ratio may not be the best way to determine this
            # If the pin is tall or fat, add two points on the ends
            if aspect_ratio <= 0.5: # Tall pin
                points = [shape.bc() + y_offset, shape.uc() - y_offset]
            elif aspect_ratio >= 2: # Fat pin
                points = [shape.lc() + x_offset, shape.rc() - x_offset]
            else: # Square-like pin
                points = [shape.center()]
            for p in points:
                x_values.add(p.x)
                y_values.add(p.y)

        # Add corners for blockages
        offset = drc["grid"]
        for blockage in self.graph_blockages:
            ll, ur = blockage.rect
            # Add minimum offset to the blockage corner nodes to prevent overlap
            x_values.update([ll.x - offset, ur.x + offset])
            y_values.update([ll.y - offset, ur.y + offset])

        # Sort x and y values
        x_values = list(x_values)
        y_values = list(y_values)
        x_values.sort()
        y_values.sort()

        return x_values, y_values


    def generate_graph_nodes(self, x_values, y_values):
        """
        Generate all graph nodes using the cartesian values and connect the
        orthogonal neighbors.
        """

        # Generate all nodes
        self.nodes = []
        for x in x_values:
            for y in y_values:
                for z in [0, 1]:
                    self.nodes.append(graph_node([x, y, z]))

        # Mark nodes that will be removed
        self.mark_blocked_nodes()

        # Connect closest nodes that won't be removed
        def search(index, condition, shift):
            """ Search and connect neighbor nodes. """
            base_nodes = self.nodes[index:index+2]
            found = [hasattr(base_nodes[0], "remove"),
                     hasattr(base_nodes[1], "remove")]
            while condition(index) and not all(found):
                nodes = self.nodes[index - shift:index - shift + 2]
                for k in range(2):
                    if not found[k] and not hasattr(nodes[k], "remove"):
                        found[k] = True
                        if not self.is_probe_blocked(base_nodes[k].center, nodes[k].center):
                            base_nodes[k].add_neighbor(nodes[k])
                index -= shift
        y_len = len(y_values)
        for i in range(0, len(self.nodes), 2):
            search(i, lambda count: (count / 2) % y_len, 2) # Down
            search(i, lambda count: (count / 2) >= y_len, y_len * 2) # Left
            if not hasattr(self.nodes[i], "remove") and \
               not hasattr(self.nodes[i + 1], "remove") and \
               not self.is_via_blocked(self.nodes[i].center):
                self.nodes[i].add_neighbor(self.nodes[i + 1])

        # Remove marked nodes
        self.remove_blocked_nodes()


    def mark_blocked_nodes(self):
        """ Mark graph nodes to be removed that are blocked by a blockage. """

        for i in range(len(self.nodes) - 1, -1, -1):
            node = self.nodes[i]
            if self.is_node_blocked(node):
                node.remove = True


    def remove_blocked_nodes(self):
        """ Remove graph nodes that are marked to be removed. """

        for i in range(len(self.nodes) - 1, -1, -1):
            node = self.nodes[i]
            if hasattr(node, "remove"):
                node.remove_all_neighbors()
                self.nodes.remove(node)


    def save_end_nodes(self):
        """ Save graph nodes that are inside source and target pins. """

        for node in self.nodes:
            if self.inside_shape(node.center, self.source):
                self.source_nodes.append(node)
            elif self.inside_shape(node.center, self.target):
                self.target_nodes.append(node)


    def find_shortest_path(self):
        """
        Find the shortest path from the source node to target node using the
        A* algorithm.
        """

        # Heuristic function to calculate the scores
        def h(node):
            """ Return the estimated distance to the closest target. """
            min_dist = float("inf")
            for t in self.target_nodes:
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
        for node in self.source_nodes:
            g_scores[node.id] = 0
            f_scores[node.id] = h(node)
            heapq.heappush(queue, (f_scores[node.id], node.id, node))

        # Run the A* algorithm
        while len(queue) > 0:
            # Get the closest node from the queue
            current = heapq.heappop(queue)[2]

            # Skip this node if already discovered
            if current in close_set:
                continue
            close_set.add(current)

            # Check if we've reached the target
            if current in self.target_nodes:
                path = []
                while current.id in came_from:
                    path.append(current)
                    current = came_from[current.id]
                path.append(current)
                return path

            # Get the previous node to better calculate the next costs
            prev_node = None
            if current.id in came_from:
                prev_node = came_from[current.id]

            # Update neighbor scores
            for node in current.neighbors:
                tentative_score = current.get_edge_cost(node, prev_node) + g_scores[current.id]
                if node.id not in g_scores or tentative_score < g_scores[node.id]:
                    came_from[node.id] = current
                    g_scores[node.id] = tentative_score
                    f_scores[node.id] = tentative_score + h(node)
                    heapq.heappush(queue, (f_scores[node.id], node.id, node))

        # Return None if not connected
        return None
