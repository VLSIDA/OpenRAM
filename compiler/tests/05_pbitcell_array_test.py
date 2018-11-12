#!/usr/bin/env python3
"""
Run a regression test on a basic array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

#@unittest.skip("SKIPPING 05_pbitcell_array_test")
class pbitcell_array_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import bitcell_array

        debug.info(2, "Testing 4x4 array for multiport bitcell, with read ports at the edge of the bit cell")
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 2
        OPTS.num_r_ports = 2
        OPTS.num_w_ports = 2
        a = bitcell_array.bitcell_array(name="pbitcell_array_Rport_edge", cols=4, rows=4)
        self.local_check(a)
            
        debug.info(2, "Testing 4x4 array for multiport bitcell, with write ports at the edge of the bit cell")
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 2
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 2
        a = bitcell_array.bitcell_array(name="pbitcell_array_Wport_edge", cols=4, rows=4)
        self.local_check(a)
        
        debug.info(2, "Testing 4x4 array for multiport bitcell, with read/write ports at the edge of the bit cell")
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 2
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0
        a = bitcell_array.bitcell_array(name="pbitcell_array_RWport_edge", cols=4, rows=4)
        self.local_check(a)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
