#!/usr/bin/env python3
"""
Run a regression test on a hierarchical_decoder.
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

        # check hierarchical decoder for single port
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
        
        # check hierarchical decoder for multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        debug.info(1, "Testing 16 row sample for hierarchical_decoder (multi-port case)")
        a = hierarchical_decoder.hierarchical_decoder(rows=16)
        self.local_check(a)

        debug.info(1, "Testing 32 row sample for hierarchical_decoder (multi-port case)")
        a = hierarchical_decoder.hierarchical_decoder(rows=32)
        self.local_check(a)

        debug.info(1, "Testing 128 row sample for hierarchical_decoder (multi-port case)")
        a = hierarchical_decoder.hierarchical_decoder(rows=128)
        self.local_check(a)

        debug.info(1, "Testing 512 row sample for hierarchical_decoder (multi-port case)")
        a = hierarchical_decoder.hierarchical_decoder(rows=512)
        self.local_check(a)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
