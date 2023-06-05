# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from datetime import datetime
from openram import debug
from openram.base.vector3d import vector3d
from openram import print_time
from .router import router
from .direction import direction
from .supply_grid import supply_grid
from . import grid_utils


class supply_grid_router(router):
    """
    A router class to read an obstruction map from a gds and
    routes a grid to connect the supply on the two layers.
    """

    def __init__(self, layers, design, bbox=None, pin_type=None):
        """
        This will route on layers in design. It will get the blockages from
        either the gds file name or the design itself (by saving to a gds file).
        """
        start_time = datetime.now()

        # Power rail width in minimum wire widths
        self.route_track_width = 1

        router.__init__(self, layers, design, bbox=bbox, margin=margin, route_track_width=self.route_track_width)

        # The list of supply rails (grid sets) that may be routed
        self.supply_rails = {}
        # This is the same as above but as a sigle set for the all the rails
        self.supply_rail_tracks = {}

        print_time("Init supply router", datetime.now(), start_time, 3)

    def route(self, vdd_name="vdd", gnd_name="gnd"):
        """
        Add power supply rails and connect all pins to these rails.
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
            self.create_routing_grid(supply_grid)

        # Get the pin shapes
        start_time = datetime.now()
        self.find_pins_and_blockages([self.vdd_name, self.gnd_name])
        print_time("Finding pins and blockages", datetime.now(), start_time, 3)
        # Add the supply rails in a mesh network and connect H/V with vias
        start_time = datetime.now()
        # Block everything
        self.prepare_blockages()
        self.clear_blockages(self.gnd_name)


        # Determine the rail locations
        self.route_supply_rails(self.gnd_name, 0)

        # Block everything
        self.prepare_blockages()
        self.clear_blockages(self.vdd_name)
        # Determine the rail locations
        self.route_supply_rails(self.vdd_name, 1)
        print_time("Routing supply rails", datetime.now(), start_time, 3)

        start_time = datetime.now()
        self.route_simple_overlaps(vdd_name)
        self.route_simple_overlaps(gnd_name)
        print_time("Simple overlap routing", datetime.now(), start_time, 3)

        # Route the supply pins to the supply rails
        # Route vdd first since we want it to be shorter
        start_time = datetime.now()
        self.route_pins_to_rails(vdd_name)
        self.route_pins_to_rails(gnd_name)
        print_time("Maze routing supplies", datetime.now(), start_time, 3)
        # self.write_debug_gds("final.gds", False)

        # Did we route everything??
        if not self.check_all_routed(vdd_name):
            return False
        if not self.check_all_routed(gnd_name):
            return False

        return True

    def route_simple_overlaps(self, pin_name):
        """
        This checks for simple cases where a pin component already overlaps a supply rail.
        It will add an enclosure to ensure the overlap in wide DRC rule cases.
        """
        debug.info(1, "Routing simple overlap pins for {0}".format(pin_name))

        # These are the wire tracks
        wire_tracks = self.supply_rail_tracks[pin_name]
        routed_count=0
        for pg in self.pin_groups[pin_name]:
            if pg.is_routed():
                continue

            # First, check if we just overlap, if so, we are done.
            overlap_grids = wire_tracks & pg.grids
            if len(overlap_grids)>0:
                routed_count += 1
                pg.set_routed()
                continue

            # Else, if we overlap some of the space track, we can patch it with an enclosure
            # pg.create_simple_overlap_enclosure(pg.grids)
            # pg.add_enclosure(self.cell)

        debug.info(1, "Routed {} simple overlap pins".format(routed_count))

    def finalize_supply_rails(self, name):
        """
        Determine which supply rails overlap and can accomodate a via.
        Remove any supply rails that do not have a via since they are disconnected.
        NOTE: It is still possible though unlikely that there are disconnected groups of rails.
        """

        all_rails = self.supply_rails[name]

        connections = set()
        via_areas = []
        for i1, r1 in enumerate(all_rails):
            # Only consider r1 horizontal rails
            e = next(iter(r1))
            if e.z==1:
                continue

            # We need to move this rail to the other layer for the z indices to match
            # during the intersection. This also makes a copy.
            new_r1 = {vector3d(i.x, i.y, 1) for i in r1}

            for i2, r2 in enumerate(all_rails):
                # Never compare to yourself
                if i1==i2:
                    continue

                # Only consider r2 vertical rails
                e = next(iter(r2))
                if e.z==0:
                    continue

                # Determine if we have sufficient overlap and, if so,
                # remember:
                # the indices to determine a rail is connected to another
                # the overlap area for placement of a via
                overlap = new_r1 & r2
                if len(overlap) >= 1:
                    debug.info(3, "Via overlap {0} {1}".format(len(overlap),overlap))
                    connections.update([i1, i2])
                    via_areas.append(overlap)

        # Go through and add the vias at the center of the intersection
        for area in via_areas:
            ll = grid_utils.get_lower_left(area)
            ur = grid_utils.get_upper_right(area)
            center = (ll + ur).scale(0.5, 0.5, 0)
            self.add_via(center, 1)

        # Determien which indices were not connected to anything above
        missing_indices = set([x for x in range(len(self.supply_rails[name]))])
        missing_indices.difference_update(connections)

        # Go through and remove those disconnected indices
        # (No via was added, so that doesn't need to be removed)
        for rail_index in sorted(missing_indices, reverse=True):
            ll = grid_utils.get_lower_left(all_rails[rail_index])
            ur = grid_utils.get_upper_right(all_rails[rail_index])
            debug.info(1, "Removing disconnected supply rail {0} .. {1}".format(ll, ur))
            self.supply_rails[name].pop(rail_index)

        # Make the supply rails into a big giant set of grids for easy blockages.
        # Must be done after we determine which ones are connected.
        self.create_supply_track_set(name)

    def add_supply_rails(self, name):
        """
        Add the shapes that represent the routed supply rails.
        This is after the paths have been pruned and only include rails that are
        connected with vias.
        """
        for rail in self.supply_rails[name]:
            ll = grid_utils.get_lower_left(rail)
            ur = grid_utils.get_upper_right(rail)
            z = ll.z
            pin = self.compute_pin_enclosure(ll, ur, z, name)
            debug.info(3, "Adding supply rail {0} {1}->{2} {3}".format(name, ll, ur, pin))
            self.cell.add_layout_pin(text=name,
                                     layer=pin.layer,
                                     offset=pin.ll(),
                                     width=pin.width(),
                                     height=pin.height())

    def compute_supply_rails(self, name, supply_number):
        """
        Compute the unblocked locations for the horizontal and vertical supply rails.
        Go in a raster order from bottom to the top (for horizontal) and left to right
        (for vertical). Start with an initial start_offset in x and y direction.
        """

        self.supply_rails[name]=[]

        max_yoffset = self.rg.ur.y
        max_xoffset = self.rg.ur.x
        min_yoffset = self.rg.ll.y
        min_xoffset = self.rg.ll.x

        # Horizontal supply rails
        start_offset = min_yoffset + supply_number
        for offset in range(start_offset, max_yoffset, 2):
            # Seed the function at the location with the given width
            wave = [vector3d(min_xoffset, offset, 0)]
            # While we can keep expanding east in this horizontal track
            while wave and wave[0].x < max_xoffset:
                added_rail = self.find_supply_rail(name, wave, direction.EAST)
                if not added_rail:
                    # Just seed with the next one
                    wave = [x+vector3d(1, 0, 0) for x in wave]
                else:
                    # Seed with the neighbor of the end of the last rail
                    wave = added_rail.neighbor(direction.EAST)

        # Vertical supply rails
        start_offset = min_xoffset + supply_number
        for offset in range(start_offset, max_xoffset, 2):
            # Seed the function at the location with the given width
            wave = [vector3d(offset, min_yoffset, 1)]
            # While we can keep expanding north in this vertical track
            while wave and wave[0].y < max_yoffset:
                added_rail = self.find_supply_rail(name, wave, direction.NORTH)
                if not added_rail:
                    # Just seed with the next one
                    wave = [x + vector3d(0, 1, 0) for x in wave]
                else:
                    # Seed with the neighbor of the end of the last rail
                    wave = added_rail.neighbor(direction.NORTH)

    def find_supply_rail(self, name, seed_wave, direct):
        """
        Find a start location, probe in the direction, and see if the rail is big enough
        to contain a via, and, if so, add it.
        """
        # Sweep to find an initial unblocked valid wave
        start_wave = self.rg.find_start_wave(seed_wave, direct)

        # This means there were no more unblocked grids in the row/col
        if not start_wave:
            return None

        wave_path = self.probe_supply_rail(name, start_wave, direct)

        self.approve_supply_rail(name, wave_path)

        # Return the rail whether we approved it or not,
        # as it will be used to find the next start location
        return wave_path

    def probe_supply_rail(self, name, start_wave, direct):
        """
        This finds the first valid starting location and routes a supply rail
        in the given direction.
        It returns the space after the end of the rail to seed another call for multiple
        supply rails in the same "track" when there is a blockage.
        """

        # Expand the wave to the right
        wave_path = self.rg.probe(start_wave, direct)

        if not wave_path:
            return None

        # drop the first and last steps to leave escape routing room
        # around the blockage that stopped the probe
        # except, don't drop the first if it is the first in a row/column
        if (direct==direction.NORTH and start_wave[0].y>0):
            wave_path.trim_first()
        elif (direct == direction.EAST and start_wave[0].x>0):
            wave_path.trim_first()

        wave_path.trim_last()

        return wave_path

    def approve_supply_rail(self, name, wave_path):
        """
        Check if the supply rail is sufficient (big enough) and add it to the
        data structure. Return whether it was added or not.
        """
        # We must have at least 2 tracks to drop plus 2 tracks for a via
        if len(wave_path) >= 4 * self.route_track_width:
            grid_set = wave_path.get_grids()
            self.supply_rails[name].append(grid_set)
            return True

        return False

    def route_supply_rails(self, name, supply_number):
        """
        Route the horizontal and vertical supply rails across the entire design.
        Must be done with lower left at 0,0
        """
        debug.info(1, "Routing supply rail {0}.".format(name))

        # Compute the grid locations of the supply rails
        self.compute_supply_rails(name, supply_number)

        # Add the supply rail vias (and prune disconnected rails)
        self.finalize_supply_rails(name)

        # Add the rails themselves
        self.add_supply_rails(name)

    def create_supply_track_set(self, pin_name):
        """
        Make a single set of all the tracks for the rail and wire itself.
        """
        rail_set = set()
        for rail in self.supply_rails[pin_name]:
            rail_set.update(rail)
        self.supply_rail_tracks[pin_name] = rail_set

    def route_pins_to_rails(self, pin_name):
        """
        This will route each of the remaining pin components to the supply rails.
        After it is done, the cells are added to the pin blockage list.
        """

        remaining_components = sum(not x.is_routed() for x in self.pin_groups[pin_name])
        debug.info(1, "Maze routing {0} with {1} pin components to connect.".format(pin_name,
                                                                                    remaining_components))

        for index, pg in enumerate(self.pin_groups[pin_name]):
            if pg.is_routed():
                continue

            debug.info(3, "Routing component {0} {1}".format(pin_name, index))

            # Clear everything in the routing grid.
            self.rg.reinit()

            # This is inefficient since it is non-incremental, but it was
            # easier to debug.
            self.prepare_blockages()
            self.clear_blockages(self.vdd_name)

            # Add the single component of the pin as the source
            # which unmarks it as a blockage too
            self.add_pin_component_source(pin_name, index)

            # Add all of the rails as targets
            # Don't add the other pins, but we could?
            self.add_supply_rail_target(pin_name)

            # Actually run the A* router
            if not self.run_router(detour_scale=5):
                self.write_debug_gds("debug_route.gds")

            # if index==3 and pin_name=="vdd":
            #     self.write_debug_gds("route.gds",False)

    def add_supply_rail_target(self, pin_name):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(4, "Add supply rail target {}".format(pin_name))
        # Add the wire itself as the target
        self.rg.set_target(self.supply_rail_tracks[pin_name])
        # But unblock all the rail tracks including the space
        self.rg.set_blocked(self.supply_rail_tracks[pin_name], False)

    def set_supply_rail_blocked(self, value=True):
        """
        Add the supply rails of given name as a routing target.
        """
        debug.info(4, "Blocking supply rail")
        for rail_name in self.supply_rail_tracks:
            self.rg.set_blocked(self.supply_rail_tracks[rail_name])
