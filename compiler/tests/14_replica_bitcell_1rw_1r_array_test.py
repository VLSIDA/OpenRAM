#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
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

class replica_bitcell_array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.replica_bitcell = "replica_bitcell_1rw_1r"
        OPTS.dummy_bitcell="dummy_bitcell_1rw_1r"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        
        debug.info(2, "Testing 4x4 array for cell_1rw_1r")
        a = factory.create(module_type="replica_bitcell_array", cols=4, rows=4, left_rbl=2, right_rbl=0, bitcell_ports=[0,1])
        self.local_check(a)

        debug.info(2, "Testing 4x4 array for cell_1rw_1r")
        a = factory.create(module_type="replica_bitcell_array", cols=4, rows=4, left_rbl=1, right_rbl=1, bitcell_ports=[0,1])
        self.local_check(a)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
