#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os

import globals
from globals import OPTS
from sram_factory import factory
import debug

class timing_sram_test(openram_test):

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
        from characterizer import delay
        from modules import sram_config
        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        c = sram_config(word_size=4,
                        num_words=16,
                        num_banks=1,
                        num_spare_cols=num_spare_cols,
                        num_spare_rows=num_spare_rows)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        debug.info(1, "Probe address {0} probe data bit {1}".format(probe_address, probe_data))

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        d = delay(s.s, tempspice, corner)
        import tech
        loads = [tech.spice["dff_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        load_slews = []
        for slew in slews:
            for load in loads:
                load_slews.append((load, slew))
        data, port_data = d.analyze(probe_address, probe_data, load_slews)
        #Combine info about port into all data
        data.update(port_data[0])

        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl': [0.24671600000000002],
                           'delay_lh': [0.24671600000000002],
                           'disabled_read0_power': [0.1749204],
                           'disabled_read1_power': [0.1873704],
                           'disabled_write0_power': [0.204619],
                           'disabled_write1_power': [0.2262653],
                           'leakage_power': 0.0021375310000000002,
                           'min_period': 0.977,
                           'read0_power': [0.3856875],
                           'read1_power': [0.38856060000000003],
                           'slew_hl': [0.2842019],
                           'slew_lh': [0.2842019],
                           'write0_power': [0.45274410000000004],
                           'write1_power': [0.38727789999999995]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data =  {'delay_hl': [1.882508],
                            'delay_lh': [1.882508],
                            'disabled_read0_power': [7.487227],
                            'disabled_read1_power': [8.749013],
                            'disabled_write0_power': [9.268901],
                            'disabled_write1_power': [9.962973],
                            'leakage_power': 0.0046686359999999994,
                            'min_period': 7.188,
                            'read0_power': [16.64011],
                            'read1_power': [17.20825],
                            'slew_hl': [2.039655],
                            'slew_lh': [2.039655],
                            'write0_power': [19.31883],
                            'write1_power': [15.297369999999999]} 
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))

        globals.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
