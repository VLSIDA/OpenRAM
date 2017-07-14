#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header,isclose
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 21_timing_sram_test")


class timing_setup_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.spice_version="ngspice"
        OPTS.force_spice = True
        globals.set_spice()
        
        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        import setup_hold
        
        sh = setup_hold.setup_hold()
        data = sh.analyze(slews,slews)

        # reset these options
        OPTS.check_lvsdrc = True
        OPTS.spice_version="hspice"
        OPTS.force_spice = False
        globals.set_spice()

        one_setup_time = data['setup_times_LH'][0]
        zero_setup_time = data['setup_times_HL'][0]
        one_hold_time = data['hold_times_LH'][0]
        zero_hold_time = data['hold_times_HL'][0]

        if OPTS.tech_name == "freepdk45":
            self.assertTrue(isclose(one_setup_time,0.0146)) 
            self.assertTrue(isclose(zero_setup_time,0.0085)) 
            self.assertTrue(isclose(one_hold_time,0.00244)) 
            self.assertTrue(isclose(zero_hold_time,-0.00366)) 
        elif OPTS.tech_name == "scn3me_subm":
            self.assertTrue(isclose(one_setup_time,0.1001)) 
            self.assertTrue(isclose(zero_setup_time,0.0208)) 
            self.assertTrue(isclose(one_hold_time,0.02075)) 
            self.assertTrue(isclose(zero_hold_time,-0.08301)) 
        else:
            self.assertTrue(False) # other techs fail

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
