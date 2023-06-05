#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys, os
from testutils import *

import openram
from openram import OPTS
from openram.sram_factory import factory
from openram import debug


class column_mux_pbitcell_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)

        # check single level column mux array in multi-port
        OPTS.bitcell = "pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1

        debug.info(1, "Testing sample for 2-way column_mux_array in multi-port")
        a = factory.create(module_type="column_mux_array", columns=16, word_size=8, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 4-way column_mux_array  in multi-port")
        a = factory.create(module_type="column_mux_array", columns=16, word_size=4, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 8-way column_mux_array  in multi-port (innermost connections)")
        a = factory.create(module_type="column_mux_array", columns=32, word_size=4, bitcell_bl="bl0", bitcell_br="br0")
        self.local_check(a)

        debug.info(1, "Testing sample for 8-way column_mux_array  in multi-port (outermost connections)")
        a = factory.create(module_type="column_mux_array", columns=32, word_size=4, bitcell_bl="bl2", bitcell_br="br2", column_offset=3)
        self.local_check(a)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
