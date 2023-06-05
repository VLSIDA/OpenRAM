#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


#@unittest.skip("SKIPPING 04_pbitcell_test")
class pbitcell_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 1 of each port: read/write, write, and read")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=0
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 2 of each port: read/write, write, and read")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=0
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = factory.create(module_type="pbitcell")
        self.local_check(tx)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
