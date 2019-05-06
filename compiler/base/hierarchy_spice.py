# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import debug
import re
import os
import math
import tech

class spice():
    """
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    Class consisting of a set of modules and instances of these modules
    """

    def __init__(self, name):
        self.name = name

        # Holds subckts/mods for this module
        self.mods = []  
        # Holds the pins for this module
        self.pins = []
        # The type map of each pin: INPUT, OUTPUT, INOUT, POWER, GROUND
        # for each instance, this is the set of nets/nodes that map to the pins for this instance
        self.pin_type = {} 
        # THE CONNECTIONS MUST MATCH THE ORDER OF THE PINS (restriction imposed by the
        # Spice format)
        self.conns = []
        # Keep track of any comments to add the the spice
        try:
            self.commments
        except:
            self.comments = []

        self.sp_read()

############################################################
# Spice circuit
############################################################

    def add_comment(self, comment):
        """ Add a comment to the spice file """
        try:
            self.commments
        except:
            self.comments = []
        else:
            self.comments.append(comment)
        
    def add_pin(self, name, pin_type="INOUT"):
        """ Adds a pin to the pins list. Default type is INOUT signal. """
        self.pins.append(name)
        self.pin_type[name]=pin_type

    def add_pin_list(self, pin_list, pin_type_list="INOUT"):
        """ Adds a pin_list to the pins list """
        # The type list can be a single type for all pins
        # or a list that is the same length as the pin list.
        if type(pin_type_list)==str:
            for pin in pin_list:
                self.add_pin(pin,pin_type_list)
        elif len(pin_type_list)==len(pin_list):
            for (pin,ptype) in zip(pin_list, pin_type_list):
                self.add_pin(pin,ptype)
        else:
            debug.error("Mismatch in type and pin list lengths.", -1)

    def get_pin_type(self, name):
        """ Returns the type of the signal pin. """
        return self.pin_type[name]

    def get_pin_dir(self, name):
        """ Returns the direction of the pin. (Supply/ground are INOUT). """
        if self.pin_type[name] in ["POWER","GROUND"]:
            return "INOUT"
        else:
            return self.pin_type[name]
        
    def get_inputs(self):
        """ These use pin types to determine pin lists. These
        may be over-ridden by submodules that didn't use pin directions yet."""
        input_list = []
        for pin in self.pins:
            if self.pin_type[pin]=="INPUT":
                input_list.append(pin)
        return input_list

    def get_outputs(self):
        """ These use pin types to determine pin lists. These
        may be over-ridden by submodules that didn't use pin directions yet."""
        output_list = []
        for pin in self.pins:
            if self.pin_type[pin]=="OUTPUT":
                output_list.append(pin)
        return output_list


    def add_mod(self, mod):
        """Adds a subckt/submodule to the subckt hierarchy"""
        self.mods.append(mod)

    def connect_inst(self, args, check=True):
        """Connects the pins of the last instance added
        It is preferred to use the function with the check to find if
        there is a problem. The check option can be set to false
        where we dynamically generate groups of connections after a
        group of modules are generated."""

        if (check and (len(self.insts[-1].mod.pins) != len(args))):
            from pprint import pformat
            modpins_string=pformat(self.insts[-1].mod.pins)
            argpins_string=pformat(args)
            debug.error("Mod  connections: {}".format(modpins_string))
            debug.error("Inst connections: {}".format(argpins_string))
            debug.error("Number of net connections ({0}) does not match last instance ({1})".format(len(self.insts[-1].mod.pins),
                                                                                                    len(args)), 1)
        self.conns.append(args)

        if check and (len(self.insts)!=len(self.conns)):
            from pprint import pformat
            insts_string=pformat(self.insts)
            conns_string=pformat(self.conns)
            
            debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.name,
                                                                                        len(self.insts),
                                                                                        len(self.conns)))
            debug.error("Instances: \n"+str(insts_string))
            debug.error("-----")
            debug.error("Connections: \n"+str(conns_string),1)



    def sp_read(self):
        """Reads the sp file (and parse the pins) from the library 
           Otherwise, initialize it to null for dynamic generation"""
        if self.sp_file and os.path.isfile(self.sp_file):
            debug.info(3, "opening {0}".format(self.sp_file))
            f = open(self.sp_file)
            self.spice = f.readlines()
            for i in range(len(self.spice)):
                self.spice[i] = self.spice[i].rstrip(" \n")
            f.close()

            # find the correct subckt line in the file
            subckt = re.compile("^.subckt {}".format(self.name), re.IGNORECASE)
            subckt_line = list(filter(subckt.search, self.spice))[0]
            # parses line into ports and remove subckt
            self.pins = subckt_line.split(" ")[2:]
        else:
            self.spice = []

    def contains(self, mod, modlist):
        for x in modlist:
            if x.name == mod.name:
                return True
        return False

    def sp_write_file(self, sp, usedMODS):
        """ Recursive spice subcircuit write;
            Writes the spice subcircuit from the library or the dynamically generated one"""
        if not self.spice:
            # recursively write the modules
            for i in self.mods:
                if self.contains(i, usedMODS):
                    continue
                usedMODS.append(i)
                i.sp_write_file(sp, usedMODS)

            if len(self.insts) == 0:
                return
            if self.pins == []:
                return

            
            # write out the first spice line (the subcircuit)
            sp.write("\n.SUBCKT {0} {1}\n".format(self.name,
                                                  " ".join(self.pins)))

            for line in self.comments:
                sp.write("* {}\n".format(line))
                    
            # every instance must have a set of connections, even if it is empty.
            if  len(self.insts)!=len(self.conns):
                debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.name,
                                                                                            len(self.insts),
                                                                                            len(self.conns)))
                debug.error("Instances: \n"+str(self.insts))
                debug.error("-----")
                debug.error("Connections: \n"+str(self.conns),1)



            for i in range(len(self.insts)):
                # we don't need to output connections of empty instances.
                # these are wires and paths
                if self.conns[i] == []:
                    continue
                if hasattr(self.insts[i].mod,"spice_device"):
                    sp.write(self.insts[i].mod.spice_device.format(self.insts[i].name,
                                                                   " ".join(self.conns[i])))
                    sp.write("\n")

                else:
                    sp.write("X{0} {1} {2}\n".format(self.insts[i].name,
                                                     " ".join(self.conns[i]),
                                                     self.insts[i].mod.name))

            sp.write(".ENDS {0}\n".format(self.name))

        else:
            # write the subcircuit itself
            # Including the file path makes the unit test fail for other users.
            #if os.path.isfile(self.sp_file):
            #    sp.write("\n* {0}\n".format(self.sp_file))
            sp.write("\n".join(self.spice))
            
            sp.write("\n")

    def sp_write(self, spname):
        """Writes the spice to files"""
        debug.info(3, "Writing to {0}".format(spname))
        spfile = open(spname, 'w')
        spfile.write("*FIRST LINE IS A COMMENT\n")
        usedMODS = list()
        self.sp_write_file(spfile, usedMODS)
        del usedMODS
        spfile.close()

    def analytical_delay(self, corner, slew, load=0.0):
        """Inform users undefined delay module while building new modules"""
        debug.warning("Design Class {0} delay function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__, 
                              self.name))         
        # return 0 to keep code running while building
        return delay_data(0.0, 0.0)

    def cal_delay_with_rc(self, corner, r, c ,slew, swing = 0.5):
        """ 
        Calculate the delay of a mosfet by 
        modeling it as a resistance driving a capacitance
        """
        swing_factor = abs(math.log(1-swing)) # time constant based on swing
        delay = swing_factor * r * c #c is in ff and delay is in fs
        delay = self.apply_corners_analytically(delay, corner)
        delay = delay * 0.001 #make the unit to ps
        
        # Output slew should be linear to input slew which is described 
        # as 0.005* slew.

        # The slew will be also influenced by the delay.
        # If no input slew(or too small to make impact) 
        # The mimum slew should be the time to charge RC. 
        # Delay * 2 is from 0 to 100%  swing. 0.6*2*delay is from 20%-80%.
        slew = delay * 0.6 * 2 + 0.005 * slew
        return delay_data(delay = delay, slew = slew)

    def apply_corners_analytically(self, delay, corner):
        """Multiply delay by corner factors"""
        proc,vdd,temp = corner
        #FIXME: type of delay is needed to know which process to use.
        proc_mult = max(self.get_process_delay_factor(proc)) 
        volt_mult = self.get_voltage_delay_factor(vdd)
        temp_mult = self.get_temp_delay_factor(temp)
        return delay * proc_mult * volt_mult * temp_mult
        
    def get_process_delay_factor(self, proc):
        """Returns delay increase estimate based off process
           Currently does +/-10 for fast/slow corners."""
        proc_factors = []
        for mos_proc in proc:
            if mos_proc == 'T':
                proc_factors.append(1.0)
            elif mos_proc == 'F':
                proc_factors.append(0.9)
            elif mos_proc == 'S':
                proc_factors.append(1.1)  
        return proc_factors
        
    def get_voltage_delay_factor(self, voltage):
        """Returns delay increase due to voltage.
           Implemented as linear factor based off nominal voltage.
        """
        return tech.spice['vdd_nominal']/voltage
        
    def get_temp_delay_factor(self, temp):
        """Returns delay increase due to temperature (in C).
           Determines effect on threshold voltage and then linear factor is estimated.
        """
        #Some portions of equation condensed (phi_t = k*T/q for T in Kelvin) in mV
        #(k/q)/100 = .008625, The division 100 simplifies the conversion from C to K and mV to V
        thermal_voltage_nom = .008625*tech.spice["temp_nominal"]
        thermal_voltage = .008625*temp
        vthresh = (tech.spice["v_threshold_typical"]+2*(thermal_voltage-thermal_voltage_nom))
        #Calculate effect on Vdd-Vth. The current vdd is not used here. A separate vdd factor is calculated.
        return (tech.spice['vdd_nominal'] - tech.spice["v_threshold_typical"])/(tech.spice['vdd_nominal']-vthresh)

    def return_delay(self, delay, slew):
        return delay_data(delay, slew)

    def generate_rc_net(self,lump_num, wire_length, wire_width):
        return wire_spice_model(lump_num, wire_length, wire_width)
        
    def calc_dynamic_power(self, corner, c, freq, swing=1.0):
        """ 
        Calculate dynamic power using effective capacitance, frequency, and corner (PVT)
        """
        proc,vdd,temp = corner
        net_vswing = vdd*swing
        power_dyn = c*vdd*net_vswing*freq
        
        #Apply process and temperature factors. Roughly, process and Vdd affect the delay which affects the power.
        #No other estimations are currently used. Increased delay->slower freq.->less power
        proc_div = max(self.get_process_delay_factor(proc)) 
        temp_div = self.get_temp_delay_factor(temp)
        power_dyn = power_dyn/(proc_div*temp_div)
        
        return power_dyn  
        
    def return_power(self, dynamic=0.0, leakage=0.0):
        return power_data(dynamic, leakage)

class delay_data:
    """
    This is the delay class to represent the delay information
    Time is 50% of the signal to 50% of reference signal delay.
    Slew is the 10% of the signal to 90% of signal
    """
    def __init__(self, delay=0.0, slew=0.0):
        """ init function support two init method"""
        # will take single input as a coordinate
        self.delay = delay
        self.slew = slew

    def __str__(self):
        """ override print function output """
        return "Delay Data: Delay "+str(self.delay)+", Slew "+str(self.slew)+""

    def __add__(self, other):
        """
        Override - function (left), for delay_data: a+b != b+a
        """
        assert isinstance(other,delay_data)
        return delay_data(other.delay + self.delay,
                          other.slew)

    def __radd__(self, other):
        """
        Override - function (right), for delay_data: a+b != b+a
        """
        assert isinstance(other,delay_data)
        return delay_data(other.delay + self.delay,
                          self.slew)
                          
class power_data:
    """
    This is the power class to represent the power information
    Dynamic and leakage power are stored as a single object with this class.
    """
    def __init__(self, dynamic=0.0, leakage=0.0):
        """ init function support two init method"""
        # will take single input as a coordinate
        self.dynamic = dynamic
        self.leakage = leakage

    def __str__(self):
        """ override print function output """
        return "Power Data: Dynamic "+str(self.dynamic)+", Leakage "+str(self.leakage)+" in nW"

    def __add__(self, other):
        """
        Override - function (left), for power_data: a+b != b+a
        """
        assert isinstance(other,power_data)
        return power_data(other.dynamic + self.dynamic,
                          other.leakage + self.leakage)

    def __radd__(self, other):
        """
        Override - function (left), for power_data: a+b != b+a
        """
        assert isinstance(other,power_data)
        return power_data(other.dynamic + self.dynamic,
                          other.leakage + self.leakage)


class wire_spice_model:
    """
    This is the spice class to represent a wire
    """
    def __init__(self, lump_num, wire_length, wire_width):
        self.lump_num = lump_num # the number of segment the wire delay has
        self.wire_c = self.cal_wire_c(wire_length, wire_width) # c in each segment  
        self.wire_r = self.cal_wire_r(wire_length, wire_width) # r in each segment

    def cal_wire_c(self, wire_length, wire_width):
        from tech import spice
        total_c = spice["wire_unit_c"] * wire_length * wire_width
        wire_c = total_c / self.lump_num
        return wire_c

    def cal_wire_r(self, wire_length, wire_width):
        from tech import spice
        total_r = spice["wire_unit_r"] * wire_length / wire_width
        wire_r = total_r / self.lump_num
        return wire_r

    def return_input_cap(self):
        return 0.5 * self.wire_c * self.lump_num

    def return_delay_over_wire(self, slew, swing = 0.5):
        # delay will be sum of arithmetic sequence start from
        # rc to self.lump_num*rc with step of rc

        swing_factor = abs(math.log(1-swing)) # time constant based on swing
        sum_factor = (1+self.lump_num) * self.lump_num * 0.5 # sum of the arithmetic sequence
        delay = sum_factor * swing_factor * self.wire_r * self.wire_c 
        slew = delay * 2 + slew
        result= delay_data(delay, slew)
        return result

