#!/usr/bin/env python3
"""
Run a regression test on various srams
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
from sram_factory import factory
import debug

class timing_sram_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        
        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import delay
        from sram_config import sram_config
        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1)
        c.words_per_row=1
        # c = sram_config(word_size=32,
                        # num_words=256,
                        # num_banks=1)
        # c.words_per_row=2
        #OPTS.use_tech_delay_chain_size = True
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)
        
        #Exclude things known not to be in critical path.
        #Intended for characterizing read paths. Somewhat hacky implementation
        # s.s.bank.bitcell_array.graph_exclude_bits(15,0)
        # s.s.bank.graph_exclude_precharge()
        # s.s.graph_exclude_addr_dff()
        # s.s.graph_exclude_data_dff()
        # s.s.graph_exclude_ctrl_dffs()
        
        # debug.info(1,'pins={}'.format(s.s.pins))
        # import graph_util
        # graph = graph_util.timing_graph()
        # pins=['DIN0[0]', 'ADDR0[0]', 'ADDR0[1]', 'ADDR0[2]', 'ADDR0[3]', 'csb0', 'web0', 'clk0', 'DOUT0[0]', 'vdd', 'gnd']
        # s.s.build_graph(graph,"Xsram",pins)
        # #debug.info(1,"{}".format(graph))
        # graph.print_all_paths('clk0', 'DOUT0[0]')
        # import sys
        # sys.exit(1)

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        debug.info(1, "Probe address {0} probe data bit {1}".format(probe_address, probe_data))

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        d = delay(s.s, tempspice, corner)
        import tech
        loads = [tech.spice["msflop_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        data, port_data = d.analyze(probe_address, probe_data, slews, loads)
        #Combine info about port into all data
        data.update(port_data[0])
     
        if OPTS.tech_name == "freepdk45":
            golden_data = {'delay_hl': [0.2121267],
                         'delay_lh': [0.2121267],
                         'leakage_power': 0.0023761999999999998,
                         'min_period': 0.43,
                         'read0_power': [0.5139368],
                         'read1_power': [0.48940979999999995],
                         'slew_hl': [0.0516745],
                         'slew_lh': [0.0516745],
                         'write0_power': [0.46267169999999996],
                         'write1_power': [0.4670826]}
        elif OPTS.tech_name == "scn4m_subm":
            golden_data = {'delay_hl': [1.288],
                         'delay_lh': [1.288],
                         'leakage_power': 0.0273896,
                         'min_period': 2.578,
                         'read0_power': [16.9996],
                         'read1_power': [16.2616],
                         'slew_hl': [0.47891700000000004],
                         'slew_lh': [0.47891700000000004],
                         'write0_power': [16.0656],
                         'write1_power': [16.2616]}

        else:
            self.assertTrue(False) # other techs fail
        # Check if no too many or too few results
        self.assertTrue(len(data.keys())==len(golden_data.keys()))

        self.assertTrue(self.check_golden_data(data,golden_data,0.25))
        
        globals.end_openram()
        
# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
