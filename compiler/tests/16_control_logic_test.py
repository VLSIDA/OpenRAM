#!/usr/bin/env python3
"""
Run a regression test on a control_logic
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class control_logic_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import control_logic
        import tech

        # check control logic for single port
        debug.info(1, "Testing sample for control_logic")
        a = control_logic.control_logic(num_rows=128, words_per_row=1)
        self.local_check(a)
        
        # check control logic for multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        debug.info(1, "Testing sample for control_logic for multiport")
        a = control_logic.control_logic(num_rows=128, words_per_row=1)
        self.local_check(a)
        
        # Check port specific control logic
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 1
        OPTS.num_r_ports = 1

        debug.info(1, "Testing sample for control_logic for multiport, only write control logic")
        a = control_logic.control_logic(num_rows=128, words_per_row=1,  port_type="rw")
        self.local_check(a)
        
        debug.info(1, "Testing sample for control_logic for multiport, only write control logic")
        a = control_logic.control_logic(num_rows=128, words_per_row=1, port_type="w")
        self.local_check(a)
        
        debug.info(1, "Testing sample for control_logic for multiport, only read control logic")
        a = control_logic.control_logic(num_rows=128, words_per_row=1, port_type="r")
        self.local_check(a)

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
