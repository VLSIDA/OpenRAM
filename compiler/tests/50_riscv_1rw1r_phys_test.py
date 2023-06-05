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


# @unittest.skip("SKIPPING 50_riscv_phys_test")
class riscv_phys_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram import sram_config

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        OPTS.local_array_size = 16
        openram.setup_bitcell()
        OPTS.route_supplies = False
        OPTS.perimeter_pins = False

        c = sram_config(word_size=32,
                        write_size=8,
                        num_words=256,
                        num_banks=1)

        c.words_per_row=2
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

        openram.end_openram()


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
