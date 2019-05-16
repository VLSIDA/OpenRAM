#!/usr/bin/env python3
# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
Run a regression test on a tri_gate_array.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class tri_gate_array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        debug.info(1, "Testing tri_gate_array for columns=8, word_size=8")
        a = factory.create(module_type="tri_gate_array", columns=8, word_size=8)
        self.local_check(a)
        
        debug.info(1, "Testing tri_gate_array for columns=16, word_size=8")
        a = factory.create(module_type="tri_gate_array", columns=16, word_size=8)
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
