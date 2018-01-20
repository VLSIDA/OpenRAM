#!/usr/bin/env python2.7
"Run a regresion test on a basic parameterized transistors"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class ptx_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import ptx
        import tech

        debug.info(2, "Checking three fingers NMOS")
        fet = ptx.ptx(width=tech.drc["minwidth_tx"],
                      mults=4,
                      tx_type="nmos",
                      connect_active=True,
                      connect_poly=True)
        self.local_check(fet)

        OPTS.check_lvsdrc = True
        globals.end_openram()

    def local_check(self, fet):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        fet.sp_write(tempspice)
        fet.gds_write(tempgds)

        self.assertFalse(verify.run_drc(fet.name, tempgds))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
