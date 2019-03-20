#!/usr/bin/env python3
"""
Run regresion tests on a parameterized bitcell
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug
from sram_factory import factory

#@unittest.skip("SKIPPING 04_pbitcell_test")
class pbitcell_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        factory.reset()
        debug.info(2, "Bitcell with 1 of each port: read/write, write, and read")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=0
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        factory.reset()
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=1
        factory.reset()
        debug.info(2, "Bitcell with 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=0
        factory.reset()
        debug.info(2, "Bitcell with 0 read ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        factory.reset()
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        factory.reset()
        debug.info(2, "Bitcell with 2 of each port: read/write, write, and read")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=0
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        factory.reset()
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=2
        factory.reset()
        debug.info(2, "Bitcell with 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=0
        factory.reset()
        debug.info(2, "Bitcell with 0 read ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        factory.reset()
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        globals.end_openram()



# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
