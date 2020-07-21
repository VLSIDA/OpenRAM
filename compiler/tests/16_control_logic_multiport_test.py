#!/usr/bin/env python3
# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
Run a regression test on a control_logic
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class control_logic_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        import control_logic
        import tech

        # check control logic for multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell = "replica_pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 1
        OPTS.num_r_ports = 1

        debug.info(1, "Testing sample for control_logic for multiport, only write control logic")
        a = factory.create(module_type="control_logic", num_rows=128, words_per_row=1, word_size=8, port_type="rw")
        self.local_check(a)
        
        # OPTS.num_rw_ports = 0
        # OPTS.num_w_ports = 1
        debug.info(1, "Testing sample for control_logic for multiport, only write control logic")
        a = factory.create(module_type="control_logic", num_rows=128, words_per_row=1, word_size=8, port_type="w")
        self.local_check(a)
        
        # OPTS.num_w_ports = 0
        # OPTS.num_r_ports = 1
        debug.info(1, "Testing sample for control_logic for multiport, only read control logic")
        a = factory.create(module_type="control_logic", num_rows=128, words_per_row=1, word_size=8, port_type="r")
        self.local_check(a)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
