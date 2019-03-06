#!/usr/bin/env python3
"""
Run a regression test on a basic array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

#@unittest.skip("SKIPPING 05_bitcell_1rw_1r_array_test")

class bitcell_1rw_1r_array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        debug.info(2, "Testing 4x4 array for cell_1rw_1r")
        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        a = factory.create(module_type="bitcell_array", cols=4, rows=4)
        self.local_check(a)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
