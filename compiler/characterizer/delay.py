import sys,re,shutil
import debug
import tech
import math
from .stimuli import *
from .trim_spice import *
from .charutils import *
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

        # These are the member variables for a simulation
        self.period = 0
        self.set_load_slew(0,0)
        self.set_corner(corner)

    def set_corner(self,corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner
        
    def set_load_slew(self,load,slew):
        """ Set the load and slew """
        self.load = load
        self.slew = slew
        
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
        
        #Adding port options here which the characterizer cannot handle. Some may be added later like ROM
        if len(self.targ_write_ports) == 0 and len(self.targ_read_ports) == 0:
            debug.error("No ports selected for characterization.",1)
        if len(self.read_ports) == 0:
           debug.error("Characterizer does not currently support SRAMs without read ports.",1)
        if len(self.write_ports) == 0:
           debug.error("Characterizer does not currently support SRAMs without write ports.",1)

    def write_generic_stimulus(self):
        """ Create the instance, supplies, loads, and access transistors. """

        # add vdd/gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()

        # instantiate the sram
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_sram(abits=self.addr_size, 
                            dbits=self.word_size, 
                            port_info=(self.total_port_num,self.readwrite_port_num,self.read_ports,self.write_ports),
                            sram_name=self.name)

        self.sf.write("\n* SRAM output loads\n")
        for port in self.read_ports:
            for i in range(self.word_size):
                self.sf.write("CD{0}{1} DOUT{0}[{1}] 0 {2}f\n".format(port,i,self.load))
        

    def write_delay_stimulus(self):
        """ Creates a stimulus file for simulations to probe a bitcell at a given clock period.
        Address and bit were previously set with set_probe().
        Input slew (in ns) and output capacitive load (in fF) are required for charaterization.
        """
        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        self.create_test_cycles()

        # creates and opens stimulus file for writing
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Delay stimulus for period of {0}n load={1}fF slew={2}ns\n\n".format(self.period,
                                                                                             self.load,
                                                                                             self.slew))
        self.stim = stimuli(self.sf, self.corner)
        # include files in stimulus file
        self.stim.write_include(self.trim_sp_file)

        self.write_generic_stimulus()
        
        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        self.gen_data()
        self.gen_addr()


        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        self.gen_control()

        self.sf.write("\n* Generation of global clock signal\n")
        self.stim.gen_pulse(sig_name="CLK",
                            v1=0,
                            v2=self.vdd_voltage,
                            offset=self.period,
                            period=self.period,
                            t_rise=self.slew,
                            t_fall=self.slew)
                          
        self.write_delay_measures()

        # run until the end of the cycle time
        self.stim.write_control(self.cycle_times[-1] + self.period)

        self.sf.close()


    def write_power_stimulus(self, trim):
        """ Creates a stimulus file to measure leakage power only. 
        This works on the *untrimmed netlist*.
        """
        self.check_arguments()

        # obtains list of time-points for each rising clk edge
        #self.create_test_cycles()

        # creates and opens stimulus file for writing
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Power stimulus for period of {0}n\n\n".format(self.period))
        self.stim = stimuli(self.sf, self.corner)
        
        # include UNTRIMMED files in stimulus file
        if trim:
            self.stim.write_include(self.trim_sp_file)
        else:
            self.stim.write_include(self.sim_sp_file)
            
        self.write_generic_stimulus()
        
        # generate data and addr signals
        self.sf.write("\n* Generation of data and address signals\n")
        for write_port in self.write_ports:
            for i in range(self.word_size):
                self.stim.gen_constant(sig_name="DIN{0}[{1}] ".format(write_port, i),
                                    v_val=0)
        for port in range(self.total_port_num):
            for i in range(self.addr_size):
                self.stim.gen_constant(sig_name="A{0}[{1}]".format(port, i),
                                       v_val=0)

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        for port in range(self.total_port_num):
            self.stim.gen_constant(sig_name="CSB{0}".format(port), v_val=self.vdd_voltage)
            if port in self.read_ports and port in self.write_ports:
                self.stim.gen_constant(sig_name="WEB{0}".format(port), v_val=self.vdd_voltage)

        self.sf.write("\n* Generation of global clock signal\n")
        self.stim.gen_constant(sig_name="CLK", v_val=0)  
                          
        self.write_power_measures()

        # run until the end of the cycle time
        self.stim.write_control(2*self.period)

        self.sf.close()
        
    def write_delay_measures_read_port(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """

        # Trigger on the clk of the appropriate cycle
        trig_name = "clk"
        #Target name should be an input to the function or a member variable. That way, the ports can be singled out for testing
        targ_name = "{0}".format("DOUT{0}[{1}]".format(port,self.probe_data))
        trig_val = targ_val = 0.5 * self.vdd_voltage

        # Delay the target to measure after the negative edge
        self.stim.gen_meas_delay(meas_name="DELAY_HL{0}".format(port),
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="RISE",
                                 targ_dir="FALL",
                                 trig_td=self.cycle_times[self.measure_cycles["read0_{0}".format(port)]],
                                 targ_td=self.cycle_times[self.measure_cycles["read0_{0}".format(port)]])

        self.stim.gen_meas_delay(meas_name="DELAY_LH{0}".format(port),
                                 trig_name=trig_name,
                                 targ_name=targ_name,
                                 trig_val=trig_val,
                                 targ_val=targ_val,
                                 trig_dir="RISE",
                                 targ_dir="RISE",
                                 trig_td=self.cycle_times[self.measure_cycles["read1_{0}".format(port)]],
                                 targ_td=self.cycle_times[self.measure_cycles["read1_{0}".format(port)]])

        self.stim.gen_meas_delay(meas_name="SLEW_HL{0}".format(port),
                                 trig_name=targ_name,
                                 targ_name=targ_name,
                                 trig_val=0.9*self.vdd_voltage,
                                 targ_val=0.1*self.vdd_voltage,
                                 trig_dir="FALL",
                                 targ_dir="FALL",
                                 trig_td=self.cycle_times[self.measure_cycles["read0_{0}".format(port)]],
                                 targ_td=self.cycle_times[self.measure_cycles["read0_{0}".format(port)]])

        self.stim.gen_meas_delay(meas_name="SLEW_LH{0}".format(port),
                                 trig_name=targ_name,
                                 targ_name=targ_name,
                                 trig_val=0.1*self.vdd_voltage,
                                 targ_val=0.9*self.vdd_voltage,
                                 trig_dir="RISE",
                                 targ_dir="RISE",
                                 trig_td=self.cycle_times[self.measure_cycles["read1_{0}".format(port)]],
                                 targ_td=self.cycle_times[self.measure_cycles["read1_{0}".format(port)]])
        
        # add measure statements for power
        t_initial = self.cycle_times[self.measure_cycles["read0_{0}".format(port)]]
        t_final = self.cycle_times[self.measure_cycles["read0_{0}".format(port)]+1]
        self.stim.gen_meas_power(meas_name="READ0_POWER{0}".format(port),
                                 t_initial=t_initial,
                                 t_final=t_final)

        t_initial = self.cycle_times[self.measure_cycles["read1_{0}".format(port)]]
        t_final = self.cycle_times[self.measure_cycles["read1_{0}".format(port)]+1]
        self.stim.gen_meas_power(meas_name="READ1_POWER{0}".format(port),
                                 t_initial=t_initial,
                                 t_final=t_final)
        
    def write_delay_measures_write_port(self, port):
        """
        Write the measure statements to quantify the power results for a write port.
        """
        # add measure statements for power
        t_initial = self.cycle_times[self.measure_cycles["write0_{0}".format(port)]]
        t_final = self.cycle_times[self.measure_cycles["write0_{0}".format(port)]+1]
        self.stim.gen_meas_power(meas_name="WRITE0_POWER{0}".format(port),
                                 t_initial=t_initial,
                                 t_final=t_final)

        t_initial = self.cycle_times[self.measure_cycles["write1_{0}".format(port)]]
        t_final = self.cycle_times[self.measure_cycles["write1_{0}".format(port)]+1]
        self.stim.gen_meas_power(meas_name="WRITE1_POWER{0}".format(port),
                                 t_initial=t_initial,
                                 t_final=t_final)

    def write_delay_measures(self):
        """
        Write the measure statements to quantify the delay and power results for all targeted ports.
        """
        self.sf.write("\n* Measure statements for delay and power\n")

        # Output some comments to aid where cycles start and
        # what is happening
        for comment in self.cycle_comments:
            self.sf.write("* {}\n".format(comment))
            
        for read_port in self.targ_read_ports:
           self.write_delay_measures_read_port(read_port)
        for write_port in self.targ_write_ports:
           self.write_delay_measures_write_port(write_port)
        
                                 
    def write_power_measures(self):
        """
        Write the measure statements to quantify the leakage power only. 
        """

        self.sf.write("\n* Measure statements for idle leakage power\n")

        # add measure statements for power
        t_initial = self.period
        t_final = 2*self.period
        self.stim.gen_meas_power(meas_name="leakage_power",
                                 t_initial=t_initial,
                                 t_final=t_final)
        
    def find_feasible_period_one_port(self, port):
        """
        Uses an initial period and finds a feasible period before we
        run the binary search algorithm to find min period. We check if
        the given clock period is valid and if it's not, we continue to
        double the period until we find a valid period to use as a
        starting point. 
        """
        debug.check(port in self.read_ports, "Characterizer requires a read port to determine a period.")
        #Adding this as a sanity check for editing this function later. This function assumes period has been set previously
        debug.check(self.period > 0, "Initial starting period not defined") 
        feasible_period = float(tech.spice["feasible_period"])
        #feasible_period = float(2.5)#What happens if feasible starting point is wrong?
        time_out = 9
        while True:
            time_out -= 1
            if (time_out <= 0):
                debug.error("Timed out, could not find a feasible period.",2)
            
            #Clear any write target ports and set read port
            self.targ_write_ports = []
            self.targ_read_ports = [port]
            success = False
           
            debug.info(1, "Trying feasible period: {0}ns on Port {1}".format(feasible_period, port))
            self.period = feasible_period
            (success, results)=self.run_delay_simulation()
            #Clear these target ports after simulation
            self.targ_read_ports = []
            
            if not success:
                feasible_period = 2 * feasible_period
                break
            feasible_delay_lh = results["delay_lh{0}".format(port)]
            feasible_delay_hl = results["delay_hl{0}".format(port)]
            feasible_slew_lh = results["slew_lh{0}".format(port)]
            feasible_slew_hl = results["slew_hl{0}".format(port)]

            delay_str = "feasible_delay {0:.4f}ns/{1:.4f}ns".format(feasible_delay_lh, feasible_delay_hl)
            slew_str = "slew {0:.4f}ns/{1:.4f}ns".format(feasible_slew_lh, feasible_slew_hl)
            debug.info(2, "feasible_period passed for Port {3}: {0}ns {1} {2} ".format(feasible_period,
                                                                         delay_str,
                                                                         slew_str,
                                                                         port))
            #Add feasible delays of port to dict
            #feasible_delays_lh[port] = feasible_delay_lh
            #feasible_delays_hl[port] = feasible_delay_hl
                
            if success:
                debug.info(1, "Found feasible_period: {0}ns".format(feasible_period))
                self.period = feasible_period
                return (feasible_delay_lh, feasible_delay_hl)

    def find_feasible_period(self):
        """
        Loops through all read ports determining the feasible period and collecting 
        delay information from each port.
        """
        feasible_delays_lh = {}
        feasible_delays_hl = {}
        self.period = float(tech.spice["feasible_period"])
        
        #Get initial feasible period from first port
        (feasible_delays_lh[0], feasible_delays_hl[0]) = self.find_feasible_period_one_port(self.read_ports[0])
        previous_period = self.period
        
        
        #Loops through all the ports checks if the feasible period works. Everything restarts it if does not.
        #Write ports do not produce delays which is why they are not included here.
        i = 1
        while i < len(self.read_ports):
            port = self.read_ports[i]
            (feasible_delays_lh[port], feasible_delays_hl[port]) = self.find_feasible_period_one_port(port)
            #Function sets the period. Restart the entire process if period changes to collect accurate delays 
            if self.period > previous_period:
                i = 0
            else:
                i+=1
            previous_period = self.period
        return (feasible_delays_lh, feasible_delays_hl)
           
                
    def parse_values(self, values_names, mult = 1.0):
        """Parse multiple values in the timing output file. Optional multiplier."""
        values = []
        all_values_floats = True
        for vname in values_names:
            #ngspice converts all measure characters to lowercase, not tested on other sims
            value = parse_spice_list("timing", vname.lower()) 
            #Check if any of the values fail to parse
            if type(value)!=float: 
                all_values_floats = False
            values.append(value)
            
        #Apply Multiplier only if all values are floats. Let other check functions handle this error.
        if all_values_floats:
            return {values_names[i]:values[i]*mult for i in range(len(values))}
        else:
            return {values_names[i]:values[i] for i in range(len(values))}
            
    def run_delay_simulation(self):
        """
        This tries to simulate a period and checks if the result works. If
        so, it returns True and the delays, slews, and powers.  It
        works on the trimmed netlist by default, so powers do not
        include leakage of all cells.
        """
        result = {}
        # Checking from not data_value to data_value
        self.write_delay_stimulus()

        self.stim.run_sim()
        
        #Loop through all targeted ports and collect delays and powers. 
        #Too much duplicate code here. Try reducing
        for port in self.targ_read_ports:
            delay_names = ["delay_hl{0}".format(port), "delay_lh{0}".format(port),
                           "slew_hl{0}".format(port), "slew_lh{0}".format(port)]
            delays = self.parse_values(delay_names, 1e9) # scale delays to ns
            if not self.check_valid_delays((delays[delay_names[0]],delays[delay_names[1]],delays[delay_names[2]],delays[delay_names[3]])):
                return (False,{})
            result.update(delays)
            
            power_names = ["read0_power{0}".format(port), "read1_power{0}".format(port)]
            powers = self.parse_values(power_names, 1e3) # scale power to mw
            #Check that power parsing worked.
            for name, power in powers.items():
                if type(power)!=float:
                    debug.error("Failed to Parse Power Values:\n\t\t{0}".format(powers),1) #Printing the entire dict looks bad.
            result.update(powers)
        
        for port in self.targ_write_ports:
            power_names = ["write0_power{0}".format(port), "write1_power{0}".format(port)]
            powers = self.parse_values(power_names, 1e3) # scale power to mw
            #Check that power parsing worked.
            for name, power in powers.items():
                if type(power)!=float:
                    debug.error("Failed to Parse Power Values:\n\t\t{0}".format(powers),1) #Printing the entire dict looks bad.
            result.update(powers)
            
        # The delay is from the negative edge for our SRAM
        return (True,result)


    def run_power_simulation(self):
        """ 
        This simulates a disabled SRAM to get the leakage power when it is off.
        
        """
        #Select any available port. Does not need to be specified for leakage power.
        #Doing this just passes a debug check and nothing else. Put on TODO to remove...
        self.targ_read_ports = [self.get_available_port(get_read_port=True)]
        
        debug.info(1, "Performing leakage power simulations.")
        self.write_power_stimulus(trim=False)
        self.stim.run_sim()
        leakage_power=parse_spice_list("timing", "leakage_power")
        debug.check(leakage_power!="Failed","Could not measure leakage power.")
        debug.info(1, "Leakage power of full array is {0} mW".format(leakage_power*1e3))
        #debug
        #sys.exit(1)

        self.write_power_stimulus(trim=True)
        self.stim.run_sim()
        trim_leakage_power=parse_spice_list("timing", "leakage_power")
        debug.check(trim_leakage_power!="Failed","Could not measure leakage power.")
        debug.info(1, "Leakage power of trimmed array is {0} mW".format(trim_leakage_power*1e3))
        
        # For debug, you sometimes want to inspect each simulation.
        #key=raw_input("press return to continue")
        return (leakage_power*1e3, trim_leakage_power*1e3)
    
    def check_valid_delays(self, delay_tuple):
        """ Check if the measurements are defined and if they are valid. """

        (delay_hl, delay_lh, slew_hl, slew_lh) = delay_tuple
        period_load_slew_str = "period {0} load {1} slew {2}".format(self.period,self.load, self.slew)
        
        # if it failed or the read was longer than a period
        if type(delay_hl)!=float or type(delay_lh)!=float or type(slew_lh)!=float or type(slew_hl)!=float:
            delays_str = "delay_hl={0} delay_lh={1}".format(delay_hl, delay_lh)
            slews_str = "slew_hl={0} slew_lh={1}".format(slew_hl,slew_lh)
            debug.info(2,"Failed simulation (in sec):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                         delays_str,
                                                                                         slews_str))
            return False
            
        delays_str = "delay_hl={0} delay_lh={1}".format(delay_hl, delay_lh)
        slews_str = "slew_hl={0} slew_lh={1}".format(slew_hl,slew_lh)
        if delay_hl>self.period or delay_lh>self.period or slew_hl>self.period or slew_lh>self.period:
            debug.info(2,"UNsuccessful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                              delays_str,
                                                                                              slews_str))
            return False
        else:
            debug.info(2,"Successful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                            delays_str,
                                                                                            slews_str))

        return True
        
    def find_min_period(self, feasible_delays_lh, feasible_delays_hl):
        """
        Determine the minimum period for all ports.
        """

        feasible_period = ub_period = self.period
        lb_period = 0.0
        target_period = 0.5 * (ub_period + lb_period)
        
        #Find the minimum period for all ports. Start at one port and perform binary search then use that delay as a starting position.
        #For testing purposes, only checks read ports.
        for port in self.read_ports:
            target_period = self.find_min_period_one_port(feasible_delays_lh, feasible_delays_hl, port, lb_period, ub_period, target_period)
            #The min period of one port becomes the new lower bound. Reset the upper_bound.
            lb_period = target_period
            ub_period = feasible_period        
        
        #Clear the target ports before leaving
        self.targ_read_ports = []
        self.targ_write_ports = []
        return target_period 
        
    def find_min_period_one_port(self, feasible_delays_lh, feasible_delays_hl, port, lb_period, ub_period, target_period):
        """
        Searches for the smallest period with output delays being within 5% of 
        long period. For the current logic to characterize multiport, bound are required as an input.
        """

        #previous_period = ub_period = self.period
        #ub_period = self.period
        #lb_period = 0.0
        #target_period = 0.5 * (ub_period + lb_period)
        
        # Binary search algorithm to find the min period (max frequency) of input port
        time_out = 25
        self.targ_read_ports = [port]
        while True:
            time_out -= 1
            if (time_out <= 0):
                debug.error("Timed out, could not converge on minimum period.",2)

            self.period = target_period
            debug.info(1, "MinPeriod Search Port {3}: {0}ns (ub: {1} lb: {2})".format(target_period,
                                                                             ub_period,
                                                                             lb_period,
                                                                             port))

            if self.try_period(feasible_delays_lh, feasible_delays_hl):
                ub_period = target_period
            else:
                lb_period = target_period

            if relative_compare(ub_period, lb_period, error_tolerance=0.05):
                # ub_period is always feasible. When done with a port, set the target period of the next port as the lower bound
                # and reset the upperbound
                return ub_period
                #target_period = lb_period = ub_period
                #ub_period = previous_period
                #break
            
            #Update target
            target_period = 0.5 * (ub_period + lb_period)

        
    def try_period(self, feasible_delays_lh, feasible_delays_hl):
        """ 
        This tries to simulate a period and checks if the result
        works. If it does and the delay is within 5% still, it returns True.
        """
        # Run Delay simulation but Power results not used.
        (success, results) = self.run_delay_simulation()
        if not success:
            return False
        
        #Check the values of target readwrite and read ports. Write ports do not produce delays in this current version
        for port in self.targ_read_ports:
            delay_hl = results["delay_hl{0}".format(port)]
            delay_lh = results["delay_lh{0}".format(port)]
            slew_hl = results["slew_hl{0}".format(port)]
            slew_lh = results["slew_lh{0}".format(port)]

            if not relative_compare(delay_lh,feasible_delays_lh[port],error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay_lh,feasible_delays_lh[port]))
                return False
            elif not relative_compare(delay_hl,feasible_delays_hl[port],error_tolerance=0.05):
                debug.info(2,"Delay too big {0} vs {1}".format(delay_hl,feasible_delays_hl[port]))
                return False

            #key=raw_input("press return to continue")

            debug.info(2,"Successful period {0}, Port {5}, delay_hl={1}ns, delay_lh={2}ns slew_hl={3}ns slew_lh={4}ns".format(self.period,
                                                                                                                    delay_hl,
                                                                                                                    delay_lh,
                                                                                                                    slew_hl,
                                                                                                                    slew_lh,
                                                                                                                    port))
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
        
        self.create_port_names()
        
        self.create_char_data_dict()
        
        self.load=max(loads)
        self.slew=max(slews)
        # This is for debugging a full simulation
        # debug.info(0,"Debug simulation running...")
        # target_period=50.0
        # feasible_delay_lh=0.059083183
        # feasible_delay_hl=0.17953789
        # load=1.6728
        # slew=0.04
        # self.try_period(target_period, feasible_delay_lh, feasible_delay_hl)
        # sys.exit(1)

        #For debugging, skips characterization and returns dummy values.
        # i = 1.0
        # for slew in slews:
            # for load in loads:
                # for k,v in char_data.items():        
                    # char_data[k].append(i)
                    # i+=1.0
        # char_data["min_period"] = i
        # char_data["leakage_power"] = i+1.0
        # return char_data
        
        # 1) Find a feasible period and it's corresponding delays using the trimmed array.
        (feasible_delays_lh, feasible_delays_hl) = self.find_feasible_period()
        #Check all the delays
        for k,v in feasible_delays_lh.items():
            debug.check(v>0,"Negative delay may not be possible")
        for k,v in feasible_delays_hl.items():
            debug.check(v>0,"Negative delay may not be possible")

        
        # 2) Finds the minimum period without degrading the delays by X%
        self.set_load_slew(max(loads),max(slews))
        min_period = self.find_min_period(feasible_delays_lh, feasible_delays_hl)
        debug.check(type(min_period)==float,"Couldn't find minimum period.")
        debug.info(1, "Min Period Found: {0}ns".format(min_period))
        self.char_data["min_period"] = round_time(min_period)

        # 3) Find the leakage power of the trimmmed and  UNtrimmed arrays.
        (full_array_leakage, trim_array_leakage)=self.run_power_simulation()
        self.char_data["leakage_power"]=full_array_leakage
        leakage_offset = full_array_leakage - trim_array_leakage
        
        # 4) At the minimum period, measure the delay, slew and power for all slew/load pairs.
        self.simulate_loads_and_slews(slews, loads, leakage_offset)

        return self.char_data

    def simulate_loads_and_slews(self, slews, loads, leakage_offset):
        """Simulate all specified output loads and input slews pairs"""
        #Set the target simulation ports to all available ports. This make sims slower but failed sims exit anyways.
        self.targ_read_ports = self.read_ports
        self.targ_write_ports = self.write_ports
        for slew in slews:
            for load in loads:
                self.set_load_slew(load,slew)
                # Find the delay, dynamic power, and leakage power of the trimmed array.
                (success, delay_results) = self.run_delay_simulation()
                debug.check(success,"Couldn't run a simulation. slew={0} load={1}\n".format(self.slew,self.load))
                for k,v in delay_results.items():
                    if "power" in k:
                        # Subtract partial array leakage and add full array leakage for the power measures
                        self.char_data[k].append(v + leakage_offset)
                    else:
                        self.char_data[k].append(v)
                        
    def add_data(self, data, port):
        """ Add the array of data values """
        debug.check(len(data)==self.word_size, "Invalid data word size.")
        debug.check(port < len(self.data_values), "Port number cannot index data values.")
        index = 0
        for c in data:
            if c=="0":
                self.data_values[port][index].append(0)
            elif c=="1":
                self.data_values[port][index].append(1)
            else:
                debug.error("Non-binary data string",1)
            index += 1

    def add_address(self, address, port):
        """ Add the array of address values """
        debug.check(len(address)==self.addr_size, "Invalid address size.")
        index = 0
        for c in address:
            if c=="0":
                self.addr_values[port][index].append(0)
            elif c=="1":
                self.addr_values[port][index].append(1)
            else:
                debug.error("Non-binary address string",1)
            index += 1
    
    def add_noop_one_port(self, address, data, port):
        """ Add the control values for a noop to a single port. """
        #This is to be used as a helper function for the other add functions. Cycle and comments are omitted.    
        self.csb_values[port].append(1)
        #If port is in both lists, add rw control signal. Condition indicates its a RW port.
        if port < len(self.web_values):
            self.web_values[port].append(1)
        
        if port in self.write_ports:
            self.add_data(data,port)
        self.add_address(address, port)
    
    def add_noop_all_ports(self, comment, address, data):
        """ Add the control values for a noop to all ports. """
        self.cycle_comments.append("Cycle {0:2d}\tPort All\t{1:5.2f}ns:\t{2}".format(len(self.cycle_times),
                                                                           self.t_current,
                                                                           comment))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
         
        for port in range(self.total_port_num):
            self.add_noop_one_port(address, data, port)
        
                 
    def add_read(self, comment, address, data, port):
        """ Add the control values for a read cycle. """
        debug.check(port in self.read_ports, "Cannot add read cycle to a write port.")
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                           self.t_current,
                                                                           comment,
                                                                           port))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.csb_values[port].append(0)
        #If port is in both lists, add rw control signal. Condition indicates its a RW port.
        if port < len(self.web_values):
            self.web_values[port].append(1)
        
        #If the port is also a readwrite then add data.
        if port in self.write_ports:
            self.add_data(data,port)
        self.add_address(address, port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in range(self.total_port_num):
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, unselected_port)

    def add_write(self, comment, address, data, port):
        """ Add the control values for a write cycle. """
        debug.check(port in self.write_ports, "Cannot add read cycle to a read port.")
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                           self.t_current,
                                                                           comment,
                                                                           port))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.csb_values[port].append(0)
        #If port is in both lists, add rw control signal. Condition indicates its a RW port.
        if port < len(self.web_values):
            self.web_values[port].append(0)
   
        self.add_data(data,port)
        self.add_address(address,port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in range(self.total_port_num):
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, unselected_port)
    
    def gen_test_cycles_one_port(self, read_port, write_port):
        """Intended but not implemented: Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation of a single port. Current: Values overwritten for multiple calls"""

        # Create the inverse address for a scratch address
        inverse_address = ""
        for c in self.probe_address:
            if c=="0":
                inverse_address += "1"
            elif c=="1":
                inverse_address += "0"
            else:
                debug.error("Non-binary address string",1)

        # For now, ignore data patterns and write ones or zeros
        data_ones = "1"*self.word_size
        data_zeros = "0"*self.word_size
        
        if self.t_current == 0:
            self.add_noop_all_ports("Idle cycle (no positive clock edge)",
                      inverse_address, data_zeros)
        
        self.add_write("W data 1 address 0..00",
                       inverse_address,data_ones,write_port) 

        self.add_write("W data 0 address 11..11 to write value",
                       self.probe_address,data_zeros,write_port)
        self.measure_cycles["write0_{0}".format(write_port)] = len(self.cycle_times)-1
        #self.write0_cycle=len(self.cycle_times)-1 # Remember for power measure
        
        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address 00..00 to set DOUT caps",
                      inverse_address,data_zeros,read_port) 

        self.add_read("R data 0 address 11..11 to check W0 worked",
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles["read0_{0}".format(read_port)] = len(self.cycle_times)-1              
        #self.read0_cycle=len(self.cycle_times)-1 # Remember for power measure
        
        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle)",
                      inverse_address,data_zeros)
        #Does not seem like is is used anywhere commenting out for now.
        #self.idle_cycle=len(self.cycle_times)-1 # Remember for power measure

        self.add_write("W data 1 address 11..11 to write value",
                       self.probe_address,data_ones,write_port)
        self.measure_cycles["write1_{0}".format(write_port)] = len(self.cycle_times)-1
        #self.write1_cycle=len(self.cycle_times)-1 # Remember for power measure

        self.add_write("W data 0 address 00..00 to clear DIN caps",
                       inverse_address,data_zeros,write_port)

        # This also ensures we will have a L->H transition on the next read
        self.add_read("R data 0 address 00..00 to clear DOUT caps",
                      inverse_address,data_zeros,read_port)
        
        self.add_read("R data 1 address 11..11 to check W1 worked",
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles["read1_{0}".format(read_port)] = len(self.cycle_times)-1                
        #self.read1_cycle=len(self.cycle_times)-1 # Remember for power measure
        
        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle))",
                      self.probe_address,data_zeros)
                      
    def get_available_port(self,get_read_port):
        """Returns the first accessible read or write port. """   
        if get_read_port and len(self.read_ports) > 0:
            return self.read_ports[0]
        elif not get_read_port and len(self.write_ports) > 0:
            return self.write_ports[0]
        return None
        
    def create_test_cycles(self):
        """Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation. The last time is the end of the simulation
        and does not need a rising edge."""

        # Start at time 0
        self.t_current = 0

        # Cycle times (positive edge) with comment
        self.cycle_comments = [] 
        self.cycle_times = []
        self.measure_cycles = {}

        # Control signals for ports. These are not the final signals and will likely be changed later.
        #write enable bar for readwrite ports to control read or write
        self.web_values = [[] for i in range(self.readwrite_port_num)]
        #csb represents a basic "enable" signal that all ports have.
        self.csb_values = [[] for i in range(self.total_port_num)]
        
        # Address and data values for each address/data bit. A dict of 3d lists of size #ports x bits x cycles.
        self.data_values=[[[] for i in range(self.addr_size)]]*len(self.read_ports) 
        self.addr_values=[[[] for i in range(self.addr_size)]]*self.total_port_num 
        
        #Get any available read/write port in case only a single write or read ports is being characterized.
        cur_read_port = self.get_available_port(get_read_port=True)   
        cur_write_port = self.get_available_port(get_read_port=False)          
        
        #These checks should be superceded by check_arguments which should have been called earlier, so this is a double check.
        debug.check(cur_read_port != None, "Characterizer requires at least 1 read port")
        debug.check(cur_write_port != None, "Characterizer requires at least 1 write port")
        
        #Characterizing the remaining target ports. Not the final design.
        write_pos = 0
        read_pos = 0
        while True:
            #Exit when all ports have been characterized
            if write_pos >= len(self.targ_write_ports) and read_pos >= len(self.targ_read_ports):
                break
                
            #Select new write and/or read ports for the next cycle. Use previous port if none remaining.
            if write_pos < len(self.targ_write_ports):
                cur_write_port = self.targ_write_ports[write_pos]
                write_pos+=1
            if read_pos < len(self.targ_read_ports):
                cur_read_port = self.targ_read_ports[read_pos]
                read_pos+=1
            
            #Add test cycle of read/write port pair. One port could have been used already, but the other has not.
            self.gen_test_cycles_one_port(cur_read_port, cur_write_port)

    def analytical_delay(self,sram, slews, loads):
        """ Return the analytical model results for the SRAM. 
        """
        debug.check(OPTS.num_rw_ports < 2 and OPTS.num_w_ports < 1 and OPTS.num_r_ports < 1 ,
                    "Analytical characterization does not currently support multiport.")
        
        delay_lh = []
        delay_hl = []
        slew_lh = []
        slew_hl = []
        for slew in slews:
            for load in loads:
                self.set_load_slew(load,slew)
                bank_delay = sram.analytical_delay(self.slew,self.load)
                # Convert from ps to ns
                delay_lh.append(bank_delay.delay/1e3)
                delay_hl.append(bank_delay.delay/1e3)
                slew_lh.append(bank_delay.slew/1e3)
                slew_hl.append(bank_delay.slew/1e3)
        
        power = sram.analytical_power(self.process, self.vdd_voltage, self.temperature, load) 
        #convert from nW to mW
        power.dynamic /= 1e6 
        power.leakage /= 1e6
        debug.info(1,"Dynamic Power: {0} mW".format(power.dynamic))        
        debug.info(1,"Leakage Power: {0} mW".format(power.leakage)) 
        
        data = {"min_period": 0, 
                "delay_lh0": delay_lh,
                "delay_hl0": delay_hl,
                "slew_lh0": slew_lh,
                "slew_hl0": slew_hl,
                "read0_power0": power.dynamic,
                "read1_power0": power.dynamic,
                "write0_power0": power.dynamic,
                "write1_power0": power.dynamic,
                "leakage_power": power.leakage
                }
        return data

    def gen_data(self):
        """ Generates the PWL data inputs for a simulation timing test. """
        for read_port in self.read_ports:
            for i in range(self.word_size):
                sig_name="DIN{0}[{1}] ".format(read_port, i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[read_port][i], self.period, self.slew, 0.05)

    def gen_addr(self):
        """ 
        Generates the address inputs for a simulation timing test. 
        This alternates between all 1's and all 0's for the address.
        """
        for port in range(self.total_port_num):
            for i in range(self.addr_size):
                sig_name = "A{0}[{1}]".format(port,i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][i], self.period, self.slew, 0.05)

    def gen_control(self):
        """ Generates the control signals """
        for port in range(self.total_port_num):
            self.stim.gen_pwl("CSB{0}".format(port), self.cycle_times, self.csb_values[port], self.period, self.slew, 0.05)
        
        for readwrite_port in range(self.readwrite_port_num):
            self.stim.gen_pwl("WEB{0}".format(readwrite_port), self.cycle_times, self.web_values[readwrite_port], self.period, self.slew, 0.05)
            

    def create_port_names(self):
        """Generates the port names to be used in characterization and sets default simulation target ports"""
        self.write_ports = []
        self.read_ports = []
        self.total_port_num = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
        
        #save a member variable to avoid accessing global. readwrite ports have different control signals.
        self.readwrite_port_num = OPTS.num_rw_ports
        
        #Generate the port names. readwrite ports are required to be added first for this to work.
        for readwrite_port_num in range(OPTS.num_rw_ports):
            self.read_ports.append(readwrite_port_num)
            self.write_ports.append(readwrite_port_num)
        #This placement is intentional. It makes indexing input data easier. See self.data_values
        for read_port_num in range(OPTS.num_rw_ports, OPTS.num_r_ports):
            self.read_ports.append(read_port_num)
        for write_port_num in range(OPTS.num_rw_ports+OPTS.num_r_ports, OPTS.num_w_ports):
            self.write_ports.append(write_port_num)
        
        
        #Set the default target ports for simulation. Default is all the ports.
        self.targ_read_ports = self.read_ports
        self.targ_write_ports = self.write_ports
    
    def create_char_data_dict(self):
        """Make a dict of lists for each type of measurement to append results to"""
        #Making this a member variable may not be the best option, but helps reduce code clutter
        self.char_data = {}
        for port in range(self.total_port_num):
            for m in ["delay_lh", "delay_hl", "slew_lh", "slew_hl", "read0_power",
                    "read1_power", "write0_power", "write1_power"]:
                self.char_data ["{0}{1}".format(m,port)]=[]