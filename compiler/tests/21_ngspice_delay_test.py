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
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


class timing_sram_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import delay
        from openram import sram_config
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
        from openram import tech
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
            golden_data = {'delay_hl': [0.2764415],
                           'delay_lh': [0.2764415],
                           'disabled_read0_power': [0.18364834],
                           'disabled_read1_power': [0.20878333999999998],
                           'disabled_write0_power': [0.24064433999999998],
                           'disabled_write1_power': [0.27207664],
                           'leakage_power': 0.0443369,
                           'min_period': 0.938,
                           'read0_power': [0.37790994],
                           'read1_power': [0.37646214],
                           'slew_hl': [0.0266144],
                           'slew_lh': [0.0266144],
                           'write0_power': [0.44694044],
                           'write1_power': [0.36824544000000003]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data =  {'delay_hl': [1.905376],
                            'delay_lh': [1.905376],
                            'disabled_read0_power': [7.673850999999999],
                            'disabled_read1_power': [10.051073],
                            'disabled_write0_power': [10.638803],
                            'disabled_write1_power': [10.385253],
                            'leakage_power': 2.704021,
                            'min_period': 6.875,
                            'read0_power': [17.583853],
                            'read1_power': [17.689162999999997],
                            'slew_hl': [0.19331199999999998],
                            'slew_lh': [0.19331199999999998],
                            'write0_power': [20.607043],
                            'write1_power': [16.107403]}

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
