#!/usr/bin/env python2.7
"Run a regresion test for DRC on basic contacts of different array sizes"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class contact_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import contact


        for layer_stack in [("poly", "contact", "metal1"), ("metal1", "via1", "metal2")]:
            stack_name = ":".join(map(str, layer_stack))

            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            c = contact.contact(layer_stack, (1, 1))
            self.local_drc_check(c)

            # check vertical array with one in the middle and two ends
            debug.info(2, "1 x 3 {} test".format(stack_name))
            c = contact.contact(layer_stack, (1, 3))
            self.local_drc_check(c)

            # check horizontal array with one in the middle and two ends
            debug.info(2, "3 x 1 {} test".format(stack_name))
            c = contact.contact(layer_stack, (3, 1))
            self.local_drc_check(c)

            # check 3x3 array for all possible neighbors
            debug.info(2, "3 x 3 {} test".format(stack_name))
            c = contact.contact(layer_stack, (3, 3))
            self.local_drc_check(c)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
