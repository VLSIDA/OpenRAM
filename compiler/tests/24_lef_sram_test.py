#!/usr/bin/env python2.7
"""
Check the LEF file for an SRMA
"""

import unittest
from testutils import header,isdiff
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()


class lef_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import sram
        import lef

        debug.info(1, "Testing LEF for sample 2 bit, 16 words SRAM with 1 bank")
        s = sram.sram(word_size=2,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
                      name="sram_2_16_1_{0}".format(OPTS.tech_name))

        OPTS.check_lvsdrc = True

        gdsfile = s.name + ".gds"
        leffile = s.name + ".lef"
        gdsname = OPTS.openram_temp + gdsfile
        lefname = OPTS.openram_temp + leffile
        s.gds_write(gdsname)
        lef.lef(gdsname,lefname,s)

        # let's diff the result with a golden model
        golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),leffile)
        self.assertEqual(isdiff(lefname,golden),True)

        os.system("rm {0}".format(gdsname))
        os.system("rm {0}".format(lefname))

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
