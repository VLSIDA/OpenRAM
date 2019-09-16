# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
#!/usr/bin/env python3
"Run a regresion test the library cells for DRC"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],"../.."))
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug

OPTS = globals.OPTS

class big_test(openram_test):
    """
    Simplest two pin route test with no blockages using the pin locations instead of labels.
    """

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        from gds_cell import gds_cell
        from design import design
        from signal_router import signal_router as router

        class routing(design, openram_test):
            """
            A generic GDS design that we can route on.
            """
            def __init__(self, name):
                design.__init__(self, "top")

                # Instantiate a GDS cell with the design
                gds_file = "{0}/{1}.gds".format(os.path.dirname(os.path.realpath(__file__)),name)
                cell = gds_cell(name, gds_file)
                self.add_inst(name=name,
                              mod=cell,
                              offset=[0,0])
                self.connect_inst([])
                
                layer_stack =("metal1","via1","metal2")
                r=router(layer_stack,self,gds_file)
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
                    self.assertTrue(r.route(src=src,dest=tgt))

        # This test only runs on scn3me_subm tech
        if OPTS.tech_name=="scn3me_subm":
            r = routing("07_big_test_{0}".format(OPTS.tech_name))
            self.local_drc_check(r)
        else:
            debug.warning("This test does not support technology {0}".format(OPTS.tech_name))
                
        # fails if there are any DRC errors on any cells
        globals.end_openram()
                             


# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
