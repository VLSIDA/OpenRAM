#!/usr/bin/env python2.7
"""
Check the .lib file for an SRAM
"""

import unittest
from testutils import header,isapproxdiff
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify

class lib_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.analytical_delay = False
        OPTS.trim_netlist = False
        import characterizer
        reload(characterizer)
        from characterizer import lib

        import sram

        debug.info(1, "Testing timing for sample 2 bit, 16 words SRAM with 1 bank")
        s = sram.sram(word_size=2,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
                      name="sram_2_16_1_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = True

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        filename = s.name + ".lib"     
        libname = OPTS.openram_temp + filename
        lib.lib(libname=libname,sram=s,spfile=tempspice,use_model=False)
        
        # let's diff the result with a golden model
        golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),filename)
        self.assertEqual(isapproxdiff(libname,golden,0.15),True)

        OPTS.analytical_delay = True
        OPTS.trim_netlist = True
        reload(characterizer)
        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()






