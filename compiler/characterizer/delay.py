import sys
import re
import debug
import tech
import math
import stimuli
import charutils as ch
import utils
from globals import OPTS

class delay():
    """
    Functions to measure the delay of an SRAM at a given address and
    data bit.
    """

    def __init__(self,sram,spfile):
        self.name = sram.name
        self.num_words = sram.num_words
        self.word_size = sram.word_size
        self.addr_size = sram.addr_size
        self.sram_sp_file = spfile

        self.vdd = tech.spice["supply_voltage"]
        self.gnd = tech.spice["gnd_voltage"]

        
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


    def write_stimulus(self, period, load, slew):
        """ Creates a stimulus file for simulations to probe a bitcell at a given clock period.
        Address and bit were previously set with set_probe().
        Input slew (in ns) and output capacitive load (in fF) are required for charaterization.
        """
        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        self.obtain_cycle_times(period)

        # creates and opens stimulus file for writing
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Stimulus for period of {0}n load={1}fF slew={2}ns\n\n".format(period,load,slew))

        # include files in stimulus file
        model_list = tech.spice["fet_models"] + [self.sram_sp_file]
        stimuli.write_include(stim_file=self.sf, models=model_list)

        # add vdd/gnd statements

        self.sf.write("\n* Global Power Supplies\n")
        stimuli.write_supply(self.sf)

        # instantiate the sram
        self.sf.write("\n* Instantiation of the SRAM\n")
        stimuli.inst_sram(stim_file=self.sf,
                          abits=self.addr_size, 
                          dbits=self.word_size, 
                          sram_name=self.name)

        self.sf.write("\n* SRAM output loads\n")
        for i in range(self.word_size):
            self.sf.write("CD{0} d[{0}] 0 {1}f\n".format(i,load))
        
        # add access transistors for data-bus
        self.sf.write("\n* Transmission Gates for data-bus and control signals\n")
        stimuli.inst_accesstx(stim_file=self.sf, dbits=self.word_size)

        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        for i in range(self.word_size):
            if i == self.probe_data:
                self.gen_data(clk_times=self.cycle_times,
                              sig_name="data[{0}]".format(i),
                              period=period,
                              slew=slew)
            else:
                stimuli.gen_constant(stim_file=self.sf,
                                     sig_name="d[{0}]".format(i),
                                     v_val=self.gnd)

        self.gen_addr(clk_times=self.cycle_times,
                         addr=self.probe_address,
                         period=period,
                         slew=slew)

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        self.gen_csb(self.cycle_times, period, slew)
        self.gen_web(self.cycle_times, period, slew)
        self.gen_oeb(self.cycle_times, period, slew)

        self.sf.write("\n* Generation of global clock signal\n")
        stimuli.gen_pulse(stim_file=self.sf,
                          sig_name="CLK",
                          v1=self.gnd,
                          v2=self.vdd,
                          offset=period,
                          period=period,
                          t_rise=slew,
                          t_fall=slew)
                          
        self.write_measures(period)

        # run until the end of the cycle time
        stimuli.write_control(self.sf,self.cycle_times[-1] + period)

        self.sf.close()

    def write_measures(self,period):
        """
        Write the measure statements to quantify the delay and power results.
        """

        self.sf.write("\n* Measure statements for delay and power\n")

        # Output some comments to aid where cycles start and
        # what is happening
        for comment in self.cycle_comments:
            self.sf.write("* {}\n".format(comment))

        # Trigger on the clk of the appropriate cycle
        trig_name = "clk"
        targ_name = "{0}".format("d[{0}]".format(self.probe_data))
        trig_val = targ_val = 0.5 * self.vdd

        # Delay the target to measure after the negative edge
        stimuli.gen_meas_delay(stim_file=self.sf,
                               meas_name="DELAY0",
                               trig_name=trig_name,
                               targ_name=targ_name,
                               trig_val=trig_val,
                               targ_val=targ_val,
                               trig_dir="FALL",
                               targ_dir="FALL",
                               trig_td=self.cycle_times[self.read0_cycle],
                               targ_td=self.cycle_times[self.read0_cycle]+0.5*period)

        stimuli.gen_meas_delay(stim_file=self.sf,
                               meas_name="DELAY1",
                               trig_name=trig_name,
                               targ_name=targ_name,
                               trig_val=trig_val,
                               targ_val=targ_val,
                               trig_dir="FALL",
                               targ_dir="RISE",
                               trig_td=self.cycle_times[self.read1_cycle],
                               targ_td=self.cycle_times[self.read1_cycle]+0.5*period)

        stimuli.gen_meas_delay(stim_file=self.sf,
                               meas_name="SLEW0",
                               trig_name=targ_name,
                               targ_name=targ_name,
                               trig_val=0.9*self.vdd,
                               targ_val=0.1*self.vdd,
                               trig_dir="FALL",
                               targ_dir="FALL",
                               trig_td=self.cycle_times[self.read0_cycle],
                               targ_td=self.cycle_times[self.read0_cycle]+0.5*period)

        stimuli.gen_meas_delay(stim_file=self.sf,
                               meas_name="SLEW1",
                               trig_name=targ_name,
                               targ_name=targ_name,
                               trig_val=0.1*self.vdd,
                               targ_val=0.9*self.vdd,
                               trig_dir="RISE",
                               targ_dir="RISE",
                               trig_td=self.cycle_times[self.read1_cycle],
                               targ_td=self.cycle_times[self.read1_cycle]+0.5*period)
        
        # add measure statements for power
        t_initial = self.cycle_times[self.write0_cycle]
        t_final = self.cycle_times[self.write0_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="WRITE0_POWER",
                               t_initial=t_initial,
                               t_final=t_final)

        t_initial = self.cycle_times[self.write1_cycle]
        t_final = self.cycle_times[self.write1_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="WRITE1_POWER",
                               t_initial=t_initial,
                               t_final=t_final)
        
        t_initial = self.cycle_times[self.read0_cycle]
        t_final = self.cycle_times[self.read0_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="READ0_POWER",
                               t_initial=t_initial,
                               t_final=t_final)

        t_initial = self.cycle_times[self.read1_cycle]
        t_final = self.cycle_times[self.read1_cycle+1]
        stimuli.gen_meas_power(stim_file=self.sf,
                               meas_name="READ1_POWER",
                               t_initial=t_initial,
                               t_final=t_final)
        
    def find_feasible_period(self, load, slew):
        """
        Uses an initial period and finds a feasible period before we
        run the binary search algorithm to find min period. We check if
        the given clock period is valid and if it's not, we continue to
        double the period until we find a valid period to use as a
        starting point. 
        """

        feasible_period = tech.spice["feasible_period"]
        time_out = 8
        while True:
            debug.info(1, "Trying feasible period: {0}ns".format(feasible_period))
            time_out -= 1

            if (time_out <= 0):
                debug.error("Timed out, could not find a feasible period.",2)

            (success, feasible_delay1, feasible_slew1, feasible_delay0, feasible_slew0)=self.run_simulation(feasible_period,load,slew)
            if not success:
                feasible_period = 2 * feasible_period
                continue

            debug.info(1, "Found feasible_period: {0}ns " +
                       "feasible_delay1/0 {1}ns/{2}ns slew {3}ns/{4}ns".format(feasible_period,
                                                                               feasible_delay1,
                                                                               feasible_delay0,
                                                                               feasible_slew1,
                                                                               feasible_slew0))
            return (feasible_period, feasible_delay1, feasible_delay0)


    def run_simulation(self, period, load, slew):
        """ 
        This tries to simulate a period and checks if the result
        works. If so, it returns True and the delays and slews.
        """

        # Checking from not data_value to data_value
        self.write_stimulus(period, load, slew)
        stimuli.run_sim()
        delay0 = ch.convert_to_float(ch.parse_output("timing", "delay0"))
        delay1 = ch.convert_to_float(ch.parse_output("timing", "delay1"))        
        slew0 = ch.convert_to_float(ch.parse_output("timing", "slew0"))
        slew1 = ch.convert_to_float(ch.parse_output("timing", "slew1"))        
        
        # if it failed or the read was longer than a period
        if type(delay0)!=float or type(delay1)!=float or type(slew1)!=float or type(slew0)!=float:
            debug.info(2,"Failed simulation: period {0} load {1} slew {2}, " +
                       "delay0={3}n delay1={4}ns slew0={5}n slew1={6}n".format(period,
                                                                               load,
                                                                               slew,
                                                                               delay0,
                                                                               delay1,
                                                                               slew0,
                                                                               slew1))
            return (False,0,0,0,0)
        # Scale delays to ns (they previously could have not been floats)
        delay0 *= 1e9
        delay1 *= 1e9
        slew0 *= 1e9
        slew1 *= 1e9
        if delay0>period or delay1>period or slew0>period or slew1>period:
            debug.info(2,"UNsuccessful simulation: period {0} load {1} slew {2}, " +
                       "delay0={3}n delay1={4}ns slew0={5}n slew1={6}n".format(period,
                                                                               load,
                                                                               slew,
                                                                               delay0,
                                                                               delay1,
                                                                               slew0,
                                                                               slew1))
            return (False,0,0,0,0)
        else:
            debug.info(2,"Successful simulation: period {0} load {1} slew {2}, " +
                       "delay0={3}n delay1={4}ns slew0={5}n slew1={6}n".format(period,
                                                                               load,
                                                                               slew,
                                                                               delay0,
                                                                               delay1,
                                                                               slew0,
                                                                               slew1))
        # For debug, you sometimes want to inspect each simulation.
        #key=raw_input("press return to continue")

        # The delay is from the negative edge for our SRAM
        return (True,delay1,slew1,delay0,slew0)



    def find_min_period(self,feasible_period, load, slew, feasible_delay1, feasible_delay0):
        """
        Searches for the smallest period with output delays being within 5% of 
        long period. 
        """

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

            if self.try_period(target_period, load, slew, feasible_delay1, feasible_delay0):
                ub_period = target_period
            else:
                lb_period = target_period

            if ch.relative_compare(ub_period, lb_period, error_tolerance=0.05):
                # ub_period is always feasible
                return ub_period


    def try_period(self, period, load, slew, feasible_delay1, feasible_delay0):
        """ 
        This tries to simulate a period and checks if the result
        works. If it does and the delay is within 5% still, it returns True.
        """

        # Checking from not data_value to data_value
        self.write_stimulus(period,load,slew)
        stimuli.run_sim()
        delay0 = ch.convert_to_float(ch.parse_output("timing", "delay0"))
        delay1 = ch.convert_to_float(ch.parse_output("timing", "delay1"))
        slew0 = ch.convert_to_float(ch.parse_output("timing", "slew0"))
        slew1 = ch.convert_to_float(ch.parse_output("timing", "slew1"))
        # if it failed or the read was longer than a period
        if type(delay0)!=float or type(delay1)!=float or type(slew1)!=float or type(slew0)!=float:
            debug.info(2,"Invalid measures: Period {0}, " +
                       "delay0={1}ns, delay1={2}ns slew0={3}ns slew1={4}ns".format(period, delay0, delay1, slew0, slew1))
            return False
        delay0 *= 1e9
        delay1 *= 1e9
        slew0 *= 1e9
        slew1 *= 1e9
        if delay0>period or delay1>period or slew0>period or slew1>period:
            debug.info(2,"Too long delay/slew: Period {0}, " +
                       "delay0={1}ns, delay1={2}ns slew0={3}ns slew1={4}ns".format(period, delay0, delay1, slew0, slew1))
            return False
        else:
            if not ch.relative_compare(delay1,feasible_delay1,error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay1,feasible_delay1))
                return False
            elif not ch.relative_compare(delay0,feasible_delay0,error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay0,feasible_delay0))
                return False


        #key=raw_input("press return to continue")

        debug.info(2,"Successful period {0}, " +
                   "delay0={1}ns, delay1={2}ns slew0={3}ns slew1={4}ns".format(period, delay0, delay1, slew0, slew1))
        return True
    
    def set_probe(self,probe_address, probe_data):
        """ Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze."""
        self.probe_address = probe_address
        self.probe_data = probe_data


    def analyze(self,probe_address, probe_data, slews, loads):
        """main function to calculate the min period for a low_to_high
        transistion and a high_to_low transistion returns a dictionary
        that contains all both the min period and associated delays
        Dictionary Keys: min_period1, delay1, min_period0, delay0
        """
        
        self.set_probe(probe_address, probe_data)

        # This is for debugging a full simulation
        # debug.info(0,"Debug simulation running...")
        # target_period=50.0
        # feasible_delay1=0.059083183
        # feasible_delay0=0.17953789
        # load=1.6728
        # slew=0.04
        # self.try_period(target_period, load, slew, feasible_delay1, feasible_delay0)
        # sys.exit(1)

        
        (feasible_period, feasible_delay1, feasible_delay0) = self.find_feasible_period(max(loads), max(slews))
        debug.check(feasible_delay1>0,"Negative delay may not be possible")
        debug.check(feasible_delay0>0,"Negative delay may not be possible")

        # The power variables are just scalars. These use the final feasible period simulation
        # which should have worked.
        read0_power=ch.convert_to_float(ch.parse_output("timing", "read0_power"))
        write0_power=ch.convert_to_float(ch.parse_output("timing", "write0_power"))
        read1_power=ch.convert_to_float(ch.parse_output("timing", "read1_power"))
        write1_power=ch.convert_to_float(ch.parse_output("timing", "write1_power"))
        
        LH_delay = []
        HL_delay = []
        LH_slew = []
        HL_slew = []
        for slew in slews:
            for load in loads:
                (success, delay1, slew1, delay0, slew0) = self.run_simulation(feasible_period, load, slew)
                debug.check(success,"Couldn't run a simulation. slew={0} load={1}\n".format(slew,load))
                LH_delay.append(delay1)
                HL_delay.append(delay0)
                LH_slew.append(slew1)
                HL_slew.append(slew0)
                
        # finds the minimum period without degrading the delays by X%
        min_period = self.find_min_period(feasible_period, max(loads), max(slews), feasible_delay1, feasible_delay0)
        debug.check(type(min_period)==float,"Couldn't find minimum period.")
        debug.info(1, "Min Period: {0}n with a delay of {1} / {2}".format(min_period, feasible_delay1, feasible_delay0))


        data = {"min_period": ch.round_time(min_period), 
                "delay1": LH_delay,
                "delay0": HL_delay,
                "slew1": LH_slew,
                "slew0": HL_slew,
                "read0_power": read0_power*1e3,
                "read1_power": read1_power*1e3,
                "write0_power": write0_power*1e3,
                "write1_power": write1_power*1e3
                }
        return data


    def obtain_cycle_times(self, period):
        """Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation. The last time is the end of the simulation
        and does not need a rising edge."""

        self.cycle_comments = []
        self.cycle_times = []
        t_current = 0

        # idle cycle, no operation
        msg = "Idle cycle (no clock)"
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(0,
                                                                t_current,
                                                                msg))
        self.cycle_times.append(t_current)
        t_current += period

        # One period
        msg = "W data 1 address 11..11 to initialize cell"
        self.cycle_times.append(t_current)
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period

        # One period
        msg = "W data 0 address 11..11 (to ensure a write of value works)"
        self.cycle_times.append(t_current)
        self.write0_cycle=len(self.cycle_times)-1
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period
        
        # One period
        msg = "W data 1 address 00..00 (to clear bus caps)"
        self.cycle_times.append(t_current)
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period

        # One period
        msg = "R data 0 address 11..11 to check W0 worked"
        self.cycle_times.append(t_current)
        self.read0_cycle=len(self.cycle_times)-1
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period

        # One period
        msg = "Idle cycle"
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        self.cycle_times.append(t_current)
        t_current += period

        # One period
        msg = "W data 1 address 11..11 (to ensure a write of value worked)"
        self.cycle_times.append(t_current)
        self.write1_cycle=len(self.cycle_times)-1
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period

        # One period
        msg = "W data 0 address 00..00 (to clear bus caps)"
        self.cycle_times.append(t_current)
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period
        
        # One period
        msg = "R data 1 address 11..11 to check W1 worked"
        self.cycle_times.append(t_current)
        self.read1_cycle=len(self.cycle_times)-1
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        t_current += period

        # One period
        msg = "Idle cycle"
        self.cycle_comments.append("Cycle{0}\t{1}ns:\t{2}".format(len(self.cycle_times)-1,
                                                                t_current,
                                                                msg))
        self.cycle_times.append(t_current)
        t_current += period



    def analytical_model(self,sram, slews, loads):
        """ Just return the analytical model results for the SRAM. 
        """
        LH_delay = []
        HL_delay = []
        LH_slew = []
        HL_slew = []
        for slew in slews:
            for load in loads:
                bank_delay = sram.analytical_delay(slew,load)
                # Convert from ps to ns
                LH_delay.append(bank_delay.delay/1e3)
                HL_delay.append(bank_delay.delay/1e3)
                LH_slew.append(bank_delay.slew/1e3)
                HL_slew.append(bank_delay.slew/1e3)
        
        data = {"min_period": 0, 
                "delay1": LH_delay,
                "delay0": HL_delay,
                "slew1": LH_slew,
                "slew0": HL_slew,
                "read0_power": 0,
                "read1_power": 0,
                "write0_power": 0,
                "write1_power": 0
                }
        return data

    def gen_data(self, clk_times, sig_name, period, slew):
        """ Generates the PWL data inputs for a simulation timing test. """
        # values for NOP, W1, W0, W1, R0, NOP, W1, W0, R1, NOP
        # we are asserting the opposite value on the other side of the tx gate during
        # the read to be "worst case". Otherwise, it can actually assist the read.
        values = [0, 1, 0, 1, 1, 1, 1, 0, 0, 0 ]
        stimuli.gen_pwl(self.sf, sig_name, clk_times, values, period, slew, 0.05)

    def gen_addr(self, clk_times, addr, period, slew):
        """ 
        Generates the address inputs for a simulation timing test. 
        This alternates between all 1's and all 0's for the address.
        """

        zero_values = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0 ]
        ones_values = [1, 1, 1, 0, 1, 0, 1, 0, 1, 1 ]

        for i in range(len(addr)):
            sig_name = "A[{0}]".format(i)
            if addr[i]=="1":
                stimuli.gen_pwl(self.sf, sig_name, clk_times, ones_values, period, slew, 0.05)
            else:
                stimuli.gen_pwl(self.sf, sig_name, clk_times, zero_values, period, slew, 0.05)


    def gen_csb(self, clk_times, period, slew):
        """ Generates the PWL CSb signal """
        # values for NOP, W1, W0, W1, R0, NOP, W1, W0, R1, NOP
        # Keep CSb asserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        stimuli.gen_pwl(self.sf, "csb", clk_times, values, period, slew, 0.05)

    def gen_web(self, clk_times, period, slew):
        """ Generates the PWL WEb signal """
        # values for NOP, W1, W0, W1, R0, NOP, W1, W0, R1, NOP
        # Keep WEb deasserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1]
        stimuli.gen_pwl(self.sf, "web", clk_times, values, period, slew, 0.05)

        # Keep acc_en deasserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1]
        stimuli.gen_pwl(self.sf, "acc_en", clk_times, values, period, slew, 0)
        values = [0, 1, 1, 1, 0, 0, 1, 1, 0, 0]
        stimuli.gen_pwl(self.sf, "acc_en_inv", clk_times, values, period, slew, 0)
        
    def gen_oeb(self, clk_times, period, slew):
        """ Generates the PWL WEb signal """
        # values for NOP, W1, W0, W1, R0, W1, W0, R1, NOP
        # Keep OEb asserted in NOP for measuring >1 period
        values = [1, 1, 1, 1, 0, 0, 1, 1, 0, 0]
        stimuli.gen_pwl(self.sf, "oeb", clk_times, values, period, slew, 0.05)
