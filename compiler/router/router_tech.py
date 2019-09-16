# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from tech import drc,layer
from contact import contact
from pin_group import pin_group
from vector import vector
import debug
import math

class router_tech:
    """
    This is a class to hold the router tech constants.
    """
    def __init__(self, layers, rail_track_width):
        """
        Allows us to change the layers that we are routing on. First layer
        is always horizontal, middle is via, and last is always
        vertical.
        """
        self.layers = layers
        self.rail_track_width = rail_track_width

        if len(self.layers)==1:
            self.horiz_layer_name = self.vert_layer_name = self.layers[0]
            self.horiz_layer_number = self.vert_layer_number = layer[self.layers[0]]
            
            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_supply_layer_width_space(1)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_supply_layer_width_space(0)
            
            self.horiz_track_width = self.horiz_layer_minwidth + self.horiz_layer_spacing
            self.vert_track_width = self.vert_layer_minwidth + self.vert_layer_spacing
        else:
            (self.horiz_layer_name, self.via_layer_name, self.vert_layer_name) = self.layers

            via_connect = contact(self.layers, (1, 1))
            max_via_size = max(via_connect.width,via_connect.height)

            self.horiz_layer_number = layer[self.horiz_layer_name]
            self.vert_layer_number = layer[self.vert_layer_name]
        
            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_supply_layer_width_space(1)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_supply_layer_width_space(0)
            
            # For supplies, we will make the wire wider than the vias
            self.vert_layer_minwidth = max(self.vert_layer_minwidth, max_via_size)
            self.horiz_layer_minwidth = max(self.horiz_layer_minwidth, max_via_size)
            
            self.horiz_track_width = self.horiz_layer_minwidth + self.horiz_layer_spacing
            self.vert_track_width = self.vert_layer_minwidth + self.vert_layer_spacing
            
        # We'll keep horizontal and vertical tracks the same for simplicity.
        self.track_width = max(self.horiz_track_width,self.vert_track_width)
        debug.info(1,"Track width: {:.3f}".format(self.track_width))
        self.track_space = max(self.horiz_layer_spacing,self.vert_layer_spacing)
        debug.info(1,"Track space: {:.3f}".format(self.track_space))
        self.track_wire = self.track_width - self.track_space
        debug.info(1,"Track wire width: {:.3f}".format(self.track_wire))
        
        self.track_widths = vector([self.track_width] * 2)
        self.track_factor = vector([1/self.track_width] * 2)
        debug.info(2,"Track factor: {}".format(self.track_factor))
    
        # When we actually create the routes, make them the width of the track (minus 1/2 spacing on each side)
        self.layer_widths = [self.track_wire, 1, self.track_wire]
        
    def get_zindex(self,layer_num):
        if layer_num==self.horiz_layer_number:
            return 0
        else:
            return 1

    def get_layer(self, zindex):
        if zindex==1:
            return self.vert_layer_name
        elif zindex==0:
            return self.horiz_layer_name
        else:
            debug.error("Invalid zindex {}".format(zindex),-1)

    def get_supply_layer_width_space(self, zindex):
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
        
        min_width = drc("minwidth_{0}".format(layer_name), self.rail_track_width*min_wire_width, math.inf)
        min_spacing = drc(str(layer_name)+"_to_"+str(layer_name), self.rail_track_width*min_wire_width, math.inf)

        return (min_width,min_spacing)

    
