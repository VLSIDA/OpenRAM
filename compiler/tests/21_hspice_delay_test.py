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

class timing_sram_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        from sram_config import sram_config
        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        # c = sram_config(word_size=32,
                        # num_words=256,
                        # num_banks=1)
        # c.words_per_row=2
        # OPTS.use_tech_delay_chain_size = True
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)
        #import sys
        #sys.exit(1)
        
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
        data, port_data = d.analyze(probe_address, probe_data, slews, loads)
        #Combine info about port into all data
        data.update(port_data[0])
     
        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl': [0.2383338],
                           'delay_lh': [0.2383338],
                           'leakage_power': 0.0014532999999999998,
                           'min_period': 0.898,
                           'read0_power': [0.30059800000000003],
                           'read1_power': [0.30061810000000005],
                           'slew_hl': [0.25358420000000004],
                           'slew_lh': [0.25358420000000004],
                           'write0_power': [0.34616749999999996],
                           'write1_power': [0.2792924]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'delay_hl': [1.7448],
                           'delay_lh': [1.7448],
                           'leakage_power': 0.0006356744000000001,
                           'min_period': 6.25,
                           'read0_power': [12.9846],
                           'read1_power': [12.9722],
                           'slew_hl': [1.7433],
                           'slew_lh': [1.7433],
                           'write0_power': [14.8772],
                           'write1_power': [11.7217]}
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
