#!/usr/bin/env python2.7
"""
Run a regresion test on a hierarchical_decoder.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class hierarchical_decoder_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import hierarchical_decoder
        import tech

        # Doesn't require hierarchical decoder
        # debug.info(1, "Testing 4 row sample for hierarchical_decoder")
        # a = hierarchical_decoder.hierarchical_decoder(rows=4)
        # self.local_check(a)

        # Doesn't require hierarchical decoder
        # debug.info(1, "Testing 8 row sample for hierarchical_decoder")
        # a = hierarchical_decoder.hierarchical_decoder(rows=8)
        # self.local_check(a)

        debug.info(1, "Testing 16 row sample for hierarchical_decoder")
        a = hierarchical_decoder.hierarchical_decoder(rows=16)
        self.local_check(a)

        debug.info(1, "Testing 32 row sample for hierarchical_decoder")
        a = hierarchical_decoder.hierarchical_decoder(rows=32)
        self.local_check(a)

        debug.info(1, "Testing 128 row sample for hierarchical_decoder")
        a = hierarchical_decoder.hierarchical_decoder(rows=128)
        self.local_check(a)

        debug.info(1, "Testing 512 row sample for hierarchical_decoder")
        a = hierarchical_decoder.hierarchical_decoder(rows=512)
        self.local_check(a)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
