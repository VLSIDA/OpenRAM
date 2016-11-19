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
                (src_rect,path,dest_rect)=r.route(layer_stack,src="A",dest="B")
                #r.rg.view()
                self.add_rect(layer=layer_stack[0],
                              offset=src_rect[0],
                              width=src_rect[1].x-src_rect[0].x,
                              height=src_rect[1].y-src_rect[0].y)
                self.add_wire(layer_stack,path)
                self.add_rect(layer=layer_stack[0],
                              offset=dest_rect[0],
                              width=dest_rect[1].x-dest_rect[0].x,
                              height=dest_rect[1].y-dest_rect[0].y)
                

        
        r = routing("test1", "AB_same_layer_pins")
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
