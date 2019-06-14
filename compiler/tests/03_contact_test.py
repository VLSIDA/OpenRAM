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

class contact_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        for layer_stack in [("metal1", "via1", "metal2"), ("poly", "contact", "metal1")]:
            stack_name = ":".join(map(str, layer_stack))

            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 1))
            self.local_drc_check(c)
            
            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 1), directions=("H","V"))
            self.local_drc_check(c)

            # Check single x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 1), directions=("H","H"))
            self.local_drc_check(c)

            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 1), directions=("V","V"))
            self.local_drc_check(c)
            
            # check vertical array with one in the middle and two ends
            debug.info(2, "1 x 3 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 3))
            self.local_drc_check(c)

            # check horizontal array with one in the middle and two ends
            debug.info(2, "3 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(3, 1))
            self.local_drc_check(c)

            # check 3x3 array for all possible neighbors
            debug.info(2, "3 x 3 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(3, 3))
            self.local_drc_check(c)

        globals.end_openram()
        


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
