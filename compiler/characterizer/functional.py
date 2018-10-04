import sys,re,shutil
from design import design
import debug
import math
import tech
import random
from .stimuli import *
from .charutils import *
import utils
from globals import OPTS

from .simulation import simulation


class functional(simulation):
    """
       Functions to write random data values to a random address then read them back and check
       for successful SRAM operation.
    """

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)

        self.set_corner(corner)
        self.set_spice_constants()
        self.set_stimulus_variables()
        
        # Number of checks can be changed
        self.num_checks = 1
        self.cycles = 0
        self.eo_period = []
        
        # set to 1 if functional simulation fails during any check
        self.functional_fail = 0
        self.error = ""
        
    def run(self):
        """ Main function to generate random writes/reads, run spice, and analyze results """
        self.noop()
        
        self.overwrite_test()
        self.write_read_test()
        
        self.noop()
        
        # Run SPICE simulation
        self.write_functional_stimulus()
        self.stim.run_sim()
        
        # Extrat DOUT values from spice timing.lis
        for i in range(2*self.num_checks):
            self.sp_read_value = ["" for port in range(self.total_read)]
            for port in range(self.total_read):
                for bit in range(self.word_size):
                    value = parse_spice_list("timing", "vdout{0}.{1}.ck{2}".format(self.read_index[port],bit,i))
                    if value > 0.9 * self.vdd_voltage:
                        self.sp_read_value[port] = "1" + self.sp_read_value[port]
                    elif value < 0.1 * self.vdd_voltage:
                        self.sp_read_value[port] = "0" + self.sp_read_value[port]
                    else:
                        self.functional_fail = 1
                        self.error ="FAILED: DOUT{0}[{1}] value {2} at time {3}n does not fall within noise margins <{4} or >{5}.".format(port,
                                                                                                                             bit,
                                                                                                                             value,
                                                                                                                             self.eo_period[i],
                                                                                                                             0.1*self.vdd_voltage,
                                                                                                                             0.9*self.vdd_voltage)
                                                                                                                    
                    if self.functional_fail:
                        return (self.functional_fail, self.error)
                
                if i < self.num_checks:
                    self.read_values_over_test[i].append(self.sp_read_value[port])
                else:
                    self.read_values_test[i-self.num_checks].append(self.sp_read_value[port])
        
        # Compare written values to read values
        for i in range(self.num_checks):
            debug.info(1, "Stored Word - Overwrite Test: {}".format(self.stored_values_over_test[i]))
            debug.info(1, "Read Word - Overwrite Test: {}".format(self.read_values_over_test[i]))
            for port in range(self.total_read):
                if self.stored_values_over_test[i] != self.read_values_over_test[i][port]:
                    self.functional_fail = 1
                    self.error ="FAILED: Overwrite Test - read value {0} does not match writen value {1}.".format(self.read_values_over_test[i][port],
                                                                                                                  self.stored_values_over_test[i])
        
        for i in range(self.num_checks):
            debug.info(1, "Stored Word - Standard W/R Test: {}".format(self.stored_values_test[i]))
            debug.info(1, "Read Word - Standard W/R Test: {}".format(self.read_values_test[i]))
            for port in range(self.total_read):
                if self.stored_values_test[i] != self.read_values_test[i][port]:
                    self.functional_fail = 1
                    self.error ="FAILED: Standard W/R Test - read value {0} does not match writen value {1}.".format(self.read_values_test[i][port],
                                                                                                                     self.stored_values_test[i])
                    
        return (self.functional_fail, self.error)
    
    def multiport_run(self):
        """ Main function to generate random writes/reads, run spice, and analyze results. This function includes a multiport check. """ 
        self.noop()
        
        self.multi_read_test()
        self.overwrite_test()
        self.write_read_test()
        
        self.noop()
        
        # Run SPICE simulation
        self.write_functional_stimulus()
        self.stim.run_sim()
        
        # Extrat DOUT values from spice timing.lis
        for i in range(3*self.num_checks):
            self.sp_read_value = ["" for port in range(self.total_read)]
            for port in range(self.total_read):
                for bit in range(self.word_size):
                    value = parse_spice_list("timing", "vdout{0}.{1}.ck{2}".format(self.read_index[port],bit,i))
                    if value > 0.9 * self.vdd_voltage:
                        self.sp_read_value[port] = "1" + self.sp_read_value[port]
                    elif value < 0.1 * self.vdd_voltage:
                        self.sp_read_value[port] = "0" + self.sp_read_value[port]
                    else:
                        self.functional_fail = 1
                        self.error ="FAILED: DOUT{0}[{1}] value {2} at time {3}n does not fall within noise margins <{4} or >{5}.".format(port,
                                                                                                                             bit,
                                                                                                                             value,
                                                                                                                             self.eo_period[i],
                                                                                                                             0.1*self.vdd_voltage,
                                                                                                                             0.9*self.vdd_voltage)
                                                                                                                             
                    if self.functional_fail:
                        return (self.functional_fail, self.error)
                
                if i < self.num_checks:
                    self.read_values_multi_test[i][self.multi_addrs[i][port]] = self.sp_read_value[port]
                elif i < 2*self.num_checks:
                    self.read_values_over_test[i-self.num_checks].append(self.sp_read_value[port])
                else:
                    self.read_values_test[i-2*self.num_checks].append(self.sp_read_value[port])
                    
        # Compare written values to read values
        for i in range(self.num_checks):
            debug.info(1, "Stored Words - Multi Test (addr:word): {}".format(self.stored_values_multi_test[i]))
            debug.info(1, "Read Words - Mutlti Test (addr:word): {}".format(self.read_values_multi_test[i]))
            for addr in self.multi_addrs[i]:
                if self.stored_values_multi_test[i][addr] != self.read_values_multi_test[i][addr]:
                    self.functional_fail = 1
                    self.error ="FAILED: Multi Test - read value {0} does not match writen value {1}.".format(self.read_values_multi_test[i][addr],
                                                                                                              self.stored_values_multi_test[i][addr])
                    
        for i in range(self.num_checks):
            debug.info(1, "Stored Word - Overwrite Test: {}".format(self.stored_values_over_test[i]))
            debug.info(1, "Read Word - Overwrite Test: {}".format(self.read_values_over_test[i]))
            for port in range(self.total_read):
                if self.stored_values_over_test[i] != self.read_values_over_test[i][port]:
                    self.functional_fail = 1
                    self.error ="FAILED: Overwrite Test - read value {0} does not match writen value {1}.".format(self.read_values_over_test[i][port],
                                                                                                                  self.stored_values_over_test[i])
        
        for i in range(self.num_checks):
            debug.info(1, "Stored Word - Standard W/R Test: {}".format(self.stored_values_test[i]))
            debug.info(1, "Read Word - Standard W/R Test: {}".format(self.read_values_test[i]))
            for port in range(self.total_read):
                if self.stored_values_test[i] != self.read_values_test[i][port]:
                    self.functional_fail = 1
                    self.error ="FAILED: Standard W/R Test - read value {0} does not match writen value {1}.".format(self.read_values_test[i][port],
                                                                                                                     self.stored_values_test[i])
        
        return (self.functional_fail, self.error)
    
    def multi_read_test(self):
        """ Multiport functional test to see if mutliple words on multiple addresses can be accessed at the same time. """
        self.stored_values_multi_test = [{} for i in range(self.num_checks)]
        self.read_values_multi_test = [{} for i in range(self.num_checks)]
        self.multi_addrs = []
        
        for i in range(self.num_checks):
            # Write random words to a random addresses until there are as many stored words as there are RW and R ports
            while(len(self.stored_values_multi_test[i]) < self.total_read):
                addr = self.gen_addr()
                word = self.gen_data()
                self.write(addr,word)
                self.stored_values_multi_test[i][addr] = word
        
            # Each RW and R port will read from a different address
            stored_addrs = []
            stored_words = []
            for (addr,word) in self.stored_values_multi_test[i].items():
                stored_addrs.append(addr)
                stored_words.append(word)
                
            self.multi_addrs.append(stored_addrs)
            self.multi_read(stored_addrs,stored_words)
    
    def overwrite_test(self):
        """ Functional test to see if a word at a particular address can be overwritten without being corrupted. """
        self.stored_values_over_test = []
        self.read_values_over_test = [[] for i in range(self.num_checks)]
        
        for i in range(self.num_checks):
            # Write a random word to a random address 3 different times, overwriting the stored word twice
            addr = self.gen_addr()
            for j in range(2):
                word = self.gen_data()
                self.write(addr,word)
            self.stored_values_over_test.append(word)
            
            # Read word from address (use all RW and R ports)
            self.read(addr,word)
    
    def write_read_test(self):
        """ A standard functional test for writing to an address and reading back the value. """
        self.stored_values_test = []
        self.read_values_test = [[] for i in range(self.num_checks)]
        
        for i in range(self.num_checks):
            # Write a random word to a random address
            addr = self.gen_addr()
            word = self.gen_data()
            self.write(addr,word)
            self.stored_values_test.append(word)
            
            # Read word from address (use all RW and R ports)
            self.read(addr,word)
    
    def noop(self):
        """ Noop cycle. """
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        for port in range(self.total_ports):        
            self.csb_values[port].append(1)
            
        for port in range(self.total_write):        
            self.web_values[port].append(1)

        for port in range(self.total_ports):     
            for bit in range(self.addr_size):
                self.addr_values[port][bit].append(0)
        
        for port in range(self.total_write):    
            for bit in range(self.word_size):
                self.data_values[port][bit].append(0)
    
    def write(self,addr,word,write_port=0):
        """ Generates signals for a write cycle. """
        debug.info(1, "Writing {0} to address {1} in cycle {2}...".format(word,addr,self.cycles))
        self.cycles += 1
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        # Write control signals
        for port in range(self.total_ports):
            if port == write_port:
                self.csb_values[port].append(0)
            else:
                self.csb_values[port].append(1)
        
        for port in range(self.total_write):
            if port == write_port:
                self.web_values[port].append(0)
            else:
                self.web_values[port].append(1)

        # Write address
        for port in range(self.total_ports):
            for bit in range(self.addr_size):
                current_address_bit = int(addr[self.addr_size-1-bit])
                self.addr_values[port][bit].append(current_address_bit)
        
        # Write data
        for port in range(self.total_write):
            for bit in range(self.word_size):
                current_word_bit = int(word[self.word_size-1-bit])
                self.data_values[port][bit].append(current_word_bit)

    def read(self,addr,word):
        """ Generates signals for a read cycle. """
        debug.info(1, "Reading {0} from address {1} in cycle {2}...".format(word,addr,self.cycles))
        self.cycles += 1
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        # Read control signals
        for port in range(self.total_ports):
            if self.port_id[port] == "w":
                self.csb_values[port].append(1)
            else:
                self.csb_values[port].append(0)
            
        for port in range(self.total_write):
            self.web_values[port].append(1)

        # Read address
        for port in range(self.total_ports):
            for bit in range(self.addr_size):
                current_address_bit = int(addr[self.addr_size-1-bit])
                self.addr_values[port][bit].append(current_address_bit)
            
        # Data input doesn't matter during read cycle, so arbitrarily set to 0 for simulation
        for port in range(self.total_write):
            for bit in range(self.word_size):
                self.data_values[port][bit].append(0)
        
        # Record the end of the period that the read operation occured in
        self.eo_period.append(self.t_current)
    
    def multi_read(self,addrs,words):
        """ Generates signals for a read cycle but all ports read from a different address. The inputs 'addrs' and 'words' are lists. """
        debug.info(1, "Reading {0} from addresses {1} in cycle {2}...".format(words,addrs,self.cycles))
        self.cycles += 1
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        # Read control signals
        for port in range(self.total_ports):
            if self.port_id[port] == "w":
                self.csb_values[port].append(1)
            else:
                self.csb_values[port].append(0)
            
        for port in range(self.total_write):
            self.web_values[port].append(1)

        # Read address
        addr_index = 0
        for port in range(self.total_ports):
            for bit in range(self.addr_size):
                if self.port_id[port] == "w":
                    current_address_bit = 0
                else:
                    current_address_bit = int(addrs[addr_index][self.addr_size-1-bit])
                
                self.addr_values[port][bit].append(current_address_bit)
                
            if self.port_id[port] != "w":
                addr_index += 1
            
        # Data input doesn't matter during read cycle, so arbitrarily set to 0 for simulation
        for port in range(self.total_write):
            for bit in range(self.word_size):
                self.data_values[port][bit].append(0)
        
        # Record the end of the period that the read operation occured in
        self.eo_period.append(self.t_current)
        
    def gen_data(self):
        """ Generates a random word to write. """
        rand = random.randint(0,(2**self.word_size)-1)
        data_bits = self.convert_to_bin(rand,False)
        return data_bits
        
    def gen_addr(self):
        """ Generates a random address value to write to. """
        rand = random.randint(0,(2**self.addr_size)-1)  
        addr_bits = self.convert_to_bin(rand,True)
        return addr_bits 
        
    def get_data(self):
        """ Gets an available address and corresponding word. """
        # Currently unused but may need later depending on how the functional test develops
        addr = random.choice(self.stored_words.keys())
        word = self.stored_words[addr]
        return (addr,word)
        
    def convert_to_bin(self,value,is_addr):
        """ Converts addr & word to usable binary values. """
        new_value = str.replace(bin(value),"0b","")
        if(is_addr):
            expected_value = self.addr_size
        else:
            expected_value = self.word_size
        for i in range (expected_value - len(new_value)):
            new_value =  "0" + new_value
            
        #print("Binary Conversion: {} to {}".format(value, new_value))
        return new_value
        
    def obtain_cycle_times(self,period):
        """ Generate clock cycle times based on period and number of cycles. """
        t_current = 0
        self.cycle_times = []
        for i in range(self.cycles):
            self.cycle_times.append(t_current)
            t_current += period 
            
    def write_functional_stimulus(self):
        """ Writes SPICE stimulus. """
        #self.obtain_cycle_times(self.period)
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim,"w")
        self.sf.write("* Functional test stimulus file for {}ns period\n\n".format(self.period))
        self.stim = stimuli(self.sf,self.corner)

        #Write include statements
        self.sram_sp_file = "{}sram.sp".format(OPTS.openram_temp)
        shutil.copy(self.sp_file, self.sram_sp_file)
        self.stim.write_include(self.sram_sp_file)

        #Write Vdd/Gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()
        
        #Instantiate the SRAM
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_full_sram(sram=self.sram,
                                 sram_name=self.name)
        #self.stim.inst_sram(abits=self.addr_size,
        #                    dbits=self.word_size,
        #                    port_info=(self.total_ports,self.total_write,self.read_index,self.write_index),
        #                    sram_name=self.name)

        # Add load capacitance to each of the read ports
        self.sf.write("\n* SRAM output loads\n")
        for port in range(self.total_read):
            for bit in range(self.word_size):
                self.sf.write("CD{0}{1} DOUT{0}[{1}] 0 {2}f\n".format(self.read_index[port], bit, self.load))
                
        # Generate data input bits 
        self.sf.write("\n* Generation of data and address signals\n")
        for port in range(self.total_write):
            for bit in range(self.word_size):
                sig_name = "DIN{0}[{1}]".format(port,bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[port][bit], self.period, self.slew, 0.05)
        
        # Generate address bits
        for port in range(self.total_ports):
            for bit in range(self.addr_size):
                sig_name = "ADDR{0}[{1}]".format(port,bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][bit], self.period, self.slew, 0.05)

        # Generate control signals
        self.sf.write("\n * Generation of control signals\n")
        for port in range(self.total_ports):
            self.stim.gen_pwl("CSB{}".format(port), self.cycle_times , self.csb_values[port], self.period, self.slew, 0.05)
            
        for port in range(self.total_write):
            self.stim.gen_pwl("WEB{}".format(port), self.cycle_times , self.web_values[port], self.period, self.slew, 0.05)

        # Generate CLK signals
        for port in range(self.total_ports):
            self.stim.gen_pulse(sig_name="CLK{}".format(port),
                                v1=self.gnd_voltage,
                                v2=self.vdd_voltage,
                                offset=self.period,
                                period=self.period,
                                t_rise=self.slew,
                                t_fall=self.slew)
        
        # Generate DOUT value measurements
        if self.total_ports > 1:
            num_tests = 3
        else:
            num_tests = 2
        
        self.sf.write("\n * Generation of dout measurements\n")
        for i in range(num_tests*self.num_checks):
            t_intital = self.eo_period[i] - 0.01*self.period
            t_final = self.eo_period[i] + 0.01*self.period
            for port in range(self.total_read):
                for bit in range(self.word_size):
                    self.stim.gen_meas_value(meas_name="VDOUT{0}[{1}]ck{2}".format(self.read_index[port],bit,i),
                                             dout="DOUT{0}[{1}]".format(self.read_index[port],bit),
                                             t_intital=t_intital,
                                             t_final=t_final)
        
        self.stim.write_control(self.cycle_times[-1] + self.period)
        self.sf.close()


