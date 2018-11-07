#!/usr/bin/env python3
"""
Run regression tests on a parameterized inverter
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class pinv_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import pinv
        import tech

        debug.info(2, "Checking 2x size inverter")
        tx = pinv.pinv(size=2)
        self.local_check(tx)

        globals.end_openram()        


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
