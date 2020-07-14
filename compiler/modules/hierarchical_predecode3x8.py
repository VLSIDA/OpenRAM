# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from hierarchical_predecode import hierarchical_predecode
from globals import OPTS


class hierarchical_predecode3x8(hierarchical_predecode):
    """
    Pre 3x8 decoder used in hierarchical_decoder.
    """
    def __init__(self, name, height=None):
        hierarchical_predecode.__init__(self, name, 3, height)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_input_inverters()
        connections=[["inbar_0", "inbar_1", "inbar_2", "out_0", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "inbar_2", "out_1", "vdd", "gnd"],            
                     ["inbar_0", "in_1",    "inbar_2", "out_2", "vdd", "gnd"],
                     ["in_0",    "in_1",    "inbar_2", "out_3", "vdd", "gnd"],            
                     ["inbar_0", "inbar_1", "in_2",    "out_4", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "in_2",    "out_5", "vdd", "gnd"],
                     ["inbar_0", "in_1",    "in_2",    "out_6", "vdd", "gnd"],
                     ["in_0",    "in_1",    "in_2",    "out_7", "vdd", "gnd"]]
        self.create_and_array(connections)

    def get_and_input_line_combination(self):
        """ These are the decoder connections of the NAND gates to the A,B,C pins """
        combination = [["Abar_0", "Abar_1", "Abar_2"],
                       ["A_0",    "Abar_1", "Abar_2"],
                       ["Abar_0", "A_1",    "Abar_2"],
                       ["A_0",    "A_1",    "Abar_2"],
                       ["Abar_0", "Abar_1", "A_2"],
                       ["A_0",    "Abar_1", "A_2"], 
                       ["Abar_0", "A_1",    "A_2"], 
                       ["A_0",    "A_1",    "A_2"]]
        return combination
