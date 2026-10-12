#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, re, os
import unittest
from testutils import *

import openram
from openram import debug
from openram import OPTS


class lib_nonpow2_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import lib, get_probe_address
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

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
        debug.info(1, "Testing timing for sample 2 bit, 24 words SRAM with 1 bank")

        s = sram(c, "sram_2_24_1_{0}".format(OPTS.tech_name))

        probe_address = get_probe_address(s.s)
        self.assertLess(int(probe_address, 2), c.num_words)
        if num_spare_rows == 0:
            self.assertEqual(probe_address, "10111")

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        lib(out_dir=OPTS.openram_temp, sram=s.s, sp_file=tempspice, use_model=False)

        nametest = re.compile(r"\.lib$", re.IGNORECASE)
        lib_files = list(filter(nametest.search, os.listdir(OPTS.openram_temp)))
        self.assertTrue(len(lib_files) > 0)

        reload(characterizer)
        openram.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
