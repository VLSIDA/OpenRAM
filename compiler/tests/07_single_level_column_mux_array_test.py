#!/usr/bin/env python2.7
"""
Run a regresion test on a single transistor column_mux.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify


class single_level_column_mux_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
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
        
    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(verify.run_drc(a.name, tempgds))
        self.assertFalse(verify.run_lvs(a.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)

        # reset the static duplicate name checker for unit tests
        import design
        design.design.name_map=[]

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
