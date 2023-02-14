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


class hierarchical_decoder_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        # Checks 2x4 and 2 x 3x8 and 3-input NAND with non-power-of-two
        debug.info(1, "Testing 132 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=132)
        self.local_check(a)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
