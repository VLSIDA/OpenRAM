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


class sram_wmask_1w_1r_func_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        OPTS.trim_netlist = False

        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 1
        openram.setup_bitcell()

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import functional
        from openram import sram_config
        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        c = sram_config(word_size=8,
                        num_words=16,
                        write_size=2,
                        num_banks=1,
                        num_spare_cols=num_spare_cols,
                        num_spare_rows=num_spare_rows)
        c.words_per_row = 1
        c.recompute_sizes()
        debug.info(1,
                   "Functional test for sram with {} bit words, {} words, {} words per row, {} bit writes, {} banks".format(
                       c.word_size,
                       c.num_words,
                       c.words_per_row,
                       c.write_size,
                       c.num_banks))
        s = factory.create(module_type="sram", sram_config=c)
        f = functional(s.s)
        (fail, error) = f.run()
        self.assertTrue(fail, error)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
