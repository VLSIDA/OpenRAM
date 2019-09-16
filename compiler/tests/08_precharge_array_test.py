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

class precharge_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        # check precharge array in single port
        debug.info(2, "Checking 3 column precharge")
        pc = factory.create(module_type="precharge_array", columns=3)
        self.local_check(pc)
        
        # check precharge array in multi-port
        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0

        factory.reset()
        debug.info(2, "Checking 3 column precharge array for 1RW/1R bitcell")
        pc = factory.create(module_type="precharge_array", columns=3, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(pc)
        
        # debug.info(2, "Checking 3 column precharge array for pbitcell (innermost connections)")
        # pc = precharge_array.precharge_array(name="pre3", columns=3, bitcell_bl="bl0", bitcell_br="br0")
        # self.local_check(pc)
        
        # debug.info(2, "Checking 3 column precharge array for pbitcell (outermost connections)")
        # pc = precharge_array.precharge_array(name="pre4", columns=3, bitcell_bl="bl2", bitcell_br="br2")
        # self.local_check(pc)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
