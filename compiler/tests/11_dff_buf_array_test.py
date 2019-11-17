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
from sram_factory import factory
import debug

class dff_buf_array_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        debug.info(2, "Testing dff_buf_array for 3x3")
        a = factory.create(module_type="dff_buf_array", rows=3, columns=3)
        self.local_check(a)

        debug.info(2, "Testing dff_buf_array for 1x3")
        a = factory.create(module_type="dff_buf_array", rows=1, columns=3)
        self.local_check(a)

        debug.info(2, "Testing dff_buf_array for 3x1")
        a = factory.create(module_type="dff_buf_array", rows=3, columns=1)
        self.local_check(a)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
