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

class pdriver_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

        debug.info(2, "Testing inverter/buffer 4x 8x")
        # a tests the error message for specifying conflicting conditions
        #a = pdriver.pdriver(fanout = 4,size_list = [1,2,4,8])
        #self.local_check(a)
        
        b = factory.create(module_type="pdriver", size_list = [1,2,4,8])
        self.local_check(b)
        
        c = factory.create(module_type="pdriver", fanout = 50)
        self.local_check(c)
        
        d = factory.create(module_type="pdriver", fanout = 50, inverting = True)
        self.local_check(d)
        
        e = factory.create(module_type="pdriver", fanout = 64)
        self.local_check(e)
        
        f = factory.create(module_type="pdriver", fanout = 64, inverting = True)
        self.local_check(f)

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
