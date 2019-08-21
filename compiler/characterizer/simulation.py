# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys,re,shutil
from design import design
import debug
import math
import tech
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
        self.write_size = self.sram.write_size
        self.sp_file = spfile
        
        self.all_ports = self.sram.all_ports
        self.readwrite_ports = self.sram.readwrite_ports
        self.read_ports = self.sram.read_ports
        self.write_ports = self.sram.write_ports
        if self.write_size:
            self.num_wmasks = int(self.word_size/self.write_size)
        else:
            self.num_wmasks = 0


    def set_corner(self,corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner

    def set_spice_constants(self):
        """ sets feasible timing parameters """
        self.period = tech.spice["feasible_period"]
        self.slew = tech.spice["rise_time"]*2
        self.load = tech.spice["msflop_in_cap"]*4

        self.v_high = self.vdd_voltage - tech.spice["v_threshold_typical"]
        self.v_low = tech.spice["v_threshold_typical"]        
        self.gnd_voltage = 0
        
    def create_signal_names(self):
        self.addr_name = "a"
        self.din_name = "din"
        self.dout_name = "dout"
        self.pins = self.gen_pin_names(port_signal_names=(self.addr_name,self.din_name,self.dout_name),
                                       port_info=(len(self.all_ports),self.write_ports,self.read_ports),
                                       abits=self.addr_size,
                                       dbits=self.word_size)
        debug.check(len(self.sram.pins) == len(self.pins), "Number of pins generated for characterization \
                 do match pins of SRAM\nsram.pins = {0}\npin_names = {1}".format(self.sram.pins,self.pins))
        #This is TODO once multiport control has been finalized.
        #self.control_name = "CSB"    
        
    def set_stimulus_variables(self):
        # Clock signals
        self.cycle_times = []
        self.t_current = 0
        
        # control signals: only one cs_b for entire multiported sram, one we_b for each write port
        self.csb_values = [[] for port in self.all_ports]
        self.web_values = [[] for port in self.readwrite_ports]
        
        # Three dimensional list to handle each addr and data bits for wach port over the number of checks
        self.addr_values = [[[] for bit in range(self.addr_size)] for port in self.all_ports]
        self.data_values = [[[] for bit in range(self.word_size)] for port in self.write_ports]
        self.wmask_values = [[[] for bit in range(self.num_wmasks)] for port in self.write_ports]
        
        # For generating comments in SPICE stimulus
        self.cycle_comments = []
        self.fn_cycle_comments = []

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
        if port in self.readwrite_ports:
            self.web_values[port].append(web_val)
            
    def add_data(self, data, port):
        """ Add the array of data values """
        debug.check(len(data)==self.word_size, "Invalid data word size.")
        
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

    def add_wmask(self, wmask, port):
        """ Add the array of address values """
        debug.check(len(wmask) == self.num_wmasks, "Invalid wmask size.")

        bit = self.num_wmasks - 1
        for c in wmask:
            if c == "0":
                self.wmask_values[port][bit].append(0)
            elif c == "1":
                self.wmask_values[port][bit].append(1)
            else:
                debug.error("Non-binary wmask string", 1)
            bit -= 1
                
    def add_write(self, comment, address, data, wmask, port):
        """ Add the control values for a write cycle. """
        debug.check(port in self.write_ports, "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port, self.write_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment(port, comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        
        self.add_control_one_port(port, "write")
        self.add_data(data,port)
        self.add_address(address,port)
        self.add_wmask(wmask,port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in self.all_ports:
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, wmask, unselected_port)
                    
    def add_read(self, comment, address, din_data, wmask, port):
        """ Add the control values for a read cycle. """
        debug.check(port in self.read_ports, "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port, self.read_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment(port, comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.add_control_one_port(port, "read")
        
        #If the port is also a readwrite then add data.
        if port in self.write_ports:
            self.add_data(din_data,port)
            self.add_wmask(wmask,port)
        self.add_address(address, port)
        
        #This value is hard coded here. Possibly change to member variable or set in add_noop_one_port
        noop_data = "0"*self.word_size
        #Add noops to all other ports.
        for unselected_port in self.all_ports:
            if unselected_port != port:
                self.add_noop_one_port(address, noop_data, wmask, unselected_port)

    def add_noop_all_ports(self, comment, address, data, wmask):
        """ Add the control values for a noop to all ports. """
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment("All", comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period
         
        for port in self.all_ports:
            self.add_noop_one_port(address, data, wmask, port)

    def add_write_one_port(self, comment, address, data, wmask, port):
        """ Add the control values for a write cycle. Does not increment the period. """
        debug.check(port in self.write_ports, "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port, self.write_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)

        self.add_control_one_port(port, "write")
        self.add_data(data,port)
        self.add_address(address,port)
        self.add_wmask(wmask,port)
                
    def add_read_one_port(self, comment, address, din_data, wmask, port):
        """ Add the control values for a read cycle. Does not increment the period. """
        debug.check(port in self.read_ports, "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port, self.read_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        
        self.add_control_one_port(port, "read")
        #If the port is also a readwrite then add data.
        if port in self.write_ports:
            self.add_data(din_data,port)
            self.add_wmask(wmask,port)
        self.add_address(address, port)
                
    def add_noop_one_port(self, address, data, wmask, port):
        """ Add the control values for a noop to a single port. Does not increment the period. """   
        self.add_control_one_port(port, "noop")
        if port in self.write_ports:
            self.add_data(data,port)
            self.add_wmask(wmask,port)
        self.add_address(address, port)

    def append_cycle_comment(self, port, comment):
        """Add comment to list to be printed in stimulus file"""
        #Clean up time before appending. Make spacing dynamic as well.
        time = "{0:.2f} ns:".format(self.t_current)
        time_spacing = len(time)+6
        self.cycle_comments.append("Cycle {0:<6d} Port {1:<6} {2:<{3}}: {4}".format(len(self.cycle_times),
                                                                           port,
                                                                           time,
                                                                           time_spacing,
                                                                           comment))  
        
    def gen_cycle_comment(self, op, word, addr, wmask, port, t_current):
        if op == "noop":
            comment = "\tIdle during cycle {0} ({1}ns - {2}ns)".format(int(t_current/self.period),
                                                                     t_current,
                                                                     t_current+self.period)
        elif op == "write":
            comment = "\tWriting {0}  to  address {1} (from port {2}) during cycle {3} ({4}ns - {5}ns)".format(word,
                                                                                                               addr,
                                                                                                               port,
                                                                                                               int(t_current/self.period),
                                                                                                               t_current,
                                                                                                               t_current+self.period)
        elif op == "partial_write":
            comment = "\tWriting (partial) {0}  to  address {1} with mask bit {2} (from port {3}) during cycle {4} ({5}ns - {6}ns)".format(word,
                                                                                                                                           addr,
                                                                                                                                           wmask,
                                                                                                                                           port,
                                                                                                                                           int(t_current / self.period),
                                                                                                                                           t_current,
                                                                                                                                           t_current + self.period)
        else:
            comment = "\tReading {0} from address {1} (from port {2}) during cycle {3} ({4}ns - {5}ns)".format(word,
                                                                                                               addr,
                                                                                                               port,
                                                                                                               int(t_current/self.period),
                                                                                                               t_current,
                                                                                                               t_current+self.period)

        
        return comment
        
    def gen_pin_names(self, port_signal_names, port_info, abits, dbits):
        """Creates the pins names of the SRAM based on the no. of ports."""
        #This may seem redundant as the pin names are already defined in the sram. However, it is difficult 
        #to extract the functionality from the names, so they are recreated. As the order is static, changing 
        #the order of the pin names will cause issues here.
        pin_names = []
        (addr_name, din_name, dout_name) = port_signal_names
        (total_ports, write_index, read_index) = port_info
        
        for write_input in write_index:
            for i in range(dbits):
                pin_names.append("{0}{1}_{2}".format(din_name,write_input, i))
        
        for port in range(total_ports):
            for i in range(abits):
                pin_names.append("{0}{1}_{2}".format(addr_name,port,i))    

        #Control signals not finalized.
        for port in range(total_ports):
            pin_names.append("CSB{0}".format(port))
        for port in range(total_ports):
            if (port in read_index) and (port in write_index):
                pin_names.append("WEB{0}".format(port))

        for port in range(total_ports):
            pin_names.append("{0}{1}".format(tech.spice["clk"], port))

        if self.write_size:
            for port in write_index:
                for bit in range(self.num_wmasks):
                    pin_names.append("WMASK{0}_{1}".format(port,bit))
            
        for read_output in read_index:
            for i in range(dbits):
                pin_names.append("{0}{1}_{2}".format(dout_name,read_output, i))
                
        pin_names.append("{0}".format(tech.spice["vdd_name"]))
        pin_names.append("{0}".format(tech.spice["gnd_name"]))
        return pin_names
        
