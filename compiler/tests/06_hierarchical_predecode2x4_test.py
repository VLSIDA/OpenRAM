#!/usr/bin/env python2.7
"""
Run a regresion test on a hierarchical_predecode2x4.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import verify

OPTS = globals.OPTS


class hierarchical_predecode2x4_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import hierarchical_predecode2x4 as pre
        import tech

        debug.info(1, "Testing sample for hierarchy_predecode2x4")
        a = pre.hierarchical_predecode2x4()
        self.local_check(a)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(verify.run_drc(a.name, tempgds))
        self.assertFalse(verify.run_lvs(a.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
