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

class pdriver_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify

        import pdriver

        debug.info(2, "Testing inverter/buffer 4x 8x")
        # a tests the error message for specifying conflicting conditions
        #a = pdriver.pdriver(fanout_size = 4,size_list = [1,2,4,8])
        #self.local_check(a)
        
        b = pdriver.pdriver(name="pdriver1", size_list = [1,2,4,8])
        self.local_check(b)
        
        c = pdriver.pdriver(name="pdriver2", fanout_size = 50)
        self.local_check(c)
        
        d = pdriver.pdriver(name="pdriver3", fanout_size = 50, neg_polarity = True)
        self.local_check(d)
        
        e = pdriver.pdriver(name="pdriver4", fanout_size = 64)
        self.local_check(e)
        
        f = pdriver.pdriver(name="pdriver5", fanout_size = 64, neg_polarity = True)
        self.local_check(f)

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
