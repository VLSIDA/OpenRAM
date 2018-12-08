#!/usr/bin/env python3
"""
Run a regression test on a 2-row buffer cell
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

#os.system("chmod u+x 04_pdriver_test.py")

class pdriver_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify

        import pdriver

        debug.info(2, "Testing inverter/buffer 4x 8x")
        # a tests the error message for specifying conflicting conditions
        #a = pdriver.pdriver(fanout_size = 4,size_list = [1,2,4,8])
        b = pdriver.pdriver(size_list = [1,2,4,8])
        c = pdriver.pdriver(fanout_size = 50)
        d = pdriver.pdriver(fanout_size = 50, neg_polarity = True)
        e = pdriver.pdriver(fanout_size = 64)
        f = pdriver.pdriver(fanout_size = 64, neg_polarity = True)
        #self.local_check(a)
        self.local_check(b)
        self.local_check(c)
        self.local_check(d)
        self.local_check(e)
        self.local_check(f)

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
