# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os
import re
import math
import textwrap as tr
from pprint import pformat
from openram import debug
from openram import tech
from openram import OPTS
from .delay_data import delay_data
from .wire_spice_model import wire_spice_model
from .power_data import power_data
from .logical_effort import convert_relative_c_to_farad, convert_farad_to_relative_c


class spice():
    """
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    Class consisting of a set of modules and instances of these modules
    """

    def __init__(self, name, cell_name):
        # This gets set in both spice and layout so either can be called first.
        self.name = name
        self.cell_name = cell_name
        self.sp_file = OPTS.openram_tech + "sp_lib/" + cell_name + ".sp"

        # If we have a separate lvs directory, then all the lvs files
        # should be in there (all or nothing!)
        try:
            from openram.tech import lvs_name
            lvs_dir = OPTS.openram_tech + lvs_name + "_lvs_lib/"
        except ImportError:
            lvs_dir = OPTS.openram_tech + "lvs_lib/"
        if not os.path.exists(lvs_dir):
            lvs_dir = OPTS.openram_tech + "lvs_lib/"

        self.lvs_file = lvs_dir + cell_name + ".sp"
        if not os.path.exists(self.lvs_file):
            self.lvs_file = self.sp_file

        self.valid_signal_types = ["INOUT", "INPUT", "OUTPUT", "BIAS", "POWER", "GROUND"]
        # Holds subckts/mods for this module
        self.mods = set()
        # Holds the pins for this module (in order)
        self.pins = []
        # The type map of each pin: INPUT, OUTPUT, INOUT, POWER, GROUND
        # for each instance, this is the set of nets/nodes that map to the pins for this instance
        self.pin_type = {}
        # An (optional) list of indices to reorder the pins to match the spice.
        self.pin_indices = []
        # THE CONNECTIONS MUST MATCH THE ORDER OF THE PINS (restriction imposed by the
        # Spice format)
        self.conns = []
        # If this is set, it will out output subckt or isntances of this (for row/col caps etc.)
        self.no_instances = False
        # If we are doing a trimmed netlist, these are the instance that will be filtered
        self.trim_insts = set()
        # Keep track of any comments to add the the spice
        try:
            self.commments
        except AttributeError:
            self.comments = []

        self.sp_read()

############################################################
# Spice circuit
############################################################

    def add_comment(self, comment):
        """ Add a comment to the spice file """

        try:
            self.commments
        except AttributeError:
            self.comments = []

        self.comments.append(comment)

    def add_pin(self, name, pin_type="INOUT"):
        """ Adds a pin to the pins list. Default type is INOUT signal. """
        self.pins.append(name)
        self.pin_type[name]=pin_type
        debug.check(pin_type in self.valid_signal_types,
                    "Invalid signaltype for {0}: {1}".format(name,
                                                             pin_type))

    def add_pin_list(self, pin_list, pin_type="INOUT"):
        """ Adds a pin_list to the pins list """
        # The type list can be a single type for all pins
        # or a list that is the same length as the pin list.
        if type(pin_type)==str:
            for pin in pin_list:
                debug.check(pin_type in self.valid_signal_types,
                            "Invalid signaltype for {0}: {1}".format(pin,
                                                                     pin_type))
                self.add_pin(pin, pin_type)

        elif len(pin_type)==len(pin_list):
            for (pin, ptype) in zip(pin_list, pin_type):
                debug.check(ptype in self.valid_signal_types,
                            "Invalid signaltype for {0}: {1}".format(pin,
                                                                     ptype))
                self.add_pin(pin, ptype)
        else:
            debug.error("Mismatch in type and pin list lengths.", -1)

    def add_pin_indices(self, index_list):
        """
        Add pin indices for all the cell's pins.
        """
        self.pin_indices = index_list

    def get_ordered_inputs(self, input_list):
        """
        Return the inputs reordered to match the pins.
        """
        if not self.pin_indices:
            return input_list

        new_list = [input_list[x] for x in self.pin_indices]
        return new_list

    def add_pin_types(self, type_list):
        """
        Add pin types for all the cell's pins.
        """
        # This only works if self.pins == bitcell.pin_names
        if len(type_list) != len(self.pins):
            debug.error("{} spice subcircuit number of port types does not match number of pins\
                      \n SPICE names={}\
                      \n Module names={}\
                      ".format(self.name, self.pins, type_list), 1)
        self.pin_type = {pin: type for pin, type in zip(self.pins, type_list)}

    def get_pin_type(self, name):
        """ Returns the type of the signal pin. """
        pin_type = self.pin_type[name]
        debug.check(pin_type in self.valid_signal_types,
                    "Invalid signaltype for {0}: {1}".format(name, pin_type))
        return pin_type

    def get_pin_dir(self, name):
        """ Returns the direction of the pin. (Supply/ground are INOUT). """
        if self.pin_type[name] in ["POWER", "GROUND"]:
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

    def copy_pins(self, other_module, suffix=""):
        """ This will copy all of the pins from the other module and add an optional suffix."""
        for pin in other_module.pins:
            self.add_pin(pin + suffix, other_module.get_pin_type(pin))

    def get_inouts(self):
        """ These use pin types to determine pin lists. These
        may be over-ridden by submodules that didn't use pin directions yet."""
        inout_list = []
        for pin in self.pins:
            if self.pin_type[pin]=="INOUT":
                inout_list.append(pin)
        return inout_list

    def connect_inst(self, args, check=True):
        """
        Connects the pins of the last instance added
        It is preferred to use the function with the check to find if
        there is a problem. The check option can be set to false
        where we dynamically generate groups of connections after a
        group of modules are generated.
        """

        num_pins = len(self.insts[-1].mod.pins)
        num_args = len(args)

        # Order the arguments if the hard cell has a custom port order
        ordered_args = self.get_ordered_inputs(args)

        if (check and num_pins != num_args):
            if num_pins < num_args:
                mod_pins = self.insts[-1].mod.pins + [""] * (num_args - num_pins)
                arg_pins = ordered_args
            else:
                arg_pins = ordered_args + [""] * (num_pins - num_args)
                mod_pins = self.insts[-1].mod.pins

            modpins_string = "\n".join(["{0} -> {1}".format(arg, mod) for (arg, mod) in zip(arg_pins, mod_pins)])
            debug.error("Connection mismatch:\nInst ({0}) -> Mod ({1})\n{2}".format(num_args,
                                                                                    num_pins,
                                                                                    modpins_string),
                        1)

        self.conns.append(ordered_args)

        # This checks if we don't have enough instance port connections for the number of insts
        if check and (len(self.insts)!=len(self.conns)):
            insts_string=pformat(self.insts)
            conns_string=pformat(self.conns)

            debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.name,
                                                                                        len(self.insts),
                                                                                        len(self.conns)))
            debug.error("Instances: \n" + str(insts_string))
            debug.error("-----")
            debug.error("Connections: \n" + str(conns_string), 1)

    def get_conns(self, inst):
        """Returns the connections of a given instance."""
        for i in range(len(self.insts)):
            if inst is self.insts[i]:
                return self.conns[i]
        # If not found, returns None
        return None

    def sp_read(self):
        """
        Reads the sp file (and parse the pins) from the library
        Otherwise, initialize it to null for dynamic generation
        """
        if self.sp_file and os.path.isfile(self.sp_file):
            debug.info(3, "opening {0}".format(self.sp_file))
            f = open(self.sp_file)
            self.spice = f.readlines()
            for i in range(len(self.spice)):
                self.spice[i] = self.spice[i].rstrip(" \n")
            f.close()

            # find the correct subckt line in the file
            subckt = re.compile("^.subckt {}".format(self.cell_name), re.IGNORECASE)
            subckt_line = list(filter(subckt.search, self.spice))[0]
            # parses line into ports and remove subckt
            self.pins = subckt_line.split(" ")[2:]
        else:
            debug.info(4, "no spfile {0}".format(self.sp_file))
            self.spice = []

        # We don't define self.lvs and will use self.spice if dynamically created
        # or they are the same file
        if self.lvs_file != self.sp_file and os.path.isfile(self.lvs_file):
            debug.info(3, "opening {0}".format(self.lvs_file))
            f = open(self.lvs_file)
            self.lvs = f.readlines()
            for i in range(len(self.lvs)):
                self.lvs[i] = self.lvs[i].rstrip(" \n")
            f.close()

            # pins and subckt should be the same
            # find the correct subckt line in the file
            subckt = re.compile("^.subckt {}".format(self.cell_name), re.IGNORECASE)
            subckt_line = list(filter(subckt.search, self.lvs))[0]
            # parses line into ports and remove subckt
            lvs_pins = subckt_line.split(" ")[2:]
            debug.check(lvs_pins == self.pins,
                        "Spice netlists for LVS and simulation have port mismatches:\n{0} (LVS {1})\nvs\n{2} (sim {3})".format(lvs_pins,
                                                                                                                               self.lvs_file,
                                                                                                                               self.pins,
                                                                                                                               self.sp_file))

    def check_net_in_spice(self, net_name):
        """Checks if a net name exists in the current. Intended to be check nets in hand-made cells."""
        # Remove spaces and lower case then add spaces.
        # Nets are separated by spaces.
        net_formatted = ' ' + net_name.lstrip().rstrip().lower() + ' '
        for line in self.spice:
            # Lowercase the line and remove any part of the line that is a comment.
            line = line.lower().split('*')[0]

            # Skip .subckt or .ENDS lines
            if line.find('.') == 0:
                continue
            if net_formatted in line:
                return True
        return False

    def do_nets_exist(self, nets):
        """For handmade cell, checks sp file contains the storage nodes."""
        nets_match = True
        for net in nets:
            nets_match = nets_match and self.check_net_in_spice(net)
        return nets_match

    def contains(self, mod, modlist):
        for x in modlist:
            if x.name == mod.name:
                return True
        return False

    def sp_write_file(self, sp, usedMODS, lvs=False, trim=False):
        """
        Recursive spice subcircuit write;
        Writes the spice subcircuit from the library or the dynamically generated one.
        Trim netlist is intended ONLY for bitcell arrays.
        """

        if self.no_instances:
            return
        elif not self.spice:
            # If spice isn't defined, we dynamically generate one.

            # recursively write the modules
            for i in self.mods:
                if self.contains(i, usedMODS):
                    continue
                usedMODS.append(i)
                i.sp_write_file(sp, usedMODS, lvs, trim)

            if len(self.insts) == 0:
                return
            if self.pins == []:
                return

            # write out the first spice line (the subcircuit)
            wrapped_pins = "\n+ ".join(tr.wrap(" ".join(self.pins)))
            sp.write("\n.SUBCKT {0}\n+ {1}\n".format(self.cell_name,
                                                     wrapped_pins))

            # write a PININFO line
            if False:
                pin_info = "*.PININFO"
                for pin in self.pins:
                    if self.pin_type[pin] == "INPUT":
                        pin_info += " {0}:I".format(pin)
                    elif self.pin_type[pin] == "OUTPUT":
                        pin_info += " {0}:O".format(pin)
                    else:
                        pin_info += " {0}:B".format(pin)
                sp.write(pin_info + "\n")

            # Also write pins as comments
            for pin in self.pins:
                sp.write("* {1:6}: {0} \n".format(pin, self.pin_type[pin]))

            for line in self.comments:
                sp.write("* {}\n".format(line))

            # every instance must have a set of connections, even if it is empty.
            if len(self.insts) != len(self.conns):
                debug.error("{0} : Not all instance pins ({1}) are connected ({2}).".format(self.cell_name,
                                                                                            len(self.insts),
                                                                                            len(self.conns)))
                debug.error("Instances: \n" + str(self.insts))
                debug.error("-----")
                debug.error("Connections: \n" + str(self.conns), 1)

            for i in range(len(self.insts)):
                # we don't need to output connections of empty instances.
                # these are wires and paths
                if self.conns[i] == []:
                    continue

                # Instance with no devices in it needs no subckt/instance
                if self.insts[i].mod.no_instances:
                    continue

                # If this is a trimmed netlist, skip it by adding comment char
                if trim and self.insts[i].name in self.trim_insts:
                    sp.write("* ")

                if lvs and hasattr(self.insts[i].mod, "lvs_device"):
                    sp.write(self.insts[i].mod.lvs_device.format(self.insts[i].name,
                                                                   " ".join(self.conns[i])))
                    sp.write("\n")
                elif hasattr(self.insts[i].mod, "spice_device"):
                    sp.write(self.insts[i].mod.spice_device.format(self.insts[i].name,
                                                                   " ".join(self.conns[i])))
                    sp.write("\n")
                else:
                    wrapped_connections = "\n+ ".join(tr.wrap(" ".join(self.conns[i])))

                    sp.write("X{0}\n+ {1}\n+ {2}\n".format(self.insts[i].name,
                                                           wrapped_connections,
                                                           self.insts[i].mod.cell_name))

            sp.write(".ENDS {0}\n".format(self.cell_name))

        else:
            # If spice is a hard module, output the spice file contents.
            # Including the file path makes the unit test fail for other users.
            # if os.path.isfile(self.sp_file):
            #    sp.write("\n* {0}\n".format(self.sp_file))
            if lvs and hasattr(self, "lvs"):
                sp.write("\n".join(self.lvs))
            else:
                sp.write("\n".join(self.spice))

            sp.write("\n")


    def sp_write(self, spname, lvs=False, trim=False):
        """Writes the spice to files"""
        debug.info(3, "Writing to {0}".format(spname))
        spfile = open(spname, 'w')
        spfile.write("*FIRST LINE IS A COMMENT\n")
        usedMODS = list()
        self.sp_write_file(spfile, usedMODS, lvs=lvs, trim=trim)
        del usedMODS
        spfile.close()

    def cacti_delay(self, corner, inrisetime, c_load, cacti_params):
        """Generalization of how Cacti determines the delay of a gate"""
        self.cacti_params = cacti_params
        # Get the r_on the the tx
        rd = self.get_on_resistance()
        # Calculate the intrinsic capacitance
        c_intrinsic = self.get_intrinsic_capacitance()
        # Get wire values
        c_wire = self.module_wire_c()
        r_wire = self.module_wire_r()

        tf = rd*(c_intrinsic+c_load+c_wire)+r_wire*(c_load+c_wire/2)
        extra_param_dict = {}
        extra_param_dict['vdd'] = corner[1] #voltage is second in PVT corner
        extra_param_dict['load'] = c_wire+c_intrinsic+c_load #voltage is second in PVT corner
        this_delay = self.cacti_rc_delay(inrisetime, tf, 0.5, 0.5, True, extra_param_dict)
        inrisetime = this_delay / (1.0 - 0.5)
        return delay_data(this_delay, inrisetime)

    def analytical_delay(self, corner, slew, load=0.0):
        """Inform users undefined delay module while building new modules"""

        # FIXME: Slew is not used in the model right now.
        # Can be added heuristically as linear factor
        relative_cap = convert_farad_to_relative_c(load)
        stage_effort = self.get_stage_effort(relative_cap)

        # If it fails, then keep running with a valid object.
        if not stage_effort:
            return delay_data(0.0, 0.0)

        abs_delay = stage_effort.get_absolute_delay()
        corner_delay = self.apply_corners_analytically(abs_delay, corner)
        SLEW_APPROXIMATION = 0.1
        corner_slew = SLEW_APPROXIMATION * corner_delay
        return delay_data(corner_delay, corner_slew)

    def module_wire_c(self):
        """All devices assumed to have ideal capacitance (0).
           Non-ideal cases should have this function re-defined.
        """
        return 0

    def module_wire_r(self):
        """All devices assumed to have ideal resistance (0).
           Non-ideal cases should have this function re-defined.
        """
        return 0

    def get_stage_effort(self, cout, inp_is_rise=True):
        """Inform users undefined delay module while building new modules"""
        debug.warning("Design Class {0} logical effort function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__,
                              self.cell_name))
        return None

    def get_on_resistance(self):
        """Inform users undefined delay module while building new modules"""
        debug.warning("Design Class {0} on resistance function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__,
                              self.cell_name))
        return 0

    def get_input_capacitance(self):
        """Inform users undefined delay module while building new modules"""
        debug.warning("Design Class {0} input capacitance function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__,
                              self.cell_name))
        return 0

    def get_intrinsic_capacitance(self):
        """Inform users undefined delay module while building new modules"""
        debug.warning("Design Class {0} intrinsic capacitance function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__,
                              self.cell_name))
        return 0

    def get_cin(self):
        """Returns input load in Femto-Farads. All values generated using
           relative capacitance function then converted based on tech file parameter."""

        # Override this function within a module if a more accurate input capacitance is needed.
        # Input/outputs with differing capacitances is not implemented.
        relative_cap = self.input_load()
        return convert_relative_c_to_farad(relative_cap)

    def input_load(self):
        """Inform users undefined relative capacitance functions used for analytical delays."""
        debug.warning("Design Class {0} input load function needs to be defined"
                      .format(self.__class__.__name__))
        debug.warning("Class {0} name {1}"
                      .format(self.__class__.__name__,
                              self.cell_name))
        return 0

    def cacti_rc_delay(self,
                 inputramptime, # input rise time
                 tf,            # time constant of gate
                 vs1,           # threshold voltage
                 vs2,           # threshold voltage
                 rise,          # whether input rises or fall
                 extra_param_dict=None):
        """By default, CACTI delay uses horowitz for gate delay.
           Can be overriden in cases like bitline if equation is different.
        """
        return self.horowitz(inputramptime, tf, vs1, vs2, rise)

    def horowitz(self,
                 inputramptime, # input rise time
                 tf,            # time constant of gate
                 vs1,           # threshold voltage
                 vs2,           # threshold voltage
                 rise):         # whether input rises or fall

        if inputramptime == 0 and vs1 == vs2:
            return tf * (-math.log(vs1) if vs1 < 1 else math.log(vs1))

        a = inputramptime / tf
        if rise == True:
            b = 0.5
            td = tf * math.sqrt(math.log(vs1)*math.log(vs1) + 2*a*b*(1.0 - vs1)) + tf*(math.log(vs1) - math.log(vs2))

        else:
            b = 0.4
            td = tf * math.sqrt(math.log(1.0 - vs1)*math.log(1.0 - vs1) + 2*a*b*(vs1)) + tf*(math.log(1.0 - vs1) - math.log(1.0 - vs2))

        return td

    def tr_r_on(self, width, is_nchannel, stack, _is_cell):

        restrans = self.cacti_params["r_nch_on"] if is_nchannel else self.cacti_params["r_pch_on"]
        return stack * restrans / width

    def gate_c(self, width):

        return (tech.spice["c_g_ideal"] + tech.spice["c_overlap"] + 3*tech.spice["c_fringe"])*width +\
               tech.drc["minlength_channel"]*tech.spice["cpolywire"]

    def drain_c_(self,
                 width,
                 stack,
                 folds):

        c_junc_area = tech.spice["c_junc"]
        c_junc_sidewall = tech.spice["c_junc_sw"]
        c_fringe = 2*tech.spice["c_overlap"]
        c_overlap = 2*tech.spice["c_fringe"]
        drain_C_metal_connecting_folded_tr = 0

        w_folded_tr = width/folds
        num_folded_tr = folds

        # Re-created some logic contact to get minwidth as importing the contact
        # module causes a failure
        if "minwidth_contact" in tech.drc:
            contact_width = tech.drc["minwidth_contact"]
        elif "minwidth_active_contact" in tech.drc:
            contact_width = tech.drc["minwidth_active_contact"]
        else:
            debug.warning("Undefined minwidth_contact in tech.")
            contact_width = 0

        # only for drain
        total_drain_w = (contact_width + 2 * tech.drc["active_contact_to_gate"]) +\
                        (stack - 1) * tech.drc["poly_to_poly"]
        drain_h_for_sidewall = w_folded_tr
        total_drain_height_for_cap_wrt_gate = w_folded_tr + 2 * w_folded_tr * (stack - 1)
        if num_folded_tr > 1:
            total_drain_w += (num_folded_tr - 2) * (contact_width + 2 * tech.drc["active_contact_to_gate"]) +\
                             (num_folded_tr - 1) * ((stack - 1) * tech.drc["poly_to_poly"])

            if num_folded_tr%2 == 0:
                drain_h_for_sidewall = 0

            total_drain_height_for_cap_wrt_gate *= num_folded_tr
            drain_C_metal_connecting_folded_tr   = tech.spice["wire_c_per_um"] * total_drain_w


        drain_C_area     = c_junc_area * total_drain_w * w_folded_tr
        drain_C_sidewall = c_junc_sidewall * (drain_h_for_sidewall + 2 * total_drain_w)
        drain_C_wrt_gate = (c_fringe + c_overlap) * total_drain_height_for_cap_wrt_gate

        return drain_C_area + drain_C_sidewall + drain_C_wrt_gate + drain_C_metal_connecting_folded_tr

    def cal_delay_with_rc(self, corner, r, c, slew, swing=0.5):
        """
        Calculate the delay of a mosfet by
        modeling it as a resistance driving a capacitance
        """
        swing_factor = abs(math.log(1 - swing)) # time constant based on swing
        delay = swing_factor * r * c # c is in ff and delay is in fs
        delay = self.apply_corners_analytically(delay, corner)
        delay = delay * 0.001 # make the unit to ps

        # Output slew should be linear to input slew which is described
        # as 0.005* slew.

        # The slew will be also influenced by the delay.
        # If no input slew(or too small to make impact)
        # The mimum slew should be the time to charge RC.
        # Delay * 2 is from 0 to 100%  swing. 0.6*2*delay is from 20%-80%.
        slew = delay * 0.6 * 2 + 0.005 * slew
        return delay_data(delay=delay, slew=slew)

    def apply_corners_analytically(self, delay, corner):
        """Multiply delay by corner factors"""
        proc, vdd, temp = corner
        # FIXME: type of delay is needed to know which process to use.
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
        return tech.spice["nom_supply_voltage"] / voltage

    def get_temp_delay_factor(self, temp):
        """Returns delay increase due to temperature (in C).
           Determines effect on threshold voltage and then linear factor is estimated.
        """
        # Some portions of equation condensed (phi_t = k*T/q for T in Kelvin) in mV
        # (k/q)/100 = .008625, The division 100 simplifies the conversion from C to K and mV to V
        thermal_voltage_nom = 0.008625 * tech.spice["nom_temperature"]
        thermal_voltage = 0.008625 * temp
        vthresh = (tech.spice["nom_threshold"] + 2 * (thermal_voltage - thermal_voltage_nom))
        # Calculate effect on Vdd-Vth.
        # The current vdd is not used here.
        # A separate vdd factor is calculated.
        return (tech.spice["nom_supply_voltage"] - tech.spice["nom_threshold"]) / (tech.spice["nom_supply_voltage"] - vthresh)

    def return_delay(self, delay, slew):
        return delay_data(delay, slew)

    def generate_rc_net(self, lump_num, wire_length, wire_width):
        return wire_spice_model(lump_num, wire_length, wire_width)

    def calc_dynamic_power(self, corner, c, freq, swing=1.0):
        """
        Calculate dynamic power using effective capacitance, frequency, and corner (PVT)
        """
        proc, vdd, temp = corner
        net_vswing = vdd * swing
        power_dyn = c * vdd * net_vswing * freq

        # A pply process and temperature factors.
        # Roughly, process and Vdd affect the delay which affects the power.
        # No other estimations are currently used. Increased delay->slower freq.->less power
        proc_div = max(self.get_process_delay_factor(proc))
        temp_div = self.get_temp_delay_factor(temp)
        power_dyn = power_dyn / (proc_div * temp_div)

        return power_dyn

    def return_power(self, dynamic=0.0, leakage=0.0):
        return power_data(dynamic, leakage)

    def find_aliases(self, inst_name, port_nets, path_nets, alias, alias_mod, exclusion_set=None):
        """
        Given a list of nets, will compare the internal alias of a mod to determine
        if the nets have a connection to this mod's net (but not inst).
        """
        if not exclusion_set:
            exclusion_set = set()
        try:
            self.name_dict
        except AttributeError:
            self.name_dict = {}
            self.build_names(self.name_dict, inst_name, port_nets)
        aliases = []
        for net in path_nets:
            net = net.lower()
            int_net = self.name_dict[net]['int_net']
            int_mod = self.name_dict[net]['mod']

            if int_mod.is_net_alias(int_net, alias, alias_mod, exclusion_set):
                aliases.append(net)
        return aliases

    def is_net_alias(self, known_net, net_alias, mod, exclusion_set):
        """
        Checks if the alias_net in input mod is the same as the input net for this mod (self).
        """
        if self in exclusion_set:
            return False
        # Check ports of this mod
        for pin in self.pins:
            if self.is_net_alias_name_check(known_net, pin, net_alias, mod):
                return True
        # Check connections of all other subinsts
        mod_set = set()
        for subinst, inst_conns in zip(self.insts, self.conns):
            for inst_conn, mod_pin in zip(inst_conns, subinst.mod.pins):
                if self.is_net_alias_name_check(known_net, inst_conn, net_alias, mod):
                    return True
                elif inst_conn.lower() == known_net.lower() and subinst.mod not in mod_set:
                    if subinst.mod.is_net_alias(mod_pin, net_alias, mod, exclusion_set):
                        return True
                    mod_set.add(subinst.mod)
        return False

    def is_net_alias_name_check(self, parent_net, child_net, alias_net, mod):
        """
        Utility function for checking single net alias.
        """
        return self == mod and \
               child_net.lower() == alias_net.lower() and \
               parent_net.lower() == alias_net.lower()
