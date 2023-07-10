# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import os, sys, re
import time
import datetime
import numpy as np
from openram import debug
from openram import tech
from openram.tech import spice
from openram import OPTS
from .setup_hold import *
from .delay import *
from .charutils import *


class lib:
    """ lib file generation."""

    def __init__(self, out_dir, sram, sp_file, use_model=OPTS.analytical_delay):

        try:
            self.vdd_name = spice["power"]
        except KeyError:
            self.vdd_name = "vdd"
        try:
            self.gnd_name = spice["ground"]
        except KeyError:
            self.gnd_name = "gnd"

        self.out_dir = out_dir
        self.sram = sram
        self.sp_file = sp_file
        self.use_model = use_model
        self.pred_time = None
        self.set_port_indices()

        self.prepare_tables()

        self.create_corners()

        self.characterize_corners()

    def set_port_indices(self):
        """Copies port information set in the SRAM instance"""
        self.total_port_num = len(self.sram.all_ports)
        self.all_ports = self.sram.all_ports
        self.readwrite_ports = self.sram.readwrite_ports
        self.read_ports = self.sram.read_ports
        self.write_ports = self.sram.write_ports

    def prepare_tables(self):
        """ Determine the load/slews if they aren't specified in the config file. """
        # These are the parameters to determine the table sizes
        if OPTS.use_specified_load_slew == None:
            self.load_scales = np.array(OPTS.load_scales)
            self.load = tech.spice["dff_in_cap"]
            self.loads = self.load_scales * self.load


            self.slew_scales = np.array(OPTS.slew_scales)
            self.slew = tech.spice["rise_time"]
            self.slews = self.slew_scales * self.slew
            self.load_slews = []
            for slew in self.slews:
                for load in self.loads:
                    self.load_slews.append((load, slew))
        else:
            debug.warning("Using the option \"use_specified_load_slew\" will make load slew,data in lib file inaccurate.")
            self.load_slews = OPTS.use_specified_load_slew
            self.loads = []
            self.slews = []
            for load,slew in self.load_slews:
                self.loads.append(load)
                self.slews.append(slew)
        self.loads = np.array(self.loads)
        self.slews = np.array(self.slews)
        debug.info(1, "Slews: {0}".format(self.slews))
        debug.info(1, "Loads: {0}".format(self.loads))
        debug.info(1, "self.load_slews : {0}".format(self.load_slews))

    def create_corners(self):
        """ Create corners for characterization. """
        # Get the corners from the options file
        self.temperatures = OPTS.temperatures
        self.supply_voltages = OPTS.supply_voltages
        self.process_corners = OPTS.process_corners

        # Corner values
        min_temperature = min(self.temperatures)
        nom_temperature = tech.spice["nom_temperature"]
        max_temperature = max(self.temperatures)
        min_supply = min(self.supply_voltages)
        nom_supply = tech.spice["nom_supply_voltage"]
        max_supply = max(self.supply_voltages)
        min_process = "FF"
        nom_process = "TT"
        max_process = "SS"

        self.corners = []
        self.lib_files = []

        if OPTS.use_specified_corners == None:
            # Nominal corner
            corner_tuples = set()
            if OPTS.only_use_config_corners:
                if OPTS.nominal_corner_only:
                    debug.warning("Nominal corner only option ignored if use only config corners is set.")
                # Generate a powerset of input PVT lists
                for p in self.process_corners:
                    for v in self.supply_voltages:
                        for t in self.temperatures:
                            corner_tuples.add((p, v, t))
            else:
                nom_corner = (nom_process, nom_supply, nom_temperature)
                corner_tuples.add(nom_corner)
                if not OPTS.nominal_corner_only:
                    # Temperature corners
                    corner_tuples.add((nom_process, nom_supply, min_temperature))
                    corner_tuples.add((nom_process, nom_supply, max_temperature))
                    # Supply corners
                    corner_tuples.add((nom_process, min_supply, nom_temperature))
                    corner_tuples.add((nom_process, max_supply, nom_temperature))
                    # Process corners
                    corner_tuples.add((min_process, nom_supply, nom_temperature))
                    corner_tuples.add((max_process, nom_supply, nom_temperature))
            # Enforce that nominal corner is the first to be characterized
            self.add_corner(*nom_corner)
            corner_tuples.remove(nom_corner)
        else:
            corner_tuples = OPTS.use_specified_corners

        for corner_tuple in corner_tuples:
            self.add_corner(*corner_tuple)

    def add_corner(self, proc, volt, temp):
        self.corner_name = "{0}_{1}_{2}V_{3}C".format(self.sram.name,
                                                      proc,
                                                      volt,
                                                      temp)
        self.corner_name = self.corner_name.replace(".","p") # Remove decimals
        lib_name = self.out_dir+"{}.lib".format(self.corner_name)

        # A corner is a tuple of PVT
        self.corners.append((proc, volt, temp))
        self.lib_files.append(lib_name)


    def characterize_corners(self):
        """ Characterize the list of corners. """
        debug.info(1,"Characterizing corners: " + str(self.corners))
        is_first_corner = True
        for (self.corner,lib_name) in zip(self.corners,self.lib_files):
            run_start = time.time()
            debug.info(1,"Corner: " + str(self.corner))
            (self.process, self.voltage, self.temperature) = self.corner
            self.lib = open(lib_name, "w")
            debug.info(1,"Writing to {0}".format(lib_name))
            self.corner_name = lib_name.replace(self.out_dir,"").replace(".lib","")
            self.characterize()
            self.lib.close()
            if self.pred_time == None:
                total_time = time.time()-run_start
            else:
                total_time = self.pred_time
            self.parse_info(self.corner,lib_name, is_first_corner, total_time)
            is_first_corner = False

    def characterize(self):
        """ Characterize the current corner. """

        self.compute_delay()

        self.compute_setup_hold()

        self.write_header()

        # Loop over all ports.
        for port in self.all_ports:
            # set the read and write port as inputs.
            self.write_data_bus(port)
            self.write_addr_bus(port)
            if self.sram.write_size != self.sram.word_size and \
                    port in self.write_ports:
                self.write_wmask_bus(port)
            # need to split this into sram and port control signals
            self.write_control_pins(port)
            self.write_clk_timing_power(port)

        self.write_footer()

    def write_footer(self):
        """ Write the footer """
        self.lib.write("    }\n") # Closing brace for the cell
        self.lib.write("}\n") # Closing brace for the library

    def write_header(self):
        """ Write the header information """
        self.lib.write("library ({0}_lib)".format(self.corner_name))
        self.lib.write("{\n")
        self.lib.write("    delay_model : \"table_lookup\";\n")

        self.write_units()
        self.write_defaults()
        self.write_LUT_templates()

        self.lib.write("    default_operating_conditions : OC; \n")

        self.write_bus()

        self.lib.write("cell ({0})".format(self.sram.name))
        self.lib.write("{\n")
        self.lib.write("    memory(){ \n")
        self.lib.write("    type : ram;\n")
        self.lib.write("    address_width : {};\n".format(self.sram.addr_size))
        self.lib.write("    word_width : {};\n".format(self.sram.word_size))
        self.lib.write("    }\n")
        self.lib.write("    interface_timing : true;\n")
        self.lib.write("    dont_use  : true;\n")
        self.lib.write("    map_only   : true;\n")
        self.lib.write("    dont_touch : true;\n")
        self.lib.write("    area : {};\n\n".format(self.sram.width * self.sram.height))

        self.write_pg_pin()

        #Build string of all control signals.
        control_str = 'csb0' #assume at least 1 port
        for i in range(1, self.total_port_num):
            control_str += ' & csb{0}'.format(i)

        # Leakage is included in dynamic when macro is enabled
        self.lib.write("    leakage_power () {\n")
        # 'when' condition unnecessary when cs pin does not turn power to devices
        # self.lib.write("      when : \"{0}\";\n".format(control_str))
        self.lib.write("      value : {};\n".format(self.char_sram_results["leakage_power"]))
        self.lib.write("    }\n")
        self.lib.write("    cell_leakage_power : {};\n".format(self.char_sram_results["leakage_power"]))


    def write_units(self):
        """ Adds default units for time, voltage, current,...
            Valid values are 1mV, 10mV, 100mV, and 1V.
            For time: Valid values are 1ps, 10ps, 100ps, and 1ns.
            For power: Valid values are 1mW, 100uW (for 100mW), 10uW (for 10mW),
                       1uW (for 1mW), 100nW, 10nW, 1nW, 100pW, 10pW, and 1pW.
        """
        self.lib.write("    time_unit : \"1ns\" ;\n")
        self.lib.write("    voltage_unit : \"1V\" ;\n")
        self.lib.write("    current_unit : \"1mA\" ;\n")
        self.lib.write("    resistance_unit : \"1kohm\" ;\n")
        self.lib.write("    capacitive_load_unit(1, pF) ;\n")
        self.lib.write("    leakage_power_unit : \"1mW\" ;\n")
        self.lib.write("    pulling_resistance_unit :\"1kohm\" ;\n")
        self.lib.write("    operating_conditions(OC){\n")
        self.lib.write("    process : {} ;\n".format(1.0)) # How to use TT, FF, SS?
        self.lib.write("    voltage : {} ;\n".format(self.voltage))
        self.lib.write("    temperature : {};\n".format(self.temperature))
        self.lib.write("    }\n\n")

    def write_defaults(self):
        """ Adds default values for slew and capacitance."""

        self.lib.write("    input_threshold_pct_fall       :  50.0 ;\n")
        self.lib.write("    output_threshold_pct_fall      :  50.0 ;\n")
        self.lib.write("    input_threshold_pct_rise       :  50.0 ;\n")
        self.lib.write("    output_threshold_pct_rise      :  50.0 ;\n")
        self.lib.write("    slew_lower_threshold_pct_fall  :  10.0 ;\n")
        self.lib.write("    slew_upper_threshold_pct_fall  :  90.0 ;\n")
        self.lib.write("    slew_lower_threshold_pct_rise  :  10.0 ;\n")
        self.lib.write("    slew_upper_threshold_pct_rise  :  90.0 ;\n\n")

        self.lib.write("    nom_voltage : {};\n".format(self.voltage))
        self.lib.write("    nom_temperature : {};\n".format(self.temperature))
        self.lib.write("    nom_process : 1.0;\n")
        self.lib.write("    default_cell_leakage_power    : 0.0 ;\n")
        self.lib.write("    default_leakage_power_density : 0.0 ;\n")
        self.lib.write("    default_input_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_inout_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_output_pin_cap   : 0.0 ;\n")
        self.lib.write("    default_max_transition   : 0.5 ;\n")
        self.lib.write("    default_fanout_load      : 1.0 ;\n")
        self.lib.write("    default_max_fanout   : 4.0 ;\n")
        self.lib.write("    default_connection_class : universal ;\n\n")

        self.lib.write("    voltage_map ( {0}, {1} );\n".format(self.vdd_name.upper(), self.voltage))
        self.lib.write("    voltage_map ( {0}, 0 );\n\n".format(self.gnd_name.upper()))

    def create_list(self,values):
        """ Helper function to create quoted, line wrapped list """
        list_values = ", ".join(str(v) for v in values)
        return "\"{0}\"".format(list_values)

    def create_array(self,values, length):
        """ Helper function to create quoted, line wrapped array with each row of given length """
        # check that the length is a multiple or give an error!
        debug.check(len(values)%length == 0,"Values are not a multiple of the length. Cannot make a full array.")
        rounded_values = list(map(round_time,values))
        split_values = [rounded_values[i:i+length] for i in range(0, len(rounded_values), length)]
        formatted_rows = list(map(self.create_list,split_values))
        formatted_array = ",\\\n".join(formatted_rows)
        return formatted_array

    def write_index(self, number, values):
        """ Write the index """
        quoted_string = self.create_list(values)
        self.lib.write("        index_{0}({1});\n".format(number,quoted_string))

    def write_values(self, values, row_length, indent):
        """ Write the index """
        quoted_string = self.create_array(values, row_length)
        # indent each newline plus extra spaces for word values
        indented_string = quoted_string.replace('\n', '\n' + indent +"       ")
        self.lib.write("{0}values({1});\n".format(indent,indented_string))

    def write_LUT_templates(self):
        """ Adds lookup_table format (A 1x1 lookup_table)."""

        Tran = ["CELL_TABLE"]
        for i in Tran:
            self.lib.write("    lu_table_template({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        variable_1 : input_net_transition;\n")
            self.lib.write("        variable_2 : total_output_net_capacitance;\n")
            self.write_index(1,self.slews)
            # Dividing by 1000 to all cap values since output of .sp is in fF,
            # and it needs to be in pF for Innovus.
            self.write_index(2,self.loads/1000)
            self.lib.write("    }\n\n")

        CONS = ["CONSTRAINT_TABLE"]
        for i in CONS:
            self.lib.write("    lu_table_template({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        variable_1 : related_pin_transition;\n")
            self.lib.write("        variable_2 : constrained_pin_transition;\n")
            self.write_index(1,self.slews)
            self.write_index(2,self.slews)
            self.lib.write("    }\n\n")

        # self.lib.write("    lu_table_template(CLK_TRAN) {\n")
        # self.lib.write("        variable_1 : constrained_pin_transition;\n")
        # self.write_index(1,self.slews)
        # self.lib.write("    }\n\n")

        # self.lib.write("    lu_table_template(TRAN) {\n")
        # self.lib.write("        variable_1 : total_output_net_capacitance;\n")
        # self.write_index(1,self.slews)
        # self.lib.write("    }\n\n")

        # CONS2 = ["INPUT_BY_TRANS_FOR_CLOCK" , "INPUT_BY_TRANS_FOR_SIGNAL"]
        # for i in CONS2:
        #     self.lib.write("    power_lut_template({0})".format(i))
        #     self.lib.write("{\n")
        #     self.lib.write("        variable_1 : input_transition_time;\n")
        #     #self.write_index(1,self.slews)
        #     self.write_index(1,[self.slews[0]])
        #     self.lib.write("    }\n\n")

    def write_bus(self):
        """ Adds format of data and addr bus."""

        self.lib.write("\n\n")
        self.lib.write("    type (data){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.sram.word_size))
        self.lib.write("    bit_from : {0};\n".format(self.sram.word_size - 1))
        self.lib.write("    bit_to : 0;\n")
        self.lib.write("    }\n\n")

        self.lib.write("    type (addr){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.sram.addr_size))
        self.lib.write("    bit_from : {0};\n".format(self.sram.addr_size - 1))
        self.lib.write("    bit_to : 0;\n")
        self.lib.write("    }\n\n")

        if self.sram.write_size != self.sram.word_size:
            self.lib.write("    type (wmask){\n")
            self.lib.write("    base_type : array;\n")
            self.lib.write("    data_type : bit;\n")
            self.lib.write("    bit_width : {0};\n".format(self.sram.num_wmasks))
            self.lib.write("    bit_from : {0};\n".format(self.sram.num_wmasks - 1))
            self.lib.write("    bit_to : 0;\n")
            self.lib.write("    }\n\n")


    def write_FF_setuphold(self, port):
        """ Adds Setup and Hold timing results"""

        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : setup_rising; \n")
        self.lib.write("            related_pin  : \"clk{0}\"; \n".format(port))
        self.lib.write("            rise_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = list(map(round_time,self.times["setup_times_LH"]))
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = list(map(round_time,self.times["setup_times_HL"]))
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : hold_rising; \n")
        self.lib.write("            related_pin  : \"clk{0}\"; \n".format(port))
        self.lib.write("            rise_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = list(map(round_time,self.times["hold_times_LH"]))
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("              }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = list(map(round_time,self.times["hold_times_HL"]))
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("        }\n")

    def write_data_bus_output(self, read_port):
        """ Adds data bus timing results."""

        self.lib.write("    bus(dout{0}){{\n".format(read_port))
        self.lib.write("        bus_type  : data; \n")
        self.lib.write("        direction  : output; \n")
        # This is conservative, but limit to range that we characterized.
        self.lib.write("        max_capacitance : {0};  \n".format(max(self.loads)/1000))
        self.lib.write("        min_capacitance : {0};  \n".format(min(self.loads)/1000))
        self.lib.write("        memory_read(){ \n")
        self.lib.write("            address : addr{0}; \n".format(read_port))
        self.lib.write("        }\n")


        self.lib.write("        pin(dout{0}[{1}:0]){{\n".format(read_port,self.sram.word_size-1))
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_sense : non_unate; \n")
        self.lib.write("            related_pin : \"clk{0}\"; \n".format(read_port))
        self.lib.write("            timing_type : falling_edge; \n")
        self.lib.write("            cell_rise(CELL_TABLE) {\n")
        self.write_values(self.char_port_results[read_port]["delay_lh"],len(self.loads),"            ")
        self.lib.write("            }\n") # rise delay
        self.lib.write("            cell_fall(CELL_TABLE) {\n")
        self.write_values(self.char_port_results[read_port]["delay_hl"],len(self.loads),"            ")
        self.lib.write("            }\n") # fall delay
        self.lib.write("            rise_transition(CELL_TABLE) {\n")
        self.write_values(self.char_port_results[read_port]["slew_lh"],len(self.loads),"            ")
        self.lib.write("            }\n") # rise trans
        self.lib.write("            fall_transition(CELL_TABLE) {\n")
        self.write_values(self.char_port_results[read_port]["slew_hl"],len(self.loads),"            ")
        self.lib.write("            }\n") # fall trans
        self.lib.write("        }\n") # timing
        self.lib.write("        }\n") # pin
        self.lib.write("    }\n\n") # bus

    def write_data_bus_input(self, write_port):
        """ Adds din data bus timing results."""

        self.lib.write("    bus(din{0}){{\n".format(write_port))
        self.lib.write("        bus_type  : data; \n")
        self.lib.write("        direction  : input; \n")
        # This is conservative, but limit to range that we characterized.
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]/1000))
        self.lib.write("        memory_write(){ \n")
        self.lib.write("            address : addr{0}; \n".format(write_port))
        self.lib.write("            clocked_on  : clk{0}; \n".format(write_port))
        self.lib.write("        }\n")
        self.lib.write("        pin(din{0}[{1}:0]){{\n".format(write_port,self.sram.word_size-1))
        self.write_FF_setuphold(write_port)
        self.lib.write("        }\n") # pin
        self.lib.write("    }\n") #bus

    def write_data_bus(self, port):
        """ Adds data bus timing results."""
        if port in self.write_ports:
            self.write_data_bus_input(port)
        if port in self.read_ports:
            self.write_data_bus_output(port)

    def write_addr_bus(self, port):
        """ Adds addr bus timing results."""

        self.lib.write("    bus(addr{0}){{\n".format(port))
        self.lib.write("        bus_type  : addr; \n")
        self.lib.write("        direction  : input; \n")
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]/1000))
        self.lib.write("        max_transition       : {0};\n".format(self.slews[-1]))
        self.lib.write("        pin(addr{0}[{1}:0])".format(port,self.sram.addr_size-1))
        self.lib.write("{\n")

        self.write_FF_setuphold(port)
        self.lib.write("        }\n")
        self.lib.write("    }\n\n")

    def write_wmask_bus(self, port):
        """ Adds addr bus timing results."""

        self.lib.write("    bus(wmask{0}){{\n".format(port))
        self.lib.write("        bus_type  : wmask; \n")
        self.lib.write("        direction  : input; \n")
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"] / 1000))
        self.lib.write("        max_transition       : {0};\n".format(self.slews[-1]))
        self.lib.write("        pin(wmask{0}[{1}:0])".format(port, self.sram.num_wmasks - 1))
        self.lib.write("{\n")

        self.write_FF_setuphold(port)
        self.lib.write("        }\n")
        self.lib.write("    }\n\n")

    def write_control_pins(self, port):
        """ Adds control pins timing results."""
        #The control pins are still to be determined. This is a placeholder for what could be.
        ctrl_pin_names = ["csb{0}".format(port)]
        if port in self.readwrite_ports:
            ctrl_pin_names.append("web{0}".format(port))

        for i in ctrl_pin_names:
            self.lib.write("    pin({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        direction  : input; \n")
            self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]/1000))
            self.write_FF_setuphold(port)
            self.lib.write("    }\n\n")

    def write_clk_timing_power(self, port):
        """ Adds clk pin timing results."""

        self.lib.write("    pin(clk{0}){{\n".format(port))
        self.lib.write("        clock             : true;\n")
        self.lib.write("        direction  : input; \n")
        # FIXME: This depends on the clock buffer size in the control logic
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]/1000))

        self.add_clk_control_power(port)

        min_pulse_width = round_time(self.char_sram_results["min_period"])/2.0
        min_period = round_time(self.char_sram_results["min_period"])
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"min_pulse_width\"; \n")
        self.lib.write("            related_pin  : clk{0}; \n".format(port))
        self.lib.write("            rise_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"minimum_period\"; \n")
        self.lib.write("            related_pin  : clk{0}; \n".format(port))
        self.lib.write("            rise_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("    }\n\n")

    def add_clk_control_power(self, port):
        """Writes powers under the clock pin group for a specified port"""
        #Web added to read/write ports. Likely to change when control logic finished.
        web_name = ""

        if port in self.write_ports:
            if port in self.read_ports:
                web_name = " & !web{0}".format(port)
            write1_power = np.mean(self.char_port_results[port]["write1_power"])
            write0_power = np.mean(self.char_port_results[port]["write0_power"])
            self.lib.write("        internal_power(){\n")
            self.lib.write("            when : \"!csb{0}{1}\"; \n".format(port, web_name))
            self.lib.write("            rise_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(write1_power))
            self.lib.write("            }\n")
            self.lib.write("            fall_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(write0_power))
            self.lib.write("            }\n")
            self.lib.write("        }\n")

            # Disabled power.
            disabled_write1_power = np.mean(self.char_port_results[port]["disabled_write1_power"])
            disabled_write0_power = np.mean(self.char_port_results[port]["disabled_write0_power"])
            self.lib.write("        internal_power(){\n")
            self.lib.write("            when : \"csb{0}{1}\"; \n".format(port, web_name))
            self.lib.write("            rise_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(disabled_write1_power))
            self.lib.write("            }\n")
            self.lib.write("            fall_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(disabled_write0_power))
            self.lib.write("            }\n")
            self.lib.write("        }\n")

        if port in self.read_ports:
            if port in self.write_ports:
                web_name = " & web{0}".format(port)
            read1_power = np.mean(self.char_port_results[port]["read1_power"])
            read0_power = np.mean(self.char_port_results[port]["read0_power"])
            self.lib.write("        internal_power(){\n")
            self.lib.write("            when : \"!csb{0}{1}\"; \n".format(port, web_name))
            self.lib.write("            rise_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(read1_power))
            self.lib.write("            }\n")
            self.lib.write("            fall_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(read0_power))
            self.lib.write("            }\n")
            self.lib.write("        }\n")

            # Disabled power.
            disabled_read1_power = np.mean(self.char_port_results[port]["disabled_read1_power"])
            disabled_read0_power = np.mean(self.char_port_results[port]["disabled_read0_power"])
            self.lib.write("        internal_power(){\n")
            self.lib.write("            when : \"csb{0}{1}\"; \n".format(port, web_name))
            self.lib.write("            rise_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(disabled_read1_power))
            self.lib.write("            }\n")
            self.lib.write("            fall_power(scalar){\n")
            self.lib.write("                values(\"{0:.6e}\");\n".format(disabled_read0_power))
            self.lib.write("            }\n")
            self.lib.write("        }\n")

    def write_pg_pin(self):
        self.lib.write("    pg_pin({0}) ".format(self.vdd_name) + "{\n")
        self.lib.write("         voltage_name : {};\n".format(self.vdd_name.upper()))
        self.lib.write("         pg_type : primary_power;\n")
        self.lib.write("    }\n\n")
        self.lib.write("    pg_pin({0}) ".format(self.gnd_name) + "{\n")
        self.lib.write("         voltage_name : {};\n".format(self.gnd_name.upper()))
        self.lib.write("         pg_type : primary_ground;\n")
        self.lib.write("    }\n\n")

    def compute_delay(self):
        """Compute SRAM delays for current corner"""
        if self.use_model:
            model_name_lc = OPTS.model_name.lower()
            if model_name_lc == "linear_regression":
                from .linear_regression import linear_regression as model
            elif model_name_lc == "elmore":
                from .elmore import elmore as model
            elif model_name_lc == "neural_network":
                from .neural_network import neural_network as model
            elif model_name_lc == "cacti":
                from .cacti import cacti as model
            else:
                debug.error("{} model not recognized. See options.py for available models.".format(OPTS.model_name))

            m = model(self.sram, self.sp_file, self.corner)
            char_results = m.get_lib_values(self.load_slews)

        else:
            self.d = delay(self.sram, self.sp_file, self.corner)
            if (self.sram.num_spare_rows == 0):
                probe_address = "1" * self.sram.addr_size
            else:
                probe_address = "0" + "1" * (self.sram.addr_size - 1)
            probe_data = self.sram.word_size - 1
            char_results = self.d.analyze(probe_address, probe_data, self.load_slews)



        self.char_sram_results, self.char_port_results = char_results
        if 'sim_time' in self.char_sram_results:
            self.pred_time = self.char_sram_results['sim_time']
        # Add to the OPTS to be written out as part of the extended OPTS file
        # FIXME: Temporarily removed from characterization output
        # if not self.use_model:
            # OPTS.sen_path_delays = self.char_sram_results["sen_path_measures"]
            # OPTS.sen_path_names = self.char_sram_results["sen_path_names"]
            # OPTS.bl_path_delays = self.char_sram_results["bl_path_measures"]
            # OPTS.bl_path_names = self.char_sram_results["bl_path_names"]


    def compute_setup_hold(self):
        """ Do the analysis if we haven't characterized a FF yet """
        # Do the analysis if we haven't characterized a FF yet
        if not hasattr(self,"sh"):
            self.sh = setup_hold(self.corner)
            if self.use_model:
                self.times = self.sh.analytical_setuphold(self.slews,self.slews)
            else:
                self.times = self.sh.analyze(self.slews,self.slews)


    def parse_info(self,corner,lib_name, is_first_corner, time):
        """ Copies important characterization data to datasheet.info to be added to datasheet """
        if OPTS.output_datasheet_info:
            datasheet_path = OPTS.output_path
        else:
            datasheet_path = OPTS.openram_temp
        # Open for write and truncate to not conflict with a previous run using the same name
        if is_first_corner:
            datasheet = open(datasheet_path +'/datasheet.info', 'w')
        else:
            datasheet = open(datasheet_path +'/datasheet.info', 'a+')

        self.write_inp_params_datasheet(datasheet, corner, lib_name)
        self.write_signal_from_ports(datasheet,
                                "din{1}[{0}:0]".format(self.sram.word_size - 1, '{}'),
                                self.write_ports,
                                "setup_times_LH",
                                "setup_times_HL",
                                "hold_times_LH",
                                "hold_times_HL")

        # self.write_signal_from_ports(datasheet,
                                # "dout{1}[{0}:0]".format(self.sram.word_size - 1, '{}'),
                                # self.read_ports,
                                # "delay_lh",
                                # "delay_hl",
                                # "slew_lh",
                                # "slew_hl")
        for port in self.all_ports:
            #dout timing
            if port in self.read_ports:
                datasheet.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},".format(
                        "dout{1}[{0}:0]".format(self.sram.word_size - 1, port),
                        min(list(map(round_time,self.char_port_results[port]["delay_lh"]))),
                        max(list(map(round_time,self.char_port_results[port]["delay_lh"]))),

                        min(list(map(round_time,self.char_port_results[port]["delay_hl"]))),
                        max(list(map(round_time,self.char_port_results[port]["delay_hl"]))),

                        min(list(map(round_time,self.char_port_results[port]["slew_lh"]))),
                        max(list(map(round_time,self.char_port_results[port]["slew_lh"]))),

                        min(list(map(round_time,self.char_port_results[port]["slew_hl"]))),
                        max(list(map(round_time,self.char_port_results[port]["slew_hl"])))
                        ))

        self.write_signal_from_ports(datasheet,
                                "csb{}",
                                self.all_ports,
                                "setup_times_LH",
                                "setup_times_HL",
                                "hold_times_LH",
                                "hold_times_HL")

        self.write_signal_from_ports(datasheet,
                                "addr{1}[{0}:0]".format(self.sram.addr_size - 1, '{}'),
                                self.all_ports,
                                "setup_times_LH",
                                "setup_times_HL",
                                "hold_times_LH",
                                "hold_times_HL")

        self.write_signal_from_ports(datasheet,
                                "web{}",
                                self.readwrite_ports,
                                "setup_times_LH",
                                "setup_times_HL",
                                "hold_times_LH",
                                "hold_times_HL")

        self.write_power_datasheet(datasheet)

        self.write_model_params(datasheet, time)

        datasheet.write("END\n")
        datasheet.close()

    def write_inp_params_datasheet(self, datasheet, corner, lib_name):

        if OPTS.is_unit_test:
            git_id = 'FFFFFFFFFFFFFFFFFFFF'

        else:
            with open(os.devnull, 'wb') as devnull:
                # parses the most recent git commit id - reason for global git dependancy
                proc = subprocess.Popen(['git','rev-parse','HEAD'], cwd=os.path.abspath(os.environ.get("OPENRAM_HOME")) + '/', stdout=subprocess.PIPE)

                git_id = str(proc.stdout.read())

                try:
                    git_id = git_id[2:-3]
                except:
                    pass
                # check if git id is valid
                if len(git_id) != 40:
                    debug.warning("Failed to retrieve git id")
                    git_id = 'Failed to retrieve'
        current_time = datetime.date.today()

        # write static information to be parser later
        datasheet.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},".format(
                        OPTS.output_name,
                        OPTS.num_words,
                        OPTS.num_banks,
                        OPTS.num_rw_ports,
                        OPTS.num_w_ports,
                        OPTS.num_r_ports,
                        OPTS.tech_name,
                        corner[2],
                        corner[1],
                        corner[0],
                        round_time(self.char_sram_results["min_period"]),
                        self.out_dir,
                        lib_name,
                        OPTS.word_size,
                        git_id,
                        current_time,
                        OPTS.analytical_delay
                        ))

        # information of checks
        # run it only the first time
        if OPTS.top_process != "memchar":
            datasheet.write("{0},{1},".format(self.sram.drc_errors, self.sram.lvs_errors))

        # write area
        datasheet.write(str(self.sram.width * self.sram.height) + ',')

    def write_signal_from_ports(self, datasheet, signal, ports, time_pos_1, time_pos_2, time_pos_3, time_pos_4):
        for port in ports:
            datasheet.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},".format(
                    signal.format(port),
                    min(list(map(round_time,self.times[time_pos_1]))),
                    max(list(map(round_time,self.times[time_pos_1]))),

                    min(list(map(round_time,self.times[time_pos_2]))),
                    max(list(map(round_time,self.times[time_pos_2]))),

                    min(list(map(round_time,self.times[time_pos_3]))),
                    max(list(map(round_time,self.times[time_pos_3]))),

                    min(list(map(round_time,self.times[time_pos_4]))),
                    max(list(map(round_time,self.times[time_pos_4])))

                    ))

    def write_power_datasheet(self, datasheet):
        # write power information
        for port in self.all_ports:
            name = ''
            read_write = ''

            # write dynamic power usage
            if port in self.read_ports:
                web_name = " & !web{0}".format(port)
                name = "!csb{0} & clk{0}{1}".format(port, web_name)
                read_write = 'Read'

                datasheet.write("{0},{1},{2},{3},".format(
                    "power",
                    name,
                    read_write,

                    np.mean(self.char_port_results[port]["read1_power"] + self.char_port_results[port]["read0_power"])/2
                    ))

            if port in self.write_ports:
                web_name = " & web{0}".format(port)
                name = "!csb{0} & !clk{0}{1}".format(port, web_name)
                read_write = 'Write'

                datasheet.write("{0},{1},{2},{3},".format(
                        'power',
                        name,
                        read_write,
                        np.mean(self.char_port_results[port]["write1_power"] + self.char_port_results[port]["write0_power"])/2

                        ))

        # write leakage power
        control_str = 'csb0'
        for i in range(1, self.total_port_num):
            control_str += ' & csb{0}'.format(i)

        datasheet.write("{0},{1},{2},".format('leak', control_str, self.char_sram_results["leakage_power"]))

    def write_model_params(self, datasheet, time):
        """Write values which will be used in the analytical model as inputs"""
        datasheet.write("{0},{1},".format('sim_time', time))
        datasheet.write("{0},{1},".format('words_per_row', OPTS.words_per_row))
        datasheet.write("{0},{1},".format('slews', list(self.slews)))
        datasheet.write("{0},{1},".format('loads', list(self.loads)))

        for port in self.read_ports:
            datasheet.write("{0},{1},".format('cell_rise_{}'.format(port), self.char_port_results[port]["delay_lh"]))
            datasheet.write("{0},{1},".format('cell_fall_{}'.format(port), self.char_port_results[port]["delay_hl"]))
            datasheet.write("{0},{1},".format('rise_transition_{}'.format(port), self.char_port_results[port]["slew_lh"]))
            datasheet.write("{0},{1},".format('fall_transition_{}'.format(port), self.char_port_results[port]["slew_hl"]))

        for port in self.write_ports:
            write1_power = np.mean(self.char_port_results[port]["write1_power"])
            write0_power = np.mean(self.char_port_results[port]["write0_power"])
            datasheet.write("{0},{1},".format('write_rise_power_{}'.format(port), write1_power))
            #FIXME: should be write_fall_power
            datasheet.write("{0},{1},".format('write_fall_power_{}'.format(port), write0_power))

        for port in self.read_ports:
            read1_power = np.mean(self.char_port_results[port]["read1_power"])
            read0_power = np.mean(self.char_port_results[port]["read0_power"])
            datasheet.write("{0},{1},".format('read_rise_power_{}'.format(port), read1_power))
            #FIXME: should be read_fall_power
            datasheet.write("{0},{1},".format('read_fall_power_{}'.format(port), read0_power))
