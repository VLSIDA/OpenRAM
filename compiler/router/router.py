# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
import itertools
from datetime import datetime
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.base.pin_layout import pin_layout
from openram.gdsMill import gdsMill
from openram.tech import drc, GDS
from openram.tech import layer as techlayer
from openram import OPTS, print_time
from .router_tech import router_tech
from .pin_group import pin_group
from . import grid_utils


class router(router_tech):
    """
    A router class to read an obstruction map from a gds and plan a
    route on a given layer. This is limited to two layer routes.
    It populates blockages on a grid class.
    """
    def __init__(self, layers, design, bbox=None, margin=0, route_track_width=1):
        """
        This will instantiate a copy of the gds file or the module at (0,0) and
        route on top of this. The blockages from the gds/module will be
        considered.
        """

        router_tech.__init__(self, layers, route_track_width)

        self.cell = design

        self.gds_filename = OPTS.openram_temp + "temp.gds"

        # The pin data structures
        # A map of pin names to a set of pin_layout structures
        # (i.e. pins with a given label)
        self.pins = {}
        # This is a set of all pins (ignoring names) so that can quickly
        # not create blockages for pins
        # (They will be blocked when we are routing other
        # nets based on their name.)
        self.all_pins = set()

        # The labeled pins above categorized into pin groups
        # that are touching/connected.
        self.pin_groups = {}

        # The blockage data structures
        # A list of metal shapes (using the same pin_layout structure)
        # that could be blockages.
        # This will include the pins above as well.
        self.blockages = []
        # The corresponding set of blocked grids for above blockage pin_layout shapes
        # It is a cached set of grids that *could* be blocked, but may be unblocked
        # depending on which pin we are routing.
        self.blocked_grids = set()

        # The routed data structures
        # A list of paths that have been "routed"
        self.paths = []
        # A list of path blockages (they might be expanded for wide metal DRC)
        self.path_blockages = []

        # The perimeter pins should be placed outside the SRAM macro by a distance
        self.margin = margin
        self.init_bbox(bbox, margin)

        # New pins if we create a ring or side pins or etc.
        self.new_pins = {}

    def init_bbox(self, bbox=None, margin=0):
        """
        Initialize the ll,ur values with the paramter or using the layout boundary.
        """
        if not bbox:
            self.bbox = self.cell.get_bbox(margin)
        else:
            self.bbox = bbox

        (self.ll, self.ur) = self.bbox

    def get_bbox(self):
        return self.bbox

    def create_routing_grid(self, router_type=None):
        """
        Create (or recreate) a sprase routing grid with A* expansion functions.
        """
        debug.check(router_type or hasattr(self, "router_type"), "Must specify a routing grid type.")

        self.init_bbox(self.bbox, self.margin)

        if router_type:
            self.router_type = router_type
            self.rg = router_type(self.ll, self.ur, self.track_width)
        else:
            self.rg = self.router_type(self.ll, self.ur, self.track_width)

    def clear_pins(self):
        """
        Convert the routed path to blockages.
        Keep the other blockages unchanged.
        """
        self.pins = {}
        self.all_pins = set()
        self.pin_groups = {}
        # DO NOT clear the blockages as these don't change
        self.rg.reinit()

    def set_top(self, top_name):
        """ If we want to route something besides the top-level cell."""
        self.top_name = top_name

    def is_wave(self, path):
        """
        Determines if this is a multi-track width wave (True)
        # or a normal route (False)
        """
        return len(path[0]) > 1

    def retrieve_pins(self, pin_name):
        """
        Retrieve the pin shapes on metal 3 from the layout.
        """
        debug.info(2, "Retrieving pins for {}.".format(pin_name))
        shape_list = self.layout.getAllPinShapes(str(pin_name))
        pin_set = set()
        for shape in shape_list:
            (layer, boundary) = shape
            # GDSMill boundaries are in (left, bottom, right, top) order
            # so repack and snap to the grid
            ll = vector(boundary[0], boundary[1]).snap_to_grid()
            ur = vector(boundary[2], boundary[3]).snap_to_grid()
            rect = [ll, ur]
            pin = pin_layout(pin_name, rect, layer)
            pin_set.add(pin)

        debug.check(len(pin_set) > 0,
                    "Did not find any pin shapes for {0}.".format(str(pin_name)))

        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)

        for pin in self.pins[pin_name]:
            debug.info(3, "Retrieved pin {}".format(str(pin)))

    def find_blockages(self):
        """
        Iterate through all the layers and write the obstacles to the routing grid.
        This doesn't consider whether the obstacles will be pins or not.
        They get reset later if they are not actually a blockage.
        """
        debug.info(1, "Finding blockages.")
        for lpp in [self.vert_lpp, self.horiz_lpp]:
            self.retrieve_blockages(lpp)

    def find_pins_and_blockages(self, pin_list):
        """
        Find the pins and blockages in the design
        """

        # If didn't specify a gds blockage file, write it out to read the gds
        # This isn't efficient, but easy for now
        # Load the gds file and read in all the shapes
        self.cell.gds_write(self.gds_filename)
        self.layout = gdsMill.VlsiLayout(units=GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(self.gds_filename)
        self.top_name = self.layout.rootStructureName
        # print_time("GDS read",datetime.now(), start_time)

        # This finds the pin shapes and sorts them into "groups" that
        # are connected. This must come before the blockages, so we
        # can not count the pins themselves
        # as blockages.
        start_time = datetime.now()
        for pin_name in pin_list:
            self.retrieve_pins(pin_name)
        print_time("Retrieving pins", datetime.now(), start_time, 4)

        start_time = datetime.now()
        for pin_name in pin_list:
            self.analyze_pins(pin_name)
        print_time("Analyzing pins", datetime.now(), start_time, 4)

        # This will get all shapes as blockages and convert to grid units
        # This ignores shapes that were pins
        start_time = datetime.now()
        self.find_blockages()
        print_time("Finding blockages", datetime.now(), start_time, 4)

        # Convert the blockages to grid units
        start_time = datetime.now()
        self.convert_blockages()
        print_time("Converting blockages", datetime.now(), start_time, 4)

        # This will convert the pins to grid units
        # It must be done after blockages to ensure no DRCs
        # between expanded pins and blocked grids
        start_time = datetime.now()
        for pin in pin_list:
            self.convert_pins(pin)
        print_time("Converting pins", datetime.now(), start_time, 4)

        # Combine adjacent pins into pin groups to reduce run-time
        # by reducing the number of maze routes.
        # This algorithm is > O(n^2) so remove it for now
        # start_time = datetime.now()
        # for pin in pin_list:
        #     self.combine_adjacent_pins(pin)
        # print_time("Combining adjacent pins",datetime.now(), start_time, 4)

        # Separate any adjacent grids of differing net names
        # that overlap
        # Must be done before enclosing pins
        start_time = datetime.now()
        self.separate_adjacent_pins(0)
        print_time("Separating adjacent pins", datetime.now(), start_time, 4)

        # Enclose the continguous grid units in a metal
        # rectangle to fix some DRCs
        #start_time = datetime.now()
        #self.enclose_pins()
        #print_time("Enclosing pins", datetime.now(), start_time, 4)

    # MRG: Removing this code for now. The later compute enclosure code
    # assumes that all pins are touching and this may produce sets of pins
    # that are not connected.
    # def combine_adjacent_pins(self, pin_name):
    #     """
    #     Find pins that have adjacent routing tracks and merge them into a
    #     single pin_group.  The pins themselves may not be touching, but
    #     enclose_pins in the next step will ensure they are touching.
    #     """
    #     debug.info(1,"Combining adjacent pins for {}.".format(pin_name))
    #     # Find all adjacencies
    #     adjacent_pins = {}
    #     for index1,pg1 in enumerate(self.pin_groups[pin_name]):
    #         for index2,pg2 in enumerate(self.pin_groups[pin_name]):
    #             # Cannot combine with yourself, also don't repeat
    #             if index1<=index2:
    #                 continue
    #             # Combine if at least 1 grid cell is adjacent
    #             if pg1.adjacent(pg2):
    #                 if not index1 in adjacent_pins:
    #                     adjacent_pins[index1] = set([index2])
    #                 else:
    #                     adjacent_pins[index1].add(index2)

    #     # Make a list of indices to ensure every group gets in the new set
    #     all_indices = set([x for x in range(len(self.pin_groups[pin_name]))])

    #     # Now reconstruct the new groups
    #     new_pin_groups = []
    #     for index1,index2_set in adjacent_pins.items():
    #         # Remove the indices if they are added to the new set
    #         all_indices.discard(index1)
    #         all_indices.difference_update(index2_set)

    #         # Create the combined group starting with the first item
    #         combined = self.pin_groups[pin_name][index1]
    #         # Add all of the other items that overlapped
    #         for index2 in index2_set:
    #             pg = self.pin_groups[pin_name][index2]
    #             combined.add_group(pg)
    #             debug.info(3,"Combining {0} {1}:".format(pin_name, index2))
    #             debug.info(3, "     {0}\n  {1}".format(combined.pins, pg.pins))
    #             debug.info(3,"  --> {0}\n      {1}".format(combined.pins,combined.grids))
    #             new_pin_groups.append(combined)

    #     # Add the pin groups that weren't added to the new set
    #     for index in all_indices:
    #         new_pin_groups.append(self.pin_groups[pin_name][index])

    #     old_size = len(self.pin_groups[pin_name])
    #     # Use the new pin group!
    #     self.pin_groups[pin_name] = new_pin_groups
    #     removed_pairs = old_size - len(new_pin_groups)
    #     debug.info(1,
    #                "Combined {0} pin groups for {1}".format(removed_pairs,pin_name))

    #     return removed_pairs

    def separate_adjacent_pins(self, separation):
        """
        This will try to separate all grid pins by the supplied
        number of separation tracks (default is to prevent adjacency).
        """
        pin_names = self.pin_groups.keys()

        for (pin_name1, pin_name2) in itertools.combinations(pin_names, 2):
            self.separate_adjacent_pin(pin_name1, pin_name2, separation)

    def separate_adjacent_pin(self, pin_name1, pin_name2, separation):
        """
        Go through all of the pin groups and check if any other pin group is
        within a separation of it.
        If so, reduce the pin group grid to not include the adjacent grid.
        Try to do this intelligently to keep th pins enclosed.
        """
        debug.info(2,
                   "Comparing {0} and {1} adjacency".format(pin_name1,
                                                            pin_name2))
        removed_grids = 0

        for index1, pg1 in enumerate(self.pin_groups[pin_name1]):
            for index2, pg2 in enumerate(self.pin_groups[pin_name2]):
                adj_grids = pg1.adjacent_grids(pg2, separation)
                removed_grids += len(adj_grids)
                # These should have the same length, so...
                if len(adj_grids) > 0:
                    debug.info(3,
                               "Adjacent grids {0} {1} adj={2}".format(index1,
                                                                       index2,
                                                                       adj_grids))
                    self.remove_adjacent_grid(pg1, pg2, adj_grids)

        debug.info(2, "Removed {} adjacent grids.".format(removed_grids))

    def remove_adjacent_grid(self, pg1, pg2, adj_grids):
        """
        Remove one of the adjacent grids in a heuristic manner.
        This will try to keep the groups similar sized by
        removing from the bigger group.
        """

        if pg1.size() > pg2.size():
            bigger = pg1
            smaller = pg2
        else:
            bigger = pg2
            smaller = pg1

        for adj in adj_grids:


            # If the adjacent grids are a subset of the secondary
            # grids (i.e. not necessary) remove them from each
            if adj in bigger.secondary_grids:
                debug.info(3,"Removing {} from bigger secondary {}".format(adj,
                                                                           bigger))
                bigger.grids.remove(adj)
                bigger.secondary_grids.remove(adj)
                self.blocked_grids.add(adj)
            elif adj in smaller.secondary_grids:
                debug.info(3,"Removing {} from smaller secondary {}".format(adj,
                                                                            smaller))
                smaller.grids.remove(adj)
                smaller.secondary_grids.remove(adj)
                self.blocked_grids.add(adj)
            else:
                # If we couldn't remove from a secondary grid,
                # we must remove from the primary
                # grid of at least one pin
                if adj in bigger.grids:
                    debug.info(3,"Removing {} from bigger primary {}".format(adj,
                                                                             bigger))
                    bigger.grids.remove(adj)
                elif adj in smaller.grids:
                    debug.info(3,"Removing {} from smaller primary {}".format(adj,
                                                                              smaller))
                    smaller.grids.remove(adj)

    def set_supply_rail_blocked(self, value):
        # This is just a virtual function
        pass

    def prepare_blockages(self, src=None, dest=None):
        """
        Reset and add all of the blockages in the design.
        Skip adding blockages from src and dest component if specified as a tuple of name,component.
        """
        debug.info(3, "Preparing blockages.")

        # Start fresh. Not the best for run-time, but simpler.
        self.clear_all_blockages()

        # This adds the initial blockges of the design
        # which includes all blockages due to non-pin shapes
        # print("BLOCKING:", self.blocked_grids)
        self.set_blockages(self.blocked_grids, True)

        # Block all of the supply rails
        # (some will be unblocked if they're a target)
        try:
            self.set_supply_rail_blocked(True)
        except AttributeError:
            # If function doesn't exist, it isn't a supply router
            pass

        # Now go and block all of the blockages due to pin shapes.
        # Some of these will get unblocked later if they are the source/target.
        for name in self.pin_groups:
            blockage_grids = []
            for component_idx, component in enumerate(self.pin_groups[name]):
                # Skip adding source or dest blockages
                if src and src[0] == name and src[1] == component_idx:
                    continue
                if dest and dest[0] == name and dest[1] == component_idx:
                    continue
                blockage_grids.extend(component.blockages)
            self.set_blockages(blockage_grids, True)

        # If we have paths that were recently routed, add them as blockages as well.
        # We might later do rip-up and reroute so they might not be metal shapes in the design yet.
        # Also, this prevents having to reload an entire GDS and find the blockage shapes.
        self.set_blockages(self.path_blockages)

    def convert_shape_to_units(self, shape):
        """
        Scale a shape (two vector list) to user units
        """
        unit_factor = [GDS["unit"][0]] * 2
        ll = shape[0].scale(unit_factor)
        ur = shape[1].scale(unit_factor)
        return [ll, ur]

    def min_max_coord(self, coord):
        """
        Find the lowest and highest corner of a Rectangle
        """
        coordinate = []
        minx = min(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        maxx = max(coord[0][0], coord[1][0], coord[2][0], coord[3][0])
        miny = min(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        maxy = max(coord[0][1], coord[1][1], coord[2][1], coord[3][1])
        coordinate += [vector(minx, miny)]
        coordinate += [vector(maxx, maxy)]
        return coordinate

    def get_inertia(self, p0, p1):
        """
        Sets the direction based on the previous direction we came from.
        """
        # direction (index) of movement
        if p0.x != p1.x:
            return 0
        elif p0.y != p1.y:
            return 1
        else:
            # z direction
            return 2

    def clear_blockages(self, pin_name):
        """
        This function clears a given pin and all of its components from being blockages.
        """
        blockage_grids = {y for x in self.pin_groups[pin_name] for y in x.blockages}
        self.set_blockages(blockage_grids, False)

    def clear_all_blockages(self):
        """
        Clear all blockages on the grid.
        """
        debug.info(3, "Clearing all blockages")
        self.rg.clear_blockages()

    def set_blockages(self, blockages, value=True):
        """ Flag the blockages in the grid """
        self.rg.set_blocked(blockages, value)

    def convert_to_tracks(self, ll, ur, z):
        debug.info(3, "Converting ll={0} ur={1} z={2}".format(str(ll),str(ur),z))

        grid_list = []
        for x in range(int(ll[0]), int(ur[0])+1):
            for y in range(int(ll[1]), int(ur[1])+1):
                grid_list.append(vector3d(x, y, z))

        return set(grid_list)

    def convert_blockage(self, blockage):
        """
        Convert a pin layout blockage shape to routing grid tracks.
        """
        # Inflate the blockage by half a spacing rule
        [ll, ur] = self.convert_shape_to_tracks(blockage.inflate())
        zlayer = self.get_zindex(blockage.lpp)
        blockage_tracks = self.convert_to_tracks(ll, ur, zlayer)
        return blockage_tracks

    def convert_blockages(self):
        """ Convert blockages to grid tracks. """
        debug.info(1, "Converting blockages.")
        for blockage in self.blockages:
            debug.info(3, "Converting blockage {}".format(str(blockage)))
            blockage_list = self.convert_blockage(blockage)
            self.blocked_grids.update(blockage_list)

    def get_blocked_grids(self):
        """
        Return the blocked grids with their flag set
        """
        #return set([x for x in self.blocked_grids if self.rg.is_blocked(x)])
        # These are all the non-pin blockages
        return self.blocked_grids

    def retrieve_blockages(self, lpp):
        """
        Recursive find boundaries as blockages to the routing grid.
        """

        shapes = self.layout.getAllShapes(lpp)
        for boundary in shapes:
            ll = vector(boundary[0], boundary[1])
            ur = vector(boundary[2], boundary[3])
            rect = [ll, ur]
            new_shape = pin_layout("blockage{}".format(len(self.blockages)),
                                   rect,
                                   lpp)

            # If there is a rectangle that is the same in the pins,
            # it isn't a blockage!
            if new_shape not in self.all_pins and not self.pin_contains(new_shape):
                self.blockages.append(new_shape)

    def pin_contains(self, shape):
        for pin in self.all_pins:
            if pin.contains(shape):
                return True
        return False

    def convert_point_to_units(self, p):
        """
        Convert a path set of tracks to center line path.
        """
        pt = vector3d(p)
        pt = pt.scale(self.track_widths[0], self.track_widths[1], 1)
        return pt

    def convert_wave_to_units(self, wave):
        """
        Convert a wave to a set of center points
        """
        return [self.convert_point_to_units(i) for i in wave]

    def convert_shape_to_tracks(self, shape):
        """
        Convert a rectangular shape into track units.
        """
        (ll, ur) = shape
        ll = snap_to_grid(ll)
        ur = snap_to_grid(ur)

        # to scale coordinates to tracks
        debug.info(3, "Converting [ {0} , {1} ]".format(ll, ur))
        ll = ll.scale(self.track_factor)
        ur = ur.scale(self.track_factor)
        # We can round since we are using inflated shapes
        # and the track points are at the center
        ll = ll.round()
        ur = ur.round()
        return [ll, ur]

    def convert_pin_to_tracks(self, pin_name, pin, expansion=0):
        """
        Convert a rectangular pin shape into a list of track locations,layers.
        If no pins are "on-grid" (i.e. sufficient overlap)
        it makes the one with most overlap if it is not blocked.
        If expansion>0, expamine areas beyond the current pin
        when it is blocked.
        """
        (ll, ur) = pin.rect
        debug.info(3, "Converting pin [ {0} , {1} ]".format(ll, ur))

        # scale the size bigger to include neaby tracks
        ll_scaled = ll.scale(self.track_factor).floor()
        ur_scaled = ur.scale(self.track_factor).ceil()

        # Keep tabs on tracks with sufficient and insufficient overlap
        sufficient_list = set()
        insufficient_list = set()

        zindex = self.get_zindex(pin.lpp)
        for x in range(int(ll_scaled[0]) - expansion, int(ur_scaled[0]) + 1 + expansion):
            for y in range(int(ll_scaled[1] - expansion), int(ur_scaled[1]) + 1 + expansion):
                cur_grid = vector3d(x, y, zindex)
                (full_overlap, partial_overlap) = self.convert_pin_coord_to_tracks(pin, cur_grid)
                if full_overlap:
                    sufficient_list.update([full_overlap])
                if partial_overlap:
                    insufficient_list.update([partial_overlap])
                debug.info(3,
                           "Converting [ {0} , {1} ] full={2}".format(x,
                                                                      y,
                                                                      full_overlap))

        # Return all grids with any potential overlap (sufficient or not)
        return (sufficient_list, insufficient_list)

    def get_all_offgrid_pin(self, pin, insufficient_list):
        """
        Find a list of all pins with some overlap.
        """
        # print("INSUFFICIENT LIST",insufficient_list)
        # Find the coordinate with the most overlap
        any_overlap = set()
        for coord in insufficient_list:
            full_pin = self.convert_track_to_pin(coord)
            # Compute the overlap with that rectangle
            overlap_rect = pin.compute_overlap(full_pin)
            # Determine the max x or y overlap
            max_overlap = max(overlap_rect)
            if max_overlap > 0:
                any_overlap.update([coord])

        return any_overlap

    def get_best_offgrid_pin(self, pin, insufficient_list):
        """
        Find a list of the single pin with the most overlap.
        """
        # Find the coordinate with the most overlap
        best_coord = None
        best_overlap = -math.inf
        for coord in insufficient_list:
            full_pin = self.convert_track_to_pin(coord)
            # Compute the overlap with that rectangle
            overlap_rect = pin.compute_overlap(full_pin)
            # Determine the min x or y overlap
            min_overlap = min(overlap_rect)
            if min_overlap > best_overlap:
                best_overlap = min_overlap
                best_coord = coord

        return set([best_coord])

    def get_furthest_offgrid_pin(self, pin, insufficient_list):
        """
        Get a grid cell that is the furthest from the blocked grids.
        """

        # Find the coordinate with the most overlap
        best_coord = None
        best_dist = math.inf
        for coord in insufficient_list:
            min_dist = grid_utils.distance_set(coord, self.blocked_grids)
            if min_dist < best_dist:
                best_dist = min_dist
                best_coord = coord

        return set([best_coord])

    def get_nearest_offgrid_pin(self, pin, insufficient_list):
        """
        Given a pin and a list of grid cells (probably non-overlapping),
        return the nearest grid cell (center to center).
        """
        # Find the coordinate with the most overlap
        best_coord = None
        best_dist = math.inf
        for coord in insufficient_list:
            track_pin = self.convert_track_to_pin(coord)
            min_dist = pin.distance(track_pin)
            if min_dist < best_dist:
                best_dist = min_dist
                best_coord = coord

        return set([best_coord])

    def break_on_grids(self, tracks, xvals, yvals):
        track_list = []
        for x in xvals:
            for y in yvals:
                track_list.append(vector3d(x, y, 0))
                track_list.append(vector3d(x, y, 1))

        for current in tracks:
            if current in track_list:
                breakpoint()

    def divide_pin_to_tracks(self, pin, tracks):
        """
        Return a list of pin shape parts that are in the tracks.
        """
        # If pin is smaller than a track, just return it.
        track_pin = self.convert_track_to_shape_pin(list(tracks)[0])
        if pin.width() < track_pin.width() and pin.height() < track_pin.height():
            return [pin]

        overlap_pins = []
        for track in tracks:
            track_pin = self.convert_track_to_shape_pin(track)
            overlap_pin = track_pin.intersection(pin)

            # If pin is smaller than minwidth, in one dimension, skip it.
            min_pin_width = drc("minwidth_{0}". format(pin.layer))
            if not overlap_pin or (overlap_pin.width() < min_pin_width and overlap_pin.height() < min_pin_width):
                continue
            else:
                overlap_pins.append(overlap_pin)

        debug.check(len(overlap_pins) > 0, "No pins overlapped the tracks.")

        return overlap_pins


    def convert_pin_coord_to_tracks(self, pin, coord):
        """
        Return all tracks that an inflated pin overlaps
        """
        # This is using the full track shape rather
        # than a single track pin shape
        # because we will later patch a connector if there isn't overlap.
        track_pin = self.convert_track_to_shape_pin(coord)

        # This is the normal pin inflated by a minimum design rule
        inflated_pin = pin_layout(pin.name,
                                  pin.inflate(0.5 * self.track_space),
                                  pin.layer)

        overlap_length = pin.overlap_length(track_pin)
        debug.info(4,"Check overlap: {0} {1} . {2} = {3}".format(coord,
                                                                 pin.rect,
                                                                 track_pin,
                                                                 overlap_length))
        inflated_overlap_length = inflated_pin.overlap_length(track_pin)
        debug.info(4,"Check overlap: {0} {1} . {2} = {3}".format(coord,
                                                                 inflated_pin.rect,
                                                                 track_pin,
                                                                 inflated_overlap_length))

        # If it overlaps with the pin, it is sufficient
        if overlap_length == math.inf or overlap_length > 0:
            debug.info(4,"  Overlap: {0} >? {1}".format(overlap_length, 0))
            return (coord, None)
        # If it overlaps with the inflated pin, it is partial
        elif inflated_overlap_length == math.inf or inflated_overlap_length > 0:
            debug.info(4,"  Partial overlap: {0} >? {1}".format(inflated_overlap_length, 0))
            return (None, coord)
        else:
            debug.info(4, "  No overlap: {0} {1}".format(overlap_length, 0))
            return (None, None)

    def convert_track_to_pin(self, track):
        """
        Convert a grid point into a rectangle shape that is centered
        track in the track and leaves half a DRC space in each direction.
        """
        # calculate lower left
        x = track.x * self.track_width - 0.5 * self.track_width + 0.5 * self.track_space
        y = track.y * self.track_width - 0.5 * self.track_width + 0.5 * self.track_space
        ll = snap_to_grid(vector(x,y))

        # calculate upper right
        x = track.x * self.track_width + 0.5 * self.track_width - 0.5 * self.track_space
        y = track.y * self.track_width + 0.5 * self.track_width - 0.5 * self.track_space
        ur = snap_to_grid(vector(x, y))

        p = pin_layout("", [ll, ur], self.get_layer(track[2]))
        return p

    def convert_tracks_to_pin(self, tracks):
        """
        Convert a list of grid point into a rectangle shape.
        Must all be on the same layer.
        """
        for t in tracks:
            debug.check(t[2] == tracks[0][2], "Different layers used.")

        # For each shape, convert it to a pin
        pins = [self.convert_track_to_pin(t) for t in tracks]
        # Now find the bounding box
        minx = min([p.lx() for p in pins])
        maxx = max([p.rx() for p in pins])
        miny = min([p.by() for p in pins])
        maxy = max([p.uy() for p in pins])
        ll = vector(minx, miny)
        ur = vector(maxx, maxy)

        p = pin_layout("", [ll, ur], self.get_layer(tracks[0][2]))
        return p

    def convert_track_to_shape_pin(self, track):
        """
        Convert a grid point into a rectangle shape
        that occupies the entire centered track.
        """
        # to scale coordinates to tracks
        x = track[0]*self.track_width - 0.5*self.track_width
        y = track[1]*self.track_width - 0.5*self.track_width
        # offset lowest corner object to to (-track halo,-track halo)
        ll = snap_to_grid(vector(x, y))
        ur = snap_to_grid(ll + vector(self.track_width, self.track_width))

        p = pin_layout("", [ll, ur], self.get_layer(track[2]))
        return p

    def convert_track_to_shape(self, track):
        """
        Convert a grid point into a rectangle shape
        that occupies the entire centered track.
        """
        # to scale coordinates to tracks
        try:
            x = track[0]*self.track_width - 0.5*self.track_width
        except TypeError:
            debug.warning("{} {} {} {}".format(track[0], type(track[0]), self.track_width, type(self.track_width)))
        y = track[1]*self.track_width - 0.5*self.track_width
        # offset lowest corner object to to (-track halo,-track halo)
        ll = snap_to_grid(vector(x, y))
        ur = snap_to_grid(ll + vector(self.track_width, self.track_width))

        return [ll, ur]

    def convert_track_to_inflated_pin(self, track):
        """
        Convert a grid point into a rectangle shape
        that is inflated by a half DRC space.
        """
        # calculate lower left
        x = track.x*self.track_width - 0.5*self.track_width - 0.5*self.track_space
        y = track.y*self.track_width - 0.5*self.track_width - 0.5*self.track_space
        ll = snap_to_grid(vector(x,y))

        # calculate upper right
        x = track.x*self.track_width + 0.5*self.track_width + 0.5*self.track_space
        y = track.y*self.track_width + 0.5*self.track_width + 0.5*self.track_space
        ur = snap_to_grid(vector(x, y))

        p = pin_layout("", [ll, ur], self.get_layer(track[2]))
        return p

    def analyze_pins(self, pin_name):
        """
        Analyze the shapes of a pin and combine
        them into pin_groups which are connected.
        """
        debug.info(2, "Analyzing pin groups for {}.".format(pin_name))
        pin_set = self.pins[pin_name]

        # This will be a list of pin tuples that overlap
        overlap_list = []

        # Sort the rectangles into a list with lower/upper y coordinates
        bottom_y_coordinates = [(x.by(), x, "bottom") for x in pin_set]
        top_y_coordinates = [(x.uy(), x, "top") for x in pin_set]
        y_coordinates = bottom_y_coordinates + top_y_coordinates
        y_coordinates.sort(key=lambda x: x[0])

        # Map the pins to the lower indices
        bottom_index_map = {x[1]: i for i, x in enumerate(y_coordinates) if x[2] == "bottom"}
        # top_index_map = {x[1]: i for i, x in enumerate(y_coordinates) if x[2] == "bottom"}

        # Sort the pin list by x coordinate
        pin_list = list(pin_set)
        pin_list.sort(key=lambda x: x.lx())

        # for shapes in x order
        for pin in pin_list:
            # start at pin's lower y coordinate
            bottom_index = bottom_index_map[pin]
            compared_pins = set()
            for i in range(bottom_index, len(y_coordinates)):
                compare_pin = y_coordinates[i][1]
                # Don't overlap yourself
                if pin == compare_pin:
                    continue
                # Done when we encounter any shape above the pin
                if compare_pin.by() > pin.uy():
                    break
                # Don't double compare the same pin twice
                if compare_pin in compared_pins:
                    continue
                compared_pins.add(compare_pin)
                # If we overlap, add them to the list
                if pin.overlaps(compare_pin):
                    overlap_list.append((pin, compare_pin))

        # Initial unique group assignments
        group_id = {}
        gid = 1
        for pin in pin_list:
            group_id[pin] = gid
            gid += 1

        for p in overlap_list:
            (p1, p2) = p
            for pin in pin_list:
                if group_id[pin] == group_id[p2]:
                    group_id[pin] = group_id[p1]

        # For each pin add it to it's group
        group_map = {}
        for pin in pin_list:
            gid = group_id[pin]
            if gid not in group_map:
                group_map[gid] = pin_group(name=pin_name,
                                           pin_set=[],
                                           router=self)
            group_map[gid].add_pin(pin)

        self.pin_groups[pin_name] = list(group_map.values())

    def convert_pins(self, pin_name):
        """
        Convert the pin groups into pin tracks and blockage tracks.
        """
        debug.info(2, "Converting pins for {}.".format(pin_name))
        for pg in self.pin_groups[pin_name]:
            pg.convert_pin()

    def enclose_pins(self):
        """
        This will find the biggest rectangle enclosing some grid squares and
        put a rectangle over it. It does not enclose grid squares
        that are blocked by other shapes.
        """
        for pin_name in self.pin_groups:
            debug.info(2, "Enclosing pins for {}".format(pin_name))
            for pg in self.pin_groups[pin_name]:
                self.clear_blockages(pin_name)
                pg.enclose_pin()
                pg.add_enclosure(self.cell)

    def add_source(self, pin_name):
        """
        This will mark the grids for all pin components as a source.
        Marking as source or target also clears blockage status.
        """
        self.source_name = pin_name
        self.source_components = []
        for i in range(self.num_pin_components(pin_name)):
            self.add_pin_component_source(pin_name, i)

        # Clearing the blockage of this pin requires the inflated pins
        self.clear_blockages(pin_name)

    def add_target(self, pin_name):
        """
        This will mark the grids for all pin components as a target.
        Marking as source or target also clears blockage status.
        """
        self.target_name = pin_name
        self.target_components = []
        for i in range(self.num_pin_components(pin_name)):
            self.add_pin_component_target(pin_name, i)

        # Clearing the blockage of this pin requires the inflated pins
        self.clear_blockages(pin_name)

    def add_side_supply_pin(self, name, side="left", width=3, space=2):
        """
        Adds a supply pin to the perimeter and resizes the bounding box.
        """
        pg = pin_group(name, [], self)
        # Offset two spaces inside and one between the rings
        if name == "gnd":
            offset = width + 2 * space
        else:
            offset = space
        if side in ["left", "right"]:
            layers = [1]
        else:
            layers = [0]

        pg.grids = set(self.rg.get_perimeter_list(side=side,
                                                  width=width,
                                                  margin=self.margin,
                                                  offset=offset,
                                                  layers=layers))
        pg.enclosures = pg.compute_enclosures()
        pg.pins = set(pg.enclosures)
        debug.check(len(pg.pins)==1, "Too many pins for a side supply.")

        self.cell.pin_map[name].update(pg.pins)
        self.pin_groups[name].append(pg)

        self.new_pins[name] = pg.pins

    def add_ring_supply_pin(self, name, width=3, space=3):
        """
        Adds a ring supply pin that goes outside the given bbox.
        """
        pg = pin_group(name, [], self)

        # LEFT
        left_grids = set(self.rg.get_perimeter_list(side="left_ring",
                                                    width=width,
                                                    margin=self.margin,
                                                    offset=space,
                                                    layers=[1]))

        # RIGHT
        right_grids = set(self.rg.get_perimeter_list(side="right_ring",
                                                     width=width,
                                                     margin=self.margin,
                                                     offset=space,
                                                     layers=[1]))
        # TOP
        top_grids = set(self.rg.get_perimeter_list(side="top_ring",
                                                   width=width,
                                                   margin=self.margin,
                                                   offset=space,
                                                   layers=[0]))
        # BOTTOM
        bottom_grids = set(self.rg.get_perimeter_list(side="bottom_ring",
                                                      width=width,
                                                      margin=self.margin,
                                                      offset=space,
                                                      layers=[0]))

        horizontal_layer_grids = left_grids | right_grids

        # Must move to the same layer to find layer 1 corner grids
        vertical_layer_grids = set()
        for x in top_grids | bottom_grids:
            vertical_layer_grids.add(vector3d(x.x, x.y, 1))

        # Add vias in the overlap points
        horizontal_corner_grids = vertical_layer_grids & horizontal_layer_grids
        corners = []
        for g in horizontal_corner_grids:
            self.add_via(g)

        # The big pin group, but exclude the corners from the pins
        pg.grids = (left_grids | right_grids | top_grids | bottom_grids)
        pg.enclosures = pg.compute_enclosures()
        pg.pins = set(pg.enclosures)

        self.cell.pin_map[name].update(pg.pins)
        self.pin_groups[name].append(pg)
        self.new_pins[name] = pg.pins

        # Update the bbox so that it now includes the new pins
        for p in pg.pins:
            if p.lx() < self.ll.x or p.by() < self.ll.y:
                self.ll = p.ll()
            if p.rx() > self.ur.x or p.uy() > self.ur.y:
                self.ur = p.ur()
        self.bbox = (self.ll, self.ur)
        self.create_routing_grid()

    def get_new_pins(self, name):
        return self.new_pins[name]

    def add_perimeter_target(self, side="all"):
        """
        This will mark all the cells on the perimeter of the original layout as a target.
        """
        self.target_name = ""
        self.target_components = []
        self.rg.add_perimeter_target(side=side)

    def num_pin_components(self, pin_name):
        """
        This returns how many disconnected pin components there are.
        """
        return len(self.pin_groups[pin_name])

    def set_pin_component_source(self, pin_name, index):
        """
        Add the pin component but also set it as the exclusive one.
        Used by supply routing with multiple components.
        """
        self.source_name = pin_name
        self.source_components = []
        self.add_pin_component_source(pin_name, index)

    def add_pin_component_source(self, pin_name, index):
        """
        This will mark only the pin tracks
        from the indexed pin component as a source.
        It also unsets it as a blockage.
        """
        debug.check(index<self.num_pin_components(pin_name),
                    "Pin component index too large.")

        self.source_components.append(index)
        pin_in_tracks = self.pin_groups[pin_name][index].grids
        debug.info(3,"Set source: " + str(pin_name) + " " + str(pin_in_tracks))
        self.rg.add_source(pin_in_tracks)

    def add_path_target(self, paths):
        """
        Set all of the paths as a target too.
        """
        for p in paths:
            self.rg.set_target(p)
            self.rg.set_blocked(p, False)

    def set_pin_component_target(self, pin_name, index):
        """
        Add the pin component but also set it as the exclusive one.
        Used by supply routing with multiple components.
        """
        self.target_name = pin_name
        self.target_components = []
        self.add_pin_component_target(pin_name, index)

    def add_pin_component_target(self, pin_name, index):
        """
        This will mark only the pin tracks
        from the indexed pin component as a target.
        It also unsets it as a blockage.
        """
        debug.check(index<self.num_pin_components(pin_name),"Pin component index too large.")

        self.target_components.append(index)
        pin_in_tracks = self.pin_groups[pin_name][index].grids
        debug.info(3, "Set target: " + str(pin_name) + " " + str(pin_in_tracks))
        self.rg.add_target(pin_in_tracks)

    def add_pin_component_target_except(self, pin_name, index):
        """
        This will mark the grids for all *other* pin components as a target.
        Marking as source or target also clears blockage status.
        """
        for i in range(self.num_pin_components(pin_name)):
            if i != index:
                self.add_pin_component_target(pin_name, i)

    def set_component_blockages(self, pin_name, value=True):
        """
        Block all of the pin components.
        """
        debug.info(3, "Setting blockages {0} {1}".format(pin_name,value))
        for pg in self.pin_groups[pin_name]:
            self.set_blockages(pg.grids, value)

    def prepare_path(self,path):
        """
        Prepare a path or wave for routing ebedding.
        This tracks the path, simplifies the path and
        marks it as a path for debug output.
        """
        debug.info(4, "Set path: " + str(path))

        # This is marked for debug
        path.set_path()

        # For debugging... if the path failed to route.
        # if False or path == None:
        #     self.write_debug_gds()

        # First, simplify the path for
        # debug.info(3, str(self.path))
        contracted_path = self.contract_path(path)
        debug.info(3, "Contracted path: " + str(contracted_path))

        return contracted_path

    def add_route(self, path):
        """
        Add the current wire route to the given design instance.
        """
        prepared_path = self.prepare_path(path)

        debug.info(4, "Adding route: {}".format(str(prepared_path)))

        # convert the path back to absolute units from tracks
        # This assumes 1-track wide again
        abs_path = [self.convert_point_to_units(x[0]) for x in prepared_path]

        if len(self.layers) > 1:
            self.cell.add_route(layers=self.layers,
                                coordinates=abs_path,
                                layer_widths=self.layer_widths)
        else:
            self.cell.add_path(layer=self.layers[0],
                               coordinates=abs_path,
                               width=self.layer_widths[0])

    def create_route_connector(self, path_tracks, pin_name, components):
        """
        Find a rectangle to connect the track and the off-grid pin of a component.
        """

        if len(path_tracks) == 0 or len(components) == 0:
            return

        # Find the track pin
        track_pins = [self.convert_tracks_to_pin(x) for x in path_tracks]

        # Convert the off-grid pin into parts in each routing grid
        offgrid_pin_parts = []
        for component in components:
            pg = self.pin_groups[pin_name][component]
            for pin in pg.pins:
                # Layer min with
                min_width = drc("minwidth_{}".format(pin.layer))

                # If we intersect, by a min_width, we are done!
                for track_pin in track_pins:
                    intersection = pin.intersection(track_pin)
                    if intersection and intersection.width() > min_width and intersection.height() > min_width:
                        return

                #self.break_on_grids(pg.grids, xvals=[68], yvals=range(93,100))
                partial_pin_parts = self.divide_pin_to_tracks(pin, pg.grids)
                offgrid_pin_parts.extend(partial_pin_parts)

        debug.check(len(offgrid_pin_parts) > 0, "No offgrid pin parts found.")

        # Find closest part
        closest_track_pin, closest_part_pin = self.find_closest_pin(track_pins, offgrid_pin_parts)

        debug.check(closest_track_pin and closest_part_pin, "Found no closest pins.")

        # Find the bbox of the on-grid track and the off-grid pin part
        closest_track_pin.bbox([closest_part_pin])

        # Connect to off grid pin to track pin with closest shape
        self.cell.add_rect(layer=closest_track_pin.layer,
                           offset=closest_track_pin.ll(),
                           width=closest_track_pin.width(),
                           height=closest_track_pin.height())

    def find_closest_pin(self, first_list, second_list):
        """
        Find the closest pin in the lists. Does a stupid O(n^2).
        """
        min_dist = None
        min_item = (None, None)
        for pin1 in first_list:
            for pin2 in second_list:
                if pin1.layer != pin2.layer:
                    continue
                new_dist = pin1.distance(pin2)
                if min_dist == None or new_dist < min_dist:
                    min_item = (pin1, pin2)
                    min_dist = new_dist

        return min_item


    def add_single_enclosure(self, track):
        """
        Add a metal enclosure that is the size of
        the routing grid minus a spacing on each side.
        """
        pin = self.convert_track_to_pin(track)
        (ll, ur) = pin.rect
        self.cell.add_rect(layer=self.get_layer(track.z),
                           offset=ll,
                           width=ur.x-ll.x,
                           height=ur.y-ll.y)

    def add_via(self, loc, size=1):
        """
        Add a via centered at the current location
        """
        loc = self.convert_point_to_units(vector3d(loc[0], loc[1], 0))
        self.cell.add_via_center(layers=self.layers,
                                 offset=vector(loc.x, loc.y),
                                 size=(size, size))

    def compute_pin_enclosure(self, ll, ur, zindex, name=""):
        """
        Enclose the tracks from ll to ur in a single rectangle that meets
        the track DRC rules.
        """
        layer = self.get_layer(zindex)

        # This finds the pin shape enclosed by the
        # track with DRC spacing on the sides
        pin = self.convert_track_to_pin(ll)
        (abs_ll, unused) = pin.rect
        pin = self.convert_track_to_pin(ur)
        (unused, abs_ur) = pin.rect

        pin = pin_layout(name, [abs_ll, abs_ur], layer)

        return pin

    def contract_path(self, path):
        """
        Remove intermediate points in a rectilinear path or a wave.
        """
        # Waves are always linear, so just return the first and last.
        if self.is_wave(path):
            return [path[0], path[-1]]

        # Make a list only of points that change inertia of the path
        newpath = [path[0]]
        for i in range(1, len(path) - 1):
            prev_inertia = self.get_inertia(path[i-1][0], path[i][0])
            next_inertia = self.get_inertia(path[i][0], path[i+1][0])
            # if we switch directions, add the point, otherwise don't
            if prev_inertia != next_inertia:
                newpath.append(path[i])

        # always add the last path unless it was a single point
        if len(path) > 1:
            newpath.append(path[-1])
        return newpath

    def run_router(self, detour_scale):
        """
        This assumes the blockages, source, and target are all set up.
        """

        # Double check source and taget are not same node, if so, we are done!
        for k, v in self.rg.map.items():
            if v.source and v.target:
                self.paths.append([k])
                return True

        # returns the path in tracks
        (path, cost) = self.rg.route(detour_scale)
        if path:
            debug.info(2, "Found path: cost={0} {1}".format(cost, str(path)))

            self.paths.append(grid_utils.flatten_set(path))
            self.add_route(path)
            self.create_route_connector(path,
                                        self.source_name,
                                        self.source_components)
            self.create_route_connector(path,
                                        self.target_name,
                                        self.target_components)
            self.path_blockages.append(self.paths[-1])
            #self.write_debug_gds("debug_route.gds", False)
            #breakpoint()
            return True
        else:
            return False

    def annotate_pin_and_tracks(self, pin, tracks):
        """"
        Annotate some shapes for debug purposes
        """
        debug.info(0, "Annotating\n  pin {0}\n  tracks {1}".format(pin, tracks))
        for coord in tracks:
            (ll, ur) = self.convert_track_to_shape(coord)
            self.cell.add_rect(layer="text",
                               offset=ll,
                               width=ur[0] - ll[0],
                               height=ur[1] - ll[1])
            # (ll, ur) = self.convert_track_to_pin(coord).rect
            # self.cell.add_rect(layer="boundary",
            #                    offset=ll,
            #                    width=ur[0] - ll[0],
            #                    height=ur[1] - ll[1])
            (ll, ur) = pin.rect
            self.cell.add_rect(layer="text",
                               offset=ll,
                               width=ur[0] - ll[0],
                               height=ur[1] - ll[1])

    def write_debug_gds(self, gds_name="debug_route.gds", stop_program=True):
        """
        Write out a GDS file with the routing grid and
        search information annotated on it.
        """
        debug.info(0, "Writing annotated router gds file to {}".format(gds_name))
        self.add_router_info()
        self.cell.gds_write(gds_name)
        self.del_router_info()

        if stop_program:
            import sys
            sys.exit(1)

    def annotate_grid(self, g):
        """
        Display grid information in the GDS file for a single grid cell.
        """
        shape = self.convert_track_to_shape(g)
        partial_track = vector(0, self.track_width / 6.0)
        self.cell.add_rect(layer="text",
                           offset=shape[0],
                           width=shape[1].x - shape[0].x,
                           height=shape[1].y - shape[0].y)
        t = self.rg.map[g].get_type()

        # midpoint offset
        off = vector((shape[1].x + shape[0].x) / 2,
                     (shape[1].y + shape[0].y) / 2)
        if t:
            if g[2] == 1:
                # Upper layer is upper right label
                type_off = off + partial_track
            else:
                # Lower layer is lower left label
                type_off = off - partial_track
            self.cell.add_label(text=str(t),
                                layer="text",
                                offset=type_off)

        t = self.rg.map[g].get_cost()
        partial_track = vector(self.track_width/6.0, 0)
        if t:
            if g[2] == 1:
                # Upper layer is right label
                type_off = off + partial_track
            else:
                # Lower layer is left label
                type_off = off - partial_track
            self.cell.add_label(text=str(t),
                                layer="text",
                                offset=type_off)

        self.cell.add_label(text="{0},{1}".format(g[0], g[1]),
                            layer="text",
                            offset=shape[0])

    def del_router_info(self):
        """
        Erase all of the comments on the current level.
        """
        debug.info(2, "Erasing router info")
        lpp = techlayer["text"]
        self.cell.objs = [x for x in self.cell.objs if x.lpp != lpp]

    def add_router_info(self):
        """
        Write the routing grid and router cost, blockage, pins on
        the boundary layer for debugging purposes. This can only be
        called once or the labels will overlap.
        """
        debug.info(2, "Adding router info")

        show_bbox = False
        show_blockages = False
        show_blockage_grids = False
        show_enclosures = False
        show_all_grids = True

        if show_bbox:
            self.cell.add_rect(layer="text",
                               offset=vector(self.ll.x, self.ll.y),
                               width=self.ur.x - self.ll.x,
                               height=self.ur.y - self.ll.y)

        if show_all_grids:
            for g in self.rg.map:
                self.annotate_grid(g)

        if show_blockages:
            # Display the inflated blockage
            for blockage in self.blockages:
                debug.info(1, "Adding {}".format(blockage))
                (ll, ur) = blockage.inflate()
                self.cell.add_rect(layer="text",
                                   offset=ll,
                                   width=ur.x - ll.x,
                                   height=ur.y - ll.y)
        if show_blockage_grids:
            self.set_blockages(self.blocked_grids, True)
            for g in self.rg.map:
                self.annotate_grid(g)

        if show_enclosures:
            for key in self.pin_groups:
                for pg in self.pin_groups[key]:
                    if not pg.enclosed:
                        continue
                    for pin in pg.enclosures:
                        # print("enclosure: ",
                        # pin.name,
                        # pin.ll(),
                        # pin.width(),
                        # pin.height())
                        self.cell.add_rect(layer="text",
                                           offset=pin.ll(),
                                           width=pin.width(),
                                           height=pin.height())

    def get_perimeter_pin(self):
        """ Return the shape of the last routed path that was on the perimeter """
        lastpath = self.paths[-1]
        for v in lastpath:
            if self.rg.is_target(v):
                # Find neighboring grid to make double wide pin
                neighbor = v + vector3d(0, 1, 0)
                if neighbor in lastpath:
                    return self.convert_tracks_to_pin([v, neighbor])
                neighbor = v + vector3d(0, -1, 0)
                if neighbor in lastpath:
                    return self.convert_tracks_to_pin([v, neighbor])
                neighbor = v + vector3d(1, 0, 0)
                if neighbor in lastpath:
                    return self.convert_tracks_to_pin([v, neighbor])
                neighbor = v + vector3d(-1, 0, 0)
                if neighbor in lastpath:
                    return self.convert_tracks_to_pin([v, neighbor])

                # Else if we came from a different layer, we can only add
                # a signle grid
                return self.convert_track_to_pin(v)

        return None

    def get_ll_pin(self, pin_name):
        """ Return the lowest, leftest pin group """

        keep_pin = None
        for index, pg in enumerate(self.pin_groups[pin_name]):
            for pin in pg.enclosures:
                if not keep_pin:
                    keep_pin = pin
                else:
                    if pin.lx() <= keep_pin.lx() and pin.by() <= keep_pin.by():
                        keep_pin = pin

        return keep_pin

    def check_all_routed(self, pin_name):
        """
        Check that all pin groups are routed.
        """
        for pg in self.pin_groups[pin_name]:
            if not pg.is_routed():
                return False


# FIXME: This should be replaced with vector.snap_to_grid at some point
def snap_to_grid(offset):
    """
    Changes the coodrinate to match the grid settings
    """
    xoff = snap_val_to_grid(offset[0])
    yoff = snap_val_to_grid(offset[1])
    return vector(xoff, yoff)


def snap_val_to_grid(x):
    grid = drc("grid")
    xgrid = int(round(round((x / grid), 2), 0))
    xoff = xgrid * grid
    return xoff
