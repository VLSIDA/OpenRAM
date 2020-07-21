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
            golden_data = {'min_period': 0.898,
                           'write1_power': [0.2659137999999999],
                           'disabled_write0_power': [0.1782495],
                           'disabled_read0_power': [0.14490679999999997],
                           'write0_power': [0.3330119],
                           'disabled_write1_power': [0.1865223],
                           'leakage_power': 0.0014532,
                           'disabled_read1_power': [0.1627516],
                           'slew_lh': [0.25367799999999996],
                           'slew_hl': [0.25367799999999996],
                           'delay_lh': [0.23820930000000004],
                           'delay_hl': [0.23820930000000004],
                           'read1_power': [0.3005756],
                           'read0_power': [0.3005888]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'leakage_power': 0.0006356576000000001,
                           'write1_power': [11.292700000000002],
                           'read0_power': [12.98],
                           'disabled_write1_power': [8.3707],
                           'write0_power': [14.4447], 'delay_hl': [1.7445000000000002],
                           'disabled_read0_power': [6.4325],
                           'slew_hl': [1.7437],
                           'disabled_write0_power': [8.1307],
                           'slew_lh': [1.7437],
                           'read1_power': [12.9869],
                           'disabled_read1_power': [7.706],
                           'min_period': 6.25,
                           'delay_lh': [1.7445000000000002]}
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
