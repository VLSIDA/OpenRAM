#!/usr/bin/env python3
"""
Run a regression test on a replica pbitcell
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class replica_pbitcell_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import replica_pbitcell
        import tech
        
        # check precharge in multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0
        
        debug.info(2, "Checking replica bitcell using pbitcell (small cell)")
        tx = replica_pbitcell.replica_pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1
        
        debug.info(2, "Checking replica bitcell using pbitcell (large cell)")
        tx = replica_pbitcell.replica_pbitcell()
        self.local_check(tx)

        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
