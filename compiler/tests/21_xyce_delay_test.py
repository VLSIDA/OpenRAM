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
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
from sram_factory import factory
import debug


class timing_sram_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.spice_name="xyce"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        from sram_config import sram_config
        c = sram_config(word_size=4,
                        num_words=16,
                        num_banks=1)
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
        # Combine info about port into all data
        data.update(port_data[0])

        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl': [0.24042560000000002],
                           'delay_lh': [0.24042560000000002],
                           'disabled_read0_power': [0.8981647999999998],
                           'disabled_read1_power': [0.9101543999999998],
                           'disabled_write0_power': [0.9270382999999998],
                           'disabled_write1_power': [0.9482969999999998],
                           'leakage_power': 2.9792199999999998,
                           'min_period': 0.938,
                           'read0_power': [1.1107930999999998],
                           'read1_power': [1.1143252999999997],
                           'slew_hl': [0.2800772],
                           'slew_lh': [0.2800772],
                           'write0_power': [1.1667769],
                           'write1_power': [1.0986076999999999]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'delay_hl': [1.884186],
                           'delay_lh': [1.884186],
                           'disabled_read0_power': [20.86336],
                           'disabled_read1_power': [22.10636],
                           'disabled_write0_power': [22.62321],
                           'disabled_write1_power': [23.316010000000002],
                           'leakage_power': 13.351170000000002,
                           'min_period': 7.188,
                           'read0_power': [29.90159],
                           'read1_power': [30.47858],
                           'slew_hl': [2.042723],
                           'slew_lh': [2.042723],
                           'write0_power': [32.13199],
                           'write1_power': [28.46703]}
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
