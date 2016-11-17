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

class no_blockages_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))        
        
        import router
        import wire
        import tech
        #r=router.router("A_to_B_no_blockages.gds")
        #r=router.router("A_to_B_m1m2_blockages.gds")
        #r=router.router("A_to_B_m1m2_same_layer_pins.gds")
        r=router.router("A_to_B_m1m2_diff_layer_pins.gds")
        layer_stack =("metal1","via1","metal2")
        path=r.route(layer_stack,src="A",dest="B")

        # For debug, to view the result as an image
        r.rg.set_path(path)
        r.rg.view()
        OPTS.check_lvsdrc = False

        #w = wire.wire(layer_stack, path)
        OPTS.check_lvsdrc = True
        #self.local_check(w)

        #drc_errors = calibre.run_drc(name, gds_name)
        drc_errors = 1
        
        # fails if there are any DRC errors on any cells
        self.assertEqual(drc_errors, 0)
        globals.end_openram()




    def local_check(self, w):
        tempgds = OPTS.openram_temp + "temp.gds"
        w.gds_write(tempgds)
        self.assertFalse(calibre.run_drc(w.name, tempgds))
        os.remove(tempgds)


                             


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
