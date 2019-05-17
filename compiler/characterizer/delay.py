# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import sys,re,shutil,copy
import debug
import tech
import math
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS
from .simulation import simulation
from .measurements import *
import logical_effort
import graph_util

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
        self.add_graph_exclusions()
        
    def create_measurement_names(self):
        """Create measurement names. The names themselves currently define the type of measurement"""
        #Altering the names will crash the characterizer. TODO: object orientated approach to the measurements.
        self.delay_meas_names = ["delay_lh", "delay_hl", "slew_lh", "slew_hl"]
        self.power_meas_names = ["read0_power", "read1_power", "write0_power", "write1_power"]
        #self.voltage_when_names = ["volt_bl", "volt_br"]
        #self.bitline_delay_names = ["delay_bl", "delay_br"]
       
    def create_measurement_objects(self):
        """Create the measurements used for read and write ports"""
        self.read_meas_lists = self.create_read_port_measurement_objects()
        self.write_meas_lists = self.create_write_port_measurement_objects()

    def create_read_port_measurement_objects(self):
        """Create the measurements used for read ports: delays, slews, powers"""
        
        self.read_lib_meas = []
        trig_delay_name = "clk{0}"
        targ_name = "{0}{1}_{2}".format(self.dout_name,"{}",self.probe_data) #Empty values are the port and probe data bit
        self.read_lib_meas.append(delay_measure("delay_lh", trig_delay_name, targ_name, "RISE", "RISE", measure_scale=1e9))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ONE #Used to index time delay values when measurements written to spice file.
        self.read_lib_meas.append(delay_measure("delay_hl", trig_delay_name, targ_name, "FALL", "FALL", measure_scale=1e9))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ZERO
        self.delay_meas = self.read_lib_meas[:] #For debugging, kept separated
        
        self.read_lib_meas.append(slew_measure("slew_lh", targ_name, "RISE", measure_scale=1e9))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ONE
        self.read_lib_meas.append(slew_measure("slew_hl", targ_name, "FALL", measure_scale=1e9))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ZERO
        
        self.read_lib_meas.append(power_measure("read1_power", "RISE", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ONE
        self.read_lib_meas.append(power_measure("read0_power", "FALL", measure_scale=1e3))
        self.read_lib_meas[-1].meta_str = sram_op.READ_ZERO
        
        #This will later add a half-period to the spice time delay. Only for reading 0.
        for obj in self.read_lib_meas:
            if obj.meta_str is sram_op.READ_ZERO:
                obj.meta_add_delay = True

        # trig_name = "Xsram.s_en{}" #Sense amp enable
        # if len(self.all_ports) == 1: #special naming case for single port sram bitlines which does not include the port in name
            # port_format = ""
        # else:
            # port_format = "{}"
        
        # bl_name = "Xsram.Xbank0.bl{}_{}".format(port_format, self.bitline_column)
        # br_name = "Xsram.Xbank0.br{}_{}".format(port_format, self.bitline_column)
        # self.read_lib_meas.append(voltage_when_measure(self.voltage_when_names[0], trig_name, bl_name, "RISE", .5))
        # self.read_lib_meas.append(voltage_when_measure(self.voltage_when_names[1], trig_name, br_name, "RISE", .5))
        
        read_measures = []
        read_measures.append(self.read_lib_meas)
        #Other measurements associated with the read port not included in the liberty file
        read_measures.append(self.create_bitline_measurement_objects())
        read_measures.append(self.create_debug_measurement_objects())

        return read_measures
    
    def create_bitline_measurement_objects(self):
        """Create the measurements used for bitline delay values. Due to unique error checking, these are separated from other measurements.
           These measurements are only associated with read values
        """
        self.bitline_volt_meas = []
        #Bitline voltage measures
        self.bitline_volt_meas.append(voltage_at_measure("v_bl_READ_ZERO", 
                                                         self.bl_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ZERO
        self.bitline_volt_meas.append(voltage_at_measure("v_br_READ_ZERO", 
                                                         self.br_name))
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ZERO
        
        self.bitline_volt_meas.append(voltage_at_measure("v_bl_READ_ONE", 
                                                       self.bl_name)) 
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ONE
        self.bitline_volt_meas.append(voltage_at_measure("v_br_READ_ONE", 
                                                       self.br_name)) 
        self.bitline_volt_meas[-1].meta_str = sram_op.READ_ONE
        return self.bitline_volt_meas
        
    def create_write_port_measurement_objects(self):
        """Create the measurements used for read ports: delays, slews, powers"""
        self.write_lib_meas = []

        self.write_lib_meas.append(power_measure("write1_power", "RISE", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = sram_op.WRITE_ONE
        self.write_lib_meas.append(power_measure("write0_power", "FALL", measure_scale=1e3))
        self.write_lib_meas[-1].meta_str = sram_op.WRITE_ZERO
        
        write_measures = []
        write_measures.append(self.write_lib_meas)
        return write_measures
    
    def create_debug_measurement_objects(self):
        """Create debug measurement to help identify failures."""
        
        self.debug_delay_meas = []
        self.debug_volt_meas = []
        for meas in self.delay_meas:
            debug_meas = copy.deepcopy(meas)
            debug_meas.name = debug_meas.name+'_debug'
            #This particular debugs check if output value is flipped, so TARG_DIR is flipped
            if meas.targ_dir_str == 'FALL':
                debug_meas.targ_dir_str = 'RISE'
            else:
                debug_meas.targ_dir_str = 'FALL'
            #inserting debug member variable
            debug_meas.parent = meas.name
            self.debug_delay_meas.append(debug_meas)

            #Output voltage measures
            self.debug_volt_meas.append(voltage_at_measure("v_{}".format(debug_meas.meta_str), 
                                                           debug_meas.targ_name_no_port)) 
            self.debug_volt_meas[-1].meta_str = debug_meas.meta_str
            
        return self.debug_delay_meas+self.debug_volt_meas
         
    def set_load_slew(self,load,slew):
        """ Set the load and slew """
        self.load = load
        self.slew = slew
        
    def add_graph_exclusions(self):
        """Exclude portions of SRAM from timing graph which are not relevant"""
        #other initializations can only be done during analysis when a bit has been selected
        #for testing.
        self.sram.bank.graph_exclude_precharge()
        self.sram.graph_exclude_addr_dff()
        self.sram.graph_exclude_data_dff()
        self.sram.graph_exclude_ctrl_dffs()
        
    def create_graph(self):
        """Creates timing graph to generate the timing paths for the SRAM output."""
        self.sram.bank.bitcell_array.init_graph_params() #Removes previous bit exclusions
        self.sram.bank.bitcell_array.graph_exclude_bits(self.wordline_row, self.bitline_column)
        
        #Generate new graph every analysis as edges might change depending on test bit
        self.graph = graph_util.timing_graph()
        self.sram.build_graph(self.graph,"X{}".format(self.sram.name),self.pins)
        #debug.info(1,"{}".format(self.graph))
        port = 0
        self.graph.get_all_paths('{}{}'.format(tech.spice["clk"], port), \
                     '{}{}_{}'.format(self.dout_name, port, self.probe_data))
        sen_name = self.sram.get_sen_name(self.sram.name, port).lower()
        debug.info(1, "Sen name={}".format(sen_name))
        sen_path = []
        for path in self.graph.all_paths:
            if sen_name in path:
                sen_path = path
                break
        debug.check(len(sen_path)!=0, "Could not find s_en timing path.")
        preconv_names = []
        for path in self.graph.all_paths:
            if not path is sen_path:
                sen_preconv = self.graph.get_path_preconvergence_point(path, sen_path)
                if sen_preconv not in preconv_names:
                    preconv_names.append(sen_preconv[0]) #only save non-sen_path names
                    
        #Not an good way to separate inverting and non-inverting bitlines...            
        self.bl_name = [bl for bl in preconv_names if 'bl' in bl][0]
        self.br_name = [bl for bl in preconv_names if 'br' in bl][0]          
        debug.info(1,"bl_name={}".format(self.bl_name))
        
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
        self.stim.inst_model(pins=self.pins,
                             model_name=self.sram.name)
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
        
    def get_read_measure_variants(self, port, measure_obj):
        """Checks the measurement object and calls respective function for related measurement inputs."""
        meas_type = type(measure_obj)
        if meas_type is delay_measure or meas_type is slew_measure:
            return self.get_delay_measure_variants(port, measure_obj)
        elif meas_type is power_measure:
            return self.get_power_measure_variants(port, measure_obj, "read")
        elif meas_type is voltage_when_measure:
            return self.get_volt_when_measure_variants(port, measure_obj)
        elif meas_type is voltage_at_measure:
            return self.get_volt_at_measure_variants(port, measure_obj)
        else:
            debug.error("Input function not defined for measurement type={}".format(meas_type))
            
    def get_delay_measure_variants(self, port, delay_obj):
        """Get the measurement values that can either vary from simulation to simulation (vdd, address) or port to port (time delays)"""
        #Return value is intended to match the delay measure format:  trig_td, targ_td, vdd, port
        #vdd is arguably constant as that is true for a single lib file.
        if delay_obj.meta_str == sram_op.READ_ZERO:
            #Falling delay are measured starting from neg. clk edge. Delay adjusted to that.
            meas_cycle_delay = self.cycle_times[self.measure_cycles[port][delay_obj.meta_str]]
        elif delay_obj.meta_str == sram_op.READ_ONE:
            meas_cycle_delay = self.cycle_times[self.measure_cycles[port][delay_obj.meta_str]]
        else:
            debug.error("Unrecognised delay Index={}".format(delay_obj.meta_str),1)
            
        #These measurements have there time further delayed to the neg. edge of the clock.    
        if delay_obj.meta_add_delay:    
            meas_cycle_delay += self.period/2
            
        return (meas_cycle_delay, meas_cycle_delay, self.vdd_voltage, port)
    
    def get_power_measure_variants(self, port, power_obj, operation):
        """Get the measurement values that can either vary port to port (time delays)"""
        #Return value is intended to match the power measure format:  t_initial, t_final, port
        t_initial = self.cycle_times[self.measure_cycles[port][power_obj.meta_str]]
        t_final = self.cycle_times[self.measure_cycles[port][power_obj.meta_str]+1]
    
        return (t_initial, t_final, port)
    
    def get_volt_at_measure_variants(self, port, volt_meas):
        """Get the measurement values that can either vary port to port (time delays)"""
        #Only checking 0 value reads for now.
        if volt_meas.meta_str == sram_op.READ_ZERO:
            #Falling delay are measured starting from neg. clk edge. Delay adjusted to that.
            meas_cycle = self.cycle_times[self.measure_cycles[port][volt_meas.meta_str]]
        elif volt_meas.meta_str == sram_op.READ_ONE:
            meas_cycle = self.cycle_times[self.measure_cycles[port][volt_meas.meta_str]]
        else:
            debug.error("Unrecognised delay Index={}".format(volt_meas.meta_str),1)
        #Measurement occurs at the end of the period -> current period start + period 
        at_time = meas_cycle+self.period
        return (at_time, port)
    
    def get_volt_when_measure_variants(self, port, volt_meas):
        """Get the measurement values that can either vary port to port (time delays)"""
        #Only checking 0 value reads for now.
        t_trig = meas_cycle_delay = self.cycle_times[self.measure_cycles[port][sram_op.READ_ZERO]]

        return (t_trig, self.vdd_voltage, port)
    
    def write_delay_measures_read_port(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """
        # add measure statements for delays/slews
        for meas_list in self.read_meas_lists:
            for measure in meas_list:
                measure_variant_inp_tuple = self.get_read_measure_variants(port, measure)
                measure.write_measure(self.stim, measure_variant_inp_tuple)

    def get_write_measure_variants(self, port, measure_obj):
        """Checks the measurement object and calls respective function for related measurement inputs."""
        meas_type = type(measure_obj)
        if meas_type is power_measure:
            return self.get_power_measure_variants(port, measure_obj, "write")
        else:
            debug.error("Input function not defined for measurement type={}".format(meas_type))        
            
    def write_delay_measures_write_port(self, port):
        """
        Write the measure statements to quantify the power results for a write port.
        """
        # add measure statements for power
        for meas_list in self.write_meas_lists:
            for measure in meas_list:
                measure_variant_inp_tuple = self.get_write_measure_variants(port, measure)
                measure.write_measure(self.stim, measure_variant_inp_tuple)

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
    
    def run_delay_simulation(self):
        """
        This tries to simulate a period and checks if the result works. If
        so, it returns True and the delays, slews, and powers.  It
        works on the trimmed netlist by default, so powers do not
        include leakage of all cells.
        """
        #Sanity Check
        debug.check(self.period > 0, "Target simulation period non-positive") 
        
        sim_passed = True
        result = [{} for i in self.all_ports]
        # Checking from not data_value to data_value
        self.write_delay_stimulus()

        self.stim.run_sim()
        
        #Loop through all targeted ports and collect delays and powers. 
        #Too much duplicate code here. Try reducing
        for port in self.targ_read_ports:
            debug.info(2, "Checking delay values for port {}".format(port))
            read_port_dict = {}
            #Get measurements from output file
            for measure in self.read_lib_meas:
                read_port_dict[measure.name] = measure.retrieve_measure(port=port)
            debug_passed = self.check_debug_measures(port, read_port_dict)
            
            #Check timing for read ports. Power is only checked if it was read correctly
            if not self.check_valid_delays(read_port_dict) or not debug_passed:
                return (False,{})
            if not check_dict_values_is_float(read_port_dict):
                debug.error("Failed to Measure Read Port Values:\n\t\t{0}".format(read_port_dict),1) #Printing the entire dict looks bad.       
                
            result[port].update(read_port_dict)
            
        for port in self.targ_write_ports:
            write_port_dict = {}
            for measure in self.write_lib_meas:
                write_port_dict[measure.name] = measure.retrieve_measure(port=port)

            if not check_dict_values_is_float(write_port_dict):
                debug.error("Failed to Measure Write Port Values:\n\t\t{0}".format(write_port_dict),1) #Printing the entire dict looks bad. 
            result[port].update(write_port_dict)
            
        # The delay is from the negative edge for our SRAM
        return (sim_passed,result)

    def check_debug_measures(self, port, read_measures):
        """Debug measures that indicate special conditions."""
        #Currently, only check if the opposite than intended value was read during
        # the read cycles i.e. neither of these measurements should pass.
        success = True
        for meas in self.debug_delay_meas:
            val = meas.retrieve_measure(port=port)
            debug.info(2,"{}={}".format(meas.name, val))
            if type(val) != float:
                continue
            
            if meas.meta_add_delay:
                max_delay = self.period/2
            else:
                max_delay = self.period
                
            #If the debug measurement occurs after the original (and passes other conditions)
            #then it fails i.e. the debug value represents the final (but failing) state of the output
            parent_compare = type(read_measures[meas.parent]) != float or val > read_measures[meas.parent]
            if 0 < val < max_delay and parent_compare:
                success = False
                debug.info(1, "Debug measurement failed. Incorrect Value found on output.") 
                break
                
        #FIXME: these checks need to be re-done to be more robust against possible errors        
        bl_vals = {}
        br_vals = {}
        for meas in self.bitline_volt_meas:
            val = meas.retrieve_measure(port=port)
            if self.bl_name == meas.targ_name_no_port:
                bl_vals[meas.meta_str] = val
            elif self.br_name == meas.targ_name_no_port: 
                br_vals[meas.meta_str] = val

            debug.info(1,"{}={}".format(meas.name,val))
                
        bl_check = False    
        for meas in self.debug_volt_meas:
            val = meas.retrieve_measure(port=port)
            debug.info(2,"{}={}".format(meas.name, val))
            if type(val) != float:
                continue

            if meas.meta_str == sram_op.READ_ONE and val < self.vdd_voltage*.1:
                success = False
                debug.info(1, "Debug measurement failed. Value {}v was read on read 1 cycle.".format(val))
                bl_check = self.check_bitline_meas(bl_vals[sram_op.READ_ONE], br_vals[sram_op.READ_ONE])
            elif meas.meta_str == sram_op.READ_ZERO and val > self.vdd_voltage*.9:
                success = False
                debug.info(1, "Debug measurement failed. Value {}v was read on read 0 cycle.".format(val))
                bl_check = self.check_bitline_meas(br_vals[sram_op.READ_ONE], bl_vals[sram_op.READ_ONE])
                
            #If the bitlines have a correct value while the output does not then that is a 
            #sen error. FIXME: there are other checks that can be done to solidfy this conclusion.
            if bl_check:
                debug.error("Sense amp enable timing error. Increase the delay chain through the configuration file.",1)
            
        return success
        
        
    def check_bitline_meas(self, v_discharged_bl, v_charged_bl):
        """Checks the value of the discharging bitline. Confirms s_en timing errors.
           Returns true if the bitlines are at there expected value."""
        #The inputs looks at discharge/charged bitline rather than left or right (bl/br)
        #Performs two checks, discharging bitline is at least 10% away from vdd and there is a 
        #10% vdd difference between the bitlines. Both need to fail to be considered a s_en error.
        min_dicharge = v_discharged_bl < self.vdd_voltage*0.9
        min_diff = (v_charged_bl - v_discharged_bl) > self.vdd_voltage*0.1
        
        debug.info(1,"min_dicharge={}, min_diff={}".format(min_dicharge,min_diff))
        return (min_dicharge and min_diff) 
        
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
    
    def check_valid_delays(self, result_dict):
        """ Check if the measurements are defined and if they are valid. """
        #Hard coded names currently
        delay_hl = result_dict["delay_hl"]
        delay_lh = result_dict["delay_lh"]
        slew_hl = result_dict["slew_hl"]
        slew_lh = result_dict["slew_lh"]
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
        if abs(delay_hl)>half_period or abs(delay_lh)>self.period or abs(slew_hl)>half_period or abs(slew_lh)>self.period \
           or delay_hl<0 or delay_lh<0 or slew_hl<0 or slew_lh<0:
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
            #key=input("press return to continue")

        
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
                
                #FIXME: This is a hack solution to fix the min period search. The slew will always be based on the period when there
                #is a column mux. Therefore, the checks are skipped for this condition. This is hard to solve without changing the netlist.
                #Delays/slews based on the period will cause the min_period search to come to the wrong period.
                if self.sram.col_addr_size>0 and "slew" in dname:
                    continue

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
        self.bitline_column = self.get_data_bit_column_number(probe_address, probe_data)
        self.wordline_row = self.get_address_row_number(probe_address)
        self.prepare_netlist()
        
    def get_data_bit_column_number(self, probe_address, probe_data):
        """Calculates bitline column number of data bit under test using bit position and mux size"""
        if self.sram.col_addr_size>0:
            col_address = int(probe_address[0:self.sram.col_addr_size],2)
        else:
            col_address = 0
        bl_column = int(self.sram.words_per_row*probe_data + col_address)
        return bl_column 

    def get_address_row_number(self, probe_address):
        """Calculates wordline row number of data bit under test using address and column mux size"""
        return int(probe_address[self.sram.col_addr_size:],2)

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

    def analysis_init(self, probe_address, probe_data):
        """Sets values which are dependent on the data address/bit being tested."""
        self.set_probe(probe_address, probe_data)
        self.create_graph()
        self.create_measurement_names()
        self.create_measurement_objects()
        
    def analyze(self, probe_address, probe_data, slews, loads):
        """
        Main function to characterize an SRAM for a table. Computes both delay and power characterization.
        """
        #Dict to hold all characterization values
        char_sram_data = {}
        self.analysis_init(probe_address, probe_data)
        
        self.load=max(loads)
        self.slew=max(slews)
        
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
    
    def calculate_inverse_address(self):
        """Determine dummy test address based on probe address and column mux size."""
        #The inverse address needs to share the same bitlines as the probe address as the trimming will remove all other bitlines
        #This is only an issue when there is a column mux and the address maps to different bitlines. 
        column_addr = self.probe_address[:self.sram.col_addr_size] #do not invert this part
        inverse_address = ""
        for c in self.probe_address[self.sram.col_addr_size:]: #invert everything else
            if c=="0":
                inverse_address += "1"
            elif c=="1":
                inverse_address += "0"
            else:
                debug.error("Non-binary address string",1)
        return inverse_address+column_addr

    def gen_test_cycles_one_port(self, read_port, write_port):
        """Sets a list of key time-points [ns] of the waveform (each rising edge)
        of the cycles to do a timing evaluation of a single port """

        # Create the inverse address for a scratch address
        inverse_address = self.calculate_inverse_address()

        # For now, ignore data patterns and write ones or zeros
        data_ones = "1"*self.word_size
        data_zeros = "0"*self.word_size
        
        if self.t_current == 0:
            self.add_noop_all_ports("Idle cycle (no positive clock edge)",
                      inverse_address, data_zeros)
        
        self.add_write("W data 1 address {}".format(inverse_address),
                       inverse_address,data_ones,write_port) 

        self.add_write("W data 0 address {} to write value".format(self.probe_address),
                       self.probe_address,data_zeros,write_port)
        self.measure_cycles[write_port][sram_op.WRITE_ZERO] = len(self.cycle_times)-1
        
        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address {} to set DOUT caps".format(inverse_address),
                      inverse_address,data_zeros,read_port) 

        self.add_read("R data 0 address {} to check W0 worked".format(self.probe_address),
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles[read_port][sram_op.READ_ZERO] = len(self.cycle_times)-1              
        
        self.add_noop_all_ports("Idle cycle (if read takes >1 cycle)",
                      inverse_address,data_zeros)

        self.add_write("W data 1 address {} to write value".format(self.probe_address),
                       self.probe_address,data_ones,write_port)
        self.measure_cycles[write_port][sram_op.WRITE_ONE] = len(self.cycle_times)-1

        self.add_write("W data 0 address {} to clear DIN caps".format(inverse_address),
                       inverse_address,data_zeros,write_port)

        # This also ensures we will have a L->H transition on the next read
        self.add_read("R data 0 address {} to clear DOUT caps".format(inverse_address),
                      inverse_address,data_zeros,read_port)
        
        self.add_read("R data 1 address {} to check W1 worked".format(self.probe_address),
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles[read_port][sram_op.READ_ONE] = len(self.cycle_times)-1                
        
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
        self.create_measurement_names()
        power = self.analytical_power(slews, loads)
        port_data = self.get_empty_measure_data_dict()
        relative_loads = [logical_effort.convert_farad_to_relative_c(c_farad) for c_farad in loads]
        for slew in slews:
            for load in relative_loads:
                self.set_load_slew(load,slew)
                bank_delay = self.sram.analytical_delay(self.corner, self.slew,self.load)
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
        period_margin = 0.1
        risefall_delay = bank_delay[self.read_ports[0]].delay/1e3
        sram_data = { "min_period":risefall_delay*2*period_margin, 
                      "leakage_power": power.leakage}
        debug.info(2,"SRAM Data:\n{}".format(sram_data))                 
        debug.info(2,"Port Data:\n{}".format(port_data)) 
        return (sram_data,port_data)
        
    
    def analytical_power(self, slews, loads):
        """Get the dynamic and leakage power from the SRAM"""
        #slews unused, only last load is used
        load = loads[-1]
        power = self.sram.analytical_power(self.corner, load) 
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
