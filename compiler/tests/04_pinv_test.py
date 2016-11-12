#!/usr/bin/env python2.7
"""
Run regresion tests on a parameterized inverter
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 04_pinv_test")


class pinv_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import pinv
        import tech

        debug.info(2, "Checking min size inverter")
        OPTS.check_lvsdrc = False
        tx = pinv.pinv(name="a_inv_1", nmos_width=tech.drc["minwidth_tx"], beta=tech.parameter["pinv_beta"])
        OPTS.check_lvsdrc = True
        self.local_check(tx)

        debug.info(2, "Checking 2x min size inverter")
        OPTS.check_lvsdrc = False
        tx = pinv.pinv(name="a_inv_2", nmos_width=2 * tech.drc["minwidth_tx"], beta=tech.parameter["pinv_beta"])
        OPTS.check_lvsdrc = True
        self.local_check(tx)

        debug.info(2, "Checking 5x min size inverter")
        OPTS.check_lvsdrc = False
        tx = pinv.pinv(name="a_inv_5", nmos_width=5 * tech.drc["minwidth_tx"], beta=tech.parameter["pinv_beta"])
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
