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
        OPTS.spice_version="hspice"
        OPTS.force_spice = True
        globals.set_spice()

        import sram
        import setup_hold
        
        sh = setup_hold.setup_hold()
        [one_setup_time, zero_setup_time] = sh.setup_time()

        OPTS.check_lvsdrc = True
        if OPTS.tech_name == "freepdk45":
            self.assertTrue(isclose(one_setup_time,0.0146484375)) 
            self.assertTrue(isclose(zero_setup_time,0.008544921875)) 
        elif OPTS.tech_name == "scn3me_subm":
            self.assertTrue(isclose(one_setup_time,0.0927734375))
            self.assertTrue(isclose(zero_setup_time,-0.0244140625))
        else:
            self.assertTrue(False) # other techs fail

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
