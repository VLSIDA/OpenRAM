#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# All rights reserved.
#
import unittest
from testutils import *
import sys, os

import globals
from globals import OPTS
from sram_factory import factory
import debug


class capped_bitcell_array_1rw_1r_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        globals.setup_bitcell()

        debug.info(2, "Testing 4x4 left replica array for dp cell")
        a = factory.create(module_type="capped_bitcell_array",
                           cols=4,
                           rows=4,
                           rbl=[1, 1],
                           left_rbl=[0])
        self.local_check(a)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
