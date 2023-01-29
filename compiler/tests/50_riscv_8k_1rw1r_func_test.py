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


@unittest.skip("SKIPPING 50_riscv_func_test")
class riscv_func_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        OPTS.trim_netlist = False

        OPTS.local_array_size = 16
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import functional
        from openram import sram_config
        c = sram_config(word_size=32,
                        write_size=8,
                        num_words=2048,
                        num_banks=1)

        debug.info(1, "Functional test RISC-V memory"
                   "{} bit words, {} words, {} words per row, {} banks".format(c.word_size,
                                                                               c.num_words,
                                                                               c.words_per_row,
                                                                               c.num_banks))
        s = factory.create(module_type="sram", sram_config=c)
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        f = functional(s.s, corner=corner, cycles=100)
        (fail, error) = f.run()
        self.assertTrue(fail, error)

        openram.end_openram()


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
