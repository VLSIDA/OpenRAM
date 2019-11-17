#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys,os
sys.path.append(os.getenv("OPENRAM_HOME"))
import globals
from globals import OPTS
import debug
from sram_factory import factory

#@unittest.skip("SKIPPING 04_pbitcell_test")
class pbitcell_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        globals.init_openram(config_file)

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
    unittest.main(testRunner=debugTestRunner())
