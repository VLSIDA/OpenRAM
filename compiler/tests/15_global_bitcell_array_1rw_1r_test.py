#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os

import globals
from sram_factory import factory
import debug


# @unittest.skip("SKIPPING 05_global_bitcell_array_test")
class global_bitcell_array_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        globals.setup_bitcell()

        debug.info(2, "Testing 2 x 4x4 global bitcell array for cell_1rw_1r")
        a = factory.create(module_type="global_bitcell_array", cols=[4, 4], rows=4)
        self.local_check(a)

        # debug.info(2, "Testing 4x4 local bitcell array for 6t_cell with replica column")
        # a = factory.create(module_type="local_bitcell_array", cols=4, left_rbl=1, rows=4, ports=[0])
        # self.local_check(a)

        globals.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
