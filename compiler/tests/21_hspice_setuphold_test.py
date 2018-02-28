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

class timing_setup_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = False
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        import characterizer
        reload(characterizer)
        from characterizer import setup_hold
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)
            

        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sh = setup_hold.setup_hold(corner)
        data = sh.analyze(slews,slews)
        #print data
        if OPTS.tech_name == "freepdk45":
            golden_data = {'setup_times_LH': [0.014648399999999999],
                           'hold_times_LH': [0.0024414],
                           'hold_times_HL': [-0.0036620999999999997],
                           'setup_times_HL': [0.0085449]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'setup_times_LH': [0.08178709999999999],
                           'hold_times_LH': [0.0024414],
                           'hold_times_HL': [-0.0646973],
                           'setup_times_HL': [0.0390625]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        # Check each result
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    self.isclose(data[k][i],golden_data[k][i],0.15)
            else:
                self.isclose(data[k],golden_data[k],0.15)

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
