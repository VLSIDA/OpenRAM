# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from globals import print_time
from router import router
from datetime import datetime
from signal_grid import signal_grid


class signal_escape_router(router):
    """
    A router that routes signals to perimeter and makes pins.
    """

    def __init__(self, layers, design, gds_filename=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        router.__init__(self, layers, design, gds_filename, 1)

    def create_routing_grid(self):
        """
        Create a sprase routing grid with A* expansion functions.
        """
        size = self.ur - self.ll
        debug.info(1,"Size: {0} x {1}".format(size.x, size.y))
        self.rg = signal_grid(self.ll, self.ur, self.track_width)

    def escape_route(self, pin_names):
        """
        Takes a list of tuples (name, side) and routes them. After routing,
        it removes the old pin and places a new one on the perimeter.
        """
        self.create_routing_grid()

        start_time = datetime.now()
        self.find_pins_and_blockages(pin_names)
        print_time("Finding pins and blockages",datetime.now(), start_time, 3)

        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        start_time = datetime.now()
        for pin_name in pin_names:
            self.route_signal(pin_name)
            
        print_time("Maze routing pins",datetime.now(), start_time, 3)

        # self.write_debug_gds("final_escape_router.gds",False)
        
        return True

    def route_signal(self, pin_name, side="all"):
        
        for detour_scale in [5 * pow(2, x) for x in range(5)]:
            debug.info(1, "Escape routing {0} with scale {1}".format(pin_name, detour_scale))
            
            # Clear everything in the routing grid.
            self.rg.reinit()

            # This is inefficient since it is non-incremental, but it was
            # easier to debug.
            self.prepare_blockages(pin_name)

            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_source(pin_name)

            # Marks the grid cells all along the perimeter as a target
            self.add_perimeter_target(side)
            
            # Actually run the A* router
            if self.run_router(detour_scale=detour_scale):
                new_pin = self.get_perimeter_pin()
                self.cell.replace_layout_pin(pin_name, new_pin)
                return

        self.write_debug_gds("debug_route.gds", True)


