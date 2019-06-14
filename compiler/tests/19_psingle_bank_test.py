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
from sram_factory import factory
import debug

#@unittest.skip("SKIPPING 19_psingle_bank_test")
class psingle_bank_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        from bank import bank
        from sram_config import sram_config
        OPTS.bitcell = "pbitcell"
        
        # testing layout of bank using pbitcell with 1 RW port (a 6T-cell equivalent)
        OPTS.num_rw_ports = 1
        OPTS.num_w_ports = 0
        OPTS.num_r_ports = 0
        c = sram_config(word_size=4,
                        num_words=16)
        
        c.words_per_row=1
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        c.num_words=32
        c.words_per_row=2
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Two way column mux")
        name = "bank2_{0}rw_{1}w_{2}r_single".format(OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        c.num_words=64
        c.words_per_row=4
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Four way column mux")
        name = "bank3_{0}rw_{1}w_{2}r_single".format(OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        factory.reset()
        c.recompute_sizes()
        debug.info(1, "Four way column mux")
        name = "bank4_{0}rw_{1}w_{2}r_single".format(OPTS.num_rw_ports, OPTS.num_w_ports, OPTS.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        
        # testing bank using pbitcell in various port combinations
        # layout for multiple ports does not work yet
        """
        OPTS.netlist_only = True

        c.num_words=16
        c.words_per_row=1
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        OPTS.num_rw_ports = c.num_rw_ports = 0
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 0
        OPTS.num_r_ports = c.num_r_ports = 2

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 0

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 0
        OPTS.num_r_ports = c.num_r_ports = 0

        debug.info(1, "No column mux")
        name = "bank1_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        
        # testing with various column muxes
        OPTS.num_rw_ports = c.num_rw_ports = 2
        OPTS.num_w_ports = c.num_w_ports = 2
        OPTS.num_r_ports = c.num_r_ports = 2
        
        c.num_words=32
        c.words_per_row=2
        debug.info(1, "Two way column mux")
        name = "bank2_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        c.num_words=64
        c.words_per_row=4
        debug.info(1, "Four way column mux")
        name = "bank3_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)

        # Eight way has a short circuit of one column mux select to gnd rail
        c.word_size=2
        c.num_words=128
        c.words_per_row=8
        debug.info(1, "Eight way column mux")
        name = "bank4_{0}rw_{1}w_{2}r_single".format(c.num_rw_ports, c.num_w_ports, c.num_r_ports)
        a = bank(c, name=name)
        self.local_check(a)
        """
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
