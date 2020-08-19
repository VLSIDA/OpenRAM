# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import collections
import debug
import random
from .stimuli import *
from .charutils import *
from globals import OPTS
from .simulation import simulation
# from .delay import delay
import graph_util
from sram_factory import factory


class functional(simulation):
    """
       Functions to write random data values to a random address then read them back and check
       for successful SRAM operation.
    """

    def __init__(self, sram, spfile, corner):
        super().__init__(sram, spfile, corner)
        
        # Seed the characterizer with a constant seed for unit tests
        if OPTS.is_unit_test:
            random.seed(12345)

        if self.write_size:
            self.num_wmasks = int(self.word_size / self.write_size)
        else:
            self.num_wmasks = 0

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        self.set_corner(corner)
        self.set_spice_constants()
        self.set_stimulus_variables()

        # For the debug signal names
        self.create_signal_names()
        self.add_graph_exclusions()
        self.create_graph()
        self.set_internal_spice_names()
        
        # Number of checks can be changed
        self.num_cycles = 15
        # This is to have ordered keys for random selection
        self.stored_words = collections.OrderedDict()
        self.read_check = []
        self.read_results = []

    def run(self, feasible_period=None):
        if feasible_period: #period defaults to tech.py feasible period otherwise.
            self.period = feasible_period
        # Generate a random sequence of reads and writes
        self.create_random_memory_sequence()
    
        # Run SPICE simulation
        self.write_functional_stimulus()
        self.stim.run_sim()
        
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
        if self.write_size:
            rw_ops = ["noop", "write", "partial_write", "read"]
            w_ops = ["noop", "write", "partial_write"]
        else:
            rw_ops = ["noop", "write", "read"]
            w_ops = ["noop", "write"]
        r_ops = ["noop", "read"]

        # First cycle idle is always an idle cycle
        comment = self.gen_cycle_comment("noop", "0" * self.word_size, "0" * self.addr_size, "0" * self.num_wmasks, 0, self.t_current)
        self.add_noop_all_ports(comment)

        # 1. Write all the write ports first to seed a bunch of locations.
        for port in self.write_ports:
            addr = self.gen_addr()
            word = self.gen_data()
            comment = self.gen_cycle_comment("write", word, addr, "1" * self.num_wmasks, port, self.t_current)
            self.add_write_one_port(comment, addr, word, "1" * self.num_wmasks, port)
            self.stored_words[addr] = word

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
            if port in self.write_ports:
                self.add_noop_one_port(port)
            else:
                comment = self.gen_cycle_comment("read", word, addr, "0" * self.num_wmasks, port, self.t_current)
                self.add_read_one_port(comment, addr, port)
                self.add_read_check(word, port)
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
                        word = self.gen_data()
                        comment = self.gen_cycle_comment("write", word, addr, "1" * self.num_wmasks, port, self.t_current)
                        self.add_write_one_port(comment, addr, word, "1" * self.num_wmasks, port)
                        self.stored_words[addr] = word
                        w_addrs.append(addr)
                elif op == "partial_write":
                    # write only to a word that's been written to
                    (addr, old_word) = self.get_data()
                    # two ports cannot write to the same address
                    if addr in w_addrs:
                        self.add_noop_one_port(port)
                    else:
                        word = self.gen_data()
                        wmask  = self.gen_wmask()
                        new_word = self.gen_masked_data(old_word, word, wmask)
                        comment = self.gen_cycle_comment("partial_write", word, addr, wmask, port, self.t_current)
                        self.add_write_one_port(comment, addr, word, wmask, port)
                        self.stored_words[addr] = new_word
                        w_addrs.append(addr)
                else:
                    (addr, word) = random.choice(list(self.stored_words.items()))
                    # The write driver is not sized sufficiently to drive through the two
                    # bitcell access transistors to the read port. So, for now, we do not allow
                    # a simultaneous write and read to the same address on different ports. This
                    # could be even more difficult with multiple simultaneous read ports.
                    if addr in w_addrs:
                        self.add_noop_one_port(port)
                    else:
                        comment = self.gen_cycle_comment("read", word, addr, "0" * self.num_wmasks, port, self.t_current)
                        self.add_read_one_port(comment, addr, port)
                        self.add_read_check(word, port)
                
            self.cycle_times.append(self.t_current)
            self.t_current += self.period
        
        # Last cycle idle needed to correctly measure the value on the second to last clock edge
        comment = self.gen_cycle_comment("noop", "0" * self.word_size, "0" * self.addr_size, "0" * self.num_wmasks, 0, self.t_current)
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
        try:
            self.check
        except:
            self.check = 0
        self.read_check.append([word, "{0}{1}".format(self.dout_name, port), self.t_current + self.period, self.check])
        self.check += 1
        
    def read_stim_results(self):
        # Extract dout values from spice timing.lis
        for (word, dout_port, eo_period, check) in self.read_check:
            sp_read_value = ""
            for bit in range(self.word_size + self.num_spare_cols):
                value = parse_spice_list("timing", "v{0}.{1}ck{2}".format(dout_port.lower(), bit, check))
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
                    return (0, error)
                    
            self.read_results.append([sp_read_value, dout_port, eo_period, check])                    
        return (1, "SUCCESS")
        
    def check_stim_results(self):
        for i in range(len(self.read_check)):
            if self.read_check[i][0] != self.read_results[i][0]:
                error = "FAILED: {0} value {1} does not match written value {2} read during cycle {3} at time {4}n".format(self.read_results[i][1],
                                                                                                                           self.read_results[i][0],
                                                                                                                           self.read_check[i][0],
                                                                                                                           int((self.read_results[i][2]-self.period)/self.period),
                                                                                                                           self.read_results[i][2])
                return(0, error)
        return(1, "SUCCESS")

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
        if not self.num_spare_cols:
            random_value = random.randint(0, (2 ** self.word_size) - 1)
        else:
            random_value1 = random.randint(0, (2 ** self.word_size) - 1)
            random_value2 = random.randint(0, (2 ** self.num_spare_cols) - 1)
            random_value = random_value1 + random_value2
        data_bits = self.convert_to_bin(random_value, False)
        return data_bits

    def gen_addr(self):
        """ Generates a random address value to write to. """
        if self.num_spare_rows==0:
            random_value = random.randint(0, (2 ** self.addr_size) - 1)
        else:
            random_value = random.randint(0, ((2 ** (self.addr_size - 1) - 1)) + (self.num_spare_rows * self.words_per_row))
        addr_bits = self.convert_to_bin(random_value, True)
        return addr_bits
        
    def get_data(self):
        """ Gets an available address and corresponding word. """
        # Used for write masks since they should be writing to previously written addresses
        addr = random.choice(list(self.stored_words.keys()))
        word = self.stored_words[addr]
        return (addr, word)
        
    def convert_to_bin(self, value, is_addr):
        """ Converts addr & word to usable binary values. """
        new_value = str.replace(bin(value), "0b", "")
        if(is_addr):
            expected_value = self.addr_size
        else:
            expected_value = self.word_size + self.num_spare_cols
        for i in range(expected_value - len(new_value)):
            new_value =  "0" + new_value
            
        # print("Binary Conversion: {} to {}".format(value, new_value))
        return new_value
            
    def write_functional_stimulus(self):
        """ Writes SPICE stimulus. """
        temp_stim = "{0}/stim.sp".format(OPTS.openram_temp)
        self.sf = open(temp_stim, "w")
        self.sf.write("* Functional test stimulus file for {}ns period\n\n".format(self.period))
        self.stim = stimuli(self.sf, self.corner)

        # Write include statements
        self.stim.write_include(self.sp_file)

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
        self.sf.write("* bl: {}\n".format(self.bl_name))
        self.sf.write("* br: {}\n".format(self.br_name))
        self.sf.write("* s_en: {}\n".format(self.sen_name))
        self.sf.write("* q: {}\n".format(self.q_name))
        self.sf.write("* qbar: {}\n".format(self.qbar_name))
                
        # Write debug comments to stim file
        self.sf.write("\n\n* Sequence of operations\n")
        for comment in self.fn_cycle_comments:
            self.sf.write("*{}\n".format(comment))
                
        # Generate data input bits
        self.sf.write("\n* Generation of data and address signals\n")
        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                sig_name="{0}{1}_{2} ".format(self.din_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.data_values[port][bit], self.period, self.slew, 0.05)
        
        # Generate address bits
        for port in self.all_ports:
            for bit in range(self.addr_size):
                sig_name="{0}{1}_{2} ".format(self.addr_name, port, bit)
                self.stim.gen_pwl(sig_name, self.cycle_times, self.addr_values[port][bit], self.period, self.slew, 0.05)

        # Generate control signals
        self.sf.write("\n * Generation of control signals\n")
        for port in self.all_ports:
            self.stim.gen_pwl("CSB{}".format(port), self.cycle_times, self.csb_values[port], self.period, self.slew, 0.05)
            
        for port in self.readwrite_ports:
            self.stim.gen_pwl("WEB{}".format(port), self.cycle_times, self.web_values[port], self.period, self.slew, 0.05)

        # Generate wmask bits
        for port in self.write_ports:
            if self.write_size:
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
                                offset=self.period,
                                period=self.period,
                                t_rise=self.slew,
                                t_fall=self.slew)
        
        # Generate dout value measurements
        self.sf.write("\n * Generation of dout measurements\n")
        for (word, dout_port, eo_period, check) in self.read_check:
            t_intital = eo_period - 0.01 * self.period
            t_final = eo_period + 0.01 * self.period
            for bit in range(self.word_size + self.num_spare_cols):
                self.stim.gen_meas_value(meas_name="V{0}_{1}ck{2}".format(dout_port, bit, check),
                                         dout="{0}_{1}".format(dout_port, bit),
                                         t_intital=t_intital,
                                         t_final=t_final)
        
        self.stim.write_control(self.cycle_times[-1] + self.period)
        self.sf.close()

    # FIXME: refactor to share with delay.py
    def add_graph_exclusions(self):
        """Exclude portions of SRAM from timing graph which are not relevant"""
        
        # other initializations can only be done during analysis when a bit has been selected
        # for testing.
        self.sram.bank.graph_exclude_precharge()
        self.sram.graph_exclude_addr_dff()
        self.sram.graph_exclude_data_dff()
        self.sram.graph_exclude_ctrl_dffs()
        self.sram.bank.bitcell_array.graph_exclude_replica_col_bits()
        
    # FIXME: refactor to share with delay.py
    def create_graph(self):
        """Creates timing graph to generate the timing paths for the SRAM output."""
        
        self.sram.bank.bitcell_array.init_graph_params() # Removes previous bit exclusions
        # Does wordline=0 and column=0 just for debug names
        self.sram.bank.bitcell_array.graph_exclude_bits(0, 0)
        
        # Generate new graph every analysis as edges might change depending on test bit
        self.graph = graph_util.timing_graph()
        self.sram_spc_name = "X{}".format(self.sram.name)
        self.sram.build_graph(self.graph, self.sram_spc_name, self.pins)

    # FIXME: refactor to share with delay.py
    def set_internal_spice_names(self):
        """Sets important names for characterization such as Sense amp enable and internal bit nets."""
        
        # For now, only testing these using first read port.
        port = self.read_ports[0]
        self.graph.get_all_paths('{}{}'.format("clk", port),
                                 '{}{}_{}'.format(self.dout_name, port, 0).lower())

        self.sen_name = self.get_sen_name(self.graph.all_paths)
        debug.info(2, "s_en name = {}".format(self.sen_name))
        
        self.bl_name, self.br_name = self.get_bl_name(self.graph.all_paths, port)
        debug.info(2, "bl name={}, br name={}".format(self.bl_name, self.br_name))

        self.q_name, self.qbar_name = self.get_bit_name()
        debug.info(2, "q name={}\nqbar name={}".format(self.q_name, self.qbar_name))
        
    def get_bit_name(self):
        """ Get a bit cell name """
        (cell_name, cell_inst) = self.sram.get_cell_name(self.sram.name, 0, 0)
        storage_names = cell_inst.mod.get_storage_net_names()
        debug.check(len(storage_names) == 2, ("Only inverting/non-inverting storage nodes"
                                              "supported for characterization. Storage nets={}").format(storage_names))
        q_name = cell_name + '.' + str(storage_names[0])
        qbar_name = cell_name + '.' + str(storage_names[1])

        return (q_name, qbar_name)
        
    # FIXME: refactor to share with delay.py
    def get_sen_name(self, paths):
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
        return sen_name
     
    # FIXME: refactor to share with delay.py
    def get_bl_name(self, paths, port):
        """Gets the signal name associated with the bitlines in the bank."""
        
        cell_mod = factory.create(module_type=OPTS.bitcell)
        cell_bl = cell_mod.get_bl_name(port)
        cell_br = cell_mod.get_br_name(port)
        
        # Only a single path should contain a single s_en name. Anything else is an error.
        bl_names = []
        exclude_set = self.get_bl_name_search_exclusions()
        for int_net in [cell_bl, cell_br]:
            bl_names.append(self.get_alias_in_path(paths, int_net, cell_mod, exclude_set))
                
        return bl_names[0], bl_names[1]

    def get_bl_name_search_exclusions(self):
        """Gets the mods as a set which should be excluded while searching for name."""
        
        # Exclude the RBL as it contains bitcells which are not in the main bitcell array
        # so it makes the search awkward
        return set(factory.get_mods(OPTS.replica_bitline))
        
    def get_alias_in_path(self, paths, int_net, mod, exclusion_set=None):
        """
        Finds a single alias for the int_net in given paths.
        More or less hits cause an error
        """
        
        net_found = False
        for path in paths:
            aliases = self.sram.find_aliases(self.sram_spc_name, self.pins, path, int_net, mod, exclusion_set)
            if net_found and len(aliases) >= 1:
                debug.error('Found multiple paths with {} net.'.format(int_net), 1)
            elif len(aliases) > 1:
                debug.error('Found multiple {} nets in single path.'.format(int_net), 1)
            elif not net_found and len(aliases) == 1:
                path_net_name = aliases[0]
                net_found = True
        if not net_found:
            debug.error("Could not find {} net in timing paths.".format(int_net), 1)
                
        return path_net_name
    
