#!/usr/bin/env python3
"""
Run a regression test on a 2 bank SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

@unittest.skip("Multibank is not working yet.")
class sram_2bank_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from sram_config import sram_config
        c = sram_config(word_size=16,
                        num_words=32,
                        num_banks=2)

        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Two bank, no column mux with control logic")
        factory.reset()
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        c.num_words=64
        c.words_per_row=2
        c.recompute_sizes()
        debug.info(1, "Two bank two way column mux with control logic")
        factory.reset()
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        c.num_words=128
        c.words_per_row=4
        c.recompute_sizes()
        debug.info(1, "Two bank, four way column mux with control logic")
        factory.reset()
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        c.word_size=2
        c.num_words=256
        c.words_per_row=8
        c.recompute_sizes()
        debug.info(1, "Two bank, eight way column mux with control logic")
        factory.reset()
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
