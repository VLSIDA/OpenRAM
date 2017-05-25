import os
import sys
import re
import globals
import debug
import tech
import math
import setup_hold
import delay
import charutils as ch


OPTS = globals.get_opts()

class lib:
    """ lib file generation."""
    
    def __init__(self, libname, sram, spfile, use_model=OPTS.analytical_delay):
        self.name = sram.name
        self.num_words = sram.num_words
        self.word_size = sram.word_size
        self.addr_size = sram.addr_size

        self.sh = setup_hold.setup_hold()
        self.d = delay.delay(sram, spfile)

        debug.info(1,"Writing to {0}".format(libname))
        self.lib = open(libname, "w")

        self.lib.write("library ({0}_lib)".format(self.name))
        self.lib.write("{\n")
        self.lib.write("    delay_model : \"table_lookup\";\n")
        
        self.write_units()
        self.write_defaults()
        self.write_LUT()

        self.lib.write("    default_operating_conditions : TT; \n")
        
        self.write_bus()

        self.lib.write("cell ({0})".format(self.name))
        self.lib.write("{\n")
        self.lib.write("    memory(){ \n")
        self.lib.write("    type : ram;\n")
        self.lib.write("    address_width : {0};\n".format(self.addr_size))
        self.lib.write("    word_width : {0};\n".format(self.word_size))
        self.lib.write("    }\n")
        self.lib.write("    interface_timing : true;\n")
        self.lib.write("    dont_use  : true;\n")
        self.lib.write("    map_only   : true;\n")
        self.lib.write("    dont_touch : true;\n")
        self.lib.write("    area : {0};\n\n".format(sram.width * sram.height))

        times = self.sh.analyze()
        
        for i in times.keys():
            times[i] = ch.round_time(times[i])


        probe_address = "1" * self.addr_size
        probe_data = self.word_size - 1

        if use_model:
            data = sram.analytical_model(slope=0.001)
        else:
            data = self.d.analyze(probe_address, probe_data)

        for i in data.keys():
            if i == "read_power" or i == "write_power":
                continue
            data[i] = ch.round_time(data[i])

      
        self.write_data_bus(data, times)
        self.write_addr_bus(times)
        self.write_control_pins(times)
        self.write_clk(data)
        
        self.lib.close()
        
    
    def write_units(self):
        """ Adds default units for time, voltage, current,..."""
        
        self.lib.write("    time_unit : \"1ns\" ;\n")
        self.lib.write("    voltage_unit : \"1v\" ;\n")
        self.lib.write("    current_unit : \"1mA\" ;\n")
        self.lib.write("    resistance_unit : \"1kohm\" ;\n")
        self.lib.write("    capacitive_load_unit(1 ,fF) ;\n")
        self.lib.write("    leakage_power_unit : \"1mW\" ;\n")
        self.lib.write("    pulling_resistance_unit :\"1kohm\" ;\n")
        self.lib.write("    operating_conditions(TT){\n")
        self.lib.write("    voltage : {0} ;\n".format(tech.spice["supply_voltage"]))
        self.lib.write("    temperature : 25.000 ;\n")
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

        self.lib.write("    default_cell_leakage_power    : 0.0 ;\n")
        self.lib.write("    default_leakage_power_density : 0.0 ;\n")
        self.lib.write("    default_input_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_inout_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_output_pin_cap   : 0.0 ;\n")
        self.lib.write("    default_max_transition   : 0.5 ;\n")
        self.lib.write("    default_fanout_load      : 1.0 ;\n")
        self.lib.write("    default_max_fanout   : 4.0 ;\n")
        self.lib.write("    default_connection_class : universal ;\n\n")
        
    def write_LUT(self):
        """ Adds lookup_table format (A 1x1 lookup_table)."""
        
        Tran = ["CELL_UP_FOR_CLOCK" , "CELL_DN_FOR_CLOCK"]
        for i in Tran:
            self.lib.write("    lu_table_template({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        variable_1 : input_net_transition;\n")
            self.lib.write("        variable_2 : total_output_net_capacitance;\n")
            self.lib.write("        index_1 (\"0.5\");\n")
            self.lib.write("        index_2 (\"0.5\");\n")
            self.lib.write("    }\n\n")

        CONS = ["CONSTRAINT_HIGH_POS" , "CONSTRAINT_LOW_POS"]
        for i in CONS:
            self.lib.write("    lu_table_template({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        variable_1 : related_pin_transition;\n")
            self.lib.write("        variable_2 : constrained_pin_transition;\n")
            self.lib.write("        index_1 (\"0.5\");\n")
            self.lib.write("        index_2 (\"0.5\");\n")
            self.lib.write("    }\n\n")
    
        self.lib.write("    lu_table_template(CLK_TRAN) {\n")
        self.lib.write("        variable_1 : constrained_pin_transition;\n")
        self.lib.write("        index_1 (\"0.5\");\n")
        self.lib.write("    }\n\n")
    
        self.lib.write("    lu_table_template(TRAN) {\n")
        self.lib.write("        variable_1 : total_output_net_capacitance;\n")
        self.lib.write("        index_1 (\"0.5\");\n")
        self.lib.write("    }\n\n")

        CONS2 = ["INPUT_BY_TRANS_FOR_CLOCK" , "INPUT_BY_TRANS_FOR_SIGNAL"]
        for i in CONS2:
            self.lib.write("    power_lut_template({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        variable_1 : input_transition_time;\n")
            self.lib.write("        index_1 (\"0.5\");\n")
            self.lib.write("    }\n\n")
    
    def write_bus(self):
        """ Adds format of DATA and ADDR bus."""
    
        self.lib.write("\n\n")
        self.lib.write("    type (DATA){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.word_size))
        self.lib.write("    bit_from : 0;\n")
        self.lib.write("    bit_to : {0};\n".format(self.word_size - 1))
        self.lib.write("    }\n\n")

        self.lib.write("    type (ADDR){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.addr_size))
        self.lib.write("    bit_from : 0;\n")
        self.lib.write("    bit_to : {0};\n".format(self.addr_size - 1))
        self.lib.write("    }\n\n")


    def write_timing(self, times):
        """ Adds Setup and Hold timing results"""

        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : setup_rising; \n")
        self.lib.write("            related_pin  : \"clk\"; \n")
        self.lib.write("            rise_constraint(CONSTRAINT_HIGH_POS) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(times["setup_time_one"]))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_LOW_POS) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(times["setup_time_zero"]))
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : hold_rising; \n")
        self.lib.write("            related_pin  : \"clk\"; \n")
        self.lib.write("            rise_constraint(CONSTRAINT_HIGH_POS) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(times["hold_time_one"]))
        self.lib.write("              }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_LOW_POS) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(times["hold_time_zero"]))
        self.lib.write("            }\n")
        self.lib.write("        }\n")



    def write_data_bus(self, data, times):
        """ Adds data bus timing results."""
        self.lib.write("    bus(DATA){\n")
        self.lib.write("        bus_type  : DATA; \n")
        self.lib.write("        direction  : inout; \n")
        self.lib.write("        max_capacitance : {0};  \n".format(tech.spice["FF_in_cap"] + tech.spice["tri_gate_out_cap"]  ))
        self.lib.write("        pin(DATA[{0}:0])".format(self.word_size - 1))
        self.lib.write("{\n")
        self.lib.write("        }\n")
        self.lib.write("        three_state : \"!OEb & !clk\"; \n")

        self.lib.write("        memory_write(){ \n")
        self.lib.write("            address : ADDR; \n")
        self.lib.write("            clocked_on  : clk; \n")
        self.lib.write("        }\n")
        self.lib.write("        internal_power(){\n")
        self.lib.write("            when : \"OEb & !clk\"; \n")
        self.lib.write("            rise_power(INPUT_BY_TRANS_FOR_SIGNAL){\n")
        self.lib.write("                values(\"{0}\");\n".format(data["write_power"]* 1e3))
        self.lib.write("            }\n")
        self.lib.write("            fall_power(INPUT_BY_TRANS_FOR_SIGNAL){\n")
        self.lib.write("                values(\"{0}\");\n".format(data["write_power"]* 1e3))
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.write_timing(times)
       
        self.lib.write("        memory_read(){ \n")
        self.lib.write("            address : ADDR; \n")
        self.lib.write("        }\n")
        self.lib.write("        internal_power(){\n")
        self.lib.write("            when : \"!OEb & !clk\"; \n")
        self.lib.write("            rise_power(INPUT_BY_TRANS_FOR_SIGNAL){\n")
        self.lib.write("                values(\"{0}\");\n".format(data["read_power"]* 1e3))
        self.lib.write("            }\n")
        self.lib.write("            fall_power(INPUT_BY_TRANS_FOR_SIGNAL){\n")
        self.lib.write("                values(\"{0}\");\n".format(data["read_power"]* 1e3))
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_sense : non_unate; \n")
        self.lib.write("            related_pin : \"clk\"; \n")
        self.lib.write("            timing_type : rising_edge; \n")
        self.lib.write("            cell_rise(CELL_UP_FOR_CLOCK) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(data["delay1"]))
        self.lib.write("            }\n")
        self.lib.write("            cell_fall(CELL_DN_FOR_CLOCK) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(data["delay0"]))
        self.lib.write("            }\n")
        self.lib.write("        rise_transition(TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(data["delay1"]))
        self.lib.write("              }\n")
        self.lib.write("        fall_transition(TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(data["delay0"]))
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.lib.write("    }\n\n")


    def write_addr_bus(self, times):
        """ Adds addr bus timing results."""

        self.lib.write("    bus(ADDR){\n")
        self.lib.write("        bus_type  : ADDR; \n")
        self.lib.write("        direction  : input; \n")
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["FF_in_cap"]))
        self.lib.write("        max_transition       : 0.5;\n")
        self.lib.write("        fanout_load          : 1.000000;\n")
        self.lib.write("        pin(ADDR[{0}:0])".format(self.addr_size - 1))
        self.lib.write("{\n")
        self.lib.write("        }\n")
        self.write_timing(times)
        self.lib.write("    }\n\n")


    def write_control_pins(self, times):
        """ Adds control pins timing results."""

        ctrl_pin_names = ["CSb", "OEb", "WEb"]
        for i in ctrl_pin_names:
            self.lib.write("    pin({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        direction  : input; \n")
            self.lib.write("        capacitance : {0};  \n".format(tech.spice["FF_in_cap"]))
            self.write_timing(times)
            self.lib.write("    }\n\n")


    def write_clk(self, data):
        """ Adds clk pin timing results."""
        
        self.lib.write("    pin(clk){\n")
        self.lib.write("        clock             : true;\n")
        self.lib.write("        direction  : input; \n")
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["FF_in_cap"]))
        min_pulse_width = (ch.round_time(data["min_period1"]) + ch.round_time(data["min_period0"]))/2.0
        min_period = ch.round_time(data["min_period1"]) + ch.round_time(data["min_period0"])
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"min_pulse_width\"; \n")
        self.lib.write("            related_pin  : clk; \n")
        self.lib.write("            rise_constraint(CLK_TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(CLK_TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"minimum_period\"; \n")
        self.lib.write("            related_pin  : clk; \n")
        self.lib.write("            rise_constraint(CLK_TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(CLK_TRAN) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("    }\n")
        self.lib.write("    }\n")
        self.lib.write("}\n")
