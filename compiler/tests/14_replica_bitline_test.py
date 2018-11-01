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

class replica_bitline_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import replica_bitline

        # check replica bitline in single port
        stages=4
        fanout=4
        rows=13
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        #debug.error("Exiting...", 1)
        
        stages=8
        rows=100
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        
        #check replica bitline in handmade multi-port 1rw+1r cell
        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.replica_bitcell = "replica_bitcell_1rw_1r"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 1
        stages=4
        fanout=4
        rows=13
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)

        stages=8
        rows=100
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        
        # check replica bitline in pbitcell multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        stages=4
        fanout=4
        rows=13
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)

        stages=8
        rows=100
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 1
        OPTS.num_r_ports = 1
        
        stages=4
        fanout=4
        rows=13
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        
        stages=8
        rows=100
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = replica_bitline.replica_bitline(stages,fanout,rows)
        self.local_check(a)
        
        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
