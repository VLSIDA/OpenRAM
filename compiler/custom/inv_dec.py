# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from tech import GDS, layer, spice, parameter
import logical_effort
import utils


class inv_dec(design.design):
    """
    INV for address decoders.
    """

    pin_names = ["A", "Z", "vdd", "gnd"]
    type_list = ["INPUT", "OUTPUT", "POWER", "GROUND"]
    cell_size_layer = "boundary"

    def __init__(self, name="inv_dec", height=None):
        super().__init__(name)

        (width, height) = utils.get_libcell_size(self.cell_name,
                                                 GDS["unit"],
                                                 layer[self.cell_size_layer])

        pin_map = utils.get_libcell_pins(self.pin_names,
                                         self.cell_name,
                                         GDS["unit"])

        self.width = width
        self.height = height
        self.pin_map = pin_map
        self.add_pin_types(self.type_list)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["inv_leakage"]

        total_power = self.return_power(power_dyn, power_leak)
        return total_power

    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        # In fF
        c_para = spice["min_tx_drain_c"] * (self.nmos_size / parameter["min_tx_size"])

        return transition_prob * (c_load + c_para)

    def input_load(self):
        """
        Return the capacitance of the gate connection in generic capacitive
        units relative to the minimum width of a transistor
        """
        return self.nmos_size + self.pmos_size

    def get_stage_effort(self, cout, inp_is_rise=True):
        """
        Returns an object representing the parameters for delay in tau units.
        Optional is_rise refers to the input direction rise/fall.
        Input inverted by this stage.
        """
        parasitic_delay = 1
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
