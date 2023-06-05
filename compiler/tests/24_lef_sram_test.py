#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
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


@unittest.skip("SKIPPING 24_lef_sram_test")
class lef_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.route_supplies=False
        OPTS.check_lvsdrc=False
        from openram import sram
        from openram import sram_config
        c = sram_config(word_size=2,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing LEF for sample 2 bit, 16 words SRAM with 1 bank")
        # This doesn't have to use the factory since worst case
        # it will just replaece the top-level module of the same name
        s = sram(c, "sram_2_16_1_{0}".format(OPTS.tech_name))

        gdsfile = s.name + ".gds"
        leffile = s.name + ".lef"
        gdsname = OPTS.openram_temp + gdsfile
        lefname = OPTS.openram_temp + leffile
        s.gds_write(gdsname)
        s.lef_write(lefname)

        # let's diff the result with a golden model
        golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)), leffile)
        self.assertTrue(self.isdiff(lefname, golden))

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
