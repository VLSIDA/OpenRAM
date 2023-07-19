# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram.base import timing_graph
from openram.sram_factory import factory
from openram import tech
from openram import OPTS


class simulation():

    def __init__(self, sram, spfile, corner):
        self.sram = sram

        self.name = self.sram.name
        self.word_size = self.sram.word_size
        self.bank_addr_size = self.sram.bank_addr_size
        self.write_size = self.sram.write_size
        self.num_spare_rows = self.sram.num_spare_rows
        if not self.sram.num_spare_cols:
            self.num_spare_cols = 0
        else:
            self.num_spare_cols = self.sram.num_spare_cols
        if not spfile:
            self.sp_file = OPTS.openram_temp + "sram.sp"
        else:
            self.sp_file = spfile

        self.all_ports = self.sram.all_ports
        self.readwrite_ports = self.sram.readwrite_ports
        self.read_ports = self.sram.read_ports
        self.write_ports = self.sram.write_ports
        self.words_per_row = self.sram.words_per_row
        self.num_rows = self.sram.num_rows
        self.num_cols = self.sram.num_cols
        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

    def create_measurement_names(self):
        """ Create measurement names. The names themselves currently define the type of measurement """

        self.delay_meas_names = ["delay_lh", "delay_hl", "slew_lh", "slew_hl"]
        self.power_meas_names = ["read0_power",
                                 "read1_power",
                                 "write0_power",
                                 "write1_power",
                                 "disabled_read0_power",
                                 "disabled_read1_power",
                                 "disabled_write0_power",
                                 "disabled_write1_power"]
        # self.voltage_when_names = ["volt_bl", "volt_br"]
        # self.bitline_delay_names = ["delay_bl", "delay_br"]

    def set_corner(self, corner):
        """ Set the corner values """
        self.corner = corner
        (self.process, self.vdd_voltage, self.temperature) = corner

    def set_spice_constants(self):
        """ sets feasible timing parameters """
        self.period = tech.spice["feasible_period"]
        self.slew = tech.spice["rise_time"] * 2
        self.load = tech.spice["dff_in_cap"] * 4

        self.v_high = self.vdd_voltage - tech.spice["nom_threshold"]
        self.v_low = tech.spice["nom_threshold"]
        self.gnd_voltage = 0

    def create_signal_names(self):
        self.addr_name = "a"
        self.din_name = "din"
        self.dout_name = "dout"
        self.pins = self.gen_pin_names(port_signal_names=(self.addr_name, self.din_name, self.dout_name),
                                       port_info=(len(self.all_ports), self.write_ports, self.read_ports),
                                       abits=self.bank_addr_size,
                                       dbits=self.word_size + self.num_spare_cols)
        debug.check(len(self.sram.pins) == len(self.pins),
                    "Number of pins generated for characterization \
                    do not match pins of SRAM\nsram.pins = {0}\npin_names = {1}".format(self.sram.pins,
                                                                                        self.pins))

    def set_stimulus_variables(self):
        # Clock signals
        self.cycle_times = []
        self.t_current = 0

        # control signals: only one cs_b for entire multiported sram, one we_b for each write port
        self.csb_values = {port: [] for port in self.all_ports}
        self.web_values = {port: [] for port in self.readwrite_ports}

        # Raw values added as a bit vector
        self.addr_value = {port: [] for port in self.all_ports}
        self.data_value = {port: [] for port in self.write_ports}
        self.wmask_value = {port: [] for port in self.write_ports}
        self.spare_wen_value = {port: [] for port in self.write_ports}

        # Three dimensional list to handle each addr and data bits for each port over the number of checks
        self.addr_values = {port: [[] for bit in range(self.bank_addr_size)] for port in self.all_ports}
        self.data_values = {port: [[] for bit in range(self.word_size + self.num_spare_cols)] for port in self.write_ports}
        self.wmask_values = {port: [[] for bit in range(self.num_wmasks)] for port in self.write_ports}
        self.spare_wen_values = {port: [[] for bit in range(self.num_spare_cols)] for port in self.write_ports}

        # For generating comments in SPICE stimulus
        self.cycle_comments = []
        self.fn_cycle_comments = []

    def set_probe(self, probe_address, probe_data):
        """
        Probe address and data can be set separately to utilize other
        functions in this characterizer besides analyze.
        """

        self.probe_address = probe_address
        self.probe_data = probe_data
        self.bitline_column = self.get_data_bit_column_number(probe_address, probe_data)
        self.wordline_row = self.get_address_row_number(probe_address)

    def get_data_bit_column_number(self, probe_address, probe_data):
        """Calculates bitline column number of data bit under test using bit position and mux size"""

        if self.sram.col_addr_size>0:
            col_address = int(probe_address[0:self.sram.col_addr_size], 2)
        else:
            col_address = 0
        bl_column = int(self.sram.words_per_row * probe_data + col_address)
        return bl_column

    def get_address_row_number(self, probe_address):
        """Calculates wordline row number of data bit under test using address and column mux size"""

        return int(probe_address[self.sram.col_addr_size:], 2)

    def add_control_one_port(self, port, op):
        """Appends control signals for operation to a given port"""
        # Determine values to write to port
        web_val = 1
        csb_val = 1
        if op == "read":
            csb_val = 0
        elif op == "write":
            csb_val = 0
            web_val = 0
        elif op != "noop":
            debug.error("Could not add control signals for port {0}. Command {1} not recognized".format(port, op), 1)

        # Append the values depending on the type of port
        self.csb_values[port].append(csb_val)
        # If port is in both lists, add rw control signal. Condition indicates its a RW port.
        if port in self.readwrite_ports:
            self.web_values[port].append(web_val)

    def add_data(self, data, port):
        """ Add the array of data values """
        debug.check(len(data)==(self.word_size + self.num_spare_cols), "Invalid data word size.")

        self.data_value[port].append(data)
        bit = self.word_size + self.num_spare_cols - 1
        for c in data:
            if c=="0":
                self.data_values[port][bit].append(0)
            elif c=="1":
                self.data_values[port][bit].append(1)
            else:
                debug.error("Non-binary data string", 1)
            bit -= 1

    def add_address(self, address, port):
        """ Add the array of address values """
        debug.check(len(address)==self.bank_addr_size, "Invalid address size.")

        self.addr_value[port].append(address)
        bit = self.bank_addr_size - 1
        for c in address:
            if c=="0":
                self.addr_values[port][bit].append(0)
            elif c=="1":
                self.addr_values[port][bit].append(1)
            else:
                debug.error("Non-binary address string", 1)
            bit -= 1

    def add_wmask(self, wmask, port):
        """ Add the array of address values """
        debug.check(len(wmask) == self.num_wmasks, "Invalid wmask size.")

        self.wmask_value[port].append(wmask)
        bit = self.num_wmasks - 1
        for c in wmask:
            if c == "0":
                self.wmask_values[port][bit].append(0)
            elif c == "1":
                self.wmask_values[port][bit].append(1)
            else:
                debug.error("Non-binary wmask string", 1)
            bit -= 1

    def add_spare_wen(self, spare_wen, port):
        """ Add the array of spare write enable values (for spare cols) """
        debug.check(len(spare_wen) == self.num_spare_cols, "Invalid spare enable size.")

        self.spare_wen_value[port].append(spare_wen)
        bit = self.num_spare_cols - 1
        for c in spare_wen:
            if c == "0":
                self.spare_wen_values[port][bit].append(0)
            elif c == "1":
                self.spare_wen_values[port][bit].append(1)
            else:
                debug.error("Non-binary spare enable signal string", 1)
            bit -= 1

    def add_write(self, comment, address, data, wmask, port):
        """ Add the control values for a write cycle. """
        debug.check(port in self.write_ports,
                    "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port,
                                                                                              self.write_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment(port, comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period

        self.add_control_one_port(port, "write")
        self.add_data(data, port)
        self.add_address(address, port)
        self.add_wmask(wmask, port)
        self.add_spare_wen("1" * self.num_spare_cols, port)

        # Add noops to all other ports.
        for unselected_port in self.all_ports:
            if unselected_port != port:
                self.add_noop_one_port(unselected_port)

    def add_read(self, comment, address, port):
        """ Add the control values for a read cycle. """
        debug.check(port in self.read_ports,
                    "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port,
                                                                                             self.read_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment(port, comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.add_control_one_port(port, "read")
        self.add_address(address, port)

        # If the port is also a readwrite then add
        # the same value as previous cycle
        if port in self.write_ports:
            try:
                self.add_data(self.data_value[port][-1], port)
            except:
                self.add_data("0" * (self.word_size + self.num_spare_cols), port)
            try:
                self.add_wmask(self.wmask_value[port][-1], port)
            except:
                self.add_wmask("0" * self.num_wmasks, port)
            self.add_spare_wen("0" * self.num_spare_cols, port)

        # Add noops to all other ports.
        for unselected_port in self.all_ports:
            if unselected_port != port:
                self.add_noop_one_port(unselected_port)

    def add_noop_all_ports(self, comment):
        """ Add the control values for a noop to all ports. """
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)
        self.append_cycle_comment("All", comment)

        self.cycle_times.append(self.t_current)
        self.t_current += self.period

        for port in self.all_ports:
            self.add_noop_one_port(port)

    def add_write_one_port(self, comment, address, data, wmask, port):
        """ Add the control values for a write cycle. Does not increment the period. """
        debug.check(port in self.write_ports,
                    "Cannot add write cycle to a read port. Port {0}, Write Ports {1}".format(port,
                                                                                              self.write_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)

        self.add_control_one_port(port, "write")
        self.add_data(data, port)
        self.add_address(address, port)
        self.add_wmask(wmask, port)
        # Disable spare writes for now
        self.add_spare_wen("0" * self.num_spare_cols, port)

    def add_read_one_port(self, comment, address, port):
        """ Add the control values for a read cycle. Does not increment the period. """
        debug.check(port in self.read_ports,
                    "Cannot add read cycle to a write port. Port {0}, Read Ports {1}".format(port,
                                                                                             self.read_ports))
        debug.info(2, comment)
        self.fn_cycle_comments.append(comment)

        self.add_control_one_port(port, "read")
        self.add_address(address, port)

        # If the port is also a readwrite then add
        # the same value as previous cycle
        if port in self.write_ports:
            try:
                self.add_data(self.data_value[port][-1], port)
            except:
                self.add_data("0" * (self.word_size + self.num_spare_cols), port)
            try:
                self.add_wmask(self.wmask_value[port][-1], port)
            except:
                self.add_wmask("0" * self.num_wmasks, port)
            self.add_spare_wen("0" * self.num_spare_cols, port)

    def add_noop_one_port(self, port):
        """ Add the control values for a noop to a single port. Does not increment the period. """
        self.add_control_one_port(port, "noop")

        try:
            self.add_address(self.addr_value[port][-1], port)
        except:
            self.add_address("0" * self.bank_addr_size, port)

        # If the port is also a readwrite then add
        # the same value as previous cycle
        if port in self.write_ports:
            try:
                self.add_data(self.data_value[port][-1], port)
            except:
                self.add_data("0" * (self.word_size + self.num_spare_cols), port)
            try:
                self.add_wmask(self.wmask_value[port][-1], port)
            except:
                self.add_wmask("0" * self.num_wmasks, port)
            self.add_spare_wen("0" * self.num_spare_cols, port)

    def add_noop_clock_one_port(self, port):
        """ Add the control values for a noop to a single port. Increments the period. """
        debug.info(2, 'Clock only on port {}'.format(port))
        self.fn_cycle_comments.append('Clock only on port {}'.format(port))
        self.append_cycle_comment(port, 'Clock only on port {}'.format(port))

        self.cycle_times.append(self.t_current)
        self.t_current += self.period

        self.add_noop_one_port(port)

        # Add noops to all other ports.
        for unselected_port in self.all_ports:
            if unselected_port != port:
                self.add_noop_one_port(unselected_port)

    def append_cycle_comment(self, port, comment):
        """Add comment to list to be printed in stimulus file"""
        # Clean up time before appending. Make spacing dynamic as well.
        time = "{0:.2f} ns:".format(self.t_current)
        time_spacing = len(time) + 6
        self.cycle_comments.append("Cycle {0:<6d} Port {1:<6} {2:<{3}}: {4}".format(len(self.cycle_times),
                                                                                    port,
                                                                                    time,
                                                                                    time_spacing,
                                                                                    comment))

    def combine_word(self, spare, word):
        if len(spare) > 0:
            return spare + "+" + word

        return word

    def format_value(self, value):
        """ Format in better readable manner """

        def delineate(word):
            # Create list of chars in reverse order
            split_word = list(reversed([x for x in word]))
            # Add underscore every 4th char
            split_word2 = [x + '_' * (n != 0 and n % 4 == 0) for n, x in enumerate(split_word)]
            # Join the word unreversed back together
            new_word = ''.join(reversed(split_word2))
            return (new_word)

        # Split extra cols
        if self.num_spare_cols > 0:
            vals = value[self.num_spare_cols:]
            spare_vals = value[:self.num_spare_cols]
        else:
            vals = value
            spare_vals = ""

        # Insert underscores
        vals = delineate(vals)
        spare_vals = delineate(spare_vals)

        return self.combine_word(spare_vals, vals)

    def gen_cycle_comment(self, op, word, addr, wmask, port, t_current):
        if op == "noop":
            str = "\tIdle during cycle {0} ({1}ns - {2}ns)"
            comment = str.format(int(t_current / self.period),
                                 t_current,
                                 t_current + self.period)
        elif op == "write":
            comment = "\tWriting {0}  to  address {1} (from port {2}) during cycle {3} ({4}ns - {5}ns)".format(word,
                                                                                                               addr,
                                                                                                               port,
                                                                                                               int(t_current / self.period),
                                                                                                               t_current,
                                                                                                               t_current + self.period)
        elif op == "partial_write":
            str = "\tWriting (partial) {0}  to  address {1} with mask bit {2} (from port {3}) during cycle {4} ({5}ns - {6}ns)"
            comment = str.format(word,
                                 addr,
                                 wmask,
                                 port,
                                 int(t_current / self.period),
                                 t_current,
                                 t_current + self.period)
        else:
            str = "\tReading {0} from address {1} (from port {2}) during cycle {3} ({4}ns - {5}ns)"
            comment = str.format(word,
                                 addr,
                                 port,
                                 int(t_current / self.period),
                                 t_current,
                                 t_current + self.period)

        return comment

    def gen_pin_names(self, port_signal_names, port_info, abits, dbits):
        """Creates the pins names of the SRAM based on the no. of ports."""
        # This may seem redundant as the pin names are already defined in the sram. However, it is difficult
        # to extract the functionality from the names, so they are recreated. As the order is static, changing
        # the order of the pin names will cause issues here.
        pin_names = []
        (addr_name, din_name, dout_name) = port_signal_names
        (total_ports, write_index, read_index) = port_info

        for write_input in write_index:
            for i in range(dbits):
                pin_names.append("{0}{1}_{2}".format(din_name, write_input, i))

        for port in range(total_ports):
            for i in range(abits):
                pin_names.append("{0}{1}_{2}".format(addr_name, port, i))

        # Control signals not finalized.
        for port in range(total_ports):
            pin_names.append("CSB{0}".format(port))
        for port in range(total_ports):
            if (port in read_index) and (port in write_index):
                pin_names.append("WEB{0}".format(port))

        for port in range(total_ports):
            pin_names.append("{0}{1}".format("clk", port))

        if self.write_size != self.word_size:
            for port in write_index:
                for bit in range(self.num_wmasks):
                    pin_names.append("WMASK{0}_{1}".format(port, bit))

        if self.num_spare_cols:
            for port in write_index:
                for bit in range(self.num_spare_cols):
                    pin_names.append("SPARE_WEN{0}_{1}".format(port, bit))

        for read_output in read_index:
            for i in range(dbits):
                pin_names.append("{0}{1}_{2}".format(dout_name, read_output, i))

        pin_names.append("{0}".format("vdd"))
        pin_names.append("{0}".format("gnd"))
        return pin_names

    def get_column_addr(self):
        """Returns column address of probe bit"""
        return self.probe_address[:self.sram.col_addr_size]

    def add_graph_exclusions(self):
        """
        Exclude portions of SRAM from timing graph which are not relevant
        """

        # other initializations can only be done during analysis when a bit has been selected
        # for testing.
        if OPTS.top_process != 'memchar':
            self.sram.bank.graph_exclude_precharge()
            self.sram.graph_exclude_addr_dff()
            self.sram.graph_exclude_data_dff()
            self.sram.graph_exclude_ctrl_dffs()
            self.sram.bank.bitcell_array.graph_exclude_replica_col_bits()

    def set_internal_spice_names(self):
        """
        Sets important names for characterization such as Sense amp enable and internal bit nets.
        """

        port = self.read_ports[0]
        if not OPTS.use_pex or (OPTS.use_pex and OPTS.pex_exe[0] == "calibre"):
            self.graph.get_all_paths('{}{}'.format("clk", port),
                                     '{}{}_{}'.format(self.dout_name, port, self.probe_data))
            sen_with_port = self.get_sen_name(self.graph.all_paths)
            if sen_with_port.endswith(str(port)):
                self.sen_name = sen_with_port[:-len(str(port))]
            else:
                self.sen_name = sen_with_port
                debug.warning("Error occurred while determining SEN name. Can cause faults in simulation.")

            # column_addr = self.get_column_addr()
            bl_name_port, br_name_port = self.get_bl_name(self.graph.all_paths, port)
            # port_pos = -1 - len(str(column_addr)) - len(str(port))

            if bl_name_port.endswith(str(port) + "_" + str(self.bitline_column)): # single port SRAM case, bl will not be numbered eg bl_0
                self.bl_name = bl_name_port
            else:
                self.bl_name = bl_name_port
                debug.warning("Error occurred while determining bitline names. Can cause faults in simulation.")

            if br_name_port.endswith(str(port) + "_" + str(self.bitline_column)): # single port SRAM case, bl will not be numbered eg bl_0
                self.br_name = br_name_port
            else:
                self.br_name = br_name_port
                debug.warning("Error occurred while determining bitline names. Can cause faults in simulation.")
        else:
            self.graph.get_all_paths('{}{}'.format("clk", port),
                                     '{}{}_{}'.format(self.dout_name, port, self.probe_data))

            self.sen_name = self.get_sen_name(self.graph.all_paths)
            # debug.info(2, "s_en {}".format(self.sen_name))

            self.bl_name = "bl{0}_{1}".format(port, OPTS.word_size - 1)
            self.br_name = "br{0}_{1}".format(port, OPTS.word_size - 1)
            # debug.info(2, "bl name={0}".format(self.bl_name))
            # debug.info(2, "br name={0}".format(self.br_name))

    def get_sen_name(self, paths, assumed_port=None):
        """
        Gets the signal name associated with the sense amp enable from input paths.
        Only expects a single path to contain the sen signal name.
        """

        sa_mods = factory.get_mods(OPTS.sense_amp)
        # Any sense amp instantiated should be identical, any change to that
        # will require some identification to determine the mod desired.
        debug.check(len(sa_mods) == 1, "Only expected one type of Sense Amp. Cannot perform s_en checks.")
        enable_name = sa_mods[0].get_enable_name()
        sen_name = self.get_alias_in_path(paths, enable_name, sa_mods[0])
        if OPTS.use_pex and OPTS.pex_exe[0] != "calibre":
            sen_name = sen_name.split('.')[-1]
        return sen_name

    def create_graph(self):
        """
        Creates timing graph to generate the timing paths for the SRAM output.
        """

        # Make exclusions dependent on the bit being tested.
        self.sram.clear_exclude_bits() # Removes previous bit exclusions
        self.sram.graph_exclude_bits(self.wordline_row, self.bitline_column)
        port=self.read_ports[0] # FIXME, port_data requires a port specification, assuming single port for now
        if self.words_per_row > 1:
            self.sram.graph_clear_column_mux(port)
            self.sram.graph_exclude_column_mux(self.bitline_column, port)

        # Generate new graph every analysis as edges might change depending on test bit
        self.graph = timing_graph()
        self.sram_instance_name = "X{}".format(self.sram.name)
        self.sram.build_graph(self.graph, self.sram_instance_name, self.pins)

    def get_bl_name_search_exclusions(self):
        """
        Gets the mods as a set which should be excluded while searching for name.
        """

        # Exclude the RBL as it contains bitcells which are not in the main bitcell array
        # so it makes the search awkward
        return set(factory.get_mods(OPTS.replica_bitline))

    def get_alias_in_path(self, paths, internal_net, mod, exclusion_set=None):
        """
        Finds a single alias for the internal_net in given paths.
        More or less hits cause an error
        """
        net_found = False
        for path in paths:
            aliases = self.sram.find_aliases(self.sram_instance_name, self.pins, path, internal_net, mod, exclusion_set)
            if net_found and len(aliases) >= 1:
                pass #debug.error('Found multiple paths with {} net.'.format(internal_net), 1)
            elif len(aliases) > 1:
                debug.error('Found multiple {} nets in single path.'.format(internal_net), 1)
            elif not net_found and len(aliases) == 1:
                path_net_name = aliases[0]
                net_found = True
        if not net_found:
            debug.error("Could not find {} net in timing paths.".format(internal_net), 1)

        return path_net_name

    def get_bl_name(self, paths, port):
        """
        Gets the signal name associated with the bitlines in the bank.
        """
        # FIXME: change to a solution that does not depend on the technology
        if OPTS.tech_name == "sky130" and len(self.all_ports) == 1:
            cell_mod = factory.create(module_type=OPTS.bitcell, version="opt1")
        else:
            cell_mod = factory.create(module_type=OPTS.bitcell)
        cell_bl = cell_mod.get_bl_name(port)
        cell_br = cell_mod.get_br_name(port)

        bl_names = []
        exclude_set = self.get_bl_name_search_exclusions()
        for int_net in [cell_bl, cell_br]:
            bl_names.append(self.get_alias_in_path(paths, int_net, cell_mod, exclude_set))
        if OPTS.use_pex and OPTS.pex_exe[0] != "calibre":
            for i in range(len(bl_names)):
                bl_names[i] = bl_names[i].split(OPTS.hier_seperator)[-1]
        return bl_names[0], bl_names[1]

    def get_empty_measure_data_dict(self):
        """Make a dict of lists for each type of delay and power measurement to append results to"""

        measure_names = self.delay_meas_names + self.power_meas_names
        # Create list of dicts. List lengths is # of ports. Each dict maps the measurement names to lists.
        measure_data = [{mname: [] for mname in measure_names} for i in self.all_ports]
        return measure_data

    def sum_delays(self, delays):
        """Adds the delays (delay_data objects) so the correct slew is maintained"""

        delay = delays[0]
        for i in range(1, len(delays)):
            delay+=delays[i]
        return delay
