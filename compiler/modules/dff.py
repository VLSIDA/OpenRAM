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

    pin_names = ["D", "Q", "clk", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("dff", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dff", GDS["unit"])
    
    def __init__(self, name="dff"):
        design.design.__init__(self, name)

        self.width = dff.width
        self.height = dff.height
        self.pin_map = dff.pin_map
    
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
        transition_prob = spice["flop_transition_prob"]
        return transition_prob*(c_load + c_para) 

    def analytical_delay(self, slew, load = 0.0):
        # dont know how to calculate this now, use constant in tech file
        from tech import spice
        result = self.return_delay(spice["dff_delay"], spice["dff_slew"])
        return result

