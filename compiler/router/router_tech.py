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
    def __init__(self, layers, supply_router=False):
        """
        Allows us to change the layers that we are routing on. First layer
        is always horizontal, middle is via, and last is always
        vertical.
        """
        self.layers = layers
        (self.horiz_layer_name, self.via_layer_name, self.vert_layer_name) = self.layers
        # This is the minimum routed track spacing
        via_connect = contact(self.layers, (1, 1))
        max_via_size = max(via_connect.width,via_connect.height)

        self.horiz_layer_number = layer[self.horiz_layer_name]
        self.vert_layer_number = layer[self.vert_layer_name]
        
        if supply_router:
            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_supply_layer_width_space(1,2)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_supply_layer_width_space(0,2)

            # For supplies, we will make the wire wider than the vias
            self.vert_layer_minwidth = max(self.vert_layer_minwidth, max_via_size)
            self.horiz_layer_minwidth = max(self.horiz_layer_minwidth, max_via_size)
            
            self.horiz_track_width = self.horiz_layer_minwidth + self.horiz_layer_spacing
            self.vert_track_width = self.vert_layer_minwidth + self.vert_layer_spacing
            
        else:
            (self.vert_layer_minwidth, self.vert_layer_spacing) = self.get_layer_width_space(1)
            (self.horiz_layer_minwidth, self.horiz_layer_spacing) = self.get_layer_width_space(0)
            
            self.horiz_track_width = max_via_size + self.horiz_layer_spacing
            self.vert_track_width = max_via_size + self.vert_layer_spacing
            
        # We'll keep horizontal and vertical tracks the same for simplicity.
        self.track_width = max(self.horiz_track_width,self.vert_track_width)
        debug.info(1,"Track width: "+str(self.track_width))
        
        self.track_widths = vector([self.track_width] * 2)
        self.track_factor = vector([1/self.track_width] * 2)
        debug.info(2,"Track factor: {0}".format(self.track_factor))
    
        # When we actually create the routes, make them the width of the track (minus 1/2 spacing on each side)
        self.layer_widths = [self.track_width - self.horiz_layer_spacing, 1, self.track_width - self.vert_layer_spacing]
        
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

    def get_layer_width_space(self, zindex, width=0, length=0):
        """
        Return the width and spacing of a given layer
        and wire of a given width and length.
        """
        if zindex==1:
            layer_name = self.vert_layer_name
        elif zindex==0:
            layer_name = self.horiz_layer_name
        else:
            debug.error("Invalid zindex for track", -1)

        min_width = drc("minwidth_{0}".format(layer_name), width, length)
        min_spacing = drc(str(layer_name)+"_to_"+str(layer_name), width, length)

        return (min_width,min_spacing)


    def get_supply_layer_width_space(self, zindex, widths=2):
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
            
        wire_width = widths*drc("minwidth_{0}".format(layer_name), 0, math.inf)
        
        min_width = drc("minwidth_{0}".format(layer_name), wire_width, math.inf)
        min_spacing = drc(str(layer_name)+"_to_"+str(layer_name), wire_width, math.inf)

        return (min_width,min_spacing)

    
