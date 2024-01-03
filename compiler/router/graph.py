# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import heapq
from copy import deepcopy
from openram import debug
from openram.base.vector import vector
from openram.tech import drc
from .bbox import bbox
from .bbox_node import bbox_node
from .graph_node import graph_node
from .graph_probe import graph_probe
from .graph_utils import snap


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


    def get_safe_pin_values(self, pin):
        """ Get the safe x and y values of the given pin. """

        # Constant values
        pin = pin.get_core()
        offset = self.router.half_wire
        spacing = self.router.track_space
        size_limit = snap(offset * 4 + spacing)

        x_values = []
        y_values = []
        # If one axis size of the pin is greater than the limit, we will take
        # two points at both ends. Otherwise, we will only take the center of
        # this pin.
        if pin.width() > size_limit:
            x_values.append(snap(pin.lx() + offset))
            x_values.append(snap(pin.rx() - offset))
        else:
            x_values.append(snap(pin.cx()))
        if pin.height() > size_limit:
            y_values.append(snap(pin.by() + offset))
            y_values.append(snap(pin.uy() - offset))
        else:
            y_values.append(snap(pin.cy()))

        return x_values, y_values


    def is_probe_blocked(self, p1, p2):
        """
        Return if a probe sent from p1 to p2 encounters a blockage.
        The probe must be sent vertically or horizontally.
        This function assumes that p1 and p2 are on the same layer.
        """

        probe_shape = graph_probe(p1, p2, self.router.get_lpp(p1.z))
        pll, pur = probe_shape.rect
        # Check if any blockage blocks this probe
        for blockage in self.blockage_bbox_tree.iterate_shape(probe_shape):
            bll, bur = blockage.rect
            # Not on the same layer
            if not blockage.same_lpp(blockage.lpp, probe_shape.lpp):
                continue
            # Probe is blocked if the shape isn't routable
            if not self.is_routable(blockage):
                return True
            blockage = blockage.get_core()
            bll, bur = blockage.rect
            # Not overlapping
            if bll.x > pur.x or pll.x > bur.x or bll.y > pur.y or pll.y > bur.y:
                return True
        return False


    def is_node_blocked(self, node):
        """ Return if a node is blocked by a blockage. """

        p = node.center
        x = p.x
        y = p.y
        z = p.z

        def closest(value, checklist):
            """ Return the distance of the closest value in the checklist. """
            diffs = [abs(value - other) for other in checklist]
            return snap(min(diffs))

        wide = self.router.track_wire
        half_wide = self.router.half_wire
        spacing = snap(self.router.track_space + half_wide + drc["grid"])
        blocked = False
        for blockage in self.blockage_bbox_tree.iterate_point(p):
            ll, ur = blockage.rect
            # Not on the same layer
            if self.router.get_zindex(blockage.lpp) != z:
                continue
            # Blocked if not routable
            if not self.is_routable(blockage):
                blocked = True
                continue
            blockage = blockage.get_core()
            ll, ur = blockage.rect
            # Not overlapping
            if ll.x > x or x > ur.x or ll.y > y or y > ur.y:
                blocked = True
                continue
            # Check if the node is too close to one edge of the shape
            lengths = [blockage.width(), blockage.height()]
            centers = blockage.center()
            ll, ur = blockage.rect
            safe = [True, True]
            for i in range(2):
                if lengths[i] >= wide:
                    min_diff = closest(p[i], [ll[i], ur[i]])
                    if min_diff < half_wide:
                        safe[i] = False
                elif centers[i] != p[i]:
                    safe[i] = False
            if not all(safe):
                blocked = True
                continue
            # Check if the node is in a safe region of the shape
            xs, ys = self.get_safe_pin_values(blockage)
            xdiff = closest(p.x, xs)
            ydiff = closest(p.y, ys)
            if xdiff == 0 and ydiff == 0:
                if blockage in [self.source, self.target]:
                    return False
            elif xdiff < spacing and ydiff < spacing:
                blocked = True
        return blocked


    def is_via_blocked(self, nodes):
        """ Return if a via on the given point is blocked by another via. """

        # If the nodes are blocked by a blockage other than a via
        for node in nodes:
            if self.is_node_blocked(node):
                return True

        # Skip if no via is present
        if len(self.graph_vias) == 0:
            return False

        # If the nodes are blocked by a via
        x = node.center.x
        y = node.center.y
        z = node.center.z
        for via in self.via_bbox_tree.iterate_point(node.center):
            ll, ur = via.rect
            # Not overlapping
            if ll.x > x or x > ur.x or ll.y > y or y > ur.y:
                continue
            center = via.center()
            # If not in the center
            if center.x != x or center.y != y:
                return True
        return False


    def create_graph(self, source, target):
        """ Create the graph to run routing on later. """
        debug.info(3, "Creating the graph for source '{}' and target'{}'.".format(source, target))

        # Save source and target information
        self.source = source
        self.target = target

        # Find the region to be routed and only include objects inside that region
        region = deepcopy(source)
        region.bbox([target])
        region = region.inflated_pin(spacing=self.router.track_width + self.router.track_space)
        debug.info(4, "Routing region is {}".format(region.rect))

        # Find the blockages that are in the routing area
        self.graph_blockages = []
        self.find_graph_blockages(region)

        # Find the vias that are in the routing area
        self.graph_vias = []
        self.find_graph_vias(region)

        # Generate the cartesian values from shapes in the area
        x_values, y_values = self.generate_cartesian_values()
        # Adjust the routing region to include "edge" shapes
        region.bbox(self.graph_blockages)
        # Find and include edge shapes to prevent DRC errors
        self.find_graph_blockages(region)
        # Build the bbox tree
        self.build_bbox_trees()
        # Generate the graph nodes from cartesian values
        self.generate_graph_nodes(x_values, y_values)
        # Save the graph nodes that lie in source and target shapes
        self.save_end_nodes()
        debug.info(4, "Number of blockages detected in the routing region: {}".format(len(self.graph_blockages)))
        debug.info(4, "Number of vias detected in the routing region: {}".format(len(self.graph_vias)))
        debug.info(4, "Number of nodes in the routing graph: {}".format(len(self.nodes)))


    def find_graph_blockages(self, region):
        """ Find blockages that overlap the routing region. """

        for blockage in self.router.blockages:
            # Skip if already included
            if blockage in self.graph_blockages:
                continue
            # Set the region's lpp to current blockage's lpp so that the
            # overlaps method works
            region.lpp = blockage.lpp
            if region.overlaps(blockage):
                self.graph_blockages.append(blockage)
        # Make sure that the source or target fake pins are included as blockage
        for shape in [self.source, self.target]:
            for blockage in self.graph_blockages:
                blockage = blockage.get_core()
                if shape == blockage:
                    break
            else:
                self.graph_blockages.append(shape)


    def find_graph_vias(self, region):
        """ Find vias that overlap the routing region. """

        for via in self.router.vias:
            # Skip if already included
            if via in self.graph_vias:
                continue
            # Set the regions's lpp to current via's lpp so that the
            # overlaps method works
            region.lpp = via.lpp
            if region.overlaps(via):
                self.graph_vias.append(via)


    def build_bbox_trees(self):
        """ Build bbox trees for blockages and vias in the routing region. """

        # Bbox tree for blockages
        self.blockage_bbox_tree = bbox_node(bbox(self.graph_blockages[0]))
        for i in range(1, len(self.graph_blockages)):
            self.blockage_bbox_tree.insert(bbox(self.graph_blockages[i]))
        # Bbox tree for vias
        if len(self.graph_vias) == 0:
            return
        self.via_bbox_tree = bbox_node(bbox(self.graph_vias[0]))
        for i in range(1, len(self.graph_vias)):
            self.via_bbox_tree.insert(bbox(self.graph_vias[i]))


    def generate_cartesian_values(self):
        """
        Generate x and y values from all the corners of the shapes in the
        routing region.
        """

        x_values = set()
        y_values = set()

        # Add inner values for blockages of the routed type
        for shape in self.graph_blockages:
            if not self.is_routable(shape):
                continue
            # Get the safe pin values
            xs, ys = self.get_safe_pin_values(shape)
            x_values.update(xs)
            y_values.update(ys)

        # Add corners for blockages
        offset = vector([drc["grid"]] * 2)
        for blockage in self.graph_blockages:
            ll, ur = blockage.rect
            # Add minimum offset to the blockage corner nodes to prevent overlap
            nll = snap(ll - offset)
            nur = snap(ur + offset)
            x_values.update([nll.x, nur.x])
            y_values.update([nll.y, nur.y])

        # Add center values for existing vias
        for via in self.graph_vias:
            p = via.center()
            x_values.add(p.x)
            y_values.add(p.y)

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
            found = [base_nodes[0].remove,
                     base_nodes[1].remove]
            while condition(index) and not all(found):
                nodes = self.nodes[index - shift:index - shift + 2]
                for k in range(2):
                    if not found[k] and not nodes[k].remove:
                        found[k] = True
                        if not self.is_probe_blocked(base_nodes[k].center, nodes[k].center):
                            base_nodes[k].add_neighbor(nodes[k])
                index -= shift
        y_len = len(y_values)
        for i in range(0, len(self.nodes), 2):
            search(i, lambda count: (count / 2) % y_len, 2) # Down
            search(i, lambda count: (count / 2) >= y_len, y_len * 2) # Left
            if not self.nodes[i].remove and \
               not self.nodes[i + 1].remove and \
               not self.is_via_blocked(self.nodes[i:i+2]):
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
            if node.remove:
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
                path.reverse()
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
