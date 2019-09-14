# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This file generates simple spice cards for simulation.  There are
various functions that can be be used to generate stimulus for other
simulations as well.
"""

import tech
import debug
import subprocess
import os
import sys
import numpy as np
from globals import OPTS


class stimuli():
    """ Class for providing stimuli functions """

    def __init__(self, stim_file, corner):
        self.vdd_name = tech.spice["vdd_name"]
        self.gnd_name = tech.spice["gnd_name"]
        self.pmos_name = tech.spice["pmos"]
        self.nmos_name = tech.spice["nmos"]
        self.tx_width = tech.spice["minwidth_tx"]
        self.tx_length = tech.spice["channel"]

        self.sf = stim_file
        
        (self.process, self.voltage, self.temperature) = corner
        self.device_models = tech.spice["fet_models"][self.process]
    
        self.sram_name = "Xsram"
    
    def inst_sram(self, pins, inst_name):
        """ Function to instatiate an SRAM subckt. """

        self.sf.write("{} ".format(self.sram_name))
        for pin in self.sram_pins:
            self.sf.write("{0} ".format(pin))  
        self.sf.write("{0}\n".format(inst_name))
        
    def inst_model(self, pins, model_name):
        """ Function to instantiate a generic model with a set of pins """
        self.sf.write("X{0} ".format(model_name))
        for pin in pins:
            self.sf.write("{0} ".format(pin))
        self.sf.write("{0}\n".format(model_name))


    def create_inverter(self, size=1, beta=2.5):
        """ Generates inverter for the top level signals (only for sim purposes) """
        self.sf.write(".SUBCKT test_inv in out {0} {1}\n".format(self.vdd_name, self.gnd_name))
        self.sf.write("mpinv out in {0} {0} {1} w={2}u l={3}u\n".format(self.vdd_name,
                                                                        self.pmos_name,
                                                                        beta * size * self.tx_width,
                                                                        self.tx_length))
        self.sf.write("mninv out in {0} {0} {1} w={2}u l={3}u\n".format(self.gnd_name,
                                                                        self.nmos_name,
                                                                        size * self.tx_width,
                                                                        self.tx_length))
        self.sf.write(".ENDS test_inv\n")


    def create_buffer(self, buffer_name, size=[1,3], beta=2.5):
        """
            Generates buffer for top level signals (only for sim
            purposes). Size is pair for PMOS, NMOS width multiple. 
            """

        self.sf.write(".SUBCKT test_{2} in out {0} {1}\n".format(self.vdd_name, 
                                                                 self.gnd_name,
                                                                 buffer_name))
        self.sf.write("mpinv1 out_inv in {0} {0} {1} w={2}u l={3}u\n".format(self.vdd_name,
                                                                             self.pmos_name,
                                                                             beta * size[0] * self.tx_width,
                                                                             self.tx_length))
        self.sf.write("mninv1 out_inv in {0} {0} {1} w={2}u l={3}u\n".format(self.gnd_name,
                                                                             self.nmos_name,
                                                                             size[0] * self.tx_width,
                                                                             self.tx_length))
        self.sf.write("mpinv2 out out_inv {0} {0} {1} w={2}u l={3}u\n".format(self.vdd_name,
                                                                              self.pmos_name,
                                                                              beta * size[1] * self.tx_width,
                                                                              self.tx_length))
        self.sf.write("mninv2 out out_inv {0} {0} {1} w={2}u l={3}u\n".format(self.gnd_name,
                                                                              self.nmos_name,
                                                                              size[1] * self.tx_width,
                                                                              self.tx_length))
        self.sf.write(".ENDS test_{0}\n\n".format(buffer_name))


    def inst_buffer(self, buffer_name, signal_list):
        """ Adds buffers to each top level signal that is in signal_list (only for sim purposes) """
        for signal in signal_list:
            self.sf.write("X{0}_buffer {0} {0}_buf {1} {2} test_{3}\n".format(signal,
                                                                              "test"+self.vdd_name,
                                                                              "test"+self.gnd_name,
                                                                              buffer_name))


    def inst_inverter(self, signal_list):
        """ Adds inv for each signal that needs its inverted version (only for sim purposes) """
        for signal in signal_list:
            self.sf.write("X{0}_inv {0} {0}_inv {1} {2} test_inv\n".format(signal,
                                                                           "test"+self.vdd_name,
                                                                           "test"+self.gnd_name))


    def gen_pulse(self, sig_name, v1, v2, offset, period, t_rise, t_fall):
        """ 
            Generates a periodic signal with 50% duty cycle and slew rates. Period is measured
            from 50% to 50%.
        """
        self.sf.write("* PULSE: period={0}\n".format(period))
        pulse_string="V{0} {0} 0 PULSE ({1} {2} {3}n {4}n {5}n {6}n {7}n)\n"
        self.sf.write(pulse_string.format(sig_name, 
                                          v1,
                                          v2,
                                          offset,
                                          t_rise,
                                          t_fall, 
                                          0.5*period-0.5*t_rise-0.5*t_fall,
                                          period))


    def gen_pwl(self, sig_name, clk_times, data_values, period, slew, setup):
        """ 
            Generate a PWL stimulus given a signal name and data values at each period.
            Automatically creates slews and ensures each data occurs a setup before the clock
            edge. The first clk_time should be 0 and is the initial time that corresponds
            to the initial value.
        """
        # the initial value is not a clock time
        debug.check(len(clk_times)==len(data_values),"Clock and data value lengths don't match. {0} clock values, {1} data values for {2}".format(len(clk_times), len(data_values), sig_name))
    
        # shift signal times earlier for setup time
        times = np.array(clk_times) - setup*period
        values = np.array(data_values) * self.voltage
        half_slew = 0.5 * slew
        self.sf.write("* (time, data): {}\n".format(list(zip(clk_times, data_values))))
        self.sf.write("V{0} {0} 0 PWL (0n {1}v ".format(sig_name, values[0]))
        for i in range(1,len(times)):
            self.sf.write("{0}n {1}v {2}n {3}v ".format(times[i]-half_slew,
                                                        values[i-1],
                                                        times[i]+half_slew,
                                                        values[i]))
        self.sf.write(")\n")

    def gen_constant(self, sig_name, v_val):
        """ Generates a constant signal with reference voltage and the voltage value """
        self.sf.write("V{0} {0} 0 DC {1}\n".format(sig_name, v_val))

    def get_inverse_voltage(self, value):
        if value > 0.5*self.voltage:
            return 0
        elif value <= 0.5*self.voltage:
            return self.voltage
        else:
            debug.error("Invalid value to get an inverse of: {0}".format(value))

    def get_inverse_value(self, value):
        if value > 0.5:
            return 0
        elif value <= 0.5:
            return 1
        else:
            debug.error("Invalid value to get an inverse of: {0}".format(value))
        

    def gen_meas_delay(self, meas_name, trig_name, targ_name, trig_val, targ_val, trig_dir, targ_dir, trig_td, targ_td):
        """ Creates the .meas statement for the measurement of delay """
        measure_string=".meas tran {0} TRIG v({1}) VAL={2} {3}=1 TD={4}n TARG v({5}) VAL={6} {7}=1 TD={8}n\n\n"
        self.sf.write(measure_string.format(meas_name,
                                            trig_name,
                                            trig_val,
                                            trig_dir,
                                            trig_td,
                                            targ_name,
                                            targ_val,
                                            targ_dir,
                                            targ_td))
    
    def gen_meas_find_voltage(self, meas_name, trig_name, targ_name, trig_val, trig_dir, trig_td):
        """ Creates the .meas statement for the measurement of delay """
        measure_string=".meas tran {0} FIND v({1}) WHEN v({2})={3}v {4}=1 TD={5}n \n\n"
        self.sf.write(measure_string.format(meas_name,
                                            targ_name,
                                            trig_name,
                                            trig_val,
                                            trig_dir,
                                            trig_td))
    
    def gen_meas_find_voltage_at_time(self, meas_name, targ_name, time_at):
        """ Creates the .meas statement for voltage at time"""
        measure_string=".meas tran {0} FIND v({1}) AT={2}n \n\n"
        self.sf.write(measure_string.format(meas_name,
                                            targ_name,
                                            time_at))

    def gen_meas_power(self, meas_name, t_initial, t_final):
        """ Creates the .meas statement for the measurement of avg power """
        # power mea cmd is different in different spice:
        if OPTS.spice_name == "hspice":
            power_exp = "power"
        else:
            power_exp = "par('(-1*v(" + str(self.vdd_name) + ")*I(v" + str(self.vdd_name) + "))')"
        self.sf.write(".meas tran {0} avg {1} from={2}n to={3}n\n\n".format(meas_name,
                                                                            power_exp,
                                                                            t_initial,
                                                                            t_final))
                                                                            
    def gen_meas_value(self, meas_name, dout, t_intital, t_final):
        measure_string=".meas tran {0} AVG v({1}) FROM={2}n TO={3}n\n\n".format(meas_name, dout, t_intital, t_final)
        self.sf.write(measure_string)
    
    def write_control(self, end_time, runlvl=4):
        """ Write the control cards to run and end the simulation """
        
        # These are guesses... 
        if runlvl==1:
            reltol = 0.02 # 2%
        elif runlvl==2:
            reltol = 0.01 # 1%
        elif runlvl==3:
            reltol = 0.005 # 0.5%
        else:
            reltol = 0.001 # 0.1%
        timestep = 10 #ps, was 5ps but ngspice was complaining the timestep was too small in certain tests.
           
        # UIC is needed for ngspice to converge
        self.sf.write(".TRAN {0}p {1}n UIC\n".format(timestep,end_time))
        self.sf.write(".TEMP {}\n".format(self.temperature))
        if OPTS.spice_name == "ngspice":
            # ngspice sometimes has convergence problems if not using gear method
            # which is more accurate, but slower than the default trapezoid method
            # Do not remove this or it may not converge due to some "pa_00" nodes
            # unless you figure out what these are.
            self.sf.write(".OPTIONS POST=1 RELTOL={0} PROBE method=gear\n".format(reltol))
        else:
            self.sf.write(".OPTIONS POST=1 RUNLVL={0} PROBE\n".format(runlvl))

        # create plots for all signals
        self.sf.write("* probe is used for hspice/xa, while plot is used in ngspice\n")
        if OPTS.debug_level>0:
            if OPTS.spice_name in ["hspice","xa"]:
                self.sf.write(".probe V(*)\n")
            else:
                self.sf.write(".plot V(*)\n")
        else:
            self.sf.write("*.probe V(*)\n")
            self.sf.write("*.plot V(*)\n")

        # end the stimulus file
        self.sf.write(".end\n\n")


    def write_include(self, circuit):
        """Writes include statements, inputs are lists of model files"""
        includes = self.device_models + [circuit]
        self.sf.write("* {} process corner\n".format(self.process))
        for item in list(includes):
            if os.path.isfile(item):
                self.sf.write(".include \"{0}\"\n".format(item))
            else:
                debug.error("Could not find spice model: {0}\nSet SPICE_MODEL_DIR to over-ride path.\n".format(item))


    def write_supply(self):
        """ Writes supply voltage statements """
        gnd_node_name = "0"
        self.sf.write("V{0} {0} {1} {2}\n".format(self.vdd_name, gnd_node_name, self.voltage))
        # This is for the test power supply
        self.sf.write("V{0} {0} {1} {2}\n".format("test"+self.vdd_name, gnd_node_name, self.voltage))
        self.sf.write("V{0} {0} {1} {2}\n".format("test"+self.gnd_name, gnd_node_name, 0.0))

        #Adding a commented out supply for simulators where gnd and 0 are not global grounds.
        self.sf.write("\n*Nodes gnd and 0 are the same global ground node in ngspice/hspice/xa. Otherwise, this source may be needed.\n")
        self.sf.write("*V{0} {0} {1} {2}\n".format(self.gnd_name, gnd_node_name, 0.0))

    def run_sim(self):
        """ Run hspice in batch mode and output rawfile to parse. """
        temp_stim = "{0}stim.sp".format(OPTS.openram_temp)
        import datetime
        start_time = datetime.datetime.now()
        debug.check(OPTS.spice_exe!="","No spice simulator has been found.")
    
        if OPTS.spice_name == "xa":
            # Output the xa configurations here. FIXME: Move this to write it once.
            xa_cfg = open("{}xa.cfg".format(OPTS.openram_temp), "w")
            xa_cfg.write("set_sim_level -level 7\n")
            xa_cfg.write("set_powernet_level 7 -node vdd\n")
            xa_cfg.close()
            cmd = "{0} {1} -c {2}xa.cfg -o {2}xa -mt 2".format(OPTS.spice_exe,
                                                               temp_stim,
                                                               OPTS.openram_temp)
            valid_retcode=0
        elif OPTS.spice_name == "hspice":
            # TODO: Should make multithreading parameter a configuration option
            cmd = "{0} -mt 2 -i {1} -o {2}timing".format(OPTS.spice_exe,
                                                         temp_stim,
                                                         OPTS.openram_temp)
            valid_retcode=0
        else:
            # ngspice 27+ supports threading with "set num_threads=4" in the stimulus file or a .spiceinit 
            cmd = "{0} -b -o {2}timing.lis {1}".format(OPTS.spice_exe,
                                                       temp_stim,
                                                       OPTS.openram_temp)
            # for some reason, ngspice-25 returns 1 when it only has acceptable warnings
            valid_retcode=1

        
        spice_stdout = open("{0}spice_stdout.log".format(OPTS.openram_temp), 'w')
        spice_stderr = open("{0}spice_stderr.log".format(OPTS.openram_temp), 'w')
        
        debug.info(3, cmd)
        retcode = subprocess.call(cmd, stdout=spice_stdout, stderr=spice_stderr, shell=True)

        spice_stdout.close()
        spice_stderr.close()
        
        if (retcode > valid_retcode):
            debug.error("Spice simulation error: " + cmd, -1)
        else:
            end_time = datetime.datetime.now()
            delta_time = round((end_time-start_time).total_seconds(),1)
            debug.info(2,"*** Spice: {} seconds".format(delta_time))

    
