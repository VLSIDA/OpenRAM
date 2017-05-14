#!/usr/bin/env python2.7
"""
Check the .lib file for an SRAM
"""

import unittest
from testutils import header,isapproxdiff
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()


class lib_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import sram
        import lib

        debug.info(1, "Testing timing for sample 2 bit, 16 words SRAM with 1 bank")
        total_size = 1024
        for word_size in [1,2,4,8,16,32,64]:
            num_words = total_size/word_size# OPTS.config.num_words
            s = sram.sram(word_size=word_size,
                          num_words=num_words,
                          num_banks=OPTS.config.num_banks,
                          name="sram_2_16_1_{0}".format(OPTS.tech_name))
            delay = s.analytical_model(0.1)


        OPTS.check_lvsdrc = True

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        filename = s.name + ".lib"        
        libname = OPTS.openram_temp + filename
        use_model = True
        lib.lib(libname,s,tempspice,use_model)
        

        # let's diff the result with a golden model
        golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),filename)
        # Randomly decided 10% difference between spice simulators is ok.
        if use_model != True:
            self.assertEqual(isapproxdiff(libname,golden,0.10),True)

        os.system("rm {0}".format(libname))

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()






