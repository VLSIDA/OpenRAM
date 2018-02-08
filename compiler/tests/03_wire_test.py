#!/usr/bin/env python2.7
"Run a regresion test on a basic wire"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class wire_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        global verify
        import verify
        OPTS.check_lvsdrc = False

        import wire
        import tech
        import design
        
        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("poly", "contact", "metal1")
        old_position_list = [[0, 0],
                             [0, 3 * min_space],
                             [1 * min_space, 3 * min_space],
                             [4 * min_space, 3 * min_space],
                             [4 * min_space, 0],
                             [7 * min_space, 0],
                             [7 * min_space, 4 * min_space],
                             [-1 * min_space, 4 * min_space],
                             [-1 * min_space, 0]]
        position_list  = [[x-min_space, y-min_space] for x,y in old_position_list]        
        w = design.design("wire_test1")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal1", "contact", "poly")
        old_position_list = [[0, 0],
                             [0, 3 * min_space],
                             [1 * min_space, 3 * min_space],
                             [4 * min_space, 3 * min_space],
                             [4 * min_space, 0],
                             [7 * min_space, 0],
                             [7 * min_space, 4 * min_space],
                             [-1 * min_space, 4 * min_space],
                             [-1 * min_space, 0]]
        position_list  = [[x+min_space, y+min_space] for x,y in old_position_list]
        w = design.design("wire_test2")        
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal1", "via1", "metal2")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        w = design.design("wire_test3")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)


        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal2", "via1", "metal1")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        w = design.design("wire_test4")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal3"])
        layer_stack = ("metal2", "via2", "metal3")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        position_list.reverse()
        w = design.design("wire_test5")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        min_space = 2 * (tech.drc["minwidth_metal2"] +
                         tech.drc["minwidth_metal3"])
        layer_stack = ("metal3", "via2", "metal2")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        position_list.reverse()
        w = design.design("wire_test6")
        wire.wire(w, layer_stack, position_list)
        self.local_drc_check(w)

        # return it back to it's normal state
        OPTS.check_lvsdrc = True
        globals.end_openram()
        

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
