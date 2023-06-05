#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
"""
Run regression tests/pex test on an extracted pinv to ensure pex functionality
with HSPICE.
"""
import sys, os
import unittest
from testutils import header, openram_test

import openram
from openram import debug
from openram import OPTS


@unittest.skip("SKIPPING 26_hspice_pex_pinv_test")
class hspice_pex_pinv_test(openram_test):

    def runTest(self):
        config_file = "{}/tests/configs/config".format(os.getenv("OPENRAM_HOME"))
        openram.init_openram(config_file, is_unit_test=True)
        from openram.modules import pinv

        # load the hspice
        OPTS.spice_name="hspice"
        OPTS.analytical_delay = False

        # This is a hack to reload the characterizer __init__ with the spice version
        from importlib import reload
        from openram import characterizer
        reload(characterizer)

        # generate the pinv
        prev_keep_value = OPTS.keep_temp
        # force set purge to false to save the sp file
        OPTS.keep_temp =  True
        debug.info(2, "Checking 1x size inverter")
        tx = pinv.pinv(name="pinv", size=1)
        tempgds = "{}.gds".format(tx.name)
        tx.gds_write("{0}{1}".format(OPTS.openram_temp, tempgds))
        tempsp = "{}.sp".format(tx.name)
        tx.sp_write("{0}{1}".format(OPTS.openram_temp, tempsp))

        # make sure that the library simulation is successful
        sp_delay = self.simulate_delay(test_module=tempsp,
                                       top_level_name=tx.name)
        if sp_delay == "Failed":
            self.fail('Library Spice module did not behave as expected')

        # now generate its pex file
        pex_file = self.run_pex(tx)
        OPTS.keep_temp = prev_keep_value # restore the old keep
        # generate simulation for pex, make sure the simulation is successful
        pex_delay = self.simulate_delay(test_module=pex_file,
                                        top_level_name=tx.name)
        # make sure the extracted spice simulated
        if pex_delay == "Failed":
            self.fail('Pex file did not behave as expected')

        # if pex data is bigger than original spice file then result is ok
        # However this may not always be true depending on the netlist provided
        # comment out for now
        # debug.info(2,"pex_delay: {0}".format(pex_delay))
        # debug.info(2,"sp_delay: {0}".format(sp_delay))

        # assert pex_delay > sp_delay, "pex delay {0} is smaller than sp_delay {1}"\
        # .format(pex_delay,sp_delay)

        openram.end_openram()

    def simulate_delay(self, test_module, top_level_name):
        from charutils import parse_spice_list
        # setup simulation
        sim_file = "stim.sp"
        log_file_name = "timing"
        test_sim = self.write_simulation(sim_file, test_module, top_level_name)
        test_sim.run_sim("stim.sp")
        delay = parse_spice_list(log_file_name, "pinv_delay")
        return delay

    def write_simulation(self, sim_file, cir_file, top_module_name):
        """ write pex spice simulation for a pinv test"""
        from openram import tech
        from openram.characterizer import measurements, stimuli
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sim_file = open(OPTS.openram_temp + sim_file, "w")
        simulation = stimuli(sim_file, corner)

        # library files
        simulation.write_include(cir_file)

        # supply voltages
        simulation.gen_constant(sig_name="vdd",
                                v_val=tech.spice["nom_supply_voltage"])
        simulation.gen_constant(sig_name="gnd",
                                v_val="0v")

        run_time = tech.spice["feasible_period"] * 4
        # input voltage
        clk_period = tech.spice["feasible_period"]
        simulation.gen_pwl(sig_name="input",
                           clk_times=[clk_period, clk_period],
                           data_values=[1, 0],
                           period=clk_period,
                           slew=0.001 * tech.spice["feasible_period"],
                           setup=0)

        # instantiation of simulated pinv
        simulation.inst_model(pins=["input", "output", "vdd", "gnd"],
                              model_name=top_module_name)

        # delay measurement
        delay_measure = measurements.delay_measure(measure_name="pinv_delay",
                                                   trig_name="input",
                                                   targ_name="output",
                                                   trig_dir_str="FALL",
                                                   targ_dir_str="RISE",
                                                   has_port=False)
        trig_td = trag_td = 0.01 * run_time
        rest_info = trig_td, trag_td, tech.spice["nom_supply_voltage"]
        delay_measure.write_measure(simulation, rest_info)

        simulation.write_control(end_time=run_time)
        sim_file.close()
        return simulation


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = openram.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
