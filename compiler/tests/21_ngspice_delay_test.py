#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
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
        OPTS.check_lvsdrc = False
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        import characterizer
        reload(characterizer)
        from characterizer import delay
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

        import sram

        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=OPTS.word_size,
                      num_words=OPTS.num_words,
                      num_banks=OPTS.num_banks,
                      name="sram1")

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.addr_size
        probe_data = s.word_size - 1
        debug.info(1, "Probe address {0} probe data {1}".format(probe_address, probe_data))

        d = delay.delay(s,tempspice)
        import tech
        loads = [tech.spice["FF_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        data = d.analyze(probe_address, probe_data,slews,loads)
        if OPTS.tech_name == "freepdk45":
            golden_data = {'read1_power': 0.03228762,
                           'read0_power': 0.03281849,
                           'write0_power': 0.02902607,
                           'delay1': [0.059081419999999996],
                           'delay0': [0.1716648],
                           'min_period': 0.391,
                           'write1_power': 0.02879424,
                           'slew0': [0.02851539],
                           'slew1': [0.02319674]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'read1_power': 5.063901,
                           'read0_power': 4.926464999999999,
                           'write0_power': 3.480712,
                           'delay1': [1.044746],
                           'delay0': [2.23024],
                           'min_period': 6.563,
                           'write1_power': 3.1949449999999997,
                           'slew0': [1.3469],
                           'slew1': [1.035352]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        # Check each result
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    self.isclose(data[k][i],golden_data[k][i],0.15)
            else:
                self.isclose(data[k],golden_data[k],0.15)

        # reset these options
        OPTS.check_lvsdrc = True
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = True
        reload(characterizer)

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
