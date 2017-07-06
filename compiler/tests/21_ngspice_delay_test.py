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

#@unittest.skip("SKIPPING 21_ngspice_delay_test")
class timing_sram_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
        OPTS.spice_version="ngspice"
        OPTS.force_spice = True
        globals.set_spice()
        
        import sram

        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = sram.sram(word_size=OPTS.config.word_size,
                      num_words=OPTS.config.num_words,
                      num_banks=OPTS.config.num_banks,
                      name="test_sram1")

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
            self.assertTrue(isclose(data['delay1'][0],0.0268)) # diff than hspice
            self.assertTrue(isclose(data['delay0'][0],0.1127)) # diff than hspice
            self.assertTrue(isclose(data['slew1'][0],0.0231)) # diff than hspice
            self.assertTrue(isclose(data['slew0'][0],0.0276)) # diff than hspice
            self.assertTrue(isclose(data['min_period'],0.071)) # diff than hspice
            self.assertTrue(isclose(data['read0_power'],0.0227)) # diff than hspice
            self.assertTrue(isclose(data['read1_power'],0.0223)) # diff than hspice
            self.assertTrue(isclose(data['write0_power'],0.02001)) # diff than hspice
            self.assertTrue(isclose(data['write1_power'],0.0193)) # diff than hspice
        elif OPTS.tech_name == "scn3me_subm":
            self.assertTrue(isclose(data['delay1'][0],0.6228)) # diff than hspice
            self.assertTrue(isclose(data['delay0'][0],1.4147)) # diff than hspice
            self.assertTrue(isclose(data['slew1'][0],1.0567)) # diff than hspice
            self.assertTrue(isclose(data['slew0'][0],1.3454)) # diff than hspice
            self.assertTrue(isclose(data['min_period'],1.719)) # diff than hspice
            self.assertTrue(isclose(data['read0_power'],4.7812)) # diff than hspice
            self.assertTrue(isclose(data['read1_power'],5.5500)) # diff than hspice
            self.assertTrue(isclose(data['write0_power'],3.9314)) # diff than hspice
            self.assertTrue(isclose(data['write1_power'],3.4097)) # diff than hspice
        else:
            self.assertTrue(False) # other techs fail

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
