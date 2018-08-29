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

        debug.info(2, "Checking 3 column precharge")
        pc = precharge_array.precharge_array(columns=3)
        self.local_check(pc)
        
        debug.info(2, "Checking precharge for pbitcell")
        OPTS.bitcell = "pbitcell"
        OPTS.rw_ports = 2
        OPTS.r_ports = 2
        OPTS.w_ports = 2
        
        pc = precharge_array.precharge_array(columns=3, bitcell_bl="rwbl0", bitcell_br="rwbl_bar0")
        self.local_check(pc)
        
        pc = precharge_array.precharge_array(columns=3, bitcell_bl="wbl0", bitcell_br="wbl_bar0")
        self.local_check(pc)
        
        pc = precharge_array.precharge_array(columns=3, bitcell_bl="rbl0", bitcell_br="rbl_bar0")
        self.local_check(pc)

        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
