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


@unittest.skip("SKIPPING 12_tri_gate_array_test")
class tri_gate_array_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        debug.info(1, "Testing tri_gate_array for columns=8, word_size=8")
        a = factory.create(module_type="tri_gate_array", columns=8, word_size=8)
        self.local_check(a)

        debug.info(1, "Testing tri_gate_array for columns=16, word_size=8")
        a = factory.create(module_type="tri_gate_array", columns=16, word_size=8)
        self.local_check(a)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
