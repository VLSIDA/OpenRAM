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

        # reset these options
        OPTS.check_lvsdrc = True
        OPTS.spice_version="hspice"
        OPTS.force_spice = False
        globals.set_spice()

        import delay

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.addr_size
        probe_data = s.word_size - 1
        debug.info(1, "Probe address {0} probe data {1}".format(probe_address, probe_data))

        d = delay.delay(s,tempspice)
        data = d.analyze(probe_address, probe_data)

        if OPTS.tech_name == "freepdk45":
            self.assertTrue(isclose(data['delay1'],0.013649)) # diff than hspice
            self.assertTrue(isclose(data['delay0'],0.22893)) # diff than hspice
            self.assertTrue(isclose(data['min_period1'],0.078582763671875)) # diff than hspice
            self.assertTrue(isclose(data['min_period0'],0.25543212890625)) # diff than hspice
        elif OPTS.tech_name == "scn3me_subm":
            self.assertTrue(isclose(data['delay1'],1.5342000000000002)) # diff than hspice
            self.assertTrue(isclose(data['delay0'],2.2698)) # diff than hspice
            self.assertTrue(isclose(data['min_period1'],1.534423828125)) # diff than hspice
            self.assertTrue(isclose(data['min_period0'],2.99560546875)) # diff than hspice
        else:
            self.assertTrue(False) # other techs fail

        os.remove(tempspice)

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
