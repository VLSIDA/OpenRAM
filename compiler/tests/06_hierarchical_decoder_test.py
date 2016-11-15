#!/usr/bin/env python2.7
"""
Run a regresion test on a thierarchy_decoder.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS


class hierarchical_decoder_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import hierarchical_decoder
        import tech

        debug.info(1, "Testing sample for hierarchy_decoder")
        OPTS.check_lvsdrc = False
        a = hierarchical_decoder.hierarchical_decoder(
            nand2_nmos_width=2 * tech.drc["minwidth_tx"], nand3_nmos_width=3 * tech.drc["minwidth_tx"], rows=4)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        debug.info(1, "Testing sample for hierarchy_decoder")
        OPTS.check_lvsdrc = False
        a = hierarchical_decoder.hierarchical_decoder(
            nand2_nmos_width=2 * tech.drc["minwidth_tx"], nand3_nmos_width=3 * tech.drc["minwidth_tx"], rows=8)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        debug.info(1, "Testing sample for hierarchy_decoder")
        OPTS.check_lvsdrc = False
        a = hierarchical_decoder.hierarchical_decoder(
            nand2_nmos_width=2 * tech.drc["minwidth_tx"], nand3_nmos_width=3 * tech.drc["minwidth_tx"], rows=32)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        debug.info(1, "Testing sample for hierarchy_decoder")
        OPTS.check_lvsdrc = False
        a = hierarchical_decoder.hierarchical_decoder(
            nand2_nmos_width=2 * tech.drc["minwidth_tx"], nand3_nmos_width=3 * tech.drc["minwidth_tx"], rows=128)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        debug.info(1, "Testing sample for hierarchy_decoder")
        OPTS.check_lvsdrc = False
        a = hierarchical_decoder.hierarchical_decoder(
            nand2_nmos_width=2 * tech.drc["minwidth_tx"], nand3_nmos_width=3 * tech.drc["minwidth_tx"], rows=512)
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

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
