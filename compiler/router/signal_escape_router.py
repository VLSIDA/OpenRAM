# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
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
        for source, target, _ in self.get_route_pairs(pin_names):
            # Change fake pin's name so the graph will treat it as routable
            target.name = source.name
            # This is the routing region scale
            scale = 1
            while True:
                # Create the graph
                g = graph(self)
                region = g.create_graph(source, target, scale)
                # Find the shortest path from source to target
                path = g.find_shortest_path()
                # If there is no path found, exponentially try again with a
                # larger routing region
                if path is None:
                    rll, rur = region
                    bll, bur = self.bbox
                    # Stop scaling the region and throw an error
                    if rll.x < bll.x and rll.y < bll.y and \
                       rur.x > bur.x and rur.y > bur.y:
                        self.write_debug_gds(gds_name="{}error.gds".format(OPTS.openram_temp), g=g, source=source, target=target)
                        debug.error("Couldn't route from {} to {}.".format(source, target), -1)
                    # Exponentially scale the region
                    scale *= 2
                    debug.info(0, "Retry routing in larger routing region with scale {}".format(scale))
                    continue
                # Create the path shapes on layout
                new_shapes = self.add_path(path)
                self.new_pins[source.name] = new_shapes[0]
                # Find the recently added shapes
                self.prepare_gds_reader()
                self.find_blockages(name)
                self.find_vias()
                break
        self.replace_layout_pins()


    def add_perimeter_fake_pins(self):
        """
        Add the fake pins on the perimeter to where the signals will be routed.
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


    def get_closest_perimeter_fake_pin(self, pin):
        """ Return the closest fake pin for the given pin. """

        min_dist = float("inf")
        close_fake = None
        for fake in self.fake_pins:
            dist = pin.distance(fake)
            if dist < min_dist:
                min_dist = dist
                close_fake = fake
        return close_fake


    def get_route_pairs(self, pin_names):
        """ Return the pairs to be routed. """

        to_route = []
        for name in pin_names:
            pin = next(iter(self.pins[name]))
            fake = self.get_closest_perimeter_fake_pin(pin)
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
