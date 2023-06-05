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


class dummy_bitcell_2port(bitcell_base):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    def __init__(self, name):
        super().__init__(name, prop=props.bitcell_2port)
        debug.info(2, "Create dummy bitcell 2 port object")

    def build_graph(self, graph, inst_name, port_nets):
        """ Adds edges based on inputs/outputs. Overrides base class function. """
        pass
