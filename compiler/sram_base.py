import sys
import datetime
import getpass
import debug
from math import log,sqrt,ceil
from vector import vector
from globals import OPTS, print_time

from design import design
    
class sram_base(design):
    """
    Dynamically generated SRAM by connecting banks to control logic. The
    number of banks should be 1 , 2 or 4
    """
    def __init__(self, word_size, num_words, num_banks, name):
        design.__init__(self, name)
        
        from importlib import reload
        c = reload(__import__(OPTS.control_logic))
        self.mod_control_logic = getattr(c, OPTS.control_logic)

        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()

        c = reload(__import__(OPTS.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.ms_flop)
        self.ms_flop = self.mod_ms_flop()
        
        self.word_size = word_size
        self.num_words = num_words
        self.num_banks = num_banks

    def whoami():
        print("abstract")

    def compute_sizes(self):
        """  Computes the organization of the memory using bitcell size by trying to make it square."""

        debug.check(self.num_banks in [1,2,4], "Valid number of banks are 1 , 2 and 4.")

        self.num_words_per_bank = self.num_words/self.num_banks
        self.num_bits_per_bank = self.word_size*self.num_words_per_bank

        # Compute the area of the bitcells and estimate a square bank (excluding auxiliary circuitry)
        self.bank_area = self.bitcell.width*self.bitcell.height*self.num_bits_per_bank
        self.bank_side_length = sqrt(self.bank_area)

        # Estimate the words per row given the height of the bitcell and the square side length
        self.tentative_num_cols = int(self.bank_side_length/self.bitcell.width)
        self.words_per_row = self.estimate_words_per_row(self.tentative_num_cols, self.word_size)

        # Estimate the number of rows given the tentative words per row
        self.tentative_num_rows = self.num_bits_per_bank / (self.words_per_row*self.word_size)
        self.words_per_row = self.amend_words_per_row(self.tentative_num_rows, self.words_per_row)
        
        # Fix the number of columns and rows
        self.num_cols = int(self.words_per_row*self.word_size)
        self.num_rows = int(self.num_words_per_bank/self.words_per_row)

        # Compute the address and bank sizes
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))
        
        debug.info(1,"Words per row: {}".format(self.words_per_row))

    def estimate_words_per_row(self,tentative_num_cols, word_size):
        """
        This provides a heuristic rounded estimate for the number of words
        per row.
        """

        if tentative_num_cols < 1.5*word_size:
            return 1
        elif tentative_num_cols > 3*word_size:
            return 4
        else:
            return 2

    def amend_words_per_row(self,tentative_num_rows, words_per_row):
        """
        This picks the number of words per row more accurately by limiting
        it to a minimum and maximum.
        """
        # Recompute the words per row given a hard max
        if(tentative_num_rows > 512):
            debug.check(tentative_num_rows*words_per_row <= 2048, "Number of words exceeds 2048")
            return int(words_per_row*tentative_num_rows/512)
        # Recompute the words per row given a hard min
        if(tentative_num_rows < 16):
            debug.check(tentative_num_rows*words_per_row >= 16, "Minimum number of rows is 16, but given {0}".format(tentative_num_rows))
            return int(words_per_row*tentative_num_rows/16)
            
        return words_per_row

    def add_pins(self):
        """ Add pins for entire SRAM. """

        for i in range(self.word_size):
            self.add_pin("DIN[{0}]".format(i),"INPUT")
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i),"INPUT")

        # These are used to create the physical pins too
        self.control_logic_inputs=self.control_logic.get_inputs()
        self.control_logic_outputs=self.control_logic.get_outputs()
        
        self.add_pin_list(self.control_logic_inputs,"INPUT")

        for i in range(self.word_size):
            self.add_pin("DOUT[{0}]".format(i),"OUTPUT")
        
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")


    def create_layout(self):
        """ Layout creation """    
        self.add_modules()
        self.route()

    def compute_bus_sizes(self):
        """ Compute the independent bus widths shared between two and four bank SRAMs """
        
        # address size + control signals + one-hot bank select signals
        self.num_vertical_line = self.addr_size + self.control_size + log(self.num_banks,2) + 1
        # data bus size
        self.num_horizontal_line = self.word_size

        self.vertical_bus_width = self.m2_pitch*self.num_vertical_line
        # vertical bus height depends on 2 or 4 banks
        
        self.data_bus_height = self.m3_pitch*self.num_horizontal_line
        self.data_bus_width = 2*(self.bank.width + self.bank_to_bus_distance) + self.vertical_bus_width
        
        self.control_bus_height = self.m1_pitch*(self.control_size+2) 
        self.control_bus_width = self.bank.width + self.bank_to_bus_distance + self.vertical_bus_width
        
        self.supply_bus_height = self.m1_pitch*2 # 2 for vdd/gnd placed with control bus
        self.supply_bus_width = self.data_bus_width

        # Sanity check to ensure we can fit the control logic above a single bank (0.9 is a hack really)
        debug.check(self.bank.width + self.vertical_bus_width > 0.9*self.control_logic.width,
                    "Bank is too small compared to control logic.")
        
        
        
    def add_busses(self):
        """ Add the horizontal and vertical busses """
        # Vertical bus
        # The order of the control signals on the control bus:
        self.control_bus_names = ["clk_buf", "tri_en_bar", "tri_en", "clk_buf_bar", "w_en", "s_en"]
        self.vert_control_bus_positions = self.create_vertical_bus(layer="metal2",
                                                                   pitch=self.m2_pitch,
                                                                   offset=self.vertical_bus_offset,
                                                                   names=self.control_bus_names,
                                                                   length=self.vertical_bus_height)

        self.addr_bus_names=["A[{}]".format(i) for i in range(self.addr_size)]
        self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="metal2",
                                                                            pitch=self.m2_pitch,
                                                                            offset=self.addr_bus_offset,
                                                                            names=self.addr_bus_names,
                                                                            length=self.addr_bus_height))

        
        self.bank_sel_bus_names = ["bank_sel[{}]".format(i) for i in range(self.num_banks)]
        self.vert_control_bus_positions.update(self.create_vertical_pin_bus(layer="metal2",
                                                                            pitch=self.m2_pitch,
                                                                            offset=self.bank_sel_bus_offset,
                                                                            names=self.bank_sel_bus_names,
                                                                            length=self.vertical_bus_height))
        

        # Horizontal data bus
        self.data_bus_names = ["DATA[{}]".format(i) for i in range(self.word_size)]
        self.data_bus_positions = self.create_horizontal_pin_bus(layer="metal3",
                                                                 pitch=self.m3_pitch,
                                                                 offset=self.data_bus_offset,
                                                                 names=self.data_bus_names,
                                                                 length=self.data_bus_width)

        # Horizontal control logic bus
        # vdd/gnd in bus go along whole SRAM
        # FIXME: Fatten these wires?
        self.horz_control_bus_positions = self.create_horizontal_bus(layer="metal1",
                                                                     pitch=self.m1_pitch,
                                                                     offset=self.supply_bus_offset,
                                                                     names=["vdd"],
                                                                     length=self.supply_bus_width)
        # The gnd rail must not be the entire width since we protrude the right-most vdd rail up for
        # the decoder in 4-bank SRAMs
        self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="metal1",
                                                                          pitch=self.m1_pitch,
                                                                          offset=self.supply_bus_offset+vector(0,self.m1_pitch),
                                                                          names=["gnd"],
                                                                          length=self.supply_bus_width))
        self.horz_control_bus_positions.update(self.create_horizontal_bus(layer="metal1",
                                                                          pitch=self.m1_pitch,
                                                                          offset=self.control_bus_offset,
                                                                          names=self.control_bus_names,
                                                                          length=self.control_bus_width))

        

        

    def route_vdd_gnd(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        # These are the instances that every bank has
        top_instances = [self.bitcell_array_inst,
                         self.precharge_array_inst,
                         self.sense_amp_array_inst,
                         self.write_driver_array_inst,
                         self.tri_gate_array_inst,
                         self.row_decoder_inst,
                         self.wordline_driver_inst]
        # Add these if we use the part...
        if self.col_addr_size > 0:
            top_instances.append(self.col_decoder_inst)
            top_instances.append(self.col_mux_array_inst)
            
        if self.num_banks > 1:
            top_instances.append(self.bank_select_inst)

        
        for inst in top_instances:
            # Column mux has no vdd
            if self.col_addr_size==0 or (self.col_addr_size>0 and inst != self.col_mux_array_inst):
                self.copy_layout_pin(inst, "vdd")
            # Precharge has no gnd
            if inst != self.precharge_array_inst:
                self.copy_layout_pin(inst, "gnd")
        
        
    def create_multi_bank_modules(self):
        """ Create the multibank address flops and bank decoder """
        from dff_buf_array import dff_buf_array
        self.msb_address = dff_buf_array(name="msb_address",
                                         rows=1,
                                         columns=self.num_banks/2)
        self.add_mod(self.msb_address)

        if self.num_banks>2:
            self.msb_decoder = self.bank.decoder.pre2_4
            self.add_mod(self.msb_decoder)

    def create_modules(self):
        """ Create all the modules that will be used """

        from control_logic import control_logic
        # Create the control logic module
        self.control_logic = self.mod_control_logic(num_rows=self.num_rows)
        self.add_mod(self.control_logic)

        # Create the address and control flops (but not the clk)
        dff_size = self.addr_size
        from dff_array import dff_array
        self.addr_dff = dff_array(name="dff_array", rows=dff_size, columns=1)
        self.add_mod(self.addr_dff)
        
        # Create the bank module (up to four are instantiated)
        from bank import bank
        self.bank = bank(word_size=self.word_size,
                         num_words=self.num_words_per_bank,
                         words_per_row=self.words_per_row,
                         num_banks=self.num_banks,
                         name="bank")
        self.add_mod(self.bank)

        # Create bank decoder
        if(self.num_banks > 1):
            self.create_multi_bank_modules()

        self.bank_count = 0

        self.supply_rail_width = self.bank.supply_rail_width
        self.supply_rail_pitch = self.bank.supply_rail_pitch



    def add_bank(self, bank_num, position, x_flip, y_flip):
        """ Place a bank at the given position with orientations """

        # x_flip ==  1 --> no flip in x_axis
        # x_flip == -1 --> flip in x_axis
        # y_flip ==  1 --> no flip in y_axis
        # y_flip == -1 --> flip in y_axis

        # x_flip and y_flip are used for position translation

        if x_flip == -1 and y_flip == -1:
            bank_rotation = 180
        else:
            bank_rotation = 0

        if x_flip == y_flip:
            bank_mirror = "R0"
        elif x_flip == -1:
            bank_mirror = "MX"
        elif y_flip == -1:
            bank_mirror = "MY"
        else:
            bank_mirror = "R0"
            
        bank_inst=self.add_inst(name="bank{0}".format(bank_num),
                                mod=self.bank,
                                offset=position,
                                mirror=bank_mirror,
                                rotate=bank_rotation)

        temp = []
        for i in range(self.word_size):
            temp.append("DOUT[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("DIN[{0}]".format(i))
        for i in range(self.bank_addr_size):
            temp.append("A[{0}]".format(i))
        if(self.num_banks > 1):
            temp.append("bank_sel[{0}]".format(bank_num))
        temp.extend(["s_en", "w_en", "tri_en_bar", "tri_en",
                     "clk_buf_bar","clk_buf" , "vdd", "gnd"])
        self.connect_inst(temp)

        return bank_inst



    def add_addr_dff(self, position):
        """ Add and place address and control flops """
        self.addr_dff_inst = self.add_inst(name="address",
                                           mod=self.addr_dff,
                                           offset=position)
        # inputs, outputs/output/bar
        inputs = []
        outputs = []
        for i in range(self.addr_size):
            inputs.append("ADDR[{}]".format(i))
            outputs.append("A[{}]".format(i))

        self.connect_inst(inputs + outputs + ["clk_buf", "vdd", "gnd"])
    
    def add_control_logic(self, position):
        """ Add and place control logic """
        inputs = []
        for i in self.control_logic_inputs:
            if i != "clk":
                inputs.append(i+"_s")
            else:
                inputs.append(i)
        
        self.control_logic_inst=self.add_inst(name="control",
                                              mod=self.control_logic,
                                              offset=position)
        self.connect_inst(inputs + self.control_logic_outputs + ["vdd", "gnd"])


    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        if self.num_banks==1: return
        
        for n in self.control_bus_names:
            self.add_label(text=n,
                           layer="metal2",  
                           offset=self.vert_control_bus_positions[n])
        for n in self.bank_sel_bus_names:
            self.add_label(text=n,
                           layer="metal2",  
                           offset=self.vert_control_bus_positions[n])





    def connect_rail_from_left_m2m3(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = vector(dest_pin.cx(), in_pos.y)
        self.add_wire(("metal3","via2","metal2"),[in_pos, out_pos, out_pos - vector(0,self.m2_pitch)])
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=src_pin.rc(),
                            rotate=90)
        
    def connect_rail_from_left_m2m1(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = vector(dest_pin.cx(), in_pos.y)
        self.add_wire(("metal2","via1","metal1"),[in_pos, out_pos, out_pos - vector(0,self.m2_pitch)])

        

    def sp_write(self, sp_name):
        # Write the entire spice of the object to the file
        ############################################################
        # Spice circuit
        ############################################################
        sp = open(sp_name, 'w')

        sp.write("**************************************************\n")
        sp.write("* OpenRAM generated memory.\n")
        sp.write("* Words: {}\n".format(self.num_words))
        sp.write("* Data bits: {}\n".format(self.word_size))
        sp.write("* Banks: {}\n".format(self.num_banks))
        sp.write("* Column mux: {}:1\n".format(self.words_per_row))
        sp.write("**************************************************\n")        
        # This causes unit test mismatch
        # sp.write("* Created: {0}\n".format(datetime.datetime.now()))
        # sp.write("* User: {0}\n".format(getpass.getuser()))
        # sp.write(".global {0} {1}\n".format(spice["vdd_name"], 
        #                                     spice["gnd_name"]))
        usedMODS = list()
        self.sp_write_file(sp, usedMODS)
        del usedMODS
        sp.close()

    def analytical_delay(self,slew,load):
        """ LH and HL are the same in analytical model. """
        return self.bank.analytical_delay(slew,load)

        
