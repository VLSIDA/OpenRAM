#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import unittest
from testutils import *
import sys, os

import openram
from openram import OPTS
from openram.sram_factory import factory
from openram import debug


class rom_bank_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        debug.info(1, "Testing rom cell")
        test_data = "{0}/{1}/rom_data_64B".format(os.getenv("OPENRAM_HOME"), OPTS.rom_data_dir)

        from openram import rom_config

        conf = rom_config(strap_spacing = 8,
                          rom_data = test_data,
                          word_size = 1)

        a = factory.create(module_type="rom_bank", rom_config=conf)
        a.sp_write(OPTS.openram_temp + 'simulation_file.sp')
        self.local_check(a)

        openram.end_openram()

# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
