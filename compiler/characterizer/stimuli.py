# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
"""
This file generates simple spice cards for simulation.  There are
various functions that can be be used to generate stimulus for other
simulations as well.
"""

import os
import subprocess
import numpy as np
from openram import debug
from openram import tech
from openram import OPTS


class stimuli():
    """ Class for providing stimuli functions """

    def __init__(self, stim_file, meas_file, corner):
        self.vdd_name = "vdd"
        self.gnd_name = "gnd"
        self.pmos_name = tech.spice["pmos"]
        self.nmos_name = tech.spice["nmos"]
        self.tx_width = tech.drc["minwidth_tx"]
        self.tx_length = tech.drc["minlength_channel"]

        self.sf = stim_file
        self.mf = meas_file

        (self.process, self.voltage, self.temperature) = corner
        found = False
        self.device_libraries = []
        self.device_models = []
        try:
            self.device_libraries += tech.spice["fet_libraries"][self.process]
            found = True
        except KeyError:
            pass
        try:
            self.device_models += tech.spice["fet_models"][self.process]
            found = True
        except KeyError:
            pass
        if not found:
            debug.error("Must define either fet_libraries or fet_models.", -1)

    def inst_model(self, pins, model_name):
        """ Function to instantiate a generic model with a set of pins """

        if OPTS.use_pex and OPTS.pex_exe[0] != "calibre":
            self.inst_pex_model(pins, model_name)
        else:
            self.sf.write("X{0} ".format(model_name))
            for pin in pins:
                self.sf.write("{0} ".format(pin))
            self.sf.write("{0}\n".format(model_name))

    def inst_pex_model(self, pins, model_name):
        self.sf.write("X{0} ".format(model_name))
        for pin in pins:
            self.sf.write("{0} ".format(pin))
        for bank in range(OPTS.num_banks):
            row = int(OPTS.num_words / OPTS.words_per_row) - 1
            col = int(OPTS.word_size * OPTS.words_per_row) - 1
            self.sf.write("bitcell_Q_b{0}_r{1}_c{2} ".format(bank, row, col))
            self.sf.write("bitcell_Q_bar_b{0}_r{1}_c{2} ".format(bank, row, col))
        #    can't add all bitcells to top level due to ngspice max port count of 1005
        #    for row in range(int(OPTS.num_words / OPTS.words_per_row)):
        #        for col in range(int(OPTS.word_size * OPTS.words_per_row)):
        #            self.sf.write("bitcell_Q_b{0}_r{1}_c{2} ".format(bank,row,col))
        #            self.sf.write("bitcell_Q_bar_b{0}_r{1}_c{2} ".format(bank,row,col))
        for bank in range(OPTS.num_banks):
            for col in range(OPTS.word_size * OPTS.words_per_row):
                for port in range(OPTS.num_r_ports + OPTS.num_w_ports + OPTS.num_rw_ports):
                    self.sf.write("bl{0}_{1} ".format(port, col))
                    self.sf.write("br{0}_{1} ".format(port, col))

            self.sf.write("s_en{0} ".format(bank))
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

    def create_buffer(self, buffer_name, size=[1, 3], beta=2.5):
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
                                          0.5 * period - 0.5 * t_rise - 0.5 * t_fall,
                                          period))

    def gen_pwl(self, sig_name, clk_times, data_values, period, slew, setup):
        """
            Generate a PWL stimulus given a signal name and data values at each period.
            Automatically creates slews and ensures each data occurs a setup before the clock
            edge. The first clk_time should be 0 and is the initial time that corresponds
            to the initial value.
        """

        str = "Clock and data value lengths don't match. {0} clock values, {1} data values for {2}"
        debug.check(len(clk_times)==len(data_values),
                    str.format(len(clk_times),
                               len(data_values),
                               sig_name))

        # shift signal times earlier for setup time
        times = np.array(clk_times) - setup * period
        values = np.array(data_values) * self.voltage
        half_slew = 0.5 * slew
        self.sf.write("* (time, data): {}\n".format(list(zip(clk_times, data_values))))
        self.sf.write("V{0} {0} 0 PWL (0n {1}v ".format(sig_name, values[0]))
        for i in range(1, len(times)):
            self.sf.write("{0}n {1}v {2}n {3}v ".format(times[i] - half_slew,
                                                        values[i - 1],
                                                        times[i] + half_slew,
                                                        values[i]))
        self.sf.write(")\n")

    def gen_constant(self, sig_name, v_val):
        """ Generates a constant signal with reference voltage and the voltage value """
        self.sf.write("V{0} {0} 0 DC {1}\n".format(sig_name, v_val))

    def get_voltage(self, value):
        if value == "0" or value == 0:
            return 0
        elif value == "1" or value == 1:
            return self.voltage
        else:
            debug.error("Invalid value to get a voltage of: {0}".format(value))

    def gen_meas_delay(self, meas_name, trig_name, targ_name, trig_val, targ_val, trig_dir, targ_dir, trig_td, targ_td):
        """ Creates the .meas statement for the measurement of delay """
        measure_string=".meas tran {0} TRIG v({1}) VAL={2} {3}=1 TD={4}n TARG v({5}) VAL={6} {7}=1 TD={8}n\n\n"
        self.mf.write(measure_string.format(meas_name.lower(),
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
        self.mf.write(measure_string.format(meas_name.lower(),
                                            targ_name,
                                            trig_name,
                                            trig_val,
                                            trig_dir,
                                            trig_td))

    def gen_meas_find_voltage_at_time(self, meas_name, targ_name, time_at):
        """ Creates the .meas statement for voltage at time"""
        measure_string=".meas tran {0} FIND v({1}) AT={2}n \n\n"
        self.mf.write(measure_string.format(meas_name.lower(),
                                            targ_name,
                                            time_at))

    def gen_meas_power(self, meas_name, t_initial, t_final):
        """ Creates the .meas statement for the measurement of avg power """
        # power mea cmd is different in different spice:
        if OPTS.spice_name == "hspice":
            power_exp = "power"
        else:
            power_exp = "par('(-1*v(" + str(self.vdd_name) + ")*I(v" + str(self.vdd_name) + "))')"
        self.mf.write(".meas tran {0} avg {1} from={2}n to={3}n\n\n".format(meas_name.lower(),
                                                                            power_exp,
                                                                            t_initial,
                                                                            t_final))

    def gen_meas_value(self, meas_name, dout, t_initial, t_final):
        measure_string=".meas tran {0} FIND v({1}) AT={2}n\n\n".format(meas_name.lower(), dout, (t_initial + t_final) / 2)
        # measure_string=".meas tran {0} AVG v({1}) FROM={2}n TO={3}n\n\n".format(meas_name.lower(), dout, t_initial, t_final)
        self.mf.write(measure_string)

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
        timestep = 10 # ps

        if OPTS.spice_name == "ngspice":
            self.sf.write(".TEMP {}\n".format(self.temperature))
            # UIC is needed for ngspice to converge
            # Format: .tran tstep tstop < tstart < tmax >>
            self.sf.write(".TRAN {0}p {1}n 0n {0}p UIC\n".format(timestep, end_time))
            # ngspice sometimes has convergence problems if not using gear method
            # which is more accurate, but slower than the default trapezoid method
            # Do not remove this or it may not converge due to some "pa_00" nodes
            # unless you figure out what these are.
            self.sf.write(".OPTIONS POST=1 RELTOL={0} PROBE method=gear ACCT\n".format(reltol))
        elif OPTS.spice_name == "spectre":
            self.sf.write(".TEMP {}\n".format(self.temperature))
            self.sf.write("simulator lang=spectre\n")
            if OPTS.use_pex:
                nestlvl = 1
                spectre_save = "selected"
            else:
                nestlvl = 10
                spectre_save = "lvlpub"
            self.sf.write('saveOptions options save={} nestlvl={} pwr=total \n'.format(spectre_save, nestlvl))
            self.sf.write("simulatorOptions options reltol=1e-3 vabstol=1e-6 iabstol=1e-12 temp={0} try_fast_op=no "
                          "rforce=10m maxnotes=10 maxwarns=10 "
                          " preservenode=all topcheck=fixall "
                          "digits=5 cols=80 dc_pivot_check=yes pivrel=1e-3 "
                          " \n".format(self.temperature))
            self.sf.write('tran tran step={} stop={}n ic=node write=spectre.dc errpreset=moderate '
                          ' annotate=status maxiters=5 \n'.format("5p", end_time))
            self.sf.write("simulator lang=spice\n")
        elif OPTS.spice_name in ["hspice", "xa"]:
            self.sf.write(".TEMP {}\n".format(self.temperature))
            # Format: .tran tstep tstop < tstart < tmax >>
            self.sf.write(".TRAN {0}p {1}n 0n {0}p UIC\n".format(timestep, end_time))
            self.sf.write(".OPTIONS POST=1 RUNLVL={0} PROBE\n".format(runlvl))
            self.sf.write(".OPTIONS PSF=1 \n")
            self.sf.write(".OPTIONS HIER_DELIM=1 \n")
        elif OPTS.spice_name in ["Xyce", "xyce"]:
            self.sf.write(".OPTIONS DEVICE TEMP={}\n".format(self.temperature))
            self.sf.write(".OPTIONS MEASURE MEASFAIL=1\n")
            self.sf.write(".OPTIONS LINSOL type=klu\n")
            self.sf.write(".OPTIONS TIMEINT RELTOL=1e-3 ABSTOL=1e-6 method=gear minorder=2\n")
            # Format: .TRAN <initial step> <final time> <start time> <step ceiling>
            self.sf.write(".TRAN {0}p {1}n 0n {0}p\n".format(timestep, end_time))
        elif OPTS.spice_name:
            debug.error("Unkown spice simulator {}".format(OPTS.spice_name), -1)

        # create plots for all signals
        if not OPTS.use_pex:   # Don't save all for extracted simulations
            self.sf.write("* probe is used for hspice/xa, while plot is used in ngspice\n")
            if OPTS.verbose_level>0:
                if OPTS.spice_name in ["hspice", "xa"]:
                    self.sf.write(".probe V(*)\n")
                elif OPTS.spice_name != "Xyce":
                    self.sf.write(".plot V(*)\n")
            else:
                self.sf.write("*.probe V(*)\n")
                self.sf.write("*.plot V(*)\n")

        # end the stimulus file
        self.sf.write(".end\n\n")

    def write_include(self, circuit):
        """Writes include statements, inputs are lists of model files"""

        self.sf.write("* {} process corner\n".format(self.process))
        for item in self.device_libraries:
            if OPTS.spice_name:
                item[0] = item[0].replace("SIMULATOR", OPTS.spice_name.lower())
            else:
                item[0] = item[0].replace("SIMULATOR", "ngspice")
            if os.path.isfile(item[0]):
                self.sf.write(".lib \"{0}\" {1}\n".format(item[0], item[1]))
            else:
                debug.error("Could not find spice library: {0}\nSet SPICE_MODEL_DIR to over-ride path.\n".format(item[0]), -1)

        includes = self.device_models + [circuit]

        for item in list(includes):
            if OPTS.spice_name:
                item = item.replace("SIMULATOR", OPTS.spice_name.lower())
            else:
                item = item.replace("SIMULATOR", "ngspice")
            self.sf.write(".include \"{0}\"\n".format(item))

    def add_comment(self, msg):
        self.sf.write(msg + "\n")

    def write_supply(self):
        """ Writes supply voltage statements """
        gnd_node_name = "0"
        self.sf.write("V{0} {0} {1} {2}\n".format(self.vdd_name, gnd_node_name, self.voltage))

        # Adding a commented out supply for simulators where gnd and 0 are not global grounds.
        self.sf.write("\n*Nodes gnd and 0 are the same global ground node in ngspice/hspice/xa. Otherwise, this source may be needed.\n")
        if OPTS.spice_name in ["Xyce", "xyce"]:
            self.sf.write("V{0} {0} {1} {2}\n".format(self.gnd_name, gnd_node_name, 0.0))
        else:
            self.sf.write("*V{0} {0} {1} {2}\n".format(self.gnd_name, gnd_node_name, 0.0))

    def run_sim(self, name):
        """ Run hspice in batch mode and output rawfile to parse. """
        temp_stim = "{0}{1}".format(OPTS.openram_temp, name)
        import datetime
        start_time = datetime.datetime.now()
        debug.check(OPTS.spice_exe != "", "No spice simulator has been found.")

        if OPTS.spice_name == "xa":
            # Output the xa configurations here. FIXME: Move this to write it once.
            xa_cfg = open("{}xa.cfg".format(OPTS.openram_temp), "w")
            xa_cfg.write("set_sim_level -level 7\n")
            xa_cfg.write("set_powernet_level 7 -node vdd\n")
            xa_cfg.close()
            cmd = "{0} {1} -c {2}xa.cfg -o {2}xa -mt {3}".format(OPTS.spice_exe,
                                                                 temp_stim,
                                                                 OPTS.openram_temp,
                                                                 OPTS.num_sim_threads)
            valid_retcode=0
        elif OPTS.spice_name == "spectre":
            if OPTS.use_pex:
                extra_options = " +dcopt +postlayout "
            else:
                extra_options = ""
            cmd = ("{0} -64 {1} -format psfbin -raw {2} {3} -maxwarnstolog 1000 "
                   " +mt={4} -maxnotestolog 1000 "
                   .format(OPTS.spice_exe, temp_stim, OPTS.openram_temp, extra_options,
                           OPTS.num_sim_threads))
            valid_retcode = 0
        elif OPTS.spice_name == "hspice":
            # TODO: Should make multithreading parameter a configuration option
            cmd = "{0} -mt {1} -i {2} -o {3}timing".format(OPTS.spice_exe,
                                                           OPTS.num_sim_threads,
                                                           temp_stim,
                                                           OPTS.openram_temp)
            valid_retcode=0
        elif OPTS.spice_name in ["Xyce", "xyce"]:
            if OPTS.num_sim_threads > 1 and OPTS.mpi_name:
                mpi_cmd = "{0} -np {1}".format(OPTS.mpi_exe,
                                               OPTS.num_sim_threads)
            else:
                mpi_cmd = ""

            # Xyce can save a raw file while doing timing, so keep it around
            cmd = "{0} {1} -r {3}timing.raw -o {3}timing.lis {2}".format(mpi_cmd,
                                                                         OPTS.spice_exe,
                                                                         temp_stim,
                                                                         OPTS.openram_temp)

            valid_retcode=0
        else:
            # ngspice 27+ supports threading with "set num_threads=4" in the stimulus file or a .spiceinit
            # Measurements can't be made with a raw file set in ngspice
            # -r {2}timing.raw
            ng_cfg = open("{}.spiceinit".format(OPTS.openram_temp), "w")
            ng_cfg.write("set num_threads={}\n".format(OPTS.num_sim_threads))
            ng_cfg.write("set ngbehavior=hsa\n")
            ng_cfg.write("set ng_nomodcheck\n")
            ng_cfg.close()

            cmd = "{0} -b -o {2}timing.lis {1}".format(OPTS.spice_exe,
                                                       temp_stim,
                                                       OPTS.openram_temp)
            # for some reason, ngspice-25 returns 1 when it only has acceptable warnings
            valid_retcode=1

        spice_stdout = open("{0}spice_stdout.log".format(OPTS.openram_temp), 'w')
        spice_stderr = open("{0}spice_stderr.log".format(OPTS.openram_temp), 'w')

        # Wrap the command with conda activate & conda deactivate
        # FIXME: Should use verify/run_script.py here but run_script doesn't return
        # the return code of the subprocess. File names might also mismatch.
        from openram import CONDA_HOME
        cmd = "source {0}/bin/activate && {1} && conda deactivate".format(CONDA_HOME, cmd)
        debug.info(2, cmd)
        proc = subprocess.run(cmd, stdout=spice_stdout, stderr=spice_stderr, shell=True)

        spice_stdout.close()
        spice_stderr.close()

        if (proc.returncode > valid_retcode):
            debug.error("Spice simulation error: " + cmd, -1)
        else:
            end_time = datetime.datetime.now()
            delta_time = round((end_time - start_time).total_seconds(), 1)
            debug.info(2, "*** Spice: {} seconds".format(delta_time))
