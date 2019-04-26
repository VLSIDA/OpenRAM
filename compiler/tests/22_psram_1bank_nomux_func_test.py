#!/usr/bin/env python3
# See LICENSE for licensing information.
#
#Copyright (c) 2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
"""
Run a functioal test on 1 bank SRAM
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

#@unittest.skip("SKIPPING 22_psram_1bank_nomux_func_test")
class psram_1bank_nomux_func_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        OPTS.trim_netlist = False
        OPTS.bitcell = "pbitcell"
        OPTS.replica_bitcell="replica_pbitcell"
        OPTS.num_rw_ports = 1
        OPTS.num_r_ports = 1
        OPTS.num_w_ports = 1
        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import functional, delay
        from sram_config import sram_config
        c = sram_config(word_size=4,
                        num_words=32,
                        num_banks=1)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Functional test for {}rw,{}r,{}w psram with {} bit words, {} words, {} words per row, {} banks".format(OPTS.num_rw_ports,
                                                                                                                              OPTS.num_r_ports,
                                                                                                                              OPTS.num_w_ports,
                                                                                                                              c.word_size,
                                                                                                                              c.num_words,
                                                                                                                              c.words_per_row,
                                                                                                                              c.num_banks))
        s = factory.create(module_type="sram", sram_config=c)
        tempspice = OPTS.openram_temp + "temp.sp"        
        s.sp_write(tempspice)
        
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        f = functional(s.s, tempspice, corner)
        d = delay(s.s, tempspice, corner)
        feasible_period = self.find_feasible_test_period(d, s.s, f.load, f.slew)
        
        f.num_cycles = 10
        (fail, error) = f.run()
        self.assertTrue(fail,error)
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
