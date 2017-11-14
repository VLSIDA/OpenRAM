import debug
from math import log

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
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))


    def trim(self, address, data_bit):
        """ Reduce the spice netlist but KEEP the given bits at the
        address (and things that will add capacitive load!)"""

        # Always start fresh if we do multiple reductions
        self.sp_buffer = self.spice
        
        # Find the row and column indices for the removals
        # Convert address froms tring to int
        address = int(address,2)
        array_row = address >> self.col_addr_size
        # Which word in the array (0 if only one word)
        if self.col_addr_size>0:
            lower_mask = int(self.col_addr_size-1)
            lower_address = address & lower_mask
        else:
            lower_address=0
        # Which bit in the array
        array_bit = lower_address*self.word_size + data_bit

        # 1. Keep cells in the bitcell array based on WL and BL
        wl_name = "wl[{}]".format(array_row)
        bl_name = "bl[{}]".format(array_bit)
        self.remove_insts("bitcell_array",[wl_name,bl_name])

        # 2. Keep sense amps basd on BL
        self.remove_insts("sense_amp_array",[bl_name])

        # 3. Keep column muxes basd on BL
        self.remove_insts("column_mux_array",[bl_name])
        
        # 4. Keep write driver based on DATA
        data_name = "data[{}]".format(data_bit)
        self.remove_insts("write_driver_array",[data_name])

        # 5. Keep wordline driver based on WL
        # Need to keep the gater too
        #self.remove_insts("wordline_driver",wl_name)
        
        # 6. Keep precharges based on BL
        self.remove_insts("precharge_array",[bl_name])
        
        # Everything else isn't worth removing. :)
        
        # Finally, write out the buffer as the new reduced file
        sp = open(self.reduced_spfile, "w")
        sp.write("\n".join(self.sp_buffer))

        
    def remove_insts(self, subckt_name, keep_inst_list):
        """This will remove all of the instances in the list from the named
        subckt that DO NOT contain a term in the list.  It just does a
        match of the line with a term so you can search for a single
        net connection, the instance name, anything..
        """
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
                for k in keep_inst_list:
                    if k in line:
                        new_buffer.append(line)
                        break
            else:
                new_buffer.append(line)

        self.sp_buffer = new_buffer
