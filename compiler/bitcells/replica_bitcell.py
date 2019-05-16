# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import design
import debug
import utils
from tech import GDS,layer,drc,parameter

class replica_bitcell(design.design):
    """
    A single bit cell (6T, 8T, etc.)
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = ["bl", "br", "wl", "vdd", "gnd"]
    type_list = ["OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"] 
    (width,height) = utils.get_libcell_size("replica_cell_6t", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "replica_cell_6t", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        design.design.__init__(self, "replica_cell_6t")
        debug.info(2, "Create replica bitcell object")

        self.width = replica_bitcell.width
        self.height = replica_bitcell.height
        self.pin_map = replica_bitcell.pin_map
        self.add_pin_types(self.type_list)
    
    def get_wl_cin(self):
        """Return the relative capacitance of the access transistor gates"""
        #This is a handmade cell so the value must be entered in the tech.py file or estimated.
        #Calculated in the tech file by summing the widths of all the related gates and dividing by the minimum width.
        access_tx_cin = parameter["6T_access_size"]/drc["minwidth_tx"]
        return 2*access_tx_cin

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets) 