#!/usr/bin/env python3
"Run a regresion test the library cells for DRC"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug

OPTS = globals.OPTS

class no_blockages_test(openram_test):
    """
    Simplest two pin route test with no blockages.
    """

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        from supply_router import supply_router as router

        if True:
            from control_logic import control_logic
            cell = control_logic(16)
        else:
            from sram import sram
            from sram_config import sram_config
            c = sram_config(word_size=4,
                            num_words=16,
                            num_banks=1)
            
            c.words_per_row=1
            cell = sram(c, "sram1")
                
        layer_stack =("metal3","via3","metal4")
        rtr=router(layer_stack, cell)
        self.assertTrue(rtr.route())
        self.local_check(cell,True)
        
        # fails if there are any DRC errors on any cells
        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
