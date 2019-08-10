# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import globals
import design
from math import log
import design
from tech import GDS,layer,spice,parameter
import utils

class dff(design.design):
    """
    Memory address flip-flop
    """

    pin_names = ["D", "Q", "clk", "vdd", "gnd"]
    type_list = ["INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
    (width,height) = utils.get_libcell_size("dff", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dff", GDS["unit"])
    
    def __init__(self, name="dff"):
        design.design.__init__(self, name)

        self.width = dff.width
        self.height = dff.height
        self.pin_map = dff.pin_map
        self.add_pin_types(self.type_list)
    
    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_rate"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["msflop_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        from tech import parameter
        c_load = load
        c_para = spice["flop_para_cap"]#ff
        transition_prob = spice["flop_transition_prob"]
        return transition_prob*(c_load + c_para) 

    def get_clk_cin(self):
        """Return the total capacitance (in relative units) that the clock is loaded by in the dff"""
        #This is a handmade cell so the value must be entered in the tech.py file or estimated.
        #Calculated in the tech file by summing the widths of all the gates and dividing by the minimum width.
        return parameter["dff_clk_cin"]

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets) 
        