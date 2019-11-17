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
import sys,os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class timing_setup_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import setup_hold
        import sram
        import tech
        slews = [tech.spice["rise_time"]*2]
        
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sh = setup_hold(corner)
        data = sh.analyze(slews,slews)
        #print data
        if OPTS.tech_name == "freepdk45":
            golden_data = {'hold_times_HL': [-0.01586914],
                           'hold_times_LH': [-0.01586914],
                           'setup_times_HL': [0.02685547],
                           'setup_times_LH': [0.03295898]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'hold_times_HL': [-0.08056640999999999],
                           'hold_times_LH': [-0.1293945],
                           'setup_times_HL': [0.1757812],
                           'setup_times_LH': [0.1879883]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))
        
        reload(characterizer)
        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
