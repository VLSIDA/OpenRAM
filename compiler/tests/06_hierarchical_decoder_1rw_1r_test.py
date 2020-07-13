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


class hierarchical_decoder_1rw_1r_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        # Use the 2 port cell since it is usually bigger/easier
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        globals.setup_bitcell()
        
        # Checks 2x4 and 2-input NAND decoder
        debug.info(1, "Testing 16 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=16)
        self.local_check(a)

        # Checks 2x4 and 2-input NAND decoder with non-power-of-two
        debug.info(1, "Testing 17 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=17)
        self.local_check(a)

        # Checks 2x4 with 3x8 and 2-input NAND decoder
        debug.info(1, "Testing 32 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=32)
        self.local_check(a)

        # Checks 3 x 2x4 and 3-input NAND decoder
        debug.info(1, "Testing 64 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=64)
        self.local_check(a)

        # Checks 2x4 and 2 x 3x8 and 3-input NAND with non-power-of-two
        debug.info(1, "Testing 132 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=132)
        self.local_check(a)

        # Checks 3 x 3x8 and 3-input NAND decoder
        debug.info(1, "Testing 512 row sample for hierarchical_decoder")
        a = factory.create(module_type="hierarchical_decoder", num_outputs=512)
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
