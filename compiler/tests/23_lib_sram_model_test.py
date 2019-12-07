#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys,os,re
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug

#@unittest.skip("SKIPPING 23_lib_sram_model_test")
class lib_sram_model_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.nominal_corner_only = False
        OPTS.netlist_only = True
        
        from characterizer import lib
        from sram import sram
        from sram_config import sram_config
        c = sram_config(word_size=2,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing analytical timing for sample 2 bit, 16 words SRAM with 1 bank")

        # This doesn't have to use the factory since worst case
        # it will just replaece the top-level module of the same name
        s = sram(c, "sram_2_16_1_{0}".format(OPTS.tech_name))
        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        lib(out_dir=OPTS.openram_temp, sram=s.s, sp_file=tempspice, use_model=True)

        # get all of the .lib files generated
        files = os.listdir(OPTS.openram_temp)
        nametest = re.compile("\.lib$", re.IGNORECASE)
        lib_files = filter(nametest.search, files)

        # and compare them with the golden model
        for filename in lib_files:
            newname = filename.replace(".lib","_analytical.lib")
            libname = "{0}/{1}".format(OPTS.openram_temp,filename)
            golden = "{0}/golden/{1}".format(os.path.dirname(os.path.realpath(__file__)),newname)
            self.assertTrue(self.isapproxdiff(libname,golden,0.15))
            
        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())






