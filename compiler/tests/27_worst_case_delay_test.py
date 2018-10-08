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
import debug

@unittest.skip("SKIPPING 27_worst_case_delay_test")
class worst_case_timing_sram_test(openram_test):

    def runTest(self):
        OPTS.tech_name = "freepdk45"
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False
        OPTS.trim_netlist = False
        OPTS.check_lvsdrc = True
        

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        import characterizer
        reload(characterizer)
        from characterizer import worst_case
        if not OPTS.spice_exe:
            debug.error("Could not find {} simulator.".format(OPTS.spice_name),-1)

        word_size, num_words, num_banks = 32, 32, 1
        from sram import sram
        from sram_config import sram_config
        c = sram_config(word_size=word_size,
                        num_words=num_words,
                        num_banks=num_banks)
        #c.words_per_row=1
        c.compute_sizes()
        debug.info(1, "Testing the timing different bitecells inside a {}bit, {} words SRAM with {} bank".format(
                                                                       word_size, num_words, num_banks))
        s = sram(c, name="sram1")
        
        sp_netlist_file = OPTS.openram_temp + "temp.sp"
        s.sp_write(sp_netlist_file)
        
        if OPTS.use_pex:
            gdsname = OPTS.output_path + s.name + ".gds"
            s.gds_write(gdsname)
            
            import verify
            reload(verify)
            # Output the extracted design if requested
            sp_pex_file = OPTS.output_path + s.name + "_pex.sp"
            verify.run_pex(s.name, gdsname, sp_netlist_file, output=sp_pex_file)
            sp_sim_file = sp_pex_file
        else:
            sp_sim_file = sp_netlist_file
            
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        wc = worst_case(s.s, sp_sim_file, corner)
        import tech
        loads = [tech.spice["msflop_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        wc.analyze(probe_address, probe_data, slews, loads)

        globals.end_openram()

# instantiate a copdsay of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
