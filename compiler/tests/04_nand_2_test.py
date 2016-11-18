#!/usr/bin/env python2.7
"""
Run regresion tests on a parameterized nand_2.  This module doesn't
generate multi_finger 2_input nand gate.  It generate only the minimum
size 2_input nand gate that is nmos_width=2*tech.drc[minwidth_tx].
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre
import sys

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 04_nand_2_test")


class nand_2_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import nand_2
        import tech

        debug.info(2, "Checking 2-input nand gate")
        tx = nand_2.nand_2(name="a_nand_1", nmos_width=2 * tech.drc["minwidth_tx"])
        OPTS.check_lvsdrc = True
        self.local_check(tx)
        globals.end_openram()
        

    def local_check(self, tx):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        tx.sp_write(tempspice)
        tx.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(tx.name, tempgds))
        self.assertFalse(calibre.run_lvs(tx.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
