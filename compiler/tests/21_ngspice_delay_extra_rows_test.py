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
        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1,
                        num_spare_rows=3)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "0" + ("1" * (s.s.addr_size - 1))
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
            golden_data = {'slew_lh': [0.2592187],
                           'slew_hl': [0.2592187],
                           'delay_lh': [0.2465583],
                           'disabled_write0_power': [0.1924678],
                           'disabled_read0_power': [0.152483],
                           'write0_power': [0.3409064],
                           'disabled_read1_power': [0.1737818],
                           'read0_power': [0.3096708],
                           'read1_power': [0.3107916],
                           'delay_hl': [0.2465583],
                           'write1_power': [0.26915849999999997],
                           'leakage_power': 0.002044307,
                           'min_period': 0.898,
                           'disabled_write1_power': [0.201411]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'read1_power': [12.11658],
                           'write1_power': [10.52653],
                           'read0_power': [11.956710000000001],
                           'disabled_write0_power': [7.673665],
                           'disabled_write1_power': [7.981922000000001],
                           'slew_lh': [1.868836],
                           'slew_hl': [1.868836],
                           'delay_hl': [1.8598510000000001],
                           'delay_lh': [1.8598510000000001],
                           'leakage_power': 0.005457728,
                           'disabled_read0_power': [5.904712],
                           'min_period': 6.875,
                           'disabled_read1_power': [7.132159],
                           'write0_power': [13.406400000000001]}
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
