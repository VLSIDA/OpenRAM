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


class precharge_1rw_1r_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        # check precharge array in multi-port
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        debug.info(2, "Checking 3 column precharge array for 1RW/1R bitcell (port 0)")
        pc = factory.create(module_type="precharge_array", columns=3, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(pc)

        debug.info(2, "Checking 3 column precharge array for 1RW/1R bitcell (port 1)")
        pc = factory.create(module_type="precharge_array", columns=3, bitcell_bl="bl0", bitcell_br="br0", column_offset=1)
        self.local_check(pc)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
