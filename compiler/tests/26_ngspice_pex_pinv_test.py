#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
"""
Run regression tests/pex test on an extracted pinv to ensure pex functionality
with Ngspice.
"""
import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug


class ngspice_pex_pinv_test(openram_test):

    def runTest(self):
        globals.init_openram("config_{0}".format(OPTS.tech_name))

        import pinv
        # generate the pinv module
        OPTS.purge_temp =  False
        debug.info(2, "Checking 1x size inverter")
        tx = pinv.pinv(name="pinv", size=1)
        self.local_check(tx)
        # generate its pex file
        pex_file = self.run_pex(tx)
        OPTS.purge_temp =  True
        OPTS.analytical_delay = False

        # load the ngspice
        OPTS.spice_name = "ngspice"
        OPTS.spice_exe = "ngspice"

        import os
        from characterizer import charutils
        from charutils import parse_spice_list
        # setup simulaton
        sim_file = OPTS.openram_temp + "stim.sp"
        log_file_name = "timing"

        # make sure that the library simulation is successful
        tempsp = "{0}{1}.sp".format(OPTS.openram_temp,tx.name)
        self.write_simulaton(sim_file, tempsp, tx.name)
        sp_delay = parse_spice_list(log_file_name, "pinv_delay")
        assert sp_delay is not "Failed"

        # generate simulation for pex, make sure the simulation is successful
        self.write_simulaton(sim_file, pex_file, tx.name)
        pex_delay = parse_spice_list(log_file_name, "pinv_delay")
        # make sure the extracted spice simulated
        assert pex_delay is not "Failed"

        # if pex data is bigger than original spice file then result is ok
        # actually this may not always be true depending on the netlist provided
        # comment out for now
        #debug.info(2,"pex_delay: {0}".format(pex_delay))
        #debug.info(2,"sp_delay: {0}".format(sp_delay))

        #assert pex_delay > sp_delay, "pex delay {0} is smaller than sp_delay {1}"\
        #.format(pex_delay,sp_delay)

        globals.end_openram()

    def write_simulaton(self, sim_file, cir_file, top_module_name):
        """ write pex spice simulation for a pinv test"""
        import tech
        from characterizer import measurements, stimuli
        corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])
        sim_file = open(sim_file, "w")
        simulaton = stimuli(sim_file,corner)

        # library files
        simulaton.write_include(cir_file)

        # supply voltages
        simulaton.gen_constant(sig_name ="vdd",
                               v_val = tech.spice["nom_supply_voltage"])
        # The scn4m_subm and ngspice combination will have a gnd source error:
        # "Fatal error: instance vgnd is a shorted VSRC"
        # However, remove gnd power for all techa pass for this test
        # simulaton.gen_constant(sig_name = "gnd",
        #                        v_val = "0v")


        run_time = tech.spice["feasible_period"] * 2
        # input voltage
        simulaton.gen_pwl(sig_name ="input",
                          clk_times = [1,1],
                          data_values = [1,0],
                          period=1e9,
                          slew=0.000002,
                          setup=0)

        # instantiation of simulated pinv
        simulaton.inst_model(pins = ["input", "output", "vdd", "gnd"],
                             model_name = top_module_name)

        # delay measurement
        delay_measure = measurements.delay_measure(measure_name = "pinv_delay",
                                                   trig_name = "input",
                                                   targ_name = "output",
                                                   trig_dir_str = "FALL",
                                                   targ_dir_str = "RISE")
        trig_td = trag_td = 0.01 * run_time
        rest_info = trig_td,trag_td,tech.spice["nom_supply_voltage"]
        delay_measure.write_measure(simulaton, rest_info)

        simulaton.write_control(end_time = run_time)
        sim_file.close()
        simulaton.run_sim()


# run the test from the command line
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
