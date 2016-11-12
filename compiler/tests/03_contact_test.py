#!/usr/bin/env python2.7
"Run a regresion test for DRC on basic contacts of different array sizes"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 03_contact_test")


class contact_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import contact


        for layer_stack in [("poly", "contact", "metal1"), ("metal1", "via1", "metal2")]:
            stack_name = ":".join(map(str, layer_stack))

            # Check single 1 x 1 contact"
            debug.info(2, "1 x 1 {} test".format(stack_name))
            OPTS.check_lvsdrc = False
            c = contact.contact(layer_stack, (1, 1))
            OPTS.check_lvsdrc = True
            self.local_check(c)

            # check vertical array with one in the middle and two ends
            debug.info(2, "1 x 3 {} test".format(stack_name))
            OPTS.check_lvsdrc = False
            c = contact.contact(layer_stack, (1, 3))
            OPTS.check_lvsdrc = True
            self.local_check(c)

            # check horizontal array with one in the middle and two ends
            debug.info(2, "3 x 1 {} test".format(stack_name))
            OPTS.check_lvsdrc = False
            c = contact.contact(layer_stack, (3, 1))
            OPTS.check_lvsdrc = True
            self.local_check(c)

            # check 3x3 array for all possible neighbors
            debug.info(2, "3 x 3 {} test".format(stack_name))
            OPTS.check_lvsdrc = False
            c = contact.contact(layer_stack, (3, 3))
            OPTS.check_lvsdrc = True
            self.local_check(c)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
    def local_check(self, c):
        tempgds = OPTS.openram_temp + "temp.gds"
        c.gds_write(tempgds)
        self.assertFalse(calibre.run_drc(c.name, tempgds))
        os.remove(tempgds)


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
