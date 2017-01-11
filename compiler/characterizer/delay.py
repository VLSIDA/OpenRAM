import sys
import re
import globals
import debug
import tech
import math
import stimuli
import charutils as ch
import utils

OPTS = globals.get_opts()

class delay():
    """
    Functions to measure the delay of the SRAM at a given address and
    data bit.
    """

    def __init__(self,sram,spfile):
        self.name = sram.name
        self.num_words = sram.num_words
        self.word_size = sram.word_size
        self.addr_size = sram.addr_size
        self.sram_sp_file = spfile


    def check_arguments(self):
        """Checks if arguments given for write_stimulus() meets requirements"""
        try:
            int(self.probe_address, 2)
        except ValueError:
            debug.error("Probe Address is not of binary form: {0}".format(self.probe_address),1)

        if len(self.probe_address) != self.addr_size:
            debug.error("Probe Address's number of bits does not correspond to given SRAM",1)

        if not isinstance(self.probe_data, int) or self.probe_data>self.word_size or self.probe_data<0:
            debug.error("Given probe_data is not an integer to specify a data bit",1)


    def write_stimulus(self, feasible_period, target_period, data_value):
        """Creates a stimulus file for simulations to probe a certain bitcell, given an address and data-position of the data-word 
        (probe-address form: '111010000' LSB=0, MSB=1)
        (probe_data form: number corresponding to the bit position of data-bus, begins with position 0) 
        """
        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        self.obtain_cycle_times(slow_period=feasible_period,
                                fast_period=target_period)

        # creates and opens stimulus file for writing
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Stimulus data value of {0} for target period of {1}n\n".format(data_value, target_period))
        self.sf.write("\n")

        # include files in stimulus file
        model_list = tech.spice["fet_models"] + [self.sram_sp_file]
        stimuli.write_include(stim_file=self.sf, models=model_list)
        self.sf.write("\n")

        # add vdd/gnd statements
        self.sf.write("* Global Power Supplies\n")
        stimuli.write_supply(stim_file=self.sf,
                             vdd_name=tech.spice["vdd_name"],
                             gnd_name=tech.spice["gnd_name"],
                             vdd_voltage=tech.spice["supply_voltage"],
                             gnd_voltage=tech.spice["gnd_voltage"])
        self.sf.write("\n")

        # instantiate the sram
        self.sf.write("* Instantiation of the SRAM\n")
        stimuli.inst_sram(stim_file=self.sf,
                          abits=self.addr_size, 
                          dbits=self.word_size, 
                          sram_name=self.name)
        self.sf.write("\n")

        # create a buffer and an inverter
        self.sf.write("* Buffers and inverter Initialization\n")
        # FIXME: We should replace the clock buffer with the same
        # 2x buffer for control signals. This needs the buffer to be
        # added to the control logic though.
        stimuli.create_buffer(stim_file=self.sf,
                              buffer_name="clk1_buffer",
                              size=[1, 4])
        self.sf.write("\n")
        stimuli.create_buffer(stim_file=self.sf,
                              buffer_name="clk2_buffer",
                              size=[8, 16])
        self.sf.write("\n")

        stimuli.create_buffer(stim_file=self.sf,
                              buffer_name="buffer",
                              size=[1, 2])
        self.sf.write("\n")

        stimuli.create_inverter(stim_file=self.sf)
        self.sf.write("\n")

        # add a buffer for each signal and an inverter for WEb
        signal_list = []
        for i in range(self.word_size):
            signal_list.append("D[{0}]".format(i))
        for j in range(self.addr_size):
            signal_list.append("A[{0}]".format(j))
        for k in tech.spice["control_signals"]:
            signal_list.append(k)
        self.sf.write("*Buffers for each generated signal and Inv for WEb\n")
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="buffer",
                           signal_list=signal_list)
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="clk1_buffer",
                           signal_list=["clk"])
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="clk2_buffer",
                           signal_list=["clk_buf"])
        stimuli.add_buffer(stim_file=self.sf,
                           buffer_name="buffer",
                           signal_list=["WEb_trans"])
        stimuli.add_inverter(stim_file=self.sf,
                             signal_list=["WEb_trans"])
        self.sf.write("\n")

        # add access transistors for data-bus
        self.sf.write("* Transmission Gates for data-bus\n")
        stimuli.add_accesstx(stim_file=self.sf, dbits=self.word_size)
        self.sf.write("\n")

        # generate data and addr signals
        self.sf.write("*Generation of data and address signals\n")
        if data_value == tech.spice["supply_voltage"]:
            v_val = tech.spice["gnd_voltage"] 
        else:
            v_val = tech.spice["supply_voltage"] 
        for i in range(self.word_size):
            if i == self.probe_data:
                stimuli.gen_data_pwl(stim_file=self.sf,
                                     key_times=self.cycle_times,
                                     sig_name="D[{0}]".format(i),
                                     data_value=data_value,
                                     feasible_period=feasible_period,
                                     target_period=target_period,
                                     t_rise=tech.spice["rise_time"],
                                     t_fall=tech.spice["fall_time"])
            else:
                stimuli.gen_constant(stim_file=self.sf,
                                     sig_name="D[{0}]".format(i),
                                     v_ref=tech.spice["gnd_voltage"],
                                     v_val=v_val)

        stimuli.gen_addr_pwl(stim_file=self.sf,
                             key_times=self.cycle_times,
                             addr=self.probe_address,
                             feasible_period=feasible_period,
                             target_period=target_period,
                             t_rise=tech.spice["rise_time"],
                             t_fall=tech.spice["fall_time"])
        self.sf.write("\n")

        # generate control signals
        self.sf.write("*Generation of control signals\n")
        # CSb
        (x_list, y_list) = stimuli.gen_csb_pwl(key_times=self.cycle_times,
                                               feasible_period=feasible_period,
                                               target_period=target_period,
                                               t_rise=tech.spice["rise_time"],
                                               t_fall=tech.spice["fall_time"])
        stimuli.gen_pwl(stim_file=self.sf,
                        sig_name="CSb",
                        x_list=x_list,
                        y_list=y_list)
        # WEb
        (x_list, y_list) = stimuli.gen_web_pwl(key_times=self.cycle_times,
                                               feasible_period=feasible_period,
                                               target_period=target_period,
                                               t_rise=tech.spice["rise_time"],
                                               t_fall=tech.spice["fall_time"])
        stimuli.gen_pwl(stim_file=self.sf,
                                sig_name="WEb",
                                x_list=x_list,
                                y_list=y_list)
        # OEb
        (x_list, y_list) = stimuli.gen_oeb_pwl(key_times=self.cycle_times,
                                               feasible_period=feasible_period,
                                               target_period=target_period,
                                               t_rise=tech.spice["rise_time"],
                                               t_fall=tech.spice["fall_time"])
        stimuli.gen_pwl(stim_file=self.sf,
                                sig_name="OEb",
                                x_list=x_list,
                                y_list=y_list)
        # WEb_transmission_gate
        (x_list, y_list) = stimuli.gen_web_trans_pwl(key_times=self.cycle_times,
                                                     feasible_period=feasible_period,
                                                     target_period=target_period, 
                                                     t_rise=tech.spice["rise_time"],
                                                     t_fall=tech.spice["fall_time"])
        stimuli.gen_pwl(stim_file=self.sf,
                                sig_name="WEb_trans",
                                x_list=x_list,
                                y_list=y_list)
        self.sf.write("\n")

        self.write_clock()

        self.write_measures(data_value)

        self.write_control()

        self.sf.close()

    def write_clock(self):
        # generate clk PWL based on the clock periods
        self.sf.write("* Generation of global clock signal\n")
        stimuli.gen_clk_pwl(stim_file=self.sf,
                            cycle_times=self.cycle_times,
                            t_rise=tech.spice["rise_time"],
                            t_fall=tech.spice["fall_time"])
        self.sf.write("\n")

    def write_measures(self, data_value):
        # meas statement for delay and power measurements
        self.sf.write("* Measure statements for delay and power\n")

        # add measure statments for delay
        trig_name = tech.spice["clk"] + "_buf_buf"
        targ_name = "{0}".format("DATA[{0}]".format(self.probe_data))
        trig_val = targ_val = 0.5 * tech.spice["supply_voltage"]
        trig_dir = self.read_cycle
        targ_dir = "RISE" if data_value == tech.spice["supply_voltage"] else "FALL"
        td = self.cycle_times[self.clear_bus_cycle]
        stimuli.gen_meas_delay(stim_file=self.sf,
                               meas_name="DELAY",
                               trig_name=trig_name,
                               targ_name=targ_name,
                               trig_val=trig_val,
                               targ_val=targ_val,
                               trig_dir=trig_dir,
                               targ_dir=targ_dir,
                               td=td)

        # add measure statements for power
        t_initial = self.cycle_times[self.write_cycle]
        t_final = self.cycle_times[self.write_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="POWER_WRITE",
                               t_initial=t_initial,
                               t_final=t_final)

        t_initial = self.cycle_times[self.read_cycle]
        t_final = self.cycle_times[self.read_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="POWER_READ",
                               t_initial=t_initial,
                               t_final=t_final)
        self.sf.write("\n")


    def write_control(self):
        # run until the last cycle time
        end_time = self.cycle_times[-1]
        self.sf.write(".TRAN 5p {0}n\n".format(end_time))
        self.sf.write(".OPTIONS POST=1 PROBE\n")
        # create plots for all signals
        self.sf.write(".probe V(*)\n")
        # end the stimulus file
        self.sf.write(".end\n")



    def find_feasible_period(self,initial_period):
        """Uses an initial period and finds a feasible period before we
        run the binary search algorithm to find min period. We check if
        the given clock period is valid and if it's not, we continue to
        double the period until we find a valid period to use as a
        starting point. """

        feasible_period = initial_period
        time_out = 8
        while True:
            debug.info(1, "Finding feasible period: {0}ns".format(feasible_period))
            time_out -= 1

            if (time_out <= 0):
                debug.error("Timed out, could not find a feasible period.",2)

            (success, delay_out)=self.try_period(feasible_period,feasible_period,tech.spice["supply_voltage"])                
            if not success:
                feasible_period = 2 * feasible_period
                continue

            (success, delay_out)=self.try_period(feasible_period,feasible_period,tech.spice["gnd_voltage"])                
            if not success:
                feasible_period = 2 * feasible_period
                continue

            debug.info(1, "Starting Binary Search Algorithm with feasible_period: {0}ns".format(feasible_period))
            return feasible_period


    def try_period(self, feasible_period, target_period, data_value):
        """ This tries to simulate a period and checks if the result
        works. If so, it returns True.  If not, it it doubles the
        period and returns False."""

        # Checking from not data_value to data_value
        self.write_stimulus(feasible_period, target_period, data_value)
        stimuli.run_sim()
        delay_value = ch.convert_to_float(ch.parse_output("timing", "delay"))
        
        # if it failed or the read was longer than a period
        if type(delay_value)!=float or delay_value*1e9>target_period:
            debug.info(2,"Infeasible period " + str(target_period) + " delay " + str(delay_value*1e9) + "ns")
            return (False, "NA")
        else:
            debug.info(2,"Feasible period " + str(feasible_period) \
                           + ", target period " + str(target_period) \
                           + ", read/write of " + str(data_value) \
                           + ", delay=" + str(delay_value*1e9) + "ns")
        #key=raw_input("press return to continue")

        return (True, delay_value*1e9)


    def find_min_period(self,data_value):
        """Creates a spice test and instantiates a single SRAM for
        testing.  Returns a tuple of the lowest period and its
        clk-to-q delay for the specified data_value."""

        # Find a valid and feasible period before starting the binary search
        # We just try 2.0ns here, but any value would work albeit slower.
        feasible_period = self.find_feasible_period(tech.spice["feasible_period"])
        previous_period = ub_period = feasible_period
        lb_period = 0.0

        # Binary search algorithm to find the min period (max frequency) of design
        time_out = 25
        while True:
            time_out -= 1
            if (time_out <= 0):
                debug.error("Timed out, could not converge on minimum period.",2)

            target_period = 0.5 * (ub_period + lb_period)
            debug.info(1, "MinPeriod Search: {0}ns (ub: {1} lb: {2})".format(target_period,
                                                                             ub_period,
                                                                             lb_period))

            (success, delay_out) = self.try_period(feasible_period, target_period, data_value)
            if success:
                ub_period = target_period
            else:
                lb_period = target_period

            if ch.relative_compare(ub_period, lb_period):
                # use the two values to compare, but only return the ub since it is guaranteed feasible
                (success, delay_out) = self.try_period(feasible_period, ub_period, data_value)
                return (ub_period, delay_out)

        self.error("Should not reach here.",-1)
        return (target_period, delay_out)

    def set_probe(self,probe_address, probe_data):
        """ Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze."""
        self.probe_address = probe_address
        self.probe_data = probe_data

    def analyze(self,probe_address, probe_data):
        """main function to calculate the min period for a low_to_high
        transistion and a high_to_low transistion returns a dictionary
        that contains all both the min period and associated delays
        Dictionary Keys: min_period1, delay1, min_period0, delay0
        """
        self.set_probe(probe_address, probe_data)

        (min_period1, delay1) = self.find_min_period(tech.spice["supply_voltage"])
        if (min_period1 == None) or (delay1 == None):
            return None
        debug.info(1, "Min Period for low_to_high transistion: {0}n with a delay of {1}".format(min_period1, delay1))
        (min_period0, delay0) = self.find_min_period(tech.spice["gnd_voltage"])
        if (min_period0 == None) or (delay0 == None):
            return None
        debug.info(1, "Min Period for high_to_low transistion: {0}n with a delay of {1}".format(min_period0, delay0))
        read_power=ch.convert_to_float(ch.parse_output("timing", "power_read"))
	write_power=ch.convert_to_float(ch.parse_output("timing", "power_write"))

	data = {"min_period1": min_period1,  # period in ns
                "delay1": delay1, # delay in s
                "min_period0": min_period0,
                "delay0": delay0,
                "read_power": read_power,
                "write_power": write_power
                }
	return data


    def obtain_cycle_times(self, slow_period, fast_period):
        """Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation. The last time is the end of the simulation
        and does not need a rising edge."""

        # idle: half cycle, no operation
        t_current = 0.5 * slow_period 

        # slow cycle1: W data 1 address 1111 to initialize cell to a value
        self.cycle_times = [t_current]
        self.init_cycle=1
        t_current += slow_period

        # slow cycle2: R data 1 address 1111 (to ensure cell was written to opposite data value)
        self.cycle_times.append(t_current)
        self.verify_init_cycle=2
        t_current += slow_period

        # fast cycle3: W data 0 address 1111 (to ensure a write of opposite value works)
        self.cycle_times.append(t_current)
        self.write_cycle=3
        t_current += fast_period

        # fast cycle4: W data 1 address 0000 (to invert the bus cap from prev write)
        self.cycle_times.append(t_current)
        self.clear_bus_cycle=4
        t_current += fast_period

        # fast cycle5: R data 0 address 1111 (to ensure that a read works and gets the value)
        self.cycle_times.append(t_current)
        self.read_cycle=5
        t_current += fast_period

        # slow cycle 6: wait a slow clock period  to end the simulation
        self.cycle_times.append(t_current)
        self.wait_cycle=6
        t_current += slow_period

        # end time of simulation
        self.cycle_times.append(t_current)

