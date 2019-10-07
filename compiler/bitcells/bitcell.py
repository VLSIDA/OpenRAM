# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import utils
from tech import GDS, layer
import bitcell_base


class bitcell(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    pin_names = ["bl", "br", "wl", "vdd", "gnd"]
    storage_nets = ['Q', 'Qbar']
    type_list = ["OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
    (width, height) = utils.get_libcell_size("cell_6t",
                                             GDS["unit"],
                                             layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "cell_6t", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        bitcell_base.bitcell_base.__init__(self, "cell_6t")
        debug.info(2, "Create bitcell")

        self.width = bitcell.width
        self.height = bitcell.height
        self.pin_map = bitcell.pin_map
        self.add_pin_types(self.type_list)
        self.nets_match = self.do_nets_exist(self.storage_nets)
        
    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = ["wl"]
        return row_pins
    
    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        column_pins = ["bl", "br"]
        return column_pins
    
    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        column_pins = ["bl"]
        return column_pins
        
    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        column_pins = ["br"]
        return column_pins
        
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
