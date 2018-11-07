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
        simulation.__init__(self, sram, spfile, corner)
        
        # Seed the characterizer with a constant seed for unit tests
        if OPTS.is_unit_test:
            random.seed(12345)

        self.set_corner(corner)
        self.set_spice_constants()
        self.set_stimulus_variables()
        self.create_signal_names()
        
        # Number of checks can be changed
        self.num_cycles = 2
        self.stored_words = {}      
        self.write_check = []
        self.read_check = []
    
    def set_spice_constants(self):
        """Spice constants for functional test"""
        simulation.set_spice_constants(self)
        #Heuristic increase for functional period. Base feasible period typically does not pass the functional test
        #for column mux of this size. Increase the feasible period by 20% for this case.
        if self.sram.words_per_row >= 4:
            self.period = self.period*1.2
    
    def run(self):
        # Generate a random sequence of reads and writes
        self.write_random_memory_sequence()
    
        # Run SPICE simulation
        self.write_functional_stimulus()
        self.stim.run_sim()
        
        # read DOUT values from SPICE simulation. If the values do not fall within the noise margins, return the error.
        (success, error) = self.read_stim_results()
        if not success:
            return (0, error)
            
        # Check read values with written values. If the values do not match, return an error.
        return self.check_stim_results()
    
    def write_random_memory_sequence(self):
        rw_ops = ["noop", "write", "read"]
        w_ops = ["noop", "write"]
        r_ops = ["noop", "read"]
        rw_read_din_data = "0"*self.word_size
        check = 0
        
        # First cycle idle
        comment = self.gen_cycle_comment("noop", "0"*self.word_size, "0"*self.addr_size, 0, self.t_current)
        self.add_noop_all_ports(comment, "0"*self.addr_size, "0"*self.word_size)
        
        # Write at least once
        addr = self.gen_addr()
        word = self.gen_data()
        comment = self.gen_cycle_comment("write", word, addr, 0, self.t_current)
        self.add_write(comment, addr, word, 0)
        self.stored_words[addr] = word
        
        # Read at least once. For multiport, it is important that one read cycle uses all RW and R port to read from the same address simultaniously.
        # This will test the viablilty of the transistor sizing in the bitcell.
        for port in range(self.total_ports):
            if self.port_id[port] == "w":
                self.add_noop_one_port("0"*self.addr_size, "0"*self.word_size, port)
            else:
                comment = self.gen_cycle_comment("read", word, addr, port, self.t_current)
                self.add_read_one_port(comment, addr, rw_read_din_data, port)
                self.write_check.append([word, "{0}{1}".format(self.dout_name,port), self.t_current+self.period, check])
                check += 1
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        # Perform a random sequence of writes and reads on random ports, using random addresses and random words
        for i in range(self.num_cycles):
            w_addrs = []
            for port in range(self.total_ports):
                if self.port_id[port] == "rw":
                    op = random.choice(rw_ops)
                elif self.port_id[port] == "w":
                    op = random.choice(w_ops)
                else:
                    op = random.choice(r_ops)
                    
                if op == "noop":
                    addr = "0"*self.addr_size
                    word = "0"*self.word_size
                    self.add_noop_one_port(addr, word, port)
                elif op == "write":
                    addr = self.gen_addr()
                    word = self.gen_data()
                    # two ports cannot write to the same address
                    if addr in w_addrs:
                        self.add_noop_one_port("0"*self.addr_size, "0"*self.word_size, port)
                    else:
                        comment = self.gen_cycle_comment("write", word, addr, port, self.t_current)
                        self.add_write_one_port(comment, addr, word, port)
                        self.stored_words[addr] = word
                        w_addrs.append(addr)
                else:
                    (addr,word) = random.choice(list(self.stored_words.items()))
                    # cannot read from an address that is currently being written to
                    if addr in w_addrs:
                        self.add_noop_one_port("0"*self.addr_size, "0"*self.word_size, port)
                    else:
                        comment = self.gen_cycle_comment("read", word, addr, port, self.t_current)
                        self.add_read_one_port(comment, addr, rw_read_din_data, port)
                        self.write_check.append([word, "{0}{1}".format(self.dout_name,port), self.t_current+self.period, check])
                        check += 1
                
            self.cycle_times.append(self.t_current)
            self.t_current += self.period
        
        # Last cycle idle needed to correctly measure the value on the second to last clock edge
        comment = self.gen_cycle_comment("noop", "0"*self.word_size, "0"*self.addr_size, 0, self.t_current)
        self.add_noop_all_ports(comment, "0"*self.addr_size, "0"*self.word_size)
            
    def read_stim_results(self):
        # Extrat DOUT values from spice timing.lis
        for (word, dout_port, eo_period, check) in self.write_check:
            sp_read_value = ""
            for bit in range(self.word_size):
                value = parse_spice_list("timing", "v{0}.{1}ck{2}".format(dout_port.lower(),bit,check))
                if value > 0.88 * self.vdd_voltage:
                    sp_read_value = "1" + sp_read_value
                elif value < 0.12 * self.vdd_voltage:
                    sp_read_value = "0" + sp_read_value
                else:
                    error ="FAILED: {0}_{1} value {2} at time {3}n does not fall within noise margins <{4} or >{5}.".format(dout_port,
                                                                                                                            bit,
                                                                                                                            value,
                                                                                                                            eo_period,
                                                                                                                            0.12*self.vdd_voltage,
                                                                                                                            0.88*self.vdd_voltage)
                    return (0, error)
                    
            self.read_check.append([sp_read_value, dout_port, eo_period, check])                    
        return (1, "SUCCESS")
        
    def check_stim_results(self):
        for i in range(len(self.write_check)):
            if self.write_check[i][0] != self.read_check[i][0]:
                error = "FAILED: {0} value {1} does not match written value {2} read during cycle {3} at time {4}n".format(self.read_check[i][1],
                                                                                                                           self.read_check[i][0],
                                                                                                                           self.write_check[i][0],
                                                                                                                           int((self.read_check[i][2]-self.period)/self.period),
                                                                                                                           self.read_check[i][2])
                return(0, error)
        return(1, "SUCCESS")
        
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
            
    def create_signal_names(self):
        self.addr_name = "A"
        self.din_name = "DIN"
        self.dout_name = "DOUT"
            
    def write_functional_stimulus(self):
        """ Writes SPICE stimulus. """
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
        self.stim.inst_sram(sram=self.sram,
                            port_signal_names=(self.addr_name,self.din_name,self.dout_name),
                            port_info=(self.total_ports, self.write_index, self.read_index),
                            abits=self.addr_size,
                            dbits=self.word_size,
                            sram_name=self.name)

        # Add load capacitance to each of the read ports
        self.sf.write("\n* SRAM output loads\n")
        for port in range(self.total_read):
            for bit in range(self.word_size):
                sig_name="{0}{1}_{2} ".format(self.dout_name, self.read_index[port], bit)
                self.sf.write("CD{0}{1} {2} 0 {3}f\n".format(self.read_index[port], bit, sig_name, self.load))
                
        # Write debug comments to stim file
        self.sf.write("\n\n * Sequence of operations\n")
        for comment in self.fn_cycle_comments:
            self.sf.write("*{}\n".format(comment))
                
        # Generate data input bits 
        self.sf.write("\n* Generation of data and address signals\n")
        for port in range(self.total_write):
            for bit in range(self.word_size):
                sig_name="{0}{1}_{2} ".format(self.din_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[port][bit], self.period, self.slew, 0.05)
        
        # Generate address bits
        for port in range(self.total_ports):
            for bit in range(self.addr_size):
                sig_name="{0}{1}_{2} ".format(self.addr_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][bit], self.period, self.slew, 0.05)

        # Generate control signals
        self.sf.write("\n * Generation of control signals\n")
        for port in range(self.total_ports):
            self.stim.gen_pwl("CSB{}".format(port), self.cycle_times , self.csb_values[port], self.period, self.slew, 0.05)
            
        for port in range(self.num_rw_ports):
            self.stim.gen_pwl("WEB{}".format(port), self.cycle_times , self.web_values[port], self.period, self.slew, 0.05)

        # Generate CLK signals
        for port in range(self.total_ports):
            self.stim.gen_pulse(sig_name="{0}{1}".format(tech.spice["clk"], port),
                                v1=self.gnd_voltage,
                                v2=self.vdd_voltage,
                                offset=self.period,
                                period=self.period,
                                t_rise=self.slew,
                                t_fall=self.slew)
        
        # Generate DOUT value measurements
        self.sf.write("\n * Generation of dout measurements\n")
        for (word, dout_port, eo_period, check) in self.write_check:
            t_intital = eo_period - 0.01*self.period
            t_final = eo_period + 0.01*self.period
            for bit in range(self.word_size):
                self.stim.gen_meas_value(meas_name="V{0}_{1}ck{2}".format(dout_port,bit,check),
                                         dout="{0}_{1}".format(dout_port,bit),
                                         t_intital=t_intital,
                                         t_final=t_final)
        
        self.stim.write_control(self.cycle_times[-1] + self.period)
        self.sf.close()


