# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
import utils
from tech import GDS, layer


class tri_gate(design.design):
    """
    This module implements the tri gate cell used in the design forS
    bit-line isolation. It is a hand-made cell, so the layout and
    netlist should be available in the technology library.
    """

    pin_names = ["in", "out", "en", "en_bar", "vdd", "gnd"]
    type_list = ["INPUT", "OUTPUT", "INPUT", "INPUT", "POWER", "GROUND"]
    cell_size_layer = "boundary"

    unique_id = 1

    def __init__(self, name=""):
        if name=="":
            name = "tri{0}".format(tri_gate.unique_id)
            tri_gate.unique_id += 1
        super().__init__(self, name)
        debug.info(2, "Create tri_gate")

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
        #Power in this module currently not defined. Returns 0 nW (leakage and dynamic).
        total_power = self.return_power()
        return total_power

    def get_cin(self):
        return 9*spice["min_tx_gate_c"]

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)
