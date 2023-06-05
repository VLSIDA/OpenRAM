# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.router import router


class signal_router(router):
    """
    A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    """

    def __init__(self, layers, design, bbox=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        router.__init__(self, layers, design, bbox)

    def route(self, src, dest, detour_scale=5):
        """
        Route a single source-destination net and return
        the simplified rectilinear path. Cost factor is how sub-optimal to explore for a feasible route.
        This is used to speed up the routing when there is not much detouring needed.
        """
        debug.info(1, "Running signal router from {0} to {1}...".format(src, dest))

        self.pins[src] = []
        self.pins[dest] = []

        # Clear the pins if we have previously routed
        if (hasattr(self, 'rg')):
            self.clear_pins()
        else:
            # Creat a routing grid over the entire area
            # FIXME: This could be created only over the routing region,
            # but this is simplest for now.
            self.create_routing_grid(signal_grid)

        # Get the pin shapes
        self.find_pins_and_blockages([src, dest])

        # Block everything
        self.prepare_blockages()
        # Clear the pins we are routing
        self.set_blockages(self.pin_components[src], False)
        self.set_blockages(self.pin_components[dest], False)

        # Now add the src/tgt if they are not blocked by other shapes
        self.add_source(src)
        self.add_target(dest)

        if not self.run_router(detour_scale=detour_scale):
            self.write_debug_gds(stop_program=False)
            return False

        #self.write_debug_gds(stop_program=False)
        return True






