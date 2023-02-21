#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram import OPTS


class path_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram.base import wire_path
        from openram import tech
        from openram.base import design

        min_space = 2 * tech.drc["minwidth_m1"]
        layer_stack = ("m1")
        # checks if we can retrace a path
        position_list = [[0,0],
                         [0, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [0, 3 * min_space ],
                         [0, 6 * min_space ]]
        w = design("path_test0")
        wire_path(w,layer_stack, position_list)
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
        w = design("path_test1")
        wire_path(w,layer_stack, position_list)
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
        w = design("path_test2")
        wire_path(w, layer_stack, position_list)
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
        w = design("path_test3")
        wire_path(w, layer_stack, position_list)
        self.local_drc_check(w)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
