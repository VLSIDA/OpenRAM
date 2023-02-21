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


class wire_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram.base import wire
        from openram import tech
        from openram.base import design

        layer_stacks = [tech.poly_stack] + tech.beol_stacks

        for reverse in [False, True]:
            for stack in layer_stacks:
                if reverse:
                    layer_stack = stack[::-1]
                else:
                    layer_stack = stack

                # Just make a conservative spacing. Make it wire pitch instead?
                min_space = 2 * (tech.drc["minwidth_{}".format(layer_stack[0])] +
                                 tech.drc["minwidth_{}".format(layer_stack[2])])

                position_list = [[0, 0],
                                 [0, 3 * min_space],
                                 [1 * min_space, 3 * min_space],
                                 [4 * min_space, 3 * min_space],
                                 [4 * min_space, 0],
                                 [7 * min_space, 0],
                                 [7 * min_space, 4 * min_space],
                                 [-1 * min_space, 4 * min_space],
                                 [-1 * min_space, 0]]
                position_list  = [[x - min_space, y - min_space] for x, y in position_list]
                w = design("wire_test_{}".format("_".join(layer_stack)))
                wire(w, layer_stack, position_list)
                self.local_drc_check(w)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
