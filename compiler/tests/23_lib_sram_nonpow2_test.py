#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram import OPTS


class lib_nonpow2_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.netlist_only = True

        from openram.characterizer.charutils import get_probe_address

        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        from openram import sram
        from openram import sram_config
        # 24 words need 5 address bits, so all ones (31) is not a word
        c = sram_config(word_size=2,
                        num_words=24,
                        num_banks=1,
                        num_spare_cols=num_spare_cols,
                        num_spare_rows=num_spare_rows)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing probe address for sample 2 bit, 24 words SRAM with 1 bank")

        s = sram(c, "sram_2_24_1_{0}".format(OPTS.tech_name))

        probe_address = get_probe_address(s.s)
        self.assertLess(int(probe_address, 2), c.num_words)
        self.assertEqual(len(probe_address), s.s.addr_size)
        if num_spare_rows == 0:
            self.assertEqual(probe_address, "10111")

        openram.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
