#!/usr/bin/env python2.7
"""
Run a regresion test on a single transistor column_mux.
"""

from testutils import header,openram_test,unittest
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class single_level_column_mux_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import single_level_column_mux_array
        
        debug.info(1, "Testing sample for 2-way column_mux_array")
        a = single_level_column_mux_array.single_level_column_mux_array(columns=16, word_size=8)
        self.local_check(a)

        debug.info(1, "Testing sample for 4-way column_mux_array")
        a = single_level_column_mux_array.single_level_column_mux_array(columns=16, word_size=4)
        self.local_check(a)

        debug.info(1, "Testing sample for 8-way column_mux_array")
        a = single_level_column_mux_array.single_level_column_mux_array(columns=32, word_size=4)
        self.local_check(a)

        OPTS.check_lvsdrc = True        
        globals.end_openram()
        

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
