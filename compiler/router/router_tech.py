# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram.base.contact import contact
from openram.base.vector import vector
from openram.tech import drc, layer, preferred_directions


class router_tech:
    """
    This is a class to hold the router tech constants.
    """
    def __init__(self, layers, route_track_width):
        """
        Allows us to change the layers that we are routing on.
        This uses the preferreed directions.
        """
        self.layers = layers
        self.route_track_width = route_track_width

        if len(self.layers) == 1:
            self.horiz_layer_name = self.vert_layer_name = self.layers[0]
            self.horiz_lpp = self.vert_lpp = layer[self.layers[0]]

            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_layer_width_space(1)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_layer_width_space(0)

            self.horiz_track_width = self.horiz_layer_minwidth + self.horiz_layer_spacing
            self.vert_track_width = self.vert_layer_minwidth + self.vert_layer_spacing
        else:
            (try_horiz_layer, self.via_layer_name, try_vert_layer) = self.layers

            # figure out wich of the two layers prefers horizontal/vertical
            # routing
            self.horiz_layer_name = None
            self.vert_layer_name = None

            if preferred_directions[try_horiz_layer] == "H":
                self.horiz_layer_name = try_horiz_layer
            else:
                self.horiz_layer_name = try_vert_layer
            if preferred_directions[try_vert_layer] == "V":
                self.vert_layer_name = try_vert_layer
            else:
                self.vert_layer_name = try_horiz_layer

            if not self.horiz_layer_name or not self.vert_layer_name:
                raise ValueError("Layer '{}' and '{}' are using the wrong "
                                 "preferred_directions '{}' and '{}'.")

            via_connect = contact(self.layers, (1, 1))
            max_via_size = max(via_connect.width, via_connect.height)

            self.horiz_lpp = layer[self.horiz_layer_name]
            self.vert_lpp = layer[self.vert_layer_name]

            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_layer_width_space(1)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_layer_width_space(0)

            # For supplies, we will make the wire wider than the vias
            self.vert_layer_minwidth = max(self.vert_layer_minwidth, max_via_size)
            self.horiz_layer_minwidth = max(self.horiz_layer_minwidth, max_via_size)

            self.horiz_track_width = self.horiz_layer_minwidth + self.horiz_layer_spacing
            self.vert_track_width = self.vert_layer_minwidth + self.vert_layer_spacing

        # We'll keep horizontal and vertical tracks the same for simplicity.
        self.track_width = max(self.horiz_track_width, self.vert_track_width)
        debug.info(1, "Minimum track width: {:.3f}".format(self.track_width))
        self.track_space = max(self.horiz_layer_spacing, self.vert_layer_spacing)
        debug.info(1, "Minimum track space: {:.3f}".format(self.track_space))
        self.track_wire = self.track_width - self.track_space
        debug.info(1, "Minimum track wire width: {:.3f}".format(self.track_wire))

        self.track_widths = vector([self.track_width] * 2)
        self.track_factor = vector([1/self.track_width] * 2)
        debug.info(2, "Track factor: {}".format(self.track_factor))

        # When we actually create the routes, make them the width of the track (minus 1/2 spacing on each side)
        self.layer_widths = [self.track_wire, 1, self.track_wire]

    def same_lpp(self, lpp1, lpp2):
        """
        Check if the layers and purposes are the same.
        Ignore if purpose is a None.
        """
        if lpp1[1] == None or lpp2[1] == None:
            return lpp1[0] == lpp2[0]

        return lpp1[0] == lpp2[0] and lpp1[1] == lpp2[1]

    def get_zindex(self, lpp):
        if self.same_lpp(lpp, self.horiz_lpp):
            return 0
        else:
            return 1

    def get_layer(self, zindex):
        if zindex==1:
            return self.vert_layer_name
        elif zindex==0:
            return self.horiz_layer_name
        else:
            debug.error("Invalid zindex {}".format(zindex), -1)

    def get_layer_width_space(self, zindex):
        """
        These are the width and spacing of a supply layer given a supply rail
        of the given number of min wire widths.
        """
        if zindex==1:
            layer_name = self.vert_layer_name
        elif zindex==0:
            layer_name = self.horiz_layer_name
        else:
            debug.error("Invalid zindex for track", -1)

        min_wire_width = drc("minwidth_{0}".format(layer_name), 0, math.inf)

        min_width = self.route_track_width * drc("minwidth_{0}".format(layer_name), self.route_track_width * min_wire_width, math.inf)
        min_spacing = drc(str(layer_name)+"_to_"+str(layer_name), self.route_track_width * min_wire_width, math.inf)

        return (min_width, min_spacing)


