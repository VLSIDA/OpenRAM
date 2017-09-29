#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 20_sram_test")


class single_bank_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import bank

        debug.info(1, "No column mux")
        a = bank.bank(word_size=4, num_words=16, words_per_row=1, num_banks=1, name="bank1")
        self.local_check(a)

        debug.info(1, "Two way column mux")
        a = bank.bank(word_size=4, num_words=32, words_per_row=2, num_banks=1, name="bank2")
        self.local_check(a)

        debug.info(1, "Four way column mux")
        a = bank.bank(word_size=4, num_words=64, words_per_row=4, num_banks=1, name="bank3")
        self.local_check(a)

        # Eight way has a short circuit of one column mux select to gnd rail
        # debug.info(1, "Eight way column mux")
        # a = bank.bank(word_size=2, num_words=128, words_per_row=8, num_banks=1, name="bank4")
        # self.local_check(a)
        
        OPTS.check_lvsdrc = True
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

        # reset the static duplicate name checker for unit tests
        import design
        design.design.name_map=[]
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
