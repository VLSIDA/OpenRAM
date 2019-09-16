# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from tech import drc
import debug
import design
from vector import vector
from hierarchical_predecode import hierarchical_predecode
from globals import OPTS

class hierarchical_predecode2x4(hierarchical_predecode):
    """
    Pre 2x4 decoder used in hierarchical_decoder.
    """
    def __init__(self, name, height=None):
        hierarchical_predecode.__init__(self, name, 2, height)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_input_inverters()
        self.create_output_inverters()
        connections =[["inbar_0", "inbar_1", "Z_0", "vdd", "gnd"],
                      ["in_0",    "inbar_1", "Z_1", "vdd", "gnd"],
                      ["inbar_0", "in_1",    "Z_2", "vdd", "gnd"],
                      ["in_0",    "in_1",    "Z_3", "vdd", "gnd"]]
        self.create_nand_array(connections)

    def create_layout(self):
        """ The general organization is from left to right:
        1) a set of M2 rails for input signals
        2) a set of inverters to invert input signals
        3) a set of M2 rails for the vdd, gnd, inverted inputs, inputs
        4) a set of NAND gates for inversion
        """
        self.setup_layout_constraints()
        self.route_rails()
        self.place_input_inverters()
        self.place_output_inverters()
        self.place_nand_array()
        self.route()
        self.add_boundary()
        self.DRC_LVS()        

    def get_nand_input_line_combination(self):
        """ These are the decoder connections of the NAND gates to the A,B pins """
        combination = [["Abar_0", "Abar_1"],
                       ["A_0",    "Abar_1"],
                       ["Abar_0", "A_1"],
                       ["A_0",    "A_1"]]
        return combination 