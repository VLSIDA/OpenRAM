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

# @unittest.skip("SKIPPING 21_regression_model_test")
class regression_model_test(openram_test):
    """ Compare the accuracy of the analytical model with a spice simulation. """

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import linear_regression
        from characterizer import neural_network
        from sram import sram
        from sram_config import sram_config
        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        debug.info(1, "Probe address {0} probe data bit {1}".format(probe_address, probe_data))

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        
        #m = linear_regression(s.s, tempspice, corner)
        m = neural_network(s.s, tempspice, corner)
        only_test = ['rise_delay']
        scores = m.cross_validation(only_test)
        accuracy_requirement = 0.75
        self.assertTrue(scores['rise_delay'] >= accuracy_requirement)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
