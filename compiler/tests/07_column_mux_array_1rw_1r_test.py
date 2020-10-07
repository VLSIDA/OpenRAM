#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from testutils import *
import sys, os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug


class column_mux_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        globals.setup_bitcell()
        
        debug.info(1, "Testing sample for 2-way column_mux_array port 0")
        a = factory.create(module_type="column_mux_array", columns=8, word_size=4, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 2-way column_mux_array port 1")
        a = factory.create(module_type="column_mux_array", columns=8, word_size=4, bitcell_bl="bl1", bitcell_br="br1")
        self.local_check(a)

        debug.info(1, "Testing sample for 4-way column_mux_array port 0")
        a = factory.create(module_type="column_mux_array", columns=8, word_size=2, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 4-way column_mux_array port 1")
        a = factory.create(module_type="column_mux_array", columns=8, word_size=2, bitcell_bl="bl1", bitcell_br="br1")
        self.local_check(a)

        debug.info(1, "Testing sample for 8-way column_mux_array port 0")
        a = factory.create(module_type="column_mux_array", columns=16, word_size=2, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 8-way column_mux_array port 1")
        a = factory.create(module_type="column_mux_array", columns=16, word_size=2, bitcell_bl="bl1", bitcell_br="br1")
        self.local_check(a)
        
        globals.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
