import sys,re,shutil
import debug
import tech
import math
import stimuli
from trim_spice import trim_spice
import charutils as ch
import utils
from globals import OPTS

class delay():
    """Functions to measure the delay and power of an SRAM at a given address and
    data bit.

    In general, this will perform the following actions:
    1) Trim the netlist to remove unnecessary logic.
    2) Find a feasible clock period using max load/slew on the trimmed netlist.
    3) Characterize all loads/slews and consider fail when delay is greater than 5% of feasible delay using trimmed netlist.
    4) Measure the leakage during the last cycle of the trimmed netlist when there is no operation.
    5) Measure the leakage of the whole netlist (untrimmed) in each corner.
    6) Subtract the trimmed leakage and add the untrimmed leakage to the power.

    Netlist trimming can be removed by setting OPTS.trim_netlist to
    False, but this is VERY slow.

    """

    def __init__(self, sram, spfile, corner):
        self.sram = sram
        self.name = sram.name
        self.word_size = self.sram.word_size
        self.addr_size = self.sram.addr_size
        self.num_cols = self.sram.num_cols
        self.num_rows = self.sram.num_rows
        self.num_banks = self.sram.num_banks
        self.sp_file = spfile

        self.set_corner(corner)
        
    def set_corner(self,corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner
        
        
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

    def write_generic_stimulus(self, load):
        """ Create the instance, supplies, loads, and access transistors. """

        # add vdd/gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()

        # instantiate the sram
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_sram(abits=self.addr_size, 
                            dbits=self.word_size, 
                            sram_name=self.name)

        self.sf.write("\n* SRAM output loads\n")
        for i in range(self.word_size):
            self.sf.write("CD{0} d[{0}] 0 {1}f\n".format(i,load))
        
        # add access transistors for data-bus
        self.sf.write("\n* Transmission Gates for data-bus and control signals\n")
        self.stim.inst_accesstx(dbits=self.word_size)
        

    def write_delay_stimulus(self, period, load, slew):
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
        self.sf.write("* Delay stimulus for period of {0}n load={1}fF slew={2}ns\n\n".format(period,load,slew))
        self.stim = stimuli.stimuli(self.sf, self.corner)
        # include files in stimulus file
        self.stim.write_include(self.trim_sp_file)

        self.write_generic_stimulus(load)
        
        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        for i in range(self.word_size):
            if i == self.probe_data:
                self.gen_data(clk_times=self.cycle_times,
                              sig_name="data[{0}]".format(i),
                              period=period,
                              slew=slew)
            else:
                self.stim.gen_constant(sig_name="d[{0}]".format(i),
                                       v_val=0)

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
        self.stim.gen_pulse(sig_name="CLK",
                            v1=0,
                            v2=self.vdd_voltage,
                            offset=period,
                            period=period,
                            t_rise=slew,
                            t_fall=slew)
                          
        self.write_delay_measures(period)

        # run until the end of the cycle time
        self.stim.write_control(self.cycle_times[-1] + period)

        self.sf.close()


    def write_power_stimulus(self, period, load, trim):
        """ Creates a stimulus file to measure leakage power only. 
        This works on the *untrimmed netlist*.
        """
        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        self.obtain_cycle_times(period)

        # creates and opens stimulus file for writing
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Power stimulus for period of {0}n\n\n".format(period))
        self.stim = stimuli.stimuli(self.sf, self.corner)
        
        # include UNTRIMMED files in stimulus file
        if trim:
            self.stim.write_include(self.trim_sp_file)
        else:
            self.stim.write_include(self.sim_sp_file)
            
        self.write_generic_stimulus(load)
        
        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        for i in range(self.word_size):
            self.stim.gen_constant(sig_name="d[{0}]".format(i),
                                   v_val=0)
        for i in range(self.addr_size):
            self.stim.gen_constant(sig_name="A[{0}]".format(i),
                                   v_val=0)

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        self.stim.gen_constant(sig_name="CSb", v_val=self.vdd_voltage)
        self.stim.gen_constant(sig_name="WEb", v_val=self.vdd_voltage)
        self.stim.gen_constant(sig_name="OEb", v_val=self.vdd_voltage)        

        self.sf.write("\n* Generation of global clock signal\n")
        self.stim.gen_constant(sig_name="CLK", v_val=0)  
                          
        self.write_power_measures(period)

        # run until the end of the cycle time
        self.stim.write_control(2*period)

        self.sf.close()
        
    def write_delay_measures(self,period):
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
        trig_val = targ_val = 0.5 * self.vdd_voltage

        # Delay the target to measure after the negative edge
        self.stim.gen_meas_delay(meas_name="delay_hl",
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="FALL",
                                 targ_dir="FALL",
                                 trig_td=self.cycle_times[self.read0_cycle],
                                 targ_td=self.cycle_times[self.read0_cycle]+0.5*period)

        self.stim.gen_meas_delay(meas_name="delay_lh",
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="FALL",
                                 targ_dir="RISE",
                                 trig_td=self.cycle_times[self.read1_cycle],
                                 targ_td=self.cycle_times[self.read1_cycle]+0.5*period)

        self.stim.gen_meas_delay(meas_name="slew_hl",
                                 trig_name=targ_name,
                                 targ_name=targ_name,
                                 trig_val=0.9*self.vdd_voltage,
                                 targ_val=0.1*self.vdd_voltage,
                                 trig_dir="FALL",
                                 targ_dir="FALL",
                                 trig_td=self.cycle_times[self.read0_cycle],
                                 targ_td=self.cycle_times[self.read0_cycle]+0.5*period)

        self.stim.gen_meas_delay(meas_name="slew_lh",
                                 trig_name=targ_name,
                                 targ_name=targ_name,
                                 trig_val=0.1*self.vdd_voltage,
                                 targ_val=0.9*self.vdd_voltage,
                                 trig_dir="RISE",
                                 targ_dir="RISE",
                                 trig_td=self.cycle_times[self.read1_cycle],
                                 targ_td=self.cycle_times[self.read1_cycle]+0.5*period)
        
        # add measure statements for power
        t_initial = self.cycle_times[self.write0_cycle]
        t_final = self.cycle_times[self.write0_cycle+1]
        self.stim.gen_meas_power(meas_name="write0_power",
                                 t_initial=t_initial,
                                 t_final=t_final)

        t_initial = self.cycle_times[self.write1_cycle]
        t_final = self.cycle_times[self.write1_cycle+1]
        self.stim.gen_meas_power(meas_name="write1_power",
                                 t_initial=t_initial,
                                 t_final=t_final)
        
        t_initial = self.cycle_times[self.read0_cycle]
        t_final = self.cycle_times[self.read0_cycle+1]
        self.stim.gen_meas_power(meas_name="read0_power",
                                 t_initial=t_initial,
                                 t_final=t_final)

        t_initial = self.cycle_times[self.read1_cycle]
        t_final = self.cycle_times[self.read1_cycle+1]
        self.stim.gen_meas_power(meas_name="read1_power",
                                 t_initial=t_initial,
                                 t_final=t_final)

        
    def write_power_measures(self,period):
        """
        Write the measure statements to quantify the leakage power only. 
        """

        self.sf.write("\n* Measure statements for idle leakage power\n")

        # add measure statements for power
        t_initial = period
        t_final = 2*period
        self.stim.gen_meas_power(meas_name="LEAKAGE_POWER",
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

            (success, results)=self.run_delay_simulation(feasible_period,load,slew)
            if not success:
                feasible_period = 2 * feasible_period
                continue
            
            feasible_delay_lh = results["delay_lh"]
            feasible_slew_lh = results["slew_lh"]
            feasible_delay_hl = results["delay_hl"]
            feasible_slew_hl = results["slew_hl"]
            debug.info(1, "Found feasible_period: {0}ns feasible_delay_lh/0 {1}ns/{2}ns slew {3}ns/{4}ns".format(feasible_period,
                                                                                                                feasible_delay_lh,
                                                                                                                feasible_delay_hl,
                                                                                                                feasible_slew_lh,
                                                                                                                feasible_slew_hl))
            return (feasible_period, feasible_delay_lh, feasible_delay_hl)


    def run_delay_simulation(self, period, load, slew):
        """
        This tries to simulate a period and checks if the result works. If
        so, it returns True and the delays, slews, and powers.  It
        works on the trimmed netlist by default, so powers do not
        include leakage of all cells.
        """

        # Checking from not data_value to data_value
        self.write_delay_stimulus(period, load, slew)
        self.stim.run_sim()
        delay_hl = ch.parse_output("timing", "delay_hl")
        delay_lh = ch.parse_output("timing", "delay_lh")
        slew_hl = ch.parse_output("timing", "slew_hl")
        slew_lh = ch.parse_output("timing", "slew_lh")
        delays = (delay_hl, delay_lh, slew_hl, slew_lh)

        read0_power=ch.parse_output("timing", "read0_power")
        write0_power=ch.parse_output("timing", "write0_power")
        read1_power=ch.parse_output("timing", "read1_power")
        write1_power=ch.parse_output("timing", "write1_power")

        if not self.check_valid_delays(period, load, slew, delays):
            return (False,{})
            
        # For debug, you sometimes want to inspect each simulation.
        #key=raw_input("press return to continue")

        # Scale results to ns and mw, respectively
        result = { "delay_hl" : delay_hl*1e9,
                   "delay_lh" : delay_lh*1e9,
                   "slew_hl" : slew_hl*1e9,
                   "slew_lh" : slew_lh*1e9,
                   "read0_power" : read0_power*1e3,
                   "read1_power" : read1_power*1e3,
                   "write0_power" : write0_power*1e3,
                   "write1_power" : write1_power*1e3}
            
        # The delay is from the negative edge for our SRAM
        return (True,result)


    def run_power_simulation(self, period, load):
        """ 
        This simulates a disabled SRAM to get the leakage power when it is off.
        
        """

        self.write_power_stimulus(period, load, trim=False)
        self.stim.run_sim()
        leakage_power=ch.parse_output("timing", "leakage_power")
        debug.check(leakage_power!="Failed","Could not measure leakage power.")


        self.write_power_stimulus(period, load, trim=True)
        self.stim.run_sim()
        trim_leakage_power=ch.parse_output("timing", "leakage_power")
        debug.check(trim_leakage_power!="Failed","Could not measure leakage power.")

        # For debug, you sometimes want to inspect each simulation.
        #key=raw_input("press return to continue")
        return (leakage_power*1e3, trim_leakage_power*1e3)
    
    def check_valid_delays(self, period, load, slew, (delay_hl, delay_lh, slew_hl, slew_lh)):
        """ Check if the measurements are defined and if they are valid. """

        # if it failed or the read was longer than a period
        if type(delay_hl)!=float or type(delay_lh)!=float or type(slew_lh)!=float or type(slew_hl)!=float:
            debug.info(2,"Failed simulation: period {0} load {1} slew {2}, delay_hl={3} delay_lh={4} slew_hl={5} slew_lh={6}".format(period,
                                                                                                                                     load,
                                                                                                                                     slew,
                                                                                                                                     delay_hl,
                                                                                                                                     delay_lh,
                                                                                                                                     slew_hl,
                                                                                                                                     slew_lh))
            return False
        # Scale delays to ns (they previously could have not been floats)
        delay_hl *= 1e9
        delay_lh *= 1e9
        slew_hl *= 1e9
        slew_lh *= 1e9
        if delay_hl>period or delay_lh>period or slew_hl>period or slew_lh>period:
            debug.info(2,"UNsuccessful simulation: period {0} load {1} slew {2}, delay_hl={3}n delay_lh={4}ns slew_hl={5}n slew_lh={6}n".format(period,
                                                                                                                                            load,
                                                                                                                                            slew,
                                                                                                                                            delay_hl,
                                                                                                                                            delay_lh,
                                                                                                                                            slew_hl,
                                                                                                                                            slew_lh))
            return False
        else:
            debug.info(2,"Successful simulation: period {0} load {1} slew {2}, delay_hl={3}n delay_lh={4}ns slew_hl={5}n slew_lh={6}n".format(period,
                                                                                                                                          load,
                                                                                                                                          slew,
                                                                                                                                          delay_hl,
                                                                                                                                          delay_lh,
                                                                                                                                          slew_hl,
                                                                                                                                          slew_lh))

        return True
        

    def find_min_period(self,feasible_period, load, slew, feasible_delay_lh, feasible_delay_hl):
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

            if self.try_period(target_period, load, slew, feasible_delay_lh, feasible_delay_hl):
                ub_period = target_period
            else:
                lb_period = target_period

            if ch.relative_compare(ub_period, lb_period, error_tolerance=0.05):
                # ub_period is always feasible
                return ub_period


    def try_period(self, period, load, slew, feasible_delay_lh, feasible_delay_hl):
        """ 
        This tries to simulate a period and checks if the result
        works. If it does and the delay is within 5% still, it returns True.
        """

        # Checking from not data_value to data_value
        self.write_delay_stimulus(period,load,slew)
        self.stim.run_sim()
        delay_hl = ch.parse_output("timing", "delay_hl")
        delay_lh = ch.parse_output("timing", "delay_lh")
        slew_hl = ch.parse_output("timing", "slew_hl")
        slew_lh = ch.parse_output("timing", "slew_lh")
        # if it failed or the read was longer than a period
        if type(delay_hl)!=float or type(delay_lh)!=float or type(slew_lh)!=float or type(slew_hl)!=float:
            debug.info(2,"Invalid measures: Period {0}, delay_hl={1}ns, delay_lh={2}ns slew_hl={3}ns slew_lh={4}ns".format(period,
                                                                                                                       delay_hl,
                                                                                                                       delay_lh,
                                                                                                                       slew_hl,
                                                                                                                       slew_lh))
            return False
        delay_hl *= 1e9
        delay_lh *= 1e9
        slew_hl *= 1e9
        slew_lh *= 1e9
        if delay_hl>period or delay_lh>period or slew_hl>period or slew_lh>period:
            debug.info(2,"Too long delay/slew: Period {0}, delay_hl={1}ns, delay_lh={2}ns slew_hl={3}ns slew_lh={4}ns".format(period,
                                                                                                                          delay_hl,
                                                                                                                          delay_lh,
                                                                                                                          slew_hl,
                                                                                                                          slew_lh))
            return False
        else:
            if not ch.relative_compare(delay_lh,feasible_delay_lh,error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay_lh,feasible_delay_lh))
                return False
            elif not ch.relative_compare(delay_hl,feasible_delay_hl,error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay_hl,feasible_delay_hl))
                return False


        #key=raw_input("press return to continue")

        debug.info(2,"Successful period {0}, delay_hl={1}ns, delay_lh={2}ns slew_hl={3}ns slew_lh={4}ns".format(period,
                                                                                                            delay_hl,
                                                                                                            delay_lh,
                                                                                                            slew_hl,
                                                                                                            slew_lh))
        return True
    
    def set_probe(self,probe_address, probe_data):
        """ Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze."""
        self.probe_address = probe_address
        self.probe_data = probe_data

        self.prepare_netlist()
        

    def prepare_netlist(self):
        """ Prepare a trimmed netlist and regular netlist. """
        
        # Set up to trim the netlist here if that is enabled
        if OPTS.trim_netlist:
            self.trim_sp_file = "{}reduced.sp".format(OPTS.openram_temp)
            self.trimsp=trim_spice(self.sp_file, self.trim_sp_file)
            self.trimsp.set_configuration(self.num_banks,
                                          self.num_rows,
                                          self.num_cols,
                                          self.word_size)
            self.trimsp.trim(self.probe_address,self.probe_data)
        else:
            # The non-reduced netlist file when it is disabled
            self.trim_sp_file = "{}sram.sp".format(OPTS.openram_temp)
            
        # The non-reduced netlist file for power simulation 
        self.sim_sp_file = "{}sram.sp".format(OPTS.openram_temp)
        # Make a copy in temp for debugging
        shutil.copy(self.sp_file, self.sim_sp_file)



    def analyze(self,probe_address, probe_data, slews, loads):
        """
        Main function to characterize an SRAM for a table. Computes both delay and power characterization.
        """
        
        self.set_probe(probe_address, probe_data)

        # This is for debugging a full simulation
        # debug.info(0,"Debug simulation running...")
        # target_period=50.0
        # feasible_delay_lh=0.059083183
        # feasible_delay_hl=0.17953789
        # load=1.6728
        # slew=0.04
        # self.try_period(target_period, load, slew, feasible_delay_lh, feasible_delay_hl)
        # sys.exit(1)


        # 1) Find a feasible period and it's corresponding delays using the trimmed array.
        (feasible_period, feasible_delay_lh, feasible_delay_hl) = self.find_feasible_period(max(loads), max(slews))
        debug.check(feasible_delay_lh>0,"Negative delay may not be possible")
        debug.check(feasible_delay_hl>0,"Negative delay may not be possible")

        # 2) Measure the delay, slew and power for all slew/load pairs.
        # Make a list for each type of measurement to append results to
        char_data = {}
        for m in ["delay_lh", "delay_hl", "slew_lh", "slew_hl", "read0_power",
                  "read1_power", "write0_power", "write1_power", "leakage_power"]:
            char_data[m]=[]
        full_array_leakage = []
        trim_array_leakage = []        
        for load in loads:
            # 2a) Find the leakage power of the trimmmed and  UNtrimmed arrays.
            (full_leak, trim_leak)=self.run_power_simulation(feasible_period, load)
            full_array_leakage.append(full_leak)
            trim_array_leakage.append(trim_leak)
            for slew in slews:
                # 2c) Find the delay, dynamic power, and leakage power of the trimmed array.
                (success, delay_results) = self.run_delay_simulation(feasible_period, load, slew)
                debug.check(success,"Couldn't run a simulation. slew={0} load={1}\n".format(slew,load))
                for k,v in delay_results.items():
                    if "power" in k:
                        # Subtract partial array leakage and add full array leakage for the power measures
                        char_data[k].append(v - trim_array_leakage[-1] + full_array_leakage[-1])
                        char_data["leakage_power"].append(full_array_leakage[-1])
                    else:
                        char_data[k].append(v)


        # 3) Finds the minimum period without degrading the delays by X%
        min_period = self.find_min_period(feasible_period, max(loads), max(slews), feasible_delay_lh, feasible_delay_hl)
        debug.check(type(min_period)==float,"Couldn't find minimum period.")
        debug.info(1, "Min Period: {0}n with a delay of {1} / {2}".format(min_period, feasible_delay_lh, feasible_delay_hl))

        # 4) Pack up the final measurements
        char_data["min_period"] = ch.round_time(min_period)
        
        return char_data


    

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
        self.idle_cycle=len(self.cycle_times)-1        
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



    def analytical_delay(self,sram, slews, loads):
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
                delay_lh.append(bank_delay.delay/1e3)
                delay_hl.append(bank_delay.delay/1e3)
                slew_lh.append(bank_delay.slew/1e3)
                slew_hl.append(bank_delay.slew/1e3)
        
        data = {"min_period": 0, 
                "delay_lh": delay_lh,
                "delay_hl": delay_hl,
                "slew_lh": slew_lh,
                "slew_hl": slew_hl,
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
        self.stim.gen_pwl(sig_name, clk_times, values, period, slew, 0.05)

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
                self.stim.gen_pwl(sig_name, clk_times, ones_values, period, slew, 0.05)
            else:
                self.stim.gen_pwl(sig_name, clk_times, zero_values, period, slew, 0.05)


    def gen_csb(self, clk_times, period, slew):
        """ Generates the PWL CSb signal """
        # values for NOP, W1, W0, W1, R0, NOP, W1, W0, R1, NOP
        # Keep CSb asserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stim.gen_pwl("csb", clk_times, values, period, slew, 0.05)

    def gen_web(self, clk_times, period, slew):
        """ Generates the PWL WEb signal """
        # values for NOP, W1, W0, W1, R0, NOP, W1, W0, R1, NOP
        # Keep WEb deasserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1]
        self.stim.gen_pwl("web", clk_times, values, period, slew, 0.05)

        # Keep acc_en deasserted in NOP for measuring >1 period
        values = [1, 0, 0, 0, 1, 1, 0, 0, 1, 1]
        self.stim.gen_pwl("acc_en", clk_times, values, period, slew, 0)
        values = [0, 1, 1, 1, 0, 0, 1, 1, 0, 0]
        self.stim.gen_pwl("acc_en_inv", clk_times, values, period, slew, 0)
        
    def gen_oeb(self, clk_times, period, slew):
        """ Generates the PWL WEb signal """
        # values for NOP, W1, W0, W1, R0, W1, W0, R1, NOP
        # Keep OEb asserted in NOP for measuring >1 period
        values = [1, 1, 1, 1, 0, 0, 1, 1, 0, 0]
        self.stim.gen_pwl("oeb", clk_times, values, period, slew, 0.05)
