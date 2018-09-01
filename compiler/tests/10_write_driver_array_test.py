#!/usr/bin/env python3
"""
Run a regression test on a write driver array
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class write_driver_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import write_driver_array

        # check write driver array in single port
        debug.info(2, "Testing write_driver_array for columns=8, word_size=8")
        a = write_driver_array.write_driver_array(columns=8, word_size=8)
        self.local_check(a)

        debug.info(2, "Testing write_driver_array for columns=16, word_size=8")
        a = write_driver_array.write_driver_array(columns=16, word_size=8)
        self.local_check(a)
        
        # check write driver array in multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.rw_ports = 1
        OPTS.w_ports = 1
        OPTS.r_ports = 1
        
        debug.info(2, "Testing write_driver_array for columns=8, word_size=8")
        a = write_driver_array.write_driver_array(columns=8, word_size=8)
        self.local_check(a)

        debug.info(2, "Testing write_driver_array for columns=16, word_size=8")
        a = write_driver_array.write_driver_array(columns=16, word_size=8)
        self.local_check(a)
        
        #globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
