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

class pin_location_test(unittest.TestCase):
    """
    Simplest two pin route test with no blockages using the pin locations instead of labels.
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
            
        class routing(design.design,unittest.TestCase):
            """
            A generic GDS design that we can route on.
            """
            def __init__(self, name):
                design.design.__init__(self, name)
                debug.info(2, "Create {0} object".format(name))

                cell = gdscell(name)
                self.add_inst(name=name,
                              mod=cell,
                              offset=[0,0])
                self.connect_inst([])
                
                self.gdsname = "{0}/{1}.gds".format(os.path.dirname(os.path.realpath(__file__)),name)
                r=router.router(self.gdsname)
                layer_stack =("metal1","via1","metal2")
                # these are user coordinates and layers
                src_pin = [[0.52, 4.099],11]
                tgt_pin = [[3.533, 1.087],11]
                #r.route(layer_stack,src="A",dest="B")
                self.assertTrue(r.route(self,layer_stack,src=src_pin,dest=tgt_pin))

        # This only works for freepdk45 since the coordinates are hard coded
        if OPTS.tech_name == "freepdk45":
            r = routing("06_pin_location_test_{0}".format(OPTS.tech_name))
            self.local_check(r)
        else:
            debug.warning("This test does not support technology {0}".format(OPTS.tech_name))
        
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
