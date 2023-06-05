#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import OPTS


class timing_setup_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.spice_name="Xyce"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import setup_hold
        from openram import tech
        slews = [tech.spice["rise_time"]*2]

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sh = setup_hold(corner)
        data = sh.analyze(slews,slews)
        if OPTS.tech_name == "freepdk45":
            golden_data = {'hold_times_HL': [-0.0158691],
                           'hold_times_LH': [-0.0158691],
                           'setup_times_HL': [0.026855499999999997],
                           'setup_times_LH': [0.032959]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'hold_times_HL': [-0.0805664],
                           'hold_times_LH': [-0.11718749999999999],
                           'setup_times_HL': [0.16357419999999998],
                           'setup_times_LH': [0.1757812]}
        elif OPTS.tech_name == "sky130":
            golden_data = {'hold_times_HL': [-0.03173828],
                           'hold_times_LH': [-0.05615234],
                           'setup_times_HL': [0.078125],
                           'setup_times_LH': [0.1025391]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
