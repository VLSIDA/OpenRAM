#!/usr/bin/env python3
"""
Run a regression test on a sense amp array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
from sram_factory import factory

class sense_amp_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import sense_amp_array

        # check sense amp array for single port
        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=2")
        a = sense_amp_array.sense_amp_array(name="sa1", word_size=4, words_per_row=2)
        self.local_check(a)

        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=4")
        a = sense_amp_array.sense_amp_array(name="sa2", word_size=4, words_per_row=4)
        self.local_check(a)
        
        # check sense amp array for multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0

        factory.reset()
        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=2 (multi-port case)")
        a = sense_amp_array.sense_amp_array(name="sa3", word_size=4, words_per_row=2)
        self.local_check(a)

        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=4 (multi-port case)")
        a = sense_amp_array.sense_amp_array(name="sa4", word_size=4, words_per_row=4)
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
