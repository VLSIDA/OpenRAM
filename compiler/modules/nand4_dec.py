# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.base import design
from openram.base import logical_effort
from openram.tech import spice, parameter, drc
from openram.tech import cell_properties as props


class nand4_dec(design):
    """
    4-input NAND decoder for address decoders.
    """

    def __init__(self, name="nand4_dec", height=None):
        super().__init__(name, prop=props.nand4_dec)

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
        power_leak = spice["nand4_leakage"]

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
        return logical_effort(self.name,
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

    def is_non_inverting(self):
        """Return input to output polarity for module"""

        return False

    def get_on_resistance(self):
        """On resistance of pnand, defined by stacked NMOS"""
        is_nchannel = True
        stack = 4
        is_cell = False
        return self.tr_r_on(self.nmos_width, is_nchannel, stack, is_cell)

    def get_input_capacitance(self):
        """Input cap of input, passes width of gates to gate cap function"""
        return self.gate_c(self.nmos_width+self.pmos_width)

    def get_intrinsic_capacitance(self):
        """Get the drain capacitances of the TXs in the gate."""
        nmos_stack = 4
        mult = 1
        nmos_drain_c =  self.drain_c_(self.nmos_width*mult,
                                      nmos_stack,
                                      mult)
        pmos_drain_c =  self.drain_c_(self.pmos_width*mult,
                                      1,
                                      mult)
        return nmos_drain_c + pmos_drain_c
