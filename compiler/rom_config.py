# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from typing import List
from math import log, sqrt, ceil
from openram import debug
from openram.sram_factory import factory
from openram import OPTS



class rom_config:
    """ This is a structure that is used to hold the ROM configuration options. """

    def __init__(self, word_size, rom_data, words_per_row=None, rom_endian="little", scramble_bits=True, strap_spacing=8, data_type="hex"):
        self.word_size = word_size
        self.word_bits = self.word_size * 8
        self.rom_data = rom_data
        self.strap_spacing = strap_spacing
        # TODO: This currently does nothing. It should change the behavior of the chunk funciton.
        self.endian = rom_endian
        self.data_type = data_type
        # This should pretty much always be true. If you want to make silicon art you might set to false
        self.scramble_bits = scramble_bits
        # This will get over-written when we determine the organization
        self.words_per_row = words_per_row

        self.compute_sizes()

    def __str__(self):
        """ override print function output """
        config_items = ["word_size",
                        "num_words",
                        "words_per_row",
                        "endian",
                        "strap_spacing",
                        "rom_data"]
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
        """  Computes the organization of the memory using data size by trying to make it a rectangle."""

        if self.data_type == "hex":
            raw_data = self.read_data_hex()
        elif self.data_type == "bin":
            raw_data = self.read_data_bin()
        else:
            debug.error(f"Invalid input data type: {self.data_type}", -1)

        # data size in bytes
        data_size = len(raw_data) / 8
        self.num_words = int(data_size / self.word_size)

        # If this was hard coded, don't dynamically compute it!
        if not self.words_per_row:

            # Row size if the array was square
            bytes_per_row = sqrt(self.num_words)

            # Heuristic to value longer wordlines over long bitlines.
            # The extra factor of 2 in the denominator should make the array less square
            self.words_per_row = int(ceil(bytes_per_row /(2*self.word_size)))

        self.cols = self.words_per_row * self.word_size * 8
        self.rows = int(self.num_words / self.words_per_row)

        self.chunk_data(raw_data)

        # Set word_per_row in OPTS
        OPTS.words_per_row = self.words_per_row
        debug.info(1, "Read rom data file: length {0} bytes, {1} words, set number of cols to {2}, rows to {3}, with {4} words per row".format(data_size, self.num_words, self.cols, self.rows, self.words_per_row))

    def read_data_hex(self) -> List[int]:
        # Read data as hexidecimal text file
        with open(self.rom_data, 'r') as hex_file:
            hex_data = hex_file.read()

        # Convert from hex into an int
        data_int = int(hex_data, 16)
        # Then from int into a right aligned, zero padded string
        bin_string = bin(data_int)[2:].zfill(len(hex_data) * 4)

        # Then turn the string into a list of ints
        bin_data = list(bin_string)
        raw_data = [int(x) for x in bin_data]
        return raw_data

    def read_data_bin(self) -> List[int]:

        # Read data as a binary file
        with open(self.rom_data, 'rb') as bin_file:
            bin_data = bin_file.read()

        # Convert from a list of bytes to a single string of bits
        bin_string = "".join(f"{n:08b}" for n in bin_data)

        # Then turn the string into a list of ints
        bin_data = list(bin_string)
        raw_data = [int(x) for x in bin_data]
        return raw_data


    def chunk_data(self, raw_data: List[int]):
        """
        Chunks a flat list of bits into rows based on the calculated ROM sizes. Handles scrambling of data
        """
        bits_per_row = self.cols

        chunked_data = []

        for i in range(0, len(raw_data), bits_per_row):
            row_data = raw_data[i:i + bits_per_row]
            if len(row_data) < bits_per_row:
                row_data = [0] * (bits_per_row - len(row_data)) + row_data
            chunked_data.append(row_data)

        self.data = chunked_data

        if self.scramble_bits:
            scrambled_chunked = []

            for row_data in chunked_data:
                scambled_data = []
                for bit in range(self.word_bits):
                    for word in range(self.words_per_row):
                        scambled_data.append(row_data[bit + word * self.word_bits])
                scrambled_chunked.append(scambled_data)
            self.data = scrambled_chunked

