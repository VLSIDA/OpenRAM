#!/usr/bin/env python2.7
"Run a regresion test on a basic path"

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 03_path_test")


class path_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.check_lvsdrc = False

        import path
        import tech
        import design

        min_space = 2 * tech.drc["minwidth_metal1"]
        layer_stack = ("metal1")
        # checks if we can retrace a path
        position_list = [[0,0],
                         [0, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [4 * min_space, 3 * min_space ],
                         [0, 3 * min_space ],
                         [0, 6 * min_space ]]
        w = design.design("path_test0")
        path.path(w,layer_stack, position_list)
        self.local_check(w)


        min_space = 2 * tech.drc["minwidth_metal1"]
        layer_stack = ("metal1")
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
        w = design.design("path_test1")
        path.path(w,layer_stack, position_list)
        self.local_check(w)

        min_space = 2 * tech.drc["minwidth_metal2"]
        layer_stack = ("metal2")
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
        w = design.design("path_test2")
        path.path(w, layer_stack, position_list)
        self.local_check(w)

        min_space = 2 * tech.drc["minwidth_metal3"]
        layer_stack = ("metal3")
        position_list = [[0, 0],
                         [0, 3 * min_space],
                         [1 * min_space, 3 * min_space],
                         [4 * min_space, 3 * min_space],
                         [4 * min_space, 0],
                         [7 * min_space, 0],
                         [7 * min_space, 4 * min_space],
                         [-1 * min_space, 4 * min_space],
                         [-1 * min_space, 0]]
        # run on the reverse list
        position_list.reverse()
        w = design.design("path_test3")
        path.path(w, layer_stack, position_list)
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
