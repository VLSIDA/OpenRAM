import os,sys,re
import debug
import math
import setup_hold
import delay
import charutils as ch
import tech
import numpy as np
from globals import OPTS

class lib:
    """ lib file generation."""
    
    def __init__(self, out_dir, sram, sp_file, use_model=OPTS.analytical_delay):
        self.out_dir = out_dir
        self.sram = sram
        self.sp_file = sp_file        
        self.use_model = use_model

        self.prepare_tables()
        
        self.create_corners()
        
        self.characterize_corners()
        

    def prepare_tables(self):
        """ Determine the load/slews if they aren't specified in the config file. """
        # These are the parameters to determine the table sizes
        #self.load_scales = np.array([0.1, 0.25, 0.5, 1, 2, 4, 8])
        self.load_scales = np.array([0.25, 1, 8])
        #self.load_scales = np.array([0.25, 1])
        self.load = tech.spice["dff_in_cap"]
        self.loads = self.load_scales*self.load
        debug.info(1,"Loads: {0}".format(self.loads))
        
        #self.slew_scales = np.array([0.1, 0.25, 0.5, 1, 2, 4, 8])
        self.slew_scales = np.array([0.25, 1, 8])        
        #self.slew_scales = np.array([0.25, 1])
        self.slew = tech.spice["rise_time"]        
        self.slews = self.slew_scales*self.slew
        debug.info(1,"Slews: {0}".format(self.slews))

        
    def create_corners(self):
        """ Create corners for characterization. """
        # Get the corners from the options file
        self.temperatures = OPTS.temperatures
        self.supply_voltages = OPTS.supply_voltages
        self.process_corners = OPTS.process_corners

        # Enumerate all possible corners
        self.corners = []
        self.lib_files = []
        for proc in self.process_corners:
            for temp in self.temperatures:
                for volt in self.supply_voltages:
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
        for (self.corner,lib_name) in zip(self.corners,self.lib_files):
            debug.info(1,"Corner: " + str(self.corner))
            (self.process, self.voltage, self.temperature) = self.corner
            self.lib = open(lib_name, "w")
            debug.info(1,"Writing to {0}".format(lib_name))
            self.characterize()
            self.lib.close()

    def characterize(self):
        """ Characterize the current corner. """

        self.compute_delay()

        self.compute_setup_hold()

        self.write_header()
        
        self.write_data_bus()
        
        self.write_addr_bus()
        
        self.write_control_pins()
        
        self.write_clk()

        self.write_footer()

        
    def write_footer(self):
        """ Write the footer """
        self.lib.write("}\n")

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

        # Leakage is included in dynamic when macro is enabled
        self.lib.write("    leakage_power () {\n")
        self.lib.write("      when : \"CSb\";\n")
        self.lib.write("      value : {};\n".format(self.char_results["leakage_power"]))
        self.lib.write("    }\n")
        self.lib.write("    cell_leakage_power : {};\n".format(0))
        
    
    def write_units(self):
        """ Adds default units for time, voltage, current,..."""
        
        self.lib.write("    time_unit : \"1ns\" ;\n")
        self.lib.write("    voltage_unit : \"1v\" ;\n")
        self.lib.write("    current_unit : \"1mA\" ;\n")
        self.lib.write("    resistance_unit : \"1kohm\" ;\n")
        self.lib.write("    capacitive_load_unit(1 ,fF) ;\n")
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

        self.lib.write("    nom_voltage : {};\n".format(tech.spice["nom_supply_voltage"]))
        self.lib.write("    nom_temperature : {};\n".format(tech.spice["nom_temperature"]))
        self.lib.write("    nom_process : {};\n".format(1.0))

        self.lib.write("    default_cell_leakage_power    : 0.0 ;\n")
        self.lib.write("    default_leakage_power_density : 0.0 ;\n")
        self.lib.write("    default_input_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_inout_pin_cap    : 1.0 ;\n")
        self.lib.write("    default_output_pin_cap   : 0.0 ;\n")
        self.lib.write("    default_max_transition   : 0.5 ;\n")
        self.lib.write("    default_fanout_load      : 1.0 ;\n")
        self.lib.write("    default_max_fanout   : 4.0 ;\n")
        self.lib.write("    default_connection_class : universal ;\n\n")

    def create_list(self,values):
        """ Helper function to create quoted, line wrapped list """
        list_values = ", ".join(str(v) for v in values)
        return "\"{0}\"".format(list_values)

    def create_array(self,values, length):
        """ Helper function to create quoted, line wrapped array with each row of given length """
        # check that the length is a multiple or give an error!
        debug.check(len(values)%length == 0,"Values are not a multiple of the length. Cannot make a full array.")
        rounded_values = map(ch.round_time,values)
        split_values = [rounded_values[i:i+length] for i in range(0, len(rounded_values), length)]
        formatted_rows = map(self.create_list,split_values)
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
            self.write_index(2,self.loads)
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
        """ Adds format of DATA and ADDR bus."""
    
        self.lib.write("\n\n")
        self.lib.write("    type (DATA){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.sram.word_size))
        self.lib.write("    bit_from : 0;\n")
        self.lib.write("    bit_to : {0};\n".format(self.sram.word_size - 1))
        self.lib.write("    }\n\n")

        self.lib.write("    type (ADDR){\n")
        self.lib.write("    base_type : array;\n")
        self.lib.write("    data_type : bit;\n")
        self.lib.write("    bit_width : {0};\n".format(self.sram.addr_size))
        self.lib.write("    bit_from : 0;\n")
        self.lib.write("    bit_to : {0};\n".format(self.sram.addr_size - 1))
        self.lib.write("    }\n\n")


    def write_FF_setuphold(self):
        """ Adds Setup and Hold timing results"""

        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : setup_rising; \n")
        self.lib.write("            related_pin  : \"clk\"; \n")
        self.lib.write("            rise_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = map(ch.round_time,self.times["setup_times_LH"])
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = map(ch.round_time,self.times["setup_times_HL"])
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type : hold_rising; \n")
        self.lib.write("            related_pin  : \"clk\"; \n")
        self.lib.write("            rise_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = map(ch.round_time,self.times["hold_times_LH"])
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("              }\n")
        self.lib.write("            fall_constraint(CONSTRAINT_TABLE) {\n")
        rounded_values = map(ch.round_time,self.times["hold_times_HL"])
        self.write_values(rounded_values,len(self.slews),"            ")
        self.lib.write("            }\n")
        self.lib.write("        }\n")



    def write_data_bus(self):
        """ Adds data bus timing results."""

        self.lib.write("    bus(DATA){\n")
        self.lib.write("        bus_type  : DATA; \n")
        self.lib.write("        direction  : inout; \n")
        # This is conservative, but limit to range that we characterized.
        self.lib.write("        max_capacitance : {0};  \n".format(max(self.loads)))
        self.lib.write("        min_capacitance : {0};  \n".format(min(self.loads)))        
        self.lib.write("        three_state : \"!OEb & !clk\"; \n")
        self.lib.write("        memory_write(){ \n")
        self.lib.write("            address : ADDR; \n")
        self.lib.write("            clocked_on  : clk; \n")
        self.lib.write("        }\n")
        self.lib.write("        memory_read(){ \n")
        self.lib.write("            address : ADDR; \n")
        self.lib.write("        }\n")


        self.lib.write("        pin(DATA[{0}:0]){{\n".format(self.sram.word_size - 1))
        self.write_FF_setuphold()
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_sense : non_unate; \n")
        self.lib.write("            related_pin : \"clk\"; \n")
        self.lib.write("            timing_type : falling_edge; \n")
        self.lib.write("            cell_rise(CELL_TABLE) {\n")
        self.write_values(self.char_results["delay_lh"],len(self.loads),"            ")
        self.lib.write("            }\n") # rise delay
        self.lib.write("            cell_fall(CELL_TABLE) {\n")
        self.write_values(self.char_results["delay_hl"],len(self.loads),"            ")
        self.lib.write("            }\n") # fall delay
        self.lib.write("            rise_transition(CELL_TABLE) {\n")
        self.write_values(self.char_results["slew_lh"],len(self.loads),"            ")
        self.lib.write("            }\n") # rise trans
        self.lib.write("            fall_transition(CELL_TABLE) {\n")
        self.write_values(self.char_results["slew_hl"],len(self.loads),"            ")
        self.lib.write("            }\n") # fall trans
        self.lib.write("        }\n") # timing
        self.lib.write("        }\n") # pin        
        self.lib.write("    }\n\n") # bus


    def write_addr_bus(self):
        """ Adds addr bus timing results."""

        self.lib.write("    bus(ADDR){\n")
        self.lib.write("        bus_type  : ADDR; \n")
        self.lib.write("        direction  : input; \n")
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]))
        self.lib.write("        max_transition       : {0};\n".format(self.slews[-1]))
        self.lib.write("        pin(ADDR[{0}:0])".format(self.sram.addr_size - 1))
        self.lib.write("{\n")
        
        self.write_FF_setuphold()
        self.lib.write("        }\n")        
        self.lib.write("    }\n\n")


    def write_control_pins(self):
        """ Adds control pins timing results."""

        ctrl_pin_names = ["CSb", "OEb", "WEb"]
        for i in ctrl_pin_names:
            self.lib.write("    pin({0})".format(i))
            self.lib.write("{\n")
            self.lib.write("        direction  : input; \n")
            self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]))
            self.write_FF_setuphold()
            self.lib.write("    }\n\n")


    def write_clk(self):
        """ Adds clk pin timing results."""

        self.lib.write("    pin(clk){\n")
        self.lib.write("        clock             : true;\n")
        self.lib.write("        direction  : input; \n")
        # This should actually be a min inverter cap, but ok...
        self.lib.write("        capacitance : {0};  \n".format(tech.spice["dff_in_cap"]))

        # Find the average power of 1 and 0 bits for writes and reads over all loads/slews
        # Could make it a table, but this is fine for now.
        avg_write_power = np.mean(self.char_results["write1_power"] + self.char_results["write0_power"])
        avg_read_power = np.mean(self.char_results["read1_power"] + self.char_results["read0_power"])        

        # Equally divide read/write power between first and second half of clock period
        self.lib.write("        internal_power(){\n")
        self.lib.write("            when : \"!CSb & clk & !WEb\"; \n")
        self.lib.write("            rise_power(scalar){\n")
        self.lib.write("                values(\"{0}\");\n".format(avg_write_power/2.0))
        self.lib.write("            }\n")
        self.lib.write("            fall_power(scalar){\n")
        self.lib.write("                values(\"{0}\");\n".format(avg_write_power/2.0))
        self.lib.write("            }\n")
        self.lib.write("        }\n")

        self.lib.write("        internal_power(){\n")
        self.lib.write("            when : \"!CSb & !clk & WEb\"; \n")
        self.lib.write("            rise_power(scalar){\n")
        self.lib.write("                values(\"{0}\");\n".format(avg_read_power/2.0))
        self.lib.write("            }\n")
        self.lib.write("            fall_power(scalar){\n")
        self.lib.write("                values(\"{0}\");\n".format(avg_read_power/2.0))
        self.lib.write("            }\n")
        self.lib.write("        }\n")
        # Have 0 internal power when disabled, this will be represented as leakage power.
        self.lib.write("        internal_power(){\n")
        self.lib.write("            when : \"CSb\"; \n")
        self.lib.write("            rise_power(scalar){\n")
        self.lib.write("                values(\"0\");\n")
        self.lib.write("            }\n")
        self.lib.write("            fall_power(scalar){\n")
        self.lib.write("                values(\"0\");\n")
        self.lib.write("            }\n")
        self.lib.write("        }\n")

        min_pulse_width = ch.round_time(self.char_results["min_period"])/2.0
        min_period = ch.round_time(self.char_results["min_period"])
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"min_pulse_width\"; \n")
        self.lib.write("            related_pin  : clk; \n")
        self.lib.write("            rise_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_pulse_width))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("        timing(){ \n")
        self.lib.write("            timing_type :\"minimum_period\"; \n")
        self.lib.write("            related_pin  : clk; \n")
        self.lib.write("            rise_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("            fall_constraint(scalar) {\n")
        self.lib.write("                values(\"{0}\"); \n".format(min_period))
        self.lib.write("            }\n")
        self.lib.write("         }\n")
        self.lib.write("    }\n")
        self.lib.write("    }\n")

    def compute_delay(self):
        """ Do the analysis if we haven't characterized the SRAM yet """
        try:
            self.d
        except AttributeError:
            self.d = delay.delay(self.sram, self.sp_file, self.corner)
            if self.use_model:
                self.char_results = self.d.analytical_delay(self.sram,self.slews,self.loads)
            else:
                probe_address = "1" * self.sram.addr_size
                probe_data = self.sram.word_size - 1
                self.char_results = self.d.analyze(probe_address, probe_data, self.slews, self.loads)


    def compute_setup_hold(self):
        """ Do the analysis if we haven't characterized a FF yet """
        # Do the analysis if we haven't characterized a FF yet
        try:
            self.sh
        except AttributeError:
            self.sh = setup_hold.setup_hold(self.corner)
            if self.use_model:
                self.times = self.sh.analytical_setuphold(self.slews,self.loads)
            else:
                self.times = self.sh.analyze(self.slews,self.slews)
                
