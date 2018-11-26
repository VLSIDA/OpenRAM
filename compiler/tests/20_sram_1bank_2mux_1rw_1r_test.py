#!/usr/bin/env python3
"""
Run a regression test on a 1 bank, 2 port SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class sram_1bank_2mux_1rw_1r_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from sram import sram
        from sram_config import sram_config
        
        OPTS.bitcell = "bitcell_1rw_1r"
        OPTS.replica_bitcell = "replica_bitcell_1rw_1r"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        
        c = sram_config(word_size=4,
                        num_words=32,
                        num_banks=1)

        c.words_per_row=2
        debug.info(1, "Single bank, two way column mux 1rw, 1r with control logic")
        a = sram(c, "sram")
        self.local_check(a, final_verification=True)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
