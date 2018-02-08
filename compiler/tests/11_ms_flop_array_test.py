#!/usr/bin/env python2.7
"""
Run a regresion test on a dff_array.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class dff_array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import ms_flop_array

        debug.info(2, "Testing ms_flop_array for columns=8, word_size=8")
        a = ms_flop_array.ms_flop_array(columns=8, word_size=8)
        self.local_check(a)

        debug.info(2, "Testing ms_flop_array for columns=16, word_size=8")
        a = ms_flop_array.ms_flop_array(columns=16, word_size=8)
        self.local_check(a)
        
        OPTS.check_lvsdrc = True
        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
