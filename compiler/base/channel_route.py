# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import collections
from openram import debug
from openram.tech import drc
from .vector import vector
from .design import design


class channel_net():
    def __init__(self, net_name, pins, vertical):
        self.name = net_name
        self.pins = pins
        self.vertical = vertical

        # Keep track of the internval
        if vertical:
            self.min_value = min(i.by() for i in pins)
            self.max_value = max(i.uy() for i in pins)
        else:
            self.min_value = min(i.lx() for i in pins)
            self.max_value = max(i.rx() for i in pins)

        # Keep track of the conflicts
        self.conflicts = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.min_value < other.min_value

    def pin_overlap(self, pin1, pin2, pitch):
        """ Check for vertical or horizontal overlap of the two pins """

        # FIXME: If the pins are not in a row, this may break.
        # However, a top pin shouldn't overlap another top pin,
        # for example, so the extra comparison *shouldn't* matter.

        # Pin 1 must be in the "BOTTOM" set
        x_overlap = pin1.by() < pin2.by() and abs(pin1.center().x - pin2.center().x) < pitch

        # Pin 1 must be in the "LEFT" set
        y_overlap = pin1.lx() < pin2.lx() and abs(pin1.center().y - pin2.center().y) < pitch
        overlaps = (not self.vertical and x_overlap) or (self.vertical and y_overlap)
        return overlaps

    def pins_overlap(self, other, pitch):
        """
        Check all the pin pairs on two nets and return a pin
        overlap if any pin overlaps.
        """

        for pin1 in self.pins:
            for pin2 in other.pins:
                if self.pin_overlap(pin1, pin2, pitch):
                    return True

        return False

    def segment_overlap(self, other):
        """
        Check if the horizontal span of the two nets overlaps eachother.
        """
        min_overlap = self.min_value >= other.min_value and self.min_value <= other.max_value
        max_overlap = self.max_value >= other.min_value and self.max_value <= other.max_value
        return min_overlap or max_overlap


class channel_route(design):

    unique_id = 0

    def __init__(self,
                 netlist,
                 offset,
                 layer_stack,
                 directions=None,
                 vertical=False,
                 parent=None):
        """
        The net list is a list of the nets with each net being a list of pins
        to be connected. The offset is the lower-left of where the
        routing channel will start.  This does NOT try to minimize the
        number of tracks -- instead, it picks an order to avoid the
        vertical conflicts between pins. The track size must be the number of
        nets times the *nonpreferred* routing of the non-track layer pitch.

        """
        name = "cr_{0}".format(channel_route.unique_id)
        channel_route.unique_id += 1
        super().__init__(name)

        self.netlist = netlist
        self.offset = offset
        self.layer_stack = layer_stack
        self.directions = directions
        self.vertical = vertical
        # For debugging...
        self.parent = parent

        if not directions or directions == "pref":
            # Use the preferred layer directions
            if self.get_preferred_direction(layer_stack[0]) == "V":
                self.vertical_layer = layer_stack[0]
                self.horizontal_layer = layer_stack[2]
            else:
                self.vertical_layer = layer_stack[2]
                self.horizontal_layer = layer_stack[0]
        elif directions == "nonpref":
            # Use the preferred layer directions
            if self.get_preferred_direction(layer_stack[0]) == "V":
                self.vertical_layer = layer_stack[2]
                self.horizontal_layer = layer_stack[0]
            else:
                self.vertical_layer = layer_stack[0]
                self.horizontal_layer = layer_stack[2]
        else:
            # Use the layer directions specified to the router rather than
            # the preferred directions
            debug.check(directions[0] != directions[1], "Must have unique layer directions.")
            if directions[0] == "V":
                self.vertical_layer = layer_stack[0]
                self.horizontal_layer = layer_stack[2]
            else:
                self.horizontal_layer = layer_stack[0]
                self.vertical_layer = layer_stack[2]

        layer_stuff = self.get_layer_pitch(self.vertical_layer)
        (self.vertical_nonpref_pitch, self.vertical_pitch, self.vertical_width, self.vertical_space) = layer_stuff

        layer_stuff = self.get_layer_pitch(self.horizontal_layer)
        (self.horizontal_nonpref_pitch, self.horizontal_pitch, self.horizontal_width, self.horizontal_space) = layer_stuff

        self.route()

    def remove_net_from_graph(self, pin, g):
        """
        Remove the pin from the graph and all conflicts
        """
        g.pop(pin, None)

        # Remove the pin from all conflicts
        # FIXME: This is O(n^2), so maybe optimize it.
        for other_pin, conflicts in g.items():
            if pin in conflicts:
                g[other_pin].remove(pin)
        return g

    def route(self):
        # Create names for the nets for the graphs
        nets = []
        index = 0
        # print(self.netlist)
        for pin_list in self.netlist:
            nets.append(channel_net("n{}".format(index), pin_list, self.vertical))
            index += 1

        # Create the (undirected) horizontal constraint graph
        hcg = collections.OrderedDict()
        for net1 in nets:
            for net2 in nets:
                if net1.name == net2.name:
                    continue
                if net1.segment_overlap(net2):
                    try:
                        hcg[net1.name].add(net2.name)
                    except KeyError:
                        hcg[net1.name] = set([net2.name])
                    try:
                        hcg[net2.name].add(net1.name)
                    except KeyError:
                        hcg[net2.name] = set([net1.name])


        # Initialize the vertical conflict graph (vcg)
        # and make a list of all pins
        vcg = collections.OrderedDict()

        # print("Nets:")
        # for net_name in nets:
        #     print(net_name, [x.name for x in nets[net_name]])

        # Find the vertical pin conflicts
        # FIXME: O(n^2) but who cares for now
        if self.vertical:
            pitch = self.horizontal_nonpref_pitch
        else:
            pitch = self.vertical_nonpref_pitch

        for net in nets:
            vcg[net.name] = set()

        for net1 in nets:
            for net2 in nets:
                # Skip yourself
                if net1.name == net2.name:
                    continue

                if net1.pins_overlap(net2, pitch):
                    vcg[net2.name].add(net1.name)

        # Check if there are any cycles net1 <---> net2 in the VCG


        # Some of the pins may be to the left/below the channel offset,
        # so adjust if this is the case
        self.min_value = min([n.min_value for n in nets])
        self.max_value = min([n.max_value for n in nets])
        if self.vertical:
            real_channel_offset = vector(self.offset.x, min(self.min_value, self.offset.y))
        else:
            real_channel_offset = vector(min(self.min_value, self.offset.x), self.offset.y)
        current_offset = real_channel_offset

        # Sort nets by left edge value
        nets.sort()
        while len(nets) > 0:

            current_offset_value = current_offset.y if self.vertical else current_offset.x

            # from pprint import pformat
            # print("VCG:\n", pformat(vcg))
            # for name,net in vcg.items():
            #    print(name, net.min_value, net.max_value, net.conflicts)
            # print(current_offset)
            # get a route from conflict graph with empty fanout set
            for net in nets:
                # If it has no conflicts and the interval is to the right of the current offset in the track
                if net.min_value >= current_offset_value and len(vcg[net.name]) == 0:
                    # print("Routing {}".format(net.name))
                    # Add the trunk routes from the bottom up for
                    # horizontal or the left to right for vertical
                    if self.vertical:
                        self.add_vertical_trunk_route(net.pins,
                                                      current_offset,
                                                      self.horizontal_pitch)
                        current_offset = vector(current_offset.x, net.max_value + self.horizontal_nonpref_pitch)
                    else:
                        self.add_horizontal_trunk_route(net.pins,
                                                        current_offset,
                                                        self.vertical_pitch)
                        current_offset = vector(net.max_value + self.vertical_nonpref_pitch, current_offset.y)

                    # Remove the net from other constriants in the VCG
                    vcg = self.remove_net_from_graph(net.name, vcg)
                    nets.remove(net)

                    break
            else:
                # If we made a full pass and the offset didn't change...
                current_offset_value = current_offset.y if self.vertical else current_offset.x
                initial_offset_value = real_channel_offset.y if self.vertical else real_channel_offset.x
                if current_offset_value == initial_offset_value:
                    debug.info(0, "Channel offset: {}".format(real_channel_offset))
                    debug.info(0, "Current offset: {}".format(current_offset))
                    debug.info(0, "VCG {}".format(str(vcg)))
                    debug.info(0, "HCG {}".format(str(hcg)))
                    for net in nets:
                        debug.info(0, "{0} pin: {1}".format(net.name, str(net.pins)))
                    if self.parent:
                        debug.info(0, "Saving vcg.gds")
                        self.parent.gds_write("vcg.gds")
                    debug.error("Cyclic VCG in channel router.", -1)

                # Increment the track and reset the offset to the start (like a typewriter)
                if self.vertical:
                    current_offset = vector(current_offset.x + self.horizontal_nonpref_pitch, real_channel_offset.y)
                else:
                    current_offset = vector(real_channel_offset.x, current_offset.y + self.vertical_nonpref_pitch)

        # Return the size of the channel
        if self.vertical:
            self.width = current_offset.x + self.horizontal_nonpref_pitch - self.offset.x
            self.height = self.max_value + self.vertical_nonpref_pitch - self.offset.y
        else:
            self.width = self.max_value + self.horizontal_nonpref_pitch - self.offset.x
            self.height = current_offset.y + self.vertical_nonpref_pitch - self.offset.y

    def get_layer_pitch(self, layer):
        """ Return the track pitch on a given layer """
        try:
            # FIXME: Using non-pref pitch here due to overlap bug in VCG constraints.
            # It should just result in inefficient channel width but will work.
            pitch = getattr(self, "{}_pitch".format(layer))
            nonpref_pitch = getattr(self, "{}_nonpref_pitch".format(layer))
            space = getattr(self, "{}_space".format(layer))
        except AttributeError:
            debug.error("Cannot find layer pitch.", -1)
        return (nonpref_pitch, pitch, pitch - space, space)

    def add_horizontal_trunk_route(self,
                                   pins,
                                   trunk_offset,
                                   pitch):
        """
        Create a trunk route for all pins with
        the trunk located at the given y offset.
        """
        max_x = max([pin.center().x for pin in pins])
        min_x = min([pin.center().x for pin in pins])

        # if we are less than a pitch, just create a non-preferred layer jog
        non_preferred_route = max_x - min_x <= pitch

        if non_preferred_route:
            half_layer_width = 0.5 * drc["minwidth_{0}".format(self.vertical_layer)]
            # Add the horizontal trunk on the vertical layer!
            self.add_path(self.vertical_layer,
                          [vector(min_x - half_layer_width, trunk_offset.y),
                           vector(max_x + half_layer_width, trunk_offset.y)])

            # Route each pin to the trunk
            for pin in pins:
                if pin.cy() < trunk_offset.y:
                    pin_pos = pin.uc()
                else:
                    pin_pos = pin.bc()

                # No bend needed here
                mid = vector(pin_pos.x, trunk_offset.y)
                self.add_path(self.vertical_layer, [pin_pos, mid])
        else:
            # Add the horizontal trunk
            self.add_path(self.horizontal_layer,
                          [vector(min_x, trunk_offset.y),
                           vector(max_x, trunk_offset.y)])

        # Route each pin to the trunk
        for pin in pins:
            # Find the correct side of the pin
            if pin.cy() < trunk_offset.y:
                pin_pos = pin.uc()
            else:
                pin_pos = pin.bc()
            mid = vector(pin_pos.x, trunk_offset.y)
            self.add_path(self.vertical_layer, [pin_pos, mid])
            if not non_preferred_route:
                self.add_via_center(layers=self.layer_stack,
                                    offset=mid,
                                    directions=self.directions)
            self.add_via_stack_center(from_layer=pin.layer,
                                      to_layer=self.vertical_layer,
                                      offset=pin_pos)

    def add_vertical_trunk_route(self,
                                 pins,
                                 trunk_offset,
                                 pitch):
        """
        Create a trunk route for all pins with the
        trunk located at the given x offset.
        """
        max_y = max([pin.center().y for pin in pins])
        min_y = min([pin.center().y for pin in pins])

        # if we are less than a pitch, just create a non-preferred layer jog
        non_preferred_route = max_y - min_y <= pitch

        if non_preferred_route:
            half_layer_width = 0.5 * drc["minwidth_{0}".format(self.horizontal_layer)]
            # Add the vertical trunk on the horizontal layer!
            self.add_path(self.horizontal_layer,
                          [vector(trunk_offset.x, min_y - half_layer_width),
                           vector(trunk_offset.x, max_y + half_layer_width)])

            # Route each pin to the trunk
            for pin in pins:
                # Find the correct side of the pin
                if pin.cx() < trunk_offset.x:
                    pin_pos = pin.rc()
                else:
                    pin_pos = pin.lc()
                # No bend needed here
                mid = vector(trunk_offset.x, pin_pos.y)
                self.add_path(self.horizontal_layer, [pin_pos, mid])
        else:
            # Add the vertical trunk
            self.add_path(self.vertical_layer,
                          [vector(trunk_offset.x, min_y),
                           vector(trunk_offset.x, max_y)])

        # Route each pin to the trunk
        for pin in pins:
            # Find the correct side of the pin
            if pin.cx() < trunk_offset.x:
                pin_pos = pin.rc()
            else:
                pin_pos = pin.lc()
            mid = vector(trunk_offset.x, pin_pos.y)
            self.add_path(self.horizontal_layer, [pin_pos, mid])
            if not non_preferred_route:
                self.add_via_center(layers=self.layer_stack,
                                    offset=mid,
                                    directions=self.directions)
            self.add_via_stack_center(from_layer=pin.layer,
                                      to_layer=self.horizontal_layer,
                                      offset=pin_pos)

