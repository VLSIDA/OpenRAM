import sys,re,shutil
from design import design
import debug
import math
import tech
import random
from .stimuli import *
from .trim_spice import *
from .charutils import *
import utils
from globals import OPTS

class simulation():

    def __init__(self, sram, spfile, corner):
        self.sram = sram
        
        self.name = self.sram.name
        self.word_size = self.sram.word_size
        self.addr_size = self.sram.addr_size
        self.num_cols = self.sram.num_cols
        self.num_rows = self.sram.num_rows
        self.num_banks = self.sram.num_banks
        self.sp_file = spfile
        
        self.total_ports = self.sram.total_ports
        self.total_write = self.sram.total_write
        self.total_read = self.sram.total_read
        self.read_index = self.sram.read_index
        self.write_index = self.sram.write_index
        self.num_rw_ports = self.sram.num_rw_ports
        self.port_id = self.sram.port_id

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
        # Clock signals
        self.cycle_times = []
        self.t_current = 0
        
        # control signals: only one cs_b for entire multiported sram, one we_b for each write port
        self.csb_values = [[] for port in range(self.total_ports)]
        self.web_values = [[] for port in range(self.num_rw_ports)]
        
        # Three dimensional list to handle each addr and data bits for wach port over the number of checks
        self.addr_values = [[[] for bit in range(self.addr_size)] for port in range(self.total_ports)]
        self.data_values = [[[] for bit in range(self.word_size)] for port in range(self.total_write)]
        
        # For generating comments in SPICE stimulus
        self.cycle_comments = []

    def add_control_one_port(self, port, op):
        """Appends control signals for operation to a given port"""
        #Determine values to write to port
        web_val = 1
        csb_val = 1
        if op == "read":
            csb_val = 0
        elif op == "write":
            csb_val = 0
            web_val = 0
        elif op != "noop":
            debug.error("Could not add control signals for port {0}. Command {1} not recognized".format(port,op),1)
        
        # Append the values depending on the type of port
        self.csb_values[port].append(csb_val)
        # If port is in both lists, add rw control signal. Condition indicates its a RW port.
        if port < self.num_rw_ports:
            self.web_values[port].append(web_val)
            
    def add_data(self, data, port):
        """ Add the array of data values """
        debug.check(len(data)==self.word_size, "Invalid data word size.")
        #debug.check(port < len(self.data_values), "Port number cannot index data values.")
        
        bit = self.word_size - 1
        for c in data:
            if c=="0":
                self.data_values[port][bit].append(0)
            elif c=="1":
                self.data_values[port][bit].append(1)
            else:
                debug.error("Non-binary data string",1)
            bit -= 1

    def add_address(self, address, port):
        """ Add the array of address values """
        debug.check(len(address)==self.addr_size, "Invalid address size.")
        
        bit = self.addr_size - 1
        for c in address:
            if c=="0":
                self.addr_values[port][bit].append(0)
            elif c=="1":
                self.addr_values[port][bit].append(1)
            else:
                debug.error("Non-binary address string",1)
            bit -= 1
                
    def add_write(self, comment, address, data, port):
        """ Add the control values for a write cycle. """
        debug.info(1, comment)
        debug.check(port in self.write_index, "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port, self.write_index))
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                                     self.t_current,
                                                                                     comment,
                                                                                     port))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        self.add_control_one_port(port, "write")
        self.add_data(data,port)
        self.add_address(address,port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in range(self.total_ports):
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, unselected_port)
                    
    def add_read(self, comment, address, data, port):
        """ Add the control values for a read cycle. """
        debug.info(1, comment)
        debug.check(port in self.read_index, "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port, self.read_index))
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                                     self.t_current,
                                                                                     comment,
                                                                                     port))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.add_control_one_port(port, "read")
        
        #If the port is also a readwrite then add data.
        if port in self.write_index:
            self.add_data(data,port)
        self.add_address(address, port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in range(self.total_ports):
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, unselected_port)

    def add_noop_all_ports(self, comment, address, data):
        """ Add the control values for a noop to all ports. """
        debug.info(1, comment)
        self.cycle_comments.append("Cycle {0:2d}\tPort All\t{1:5.2f}ns:\t{2}".format(len(self.cycle_times),
                                                                                     self.t_current,
                                                                                     comment))
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
         
        for port in range(self.total_ports):
            self.add_noop_one_port(address, data, port)
            
    def add_write_one_port(self, comment, address, data, port):
        """ Add the control values for a write cycle. Does not increment the period. """
        debug.check(port in self.write_index, "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port, self.write_index))
        debug.info(1, comment)
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                                     self.t_current,
                                                                                     comment,
                                                                                     port))
        self.add_control_one_port(port, "write")
        self.add_data(data,port)
        self.add_address(address,port)
                
    def add_read_one_port(self, comment, address, data, port):
        """ Add the control values for a read cycle. Does not increment the period. """
        debug.check(port in self.read_index, "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port, self.read_index))
        debug.info(1, comment)
        self.cycle_comments.append("Cycle {0:2d}\tPort {3}\t{1:5.2f}ns:\t{2}".format(len(self.cycle_comments),
                                                                                     self.t_current,
                                                                                     comment,
                                                                                     port))
        self.add_control_one_port(port, "read")
        #If the port is also a readwrite then add data.
        if port in self.write_index:
            self.add_data(data,port)
        self.add_address(address, port)
                
    def add_noop_one_port(self, address, data, port):
        """ Add the control values for a noop to a single port. Does not increment the period. """   
        self.add_control_one_port(port, "noop")
        if port in self.write_index:
            self.add_data(data,port)
        self.add_address(address, port)
        