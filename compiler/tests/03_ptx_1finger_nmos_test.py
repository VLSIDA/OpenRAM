#!/usr/bin/env python2.7
"Run a regresion test on a basic parameterized transistors"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class ptx_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import ptx
        import tech

        debug.info(2, "Checking min size NMOS with 1 finger")
        fet = ptx.ptx(width=tech.drc["minwidth_tx"],
                      mults=1,
                      tx_type="nmos")
        self.local_drc_check(fet)

        OPTS.check_lvsdrc = True
        globals.end_openram()


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
