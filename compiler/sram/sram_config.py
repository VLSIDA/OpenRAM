# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from math import log,sqrt,ceil
from importlib import reload
from globals import OPTS
from sram_factory import factory

class sram_config:
    """ This is a structure that is used to hold the SRAM configuration options. """
    
    def __init__(self, word_size, num_words, write_size = None, num_banks=1, words_per_row=None):
        self.word_size = word_size
        self.num_words = num_words
        self.write_size = write_size
        self.num_banks = num_banks

        # This will get over-written when we determine the organization
        self.words_per_row = words_per_row


        self.compute_sizes()


    def set_local_config(self, module):
        """ Copy all of the member variables to the given module for convenience """
        
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        # Copy all the variables to the local module
        for member in members:
            setattr(module,member,getattr(self,member))

    def compute_sizes(self):
        """  Computes the organization of the memory using bitcell size by trying to make it square."""

        bitcell = factory.create(module_type="bitcell")
        
        
        debug.check(self.num_banks in [1,2,4], "Valid number of banks are 1 , 2 and 4.")

        self.num_words_per_bank = self.num_words/self.num_banks
        self.num_bits_per_bank = self.word_size*self.num_words_per_bank
        
        # If this was hard coded, don't dynamically compute it!
        if not self.words_per_row:
            # Compute the area of the bitcells and estimate a square bank (excluding auxiliary circuitry)
            self.bank_area = bitcell.width*bitcell.height*self.num_bits_per_bank
            self.bank_side_length = sqrt(self.bank_area)

            # Estimate the words per row given the height of the bitcell and the square side length
            self.tentative_num_cols = int(self.bank_side_length/bitcell.width)
            self.words_per_row = self.estimate_words_per_row(self.tentative_num_cols, self.word_size)

            # Estimate the number of rows given the tentative words per row
            self.tentative_num_rows = self.num_bits_per_bank / (self.words_per_row*self.word_size)
            self.words_per_row = self.amend_words_per_row(self.tentative_num_rows, self.words_per_row)

        self.recompute_sizes()

    def recompute_sizes(self):
        """ 
        Calculate the auxiliary values assuming fixed number of words per row. 
        This can be called multiple times from the unit test when we reconfigure an 
        SRAM for testing.
        """

        debug.info(1,"Recomputing with words per row: {}".format(self.words_per_row))
        
        # If the banks changed
        self.num_words_per_bank = self.num_words/self.num_banks
        self.num_bits_per_bank = self.word_size*self.num_words_per_bank
        
        # Fix the number of columns and rows
        self.num_cols = int(self.words_per_row*self.word_size)
        self.num_rows = int(self.num_words_per_bank/self.words_per_row)
        debug.info(1,"Rows: {} Cols: {}".format(self.num_rows,self.num_cols))

        # Compute the address and bank sizes
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))
        debug.info(1,"Row addr size: {}".format(self.row_addr_size)
                   + " Col addr size: {}".format(self.col_addr_size)
                   + " Bank addr size: {}".format(self.bank_addr_size))


    def estimate_words_per_row(self,tentative_num_cols, word_size):
        """
        This provides a heuristic rounded estimate for the number of words
        per row.
        """

        if tentative_num_cols < 1.5*word_size:
            return 1
        elif tentative_num_cols < 3*word_size:
            return 2
        elif tentative_num_cols < 6*word_size:
            return 4
        else:
            if tentative_num_cols > 16*word_size:
                debug.warning("Reaching column mux size limit. Consider increasing above 8-way.")
            return 8

    def amend_words_per_row(self,tentative_num_rows, words_per_row):
        """
        This picks the number of words per row more accurately by limiting
        it to a minimum and maximum.
        """
        # Recompute the words per row given a hard max
        if(not OPTS.is_unit_test and tentative_num_rows > 512):
            debug.check(tentative_num_rows*words_per_row <= 2048, "Number of words exceeds 2048")
            return int(words_per_row*tentative_num_rows/512)
        # Recompute the words per row given a hard min
        if(not OPTS.is_unit_test and tentative_num_rows < 16):
            debug.check(tentative_num_rows*words_per_row >= 16, "Minimum number of rows is 16, but given {0}".format(tentative_num_rows))
            return int(words_per_row*tentative_num_rows/16)
            
        return words_per_row
