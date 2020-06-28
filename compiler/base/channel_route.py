# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import collections
import debug
from tech import drc
from vector import vector
import design


class channel_route(design.design):

    unique_id = 0

    def __init__(self,
                 netlist,
                 offset,
                 layer_stack,
                 directions=None,
                 vertical=False):
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
        design.design.__init__(self, name)
        
        self.netlist = netlist
        self.offset = offset
        self.layer_stack = layer_stack
        self.directions = directions
        self.vertical = vertical
        
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
                conflicts.remove(pin)
                g[other_pin]=conflicts
        return g

    def vcg_nets_overlap(self, net1, net2):
        """
        Check all the pin pairs on two nets and return a pin
        overlap if any pin overlaps.
        """

        if self.vertical:
            pitch = self.horizontal_nonpref_pitch
        else:
            pitch = self.vertical_nonpref_pitch

        for pin1 in net1:
            for pin2 in net2:
                if self.vcg_pin_overlap(pin1, pin2, pitch):
                    return True

        return False
            
    def route(self):
        # FIXME: Must extend this to a horizontal conflict graph
        # too if we want to minimize the
        # number of tracks!
        # hcg = {}

        # Initialize the vertical conflict graph (vcg)
        # and make a list of all pins
        vcg = collections.OrderedDict()

        # Create names for the nets for the graphs
        nets = collections.OrderedDict()
        index = 0
        # print(netlist)
        for pin_list in self.netlist:
            net_name = "n{}".format(index)
            index += 1
            nets[net_name] = pin_list

        # print("Nets:")
        # for net_name in nets:
         #    print(net_name, [x.name for x in nets[net_name]])

        # Find the vertical pin conflicts
        # FIXME: O(n^2) but who cares for now
        for net_name1 in nets:
            if net_name1 not in vcg.keys():
                vcg[net_name1] = []
            for net_name2 in nets:
                if net_name2 not in vcg.keys():
                    vcg[net_name2] = []
                # Skip yourself
                if net_name1 == net_name2:
                    continue
                if self.vcg_nets_overlap(nets[net_name1],
                                         nets[net_name2]):
                    vcg[net_name2].append(net_name1)

        current_offset = self.offset
        
        # list of routes to do
        while vcg:
            # from pprint import pformat
            # print("VCG:\n", pformat(vcg))
            # get a route from conflict graph with empty fanout set
            net_name = None
            for net_name, conflicts in vcg.items():
                if len(conflicts) == 0:
                    vcg = self.remove_net_from_graph(net_name, vcg)
                    break
            else:
                # FIXME: We don't support cyclic VCGs right now.
                debug.error("Cyclic VCG in channel router.", -1)

            # These are the pins we'll have to connect
            pin_list = nets[net_name]
            # print("Routing:", net_name, [x.name for x in pin_list])

            # Remove the net from other constriants in the VCG
            vcg = self.remove_net_from_graph(net_name, vcg)

            # Add the trunk routes from the bottom up for
            # horizontal or the left to right for vertical
            if self.vertical:
                self.add_vertical_trunk_route(pin_list,
                                              current_offset,
                                              self.vertical_nonpref_pitch)
                # This accounts for the via-to-via spacings
                current_offset += vector(self.horizontal_nonpref_pitch, 0)
            else:
                self.add_horizontal_trunk_route(pin_list,
                                                current_offset,
                                                self.horizontal_nonpref_pitch)
                # This accounts for the via-to-via spacings
                current_offset += vector(0, self.vertical_nonpref_pitch)

        # Return the size of the channel
        if self.vertical:
            self.width = 0
            self.height = current_offset.y
            return current_offset.y + self.vertical_nonpref_pitch - self.offset.y
        else:
            self.width = current_offset.x
            self.height = 0
            return current_offset.x + self.horizontal_nonpref_pitch - self.offset.x

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

    def vcg_pin_overlap(self, pin1, pin2, pitch):
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

