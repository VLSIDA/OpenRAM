#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header,isclose
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify

#@unittest.skip("SKIPPING 21_timing_sram_test")


class timing_setup_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.spice_version="hspice"
        OPTS.analytical_delay = False
        import characterizer
        reload(characterizer)
        from characterizer import setup_hold

        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        sh = setup_hold.setup_hold()
        data = sh.analyze(slews,slews)

        if OPTS.tech_name == "freepdk45":
            golden_data = {'setup_times_LH': [0.014648399999999999],
                           'hold_times_LH': [0.0024414],
                           'hold_times_HL': [-0.0036620999999999997],
                           'setup_times_HL': [0.0085449]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'setup_times_LH': [0.1000977],
                           'hold_times_LH': [0.020751999999999996],
                           'hold_times_HL': [-0.0830078],
                           'setup_times_HL': [0.020751999999999996]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        # Check each result
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    self.assertTrue(isclose(data[k][i],golden_data[k][i],0.10))
            else:
                self.assertTrue(isclose(data[k],golden_data[k],0.10))

        OPTS.check_lvsdrc = True
        OPTS.analytical_delay = True
        reload(characterizer)
        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
