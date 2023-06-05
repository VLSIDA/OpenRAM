# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from datetime import datetime
from openram import debug
from openram import print_time
from .router import router
from .signal_grid import signal_grid


class signal_escape_router(router):
    """
    A router that routes signals to perimeter and makes pins.
    """

    def __init__(self, layers, design, bbox=None, margin=0):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        router.__init__(self,
                        layers=layers,
                        design=design,
                        bbox=bbox,
                        margin=margin)

    def perimeter_dist(self, pin_name):
        """
        Return the shortest Manhattan distance to the bounding box perimeter.
        """
        loc = self.cell.get_pin(pin_name).center()
        x_dist = min(loc.x - self.ll.x, self.ur.x - loc.x)
        y_dist = min(loc.y - self.ll.y, self.ur.y - loc.y)

        return min(x_dist, y_dist)

    def escape_route(self, pin_names):
        """
        Takes a list of tuples (name, side) and routes them. After routing,
        it removes the old pin and places a new one on the perimeter.
        """
        self.create_routing_grid(signal_grid)

        start_time = datetime.now()
        self.find_pins_and_blockages(pin_names)
        print_time("Finding pins and blockages",datetime.now(), start_time, 3)

        # Order the routes by closest to the perimeter first
        # This prevents some pins near the perimeter from being blocked by other pins
        ordered_pin_names = sorted(pin_names, key=lambda x: self.perimeter_dist(x))

        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        start_time = datetime.now()
        for pin_name in ordered_pin_names:
            self.route_signal(pin_name)
            # if pin_name == "dout0[1]":
            #     self.write_debug_gds("postroute.gds", True)

        print_time("Maze routing pins",datetime.now(), start_time, 3)

        #self.write_debug_gds("final_escape_router.gds",False)

        return True

    def route_signal(self, pin_name, side="all"):

        for detour_scale in [5 * pow(2, x) for x in range(5)]:
            debug.info(1, "Escape routing {0} with scale {1}".format(pin_name, detour_scale))

            # Clear everything in the routing grid.
            self.rg.reinit()

            # This is inefficient since it is non-incremental, but it was
            # easier to debug.
            self.prepare_blockages()
            self.clear_blockages(pin_name)

            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_source(pin_name)

            # Marks the grid cells all along the perimeter as a target
            self.add_perimeter_target(side)

            # if pin_name == "dout0[3]":
            #     self.write_debug_gds("pre_route.gds", False)
            #     breakpoint()

            # Actually run the A* router
            if self.run_router(detour_scale=detour_scale):
                new_pin = self.get_perimeter_pin()
                self.cell.replace_layout_pin(pin_name, new_pin)
                return

            # if pin_name == "dout0[3]":
            #     self.write_debug_gds("pre_route.gds", False)
            #     breakpoint()

        self.write_debug_gds("debug_route.gds", True)
