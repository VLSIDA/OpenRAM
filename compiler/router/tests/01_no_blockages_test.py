#!/usr/bin/env python2.7
"Run a regresion test the library cells for DRC"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],"../.."))
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre
import vector

class no_blockages_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))        
        
        import router
        #r=router.router("A_to_B_no_blockages.gds")
        r=router.router("A_to_B_m1m2_blockages.gds")

        r.set_layers(("metal1","via1","metal2"))

        r.create_routing_grid()
        r.set_source("A")
        r.set_target("B")
        r.find_blockages()
        r.route()
        r.rg.view()
            
        #drc_errors = calibre.run_drc(name, gds_name)
        drc_errors = 1
        
        # fails if there are any DRC errors on any cells
        self.assertEqual(drc_errors, 0)
        globals.end_openram()






                             


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
