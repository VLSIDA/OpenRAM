#!/usr/bin/env python2.7
"""
Run a regresion test on a 2 bank SRAM
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify

#@unittest.skip("SKIPPING 20_sram_test")


class sram_2bank_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import sram

        debug.info(1, "Two bank, no column mux with control logic")
        a = sram.sram(word_size=16, num_words=32, num_banks=2, name="sram1")
        self.local_check(a)

        debug.info(1, "Two bank two way column mux with control logic")
        a = sram.sram(word_size=16, num_words=64, num_banks=2, name="sram2")
        self.local_check(a)

        debug.info(1, "Two bank, four way column mux with control logic")
        a = sram.sram(word_size=16, num_words=128, num_banks=2, name="sram3")
        self.local_check(a)

        # debug.info(1, "Two bank, eight way column mux with control logic")
        # a = sram.sram(word_size=2, num_words=256 num_banks=2, name="sram4")
        # self.local_check(a)

        OPTS.check_lvsdrc = True
        globals.end_openram()
        
    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(verify.run_drc(a.name, tempgds))
        self.assertFalse(verify.run_lvs(a.name, tempgds, tempspice))
        #self.assertFalse(verify.run_pex(a.name, tempgds, tempspice, output=OPTS.openram_temp+"temp_pex.sp"))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
