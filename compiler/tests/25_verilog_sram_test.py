#!/usr/bin/env python2.7
"""
Check the  .v file for an SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class verilog_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import sram

        debug.info(1, "Testing Verilog for sample 2 bit, 16 words SRAM with 1 bank")
        s = sram.sram(word_size=2,
                      num_words=OPTS.num_words,
                      num_banks=OPTS.num_banks,
                      name="sram_2_16_1_{0}".format(OPTS.tech_name))

        OPTS.check_lvsdrc = True

        vfile = s.name + ".v"
        vname = OPTS.openram_temp + vfile
        s.verilog_write(vname)


        # let's diff the result with a golden model
        golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),vfile)
        self.isdiff(vname,golden)

        os.system("rm {0}".format(vname))

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
