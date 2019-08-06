# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
import debug
import utils
from tech import GDS,layer,drc,parameter

class dummy_bitcell_1rw_1r(design.design):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = ["bl0", "br0", "bl1", "br1", "wl0", "wl1", "vdd", "gnd"]
    type_list = ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT", "INPUT", "INPUT", "POWER", "GROUND"]  
    (width,height) = utils.get_libcell_size("dummy_cell_1rw_1r", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dummy_cell_1rw_1r", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument        
        design.design.__init__(self, "dummy_cell_1rw_1r")
        debug.info(2, "Create dummy bitcell 1rw+1r object")

        self.width = dummy_bitcell_1rw_1r.width
        self.height = dummy_bitcell_1rw_1r.height
        self.pin_map = dummy_bitcell_1rw_1r.pin_map
        self.add_pin_types(self.type_list)

    def get_wl_cin(self):
        """Return the relative capacitance of the access transistor gates"""
        #This is a handmade cell so the value must be entered in the tech.py file or estimated.
        #Calculated in the tech file by summing the widths of all the related gates and dividing by the minimum width.
        #FIXME: sizing is not accurate with the handmade cell. Change once cell widths are fixed.
        access_tx_cin = parameter["6T_access_size"]/drc["minwidth_tx"]
        return 2*access_tx_cin

    def build_graph(self, graph, inst_name, port_nets):        
        """Dummy bitcells are cannot form a path and be part of the timing graph"""
        return 
