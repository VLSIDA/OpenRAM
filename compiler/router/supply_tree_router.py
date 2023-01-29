# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from datetime import datetime
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from openram import debug
from openram import print_time
from .router import router
from . import grid_utils
from .signal_grid import signal_grid


class supply_tree_router(router):
    """
    A router class to read an obstruction map from a gds and
    routes a grid to connect the supply on the two layers.
    """

    def __init__(self, layers, design, bbox=None, pin_type=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        # Power rail width in minimum wire widths
        # This is set to match the signal router so that the grids are aligned
        # for prettier routes.
        self.route_track_width = 1

        # The pin escape router already made the bounding box big enough,
        # so we can use the regular bbox here.
        if pin_type:
            debug.check(pin_type in ["left", "right", "top", "bottom", "single", "ring"],
                        "Invalid pin type {}".format(pin_type))
        self.pin_type = pin_type
        router.__init__(self,
                        layers,
                        design,
                        bbox=bbox,
                        route_track_width=self.route_track_width)


    def route(self, vdd_name="vdd", gnd_name="gnd"):
        """
        Route the two nets in a single layer.
        Setting pin stripe will make a power rail on the left side.
        """
        debug.info(1, "Running supply router on {0} and {1}...".format(vdd_name, gnd_name))
        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

        # Clear the pins if we have previously routed
        if (hasattr(self, 'rg')):
            self.clear_pins()
        else:
            # Creat a routing grid over the entire area
            # FIXME: This could be created only over the routing region,
            # but this is simplest for now.
            self.create_routing_grid(signal_grid)

        start_time = datetime.now()

        # Get the pin shapes
        self.find_pins_and_blockages([self.vdd_name, self.gnd_name])
        print_time("Finding pins and blockages", datetime.now(), start_time, 3)

        # Add side pins if enabled
        if self.pin_type in ["left", "right", "top", "bottom"]:
            self.add_side_supply_pin(self.vdd_name, side=self.pin_type)
            self.add_side_supply_pin(self.gnd_name, side=self.pin_type)
        elif self.pin_type == "ring":
            self.add_ring_supply_pin(self.vdd_name)
            self.add_ring_supply_pin(self.gnd_name)

        #self.write_debug_gds("initial_tree_router.gds",False)
        #breakpoint()

        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        start_time = datetime.now()
        self.route_pins(vdd_name)
        self.route_pins(gnd_name)
        print_time("Maze routing supplies", datetime.now(), start_time, 3)

        # Did we route everything??
        if not self.check_all_routed(vdd_name):
            return False
        if not self.check_all_routed(gnd_name):
            return False

        return True

    def route_pins(self, pin_name):
        """
        This will route each of the remaining pin components to the other pins.
        After it is done, the cells are added to the pin blockage list.
        """

        remaining_components = sum(not x.is_routed() for x in self.pin_groups[pin_name])
        debug.info(1, "Routing {0} with {1} pins.".format(pin_name,
                                                          remaining_components))

        # Save pin center locations
        if False:
            debug.info(2, "Creating location file {0}_{1}.csv".format(self.cell.name, pin_name))
            f = open("{0}_{1}.csv".format(self.cell.name, pin_name), "w")
            pin_size = len(self.pin_groups[pin_name])
            for index1, pg1 in enumerate(self.pin_groups[pin_name]):
                location = list(pg1.grids)[0]
                f.write("{0},{1},{2}\n".format(location.x, location.y, location.z))
            f.close()

        # Create full graph
        debug.info(2, "Creating adjacency matrix")
        pin_size = len(self.pin_groups[pin_name])
        adj_matrix = [[0] * pin_size for i in range(pin_size)]

        for index1, pg1 in enumerate(self.pin_groups[pin_name]):
            for index2, pg2 in enumerate(self.pin_groups[pin_name]):
                if index1>=index2:
                    continue
                dist = int(grid_utils.distance_set(list(pg1.grids)[0], pg2.grids))
                adj_matrix[index1][index2] = dist

        # Find MST
        debug.info(2, "Finding Minimum Spanning Tree")
        X = csr_matrix(adj_matrix)
        from scipy.sparse import save_npz
        #print("Saving {}.npz".format(self.cell.name))
        #save_npz("{}.npz".format(self.cell.name), X)
        #exit(1)

        Tcsr = minimum_spanning_tree(X)
        mst = Tcsr.toarray().astype(int)
        connections = []
        for x in range(pin_size):
            for y in range(pin_size):
                if x >= y:
                    continue
                if mst[x][y]>0:
                    connections.append((x, y))

        # Route MST components
        level=99
        for index, (src, dest) in enumerate(connections):
            if not (index % 25):
                debug.info(1, "{0} supply segments routed, {1} remaining.".format(index, len(connections) - index))
            self.route_signal(pin_name, src, dest)
            if False and pin_name == "gnd":
                debug.info(level, "\nSRC {}: ".format(src) + str(self.pin_groups[pin_name][src].grids) + str(self.pin_groups[pin_name][src].blockages))
                debug.info(level, ("DST {}: ".format(dest) + str(self.pin_groups[pin_name][dest].grids)  + str(self.pin_groups[pin_name][dest].blockages)))
                self.write_debug_gds("post_{0}_{1}.gds".format(src, dest), False)

        #self.write_debug_gds("final_tree_router_{}.gds".format(pin_name), False)
        #return

    def route_signal(self, pin_name, src_idx, dest_idx):

        # First pass, try to route normally
        # Second pass, clear prior pin blockages so that you can route over other metal
        # of the same supply. Otherwise, this can create a lot of circular routes due to accidental overlaps.
        for unblock_routes in [False, True]:
            for detour_scale in [2 * pow(2, x) for x in range(5)]:
                debug.info(2, "Routing {0} to {1} with scale {2}".format(src_idx, dest_idx, detour_scale))

                # Clear everything in the routing grid.
                self.rg.reinit()

                # This is inefficient since it is non-incremental, but it was
                # easier to debug.
                self.prepare_blockages(src=(pin_name, src_idx), dest=(pin_name, dest_idx))
                if unblock_routes:
                    msg = "Unblocking supply self blockages to improve access (may cause DRC errors):\n{0}\n{1})"
                    debug.warning(msg.format(pin_name,
                                             self.pin_groups[pin_name][src_idx].pins))
                    self.set_blockages(self.path_blockages, False)

                # Add the single component of the pin as the source
                # which unmarks it as a blockage too
                self.set_pin_component_source(pin_name, src_idx)

                # Marks all pin components except index as target
                # which unmarks it as a blockage too
                self.set_pin_component_target(pin_name, dest_idx)

                # Actually run the A* router
                if self.run_router(detour_scale=detour_scale):
                    return
                #if detour_scale > 2:
                #    self.write_debug_gds("route_{0}_{1}_d{2}.gds".format(src_idx, dest_idx, detour_scale), False)

        self.write_debug_gds("debug_route.gds", True)

    def add_io_pin(self, instance, pin_name, new_name=""):
        """
        Add a signle input or output pin up to metal 3.
        """
        pin = instance.get_pins(pin_name)

        if new_name == "":
            new_name = pin_name

        # Just use the power pin function for now to save code
        self.add_power_pin(name=new_name, loc=pin.center(), start_layer=pin.layer)
