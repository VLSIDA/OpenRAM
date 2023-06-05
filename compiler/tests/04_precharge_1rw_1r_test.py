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


class precharge_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        # check precharge array in multi-port
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        debug.info(2, "Checking precharge for 1rw1r port 0")
        tx = factory.create(module_type="precharge", size=1, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(tx)

        debug.info(2, "Checking precharge for 1rw1r port 1")
        tx = factory.create(module_type="precharge", size=1, bitcell_bl="bl1", bitcell_br="br1")
        self.local_check(tx)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
