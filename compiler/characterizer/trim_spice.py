# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import re
from math import log, ceil
from openram import debug


class trim_spice():
    """
    A utility to trim redundant parts of an SRAM spice netlist.
    Input is an SRAM spice file. Output is an equivalent netlist
    that works for a single address and range of data bits.
    """

    def __init__(self, spfile, reduced_spfile):
        self.sp_file = spfile
        self.reduced_spfile = reduced_spfile

        debug.info(1,"Trimming non-critical cells to speed-up characterization: {}.".format(reduced_spfile))

        # Load the file into a buffer for performance
        sp = open(self.sp_file, "r")
        self.spice = sp.readlines()
        sp.close()
        for i in range(len(self.spice)):
            self.spice[i] = self.spice[i].rstrip(" \n")

        self.sp_buffer = self.spice

    def set_configuration(self, banks, rows, columns, word_size):
        """ Set the configuration of SRAM sizes that we are simulating.
        Need the: number of banks, number of rows in each bank, number of
        columns in each bank, and data word size."""
        self.num_banks = banks
        self.num_rows = rows
        self.num_columns = columns
        self.word_size = word_size

        self.words_per_row = self.num_columns / self.word_size
        self.row_addr_size = ceil(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))

    def trim(self, address, data_bit):
        """
        Reduce the spice netlist but KEEP the given bits at the
        address (and things that will add capacitive load!)
        """

        # Always start fresh if we do multiple reductions
        self.sp_buffer = self.spice

        # Split up the address and convert to an int
        wl_address = int(address[self.col_addr_size:], 2)
        if self.col_addr_size > 0:
            col_address = int(address[0:self.col_addr_size], 2)
        else:
            col_address = 0

        # 1. Keep cells in the bitcell array based on WL and BL
        wl_name = "wl_{}".format(wl_address)
        bl_name = "bl_{}".format(int(self.words_per_row*data_bit + col_address))

        # Prepend info about the trimming
        addr_msg = "Keeping {} address".format(address)
        self.sp_buffer.insert(0, "* "+addr_msg)
        debug.info(1,addr_msg)
        data_msg = "Keeping {} data bit".format(data_bit)
        self.sp_buffer.insert(0, "* "+data_msg)
        debug.info(1,data_msg)
        bl_msg = "Keeping {} (trimming other BLs)".format(bl_name)
        wl_msg = "Keeping {} (trimming other WLs)".format(wl_name)
        self.sp_buffer.insert(0, "* "+bl_msg)
        debug.info(1,bl_msg)
        self.sp_buffer.insert(0, "* "+wl_msg)
        debug.info(1,wl_msg)
        self.sp_buffer.insert(0, "* It should NOT be used for LVS!!")
        self.sp_buffer.insert(0, "* WARNING: This is a TRIMMED NETLIST.")

        wl_regex = r"wl\d*_{}".format(wl_address)
        bl_regex = r"bl\d*_{}".format(int(self.words_per_row*data_bit + col_address))
        bl_no_port_regex = r"bl_{}".format(int(self.words_per_row*data_bit + col_address))

        self.remove_insts("bitcell_array",[wl_regex,bl_regex])

        # 2. Keep sense amps basd on BL
        self.remove_insts("sense_amp_array",[bl_no_port_regex])

        # 3. Keep column muxes basd on BL
        self.remove_insts("single_level_column_mux_array", [bl_no_port_regex])

        # 4. Keep write driver based on DATA
        data_regex = r"data_{}".format(data_bit)
        self.remove_insts("write_driver_array", [data_regex])

        # 5. Keep wordline driver based on WL
        # Need to keep the gater too
        #self.remove_insts("wordline_driver",wl_regex)

        # 6. Keep precharges based on BL
        self.remove_insts("precharge_array",[bl_regex])

        # Everything else isn't worth removing. :)

        # Finally, write out the buffer as the new reduced file
        sp = open(self.reduced_spfile, "w")
        sp.write("\n".join(self.sp_buffer))
        sp.close()

    def remove_insts(self, subckt_name, keep_inst_list):
        """This will remove all of the instances in the list from the named
        subckt that DO NOT contain a term in the list.  It just does a
        match of the line with a term so you can search for a single
        net connection, the instance name, anything..
        """
        removed_insts = 0
        # Expects keep_inst_list are regex patterns. Compile them here.
        compiled_patterns = [re.compile(pattern) for pattern in keep_inst_list]

        start_name = ".SUBCKT {}".format(subckt_name)
        end_name = ".ENDS {}".format(subckt_name)

        in_subckt=False
        new_buffer=[]
        for line in self.sp_buffer:
            if start_name in line:
                new_buffer.append(line)
                in_subckt=True
            elif end_name in line:
                new_buffer.append(line)
                in_subckt=False
            elif in_subckt:
                removed_insts += 1
                for pattern in compiled_patterns:
                    if pattern.search(line) != None:
                        new_buffer.append(line)
                        removed_insts -= 1
                        break
            else:
                new_buffer.append(line)

        self.sp_buffer = new_buffer
        debug.info(2, "Removed {} instances from {} subcircuit.".format(removed_insts, subckt_name))
