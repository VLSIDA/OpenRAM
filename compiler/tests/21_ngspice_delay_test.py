#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header,isclose
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify

#@unittest.skip("SKIPPING 21_ngspice_delay_test")
class timing_sram_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.spice_name="ngspice"
        OPTS.analytical_delay = False
        # This is a hack to reload the characterizer __init__ with the spice version
        import characterizer
        reload(characterizer)
        from characterizer import delay

        import sram

        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=OPTS.config.word_size,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
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
            golden_data = {'read1_power': 0.026660760000000002,
                           'read0_power': 0.02711731,
                           'write0_power': 0.02501428,
                           'delay1': [0.04867702],
                           'delay0': [0.1423633],
                           'min_period': 0.332,
                           'write1_power': 0.024162890000000003,
                           'slew0': [0.02733451],
                           'slew1': [0.02121624]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'read1_power': 4.250786000000001,
                           'read0_power': 4.093461,
                           'write0_power': 2.762675,
                           'delay1': [0.920068],
                           'delay0': [2.051821],
                           'min_period': 6.563,
                           'write1_power': 2.4545719999999998,
                           'slew0': [1.342015],
                           'slew1': [1.040868]}
        else:
            self.assertTrue(False) # other techs fail

        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        # Check each result
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    self.assertTrue(isclose(data[k][i],golden_data[k][i],0.15))
            else:
                self.assertTrue(isclose(data[k],golden_data[k],0.15))

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
