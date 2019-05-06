# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
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

class worst_case(delay):
    """Functions to test for the worst case delay in a target SRAM

    The current worst case determines a feasible period for the SRAM then tests
    several bits and record the delay and differences between the bits.

    """

    def __init__(self, sram, spfile, corner):
        delay.__init__(self,sram,spfile,corner)
        
      
    def analyze(self,probe_address, probe_data, slews, loads):
        """
        Main function to test the delays of different bits.
        """
        debug.check(OPTS.num_rw_ports < 2 and OPTS.num_w_ports < 1 and OPTS.num_r_ports < 1 ,
                    "Bit testing does not currently support multiport.")
        #Dict to hold all characterization values
        char_sram_data = {}
        
        self.set_probe(probe_address, probe_data)
        #self.prepare_netlist()
        
        self.load=max(loads)
        self.slew=max(slews)
        
        # 1) Find a feasible period and it's corresponding delays using the trimmed array.
        feasible_delays = self.find_feasible_period()
        
        # 2) Find the delays of several bits
        test_bits = self.get_test_bits()
        bit_delays = self.simulate_for_bit_delays(test_bits)
        
        for i in range(len(test_bits)):
            debug.info(1, "Bit tested: addr {0[0]} data_pos {0[1]}\n Values {1}".format(test_bits[i], bit_delays[i]))
    
    def simulate_for_bit_delays(self, test_bits):
        """Simulates the delay of the sram of over several bits."""
        bit_delays = [{} for i in range(len(test_bits))]
        
        #Assumes a bitcell with only 1 rw port. (6t, port 0)
        port = 0
        self.targ_read_ports = [self.read_ports[port]]
        self.targ_write_ports = [self.write_ports[port]]
        
        for i in range(len(test_bits)):
            (bit_addr, bit_data) = test_bits[i]
            self.set_probe(bit_addr, bit_data)
            debug.info(1,"Delay bit test: period {}, addr {}, data_pos {}".format(self.period, bit_addr, bit_data))
            (success, results)=self.run_delay_simulation()
            debug.check(success, "Bit Test Failed: period {}, addr {}, data_pos {}".format(self.period, bit_addr, bit_data))
            bit_delays[i] = results[port]
            
        return bit_delays
        
        
    def get_test_bits(self):
        """Statically determines address and bit values to test"""
        #First and last address, first middle, and last bit. Last bit is repeated twice with different data position.
        bit_addrs = ["0"*self.addr_size, "0"+"1"*(self.addr_size-1), "1"*self.addr_size, "1"*self.addr_size]
        data_positions = [0, (self.word_size-1)//2, 0, self.word_size-1]
        #Return them in a tuple form
        return [(bit_addrs[i], data_positions[i]) for i in range(len(bit_addrs))]
        
    
