# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import OPTS
from .hierarchical_predecode import hierarchical_predecode


class hierarchical_predecode4x16(hierarchical_predecode):
    """
    Pre 4x16 decoder used in hierarchical_decoder.
    """
    def __init__(self, name, column_decoder=False, height=None):
        super().__init__(name, 4, column_decoder, height)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_input_inverters()
        connections=[["inbar_0", "inbar_1", "inbar_2", "inbar_3", "out_0", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "inbar_2", "inbar_3", "out_1", "vdd", "gnd"],
                     ["inbar_0", "in_1",    "inbar_2", "inbar_3", "out_2", "vdd", "gnd"],
                     ["in_0",    "in_1",    "inbar_2", "inbar_3", "out_3", "vdd", "gnd"],
                     ["inbar_0", "inbar_1", "in_2",    "inbar_3", "out_4", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "in_2",    "inbar_3", "out_5", "vdd", "gnd"],
                     ["inbar_0", "in_1",    "in_2",    "inbar_3", "out_6", "vdd", "gnd"],
                     ["in_0",    "in_1",    "in_2",    "inbar_3", "out_7", "vdd", "gnd"],
                     ["inbar_0", "inbar_1", "inbar_2", "in_3", "out_8", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "inbar_2", "in_3", "out_9", "vdd", "gnd"],
                     ["inbar_0", "in_1",    "inbar_2", "in_3", "out_10", "vdd", "gnd"],
                     ["in_0",    "in_1",    "inbar_2", "in_3", "out_11", "vdd", "gnd"],
                     ["inbar_0", "inbar_1", "in_2",    "in_3", "out_12", "vdd", "gnd"],
                     ["in_0",    "inbar_1", "in_2",    "in_3", "out_13", "vdd", "gnd"],
                     ["inbar_0", "in_1",    "in_2",    "in_3", "out_14", "vdd", "gnd"],
                     ["in_0",    "in_1",    "in_2",    "in_3", "out_15", "vdd", "gnd"]        ]

        self.create_and_array(connections)

    def get_and_input_line_combination(self):
        """ These are the decoder connections of the AND gates to the A,B pins """
        combination = [["Abar_0", "Abar_1", "Abar_2", "Abar_3"],
                       ["A_0",    "Abar_1", "Abar_2", "Abar_3"],
                       ["Abar_0", "A_1",    "Abar_2", "Abar_3"],
                       ["A_0",    "A_1",    "Abar_2", "Abar_3"],
                       ["Abar_0", "Abar_1", "A_2"   , "Abar_3"],
                       ["A_0",    "Abar_1", "A_2"   , "Abar_3"],
                       ["Abar_0", "A_1",    "A_2"   , "Abar_3"],
                       ["A_0",    "A_1",    "A_2"   , "Abar_3"],
                       ["Abar_0", "Abar_1", "Abar_2", "A_3"],
                       ["A_0",    "Abar_1", "Abar_2", "A_3"],
                       ["Abar_0", "A_1",    "Abar_2", "A_3"],
                       ["A_0",    "A_1",    "Abar_2", "A_3"],
                       ["Abar_0", "Abar_1", "A_2",    "A_3"],
                       ["A_0",    "Abar_1", "A_2",    "A_3"],
                       ["Abar_0", "A_1",    "A_2",    "A_3"],
                       ["A_0",    "A_1",    "A_2",    "A_3"]]
        return combination
