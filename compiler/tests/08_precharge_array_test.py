#!/usr/bin/env python2.7
"""
Run a regresion test on a precharge array
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 08_precharge_test")


class precharge_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = False

        import precharge_array
        import tech

        debug.info(2, "Checking 3 column precharge")
        pc = precharge_array.precharge_array(columns=3, ptx_width=tech.drc["minwidth_tx"], beta=2)
        self.local_check(pc)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
    def local_check(self, pc):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        pc.sp_write(tempspice)
        pc.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(pc.name, tempgds))
        self.assertFalse(calibre.run_lvs(pc.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
