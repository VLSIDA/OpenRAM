#!/usr/bin/env python3
"""
Run a regression test on a hierarchical_predecode2x4.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class hierarchical_predecode2x4_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import hierarchical_predecode2x4 as pre
        import tech

        debug.info(1, "Testing sample for hierarchy_predecode2x4")
        a = pre.hierarchical_predecode2x4()
        self.local_check(a)

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
