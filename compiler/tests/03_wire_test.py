#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys,os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug

class wire_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        import wire
        import tech
        import design
        
        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("poly", "contact", "metal1")
        old_position_list = [[0, 0],
                             [0, 3 * min_space],
                             [1 * min_space, 3 * min_space],
                             [4 * min_space, 3 * min_space],
                             [4 * min_space, 0],
                             [7 * min_space, 0],
                             [7 * min_space, 4 * min_space],
                             [-1 * min_space, 4 * min_space],
                             [-1 * min_space, 0]]
        position_list  = [[x-min_space, y-min_space] for x,y in old_position_list]        
        w = design.design("wire_test1")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal1", "contact", "poly")
        old_position_list = [[0, 0],
                             [0, 3 * min_space],
                             [1 * min_space, 3 * min_space],
                             [4 * min_space, 3 * min_space],
                             [4 * min_space, 0],
                             [7 * min_space, 0],
                             [7 * min_space, 4 * min_space],
                             [-1 * min_space, 4 * min_space],
                             [-1 * min_space, 0]]
        position_list  = [[x+min_space, y+min_space] for x,y in old_position_list]
        w = design.design("wire_test2")        
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal1", "via1", "metal2")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        w = design.design("wire_test3")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)


        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal2", "via1", "metal1")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        w = design.design("wire_test4")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal3"])
        layer_stack = ("metal2", "via2", "metal3")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        position_list.reverse()
        w = design.design("wire_test5")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal3"])
        layer_stack = ("metal3", "via2", "metal2")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        position_list.reverse()
        w = design.design("wire_test6")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        globals.end_openram()
        

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
