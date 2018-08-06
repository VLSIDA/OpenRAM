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
            golden_data = {'delay_hl': [2.5614],
                            'delay_lh': [0.22929839999999999],
                            'leakage_power': 0.0020326,
                            'min_period': 4.844,
                            'read0_power': [0.0497676],
                            'read1_power': [0.0463576],
                            'slew_hl': [0.1119293],
                            'slew_lh': [0.0237043],
                            'write0_power': [0.0494321],
                            'write1_power': [0.0457268]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'delay_hl': [6.0052],
                            'delay_lh': [2.2886],
                            'leakage_power': 0.025629199999999998,
                            'min_period': 9.375,
                            'read0_power': [8.8721],
                            'read1_power': [8.3179],
                            'slew_hl': [1.0746],
                            'slew_lh': [0.413426],
                            'write0_power': [8.6601],
                            'write1_power': [8.0397]}
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
