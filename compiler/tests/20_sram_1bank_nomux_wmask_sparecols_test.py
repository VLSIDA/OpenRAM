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
from openram.sram_factory import factory
from openram import OPTS


@unittest.skip("SKIPPING 20_sram_1bank_nomux_wmask_sparecols_test, not working yet")
class sram_1bank_nomux_wmask_sparecols_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram import sram_config

        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        c = sram_config(word_size=8,
                        write_size=4,
                        num_words=16,
                        num_banks=1,
                        num_spare_cols=num_spare_cols+2,
                        num_spare_rows=num_spare_rows)

        c.words_per_row = 1
        c.recompute_sizes()
        debug.info(1, "Layout test for {}rw,{}r,{}w sram "
                      "with {} bit words, {} words, {} bit writes, {} words per "
                      "row, {} spare columns, {} banks".format(OPTS.num_rw_ports,
                                                               OPTS.num_r_ports,
                                                               OPTS.num_w_ports,
                                                               c.word_size,
                                                               c.num_words,
                                                               c.write_size,
                                                               c.words_per_row,
                                                               c.num_spare_cols,
                                                               c.num_banks))
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
