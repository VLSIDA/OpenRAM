#!/usr/bin/env python2.7
"""
Check the .lib file for an SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os,re
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class lib_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = False

        import sram
        from characterizer import lib

        debug.info(1, "Testing timing for sample 2 bit, 16 words SRAM with 1 bank")
        s = sram.sram(word_size=2,
                      num_words=16,
                      num_banks=1,
                      name="sram_2_16_1_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = True

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        lib.lib(out_dir=OPTS.openram_temp, sram=s, sp_file=tempspice, use_model=True)

        # get all of the .lib files generated
        files = os.listdir(OPTS.openram_temp)
        nametest = re.compile("\.lib$", re.IGNORECASE)
        lib_files = filter(nametest.search, files)

        # and compare them with the golden model
        for filename in lib_files:
            newname = filename.replace(".lib","_analytical.lib")
            libname = "{0}/{1}".format(OPTS.openram_temp,filename)
            golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),newname)
            self.isapproxdiff(libname,golden,0.15)
            
        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()






