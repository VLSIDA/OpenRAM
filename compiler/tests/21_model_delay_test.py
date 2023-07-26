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


# @unittest.skip("SKIPPING 21_model_delay_test")
class model_delay_test(openram_test):
    """ Compare the accuracy of the analytical model with a spice simulation. """

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        OPTS.analytical_delay = False
        OPTS.netlist_only = True
        OPTS.spice_name = "Xyce"
        OPTS.num_sim_threads = 8

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)
        from openram.characterizer import delay
        from openram.characterizer import elmore
        from openram import sram
        from openram import sram_config
        if OPTS.tech_name == "sky130":
            num_spare_rows = 1
            num_spare_cols = 1
        else:
            num_spare_rows = 0
            num_spare_cols = 0

        c = sram_config(word_size=1,
                        num_words=16,
                        num_banks=1,
                        num_spare_cols=num_spare_cols,
                        num_spare_rows=num_spare_rows)
        c.words_per_row=1
        c.recompute_sizes()
        debug.info(1, "Testing timing for sample 1bit, 16words SRAM with 1 bank")
        s = factory.create(module_type="sram", sram_config=c)

        tempspice = OPTS.openram_temp + "temp.sp"
        s.sp_write(tempspice)

        probe_address = "1" * s.s.addr_size
        probe_data = s.s.word_size - 1
        debug.info(1, "Probe address {0} probe data bit {1}".format(probe_address, probe_data))

        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])

        d = delay(s.s, tempspice, corner)
        m = elmore(s.s, tempspice, corner)
        from openram import tech
        loads = [tech.spice["dff_in_cap"]*4]
        slews = [tech.spice["rise_time"]*2]
        load_slews = []
        for slew in slews:
            for load in loads:
                load_slews.append((load, slew))

        # Run a spice characterization
        spice_data, port_data = d.analyze(probe_address, probe_data, load_slews)
        spice_data.update(port_data[0])

        # Run analytical characterization
        model_data, port_data = m.get_lib_values(load_slews)
        model_data.update(port_data[0])

        # Only compare the delays
        spice_delays = {key:value for key, value in spice_data.items() if 'delay' in key}
        spice_delays['min_period'] = spice_data['min_period']
        model_delays = {key:value for key, value in model_data.items() if 'delay' in key}
        model_delays['min_period'] = model_data['min_period']
        debug.info(1,"Spice Delays={}".format(spice_delays))
        debug.info(1,"Model Delays={}".format(model_delays))

        if OPTS.tech_name == "freepdk45":
            error_tolerance = 0.30
        elif OPTS.tech_name == "scn4m_subm":
            error_tolerance = 0.30
        else:
            self.assertTrue(False) # other techs fail

        debug.info(3, 'spice_delays {}'.format(spice_delays))
        debug.info(3, 'model_delays {}'.format(model_delays))

        # Check if no too many or too few results
        self.assertTrue(len(spice_delays.keys())==len(model_delays.keys()))

        self.assertTrue(self.check_golden_data(spice_delays,model_delays,error_tolerance))

        openram.end_openram()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main(testRunner=debugTestRunner())
