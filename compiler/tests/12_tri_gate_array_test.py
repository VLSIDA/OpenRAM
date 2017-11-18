#!/usr/bin/env python2.7
"""
Run a regresion test on a tri_gate_array.
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify


class tri_gate_array_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False

        import tri_gate_array

        debug.info(1, "Testing tri_gate_array for columns=8, word_size=8")
        a = tri_gate_array.tri_gate_array(columns=8, word_size=8)
        self.local_check(a)

        debug.info(1, "Testing tri_gate_array for columns=16, word_size=8")
        a = tri_gate_array.tri_gate_array(columns=16, word_size=8)
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
