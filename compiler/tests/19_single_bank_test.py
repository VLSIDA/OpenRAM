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

class single_bank_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from bank import bank
        from sram_config import sram_config

        c = sram_config(word_size=4,
                        num_words=16)

        c.words_per_row=1
        debug.info(1, "No column mux")
        a = bank(c, name="bank1_single")
        self.local_check(a)

        c.num_words=32
        c.words_per_row=2
        debug.info(1, "Two way column mux")
        a = bank(c, name="bank2_single")
        self.local_check(a)

        c.num_words=64
        c.words_per_row=4
        debug.info(1, "Four way column mux")
        a = bank(c, name="bank3_single")
        self.local_check(a)

        # Eight way has a short circuit of one column mux select to gnd rail
        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        debug.info(1, "Eight way column mux")
        a = bank(c, name="bank4_single")
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
