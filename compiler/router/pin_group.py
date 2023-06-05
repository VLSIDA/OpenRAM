# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.base.pin_layout import pin_layout
from .direction import direction


class pin_group:
    """
    A class to represent a group of rectangular design pin.
    It requires a router to define the track widths and blockages which
    determine how pin shapes get mapped to tracks.
    It is initially constructed with a single set of (touching) pins.
    """

    def __init__(self, name, pin_set, router):
        self.name = name
        # Flag for when it is routed
        self.routed = False
        # Flag for when it is enclosed
        self.enclosed = False

        # This is a list because we can have a pin
        # group of disconnected sets of pins
        # and these are represented by separate lists
        self.pins = set(pin_set)
        # Remove any redundant pins (i.e. contained in other pins)
        self.remove_redundant_pins()

        self.router = router
        # These are the corresponding pin grids for each pin group.
        self.grids = set()
        # These are the secondary grids that could
        # or could not be part of the pin
        self.secondary_grids = set()

        # The set of blocked grids due to this pin
        self.blockages = set()

        # This is a set of pin_layout shapes to cover the grids
        self.enclosures = set()

    def __str__(self):
        """ override print function output """
        total_string = "(pg {} ".format(self.name)

        pin_string = "\n  pins={}".format(self.pins)
        total_string += pin_string

        grids_string = "\n  grids={}".format(self.grids)
        total_string += grids_string

        grids_string = "\n  secondary={}".format(self.secondary_grids)
        total_string += grids_string

        if self.enclosed:
            enclosure_string = "\n  enclose={}".format(self.enclosures)
            total_string += enclosure_string

        total_string += ")"
        return total_string

    def add_pin(self, pin):
        self.pins.add(pin)
        self.remove_redundant_pins()

    def __repr__(self):
        """ override repr function output """
        return str(self)

    def size(self):
        return len(self.grids)

    def set_routed(self, value=True):
        self.routed = value

    def is_routed(self):
        return self.routed

    def remove_redundant_pins(self):
        """
        Remove redundant pin shapes
        """
        new_pin_list = self.remove_redundant_shapes(list(self.pins))
        self.pins = set(new_pin_list)

    def remove_redundant_shapes(self, pin_list):
        """
        Remove any pin layout that is contained within another.
        Returns a new list without modifying pin_list.
        """
        local_debug = False
        if local_debug:
            debug.info(0, "INITIAL: {}".format(pin_list))

        add_indices = set(range(len(pin_list)))
        # This is n^2, but the number is small
        for index1, pin1 in enumerate(pin_list):
            # If we remove this pin, it can't contain other pins
            if index1 not in add_indices:
                continue

            for index2, pin2 in enumerate(pin_list):
                # Can't contain yourself,
                # but compare the indices and not the pins
                # so you can remove duplicate copies.
                if index1 == index2:
                    continue
                # If we already removed it, can't remove it again...
                if index2 not in add_indices:
                    continue

                if pin1.contains(pin2):
                    if local_debug:
                        debug.info(0, "{0} contains {1}".format(pin1, pin2))
                    add_indices.remove(index2)

        new_pin_list = [pin_list[x] for x in add_indices]

        if local_debug:
            debug.info(0, "FINAL  : {}".format(new_pin_list))

        return new_pin_list

    def compute_enclosures(self):
        """
        Find the minimum rectangle enclosures of the given tracks.
        """
        # Enumerate every possible enclosure
        pin_list = []
        for seed in self.grids:
            (ll, ur) = self.enclose_pin_grids(seed,
                                              direction.NORTH,
                                              direction.EAST)
            enclosure = self.router.compute_pin_enclosure(ll, ur, ll.z)
            pin_list.append(enclosure)

            (ll, ur) = self.enclose_pin_grids(seed,
                                              direction.EAST,
                                              direction.NORTH)
            enclosure = self.router.compute_pin_enclosure(ll, ur, ll.z)
            pin_list.append(enclosure)

        if len(pin_list) == 0:
            debug.error("Did not find any enclosures for {}".format(self.name))
            self.router.write_debug_gds("pin_enclosure_error.gds")

        # Now simplify the enclosure list
        new_pin_list = self.remove_redundant_shapes(pin_list)

        # Now add the right name
        for pin in new_pin_list:
            pin.name = self.name

        debug.check(len(new_pin_list) > 0,
                    "Did not find any enclosures.")

        return new_pin_list

    def compute_connector(self, pin, enclosure):
        """
        Compute a shape to connect the pin to the enclosure shape.
        This assumes the shape will be the dimension of the pin.
        """
        if pin.xoverlaps(enclosure):
            # Is it vertical overlap, extend pin shape to enclosure
            plc = pin.lc()
            prc = pin.rc()
            elc = enclosure.lc()
            # erc = enclosure.rc()
            ymin = min(plc.y, elc.y)
            ymax = max(plc.y, elc.y)
            ll = vector(plc.x, ymin)
            ur = vector(prc.x, ymax)
        elif pin.yoverlaps(enclosure):
            # Is it horizontal overlap, extend pin shape to enclosure
            pbc = pin.bc()
            puc = pin.uc()
            ebc = enclosure.bc()
            # euc = enclosure.uc()
            xmin = min(pbc.x, ebc.x)
            xmax = max(pbc.x, ebc.x)
            ll = vector(xmin, pbc.y)
            ur = vector(xmax, puc.y)
        else:
            # Neither, so we must do a corner-to corner
            pc = pin.center()
            ec = enclosure.center()
            xmin = min(pc.x, ec.x)
            xmax = max(pc.x, ec.x)
            ymin = min(pc.y, ec.y)
            ymax = max(pc.y, ec.y)
            ll = vector(xmin, ymin)
            ur = vector(xmax, ymax)

        if ll.x == ur.x or ll.y == ur.y:
            return None
        p = pin_layout(pin.name, [ll, ur], pin.layer)
        return p

    def find_above_connector(self, pin, enclosures):
        """
        Find the enclosure that is to above the pin
        and make a connector to it's upper edge.
        """
        # Create the list of shapes that contain the pin edge
        edge_list = []
        for shape in enclosures:
            if shape.xcontains(pin):
                edge_list.append(shape)

        # Sort them by their bottom edge
        edge_list.sort(key=lambda x: x.by(), reverse=True)

        # Find the bottom edge that is next to the pin's top edge
        above_item = None
        for item in edge_list:
            if item.by() >= pin.uy():
                above_item = item
            else:
                break

        # There was nothing
        if not above_item:
            return None
        # If it already overlaps, no connector needed
        if above_item.overlaps(pin):
            return None

        # Otherwise, make a connector to the item
        p = self.compute_connector(pin, above_item)
        return p

    def find_below_connector(self, pin, enclosures):
        """
        Find the enclosure that is below the pin
        and make a connector to it's upper edge.
        """
        # Create the list of shapes that contain the pin edge
        edge_list = []
        for shape in enclosures:
            if shape.xcontains(pin):
                edge_list.append(shape)

        # Sort them by their upper edge
        edge_list.sort(key=lambda x: x.uy())

        # Find the upper edge that is next to the pin's bottom edge
        bottom_item = None
        for item in edge_list:
            if item.uy() <= pin.by():
                bottom_item = item
            else:
                break

        # There was nothing to the left
        if not bottom_item:
            return None
        # If it already overlaps, no connector needed
        if bottom_item.overlaps(pin):
            return None

        # Otherwise, make a connector to the item
        p = self.compute_connector(pin, bottom_item)
        return p

    def find_left_connector(self, pin, enclosures):
        """
        Find the enclosure that is to the left of the pin
        and make a connector to it's right edge.
        """
        # Create the list of shapes that contain the pin edge
        edge_list = []
        for shape in enclosures:
            if shape.ycontains(pin):
                edge_list.append(shape)

        # Sort them by their right edge
        edge_list.sort(key=lambda x: x.rx())

        # Find the right edge that is to the pin's left edge
        left_item = None
        for item in edge_list:
            if item.rx() <= pin.lx():
                left_item = item
            else:
                break

        # There was nothing to the left
        if not left_item:
            return None
        # If it already overlaps, no connector needed
        if left_item.overlaps(pin):
            return None

        # Otherwise, make a connector to the item
        p = self.compute_connector(pin, left_item)
        return p

    def find_right_connector(self, pin, enclosures):
        """
        Find the enclosure that is to the right of the pin
        and make a connector to it's left edge.
        """
        # Create the list of shapes that contain the pin edge
        edge_list = []
        for shape in enclosures:
            if shape.ycontains(pin):
                edge_list.append(shape)

        # Sort them by their right edge
        edge_list.sort(key=lambda x: x.lx(), reverse=True)

        # Find the left edge that is next to the pin's right edge
        right_item = None
        for item in edge_list:
            if item.lx() >= pin.rx():
                right_item = item
            else:
                break

        # There was nothing to the right
        if not right_item:
            return None
        # If it already overlaps, no connector needed
        if right_item.overlaps(pin):
            return None

        # Otherwise, make a connector to the item
        p = self.compute_connector(pin, right_item)
        return p

    def find_smallest_connector(self, pin_list, shape_list):
        """
        Compute all of the connectors between the overlapping
        pins and enclosure shape list.
        Return the smallest.
        """
        smallest = None
        for pin in pin_list:
            for enclosure in shape_list:
                new_enclosure = self.compute_connector(pin, enclosure)
                if not smallest or new_enclosure.area() < smallest.area():
                    smallest = new_enclosure

        return smallest

    def find_smallest_overlapping(self, pin_list, shape_list):
        """
        Find the smallest area shape in shape_list that overlaps with any
        pin in pin_list by a min width.
        """

        smallest_shape = None
        for pin in pin_list:
            overlap_shape = self.find_smallest_overlapping_pin(pin, shape_list)
            if overlap_shape:
                # overlap_length = pin.overlap_length(overlap_shape)
                if not smallest_shape or overlap_shape.area() < smallest_shape.area():
                    smallest_shape = overlap_shape

        return smallest_shape

    def find_smallest_overlapping_pin(self, pin, shape_list):
        """
        Find the smallest area shape in shape_list that overlaps with any
        pin in pin_list by a min width.
        """

        smallest_shape = None
        zindex = self.router.get_zindex(pin.lpp[0])
        (min_width, min_space) = self.router.get_layer_width_space(zindex)

        # Now compare it with every other shape to check how much they overlap
        for other in shape_list:
            overlap_length = pin.overlap_length(other)
            if overlap_length > min_width:
                if not smallest_shape or other.area() < smallest_shape.area():
                    smallest_shape = other

        return smallest_shape

    def overlap_any_shape(self, pin_list, shape_list):
        """
        Does the given pin overlap any of the shapes in the pin list.
        """
        for pin in pin_list:
            for other in shape_list:
                if pin.overlaps(other):
                    return True

        return False

    def max_pin_layout(self, pin_list):
        """
        Return the max area pin_layout
        """
        biggest = pin_list[0]
        for pin in pin_list:
            if pin.area() > biggest.area():
                biggest = pin

        return pin

    def enclose_pin_grids(self, ll, dir1=direction.NORTH, dir2=direction.EAST):
        """
        This encloses a single pin component with a rectangle
        starting with the seed and expanding dir1 until blocked
        and then dir2 until blocked.
        dir1 and dir2 should be two orthogonal directions.
        """

        offset1 = direction.get_offset(dir1)
        offset2 = direction.get_offset(dir2)

        # We may have started with an empty set
        debug.check(len(self.grids) > 0, "Cannot seed an grid empty set.")

        common_blockages = self.router.get_blocked_grids() & self.grids

        # Start with the ll and make the widest row
        row = [ll]
        # Move in dir1 while we can
        while True:
            next_cell = row[-1] + offset1
            # Can't move if not in the pin shape
            if next_cell in self.grids and next_cell not in common_blockages:
                row.append(next_cell)
            else:
                break
        # Move in dir2 while we can
        while True:
            next_row = [x + offset2 for x in row]
            for cell in next_row:
                # Can't move if any cell is not in the pin shape
                if cell not in self.grids or cell in common_blockages:
                    break
            else:
                row = next_row
                # Skips the second break
                continue
            # Breaks from the nested break
            break

        # Add a shape from ll to ur
        ur = row[-1]
        return (ll, ur)

    def enclose_pin(self):
        """
        If there is one set of connected pin shapes,
        this will find the smallest rectangle enclosure that
        overlaps with any pin.
        If there is not, it simply returns all the enclosures.
        """
        self.enclosed = True

        # Compute the enclosure pin_layout list of the set of tracks
        self.enclosures = self.compute_enclosures()

        # Find a connector to every pin and add it to the enclosures
        for pin in self.pins:

            # If it is contained, it won't need a connector
            if pin.contained_by_any(self.enclosures):
                continue

            # Find a connector in the cardinal directions
            # If there is overlap, but it isn't contained,
            # these could all be None
            # These could also be none if the pin is
            # diagonal from the enclosure
            left_connector = self.find_left_connector(pin, self.enclosures)
            right_connector = self.find_right_connector(pin, self.enclosures)
            above_connector = self.find_above_connector(pin, self.enclosures)
            below_connector = self.find_below_connector(pin, self.enclosures)
            connector_list = [left_connector,
                              right_connector,
                              above_connector,
                              below_connector]
            filtered_list = list(filter(lambda x: x != None, connector_list))
            if (len(filtered_list) > 0):
                import copy
                bbox_connector = copy.copy(pin)
                bbox_connector.bbox(filtered_list)
                self.enclosures.append(bbox_connector)

        # Now, make sure each pin touches an enclosure.
        # If not, add another (diagonal) connector.
        # This could only happen when there was no enclosure
        # in any cardinal direction from a pin
        if not self.overlap_any_shape(self.pins, self.enclosures):
            connector = self.find_smallest_connector(self.pins,
                                                     self.enclosures)
            if not connector:
                debug.error("Could not find a connector for {} with {}".format(self.pins,
                                                                               self.enclosures))
                self.router.write_debug_gds("no_connector.gds")
            self.enclosures.append(connector)

        # At this point, the pins are overlapping,
        # but there might be more than one!
        overlap_set = set()
        for pin in self.pins:
            overlap_set.update(self.transitive_overlap(pin, self.enclosures))
        # Use the new enclosures and recompute the grids
        # that correspond to them
        if len(overlap_set) < len(self.enclosures):
            self.enclosures = overlap_set
            self.grids = set()
            # Also update the grid locations with the new
            # (possibly pruned) enclosures
            for enclosure in self.enclosures:
                (sufficient, insufficient) = self.router.convert_pin_to_tracks(self.name,
                                                                               enclosure)
                self.grids.update(sufficient)

        debug.info(3, "Computed enclosure(s) {0}\n  {1}\n  {2}\n  {3}".format(self.name,
                                                                              self.pins,
                                                                              self.grids,
                                                                              self.enclosures))

    def transitive_overlap(self, shape, shape_list):
        """
        Given shape, find the elements in shape_list that overlap transitively.
        I.e. if shape overlaps A and A overlaps B, return both A and B.
        """

        augmented_shape_list = set(shape_list)
        old_connected_set = set()
        connected_set = set([shape])
        # Repeat as long as we expand the set
        while len(connected_set) > len(old_connected_set):
            old_connected_set = connected_set
            connected_set = set([shape])
            for old_shape in old_connected_set:
                for cur_shape in augmented_shape_list:
                    if old_shape.overlaps(cur_shape):
                        connected_set.add(cur_shape)

        # Remove the original shape
        connected_set.remove(shape)

        # if len(connected_set)<len(shape_list):
        #     import pprint
        #     print("S: ",shape)
        #     pprint.pprint(shape_list)
        #     pprint.pprint(connected_set)

        return connected_set

    def add_enclosure(self, cell):
        """
        Add the enclosure shape to the given cell.
        """
        for enclosure in self.enclosures:
            debug.info(4, "Adding enclosure {0} {1}".format(self.name,
                                                            enclosure))
            cell.add_rect(layer=enclosure.layer,
                          offset=enclosure.ll(),
                          width=enclosure.width(),
                          height=enclosure.height())

    def perimeter_grids(self):
        """
        Return a list of the grids on the perimeter.
        This assumes that we have a single contiguous shape.
        """
        perimeter_set = set()
        cardinal_offsets = direction.cardinal_offsets()
        for g1 in self.grids:
            neighbor_grids = [g1 + offset for offset in cardinal_offsets]
            neighbor_count = sum([x in self.grids for x in neighbor_grids])
            # If we aren't completely enclosed, we are on the perimeter
            if neighbor_count < 4:
                perimeter_set.add(g1)

        return perimeter_set

    def adjacent(self, other):
        """
        Chck if the two pin groups have at least one adjacent pin grid.
        """
        # We could optimize this to just check the boundaries
        for g1 in self.perimeter_grids():
            for g2 in other.perimeter_grids():
                if g1.adjacent(g2):
                    return True

        return False

    def adjacent_grids(self, other, separation):
        """
        Determine the sets of grids that are within a separation distance
        of any grid in the other set.
        """
        # We could optimize this to just check the boundaries
        adj_grids = set()
        for g1 in self.grids:
            for g2 in other.grids:
                if g1.distance(g2) <= separation:
                    adj_grids.add(g1)

        return adj_grids

    def convert_pin(self):
        """
        Convert the list of pin shapes into sets of routing grids.
        The secondary set of grids are "optional" pin shapes that
        should be either blocked or part of the pin.
        """
        # Set of tracks that overlap a pin
        pin_set = set()
        # Set of track adjacent to or paritally overlap a pin (not full DRC connection)
        partial_set = set()

        # for pin in self.pins:
        #     lx = pin.lx()
        #     ly = pin.by()
        #     if  lx > 87.9 and lx < 87.99 and ly > 18.56 and ly < 18.6:
        #         breakpoint()
        for pin in self.pins:
            debug.info(4, "  Converting {0}".format(pin))
            # Determine which tracks the pin overlaps
            (sufficient, insufficient) = self.router.convert_pin_to_tracks(self.name,
                                                                           pin)
            pin_set.update(sufficient)
            partial_set.update(insufficient)

            # Blockages will be a super-set of pins since
            # it uses the inflated pin shape.
            blockage_in_tracks = self.router.convert_blockage(pin)
            # Must include the pins here too because these are computed in a different
            # way than blockages.
            blockages = sufficient | insufficient | blockage_in_tracks
            self.blockages.update(blockages)

        # If we have a blockage, we must remove the grids
        # Remember, this excludes the pin blockages already
        blocked_grids = self.router.get_blocked_grids()
        pin_set.difference_update(blocked_grids)
        partial_set.difference_update(blocked_grids)

        # At least one of the groups must have some valid tracks
        if (len(pin_set) == 0 and len(partial_set) == 0):
            # debug.warning("Pin is very close to metal blockage.\nAttempting to expand blocked pin {}".format(self.pins))

            for pin in self.pins:
                debug.warning("  Expanding conversion {0}".format(pin))
                # Determine which tracks the pin overlaps
                (sufficient, insufficient) = self.router.convert_pin_to_tracks(self.name,
                                                                               pin,
                                                                               expansion=1)

                # This time, don't remove blockages in the hopes that it might be ok.
                # Could cause DRC problems!
                pin_set.update(sufficient)
                partial_set.update(insufficient)

            # If it's still empty, we must bail.
            if len(pin_set) == 0 and len(partial_set) == 0:
                debug.error("Unable to find unblocked pin {} {}".format(self.name,
                                                                        self.pins))
                self.router.write_debug_gds("blocked_pin.gds")

        # Consider the fully connected set first and if not the partial set
        # if len(pin_set) > 0:
        #     self.grids = pin_set
        # else:
        #     self.grids = partial_set
        # Just using the full set simplifies the enclosures, otherwise
        # we get some pin enclose DRC errors due to off grid pins
        self.grids = pin_set | partial_set
        if len(self.grids) < 0:
            debug.error("Did not find any unblocked grids: {}".format(str(self.pins)))
            self.router.write_debug_gds("blocked_pin.gds")

        # Remember the secondary grids for removing adjacent pins
        self.secondary_grids = partial_set

        debug.info(4, "     pins   {}".format(self.grids))
        debug.info(4, "     secondary {}".format(self.secondary_grids))
