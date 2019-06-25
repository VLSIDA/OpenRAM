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
from tech import GDS,layer

class write_driver(design.design):
    """
    Tristate write driver to be active during write operations only.       
    This module implements the write driver cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    """

    pin_names = ["din", "bl", "br", "en", "vdd", "gnd"]
    type_list = ["INPUT", "OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
    (width,height) = utils.get_libcell_size("write_driver", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "write_driver", GDS["unit"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create write_driver")

        self.width = write_driver.width
        self.height = write_driver.height
        self.pin_map = write_driver.pin_map
        self.add_pin_types(self.type_list)

    def get_w_en_cin(self):
        """Get the relative capacitance of a single input"""
        # This is approximated from SCMOS. It has roughly 5 3x transistor gates.
        return 5*3

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets) 