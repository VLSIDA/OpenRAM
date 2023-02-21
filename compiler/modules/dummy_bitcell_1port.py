# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import cell_properties as props
from .bitcell_base import bitcell_base


class dummy_bitcell_1port(bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """
    def __init__(self, name):
        super().__init__(name, prop=props.bitcell_1port)
        debug.info(2, "Create dummy bitcell")

    def build_graph(self, graph, inst_name, port_nets):
        """ Adds edges based on inputs/outputs. Overrides base class function. """
        pass
