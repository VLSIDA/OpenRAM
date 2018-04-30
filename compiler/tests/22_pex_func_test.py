#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class sram_func_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify

        #Initialize options
        OPTS.check_lvsdrc = False
        OPTS.use_pex = False
        OPTS.spice_name="" # Unset to use any simulator
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        import characterizer
        reload(characterizer)
        from characterizer import delay
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

        import sram

        #create sram test bank
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=2,
                      num_words=16,
                      num_banks=1,
                      name="pex_sram_test")

        #important
        OPTS.check_lvsdrc = True
        OPTS.use_pex = True

        # trimming the netlist doesn't make much time difference
        # OPTS.trim_netlist = False

        #Write a temporary spice file for analysis
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"
        s.sp_write(tempspice)
        s.gds_write(tempgds)

        #Run and debug pex test. This goes to verify folder and run_pex function
        self.assertFalse(verify.run_pex(s.name, tempgds, tempspice, output=None))

        #os.remove(tempspice)
        OPTS.analytical_delay = True
        reload(characterizer)
        globals.end_openram()
        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
