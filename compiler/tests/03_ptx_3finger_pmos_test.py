#!/usr/bin/env python3
"Run a regression test on a basic parameterized transistors"

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
        import ptx
        import tech

        debug.info(2, "Checking three fingers PMOS")
        fet = ptx.ptx(width=tech.drc["minwidth_tx"],
                      mults=3,
                      tx_type="pmos",
                      connect_active=True,
                      connect_poly=True)
        self.local_drc_check(fet)

        globals.end_openram()
        

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
