#!/usr/bin/env python3
# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
Run a test on a multiport replica bitline
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class replica_bitline_multiport_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        stages=4
        fanout=4
        rows=13
        
        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.replica_bitcell = "replica_bitcell_1rw_1r"        
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0

        factory.reset()
        debug.info(2, "Testing 1rw 1r RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = factory.create(module_type="replica_bitline", delay_fanout_list=stages*[fanout], bitcell_loads=rows)
        self.local_check(a)
        
        # check replica bitline in pbitcell multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        factory.reset()
        debug.info(2, "Testing RBL pbitcell 1rw with {0} FO4 stages, {1} rows".format(stages,rows))
        a = factory.create(module_type="replica_bitline", delay_fanout_list=stages*[fanout], bitcell_loads=rows)
        self.local_check(a)

        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 1
        OPTS.num_r_ports = 1
        
        factory.reset()
        debug.info(2, "Testing RBL pbitcell 1rw 1w 1r with {0} FO4 stages, {1} rows".format(stages,rows))
        a = factory.create(module_type="replica_bitline", delay_fanout_list=stages*[fanout], bitcell_loads=rows)
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
