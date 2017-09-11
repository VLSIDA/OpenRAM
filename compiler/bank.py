import sys
from tech import drc, parameter
import debug
import design
import math
from math import log,sqrt,ceil
from contact import contact
from pinv import pinv
from nand_2 import nand_2
from nor_2 import nor_2
from vector import vector
from globals import OPTS

class bank(design.design):
    """
    Dynamically generated a single Bank including bitcell array,
    hierarchical_decoder, precharge, column_mux, write driver and sense amplifiers.
    """

    def __init__(self, word_size, num_words, words_per_row, num_banks=1, name=""):

        mod_list = ["tri_gate", "bitcell", "decoder", "ms_flop_array", "wordline_driver",
                    "bitcell_array",   "sense_amp_array",    "precharge_array",
                    "column_mux_array", "write_driver_array", "tri_gate_array"]
        for mod_name in mod_list:
            config_mod_name = getattr(OPTS.config, mod_name)
            class_file = reload(__import__(config_mod_name))
            mod_class = getattr(class_file , config_mod_name)
            setattr (self, "mod_"+mod_name, mod_class)

        if name == "":
            name = "bank_{0}_{1}".format(word_size, num_words)
        design.design.__init__(self, name)
        debug.info(2, "create sram of size {0} with {1} words".format(word_size,num_words))

        self.word_size = word_size
        self.num_words = num_words
        self.words_per_row = words_per_row
        self.num_banks = num_banks

        self.compute_sizes()
	self.add_pins()
        self.create_modules()
        self.add_modules()
        self.setup_layout_constraints()
        self.route_layout()

        # Can remove the following, but it helps for debug!
        self.add_lvs_correspondence_points() 
        
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for Bank module"""
        for i in range(self.word_size):
            self.add_pin("DATA[{0}]".format(i))
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i))

        # For more than one bank, we have a bank select and name
        # the signals gated_*.
        if(self.num_banks > 1):
            self.add_pin("bank_select")
        self.add_pin("s_en")
        self.add_pin("w_en")
        self.add_pin("tri_en_bar")
        self.add_pin("tri_en")
        self.add_pin("clk_bar")
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def route_layout(self):
        """ Create routing amoung the modules """
        self.create_central_bus()
        self.route_precharge_to_bitcell_array()
        self.route_sense_amp_to_trigate()
        self.route_tri_gate_out()
        self.route_wordline_driver()
        self.route_row_decoder()
        self.route_column_address_lines()
        self.route_msf_address()
        self.route_control_lines()
        self.add_control_pins()
        if self.num_banks > 1:
            self.route_bank_select()
        self.route_vdd_supply()
        self.route_gnd_supply()

        #self.offset_all_coordinates()

    def add_modules(self):
        """ Add modules. The order should not matter! """
        self.add_bitcell_array()
        self.add_precharge_array()
        
        if self.col_addr_size > 0:
            self.add_column_mux_array()
            self.column_mux_height = self.column_mux_array.height
        else:
            self.column_mux_height = 0
        if self.col_addr_size > 1: # size 1 is from addr FF
            self.add_column_decoder()
            
        self.add_sense_amp_array()
        self.add_write_driver_array()
        self.add_msf_data_in()
        self.add_tri_gate_array()
        self.add_row_decoder()
        self.add_wordline_driver()
        self.add_msf_address()
        if(self.num_banks > 1):
            self.add_bank_select()

    def compute_sizes(self):
        """  Computes the required sizes to create the bank """

        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words / self.words_per_row

        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.addr_size = self.col_addr_size + self.row_addr_size

        debug.check(self.num_rows*self.num_cols==self.word_size*self.num_words,"Invalid bank sizes.")
        debug.check(self.addr_size==self.col_addr_size + self.row_addr_size,"Invalid address break down.")

        # Width for left gnd rail
        self.vdd_rail_width = 5*drc["minwidth_metal2"]
        self.gnd_rail_width = 5*drc["minwidth_metal2"]

        # Number of control lines in the bus
        self.num_control_lines = 6
        # The order of the control signals on the control bus:
        self.control_signals = ["clk", "tri_en_bar", "tri_en", "clk_bar", "w_en", "s_en"]
        if self.num_banks>1:
            self.control_signals = ["gated_"+str for str in self.control_signals]
        # The central bus is the column address (both polarities), row address
        if self.col_addr_size>0:
            self.num_addr_lines = 2**self.col_addr_size + self.row_addr_size
        else:
            self.num_addr_lines = self.row_addr_size        

        # M1/M2 routing pitch is based on contacted pitch
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.m2m3_via = contact(layer_stack=("metal2", "via2", "metal3"))
        self.m1_pitch = self.m1m2_via.height + max(drc["metal1_to_metal1"],drc["metal2_to_metal2"])
        self.m2_pitch = self.m2m3_via.height + max(drc["metal2_to_metal2"],drc["metal3_to_metal3"])
        self.m2_width = drc["minwidth_metal2"]
        self.m3_width = drc["minwidth_metal3"]        

        # Overall central bus gap. It includes all the column mux lines,
        # control lines, address flop to decoder lines and a GND power rail in M2
        # one pitch on the right on the right of the control lines
        self.start_of_right_central_bus = -self.m2_pitch * (self.num_control_lines + 1)
        # one pitch on the right on the addr lines and one on the right of the gnd rail
        self.start_of_left_central_bus = self.start_of_right_central_bus - self.m2_pitch*(self.num_addr_lines+2) - self.gnd_rail_width
        # add a pitch on each end and around the gnd rail
        self.overall_central_bus_width = self.m2_pitch * (self.num_control_lines + self.num_addr_lines + 5) + self.gnd_rail_width





    def create_modules(self):
        """ Create all the modules using the class loader """
        self.tri = self.mod_tri_gate()
        self.bitcell = self.mod_bitcell()
        
        self.bitcell_array = self.mod_bitcell_array(cols=self.num_cols,
                                                    rows=self.num_rows)
        self.add_mod(self.bitcell_array)

        self.precharge_array = self.mod_precharge_array(columns=self.num_cols,
                                                        ptx_width=drc["minwidth_tx"])
        self.add_mod(self.precharge_array)

        if(self.col_addr_size > 0):
            self.column_mux_array = self.mod_column_mux_array(columns=self.num_cols, 
                                                              word_size=self.word_size)
            self.add_mod(self.column_mux_array)


        self.sense_amp_array = self.mod_sense_amp_array(word_size=self.word_size, 
                                                       words_per_row=self.words_per_row)
        self.add_mod(self.sense_amp_array)

        self.write_driver_array = self.mod_write_driver_array(columns=self.num_cols,
                                                              word_size=self.word_size)
        self.add_mod(self.write_driver_array)

        self.decoder = self.mod_decoder(rows=self.num_rows)
        self.add_mod(self.decoder)

        self.msf_address = self.mod_ms_flop_array(name="msf_address", 
                                                  columns=self.row_addr_size+self.col_addr_size, 
                                                  word_size=self.row_addr_size+self.col_addr_size)
        self.add_mod(self.msf_address)
        
        self.msf_data_in = self.mod_ms_flop_array(name="msf_data_in", 
                                                  columns=self.num_cols, 
                                                  word_size=self.word_size)
        self.add_mod(self.msf_data_in)
        
        self.tri_gate_array = self.mod_tri_gate_array(columns=self.num_cols, 
                                                      word_size=self.word_size)
        self.add_mod(self.tri_gate_array)

        self.wordline_driver = self.mod_wordline_driver(rows=self.num_rows)
        self.add_mod(self.wordline_driver)

        self.inv = pinv()
        self.add_mod(self.inv)
        
        # 4x Inverter
        self.inv4x = pinv(nmos_width=4*drc["minwidth_tx"])
        self.add_mod(self.inv4x)

        self.nor2 = nor_2()
        self.add_mod(self.nor2)

        # Vertical metal rail gap definition
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height 
                                          - self.m1m2_via.contact_width) / 2
        self.gap_between_rails = self.metal2_extend_contact + drc["metal2_to_metal2"]
        self.gap_between_rail_offset = self.gap_between_rails + drc["minwidth_metal2"]
        self.via_shift = (self.m1m2_via.second_layer_width 
                              - self.m1m2_via.first_layer_width) / 2

    def add_bitcell_array(self):
        """ Adding Bitcell Array """

        self.bitcell_array_inst=self.add_inst(name="bitcell_array", 
                                              mod=self.bitcell_array,
                                              offset=vector(0,0))
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for j in range(self.num_rows):
            temp.append("wl[{0}]".format(j))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

            

    def add_precharge_array(self):
        """ Adding Precharge """

        # The wells must be far enough apart
        # We use two well spacings because the bitcells tend to have a shared rail in the height
        y_offset = self.bitcell_array.height + 2*drc["pwell_to_nwell"]
        self.precharge_array_inst=self.add_inst(name="precharge_array",
                                                mod=self.precharge_array, 
                                                offset=vector(0,y_offset))
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        temp.extend(["clk_bar", "vdd"])
        self.connect_inst(temp)

    def add_column_mux_array(self):
        """ Adding Column Mux when words_per_row > 1 . """

        y_offset = self.column_mux_array.height
        self.col_mux_array_inst=self.add_inst(name="column_mux_array",
                                              mod=self.column_mux_array,
                                              offset=vector(0,y_offset).scale(-1,-1))
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for k in range(self.words_per_row):
                temp.append("sel[{0}]".format(k))
        for j in range(self.word_size):
            temp.append("bl_out[{0}]".format(j))
            temp.append("br_out[{0}]".format(j))
        temp.append("gnd")
        self.connect_inst(temp)

    def add_sense_amp_array(self):
        """ Adding Sense amp  """

        y_offset = self.column_mux_height + self.sense_amp_array.height
        self.sense_amp_array_inst=self.add_inst(name="sense_amp_array",
                                                mod=self.sense_amp_array,
                                                offset=vector(0,y_offset).scale(-1,-1))
        temp = []
        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
            if self.words_per_row == 1:
                temp.append("bl[{0}]".format(i))
                temp.append("br[{0}]".format(i))
            else:
                temp.append("bl_out[{0}]".format(i))
                temp.append("br_out[{0}]".format(i))
                
        temp.extend(["s_en", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_write_driver_array(self):
        """ Adding Write Driver  """

        y_offset = self.sense_amp_array.height + self.column_mux_height + self.write_driver_array.height
        self.write_driver_array_inst=self.add_inst(name="write_driver_array", 
                                                   mod=self.write_driver_array, 
                                                   offset=vector(0,y_offset).scale(-1,-1))

        temp = []
        for i in range(self.word_size):
            temp.append("data_in[{0}]".format(i))
        for i in range(self.word_size):            
            if (self.words_per_row == 1):            
                temp.append("bl[{0}]".format(i))
                temp.append("br[{0}]".format(i))
            else:
                temp.append("bl_out[{0}]".format(i))
                temp.append("br_out[{0}]".format(i))
        temp.extend(["w_en", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_msf_data_in(self):
        """ data_in flip_flop """

        y_offset= self.sense_amp_array.height + self.column_mux_height \
                  + self.write_driver_array.height + self.msf_data_in.height
        self.msf_data_in_inst=self.add_inst(name="data_in_flop_array", 
                                            mod=self.msf_data_in, 
                                            offset=vector(0,y_offset).scale(-1,-1))

        temp = []
        for i in range(self.word_size):
            temp.append("DATA[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("data_in[{0}]".format(i))
            temp.append("data_in_bar[{0}]".format(i))
        temp.extend(["clk_bar", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_tri_gate_array(self):
        """ data tri gate to drive the data bus """
        y_offset = self.sense_amp_array.height+self.column_mux_height \
                   + self.write_driver_array.height + self.msf_data_in.height 
        self.tri_gate_array_inst=self.add_inst(name="tri_gate_array", 
                                              mod=self.tri_gate_array, 
                                               offset=vector(0,y_offset).scale(-1,-1),
                                               mirror="MX")
        temp = []
        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("DATA[{0}]".format(i))
        temp.extend(["tri_en", "tri_en_bar", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_row_decoder(self):
        """  Add the hierarchical row decoder  """


        # The address and control bus will be in between decoder and the main memory array 
        # This bus will route address bits to the decoder input and column mux inputs. 
        # The wires are actually routed after we placed the stuff on both sides.
        # The predecoder is below the x-axis and the main decoder is above the x-axis
        # The address flop and decoder are aligned in the x coord.

        decoder_x_offset = self.decoder.width + self.overall_central_bus_width
        addr_x_offset = self.msf_address.height
        offset = vector(max(decoder_x_offset, addr_x_offset),
                        self.decoder.predecoder_height)
        self.row_decoder_inst=self.add_inst(name="row_decoder", 
                                            mod=self.decoder, 
                                            offset=offset.scale(-1,-1))

        temp = []
        for i in range(self.row_addr_size):
            temp.append("A[{0}]".format(i))
        for j in range(self.num_rows):
            temp.append("dec_out[{0}]".format(j))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def add_wordline_driver(self):
        """ Wordline Driver """

        # The wordline driver is placed to the right of the main decoder width.
        # This means that it slightly overlaps with the hierarchical decoder,
        # but it shares power rails. This may differ for other decoders later...
        x_offset = self.decoder.width + self.overall_central_bus_width - self.decoder.row_decoder_width
        self.wordline_driver_inst=self.add_inst(name="wordline_driver", 
                                                mod=self.wordline_driver, 
                                                offset=vector(x_offset,0).scale(-1,-1))

        temp = []
        for i in range(self.num_rows):
            temp.append("dec_out[{0}]".format(i))
        for i in range(self.num_rows):
            temp.append("wl[{0}]".format(i))

        if(self.num_banks > 1):
            temp.append("gated_clk")
        else:
            temp.append("clk")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

    def add_msf_address(self):
        """ Adding address Flip-flops """

        # A gap between the hierarchical decoder and addr flops
        gap = max(drc["pwell_to_nwell"], 2*self.m2_pitch)

        # The address flops go below the hierarchical decoder
        decoder_x_offset = self.decoder.width + self.overall_central_bus_width
        addr_x_offset = self.msf_address.height + self.overall_central_bus_width
        # msf_address is not in the y-coord because it is rotated
        offset = vector(max(decoder_x_offset, addr_x_offset),
                        self.decoder.predecoder_height +  gap)
        self.msf_address_inst=self.add_inst(name="address_flop_array", 
                                            mod=self.msf_address, 
                                            offset=offset.scale(-1,-1), 
                                            rotate=270)
        temp = []
        for i in range(self.row_addr_size+self.col_addr_size):
            temp.append("ADDR[{0}]".format(i))
        for i in range(self.row_addr_size+self.col_addr_size):            
            if self.col_addr_size==1 and i==self.row_addr_size:
                temp.extend(["sel[1]","sel[0]"])
            else:
                temp.extend(["A[{0}]".format(i),"A_bar[{0}]".format(i)])
        if(self.num_banks > 1):
            temp.append("gated_clk")
        else:
            temp.append("clk")
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)


    def add_column_decoder(self):
        """ Create a 2:4 decoder to decode column select lines if the col_addr_size = 4 """

        # FIXME: Should just load this rather than reference a level down
        if self.col_addr_size == 1:
            return # This is done from the FF outputs directly
        if self.col_addr_size == 2:
            self.col_decoder = self.decoder.pre2_4
        elif self.col_addr_size == 3:
            self.col_decoder = self.decoder.pre3_8
        else:
            # No error checking before?
            debug.error("Invalid column decoder?",-1)
            

        # Place the col decoder just to the left of the control bus
        x_off = self.m2_pitch + self.overall_central_bus_width + self.col_decoder.width
        # Place the col decoder below the the address flops which are below the row decoder (lave some space for wells)
        vertical_gap = max(drc["pwell_to_nwell"], 2*self.m2_pitch) 
        y_off = self.decoder.predecoder_height + self.msf_address.width + self.col_decoder.height + 2*vertical_gap
        self.col_decoder_inst=self.add_inst(name="col_address_decoder", 
                                            mod=self.col_decoder, 
                                            offset=vector(x_off,y_off).scale(-1,-1))
        temp = []
        for i in range(self.col_addr_size):
            temp.append("A[{0}]".format(i + self.row_addr_size))
        for j in range(2**self.col_addr_size):
            temp.append("sel[{0}]".format(j))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def add_bank_select(self):
        """Create a bank select signal that is combined with an array of
        NOR+INV gates to gate the control signals in case of multiple
        banks are created in upper level SRAM module
        """
        xoffset_nor = self.start_of_left_central_bus + self.nor2.width + self.inv4x.width
        xoffset_inv = xoffset_nor + self.nor2.width
        self.bank_select_or_position = vector(-xoffset_nor, self.min_point)

        # bank select inverter
        self.bank_select_inv_position = vector(self.bank_select_or_position.x
                                               - 5 * drc["minwidth_metal2"]
                                               - self.inv4x.width, 
                                               self.min_point)
        self.add_inst(name="bank_select_inv", 
                      mod=self.inv4x, 
                      offset=self.bank_select_inv_position)
        self.connect_inst(["bank_select", "bank_select_bar", "vdd", "gnd"])

        for i in range(self.numb_control_lines):
            # central control bus index
            # 5 = clk,4 = tri_en_bar,3 = tri_en,2 = clk_bar,1 = w_en,0 = s_en
            name_nor = "bank_selector_nor_{0}".format(i)
            name_inv = "bank_selector_inv_{0}".format(i)
            nor2_inv_connection_height = self.inv4x.A_position.y - self.nor2.Z_position.y + 0.5 * drc["minwidth_metal1"]

            if (i % 2):
                y_offset = self.min_point + self.inv.height*(i + 1)
                mod_dir = "MX"
                # nor2 output to inv input
                y_correct = self.nor2.Z_position.y + nor2_inv_connection_height - 0.5 * drc["minwidth_metal1"]
            else:
                y_offset = self.min_point + self.inv.height*i
                mod_dir = "R0"
                # nor2 output to inv input
                y_correct = 0.5 * drc["minwidth_metal1"] - self.nor2.Z_position.y
            connection = vector(xoffset_inv, y_offset - y_correct)

            if i == 3:
                self.add_inst(name=name_nor, 
                              mod=self.nor2, 
                              offset=[xoffset_nor, y_offset], 
                              mirror=mod_dir)
                self.connect_inst(["gated_tri_en_bar",
                                   "bank_select_bar", 
                                   self.control_signals[i].format(i),
                                   "vdd",
                                   "gnd"])
                # connect the metal1 layer to connect to the old inv output
                offset = connection - vector(0, 0.5*drc["minwidth_metal1"])
                self.add_rect(layer="metal1", 
                              offset=offset, 
                              width=self.inv4x.width, 
                              height=drc["minwidth_metal1"])
            elif i == 5:
                offset = [xoffset_nor, y_offset - self.nor2.A_position.y 
                          - 0.5*drc["minwidth_metal1"]]
                self.add_rect(layer="metal1", 
                              offset=offset, 
                              width=self.nor2.width + self.inv4x.width, 
                              height=drc["minwidth_metal1"])
            else:
                self.add_inst(name=name_nor, 
                              mod=self.nor2, 
                              offset=[xoffset_nor, y_offset], 
                              mirror=mod_dir)
                self.connect_inst([self.gated_control_signals[i], 
                                   "bank_select_bar", 
                                   "net_block_nor_inv[{0}]".format(i),
                                   "vdd",
                                   "gnd"])

                self.add_inst(name=name_inv, 
                              mod=self.inv4x, 
                              offset=[xoffset_inv, y_offset], 
                              mirror=mod_dir)
                self.connect_inst(["net_block_nor_inv[{0}]".format(i), 
                                   self.control_signals[i],
                                   "vdd",
                                   "gnd"])

        # nor2 output to inv input
        for i in range(self.numb_control_lines - 1):
            nor2_inv_connection_height = (self.inv4x.A_position.y 
                                          - self.nor2.Z_position.y 
                                          + 0.5 * drc["minwidth_metal1"])
                
            if (i % 2):
                y_offset = self.min_point + self.inv.height * (i + 1)
                mod_dir = "MX"
                y_correct = (-self.nor2.Z_position.y + 0.5 * drc["minwidth_metal1"] 
                             - nor2_inv_connection_height)
            else:
                y_offset = self.min_point + self.inv.height*i
                mod_dir = "R0"
                y_correct = self.nor2.Z_position.y - 0.5 * drc["minwidth_metal1"]
            # nor2 output to inv input
            connection = vector(xoffset_inv, y_offset + y_correct)
            self.add_rect(layer="metal1", 
                          offset=connection, 
                          width=drc["minwidth_metal1"], 
                          height=nor2_inv_connection_height)

    def setup_layout_constraints(self):
        """ Calculating layout constraints, width, height etc """

        #The minimum point is either the bottom of the address flops,
        #the column decoder (if there is one) or the tristate output
        #driver.
        # Leave room for the output below the tri gate.
        tri_gate_min_point = self.tri_gate_array_inst.ll().y - 3*self.m2_pitch
        addr_min_point = self.msf_address_inst.ll().y - 2*self.m2_pitch
        if self.col_addr_size >1:
            decoder_min_point = self.col_decoder_inst.ll().y
        else:
            decoder_min_point = 0
        self.min_point = min(tri_gate_min_point, addr_min_point, decoder_min_point)
        if self.num_banks>1:
            self.min_point -= self.num_control_lines * self.bitcell.height

        # The max point is always the top of the precharge bitlines
        self.max_point = self.precharge_array_inst.uy()

        self.height = self.max_point - self.min_point
        
        # Add an extra gap between the bitcell and the rail
        self.right_vdd_x_offset = self.bitcell_array_inst.ur().x + 3 * drc["minwidth_metal1"]
        offset = vector(self.right_vdd_x_offset, self.min_point)
        self.add_layout_pin(text="vdd",
                            layer="metal1", 
                            offset=offset, 
                            width=self.vdd_rail_width,
                            height=self.height)

        # from the edge of the decoder is another 2 times minwidth metal1
        self.left_vdd_x_offset = min(self.msf_address_inst.ll().x, self.row_decoder_inst.ll().x) - self.vdd_rail_width - 2*drc["minwidth_metal1"]
        offset = vector(self.left_vdd_x_offset, self.min_point)
        self.add_layout_pin(text="vdd",
                            layer="metal1", 
                            offset=offset, 
                            width=self.vdd_rail_width,
                            height=self.height)

        self.gnd_x_offset = self.start_of_right_central_bus - self.gnd_rail_width - self.m2_pitch
        offset = vector(self.gnd_x_offset, self.min_point)
        self.add_layout_pin(text="gnd",
                            layer="metal2", 
                            offset=offset, 
                            width=self.gnd_rail_width,
                            height=self.height)

        self.width = self.right_vdd_x_offset - self.left_vdd_x_offset + self.vdd_rail_width

    def create_central_bus(self):
        """ Create the address, supply, and control signal central bus lines. """

        # Address lines in central line connection are 2*col_addr_size 
        # number of connections for the column mux (for both signal and _bar) and row_addr_size (no _bar) 

        self.central_line_xoffset = {}

        # Control lines (to the right of the GND rail)
        for i in range(self.num_control_lines):
            x_offset = self.start_of_right_central_bus + i * self.m2_pitch
            self.central_line_xoffset[self.control_signals[i]]=x_offset
            # Pins are added later if this is a single bank, so just add rectangle now
            self.add_rect(layer="metal2",  
                          offset=vector(x_offset, self.min_point), 
                          width=self.m2_width, 
                          height=self.height)

        # row address lines (to the left of the column mux or GND rail)
        # goes from 0 down to the min point
        for i in range(self.row_addr_size):
            x_offset = self.start_of_left_central_bus + i * self.m2_pitch
            name = "A[{}]".format(i)
            self.central_line_xoffset[name]=x_offset
            # Add a label pin for LVS correspondence and visual help inspecting the rail.
            self.add_label_pin(text=name,
                               layer="metal2",  
                               offset=vector(x_offset, self.min_point), 
                               width=self.m2_width, 
                               height=-self.min_point)

        # column mux lines if there is column mux [2 or 4 lines] (to the left of the GND rail)
        # goes from 0 down to the min point
        if self.col_addr_size>0:
            for i in range(2**self.col_addr_size):
                x_offset = self.start_of_left_central_bus + (i + self.row_addr_size) * self.m2_pitch
                name = "sel[{}]".format(i)
                self.central_line_xoffset[name]=x_offset
                # Add a label pin for LVS correspondence                
                self.add_label_pin(text=name,
                                   layer="metal2",  
                                   offset=vector(x_offset, self.min_point),
                                   width=self.m2_width, 
                                   height=-self.min_point)

                

            
            

    def route_precharge_to_bitcell_array(self):
        """ Routing of BL and BR between pre-charge and bitcell array """

        for i in range(self.num_cols):
            precharge_bl = self.precharge_array_inst.get_pin("bl[{}]".format(i)).bc()
            precharge_br = self.precharge_array_inst.get_pin("br[{}]".format(i)).bc()
            bitcell_bl = self.bitcell_array_inst.get_pin("bl[{}]".format(i)).uc()
            bitcell_br = self.bitcell_array_inst.get_pin("br[{}]".format(i)).uc()

            self.add_path("metal2",[precharge_bl,bitcell_bl])
            self.add_path("metal2",[precharge_br,bitcell_br])

    def route_sense_amp_to_trigate(self):
        """ Routing of sense amp output to tri_gate input """

        for i in range(self.word_size):
            # Connection of data_out of sense amp to data_ in of msf_data_out
            tri_gate_in = self.tri_gate_array_inst.get_pin("in[{}]".format(i)).bc()
            sa_data_out = self.sense_amp_array_inst.get_pin("data[{}]".format(i)).rc() # rc to get enough overlap

            startY = self.tri_gate_array_inst.ll().y - 2*drc["minwidth_metal3"] + 0.5*drc["minwidth_metal1"]
            start = vector(tri_gate_in.x - 3 * drc["minwidth_metal3"], startY)

            m3_min = vector([drc["minwidth_metal3"]] * 2)
            mid1 = tri_gate_in.scale(1,0) + sa_data_out.scale(0,1) + m3_min.scale(-3, 1)
            mid2 = sa_data_out + m3_min.scale(0.5, 1)
            self.add_path("metal3", [start, mid1, mid2])

            mid3 = [tri_gate_in.x, startY]
            self.add_path("metal2", [start, mid3, tri_gate_in])

            offset = start - vector([0.5*drc["minwidth_metal3"]] * 2)
            self.add_via(("metal2", "via2", "metal3"),offset)

    def route_tri_gate_out(self):
        """ Metal 3 routing of tri_gate output data """
        for i in range(self.word_size):
            tri_gate_out_position = self.tri_gate_array_inst.get_pin("out[{}]".format(i)).ul()
            data_line_position = vector(tri_gate_out_position.x, self.min_point)
            self.add_via(("metal2", "via2", "metal3"), data_line_position)
            self.add_rect(layer="metal3", 
                          offset=data_line_position, 
                          width=drc["minwidth_metal3"], 
                          height=tri_gate_out_position.y - self.min_point)
            self.add_layout_pin(text="DATA[{}]".format(i),
                                layer="metal2", 
                                offset=data_line_position)

    def route_row_decoder(self):
        """ Routes the row decoder inputs and supplies """

        
        for i in range(self.row_addr_size):
            # before this index, we are using 2x4 decoders
            switchover_index = 2*self.decoder.no_of_pre2x4
            # so decide what modulus to perform the height spacing
            if i < switchover_index:
                position_heights = i % 2
            else:
                position_heights = (i-switchover_index) % 3
                
            # Connect the address rails to the decoder
            # Note that the decoder inputs are long vertical rails so spread out the connections vertically.
            decoder_in_position = self.row_decoder_inst.get_pin("A[{}]".format(i)).br() + vector(0,position_heights*self.bitcell.height+self.m2_pitch)
            rail_position = vector(self.central_line_xoffset["A[{}]".format(i)]+drc["minwidth_metal2"],decoder_in_position.y)
            self.add_path("metal1",[decoder_in_position,rail_position])

            decoder_in_via = decoder_in_position - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=decoder_in_via,
                         rotate=90)
            
            contact_offset =  rail_position - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=contact_offset,
                         rotate=90)

        # Route the power and ground, but only BELOW the y=0 since the
        # others are connected with the wordline driver.
        for gnd_pin in self.row_decoder_inst.get_pins("gnd"):
            if gnd_pin.uy()>0:
                continue
            driver_gnd_position = gnd_pin.rc()
            gnd_rail_via = vector(self.gnd_x_offset, driver_gnd_position.y + 0.5*self.m1m2_via.width)            
            gnd_rail_position = vector(self.gnd_x_offset, driver_gnd_position.y)
            self.add_path("metal1", [driver_gnd_position, gnd_rail_position])
            self.add_via(layers=("metal1","via1","metal2"),
                         offset=gnd_rail_via,
                         rotate=270)
                        
        # route the vdd rails
        for vdd_pin in self.row_decoder_inst.get_pins("vdd"):
            if vdd_pin.uy()>0:
                continue
            y_offset = vdd_pin.rc().y
            left_rail_position = vector(self.left_vdd_x_offset, y_offset)
            right_rail_position = vector(self.row_decoder_inst.ur().x, y_offset)
            self.add_path("metal1", [left_rail_position, right_rail_position])

    
    def route_wordline_driver(self):
        """ Connecting Wordline driver output to Bitcell WL connection  """
        
        # we don't care about bends after connecting to the input pin, so let the path code decide.
        for i in range(self.num_rows):
            # The pre/post is to access the pin from "outside" the cell to avoid DRCs
            pre = self.row_decoder_inst.get_pin("decode[{}]".format(i)).lc()
            decoder_out_position = self.row_decoder_inst.get_pin("decode[{}]".format(i)).rc() + vector(0.5*drc["minwidth_metal1"],0)
            driver_in_position = self.wordline_driver_inst.get_pin("in[{}]".format(i)).lc() + vector(0.5*drc["minwidth_metal1"],0)
            post = self.wordline_driver_inst.get_pin("in[{}]".format(i)).rc()
            self.add_path("metal1", [pre, decoder_out_position, driver_in_position, post])

            # The mid guarantees we exit the input cell to the right.
            driver_wl_position = self.wordline_driver_inst.get_pin("wl[{}]".format(i)).rc()
            mid = driver_wl_position + vector(self.m1_pitch,0)            
            bitcell_wl_position = self.bitcell_array_inst.get_pin("wl[{}]".format(i)).lc()
            self.add_path("metal1", [driver_wl_position, mid, bitcell_wl_position])

        # route the gnd rails, add contact to rail as well
        for gnd_pin in self.wordline_driver_inst.get_pins("gnd"):
            driver_gnd_position = gnd_pin.rc()
            right_rail_position = vector(self.bitcell_array_inst.ll().x, driver_gnd_position.y)
            self.add_path("metal1", [driver_gnd_position, right_rail_position])
            gnd_rail_position = vector(self.gnd_x_offset, driver_gnd_position.y + 0.5*self.m1m2_via.width)
            self.add_via(layers=("metal1","via1","metal2"),
                         offset=gnd_rail_position,
                         rotate=270)
                        
        # route the vdd rails
        for vdd_pin in self.wordline_driver_inst.get_pins("vdd"):
            y_offset = vdd_pin.rc().y
            left_rail_position = vector(self.left_vdd_x_offset, y_offset)
            right_rail_position = vector(self.right_vdd_x_offset+self.vdd_rail_width, y_offset)
            self.add_path("metal1", [left_rail_position, right_rail_position])

        

    def route_column_address_lines(self):
        """ Connecting the select lines of column mux to the address bus """
        if not self.col_addr_size>0:
            return

        # Connect the select lines to the column mux
        for i in range(2**self.col_addr_size):
            name = "sel[{}]".format(i)
            col_addr_line_position = self.col_mux_array_inst.get_pin(name).lc()
            wire_offset = vector(self.central_line_xoffset[name]+self.m2_width, col_addr_line_position.y)
            self.add_path("metal1", [col_addr_line_position,wire_offset])
            contact_offset = wire_offset - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=contact_offset,
                         rotate=90)
            
        # Take care of the column address decoder routing
        # If there is a 2:4 decoder for column select lines
        # or TODO 3:8 decoder should work too!
        if self.col_addr_size > 1:

            # connections between outputs of decoder to the extension of
            # main address bus
            for i in range(2**self.col_addr_size):
                name = "sel[{}]".format(i)                
                x_offset = self.central_line_xoffset[name]
                decode_out_position = self.col_decoder_inst.get_pin("out[{}]".format(i)).rc()
                selx_position = vector(self.central_line_xoffset[name]+drc["minwidth_metal2"],decode_out_position.y)
                self.add_path("metal1",[decode_out_position, selx_position])

                # via on end
                decode_out_via = self.col_decoder_inst.get_pin("out[{}]".format(i)).br() 
                selx_via = vector(self.central_line_xoffset[name],decode_out_via.y - drc["minwidth_metal2"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=selx_via) 

            # route the gnd rails, add contact to rail as well
            for gnd_pin in self.col_decoder_inst.get_pins("gnd"):
                driver_gnd_position = gnd_pin.rc()
                right_rail_position = vector(self.gnd_x_offset, driver_gnd_position.y)
                self.add_path("metal1", [driver_gnd_position, right_rail_position])
                gnd_rail_position = vector(self.gnd_x_offset, driver_gnd_position.y + 0.5*self.m1m2_via.width)
                self.add_via(layers=("metal1","via1","metal2"),
                             offset=gnd_rail_position,
                             rotate=270)
                        
            # route the vdd rails
            for vdd_pin in self.col_decoder_inst.get_pins("vdd"):
                y_offset = vdd_pin.rc().y
                left_rail_position = vector(self.left_vdd_x_offset, y_offset)
                right_rail_position = vector(self.gnd_x_offset, y_offset)
                self.add_path("metal1", [left_rail_position, right_rail_position])
                                
            # The connection between last address flops to the input
            # of the column_mux line decoder
            for i in range(self.col_addr_size):                
                ff_index = i + self.row_addr_size
                dout_position = self.msf_address_inst.get_pin("dout[{}]".format(ff_index)).rc()
                in_position = self.col_decoder_inst.get_pin("in[{}]".format(i)).uc()
                mid_position = vector(in_position.x,dout_position.y)
                self.add_path("metal3",[dout_position, mid_position, in_position])

                dout_via = self.msf_address_inst.get_pin("dout[{}]".format(ff_index)).br()
                in_via = self.col_decoder_inst.get_pin("in[{}]".format(i)).ul()
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=dout_via,
                             rotate=90)
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=in_via)
                



                
                
        # if there are only two column select lines we just connect the dout_bar of the last FF 
        # to only select line and dout of that FF to the other select line
        elif self.col_addr_size == 1:

            dout_bar_position = self.msf_address_inst.get_pin("dout_bar[{}]".format(self.row_addr_size)).rc()
            sel0_position = vector(self.central_line_xoffset["sel[0]"]+drc["minwidth_metal2"],dout_bar_position.y)
            self.add_path("metal1",[dout_bar_position, sel0_position])
            
            # two vias on both ends
            dout_bar_via = dout_bar_position + vector(self.m1m2_via.height,-0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=dout_bar_via,
                         rotate=90)
            sel0_via = sel0_position - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=sel0_via,
                         rotate=90) 

            dout_position = self.msf_address_inst.get_pin("dout[{}]".format(self.row_addr_size)).rc()
            sel1_position = vector(self.central_line_xoffset["sel[1]"]+drc["minwidth_metal2"],dout_position.y)
            self.add_path("metal1",[dout_position, sel1_position])
            # two vias on both ends
            dout_via = dout_position + vector(self.m1m2_via.height,-0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=dout_via,
                         rotate=90)
            sel1_via = sel1_position - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=sel1_via,
                         rotate=90)

            
    def route_msf_address(self):
        """ Routing the row address lines from the address ms-flop array to the row-decoder  """

        # Create the address input pins
        for i in range(self.addr_size):
            msf_din_position = self.msf_address_inst.get_pin("din[{}]".format(i)).ll()
            address_position = vector(self.left_vdd_x_offset, msf_din_position.y)
            self.add_layout_pin(text="ADDR[{}]".format(i),
                                layer="metal2", 
                                offset=address_position, 
                                width=msf_din_position.x - self.left_vdd_x_offset, 
                                height=drc["minwidth_metal2"])

        for i in range(self.row_addr_size):

            # Connect the ff outputs to the rails
            dout_position = self.msf_address_inst.get_pin("dout[{}]".format(i)).rc()
            rail_position = vector(self.central_line_xoffset["A[{}]".format(i)]+drc["minwidth_metal2"],dout_position.y)
            self.add_path("metal1",[dout_position, rail_position])
            dout_via = self.msf_address_inst.get_pin("dout[{}]".format(i)).br() + vector(self.m1m2_via.height,0)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=dout_via,
                         rotate=90)
            contact_offset = rail_position - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=contact_offset,
                         rotate=90)

        # Connect address FF gnd
        for gnd_pin in self.msf_address_inst.get_pins("gnd"):
            if gnd_pin.layer != "metal2":
                continue
            gnd_via = gnd_pin.br() + vector(self.m1m2_via.height,0)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=gnd_via, 
                         rotate=90)
            gnd_offset = gnd_pin.rc()
            rail_offset = vector(self.gnd_x_offset+self.m1m2_via.height,gnd_offset.y)
            self.add_path("metal1",[gnd_offset,rail_offset])
            rail_via = rail_offset - vector(0,0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=rail_via,
                         rotate=90)
            
        # Connect address FF vdd
        for vdd_pin in self.msf_address_inst.get_pins("vdd"):
            if vdd_pin.layer != "metal1":
                continue
            vdd_offset = vdd_pin.bc()
            mid = vector(vdd_offset.x, vdd_offset.y - self.m1_pitch)
            rail_offset = vector(self.left_vdd_x_offset, mid.y)
            self.add_path("metal1", [vdd_offset,mid,rail_offset])

    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # Add the wordline names
        for i in range(self.num_rows):
            wl_name = "wl[{}]".format(i)
            wl_pin = self.bitcell_array_inst.get_pin(wl_name)
            self.add_label(text=wl_name,
                           layer="metal1",  
                           offset=wl_pin.ll())
        
        # Add the bitline names
        for i in range(self.num_cols):
            bl_name = "bl[{}]".format(i)
            br_name = "br[{}]".format(i)
            bl_pin = self.bitcell_array_inst.get_pin(bl_name)
            br_pin = self.bitcell_array_inst.get_pin(br_name)
            self.add_label(text=bl_name,
                           layer="metal2",  
                           offset=bl_pin.ll())
            self.add_label(text=br_name,
                           layer="metal2",  
                           offset=br_pin.ll())

        # Add the data input names to the data flop output
        for i in range(self.word_size):
            dout_name = "dout[{}]".format(i)
            dout_pin = self.msf_data_in_inst.get_pin(dout_name)
            self.add_label(text="data_in[{}]".format(i),
                           layer="metal2",  
                           offset=dout_pin.ll())

        # Add the data output names to the sense amp output     
        for i in range(self.word_size):
            data_name = "data[{}]".format(i)
            data_pin = self.sense_amp_array_inst.get_pin(data_name)
            self.add_label(text="data_out[{}]".format(i),
                           layer="metal2",  
                           offset=data_pin.ll())
            
            
    def route_control_lines(self):
        """ Rout the control lines of the entire bank """
        
        # Make a list of tuples that we will connect.
        # From control signal to the module pin 
        # Connection from the central bus to the main control block crosses
        # pre-decoder and this connection is in metal3
        connection = []
        if self.num_banks>1:
            prefix="gated_"
        else:
            prefix=""
        connection.append((prefix+"clk_bar", self.msf_data_in_inst.get_pin("clk").lc()))
        connection.append((prefix+"tri_en_bar", self.tri_gate_array_inst.get_pin("en_bar").lc()))
        connection.append((prefix+"tri_en", self.tri_gate_array_inst.get_pin("en").lc()))
        connection.append((prefix+"clk_bar", self.precharge_array_inst.get_pin("en").lc()))
        connection.append((prefix+"w_en", self.write_driver_array_inst.get_pin("en").lc()))
        connection.append((prefix+"s_en", self.sense_amp_array_inst.get_pin("en").lc()))
  
        for (control_signal, pin_position) in connection:
            control_x_offset = self.central_line_xoffset[control_signal] + self.m2_width
            control_position = vector(control_x_offset, pin_position.y)
            self.add_path("metal1", [control_position, pin_position])
            via_offset = vector(control_x_offset, pin_position.y - 0.5*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=via_offset,
                         rotate=90)

        # clk to msf address
        control_signal = prefix+"clk"
        pin_position = self.msf_address_inst.get_pin("clk").uc()
        mid_position = pin_position + vector(0,self.m1_pitch)
        control_x_offset = self.central_line_xoffset[control_signal]
        control_position = vector(control_x_offset + drc["minwidth_metal1"], mid_position.y)
        self.add_path("metal1",[pin_position, mid_position, control_position])
        control_via_position = vector(control_x_offset, mid_position.y-0.5*drc["minwidth_metal2"])        
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=control_via_position)

        # clk to wordline_driver
        control_signal = prefix+"clk"
        pin_position = self.wordline_driver_inst.get_pin("en").uc()
        mid_position = pin_position + vector(0,self.m1_pitch)
        control_x_offset = self.central_line_xoffset[control_signal]
        control_position = vector(control_x_offset + drc["minwidth_metal1"], mid_position.y)
        self.add_wire(("metal1","via1","metal2"),[pin_position, mid_position, control_position])
        control_via_position = vector(control_x_offset, mid_position.y-0.5*drc["minwidth_metal2"])        
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=control_via_position)
        


    def route_bank_select(self):
        """ Route array of or gates to gate the control signals in case 
            of multiple banks are created in upper level SRAM module """
        return
        bank_select_line_xoffset = (self.bank_select_or_position.x 
                                        - 3*drc["minwidth_metal2"])
        self.add_rect(layer="metal2", 
                      offset=[bank_select_line_xoffset, 
                              self.bank_select_or_position.y], 
                      width=drc["minwidth_metal2"],  
                      height=self.num_control_lines*self.inv.height)
        
        # bank select inverter routing
        # output side
        start = self.bank_select_inv_position +  self.inv4x.Z_position
        end = self.bank_select_or_position + self.nor2.B_position
        mid = vector(start.x, end.y)
        self.add_path("metal1", [start, mid, end])
        
        # input side
        start = self.bank_select_inv_position + self.inv4x.A_position
        end = vector(self.left_vdd_x_offset, start.y + 3 * drc["minwidth_metal3"])
        mid = vector(start.x, end.y)
        self.add_wire(("metal2", "via1", "metal1"), [start, mid, end])

        # save position
        self.bank_select_position = end - vector(0, 0.5 * drc["minwidth_metal2"])
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.bank_select_position)

        x_offset = (self.bank_select_or_position.x + self.nor2.width
                        + self.inv4x.width - drc["minwidth_metal1"])
        for i in range(self.num_control_lines):
            base = self.bank_select_or_position.y + self.inv.height * i
            if(i % 2):
                Z_y_offset = (base + self.inv.height - self.inv4x.Z_position.y 
                                - drc["minwidth_metal1"])
                B_y_offset = (base + self.inv.height - self.nor2.B_position.y 
                              - 0.5 * drc["minwidth_metal1"])
                A_y_offset = (base + self.inv.height - self.nor2.A_position.y 
                              - 0.5 * drc["minwidth_metal1"])
            else:
                Z_y_offset = (base + self.inv4x.Z_position.y)
                B_y_offset = (base + self.nor2.B_position.y 
                                  - 0.5 * drc["minwidth_metal1"])
                A_y_offset = (base + self.nor2.A_position.y  
                                  + 0.5 * drc["minwidth_metal1"]
                                  - self.m1m2_via.width)

            # output
            self.add_rect(layer="metal3", 
                          offset=[x_offset, Z_y_offset], 
                          width=self.central_line_xoffset[i] - x_offset,  
                          height=drc["minwidth_metal3"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=[x_offset, Z_y_offset])
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=[x_offset, Z_y_offset])
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=[self.central_line_xoffset[i], Z_y_offset])

            # B_input
            if i != 5:
                self.add_rect(layer="metal1", 
                              offset=[bank_select_line_xoffset, B_y_offset], 
                              width=(self.bank_select_or_position.x 
                                         - bank_select_line_xoffset),  
                              height=drc["minwidth_metal1"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[bank_select_line_xoffset, B_y_offset])

            # A_input
            if i != 3:
                self.add_rect(layer="metal3", 
                              offset=[self.left_vdd_x_offset, A_y_offset], 
                              width=(self.bank_select_or_position.x
                                         - self.left_vdd_x_offset),  
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                              offset=[self.bank_select_or_position.x
                                          + drc["minwidth_metal1"],
                                      A_y_offset], 
                              rotate=90)
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=[self.bank_select_or_position.x 
                                         + drc["minwidth_metal1"],
                                     A_y_offset], 
                             rotate=90)
            else:
                # connect A to last A, both are tri_en_bar
                via_offset = vector(self.bank_select_or_position.x 
                                        + drc["minwidth_metal1"], 
                                    A_y_offset)
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=via_offset,
                             rotate=90)
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=via_offset, 
                             rotate=90)

                start = via_offset + vector(0, 0.5 * self.m1m2_via.width)
                mid = [self.left_vdd_x_offset - self.left_vdd_x_offset 
                           - drc["minwidth_metal2"] - drc["metal2_to_metal2"] 
                           + bank_select_line_xoffset,
                       start.y]
                correct_y = (2 * self.nor2.A_position.y + drc["minwidth_metal1"]
                                 - self.m1m2_via.width)
                end = start +  vector(0, correct_y)
                self.add_wire(("metal3", "via2", "metal2"), [start, mid, end])

            # Save position
            setattr(self,"{0}_position".format(self.control_signals[i]),
                    [self.left_vdd_x_offset, A_y_offset])

    def route_vdd_supply(self):
        """ Route vdd for the precharge, sense amp, write_driver, data FF, tristate """

        for inst in [self.precharge_array_inst, self.sense_amp_array_inst,
                     self.write_driver_array_inst, self.msf_data_in_inst,
                     self.tri_gate_array_inst]:
            for vdd_pin in inst.get_pins("vdd"):
                self.add_rect(layer="metal1", 
                              offset=vdd_pin.ll(), 
                              width=self.right_vdd_x_offset - vdd_pin.lx(), 
                              height=drc["minwidth_metal1"])

        return

        # Connect bank_select_and2_array vdd
        if(self.num_banks > 1):
            for i in range(self.num_control_lines):
                if(i % 2):
                    self.add_rect(layer="metal1", 
                                  offset=[self.left_vdd_x_offset,
                                          self.bank_select_or_position.y
                                              + i * self.inv.height
                                              - 0.5 * drc["minwidth_metal1"]], 
                                  width=(self.bank_select_or_position.x
                                             - self.left_vdd_x_offset),  
                                  height=drc["minwidth_metal1"])

    def route_gnd_supply(self):
        """ Route gnd for the precharge, sense amp, write_driver, data FF, tristate """
        # precharge is connected by abutment
        for inst in [ self.tri_gate_array_inst, self.sense_amp_array_inst, self.msf_data_in_inst, self.write_driver_array_inst]:
            for gnd_pin in inst.get_pins("gnd"):
                if gnd_pin.layer != "metal1":
                    continue
                # route to the right hand side of the big rail to reduce via overlaps
                pin_position = gnd_pin.lc()
                gnd_offset = vector(self.gnd_x_offset+self.gnd_rail_width, pin_position.y)
                self.add_path("metal1", [gnd_offset, pin_position])
                contact_offset = gnd_offset - vector(0,0.5*drc["minwidth_metal2"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=contact_offset,
                             rotate=90)

        
        # Connect bank_select_or2_array gnd
        if(self.num_banks > 1):
            return
            self.bank_select_inv_position
            self.add_rect(layer="metal1", 
                          offset=(self.bank_select_inv_position
                                       + self.inv4x.gnd_position), 
                          width=(self.bank_select_or_position.x
                                     - self.bank_select_inv_position.x),  
                          height=drc["minwidth_metal1"])

            x_offset = (self.bank_select_or_position.x 
                            + self.nor2.width + self.inv4x.width)
            for i in range(self.num_control_lines):
                if(i % 2 == 0):
                    y_offset = self.bank_select_or_position.y + i*self.inv.height \
                        - 0.5*drc["minwidth_metal1"]
                    #both M1 & M2 are horizontal, cannot be  replaced with wire
                    self.add_rect(layer="metal1", 
                                  offset=[x_offset,  y_offset], 
                                  width=drc["minwidth_metal1"],  
                                  height=drc["minwidth_metal1"])
                    self.add_rect(layer="metal2", 
                                  offset=[x_offset,  y_offset], 
                                  width=self.left_gnd_x_offset \
                                      - x_offset + self.power_rail_width,  
                                  height=drc["minwidth_metal2"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                 offset=[x_offset + drc["minwidth_metal1"],  
                                         y_offset], 
                                 rotate=90)

    def add_control_pins(self):
        """ Add the control signal input pins """

        for ctrl in self.control_signals:
            x_offset = self.central_line_xoffset[ctrl]
            self.add_layout_pin(text=ctrl,
                                layer="metal2",  
                                offset=vector(x_offset, self.min_point), 
                                width=self.m2_width, 
                                height=self.height)


    def connect_rail_from_right(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pin = inst.get_pin(pin).lc()
        rail_position = vector(self.rail_1_x_offsets[rail], in_pin.y)
        self.add_wire(("metal3","via2","metal2"),[in_pin, rail_position, rail_position - vector(0,self.m2_pitch)])
        # Bring it up to M2 for M2/M3 routing
        self.add_via(layers=("metal1","via1","metal2"),
                     offset=in_pin + self.m1m2_via_offset,
                     rotate=90)
        self.add_via(layers=("metal2","via2","metal3"),
                     offset=in_pin + self.m2m3_via_offset,
                     rotate=90)
        
        
    def connect_rail_from_left(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pin = inst.get_pin(pin).rc()
        rail_position = vector(self.rail_1_x_offsets[rail], in_pin.y)
        self.add_wire(("metal3","via2","metal2"),[in_pin, rail_position, rail_position - vector(0,self.m2_pitch)])
        self.add_via(layers=("metal1","via1","metal2"),
                     offset=in_pin + self.m1m2_via_offset,
                     rotate=90)
        self.add_via(layers=("metal2","via2","metal3"),
                     offset=in_pin + self.m2m3_via_offset,
                     rotate=90)
        
    def delay(self, slew, load):
        """ return  analytical delay of the bank"""
        msf_addr_delay = self.msf_address.delay(slew, self.decoder.input_load())

        decoder_delay = self.decoder.delay(msf_addr_delay.slew, self.wordline_driver.input_load())

        word_driver_delay = self.wordline_driver.delay(decoder_delay.slew, self.bitcell_array.input_load())

        bitcell_array_delay = self.bitcell_array.delay(word_driver_delay.slew)

        bl_t_data_out_delay = self.sense_amp_array.delay(bitcell_array_delay.slew,
                                                        self.bitcell_array.output_load())
        # output load of bitcell_array is set to be only small part of bl for sense amp.

        data_t_DATA_delay = self.tri_gate_array.delay(bl_t_data_out_delay.slew, load)

        result = msf_addr_delay + decoder_delay + word_driver_delay \
                 + bitcell_array_delay + bl_t_data_out_delay + data_t_DATA_delay
        return result
