#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys,os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class ptx_3finger_pmos_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        import tech

        debug.info(2, "Checking three fingers PMOS")
        fet = factory.create(module_type="ptx",
                             width=tech.drc["minwidth_tx"],
                             mults=3,
                             tx_type="pmos",
                             connect_source_active=True,
                             connect_drain_active=True,
                             connect_poly=True)
        self.local_drc_check(fet)

        globals.end_openram()
        

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
