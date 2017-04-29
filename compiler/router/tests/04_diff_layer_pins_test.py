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

OPTS = globals.OPTS

class diff_layer_pins_test(unittest.TestCase):
    """
    Two pin route test with pins on different layers and blockages.
    Pins are smaller than grid size.
    """

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        import design
        import router

        class gdscell(design.design):
            """
            A generic GDS design that we can route on.
            """
            def __init__(self, name):
                #design.design.__init__(self, name)
                debug.info(2, "Create {0} object".format(name))
                self.name = name
                self.gds_file = "{0}/{1}.gds".format(os.path.dirname(os.path.realpath(__file__)),name)
                self.sp_file = "{0}/{1}.sp".format(os.path.dirname(os.path.realpath(__file__)),name)
                design.hierarchy_layout.layout.__init__(self, name)
                design.hierarchy_spice.spice.__init__(self, name)
            
        class routing(design.design):
            """
            A generic GDS design that we can route on.
            """
            def __init__(self, name, gdsname):
                design.design.__init__(self, name)
                debug.info(2, "Create {0} object".format(name))

                cell = gdscell(gdsname)
                self.add_inst(name=gdsname,
                              mod=cell,
                              offset=[0,0])
                self.connect_inst([])
                
                self.gdsname = "{0}/{1}.gds".format(os.path.dirname(os.path.realpath(__file__)),gdsname)
                r=router.router(self.gdsname)
                layer_stack =("metal1","via1","metal2")
                r.route(layer_stack,src="A",dest="B")
                r.add_route(self)

        
        
        r = routing("test1", "04_diff_layer_pins_test")
        self.local_check(r)
        
        # fails if there are any DRC errors on any cells
        globals.end_openram()


    def local_check(self, r):
        tempgds = OPTS.openram_temp + "temp.gds"
        r.gds_write(tempgds)
        self.assertFalse(calibre.run_drc(r.name, tempgds))
        os.remove(tempgds)


                             


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
