#!/usr/bin/env python2.7
"""
Run a regresion test on a basic array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

#@unittest.skip("SKIPPING 05_array_test")

class array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import bitcell_array

        debug.info(2, "Testing 4x4 array for 6t_cell")
        a = bitcell_array.bitcell_array(name="bitcell_array", cols=4, rows=4)
        self.local_check(a)

        OPTS.check_lvsdrc = True
        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
