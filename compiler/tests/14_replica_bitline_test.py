#!/usr/bin/env python3
"""
Run a test on a replica bitline
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class replica_bitline_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        # check replica bitline in single port
        stages=4
        fanout=4
        rows=13
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = factory.create(module_type="replica_bitline", delay_fanout_list=stages*[fanout], bitcell_loads=rows)
        self.local_check(a)
        
        stages=8
        rows=100
        debug.info(2, "Testing RBL with {0} FO4 stages, {1} rows".format(stages,rows))
        a = factory.create(module_type="replica_bitline", delay_fanout_list=stages*[fanout], bitcell_loads=rows)
        self.local_check(a)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
