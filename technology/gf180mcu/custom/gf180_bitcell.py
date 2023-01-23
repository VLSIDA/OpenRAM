#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2022 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.modules import bitcell_base
from openram.tech import cell_properties as props


class gf180_bitcell(bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    def __init__(self, version="opt1", name=""):
        cell_name = "cell1rw"
        super().__init__(name, cell_name=cell_name, prop=props.bitcell_1port)
        debug.info(2, "Create bitcell")

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)
