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

class replica_column_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        debug.info(2, "Testing replica column for 6t_cell")
        a = factory.create(module_type="replica_column", rows=4, left_rbl=1, right_rbl=0, replica_bit=1)
        self.local_check(a)

        debug.info(2, "Testing replica column for 6t_cell")
        a = factory.create(module_type="replica_column", rows=4, left_rbl=1, right_rbl=1, replica_bit=6)
        self.local_check(a)
        
        debug.info(2, "Testing replica column for 6t_cell")
        a = factory.create(module_type="replica_column", rows=4, left_rbl=2, right_rbl=0, replica_bit=2)
        self.local_check(a)
        
        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
