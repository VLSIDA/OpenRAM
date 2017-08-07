#!/usr/bin/env python2.7
"""
Run a regresion test on various srams
"""

import unittest
from testutils import header,isclose
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 21_timing_sram_test")


class timing_sram_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.spice_version="hspice"
        OPTS.force_spice = True
        globals.set_spice()
        
        import sram

        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=OPTS.config.word_size,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
                      name="test_sram1")

        OPTS.check_lvsdrc = True

        import delay

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
            golden_data = {'read1_power': 0.017787999999999998,
                           'read0_power': 0.017827,
                           'write0_power': 0.016626,
                           'delay1': [0.02616],
                           'delay0': [0.10966999999999999],
                           'min_period': 0.264,
                           'write1_power': 0.015919000000000003,
                           'slew0': [0.027029],
                           'slew1': [0.021002999999999997]}
        elif OPTS.tech_name == "scn3me_subm":
            golden_data = {'read1_power': 4.5206,
                           'read0_power': 4.5492,
                           'write0_power': 3.8564,
                           'delay1': [0.5985562],
                           'delay0': [1.3725000000000003],
                           'min_period': 4.531,
                           'write1_power': 3.7291,
                           'slew0': [1.3013000000000001],
                           'slew1': [1.0045]}
        else:
            self.assertTrue(False) # other techs fail
        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))
        # Check each result
        for k in data.keys():
            if type(data[k])==list:
                for i in range(len(data[k])):
                    self.assertTrue(isclose(data[k][i],golden_data[k][i]))
            else:
                self.assertTrue(isclose(data[k],golden_data[k]))

                
        # reset these options
        OPTS.check_lvsdrc = True
        OPTS.spice_version="hspice"
        OPTS.force_spice = False
        globals.set_spice()

        os.remove(tempspice)

        globals.end_openram()
        
# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
