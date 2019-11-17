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

class replica_pbitcell_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        import dummy_pbitcell
        
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0

        factory.reset()
        debug.info(2, "Checking dummy bitcell using pbitcell (small cell)")
        tx = dummy_pbitcell.dummy_pbitcell(name="rpbc")
        self.local_check(tx)
        
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1

        factory.reset()
        debug.info(2, "Checking dummy bitcell using pbitcell (large cell)")
        tx = dummy_pbitcell.dummy_pbitcell(name="rpbc")
        self.local_check(tx)

        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
