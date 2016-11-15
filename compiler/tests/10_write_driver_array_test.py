#!/usr/bin/env python2.7
"""
Run a regresion test on a write driver array
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 10_write_driver_test")


class write_driver_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import write_driver_array

        debug.info(2, "Testing write_driver_array for columns=16, word_size=4")
        OPTS.check_lvsdrc = False
        a = write_driver_array.write_driver_array(columns=16, word_size=4)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        debug.info(2, "Testing write_driver_array for columns=128, word_size=128")
        OPTS.check_lvsdrc = False
        a = write_driver_array.write_driver_array(columns=16, word_size=16)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        globals.end_openram()

    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(a.name, tempgds))
        self.assertFalse(calibre.run_lvs(a.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
