#!/usr/bin/env python3
"""
Run a regression test on a wordline_driver array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
from sram_factory import factory

#@unittest.skip("SKIPPING 04_driver_test")

class single_level_column_mux_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import single_level_column_mux
        import tech
        
        # check single level column mux in single port
        debug.info(2, "Checking column mux")
        tx = single_level_column_mux.single_level_column_mux(name="mux8", tx_size=8)
        self.local_check(tx)
        
        # check single level column mux in multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1

        factory.reset()
        debug.info(2, "Checking column mux for pbitcell (innermost connections)")
        tx = single_level_column_mux.single_level_column_mux(name="mux8_2", tx_size=8, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(tx)
        
        factory.reset()
        debug.info(2, "Checking column mux for pbitcell (outermost connections)")
        tx = single_level_column_mux.single_level_column_mux(name="mux8_3", tx_size=8, bitcell_bl="bl2", bitcell_br="br2")
        self.local_check(tx)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
