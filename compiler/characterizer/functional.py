import sys,re,shutil
import debug
import math
import tech
import random
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS


class functional():
    """
       Functions to write random data values to a random address then read them back and check
       for successful SRAM operation.
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
        
        self.total_write = OPTS.num_rw_ports + OPTS.num_w_ports
        self.total_read = OPTS.num_rw_ports + OPTS.num_r_ports
        self.total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports
    
        # These are the member variables for a simulation
        self.set_corner(corner)
        self.set_spice_constants()
        self.set_stimulus_variables()
        
        # Number of checks can be changed
        self.num_checks = 1

    def set_corner(self,corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner
    
    def set_spice_constants(self):
        """ sets feasible timing parameters """
        self.period = tech.spice["feasible_period"]
        self.slew = tech.spice["rise_time"]*2
        self.load = tech.spice["msflop_in_cap"]*4
        self.gnd_voltage = 0
        
    def set_stimulus_variables(self):
        """ Variables relevant to functional test """
        self.cycles = 0
        self.written_words = []
        
        # control signals: only one cs_b for entire multiported sram, one we_b for each write port
        self.cs_b = []
        self.we_b = [[] for port in range(self.total_write)]
        
        # "end of period" signal used to keep track of when read output should be analyzed
        self.eo_period = []
        
        # Three dimensional list to handle each addr and data bits for wach port over the number of checks
        self.addresses = [[[] for bit in range(self.addr_size)] for port in range(self.total_write)]
        self.data = [[[] for bit in range(self.word_size)] for port in range(self.total_write)]
        
    def run(self):
        """ Main function to generate random writes/reads, run spice, and analyze results """ 
        # Need a NOOP to enable the chip
        # Old code. Is this still necessary?
        self.first_run()
        
        # Generate write and read signals for spice stimulus
        for i in range(self.num_checks):
            addr = self.gen_addr()
            word = self.gen_data()
            self.write(addr,word)
            self.read(addr,word)
        
        self.write_functional_stimulus()
        self.stim.run_sim()
        
        # Extrat DOUT values from spice timing.lis
        read_value = parse_spice_list("timing", "vdout0[0]")
        print("READ VALUE = {}".format(read_value))
    
    def first_run(self):
        """ First cycle as noop to enable chip """
        self.cycles = self.cycles + 1
        
        self.cs_b.append(1)
        for port in range(self.total_write):        
            self.we_b[port].append(1)

        for port in range(self.total_write):     
            for bit in range(self.addr_size):
                self.addresses[port][bit].append(0)
        
        for port in range(self.total_write):    
            for bit in range(self.word_size):
                self.data[port][bit].append(0)
    
    def write(self,addr,word,write_port=0):
        """ Generates signals for a write cycle """
        print("Writing {0} to {1}...".format(word,addr))
        self.written_words.append(word)
        self.cycles = self.cycles + 1
        
        # Write control signals
        self.cs_b.append(0)
        self.we_b[write_port].append(0)
        for port in range(self.total_write):
            if port == write_port:
                continue
            else:
                self.we_b[port].append(1)

        # Write address
        for port in range(self.total_write):
            for bit in range(self.addr_size):
                current_address_bit = int(addr[bit])
                self.addresses[port][bit].append(current_address_bit)
        
        # Write data
        for port in range(self.total_write):
            for bit in range(self.word_size):
                current_word_bit = int(word[bit])
                self.data[port][bit].append(current_word_bit)

    def read(self,addr,word):
        """ Generates signals for a read cycle """
        print("Reading {0} from {1}...".format(word,addr))
        self.cycles = self.cycles + 2
        
        # Read control signals
        self.cs_b.append(0)
        for port in range(self.total_write):
            self.we_b[port].append(1)

        # Read address
        for port in range(self.total_write):
            for bit in range(self.addr_size):
                current_address_bit = int(addr[bit])
                self.addresses[port][bit].append(current_address_bit)
            
        # Data input doesn't matter during read cycle, so arbitrarily set to 0 for simulation
        for port in range(self.total_write):
            for bit in range(self.word_size):
                self.data[port][bit].append(0)
        
        
        # Add idle cycle since read may take more than 1 cycle
        # Idle control signals
        self.cs_b.append(1)
        for port in range(self.total_write):
            self.we_b[port].append(1)

        # Address doesn't matter during idle cycle, but keep the same as read for easier debugging
        for port in range(self.total_write):
            for bit in range(self.addr_size):
                current_address_bit = int(addr[bit])
                self.addresses[port][bit].append(current_address_bit)
        
        # Data input doesn't matter during idle cycle, so arbitrarily set to 0 for simulation
        for port in range(self.total_write):        
            for bit in range(self.word_size):
                self.data[port][bit].append(0)
        
        
        # Record the end of the period that the read operation occured in
        self.eo_period.append(self.cycles * self.period)

    def gen_data(self):
        """ Generates a random word to write """
        rand = random.randint(0,(2**self.word_size)-1)
        data_bits = self.convert_to_bin(rand,False)
        return data_bits

    def gen_addr(self):
        """ Generates a random address value to write to """
        rand = random.randint(0,(2**self.addr_size)-1)  
        addr_bits = self.convert_to_bin(rand,True)
        return addr_bits 

    def get_data(self):
        """ Gets an available address and corresponding word """
        # Currently unused but may need later depending on how the functional test develops
        addr = random.choice(self.stored_words.keys())
        word = self.stored_words[addr]
        return (addr,word)

    def convert_to_bin(self,value,is_addr):
        """ Converts addr & word to usable binary values """
        new_value = str.replace(bin(value),"0b","")
        if(is_addr):
            expected_value = self.addr_size
        else:
            expected_value = self.word_size
        for i in range (expected_value - len(new_value)):
            new_value =  "0" + new_value
            
        print("Binary Conversion: {} to {}".format(value, new_value))
        return new_value

    def obtain_cycle_times(self,period):
        """ Generate clock cycle times based on period and number of cycles """
        t_current = 0
        self.cycle_times = []
        for i in range(self.cycles):
            self.cycle_times.append(t_current)
            t_current += period 
    
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
        for write_port_num in range(OPTS.num_rw_ports, OPTS.num_rw_ports+OPTS.num_w_ports):
            self.write_ports.append(write_port_num)
        for read_port_num in range(OPTS.num_rw_ports+OPTS.num_w_ports, OPTS.num_rw_ports+OPTS.num_w_ports+OPTS.num_r_ports):
            self.read_ports.append(read_port_num)
            
        self.read_index = []
        port_number = 0
        for port in range(OPTS.num_rw_ports):
            self.read_index.append("{}".format(port_number))
            port_number += 1
        for port in range(OPTS.num_w_ports):
            port_number += 1
        for port in range(OPTS.num_r_ports):
            self.read_index.append("{}".format(port_number))
            port_number += 1

    def write_functional_stimulus(self):
        #Write Stimulus
        
        self.obtain_cycle_times(self.period)
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

        self.create_port_names()
        
        #Instantiate the SRAM
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_sram(abits=self.addr_size, 
                            dbits=self.word_size, 
                            port_info=(self.total_port_num,self.readwrite_port_num,self.read_ports,self.write_ports),
                            sram_name=self.name)

        # Add load capacitance to each of the read ports
        self.sf.write("\n* SRAM output loads\n")
        for port in range(self.total_read):
            for bit in range(self.word_size):
                self.sf.write("CD{0}{1} DOUT{0}[{1}] 0 {2}f\n".format(port, bit, self.load))
                
        # Generate data input bits 
        self.sf.write("\n* Generation of data and address signals\n")
        for port in range(self.total_write):
            for bit in range(self.word_size):
                sig_name = "DIN{0}[{1}]".format(port,bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data[port][bit], self.period, self.slew, 0.05)
        
        # Generate address bits
        for port in range(self.total_write):
            for bit in range(self.addr_size):
                sig_name = "A{0}[{1}]".format(port,bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addresses[port][bit], self.period, self.slew, 0.05)

        # Generate control signals
        self.sf.write("\n * Generation of control signals\n")
        self.stim.gen_pwl("CSB0", self.cycle_times , self.cs_b, self.period, self.slew, 0.05)
        for port in range(self.total_write):
            self.stim.gen_pwl("WEB{}".format(port), self.cycle_times , self.we_b[port], self.period, self.slew, 0.05)

        # Generate CLK
        self.stim.gen_pulse(sig_name="CLK",
                            v1=self.gnd_voltage,
                            v2=self.vdd_voltage,
                            offset=self.period,
                            period=self.period,
                            t_rise=self.slew,
                            t_fall=self.slew)
        
        # Generate DOUT value measurements
        self.sf.write("\n * Generation of dout measurements\n")
        for i in range(self.num_checks):
            for port in range(self.total_read):
                for bit in range(self.word_size):
                    self.stim.gen_meas_value(meas_name="VDOUT{0}[{1}]".format(port,bit),
                                             dout="DOUT{0}[{1}]".format(port,bit),
                                             eo_period=self.eo_period[i],
                                             slew=self.slew,
                                             setup=0.05)
        
        self.stim.write_control(self.cycle_times[-1] + self.period)
        self.sf.close()


