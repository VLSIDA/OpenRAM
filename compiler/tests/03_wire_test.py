#!/usr/bin/env python2.7
"Run a regresion test on a basic wire"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 03_wire_test")


class wire_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import wire
        import tech
        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("poly", "contact", "metal1")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)

        min_space = 2 * (tech.drc["minwidth_poly"] +
                         tech.drc["minwidth_metal1"])
        layer_stack = ("metal1", "contact", "poly")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)

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
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)


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
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)

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
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)

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
        OPTS.check_lvsdrc = False
        w = wire.wire(layer_stack, position_list)
        OPTS.check_lvsdrc = True
        self.local_check(w)

        # return it back to it's normal state
        OPTS.check_lvsdrc = True
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
