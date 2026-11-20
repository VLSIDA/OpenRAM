#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


class capped_replica_bitcell_array_dummies_1rw_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 0
        OPTS.num_w_ports = 0
        openram.setup_bitcell()

        # sky130 tiles cells in mirrored pairs, so it needs an even number of
        # physical columns and rows.
        (cols, rows) = (8, 5) if OPTS.tech_name == "sky130" else (7, 5)
        debug.info(2, "Testing {}x{} capped replica array for 1rw cell with dummy row only".format(cols, rows))
        a = factory.create(module_type="capped_replica_bitcell_array", cols=cols, rows=rows, rbl=[1, 0])
        self.local_check(a)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
