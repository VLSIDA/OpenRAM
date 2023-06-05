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


class pand2_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        #global verify
        from openram import verify

        from openram.modules import pand2

        debug.info(2, "Testing pand2 gate 4x")
        a = pand2(name="pand2x4", size=4)
        self.local_check(a)

        openram.end_openram()


# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
