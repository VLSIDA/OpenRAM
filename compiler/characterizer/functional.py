# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
import random
import collections
from os import path
import shutil
from numpy import binary_repr
from openram import debug
from openram import OPTS
from .stimuli import *
from .charutils import *
from .simulation import simulation
from .measurements import voltage_at_measure


class functional(simulation):
    """
       Functions to write random data values to a random address then read them back and check
       for successful SRAM operation.
    """

    def __init__(self, sram, spfile=None, corner=None, cycles=15, period=None, output_path=None):
        super().__init__(sram, spfile, corner)

        # Seed the characterizer with a constant seed for unit tests
        if OPTS.is_unit_test:
            random.seed(12345)

        if not spfile:
            # self.sp_file is assigned in base class
            sram.sp_write(self.sp_file, trim=OPTS.trim_netlist)
        # Copy sp file to temp dir
        self.temp_spice = path.join(OPTS.openram_temp, "sram.sp")
        shutil.copy(self.sp_file, self.temp_spice)

        if not corner:
            corner = (OPTS.process_corners[0], OPTS.supply_voltages[0], OPTS.temperatures[0])

        if not output_path:
            self.output_path = OPTS.openram_temp
        else:
            self.output_path = output_path

        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        self.max_data = 2 ** self.word_size - 1
        self.max_col_data = 2 ** self.num_spare_cols - 1
        if self.words_per_row > 1:
            # This will truncate bits for word addressing in a row_addr_dff
            # This makes one set of spares per row by using top bits of the address
            self.addr_spare_index = -int(math.log(self.words_per_row) / math.log(2))
        else:
            # This will select the entire address when one word per row
            self.addr_spare_index = self.bank_addr_size
        # If trim is set, specify the valid addresses
        self.valid_addresses = set()
        self.max_address = self.num_rows * self.words_per_row - 1
        if OPTS.trim_netlist:
            for i in range(self.words_per_row):
                self.valid_addresses.add(i)
                self.valid_addresses.add(self.max_address - i - 1)
        self.probe_address, self.probe_data = '0' * self.bank_addr_size, 0
        self.set_corner(corner)
        self.set_spice_constants()
        self.set_stimulus_variables()

        # Override default period
        if period:
            self.period = period

        # For the debug signal names
        self.wordline_row = 0
        self.bitline_column = 0
        self.create_signal_names()
        #self.add_graph_exclusions()
        #self.create_graph()
        #self.set_internal_spice_names()
        self.bl_name = "xsram:xbank0:bl_0_{}"
        self.br_name = "xsram:xbank0:br_0_{}"
        self.sen_name = "xsram:s_en"
        self.q_name, self.qbar_name = self.get_bit_name()
        debug.info(2, "q:\t\t{0}".format(self.q_name))
        debug.info(2, "qbar:\t{0}".format(self.qbar_name))
        debug.info(2, "s_en:\t{0}".format(self.sen_name))
        debug.info(2, "bl:\t{0}".format(self.bl_name))
        debug.info(2, "br:\t{0}".format(self.br_name))

        # Number of checks can be changed
        self.num_cycles = cycles
        # This is to have ordered keys for random selection
        self.stored_words = collections.OrderedDict()
        self.stored_spares = collections.OrderedDict()
        self.read_check = []
        self.read_results = []

        # Generate a random sequence of reads and writes
        self.create_random_memory_sequence()

        # Write SPICE simulation
        self.write_functional_stimulus()

    def run(self):
        self.stim.run_sim(self.stim_sp)

        # read dout values from SPICE simulation. If the values do not fall within the noise margins, return the error.
        (success, error) = self.read_stim_results()
        if not success:
            return (0, error)

        # Check read values with written values. If the values do not match, return an error.
        return self.check_stim_results()

    def check_lengths(self):
        """ Do a bunch of assertions. """

        for port in self.all_ports:
            checks = []
            if port in self.read_ports:
                checks.append((self.addr_value[port], "addr"))
            if port in self.write_ports:
                checks.append((self.data_value[port], "data"))
                checks.append((self.wmask_value[port], "wmask"))
                checks.append((self.spare_wen_value[port], "spare_wen"))

            for (val, name) in checks:
                debug.check(len(self.cycle_times)==len(val),
                            "Port {2} lengths don't match. {0} clock values, {1} {3} values".format(len(self.cycle_times),
                                                                                                    len(val),
                                                                                                    port,
                                                                                                    name))

    def create_random_memory_sequence(self):
        # Select randomly, but have 3x more reads to increase probability
        if self.write_size != self.word_size:
            rw_ops = ["noop", "write", "partial_write", "read", "read"]
            w_ops = ["noop", "write", "partial_write"]
        else:
            rw_ops = ["noop", "write", "read", "read"]
            w_ops = ["noop", "write"]
        r_ops = ["noop", "read"]

        # First cycle idle is always an idle cycle
        comment = self.gen_cycle_comment("noop", "0" * self.word_size, "0" * self.bank_addr_size, "0" * self.num_wmasks, 0, self.t_current)
        self.add_noop_all_ports(comment)

        # 1. Write all the write ports 2x to seed a bunch of locations.
        for i in range(3):
            for port in self.write_ports:
                addr = self.gen_addr()
                (word, spare) = self.gen_data()
                combined_word = self.combine_word(spare, word)
                comment = self.gen_cycle_comment("write", combined_word, addr, "1" * self.num_wmasks, port, self.t_current)
                self.add_write_one_port(comment, addr, spare + word, "1" * self.num_wmasks, port)
                self.stored_words[addr] = word
                self.stored_spares[addr[:self.addr_spare_index]] = spare

            # All other read-only ports are noops.
            for port in self.read_ports:
                if port not in self.write_ports:
                    self.add_noop_one_port(port)
            self.cycle_times.append(self.t_current)
            self.t_current += self.period
            self.check_lengths()

        # 2. Read at least once.  For multiport, it is important that one
        # read cycle uses all RW and R port to read from the same
        # address simultaniously.  This will test the viablilty of the
        # transistor sizing in the bitcell.
        for port in self.all_ports:
            if port in self.write_ports and port not in self.read_ports:
                self.add_noop_one_port(port)
            else:
                (addr, word, spare) = self.get_data()
                combined_word = self.combine_word(spare, word)
                comment = self.gen_cycle_comment("read", combined_word, addr, "0" * self.num_wmasks, port, self.t_current)
                self.add_read_one_port(comment, addr, port)
                self.add_read_check(spare + word, port)
        self.cycle_times.append(self.t_current)
        self.t_current += self.period
        self.check_lengths()

        # 3. Perform a random sequence of writes and reads on random
        # ports, using random addresses and random words and random
        # write masks (if applicable)
        for i in range(self.num_cycles):
            w_addrs = []
            for port in self.all_ports:
                if port in self.readwrite_ports:
                    op = random.choice(rw_ops)
                elif port in self.write_ports:
                    op = random.choice(w_ops)
                else:
                    op = random.choice(r_ops)

                if op == "noop":
                    self.add_noop_one_port(port)
                elif op == "write":
                    addr = self.gen_addr()
                    # two ports cannot write to the same address
                    if addr in w_addrs:
                        self.add_noop_one_port(port)
                    else:
                        (word, spare) = self.gen_data()
                        combined_word = self.combine_word(spare, word)
                        comment = self.gen_cycle_comment("write", combined_word, addr, "1" * self.num_wmasks, port, self.t_current)
                        self.add_write_one_port(comment, addr, spare + word, "1" * self.num_wmasks, port)
                        self.stored_words[addr] = word
                        self.stored_spares[addr[:self.addr_spare_index]] = spare
                        w_addrs.append(addr)
                elif op == "partial_write":
                    # write only to a word that's been written to
                    (addr, old_word, old_spare) = self.get_data()
                    # two ports cannot write to the same address
                    if addr in w_addrs:
                        self.add_noop_one_port(port)
                    else:
                        (word, spare) = self.gen_data()
                        wmask  = self.gen_wmask()
                        new_word = self.gen_masked_data(old_word, word, wmask)
                        combined_word = self.combine_word(spare, word)
                        comment = self.gen_cycle_comment("partial_write", combined_word, addr, wmask, port, self.t_current)
                        self.add_write_one_port(comment, addr, spare + word, wmask, port)
                        self.stored_words[addr] = new_word
                        self.stored_spares[addr[:self.addr_spare_index]] = spare
                        w_addrs.append(addr)
                else:
                    (addr, word) = random.choice(list(self.stored_words.items()))
                    spare = self.stored_spares[addr[:self.addr_spare_index]]
                    combined_word = self.combine_word(spare, word)
                    # The write driver is not sized sufficiently to drive through the two
                    # bitcell access transistors to the read port. So, for now, we do not allow
                    # a simultaneous write and read to the same address on different ports. This
                    # could be even more difficult with multiple simultaneous read ports.
                    if addr in w_addrs:
                        self.add_noop_one_port(port)
                    else:
                        comment = self.gen_cycle_comment("read", combined_word, addr, "0" * self.num_wmasks, port, self.t_current)
                        self.add_read_one_port(comment, addr, port)
                        self.add_read_check(spare + word, port)
            self.cycle_times.append(self.t_current)
            self.t_current += self.period

        # Last cycle idle needed to correctly measure the value on the second to last clock edge
        comment = self.gen_cycle_comment("noop", "0" * self.word_size, "0" * self.bank_addr_size, "0" * self.num_wmasks, 0, self.t_current)
        self.add_noop_all_ports(comment)

    def gen_masked_data(self, old_word, word, wmask):
        """ Create the masked data word """
        # Start with the new word
        new_word = word

        # When the write mask's bits are 0, the old data values should appear in the new word
        # as to not overwrite the old values
        for bit in range(len(wmask)):
            if wmask[bit] == "0":
                lower = bit * self.write_size
                upper = lower + self.write_size - 1
                new_word = new_word[:lower] + old_word[lower:upper + 1] + new_word[upper + 1:]

        return new_word

    def add_read_check(self, word, port):
        """ Add to the check array to ensure a read works. """
        self.read_check.append([word,
                                "{0}{1}".format(self.dout_name, port),
                                self.t_current + self.period,
                                int(self.t_current / self.period)])

    def read_stim_results(self):
        # Extract dout values from spice timing.lis
        for (word, dout_port, eo_period, cycle) in self.read_check:
            sp_read_value = ""
            for bit in range(self.word_size + self.num_spare_cols):
                measure_name = "v{0}_{1}ck{2}".format(dout_port.lower(), bit, cycle)
                # value = parse_spice_list("timing", measure_name)
                value = self.measures[measure_name].retrieve_measure(port=0)
                # FIXME: Ignore the spare columns for now
                if bit >= self.word_size:
                    value = 0

                try:
                    value = float(value)
                    if value > self.v_high:
                        sp_read_value = "1" + sp_read_value
                    elif value < self.v_low:
                        sp_read_value = "0" + sp_read_value
                    else:
                        error ="FAILED: {0}_{1} value {2} at time {3}n does not fall within noise margins <{4} or >{5}.".format(dout_port,
                                                                                                                                bit,
                                                                                                                                value,
                                                                                                                                eo_period,
                                                                                                                                self.v_low,
                                                                                                                                self.v_high)
                except ValueError:
                    error ="FAILED: {0}_{1} value {2} at time {3}n is not a float. Measure: {4}".format(dout_port,
                                                                                           bit,
                                                                                           value,
                                                                                           eo_period,
                                                                                           measure_name)

                    return (0, error)
            self.read_results.append([sp_read_value, dout_port, eo_period, cycle])
        return (1, "SUCCESS")

    def check_stim_results(self):
        for i in range(len(self.read_check)):
            if self.read_check[i][0] != self.read_results[i][0]:
                output_name = self.read_check[i][1]
                cycle = self.read_check[i][3]
                read_val = self.format_value(self.read_results[i][0])
                correct_val = self.format_value(self.read_check[i][0])
                check_name = "v{0}_Xck{1}".format(output_name, cycle)
                str = "FAILED: {0} read value {1} during cycle {3} at time {4}n ({5}) does not match written value ({2})"
                error = str.format(output_name,
                                   read_val,
                                   correct_val,
                                   cycle,
                                   self.read_results[i][2],
                                   check_name)
                return (0, error)
        return (1, "SUCCESS")

    def gen_wmask(self):
        wmask = ""
        # generate a random wmask
        for bit in range(self.num_wmasks):
            rand = random.randint(0, 1)
            wmask += str(rand)
        # prevent the wmask from having all bits on or off (this is not a partial write)
        all_zeroes = True
        all_ones = True
        for bit in range(self.num_wmasks):
            if wmask[bit]=="0":
                all_ones = False
            elif wmask[bit]=="1":
                all_zeroes = False
        if all_zeroes:
            index = random.randint(0, self.num_wmasks - 1)
            wmask = wmask[:index] + "1" + wmask[index + 1:]
        elif all_ones:
            index = random.randint(0, self.num_wmasks - 1)
            wmask = wmask[:index] + "0" + wmask[index + 1:]
        # wmask must be reversed since a python list goes right to left and sram bits go left to right.
        return wmask[::-1]

    def gen_data(self):
        """ Generates a random word to write. """
        # Don't use 0 or max value
        random_value = random.randint(1, self.max_data)
        data_bits = binary_repr(random_value, self.word_size)
        if self.num_spare_cols>0:
            random_value = random.randint(0, self.max_col_data)
            spare_bits = binary_repr(random_value, self.num_spare_cols)
        else:
            spare_bits = ""

        # FIXME: Set these to 0 for now...
        spare_bits = "0" * len(spare_bits)

        return data_bits, spare_bits

    def gen_addr(self):
        """ Generates a random address value to write to. """
        if self.valid_addresses:
            random_value = random.sample(list(self.valid_addresses), 1)[0]
        else:
            random_value = random.randint(0, self.max_address)
        addr_bits = binary_repr(random_value, self.bank_addr_size)
        return addr_bits

    def get_data(self):
        """ Gets an available address and corresponding word. """
        # Used for write masks since they should be writing to previously written addresses
        addr = random.choice(list(self.stored_words.keys()))
        word = self.stored_words[addr]
        spare = self.stored_spares[addr[:self.addr_spare_index]]
        return (addr, word, spare)

    def write_functional_stimulus(self):
        """ Writes SPICE stimulus. """
        self.stim_sp = "functional_stim.sp"
        temp_stim = path.join(self.output_path, self.stim_sp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Functional test stimulus file for {0}ns period\n\n".format(self.period))
        self.meas_sp = "functional_meas.sp"
        temp_meas = path.join(self.output_path, self.meas_sp)
        self.mf = open(temp_meas, "w")
        self.stim = stimuli(self.sf, self.mf, self.corner)

        # Write include statements
        self.stim.write_include(self.temp_spice)

        # Write Vdd/Gnd statements
        self.sf.write("\n* Global Power Supplies\n")
        self.stim.write_supply()

        # Instantiate the SRAM
        self.sf.write("\n* Instantiation of the SRAM\n")
        self.stim.inst_model(pins=self.pins,
                             model_name=self.sram.name)

        # Add load capacitance to each of the read ports
        self.sf.write("\n* SRAM output loads\n")
        for port in self.read_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                sig_name="{0}{1}_{2} ".format(self.dout_name, port, bit)
                self.sf.write("CD{0}{1} {2} 0 {3}f\n".format(port, bit, sig_name, self.load))

        # Write important signals to stim file
        self.sf.write("\n\n* Important signals for debug\n")
        self.sf.write("* bl:\t{0}\n".format(self.bl_name.format(port)))
        self.sf.write("* br:\t{0}\n".format(self.br_name.format(port)))
        self.sf.write("* s_en:\t{0}\n".format(self.sen_name))
        self.sf.write("* q:\t{0}\n".format(self.q_name))
        self.sf.write("* qbar:\t{0}\n".format(self.qbar_name))

        # Write debug comments to stim file
        self.sf.write("\n\n* Sequence of operations\n")
        for comment in self.fn_cycle_comments:
            self.sf.write("*{0}\n".format(comment))

        # Generate data input bits
        self.sf.write("\n* Generation of data and address signals\n")
        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                sig_name="{0}{1}_{2} ".format(self.din_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[port][bit], self.period, self.slew, 0.05)

        # Generate address bits
        for port in self.all_ports:
            for bit in range(self.bank_addr_size):
                sig_name="{0}{1}_{2} ".format(self.addr_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][bit], self.period, self.slew, 0.05)

        # Generate control signals
        self.sf.write("\n * Generation of control signals\n")
        for port in self.all_ports:
            self.stim.gen_pwl("CSB{0}".format(port), self.cycle_times, self.csb_values[port], self.period, self.slew, 0.05)

        for port in self.readwrite_ports:
            self.stim.gen_pwl("WEB{0}".format(port), self.cycle_times, self.web_values[port], self.period, self.slew, 0.05)

        # Generate wmask bits
        for port in self.write_ports:
            if self.write_size != self.word_size:
                self.sf.write("\n* Generation of wmask signals\n")
                for bit in range(self.num_wmasks):
                    sig_name = "WMASK{0}_{1} ".format(port, bit)
                    # self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[port][bit], self.period,
                    #                   self.slew, 0.05)
                    self.stim.gen_pwl(sig_name, self.cycle_times, self.wmask_values[port][bit], self.period,
                                      self.slew, 0.05)

        # Generate spare enable bits (for spare cols)
        for port in self.write_ports:
            if self.num_spare_cols:
                self.sf.write("\n* Generation of spare enable signals\n")
                for bit in range(self.num_spare_cols):
                    sig_name = "SPARE_WEN{0}_{1} ".format(port, bit)
                    self.stim.gen_pwl(sig_name, self.cycle_times, self.spare_wen_values[port][bit], self.period,
                                      self.slew, 0.05)

        # Generate CLK signals
        for port in self.all_ports:
            self.stim.gen_pulse(sig_name="{0}{1}".format("clk", port),
                                v1=self.gnd_voltage,
                                v2=self.vdd_voltage,
                                offset=self.period - 0.5 * self.slew,
                                period=self.period,
                                t_rise=self.slew,
                                t_fall=self.slew)

        # Generate dout value measurements
        self.sf.write("\n * Generation of dout measurements\n")
        self.measures = {}

        for (word, dout_port, eo_period, cycle) in self.read_check:
            t_initial = eo_period
            t_final = eo_period + 0.01 * self.period
            num_bits = self.word_size + self.num_spare_cols
            for bit in range(num_bits):
                signal_name = "{0}_{1}".format(dout_port, bit)
                measure_name = "v{0}ck{1}".format(signal_name, cycle)
                voltage_value = self.stim.get_voltage(word[num_bits - bit - 1])

                self.stim.add_comment("* CHECK {0} {1} = {2} time = {3}".format(signal_name,
                                                                                measure_name,
                                                                                voltage_value,
                                                                                eo_period))
                # TODO: Convert to measurement statement instead of stimuli
                meas = voltage_at_measure(measure_name, signal_name)
                self.measures[measure_name] = meas
                meas.write_measure(self.stim, ((t_initial + t_final) / 2, 0))
                # self.stim.gen_meas_value(meas_name=measure_name,
                #                          dout=signal_name,
                #                          t_initial=t_initial,
                #                          t_final=t_final

        self.sf.write(".include {0}\n".format(temp_meas))
        self.stim.write_control(self.cycle_times[-1] + self.period)
        self.sf.close()
        self.mf.close()

    # FIXME: Similar function to delay.py, refactor this
    def get_bit_name(self):
        """ Get a bit cell name """
        # TODO: Find a way to get the cell_name and storage_names statically
        # (cell_name, cell_inst) = self.sram.get_cell_name(self.sram.name, 0, 0)
        # storage_names = cell_inst.mod.get_storage_net_names()
        # debug.check(len(storage_names) == 2, ("Only inverting/non-inverting storage nodes"
        #                                       "supported for characterization. Storage nets={0}").format(storage_names))
        cell_name = "xsram:xbank0:xbitcell_array:xbitcell_array:xbit_r0_c0"
        storage_names = ("Q", "Q_bar")
        q_name = cell_name + OPTS.hier_seperator + str(storage_names[0])
        qbar_name = cell_name + OPTS.hier_seperator + str(storage_names[1])

        return (q_name, qbar_name)
