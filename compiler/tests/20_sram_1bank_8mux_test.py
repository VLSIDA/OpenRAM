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

#@unittest.skip("SKIPPING 20_sram_1bank_8mux_test")
class sram_1bank_8mux_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from sram import sram
        from sram_config import sram_config
        c = sram_config(word_size=2,
                        num_words=128,
                        num_banks=1)

        c.words_per_row=8
        debug.info(1, "Single bank, eight way column mux with control logic")
        a = sram(c, "sram")
        self.local_check(a, final_verification=True)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
