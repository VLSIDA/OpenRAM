#!/usr/bin/env python3
"""
Run a regression test on a 1 bank SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

#@unittest.skip("SKIPPING 20_psram_1bank_test, multiport layout not complete")
class sram_1bank_test(openram_test):

    def runTest(self):        
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from sram import sram
        from sram_config import sram_config
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell="replica_pbitcell"
        
        # testing layout of sram using pbitcell with 1 RW port (a 6T-cell equivalent)
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        c = sram_config(word_size=4,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
       
        c.num_words=32
        c.words_per_row=2
        debug.info(1, "Single bank two way column mux with control logic")
        a = sram(c, "sram2")
        self.local_check(a, final_verification=True)
        """
        c.num_words=64
        c.words_per_row=4
        debug.info(1, "Single bank, four way column mux with control logic")
        a = sram(c, "sram3")
        self.local_check(a, final_verification=True)

        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        debug.info(1, "Single bank, eight way column mux with control logic")
        a = sram(c, "sram4")
        self.local_check(a, final_verification=True)
        
        # testing sram using pbitcell in various port combinations
        # layout for multiple ports does not work yet
        """
        OPTS.netlist_only = True
        
        c.num_words=16
        c.words_per_row=1
        
        OPTS.num_rw_ports = 2
        OPTS.num_w_ports = 2
        OPTS.num_r_ports = 2
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
        """
        OPTS.num_rw_ports = 0
        OPTS.num_w_ports = 2
        OPTS.num_r_ports = 2
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
        
        OPTS.num_rw_ports = 2
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 2
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
        
        OPTS.num_rw_ports = 2
        OPTS.num_w_ports = 2
        OPTS.num_r_ports = 0
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
        
        OPTS.num_rw_ports = 2
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        
        debug.info(1, "Single bank, no column mux with control logic")
        a = sram(c, "sram1")
        self.local_check(a, final_verification=True)
        
        # testing with various column muxes
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2

        c.num_words=32
        c.words_per_row=2
        debug.info(1, "Single bank two way column mux with control logic")
        a = sram(c, "sram2")
        self.local_check(a, final_verification=True)

        c.num_words=64
        c.words_per_row=4
        debug.info(1, "Single bank, four way column mux with control logic")
        a = sram(c, "sram3")
        self.local_check(a, final_verification=True)

        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        debug.info(1, "Single bank, eight way column mux with control logic")
        a = sram(c, "sram4")
        self.local_check(a, final_verification=True)
        """
        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
