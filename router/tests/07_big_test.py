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

class big_test(unittest.TestCase):
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
                layer_stack =("metal3","via2","metal2")
                connections=[('out_0_2', 'a_0_0'),
                             ('out_0_3', 'b_0_0'),
                             ('out_0_0', 'a_0_1'),
                             ('out_1_2', 'a_1_0'),
                             ('out_1_3', 'b_1_0'),
                             ('out_1_0', 'a_1_1'),
                             ('out_2_1', 'a_2_0'),
                             ('out_2_2', 'b_2_0'),
                             ('out_3_1', 'a_3_0'),
                             ('out_3_2', 'b_3_0'),
                             ('out_4_6', 'a_4_0'),
                             ('out_4_7', 'b_4_0'),
                             ('out_4_8', 'a_4_2'),
                             ('out_4_9', 'b_4_2'),
                             ('out_4_10', 'a_4_4'),
                             ('out_4_11', 'b_4_4'),
                             ('out_4_0', 'a_4_1'),
                             ('out_4_2', 'b_4_1'),
                             ('out_4_4', 'a_4_5'),
                             ('out_4_1', 'a_4_3'),
                             ('out_4_5', 'b_4_3')]
                for (src,tgt) in connections:
                    self.assertTrue(r.route(self,layer_stack,src=src,dest=tgt))

        # This test only runs on scn3me_subm tech
        if OPTS.tech_name=="scn3me_subm":
            r = routing("07_big_test_{0}".format(OPTS.tech_name))
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
