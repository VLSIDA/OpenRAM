#!/usr/bin/env python3
"""
Run a regression test on a precharge array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class precharge_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import precharge_array
        import tech

        # check precharge array in single port
        debug.info(2, "Checking 3 column precharge")
        pc = precharge_array.precharge_array(columns=3)
        self.local_check(pc)
        
        # check precharge array in multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1
        
        debug.info(2, "Checking 3 column precharge array for pbitcell (innermost connections)")
        pc = precharge_array.precharge_array(columns=3, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(pc)
        
        debug.info(2, "Checking 3 column precharge array for pbitcell (outermost connections)")
        pc = precharge_array.precharge_array(columns=3, bitcell_bl="bl2", bitcell_br="br2")
        self.local_check(pc)

        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
