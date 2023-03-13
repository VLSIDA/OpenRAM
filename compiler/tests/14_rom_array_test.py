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
from openram.sram_factory import factory
from openram import OPTS


class rom_array_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        debug.info(2, "Testing 4x4 array for rom cell")


        data = [[1, 0, 0, 1, 0, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 0, 1, 0]]

        a = factory.create(module_type="rom_base_array", cols=9, rows=8, bitmap=data, strap_spacing=4, pitch_match=True)
        self.local_check(a)
        a.sp_write(OPTS.openram_temp + 'simulation_file.sp')

        openram.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
