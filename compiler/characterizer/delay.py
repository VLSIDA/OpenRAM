import sys,re,shutil
import debug
import tech
import math
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS
from .simulation import simulation

class delay(simulation):
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
        simulation.__init__(self, sram, spfile, corner)

        # These are the member variables for a simulation
        self.targ_read_ports = []
        self.targ_write_ports = []
        self.period = 0
        self.set_load_slew(0,0)
        self.set_corner(corner)
        self.create_signal_names()
        
        #Create global measure names. Should maybe be an input at some point.
        self.create_measurement_names()
        
    def create_measurement_names(self):
        """Create measurement names. The names themselves currently define the type of measurement"""
        #Altering the names will crash the characterizer. TODO: object orientated approach to the measurements.
        self.delay_meas_names = ["delay_lh", "delay_hl", "slew_lh", "slew_hl"]
        self.power_meas_names = ["read0_power", "read1_power", "write0_power", "write1_power"]
        
    def create_signal_names(self):
        self.addr_name = "A"
        self.din_name = "DIN"
        self.dout_name = "DOUT"
        
        #This is TODO once multiport control has been finalized.
        #self.control_name = "CSB"
        
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
        self.stim.inst_sram(sram=self.sram,
                            port_signal_names=(self.addr_name,self.din_name,self.dout_name),
                            port_info=(len(self.all_ports),self.write_ports,self.read_ports),
                            abits=self.addr_size,
                            dbits=self.word_size,
                            sram_name=self.name)
        self.sf.write("\n* SRAM output loads\n")
        for port in self.read_ports:
            for i in range(self.word_size):
                self.sf.write("CD{0}{1} {2}{0}_{1} 0 {3}f\n".format(port,i,self.dout_name,self.load))
        

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

        self.sf.write("\n* Generation of Port clock signal\n")
        for port in self.all_ports:
            self.stim.gen_pulse(sig_name="CLK{0}".format(port),
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
                self.stim.gen_constant(sig_name="{0}{1}_{2} ".format(self.din_name,write_port, i),
                                    v_val=0)
        for port in self.all_ports:
            for i in range(self.addr_size):
                self.stim.gen_constant(sig_name="{0}{1}_{2}".format(self.addr_name,port, i),
                                       v_val=0)

        # generate control signals
        self.sf.write("\n* Generation of control signals\n")
        for port in self.all_ports:
            self.stim.gen_constant(sig_name="CSB{0}".format(port), v_val=self.vdd_voltage)
            if port in self.readwrite_ports:
                self.stim.gen_constant(sig_name="WEB{0}".format(port), v_val=self.vdd_voltage)

        self.sf.write("\n* Generation of global clock signal\n")
        for port in self.all_ports:
            self.stim.gen_constant(sig_name="CLK{0}".format(port), v_val=0)  
                          
        self.write_power_measures()

        # run until the end of the cycle time
        self.stim.write_control(2*self.period)

        self.sf.close()
        
    def get_delay_meas_values(self, delay_name, port):
        """Get the values needed to generate a Spice measurement statement based on the name of the measurement."""
        debug.check('lh' in delay_name or 'hl' in delay_name, "Measure command {0} does not contain direction (lh/hl)")
        trig_clk_name = "clk{0}".format(port)
        meas_name="{0}{1}".format(delay_name, port)
        targ_name = "{0}".format("{0}{1}_{2}".format(self.dout_name,port,self.probe_data))
        half_vdd = 0.5 * self.vdd_voltage
        trig_slew_low = 0.1 * self.vdd_voltage
        targ_slew_high = 0.9 * self.vdd_voltage
        if 'delay' in delay_name:
            trig_val = half_vdd
            targ_val = half_vdd
            trig_name = trig_clk_name
            if 'lh' in delay_name:
                trig_dir="RISE" 
                targ_dir="RISE"
                trig_td = targ_td = self.cycle_times[self.measure_cycles[port]["read1"]]
            else:
                trig_dir="FALL" 
                targ_dir="FALL"
                trig_td = targ_td = self.cycle_times[self.measure_cycles[port]["read0"]] 
                    
        elif 'slew' in delay_name:
            trig_name = targ_name
            if 'lh' in delay_name:
                trig_val = trig_slew_low
                targ_val = targ_slew_high
                targ_dir = trig_dir = "RISE"
                trig_td = targ_td = self.cycle_times[self.measure_cycles[port]["read1"]]
            else:
                trig_val = targ_slew_high 
                targ_val = trig_slew_low
                targ_dir = trig_dir = "FALL"
                trig_td = targ_td = self.cycle_times[self.measure_cycles[port]["read0"]] 
        else:
            debug.error(1, "Measure command {0} not recognized".format(delay_name))
        return (meas_name,trig_name,targ_name,trig_val,targ_val,trig_dir,targ_dir,trig_td,targ_td)
        
    def write_delay_measures_read_port(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """
        # add measure statements for delays/slews
        for dname in self.delay_meas_names:
            meas_values = self.get_delay_meas_values(dname, port)
            self.stim.gen_meas_delay(*meas_values)
            
        # add measure statements for power
        for pname in self.power_meas_names:
            if "read" not in pname:
                continue
            #Different naming schemes are used for the measure cycle dict and measurement names. 
            #TODO: make them the same so they can be indexed the same.
            if '1' in pname:
                t_initial = self.cycle_times[self.measure_cycles[port]["read1"]]
                t_final = self.cycle_times[self.measure_cycles[port]["read1"]+1]
            elif '0' in pname:
                t_initial = self.cycle_times[self.measure_cycles[port]["read0"]]
                t_final = self.cycle_times[self.measure_cycles[port]["read0"]+1]
            self.stim.gen_meas_power(meas_name="{0}{1}".format(pname, port),
                                     t_initial=t_initial,
                                     t_final=t_final)
       
    def write_delay_measures_write_port(self, port):
        """
        Write the measure statements to quantify the power results for a write port.
        """
        # add measure statements for power
        for pname in self.power_meas_names:
            if "write" not in pname:
                continue
            t_initial = self.cycle_times[self.measure_cycles[port]["write0"]]
            t_final = self.cycle_times[self.measure_cycles[port]["write0"]+1]
            if '1' in pname:
                t_initial = self.cycle_times[self.measure_cycles[port]["write1"]]
                t_final = self.cycle_times[self.measure_cycles[port]["write1"]+1]
        
            self.stim.gen_meas_power(meas_name="{0}{1}".format(pname, port),
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
        
        feasible_period = float(tech.spice["feasible_period"])
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
                continue
            
            #Positions of measurements currently hardcoded. First 2 are delays, next 2 are slews
            feasible_delays = [results[port][mname] for mname in self.delay_meas_names if "delay" in mname]
            feasible_slews = [results[port][mname] for mname in self.delay_meas_names if "slew" in mname]
            delay_str = "feasible_delay {0:.4f}ns/{1:.4f}ns".format(*feasible_delays)
            slew_str = "slew {0:.4f}ns/{1:.4f}ns".format(*feasible_slews)
            debug.info(2, "feasible_period passed for Port {3}: {0}ns {1} {2} ".format(feasible_period,
                                                                         delay_str,
                                                                         slew_str,
                                                                         port))
                
            if success:
                debug.info(2, "Found feasible_period for port {0}: {1}ns".format(port, feasible_period))
                self.period = feasible_period
                #Only return results related to input port.
                return results[port]

    def find_feasible_period(self):
        """
        Loops through all read ports determining the feasible period and collecting 
        delay information from each port.
        """
        feasible_delays = [{} for i in self.all_ports]
        
        #Get initial feasible delays from first port
        feasible_delays[self.read_ports[0]] = self.find_feasible_period_one_port(self.read_ports[0])
        previous_period = self.period
        
        
        #Loops through all the ports checks if the feasible period works. Everything restarts it if does not.
        #Write ports do not produce delays which is why they are not included here.
        i = 1
        while i < len(self.read_ports):
            port = self.read_ports[i]
            #Only extract port values from the specified port, not the entire results.
            feasible_delays[port].update(self.find_feasible_period_one_port(port))
            #Function sets the period. Restart the entire process if period changes to collect accurate delays 
            if self.period > previous_period:
                i = 0
            else:
                i+=1
            previous_period = self.period
        debug.info(1, "Found feasible_period: {0}ns".format(self.period))
        return feasible_delays
           
                
    def parse_values(self, values_names, port, mult = 1.0):
        """Parse multiple values in the timing output file. Optional multiplier.
           Return a dict of the input names and values. Port used for parsing file.
        """
        values = []
        all_values_floats = True
        for vname in values_names:
            #ngspice converts all measure characters to lowercase, not tested on other sims
            value = parse_spice_list("timing", "{0}{1}".format(vname.lower(), port)) 
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
        #Sanity Check
        debug.check(self.period > 0, "Target simulation period non-positive") 
        
        result = [{} for i in self.all_ports]
        # Checking from not data_value to data_value
        self.write_delay_stimulus()

        self.stim.run_sim()
        
        #Loop through all targeted ports and collect delays and powers. 
        #Too much duplicate code here. Try reducing
        for port in self.targ_read_ports:
            debug.info(2, "Check delay values for port {}".format(port))
            delay_names = [mname for mname in self.delay_meas_names]
            delays = self.parse_values(delay_names, port, 1e9) # scale delays to ns
            if not self.check_valid_delays(delays):
                return (False,{})
            result[port].update(delays)
            
            power_names = [mname for mname in self.power_meas_names if 'read' in mname]
            powers = self.parse_values(power_names, port, 1e3) # scale power to mw
            #Check that power parsing worked.
            for name, power in powers.items():
                if type(power)!=float:
                    debug.error("Failed to Parse Power Values:\n\t\t{0}".format(powers),1) #Printing the entire dict looks bad.
            result[port].update(powers)
        
        for port in self.targ_write_ports:
            power_names = [mname for mname in self.power_meas_names if 'write' in mname]
            powers = self.parse_values(power_names, port, 1e3) # scale power to mw
            #Check that power parsing worked.
            for name, power in powers.items():
                if type(power)!=float:
                    debug.error("Failed to Parse Power Values:\n\t\t{0}".format(powers),1) #Printing the entire dict looks bad.
            result[port].update(powers)
            
        # The delay is from the negative edge for our SRAM
        return (True,result)


    def run_power_simulation(self):
        """ 
        This simulates a disabled SRAM to get the leakage power when it is off.
        
        """
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
    
    def check_valid_delays(self, delay_dict):
        """ Check if the measurements are defined and if they are valid. """
        #Hard coded names currently
        delay_hl = delay_dict["delay_hl"]
        delay_lh = delay_dict["delay_lh"]
        slew_hl = delay_dict["slew_hl"]
        slew_lh = delay_dict["slew_lh"]
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
        half_period = self.period/2 #high-to-low delays start at neg. clk edge, so they need to be less than half_period
        if delay_hl>half_period or delay_lh>self.period or slew_hl>half_period or slew_lh>self.period:
            debug.info(2,"UNsuccessful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                              delays_str,
                                                                                              slews_str))
            return False
        else:
            debug.info(2,"Successful simulation (in ns):\n\t\t{0}\n\t\t{1}\n\t\t{2}".format(period_load_slew_str,
                                                                                            delays_str,
                                                                                            slews_str))

        return True
        
    def find_min_period(self, feasible_delays):
        """
        Determine a single minimum period for all ports.
        """
        
        feasible_period = ub_period = self.period
        lb_period = 0.0
        target_period = 0.5 * (ub_period + lb_period)
        
        #Find the minimum period for all ports. Start at one port and perform binary search then use that delay as a starting position.
        #For testing purposes, only checks read ports.
        for port in self.read_ports:
            target_period = self.find_min_period_one_port(feasible_delays, port, lb_period, ub_period, target_period)
            #The min period of one port becomes the new lower bound. Reset the upper_bound.
            lb_period = target_period
            ub_period = feasible_period        
        
        #Clear the target ports before leaving
        self.targ_read_ports = []
        self.targ_write_ports = []
        return target_period 
        
    def find_min_period_one_port(self, feasible_delays, port, lb_period, ub_period, target_period):
        """
        Searches for the smallest period with output delays being within 5% of 
        long period. For the current logic to characterize multiport, bounds are required as an input.
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

            if self.try_period(feasible_delays):
                ub_period = target_period
            else:
                lb_period = target_period

            if relative_compare(ub_period, lb_period, error_tolerance=0.05):
                # ub_period is always feasible.
                return ub_period
                
            #Update target
            target_period = 0.5 * (ub_period + lb_period)

        
    def try_period(self, feasible_delays):
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
            for dname in self.delay_meas_names: #check that the delays and slews do not degrade with tested period.
                if not relative_compare(results[port][dname],feasible_delays[port][dname],error_tolerance=0.05):
                    debug.info(2,"Delay too big {0} vs {1}".format(results[port][dname],feasible_delays[port][dname]))
                    return False

            #key=raw_input("press return to continue")
            
            #Dynamic way to build string. A bit messy though.
            delay_str = ', '.join("{0}={1}ns".format(mname, results[port][mname]) for mname in self.delay_meas_names)
            debug.info(2,"Successful period {0}, Port {2}, {1}".format(self.period,
                                                                       delay_str,
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
        #Dict to hold all characterization values
        char_sram_data = {}
        
        self.set_probe(probe_address, probe_data)
        
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
        
        # 1) Find a feasible period and it's corresponding delays using the trimmed array.
        feasible_delays = self.find_feasible_period()
        
        # 2) Finds the minimum period without degrading the delays by X%
        self.set_load_slew(max(loads),max(slews))
        min_period = self.find_min_period(feasible_delays)
        debug.check(type(min_period)==float,"Couldn't find minimum period.")
        debug.info(1, "Min Period Found: {0}ns".format(min_period))
        char_sram_data["min_period"] = round_time(min_period)

        # 3) Find the leakage power of the trimmmed and  UNtrimmed arrays.
        (full_array_leakage, trim_array_leakage)=self.run_power_simulation()
        char_sram_data["leakage_power"]=full_array_leakage
        leakage_offset = full_array_leakage - trim_array_leakage
        # 4) At the minimum period, measure the delay, slew and power for all slew/load pairs.
        self.period = min_period
        char_port_data = self.simulate_loads_and_slews(slews, loads, leakage_offset)
        
        #FIXME: low-to-high delays are altered to be independent of the period. This makes the lib results less accurate.
        self.alter_lh_char_data(char_port_data)
        
        return (char_sram_data, char_port_data)

    def alter_lh_char_data(self, char_port_data):
        """Copies high-to-low data to low-to-high data to make them consistent on the same clock edge."""
       #This is basically a hack solution which should be removed/fixed later.
        for port in self.all_ports:
            char_port_data[port]['delay_lh'] = char_port_data[port]['delay_hl']
            char_port_data[port]['slew_lh'] = char_port_data[port]['slew_hl']
        
    def simulate_loads_and_slews(self, slews, loads, leakage_offset):
        """Simulate all specified output loads and input slews pairs of all ports"""
        measure_data = self.get_empty_measure_data_dict()
        #Set the target simulation ports to all available ports. This make sims slower but failed sims exit anyways.        
        self.targ_read_ports = self.read_ports
        self.targ_write_ports = self.write_ports
        for slew in slews:
            for load in loads:
                self.set_load_slew(load,slew)
                # Find the delay, dynamic power, and leakage power of the trimmed array.
                (success, delay_results) = self.run_delay_simulation()
                debug.check(success,"Couldn't run a simulation. slew={0} load={1}\n".format(self.slew,self.load))
                debug.info(1, "Simulation Passed: Port {0} slew={1} load={2}".format("All", self.slew,self.load))
                #The results has a dict for every port but dicts can be empty (e.g. ports were not targeted).
                for port in self.all_ports:
                    for mname,value in delay_results[port].items():
                        if "power" in mname:
                            # Subtract partial array leakage and add full array leakage for the power measures
                            measure_data[port][mname].append(value + leakage_offset)
                        else:
                            measure_data[port][mname].append(value)
        return measure_data
    

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
        self.measure_cycles[write_port]["write0"] = len(self.cycle_times)-1
        
        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address 00..00 to set DOUT caps",
                      inverse_address,data_zeros,read_port) 

        self.add_read("R data 0 address 11..11 to check W0 worked",
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles[read_port]["read0"] = len(self.cycle_times)-1              
        
        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle)",
                      inverse_address,data_zeros)

        self.add_write("W data 1 address 11..11 to write value",
                       self.probe_address,data_ones,write_port)
        self.measure_cycles[write_port]["write1"] = len(self.cycle_times)-1

        self.add_write("W data 0 address 00..00 to clear DIN caps",
                       inverse_address,data_zeros,write_port)

        # This also ensures we will have a L->H transition on the next read
        self.add_read("R data 0 address 00..00 to clear DOUT caps",
                      inverse_address,data_zeros,read_port)
        
        self.add_read("R data 1 address 11..11 to check W1 worked",
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles[read_port]["read1"] = len(self.cycle_times)-1                
        
        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle))",
                      self.probe_address,data_zeros)
                      
    def get_available_port(self,get_read_port):
        """Returns the first accessible read or write port. """   
        if get_read_port and len(self.read_ports) > 0:
            return self.read_ports[0]
        elif not get_read_port and len(self.write_ports) > 0:
            return self.write_ports[0]
        return None
     
    def set_stimulus_variables(self):
        simulation.set_stimulus_variables(self)
        self.measure_cycles = [{} for port in self.all_ports]
        
    def create_test_cycles(self):
        """Returns a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation. The last time is the end of the simulation
        and does not need a rising edge."""
        #Using this requires setting at least one port to target for simulation.
        if len(self.targ_write_ports) == 0 and len(self.targ_read_ports) == 0:
            debug.error("No port selected for characterization.",1)
        self.set_stimulus_variables()
     
        #Get any available read/write port in case only a single write or read ports is being characterized.
        cur_read_port = self.get_available_port(get_read_port=True)   
        cur_write_port = self.get_available_port(get_read_port=False)          
        debug.check(cur_read_port != None, "Characterizer requires at least 1 read port")
        debug.check(cur_write_port != None, "Characterizer requires at least 1 write port")
        
        #Create test cycles for specified target ports.
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

    def analytical_delay(self, slews, loads):
        """ Return the analytical model results for the SRAM. 
        """
        if OPTS.num_rw_ports > 1 or OPTS.num_w_ports > 0 and OPTS.num_r_ports > 0:
            debug.warning("Analytical characterization results are not supported for multiport.")
        
        power = self.analytical_power(slews, loads)
        port_data = self.get_empty_measure_data_dict()
        for slew in slews:
            for load in loads:
                self.set_load_slew(load,slew)
                bank_delay = self.sram.analytical_delay(self.vdd_voltage, self.slew,self.load)
                for port in self.all_ports:
                    for mname in self.delay_meas_names+self.power_meas_names:
                        if "power" in mname:
                            port_data[port][mname].append(power.dynamic)
                        elif "delay" in mname:
                            port_data[port][mname].append(bank_delay[port].delay/1e3)
                        elif "slew" in mname:
                            port_data[port][mname].append(bank_delay[port].slew/1e3)
                        else:
                            debug.error("Measurement name not recognized: {}".format(mname),1)
        sram_data = { "min_period": 0, 
                      "leakage_power": power.leakage}                    
         
        return (sram_data,port_data)
        
    
    def analytical_power(self, slews, loads):
        """Get the dynamic and leakage power from the SRAM"""
        #slews unused, only last load is used
        load = loads[-1]
        power = self.sram.analytical_power(self.process, self.vdd_voltage, self.temperature, load) 
        #convert from nW to mW
        power.dynamic /= 1e6 
        power.leakage /= 1e6
        debug.info(1,"Dynamic Power: {0} mW".format(power.dynamic))        
        debug.info(1,"Leakage Power: {0} mW".format(power.leakage)) 
        return power
        
    def gen_data(self):
        """ Generates the PWL data inputs for a simulation timing test. """
        for write_port in self.write_ports:
            for i in range(self.word_size):
                sig_name="{0}{1}_{2} ".format(self.din_name,write_port, i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[write_port][i], self.period, self.slew, 0.05)

    def gen_addr(self):
        """ 
        Generates the address inputs for a simulation timing test. 
        This alternates between all 1's and all 0's for the address.
        """
        for port in self.all_ports:
            for i in range(self.addr_size):
                sig_name = "{0}{1}_{2}".format(self.addr_name,port,i)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][i], self.period, self.slew, 0.05)

    def gen_control(self):
        """ Generates the control signals """
        for port in self.all_ports:
            self.stim.gen_pwl("CSB{0}".format(port), self.cycle_times, self.csb_values[port], self.period, self.slew, 0.05)
            if port in self.readwrite_ports:
                self.stim.gen_pwl("WEB{0}".format(port), self.cycle_times, self.web_values[port], self.period, self.slew, 0.05)
        
            
    def get_empty_measure_data_dict(self):
        """Make a dict of lists for each type of delay and power measurement to append results to"""
        measure_names = self.delay_meas_names + self.power_meas_names
        #Create list of dicts. List lengths is # of ports. Each dict maps the measurement names to lists.
        measure_data = [{mname:[] for mname in measure_names} for i in self.all_ports]
        return measure_data
