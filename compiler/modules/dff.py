import globals
import design
from math import log
import design
from tech import GDS,layer
import utils

class dff(design.design):
    """
    Memory address flip-flop
    """

    pin_names = ["d", "q", "clk", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("dff", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dff", GDS["unit"], layer["boundary"])
    
    def __init__(self, name="dff"):
        design.design.__init__(self, name)

        self.width = dff.width
        self.height = dff.height
        self.pin_map = dff.pin_map
    
    def analytical_delay(self, slew, load = 0.0):
        # dont know how to calculate this now, use constant in tech file
        from tech import spice
        result = self.return_delay(spice["dff_delay"], spice["dff_slew"])
        return result

