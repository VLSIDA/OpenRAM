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


class ptx_no_contacts_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram import tech

        debug.info(2, "Checking single finger no source/drain")
        fet = factory.create(module_type="ptx",
                             width=tech.drc["minwidth_tx"],
                             mults=1,
                             add_source_contact=False,
                             add_drain_contact=False,
                             tx_type="nmos")
        self.local_drc_check(fet)

        debug.info(2, "Checking multifinger no source/drain")
        fet = factory.create(module_type="ptx",
                             width=tech.drc["minwidth_tx"],
                             mults=4,
                             add_source_contact=False,
                             add_drain_contact=False,
                             tx_type="nmos")
        self.local_drc_check(fet)

        debug.info(2, "Checking series ptx")
        fet = factory.create(module_type="ptx",
                             width=tech.drc["minwidth_tx"],
                             mults=4,
                             series_devices=True,
                             tx_type="nmos")
        self.local_drc_check(fet)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
