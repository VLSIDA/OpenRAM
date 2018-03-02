import globals
import design
from math import log
import design
from tech import GDS,layer
import utils

class ms_flop(design.design):
    """
    Memory address flip-flop
    """

    pin_names = ["din", "dout", "dout_bar", "clk", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("ms_flop", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "ms_flop", GDS["unit"], layer["boundary"])
    
    def __init__(self, name="ms_flop"):
        design.design.__init__(self, name)

        self.width = ms_flop.width
        self.height = ms_flop.height
        self.pin_map = ms_flop.pin_map
    
    def analytical_delay(self, slew, load = 0.0):
        # dont know how to calculate this now, use constant in tech file
        from tech import spice
        result = self.return_delay(spice["msflop_delay"], spice["msflop_slew"])
        return result
        
    def analytical_power(self, proc, vdd, temp, load):
        """Returns dynamic and leakage power. Results in nW"""
        from tech import spice
        c_eff = self.calculate_effective_capacitance(load)
        f = spice["default_event_rate"]
        power_dyn = c_eff*vdd*vdd*f
        power_leak = spice["msflop_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        from tech import spice, parameter
        c_load = load
        c_para = spice["flop_para_cap"]#ff
        transistion_prob = spice["flop_transisition_prob"]
        return transistion_prob*(c_load + c_para) 

        
        