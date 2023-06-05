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
from testutils import header, openram_test

import openram
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


@unittest.skip("SKIPPING 04_pwrite_driver_test")
class pwrite_driver_test(openram_test):

    def runTest(self):
        openram.init_openram("config_{0}".format(OPTS.tech_name), is_unit_test=True)

        debug.info(2, "Checking 1x pwrite_driver")
        tx = factory.create(module_type="pwrite_driver", size=1)
        self.local_check(tx)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
