# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.tech import cell_properties as props


class write_driver(design):
    """
    Tristate write driver to be active during write operations only.
    This module implements the write driver cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    """

    def __init__(self, name):
        super().__init__(name, prop=props.write_driver)
        debug.info(2, "Create write_driver")

    def get_bl_names(self):
        return "bl"

    def get_br_names(self):
        return "br"

    @property
    def din_name(self):
        return "din"

    @property
    def en_name(self):
        return "en"

    def get_w_en_cin(self):
        """Get the relative capacitance of a single input"""
        # This is approximated from SCMOS. It has roughly 5 3x transistor gates.
        return 5 * 3

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)
