#!/usr/bin/env python2.7
"""
Run regresion tests on a parameterized bitcell
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 04_pbitcell_test")


class pbitcell_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import pbitcell
        import tech

        debug.info(2, "Bitcell with 2 write ports and 0 read ports")
        tx = pbitcell.pbitcell(num_write=2,num_read=0)
        self.local_check(tx)

        OPTS.check_lvsdrc = True
        globals.end_openram()


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
