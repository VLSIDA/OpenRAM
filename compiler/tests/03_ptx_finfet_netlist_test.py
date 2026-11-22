#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
FinFET netlists (ASAP7): every transistor is written with an integer
number of fins and the fin-quantized width, from ptx up to a full SRAM.
Runs in netlist-only mode, so no simulator, DRC or LVS tool is needed.
"""
import re
import sys, os
import unittest
from testutils import *

import openram
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


class ptx_finfet_netlist_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config_asap7_netlist".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram.tech import spice
        fin = spice["fin_width"]

        # 0.1um rounds to 4 fins
        fet = factory.create(module_type="ptx", width=0.1, mults=1, tx_type="nmos")
        self.assertEqual(fet.nfin, 4)
        self.assertIn("nfin=4", fet.spice_device)
        self.assertIn("w={:.4f}u".format(4 * fin), fet.spice_device)

        # Narrower than one fin still gets one fin
        fet = factory.create(module_type="ptx", width=0.01, mults=1, tx_type="pmos")
        self.assertEqual(fet.nfin, 1)

        from openram import sram_config
        c = sram_config(word_size=OPTS.word_size, num_words=OPTS.num_words)
        c.recompute_sizes()
        s = factory.create(module_type="sram", sram_config=c)
        tempspice = OPTS.openram_temp + "asap7_sram.sp"
        s.sp_write(tempspice)

        devices = [l for l in open(tempspice) if re.match(r"^M", l, re.I)]
        self.assertTrue(len(devices) > 0)
        for line in devices:
            m = re.search(r"\bnfin=(\d+)", line)
            self.assertIsNotNone(m, "missing nfin: " + line)
            self.assertGreater(int(m.group(1)), 0)

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
