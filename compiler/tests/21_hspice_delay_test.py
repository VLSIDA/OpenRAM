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

class timing_sram_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        from sram import sram
        from sram_config import sram_config
        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram(c, name="sram1")

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        debug.info(1, "Probe address {0} probe data bit {1}".format(probe_address, probe_data))

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        d = delay(s.s, tempspice, corner)
        import tech
        loads = [tech.spice["msflop_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        data, port_data = d.analyze(probe_address, probe_data, slews, loads)
        #Combine info about port into all data
        data.update(port_data[0])
        
        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl': [0.2011],
                         'delay_lh': [0.2011],
                         'leakage_power': 0.0014218000000000002,
                         'min_period': 0.41,
                         'read0_power': [0.63604],
                         'read1_power': [0.6120599999999999],
                         'slew_hl': [0.10853],
                         'slew_lh': [0.10853],
                         'write0_power': [0.51742],
                         'write1_power': [0.51095]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'delay_hl': [1.3911],
                         'delay_lh': [1.3911],
                         'leakage_power': 0.0278488,
                         'min_period': 2.812,
                         'read0_power': [22.1183],
                         'read1_power': [21.4388],
                         'slew_hl': [0.7397553],
                         'slew_lh': [0.7397553],
                         'write0_power': [19.4103],
                         'write1_power': [20.1167]}
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
    unittest.main()
