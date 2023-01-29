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


class contact_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        from openram.tech import active_stack, poly_stack, beol_stacks

        # Don't do active because of nwell contact rules
        # Don't do metal3 because of min area rules
        for layer_stack in [poly_stack] + [beol_stacks[0]]:
            stack_name = ":".join(map(str, layer_stack))

            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = factory.create(module_type="contact", layer_stack=layer_stack, dimensions=(1, 1), directions=("H", "H"))
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

        # Only do multiple contacts for BEOL
        for layer_stack in beol_stacks:
            stack_name = ":".join(map(str, layer_stack))

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

        # Test the well taps
        # check vertical array with one in the middle and two ends
        layer_stack = active_stack
        stack_name = ":".join(map(str, layer_stack))

        debug.info(2, "1 x 1 {} nwell".format(stack_name))
        c = factory.create(module_type="contact",
                           layer_stack=layer_stack,
                           implant_type="n",
                           well_type="n")
        self.local_drc_check(c)

        debug.info(2, "1 x 1 {} pwell".format(stack_name))
        c = factory.create(module_type="contact",
                           layer_stack=layer_stack,
                           implant_type="p",
                           well_type="p")
        self.local_drc_check(c)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
