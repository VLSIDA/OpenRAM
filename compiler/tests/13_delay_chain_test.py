#!/usr/bin/env python3
"""
Run a test on a delay chain
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class delay_chain_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import delay_chain

        debug.info(2, "Testing delay_chain")
        a = delay_chain.delay_chain(fanout_list=[4, 4, 4, 4])
        self.local_check(a)

        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
