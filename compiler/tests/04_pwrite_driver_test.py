#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import header, openram_test
import sys
import os

import globals
from globals import OPTS
from sram_factory import factory
import debug

@unittest.skip("SKIPPING 04_pwrite_driver_test")
class pwrite_driver_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        debug.info(2, "Checking 1x pwrite_driver")
        tx = factory.create(module_type="pwrite_driver", size=1)
        self.local_check(tx)

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
