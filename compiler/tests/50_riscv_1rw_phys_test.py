#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug


#@unittest.skip("SKIPPING 50_riscv_phys_test")
class riscv_phys_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        from sram_config import sram_config

        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0
        OPTS.local_array_size = 16
        globals.setup_bitcell()
        OPTS.route_supplies = False
        OPTS.perimeter_pins = False

        c = sram_config(word_size=32,
                        write_size=8,
                        num_words=32,
                        num_banks=1,
                        num_spare_cols=num_spare_cols,
                        num_spare_rows=num_spare_rows)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Layout test for {}rw,{}r,{}w sram "
                   "with {} bit words, {} words, {} words per "
                   "row, {} banks".format(OPTS.num_rw_ports,
                                          OPTS.num_r_ports,
                                          OPTS.num_w_ports,
                                          c.word_size,
                                          c.num_words,
                                          c.words_per_row,
                                          c.num_banks))
        a = factory.create(module_type="sram", sram_config=c)
        self.local_check(a, final_verification=True)

        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
