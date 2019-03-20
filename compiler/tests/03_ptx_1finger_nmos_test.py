#!/usr/bin/env python3
"Run a regression test on a basic parameterized transistors"

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class ptx_1finger_nmos_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        import tech

        debug.info(2, "Checking min size NMOS with 1 finger")
        fet = factory.create(module_type="ptx",
                             width=tech.drc["minwidth_tx"],
                             mults=1,
                             tx_type="nmos")
        self.local_drc_check(fet)

        globals.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
