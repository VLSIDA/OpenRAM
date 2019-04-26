#!/usr/bin/env python3
# See LICENSE for licensing information.
#
#Copyright (c) 2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
Run regression tests on a parameterized pnand3.
This module doesn't generate a multi-finger 3-input nand gate.
It generates only a minimum size 3-input nand gate.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class pnand3_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        debug.info(2, "Checking 3-input nand gate")
        tx = factory.create(module_type="pnand3", size=1)
        self.local_check(tx)

        globals.end_openram()
        

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
