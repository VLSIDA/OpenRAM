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

class path_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        import wire_path
        import tech
        import design

        min_space = 2 * tech.drc["minwidth_m1"]
        layer_stack = ("m1")
        # checks if we can retrace a path
        position_list = [[0,0],
                         [0, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [0, 3 * min_space ],
                         [0, 6 * min_space ]]
        w = design.design("path_test0")
        wire_path.wire_path(w,layer_stack, position_list)
        self.local_drc_check(w)


        min_space = 2 * tech.drc["minwidth_m1"]
        layer_stack = ("m1")
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
        w = design.design("path_test1")
        wire_path.wire_path(w,layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * tech.drc["minwidth_m2"]
        layer_stack = ("m2")
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
        w = design.design("path_test2")
        wire_path.wire_path(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * tech.drc["minwidth_m3"]
        layer_stack = ("m3")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        # run on the reverse list
        position_list.reverse()
        w = design.design("path_test3")
        wire_path.wire_path(w, layer_stack, position_list)
        self.local_drc_check(w)

        globals.end_openram()
        


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
