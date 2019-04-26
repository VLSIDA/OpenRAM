# See LICENSE for licensing information.
#
#Copyright (c) 2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import sys,re,shutil
import debug
import tech
import math
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS
from .delay import delay

class bitline_delay(delay):
    """Functions to test for the worst case delay in a target SRAM

    The current worst case determines a feasible period for the SRAM then tests
    several bits and record the delay and differences between the bits.

    """

    def __init__(self, sram, spfile, corner):
        delay.__init__(self,sram,spfile,corner)
        self.period = tech.spice["feasible_period"]
        self.is_bitline_measure = True
    
    def create_signal_names(self):
        delay.create_signal_names(self)
        self.bl_signal_names = ["Xsram.Xbank0.bl", "Xsram.Xbank0.br"]
        self.sen_name = "Xsram.s_en"

    def create_measurement_names(self):
        """Create measurement names. The names themselves currently define the type of measurement"""
        #Altering the names will crash the characterizer. TODO: object orientated approach to the measurements.
        self.bl_volt_meas_names = ["volt_bl", "volt_br"]
        self.bl_delay_meas_names = ["delay_bl", "delay_br"] #only used in SPICE simulation
        self.bl_delay_result_name = "delay_bl_vth" #Used in the return value
    
    def set_probe(self,probe_address, probe_data):
        """ Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze."""
        delay.set_probe(self,probe_address, probe_data)
        self.bitline_column = self.get_data_bit_column_number(probe_address, probe_data)
        
    def write_delay_measures(self):
        """
        Write the measure statements to quantify the bitline voltage at sense amp enable 50%.
        """
        self.sf.write("\n* Measure statements for delay and power\n")

        # Output some comments to aid where cycles start and
        for comment in self.cycle_comments:
            self.sf.write("* {}\n".format(comment))
            
        for read_port in self.targ_read_ports:
           self.write_bitline_voltage_measures(read_port)       
           self.write_bitline_delay_measures(read_port)
           
    def write_bitline_voltage_measures(self, port):
        """
        Add measurments to capture the bitline voltages at 50% Sense amp enable
        """
        debug.info(2, "Measuring bitline column={}, port={}".format(self.bitline_column,port))
        if len(self.all_ports) == 1: #special naming case for single port sram bitlines
            bitline_port = ""
        else:
            bitline_port = str(port)
            
        sen_port_name = "{}{}".format(self.sen_name,port)
        for (measure_name, bl_signal_name) in zip(self.bl_volt_meas_names, self.bl_signal_names):
            bl_port_name = "{}{}_{}".format(bl_signal_name, bitline_port, self.bitline_column)
            measure_port_name = "{}{}".format(measure_name,port)
            self.stim.gen_meas_find_voltage(measure_port_name, sen_port_name, bl_port_name, .5, "RISE", self.cycle_times[self.measure_cycles[port]["read0"]])
    
    def write_bitline_delay_measures(self, port):
        """
        Write the measure statements to quantify the delay and power results for a read port.
        """
        # add measure statements for delays/slews
        for (measure_name, bl_signal_name) in zip(self.bl_delay_meas_names, self.bl_signal_names):
            meas_values = self.get_delay_meas_values(measure_name, bl_signal_name, port)
            self.stim.gen_meas_delay(*meas_values)
    
    def get_delay_meas_values(self, delay_name, bitline_name, port):
        """Get the values needed to generate a Spice measurement statement based on the name of the measurement."""
        if len(self.all_ports) == 1: #special naming case for single port sram bitlines
            bitline_port = ""
        else:
            bitline_port = str(port)
        
        meas_name="{0}{1}".format(delay_name, port)
        targ_name = "{0}{1}_{2}".format(bitline_name,bitline_port,self.bitline_column)
        half_vdd = 0.5 * self.vdd_voltage
        trig_val = half_vdd
        targ_val = self.vdd_voltage-tech.spice["v_threshold_typical"]
        trig_name = "clk{0}".format(port)
        trig_dir="FALL" 
        targ_dir="FALL"
        #Half period added to delay measurement to negative clock edge
        trig_td = targ_td = self.cycle_times[self.measure_cycles[port]["read0"]]  + self.period/2
        return (meas_name,trig_name,targ_name,trig_val,targ_val,trig_dir,targ_dir,trig_td,targ_td)
    
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
        self.measure_cycles[write_port]["write0"] = len(self.cycle_times)-1
        
        # This also ensures we will have a H->L transition on the next read
        self.add_read("R data 1 address {} to set DOUT caps".format(inverse_address),
                      inverse_address,data_zeros,read_port) 
        self.measure_cycles[read_port]["read1"] = len(self.cycle_times)-1
                      
        self.add_read("R data 0 address {} to check W0 worked".format(self.probe_address),
                      self.probe_address,data_zeros,read_port)
        self.measure_cycles[read_port]["read0"] = len(self.cycle_times)-1
        
    def get_data_bit_column_number(self, probe_address, probe_data):
        """Calculates bitline column number of data bit under test using bit position and mux size"""
        if self.sram.col_addr_size>0:
            col_address = int(probe_address[0:self.sram.col_addr_size],2)
        else:
            col_address = 0
        bl_column = int(self.sram.words_per_row*probe_data + col_address)
        return bl_column
        
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

        self.stim.run_sim() #running sim prodoces spice output file.
          
        for port in self.targ_read_ports:  
            #Parse and check the voltage measurements
            bl_volt_meas_dict = {}  
            for mname in self.bl_volt_meas_names:
                mname_port = "{}{}".format(mname,port)
                volt_meas_val = parse_spice_list("timing", mname_port)
                if type(volt_meas_val)!=float:
                    debug.error("Failed to Parse Bitline Voltage:\n\t\t{0}={1}".format(mname,volt_meas_val),1)
                bl_volt_meas_dict[mname] = volt_meas_val
            result[port].update(bl_volt_meas_dict)

            #Parse and check the delay measurements. Intended that one measurement will fail, save the delay that did not fail.
            bl_delay_meas_dict = {}
            values_added = 0 #For error checking
            for mname in self.bl_delay_meas_names: #Parse 
                mname_port = "{}{}".format(mname,port)
                delay_meas_val = parse_spice_list("timing", mname_port) 
                if type(delay_meas_val)==float: #Only add if value is float, do not error.
                    bl_delay_meas_dict[self.bl_delay_result_name] = delay_meas_val * 1e9 #convert to ns
                    values_added+=1
            debug.check(values_added>0, "Bitline delay measurements failed in SPICE simulation.")
            debug.check(values_added<2, "Both bitlines experienced a Vth drop, check simulation results.")  
            result[port].update(bl_delay_meas_dict)
        
        # The delay is from the negative edge for our SRAM
        return (True,result)
    
    def check_bitline_all_results(self, results):
        """Checks the bitline values measured for each tested port"""
        for port in self.targ_read_ports:
            self.check_bitline_port_results(results[port])
  
    def check_bitline_port_results(self, port_results):
        """Performs three different checks for the bitline values: functionality, bitline swing from vdd, and differential bit swing"""
        bl_volt, br_volt = port_results["volt_bl"], port_results["volt_br"]
        self.check_functionality(bl_volt,br_volt)
        self.check_swing_from_vdd(bl_volt,br_volt)
        self.check_differential_swing(bl_volt,br_volt)
        
    def check_functionality(self, bl_volt, br_volt):
        """Checks whether the read failed or not. Measured values are hardcoded with the intention of reading a 0."""
        if bl_volt > br_volt:
            debug.error("Read failure. Value 1 was read instead of 0.",1)
            
    def check_swing_from_vdd(self, bl_volt, br_volt):
        """Checks difference on discharging bitline from VDD to see if it is within margin of the RBL height parameter."""
        if bl_volt < br_volt:
            discharge_volt = bl_volt
        else:
            discharge_volt = br_volt
        desired_bl_volt = tech.parameter["rbl_height_percentage"]*self.vdd_voltage
        debug.info(1, "Active bitline={:.3f}v, Desired bitline={:.3f}v".format(discharge_volt,desired_bl_volt))
        vdd_error_margin = .2 #20% of vdd margin for bitline, a little high for now.
        if abs(discharge_volt - desired_bl_volt) > vdd_error_margin*self.vdd_voltage:
            debug.warning("Bitline voltage is not within {}% Vdd margin. Delay chain/RBL could need resizing.".format(vdd_error_margin*100))
    
    def check_differential_swing(self, bl_volt, br_volt):
        """This check looks at the difference between the bitline voltages. This needs to be large enough to prevent
           sensing errors."""
        bitline_swing = abs(bl_volt-br_volt)
        debug.info(1,"Bitline swing={:.3f}v".format(bitline_swing))
        vdd_error_margin = .2 #20% of vdd margin for bitline, a little high for now.
        if bitline_swing < vdd_error_margin*self.vdd_voltage:
            debug.warning("Bitline swing less than {}% Vdd margin. Sensing errors more likely to occur.".format(vdd_error_margin))
            
    def analyze(self, probe_address, probe_data, slews, loads):
        """Measures the bitline swing of the differential bitlines (bl/br) at 50% s_en """
        self.set_probe(probe_address, probe_data)
        self.load=max(loads)
        self.slew=max(slews)
        
        read_port = self.read_ports[0] #only test the first read port
        bitline_swings = {}
        self.targ_read_ports = [read_port]
        self.targ_write_ports = [self.write_ports[0]]
        debug.info(1,"Bitline swing test: corner {}".format(self.corner))
        (success, results)=self.run_delay_simulation()
        debug.check(success, "Bitline Failed: period {}".format(self.period))
        debug.info(1,"Bitline values (voltages/delays):\n\t {}".format(results[read_port]))
        self.check_bitline_all_results(results)
        
        return results

        
    
