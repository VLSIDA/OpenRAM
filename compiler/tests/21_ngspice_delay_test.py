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
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False
        OPTS.trim_netlist = False

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

        import sram
        import tech
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=OPTS.word_size,
                      num_words=OPTS.num_words,
                      num_banks=OPTS.num_banks,
                      name="sram1")

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
        data = d.analyze(probe_address, probe_data, slews, loads)

        if OPTS.tech_name == "freepdk45":
            golden_data = {'leakage_power': 0.0007348262,
                           'delay_lh': [0.05799613],
                           'read0_power': [0.0384102],
                           'read1_power': [0.03279848],
                           'write1_power': [0.03693655],
                           'write0_power': [0.02717752],
                           'slew_hl': [0.03607912],
                           'min_period': 0.742,
                           'delay_hl': [0.3929995],
                           'slew_lh': [0.02160862]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'delay_hl': [11.69536],
                            'delay_lh': [1.260921],
                            'leakage_power': 0.00039469710000000004,
                            'min_period': 20.0,
                            'read0_power': [4.40238],
                            'read1_power': [4.126633],
                            'slew_hl': [1.259555],
                            'slew_lh': [0.9150649],
                            'write0_power': [4.988347],
                            'write1_power': [4.473887]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        
        self.assertTrue(self.check_golden_data(data,golden_data,0.25))

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
