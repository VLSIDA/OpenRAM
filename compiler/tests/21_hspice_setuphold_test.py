#!/usr/bin/env python3
"""
Run a regression test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class timing_setup_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import setup_hold
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)
            
        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sh = setup_hold(corner)
        data = sh.analyze(slews,slews)
        #print data
        if OPTS.tech_name == "freepdk45":
            golden_data = {'hold_times_HL': [-0.0097656],
                           'hold_times_LH': [-0.0158691],
                           'setup_times_HL': [0.026855499999999997],
                           'setup_times_LH': [0.032959]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'hold_times_HL': [-0.15625],
                           'hold_times_LH': [-0.1257324],
                           'setup_times_HL': [0.2038574],
                           'setup_times_LH': [0.2893066]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
