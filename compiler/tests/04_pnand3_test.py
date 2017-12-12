#!/usr/bin/env python2.7
"""
Run regresion tests on a parameterized pnand3.
This module doesn't generate a multi-finger 3-input nand gate.
It generates only a minimum size 3-input nand gate.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import verify

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 04_pnand3_test")
class pnand3_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import pnand3
        import tech

        debug.info(2, "Checking 3-input nand gate")
        tx = pnand3.pnand3(size=1)
        self.local_check(tx)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
    def local_check(self, tx):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        tx.sp_write(tempspice)
        tx.gds_write(tempgds)

        self.assertFalse(verify.run_drc(tx.name, tempgds))
        self.assertFalse(verify.run_lvs(tx.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
