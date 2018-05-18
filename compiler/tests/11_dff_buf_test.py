#!/usr/bin/env python2.7
"""
Run a regresion test on a dff_buf.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class dff_buf_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import dff_buf

        debug.info(2, "Testing dff_buf 4x 8x")
        a = dff_buf.dff_buf(4, 8)
        self.local_check(a)

        OPTS.check_lvsdrc = True
        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
