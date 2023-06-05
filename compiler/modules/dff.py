# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.base import design
from openram.tech import cell_properties as props
from openram.tech import spice


class dff(design):
    """
    Memory address flip-flop
    """

    def __init__(self, name="dff"):
        super().__init__(name, prop=props.dff)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["dff_leakage"]

        total_power = self.return_power(power_dyn, power_leak)
        return total_power

    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        c_para = spice["dff_out_cap"] # ff
        transition_prob = 0.5
        return transition_prob * (c_load + c_para)

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)

