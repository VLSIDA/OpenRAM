# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from math import log, sqrt, ceil
from openram import debug
from openram.sram_factory import factory
from openram import OPTS


class sram_config:
    """ This is a structure that is used to hold the SRAM configuration options. """

    def __init__(self, word_size, num_words, write_size=None, num_banks=1,
                 words_per_row=None, num_spare_rows=0, num_spare_cols=0):
        self.word_size = word_size
        self.num_words = num_words
        # Don't add a write mask if it is the same size as the data word
        self.write_size_init = write_size
        if write_size:
            self.write_size = write_size
        else:
            self.write_size = word_size
        self.num_banks = num_banks
        self.num_spare_rows = num_spare_rows
        self.num_spare_cols = num_spare_cols

        try:
            from openram.tech import array_row_multiple
            self.array_row_multiple = array_row_multiple
        except ImportError:
            self.array_row_multiple = 1
        try:
            from openram.tech import array_col_multiple
            self.array_col_multiple = array_col_multiple
        except ImportError:
            self.array_col_multiple = 1

        if not self.num_spare_cols:
            self.num_spare_cols = 0

        if not self.num_spare_rows:
            self.num_spare_rows = 0

        # This will get over-written when we determine the organization
        self.words_per_row = words_per_row

        self.compute_sizes()

    def __str__(self):
        """ override print function output """
        config_items = ["num_banks",
                        "word_size",
                        "num_words",
                        "words_per_row",
                        "write_size",
                        "num_spare_rows",
                        "num_spare_cols"]
        str = ""
        for item in config_items:
            val = getattr(self, item)
            str += "{} : {}\n".format(item, val)
        return str

    def set_local_config(self, module):
        """ Copy all of the member variables to the given module for convenience """

        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        # Copy all the variables to the local module
        for member in members:
            setattr(module, member, getattr(self, member))

    def compute_sizes(self):
        """  Computes the organization of the memory using bitcell size by trying to make it square."""

        bitcell = factory.create(module_type=OPTS.bitcell)

        debug.check(ceil(log(self.num_banks, 2)) == log(self.num_banks, 2) ,
                    "Number of banks should be power of 2.")

        self.num_words_per_bank = self.num_words / self.num_banks
        self.num_bits_per_bank = self.word_size * self.num_words_per_bank

        # If this was hard coded, don't dynamically compute it!
        if not self.words_per_row:
            # Compute the area of the bitcells and estimate a square bank (excluding auxiliary circuitry)
            self.bank_area = bitcell.width * bitcell.height * self.num_bits_per_bank
            self.bank_side_length = sqrt(self.bank_area)

            # Estimate the words per row given the height of the bitcell and the square side length
            self.tentative_num_cols = int(self.bank_side_length / bitcell.width)
            self.words_per_row = self.estimate_words_per_row(self.tentative_num_cols, self.word_size)

            # Estimate the number of rows given the tentative words per row
            self.tentative_num_rows = self.num_bits_per_bank / (self.words_per_row * self.word_size)
            self.words_per_row = self.amend_words_per_row(self.tentative_num_rows, self.words_per_row)

        self.recompute_sizes()

        # Set word_per_row in OPTS
        OPTS.words_per_row = self.words_per_row
        debug.info(1, "Set SRAM Words Per Row={}".format(OPTS.words_per_row))

    def recompute_sizes(self):
        """
        Calculate the auxiliary values assuming fixed number of words per row.
        This can be called multiple times from the unit test when we reconfigure an
        SRAM for testing.
        """

        debug.info(1, "Recomputing with words per row: {}".format(self.words_per_row))

        # If the banks changed
        self.num_words_per_bank = self.num_words / self.num_banks
        self.num_bits_per_bank = self.word_size * self.num_words_per_bank

        # Fix the number of columns and rows
        self.num_cols = int(self.words_per_row * self.word_size)
        self.num_rows_temp = int(self.num_words_per_bank / self.words_per_row)
        self.num_rows = self.num_rows_temp + self.num_spare_rows
        debug.info(1, "Rows: {} Cols: {}".format(self.num_rows_temp, self.num_cols))

        # Fix the write_size
        if self.write_size_init:
            self.write_size = self.write_size_init
        else:
            self.write_size = self.word_size

        # Compute the address and bank sizes
        self.row_addr_size = ceil(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))
        #self.addr_size = self.bank_addr_size
        debug.info(1, "Row addr size: {}".format(self.row_addr_size)
                   + " Col addr size: {}".format(self.col_addr_size)
                   + " Bank addr size: {}".format(self.bank_addr_size))

        num_ports = OPTS.num_rw_ports + OPTS.num_r_ports + OPTS.num_w_ports
        if num_ports == 1:
            if ((self.num_cols + num_ports + self.num_spare_cols) % self.array_col_multiple != 0):
                debug.error("Invalid number of cols including rbl(s): {}. Total cols must be divisible by {}".format(self.num_cols + num_ports + self.num_spare_cols, self.array_col_multiple), -1)

            if ((self.num_rows + num_ports) % self.array_row_multiple != 0):
                debug.error("invalid number of rows including dummy row(s): {}. Total cols must be divisible by {}".format(self.num_rows + num_ports, self.array_row_multiple), -1)

    def estimate_words_per_row(self, tentative_num_cols, word_size):
        """
        This provides a heuristic rounded estimate for the number of words
        per row.
        """
        tentative_column_ways = tentative_num_cols / word_size
        column_mux_sizes = [1, 2, 4, 8, 16]
        # If we are double, we may want a larger column mux
        if tentative_column_ways > 2 * column_mux_sizes[-1]:
            debug.warning("Extremely large number of columns for 16-way maximum column mux.")

        closest_way = min(column_mux_sizes, key=lambda x: abs(x - tentative_column_ways))

        return closest_way

    def amend_words_per_row(self, tentative_num_rows, words_per_row):
        """
        This picks the number of words per row more accurately by limiting
        it to a minimum and maximum.
        """
        # Recompute the words per row given a hard max
        if(not OPTS.is_unit_test and tentative_num_rows > 512):
            debug.check(tentative_num_rows * words_per_row <= 4096,
                        "Number of words exceeds 2048")
            return int(words_per_row * tentative_num_rows / 512)

        # Recompute the words per row given a hard min
        if (not OPTS.is_unit_test and tentative_num_rows < 16):
            debug.check(tentative_num_rows * words_per_row >= 16,
                        "Minimum number of rows is 16, but given {0}".format(tentative_num_rows))
            return int(words_per_row * tentative_num_rows / 16)

        return words_per_row

    def setup_multiport_constants(self):
        """
        These are contants and lists that aid multiport design.
        Ports are always in the order RW, W, R.
        Port indices start from 0 and increment.
        A first RW port will have clk0, csb0, web0, addr0, data0
        A first W port (with no RW ports) will be: clk0, csb0, addr0, data0

        """
        total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports

        # These are the read/write port indices.
        self.readwrite_ports = []
        # These are the read/write and write-only port indices
        self.write_ports = []
        # These are the write-only port indices.
        self.writeonly_ports = []
        # These are the read/write and read-only port indices
        self.read_ports = []
        # These are the read-only port indices.
        self.readonly_ports = []
        # These are all the ports
        self.all_ports = list(range(total_ports))

        # The order is always fixed as RW, W, R
        port_number = 0
        for port in range(OPTS.num_rw_ports):
            self.readwrite_ports.append(port_number)
            self.write_ports.append(port_number)
            self.read_ports.append(port_number)
            port_number += 1
        for port in range(OPTS.num_w_ports):
            self.write_ports.append(port_number)
            self.writeonly_ports.append(port_number)
            port_number += 1
        for port in range(OPTS.num_r_ports):
            self.read_ports.append(port_number)
            self.readonly_ports.append(port_number)
            port_number += 1
