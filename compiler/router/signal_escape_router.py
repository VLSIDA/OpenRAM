# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram import OPTS
from .graph import graph
from .graph_shape import graph_shape
from .router import router


class signal_escape_router(router):
    """
    This is the signal escape router that uses the Hanan grid graph method.
    """

    def __init__(self, layers, design, bbox=None):

        # `router` is the base router class
        router.__init__(self, layers, design, bbox)

        # New pins are the side supply pins
        self.new_pins = {}


    def route(self, pin_names):
        """ Route the given pins to the perimeter. """
        debug.info(1, "Running signal escape router...")

        # Prepare gdsMill to find pins and blockages
        self.prepare_gds_reader()

        # Find pins to be routed
        for name in pin_names:
            self.find_pins(name)

        # Find blockages and vias
        self.find_blockages()
        self.find_vias()

        # Convert blockages and vias if they overlap a pin
        self.convert_vias()
        self.convert_blockages()

        # Add fake pins on the perimeter to do the escape routing on
        self.add_perimeter_fake_pins()

        # Add vdd and gnd pins as blockages as well
        # NOTE: This is done to make vdd and gnd pins DRC-safe
        for pin in self.all_pins:
            self.blockages.append(self.inflate_shape(pin))

        # Route vdd and gnd
        routed_count = 0
        routed_max = len(pin_names)
        for source, target, _ in self.get_route_pairs(pin_names):
            # Change fake pin's name so the graph will treat it as routable
            target.name = source.name
            # Create the graph
            g = graph(self)
            g.create_graph(source, target)
            # Find the shortest path from source to target
            path = g.find_shortest_path()
            # If no path is found, throw an error
            if path is None:
                self.write_debug_gds(gds_name="{}error.gds".format(OPTS.openram_temp), g=g, source=source, target=target)
                debug.error("Couldn't route from {} to {}.".format(source, target), -1)
            # Create the path shapes on layout
            new_wires, new_vias = self.add_path(path)
            self.new_pins[source.name] = new_wires[-1]
            # Find the recently added shapes
            self.find_blockages(name, new_wires)
            self.find_vias(new_vias)
            routed_count += 1
            debug.info(2, "Routed {} of {} signal pins".format(routed_count, routed_max))
        self.replace_layout_pins()


    def get_closest_edge(self, point):
        """ Return a point's the closest edge and the edge's axis direction. """

        ll, ur = self.bbox

        # Snap the pin to the perimeter and break the iteration
        ll_diff_x = abs(point.x - ll.x)
        ll_diff_y = abs(point.y - ll.y)
        ur_diff_x = abs(point.x - ur.x)
        ur_diff_y = abs(point.y - ur.y)
        min_diff = min(ll_diff_x, ll_diff_y, ur_diff_x, ur_diff_y)

        if min_diff == ll_diff_x:
            return "left", True
        if min_diff == ll_diff_y:
            return "bottom", False
        if min_diff == ur_diff_x:
            return "right", True
        return "top", False


    def prepare_path(self, path):
        """
        Override the `prepare_path` method from the `router` class to prevent
        overflows from the SRAM layout area.
        """

        ll, ur = self.bbox
        nodes = super().prepare_path(path)
        new_nodes = []
        for i in range(len(nodes)):
            node = nodes[i]
            c = node.center
            # Haven't overflown yet
            if ll.x < c.x and c.x < ur.x and ll.y < c.y and c.y < ur.y:
                new_nodes.append(node)
                continue
            # Snap the pin to the perimeter and break the iteration
            edge, _ = self.get_closest_edge(c)
            if edge == "left":
                fake_center = vector3d(ll.x + self.half_wire, c.y, c.z)
            if edge == "bottom":
                fake_center = vector3d(c.x, ll.y + self.half_wire, c.z)
            if edge == "right":
                fake_center = vector3d(ur.x - self.half_wire, c.y, c.z)
            if edge == "top":
                fake_center = vector3d(c.x, ur.y - self.half_wire, c.z)
            node.center = fake_center
            new_nodes.append(node)
            break
        return new_nodes


    def add_perimeter_fake_pins(self):
        """
        Add the fake pins on the perimeter to where the signals will be routed.
        These perimeter fake pins are only used to replace layout pins at the
        end of routing.
        """

        ll, ur = self.bbox
        wide = self.track_wire

        for side in ["top", "bottom", "left", "right"]:
            vertical = side in ["left", "right"]

            # Calculate the lower left coordinate
            if side == "top":
                offset = vector(ll.x, ur.y - wide)
            elif side == "bottom":
                offset = vector(ll.x, ll.y)
            elif side == "left":
                offset = vector(ll.x, ll.y)
            elif side == "right":
                offset = vector(ur.x - wide, ll.y)

            # Calculate width and height
            shape = ur - ll
            if vertical:
                shape_width = wide
                shape_height = shape.y
            else:
                shape_width = shape.x
                shape_height = wide

            # Add this new pin
            # They must lie on the non-preferred direction since the side supply
            # pins will lie on the preferred direction
            layer = self.get_layer(int(not vertical))
            nll = vector(offset.x, offset.y)
            nur = vector(offset.x + shape_width, offset.y + shape_height)
            rect = [nll, nur]
            pin = graph_shape(name="fake",
                              rect=rect,
                              layer_name_pp=layer)
            self.fake_pins.append(pin)


    def create_fake_pin(self, pin):
        """ Create a fake pin on the perimeter orthogonal to the given pin. """

        ll, ur = self.bbox
        c = pin.center()

        # Find the closest edge
        edge, vertical = self.get_closest_edge(c)

        # Keep the fake pin out of the SRAM layout are so that they won't be
        # blocked by previous signals if they're on the same orthogonal line
        if edge == "left":
            fake_center = vector(ll.x - self.track_wire * 2, c.y)
        if edge == "bottom":
            fake_center = vector(c.x, ll.y - self.track_wire * 2)
        if edge == "right":
            fake_center = vector(ur.x + self.track_wire * 2, c.y)
        if edge == "top":
            fake_center = vector(c.x, ur.y + self.track_wire * 2)

        # Create the fake pin shape
        layer = self.get_layer(int(not vertical))
        half_wire_vector = vector([self.half_wire] * 2)
        nll = fake_center - half_wire_vector
        nur = fake_center + half_wire_vector
        rect = [nll, nur]
        pin = graph_shape(name="fake",
                          rect=rect,
                          layer_name_pp=layer)
        return pin


    def get_route_pairs(self, pin_names):
        """ Return the pairs to be routed. """

        to_route = []
        for name in pin_names:
            pin = next(iter(self.pins[name]))
            fake = self.create_fake_pin(pin)
            to_route.append((pin, fake, pin.distance(fake)))
        return sorted(to_route, key=lambda x: x[2])


    def replace_layout_pins(self):
        """ Replace the old layout pins with new ones around the perimeter. """

        for name, pin in self.new_pins.items():
            pin = graph_shape(pin.name, pin.boundary, pin.lpp)
            # Find the intersection of this pin on the perimeter
            for fake in self.fake_pins:
                edge = pin.intersection(fake)
                if edge:
                    break
            self.design.replace_layout_pin(name, edge)
