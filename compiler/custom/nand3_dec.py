# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from tech import GDS, layer, spice, parameter, drc
import logical_effort
import utils


class nand3_dec(design.design):
    """
    3-input NAND decoder for address decoders.
    """
    
    pin_names = ["A", "B", "C", "Z", "vdd", "gnd"]
    type_list = ["INPUT", "INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"]
    
    (width, height) = utils.get_libcell_size("nand3_dec",
                                             GDS["unit"],
                                             layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "nand3_dec", GDS["unit"])
        
    def __init__(self, name="nand3_dec", height=None):
        design.design.__init__(self, name)

        self.width = nand3_dec.width
        self.height = nand3_dec.height
        self.pin_map = nand3_dec.pin_map
        self.add_pin_types(self.type_list)

        # FIXME: For now...
        size = 1
        self.size = size
        self.nmos_size = 2 * size
        self.pmos_size = parameter["beta"] * size
        self.nmos_width = self.nmos_size * drc("minwidth_tx")
        self.pmos_width = self.pmos_size * drc("minwidth_tx")
        
    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nand3_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        # In fF
        c_para = spice["min_tx_drain_c"] * (self.nmos_size / parameter["min_tx_size"])
        transition_prob = 0.1875
        return transition_prob * (c_load + c_para)

    def input_load(self):
        """Return the relative input capacitance of a single input"""
        return self.nmos_size + self.pmos_size
    
    def get_stage_effort(self, cout, inp_is_rise=True):
        """
        Returns an object representing the parameters for delay in tau units.
        Optional is_rise refers to the input direction rise/fall.
        Input inverted by this stage.
        """
        parasitic_delay = 2
        return logical_effort.logical_effort(self.name,
                                             self.size,
                                             self.input_load(),
                                             cout,
                                             parasitic_delay,
                                             not inp_is_rise)

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)
        
