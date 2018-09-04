#!/usr/bin/env python3
"""
Run a regression test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

@unittest.skip("SKIPPING 19_psingle_bank_test")
class psingle_bank_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify

        from bank import bank
        OPTS.bitcell = "pbitcell"
        from sram_config import sram_config

        # testing all port configurations (with no column mux) to verify layout between bitcell array and peripheral circuitry
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 1
        OPTS.num_r_ports = 1
        c = sram_config(word_size=4,
                        num_words=16)
        c.words_per_row=1
        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        """
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        OPTS.num_rw_ports = c.num_rw_ports = 0
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 0
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 0

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 0
        OPTS.num_r_ports = c.num_r_ports = 0

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        # testing with various column muxes
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2
        
        c.num_words=32
        c.words_per_row=2
        debug.info(1, "Two way column mux")
        name = "bank2_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        c.num_words=64
        c.words_per_row=4
        debug.info(1, "Four way column mux")
        name = "bank3_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        # Eight way has a short circuit of one column mux select to gnd rail
        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        debug.info(1, "Eight way column mux")
        name = "bank4_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        """
        
        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
