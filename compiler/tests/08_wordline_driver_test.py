#!/usr/bin/env python3
"""
Run a regression test on a wordline_driver array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

#@unittest.skip("SKIPPING 04_driver_test")

class wordline_driver_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import wordline_driver
        import tech

        # check wordline driver for single port
        debug.info(2, "Checking driver")
        tx = wordline_driver.wordline_driver(rows=8)
        self.local_check(tx)

        # check wordline driver for multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        debug.info(2, "Checking driver (multi-port case)")
        tx = wordline_driver.wordline_driver(rows=8)
        self.local_check(tx)

        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
