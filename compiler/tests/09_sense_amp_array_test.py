#!/usr/bin/env python2.7
"""
Run a regresion test on a sense amp array
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
import verify

#@unittest.skip("SKIPPING 09_sense_amp_test")


class sense_amp_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = False

        import sense_amp_array


        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=2")
        a = sense_amp_array.sense_amp_array(word_size=4, words_per_row=2)
        self.local_check(a)

        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=4")
        a = sense_amp_array.sense_amp_array(word_size=4, words_per_row=4)
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

        
# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
