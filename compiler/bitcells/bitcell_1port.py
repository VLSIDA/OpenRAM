# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import cell_properties as props
import bitcell_base


class bitcell_1port(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    def __init__(self, name):
        super().__init__(name, prop=props.bitcell_1port)
        debug.info(2, "Create bitcell")

    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = ["wl"]
        return row_pins

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        return ["bl", "br"]

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return ["bl"]

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return ["br"]

    def get_bl_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return "bl"

    def get_br_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return "br"

    def get_wl_name(self, port=0):
        """Get wl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return "wl"

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)

    def is_non_inverting(self):
        """Return input to output polarity for module"""
        
        return False