#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


class replica_column_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        debug.info(2, "Testing one left replica column for dual port")
        a = factory.create(module_type="replica_column", rows=4, rbl=[1, 0], replica_bit=0)
        self.local_check(a)

        debug.info(2, "Testing one right replica column for dual port")
        a = factory.create(module_type="replica_column", rows=4, rbl=[0, 1], replica_bit=4)
        self.local_check(a)

        debug.info(2, "Testing two (left, right) replica columns for dual port")
        a = factory.create(module_type="replica_column", rows=4, rbl=[1, 1], replica_bit=0)
        self.local_check(a)

        debug.info(2, "Testing two (left, right) replica columns for dual port")
        a = factory.create(module_type="replica_column", rows=4, rbl=[1, 1], replica_bit=5)
        self.local_check(a)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
