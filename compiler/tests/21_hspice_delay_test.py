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

        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

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
        data = d.analyze(probe_address, probe_data, slews, loads)

        #Assumes single rw port (6t sram)
        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl0': [2.5829000000000004],
                            'delay_lh0': [0.2255964],
                            'leakage_power': 0.0019498999999999996,
                            'min_period': 4.844,
                            'read0_power0': [0.055371399999999994],
                            'read1_power0': [0.0520225],
                            'slew_hl0': [0.0794261],
                            'slew_lh0': [0.0236264],
                            'write0_power0': [0.06545659999999999],
                            'write1_power0': [0.057846299999999996]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'delay_hl0': [4.0249],
                            'delay_lh0': [2.2611],
                            'leakage_power': 0.0257389,
                            'min_period': 4.688,
                            'read0_power0': [24.9279],
                            'read1_power0': [24.0219],
                            'slew_hl0': [0.8500753999999999],
                            'slew_lh0': [0.4122653],
                            'write0_power0': [28.197600000000005],
                            'write1_power0': [25.685]}
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
