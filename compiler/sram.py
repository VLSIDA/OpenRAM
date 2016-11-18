import math
import sys
from tech import drc, spice
import debug
import design
from math import log,sqrt,ceil
from contact import contact
from bank import bank
import datetime
import getpass
from vector import vector
from globals import OPTS


class sram(design.design):
    """
    Dynamically generated SRAM by connecting banks to control logic. The
    number of banks should be 1 , 2 or 4
    """

    def __init__(self, word_size, num_words, num_banks, name):
        mod_list = ["control_logic", "ms_flop_array", "ms_flop", "bitcell"]
        for mod_name in mod_list:
            config_mod_name = getattr(OPTS.config, mod_name)
            class_file = reload(__import__(config_mod_name))
            mod_class = getattr(class_file , config_mod_name)
            setattr (self, "mod_"+mod_name, mod_class)


        self.ms_flop_chars = self.mod_ms_flop.chars
        self.bitcell_chars = self.mod_bitcell.chars

        self.word_size = word_size
        self.num_words = num_words
        self.num_banks = num_banks

        debug.info(2, "create sram of size {0} with {1} num of words".format(self.word_size, 
                                                                             self.num_words))

        design.design.__init__(self, name)
        self.ctrl_positions = {}

        self.compute_sizes()
        self.add_pins()

        self.create_layout()
        self.DRC_LVS()

    def compute_sizes(self):
        """  Computes the required sizes to create the memory """
        self.check_num_banks(self.num_banks)

        self.num_words_per_bank = self.num_words/self.num_banks
        self.num_bits_per_bank = self.word_size*self.num_words_per_bank

        self.bank_area = self.bitcell_chars["width"]*\
            self.bitcell_chars["height"]*self.num_bits_per_bank
        self.bank_side_length = math.sqrt(self.bank_area)

        self.tentative_num_cols = int(self.bank_side_length/self.bitcell_chars["width"])
        self.words_per_row = self.cal_words_per_row(self.tentative_num_cols,
                                                            self.word_size)
        self.tentative_num_rows = self.num_bits_per_bank \
            /(self.words_per_row \
                  *self.word_size)
        self.words_per_row = self.amend_words_per_row(self.tentative_num_rows,
                                                              self.words_per_row)
        
        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words_per_bank/self.words_per_row
        
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size \
            + self.row_addr_size
        self.addr_size = self.bank_addr_size + \
            int(math.log(self.num_banks, 2))
        
        self.control_size = 6

        self.bank_to_bus_distance = 5*drc["minwidth_metal3"]

    def check_num_banks(self,num_banks):
        if(num_banks != 1 and num_banks != 2 and num_banks != 4):
            debug.error("Valid number of banks are 1 , 2 and 4.")
            sys.exit(-1)

    def cal_words_per_row(self,tentative_num_cols, word_size):
        if(tentative_num_cols < 1.5*word_size):
            words_per_row = 1
        elif(tentative_num_cols > 3*word_size):
            words_per_row = 4
        else:
            words_per_row = 2
        return words_per_row

    def amend_words_per_row(self,tentative_num_rows, words_per_row):
        if(tentative_num_rows > 512):
            if(tentative_num_rows*words_per_row > 2048):
                debug.error("Number of rows exceeds 512")
                sys.exit(-1)
            words_per_row = words_per_row*tentative_num_rows/512

        if(tentative_num_rows < 16):
            if(tentative_num_rows*words_per_row < 16):
                debug.error("minimum number of rows is 16, but given {0}".format(
                    tentative_num_rows))
                sys.exit(-1)
            words_per_row = words_per_row*tentative_num_rows/16
        return words_per_row

    def add_pins(self):
        """ app pins """
        for i in range(self.word_size):
            self.add_pin("DATA[{0}]".format(i))
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i))
        for pin in ["CSb","WEb","OEb",
                    "clk","vdd","gnd"]:
            self.add_pin(pin)

    def create_layout(self):
        """ Layout creation """
        self.create_modules()
        self.add_modules()
        self.add_routing()

    def add_routing(self):
        """ Route all of the modules """
        if (self.num_banks == 2 or self.num_banks == 4):
            self.route_2or4_banks()
        if (self.num_banks == 4):
            self.route_4_banks()
        self.route_bank_and_control()
        self.route_supplies()

    def create_multibank_modules(self):
        """ Add the multibank address flops and bank decoder """
        self.msf_msb_address = self.mod_ms_flop_array(name="msf_msb_address",
                                                      array_type="address",
                                                      columns=self.num_banks/2,
                                                      word_size=self.num_banks/2)
        self.add_mod(self.msf_msb_address)
        
        self.msb_decoder = self.bank.decoder.pre2_4
        self.add_mod(self.msb_decoder)

    def create_modules(self):
        """ Create all the modules that will be used """

        # Create the control logic module
        self.control = self.mod_control_logic(num_rows=self.num_rows)
        self.add_mod(self.control)

        # Create the bank module (up to four are instantiated)
        self.bank = bank(word_size=self.word_size,
                         num_words=self.num_words_per_bank,
                         words_per_row=self.words_per_row,
                         num_banks=self.num_banks,
                         name="test_bank1")
        self.add_mod(self.bank)

        # Conditionally create the 
        if(self.num_banks > 1):
            self.create_multibank_modules()

        # These aren't for instantiating, but we use them to get the dimensions
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.m2m3_via = contact(layer_stack=("metal2", "via2", "metal3"))

        self.bank_count = 0

        self.sram_property = ["bank_clk_positions",
                              "bank_clk_bar_positions",
                              "bank_tri_en_positions",
                              "bank_tri_en_bar_positions",
                              "bank_w_en_positions",
                              "bank_s_en_positions"]
        self.bank_property = ["clk_position",
                              "clk_bar_position",
                              "tri_en_position",
                              "tri_en_bar_position",
                              "w_en_position",
                              "s_en_position", ]

        self.bank_positions = []

        self.bank_clk_positions = []
        self.bank_clk_bar_positions = []
        self.bank_tri_en_positions = []
        self.bank_tri_en_bar_positions = []
        self.bank_w_en_positions = []
        self.bank_s_en_positions = []

        # SRAM bank address 3D array
        # 2 keys will return a x,y position pair
        # example key1 = bank_index , key2 = addr_line_index will return [x,y]
        self.sram_bank_adress_positions = []

        # SRAM data lines 3D array
        # 2 keys will return a x,y position pair
        # example key1 = bank_index , key2 = data_line_index will return [x,y]
        self.sram_bank_data_positions = []

        # 2D array for bank_select position of banks
        self.sram_bank_select_positions = []

        # Bank power rail positions
        self.sram_bank_right_vdd_positions = []
        self.sram_bank_left_vdd_positions = []
        self.sram_bank_left_gnd_positions = []

        self.power_rail_width = self.bank.power_rail_width
        self.sram_power_rail_gap = 4*self.power_rail_width

        self.vdd_position = vector(0, 2*self.power_rail_width)
        self.gnd_position = vector(0, 0)



    def add_bank(self, position, x_flip, y_flip):
        """ add and place bank. All the pin position is also
        translated and saved for later use"""

        # x_flip ==  1 --> no flip in x_axis
        # x_flip == -1 --> flip in x_axis
        # y_flip ==  1 --> no flip in y_axis
        # y_flip == -1 --> flip in y_axis

        # x_flip and y_flip are used for position translation

        bank_rotation = 180 if (x_flip == -1 and y_flip == -1) else 0
        bank_mirror = "R0"

        if(x_flip == y_flip):
            bank_mirror = "R0"
        elif(x_flip == -1):
            bank_mirror = "MX"
        elif(y_flip == -1):
            bank_mirror = "MY"

        yMetalShift = drc["minwidth_metal3"] if (x_flip == -1) else 0
        xMetalShift = drc["minwidth_metal3"] if (y_flip == -1) else 0

        position=vector(position)
        self.add_inst(name="bank{0}".format(self.bank_count),
                      mod=self.bank,
                      offset=position,
                      mirror=bank_mirror,
                      rotate=bank_rotation)
        self.bank_positions.append(position)

        temp = []
        for i in range(self.word_size):
            temp.append("DATA[{0}]".format(i))
        for i in range(self.bank_addr_size):
            temp.append("ADDR[{0}]".format(i))
        if(self.num_banks > 1):
            temp.append("bank_select[{0}]".format(self.bank_count))
        temp = temp + ["s_en"   , "w_en", "tri_en_bar", "tri_en",
                       "clk_bar", "clk" , "vdd"       , "gnd"   ]
        self.connect_inst(temp)

        # Saving control line properties
        for i in range(len(self.sram_property)):
            sub_mod_offset = getattr(self.bank,self.bank_property[i])
            new=(position + vector(y_flip,x_flip).scale(sub_mod_offset) 
                     - vector(xMetalShift,yMetalShift))

            pos_list=getattr(self,self.sram_property[i])
            if pos_list is None:
                pos_list=[]
            pos_list.append(new)
            setattr(self,self.sram_property[i],pos_list)

        # Address input lines
        bank_address_positions = []
        for addr_position in self.bank.address_positions:
            new=(position + vector(y_flip,x_flip).scale(addr_position) 
                     - vector(xMetalShift,yMetalShift))
            bank_address_positions.append(new)
        self.sram_bank_adress_positions.append(bank_address_positions)

        # Bank select
        if (self.num_banks > 1):
            new=(position + vector(y_flip,x_flip).scale(self.bank.bank_select_position) 
                     - vector(xMetalShift,yMetalShift))
            self.sram_bank_select_positions.append(new)

        # Data input lines
        bank_data_positions = []
        for data_position in self.bank.data_positions:
            new=(position + vector(y_flip,x_flip).scale(data_position) 
                     - vector(xMetalShift,yMetalShift))
            bank_data_positions.append(new)
        self.sram_bank_data_positions.append(bank_data_positions)

        # VDD rails

        yPowerShift = self.power_rail_width if(x_flip == -1) else 0
        xPowerShift = self.power_rail_width if(y_flip == -1) else 0

        # Right vdd
        new=(position + vector(y_flip,x_flip).scale(self.bank.right_vdd_position) 
                 - vector(xPowerShift,yPowerShift))
        self.sram_bank_right_vdd_positions.append(new)
        # left vdd
        new=(position + vector(y_flip,x_flip).scale(self.bank.left_vdd_position) 
                 - vector(xPowerShift,yPowerShift))
        self.sram_bank_left_vdd_positions.append(new)
        # left gnd
        new=(position + vector(y_flip,x_flip).scale(self.bank.left_gnd_position) 
                 - vector(xPowerShift,yPowerShift))
        self.sram_bank_left_gnd_positions.append(new)

        self.bank_count = self.bank_count + 1

    # FIXME: This should be in geometry.py or it's own class since it is
    # reusable
    def create_bus(self, layer, offset, bits, height, rotate):
        """ Create a bus and place it according to rotate and
        return an array of line positions """

        minwidth = "minwidth_{0}".format(layer)
        m2m = "{0}_to_{0}".format(layer)
        line_width = drc[minwidth]
        line_gap = 2*drc[m2m]

        line_positions = []
        bus_width = bits*(line_width + line_gap)
        if(rotate == 0):
            for i in range(bits):
                line_offset = offset + vector(i*(line_width + line_gap),0)
                self.add_rect(layer=layer,
                              offset=line_offset,
                              width=line_width,
                              height=height)
                line_positions.append(line_offset)
        elif(rotate == 270):
            for i in range(bits):
                line_offset = offset - vector(0, (i+1)*line_width + i*line_gap)
                self.add_rect(layer=layer,
                              offset=line_offset,  
                              width=height,
                              height=line_width)
                line_positions.append(line_offset)
        else:
            debug.error("Unimplemented rotation for create_bus")

        return line_positions

    def calculate_bus_width(self, layer, bits):
        """ Calculate the bus width """
        minwidth = "minwidth_{0}".format(layer)
        m2m = "{0}_to_{0}".format(layer)
        line_width = drc[minwidth]
        line_gap = 2*drc[m2m]
        return bits*(line_width + line_gap) - line_gap

    def add_control_logic(self, position, mirror):
        """ Add and place control logic """
        self.control_position = position
        self.add_inst(name="control",
                      mod=self.control,
                      offset=self.control_position,
                      mirror=mirror)
        temp = ["CSb", "WEb",  "OEb", "s_en", "w_en", "tri_en",
                "tri_en_bar", "clk_bar", "clk", "vdd", "gnd"]
        self.connect_inst(temp)

    def add_singlebank_modules(self):
        """ This adds the moduels for a single bank SRAM with control
        logic. """
        self.add_bank([0, 0], 1, 1)
        # FIXME: document
        loc = vector(- 2 * drc["minwidth_metal3"],
                     self.bank_positions[0].y + self.bank.decoder_position.y
                         + 2 * drc["minwidth_metal3"])
        self.add_control_logic(loc, "R90")

        self.width = self.bank.width + self.control.height + 2*drc["minwidth_metal3"]
        self.height = self.bank.height
        self.control.CSb_position.rotate_scale(-1,1)
        self.CSb_position = (self.control.CSb_position.rotate_scale(-1,1)
                                +self.control_position)
        self.OEb_position = (self.control.OEb_position.rotate_scale(-1,1)
                                +self.control_position)
        self.WEb_position = (self.control.WEb_position.rotate_scale(-1,1)
                                +self.control_position)
        self.clk_position = (self.control.clk_position.rotate_scale(-1,1)
                                +self.control_position)
        for i in range(0, self.word_size):
            self.add_label(text="DATA[{0}]".format(i),
                           layer="metal3",
                           offset=self.bank.data_positions[i])

    def add_multibank_modules(self):
        """ This creates either a 2 or 4 bank SRAM with control logic
        and bank selection logic."""

        self.bank_h = self.bank.height
        self.bank_w = self.bank.width

        self.num_vertical_line = self.bank_addr_size + self.control_size \
            + self.num_banks + self.num_banks/2
        self.num_horizontal_line = self.word_size

        self.vertical_bus_width = self.calculate_bus_width("metal2",
                                                           self.num_vertical_line)
        self.horizontal_bus_width = self.calculate_bus_width("metal3",
                                                             self.num_horizontal_line)

        self.vertical_bus_height = (self.num_banks/2)*(self.bank_h + self.bank_to_bus_distance) \
            + self.horizontal_bus_width
        self.horizontal_bus_height = (2 * (self.bank_w + self.bank_to_bus_distance)
                                          + self.vertical_bus_width)

        self.vertical_bus_offset = vector(self.bank_w + self.bank_to_bus_distance,
                                          self.sram_power_rail_gap)
        self.horizontal_bus_offset = vector(0,
                                            self.bank_h + self.bank_to_bus_distance
                                                + self.sram_power_rail_gap 
                                                + self.horizontal_bus_width)
                                      
        # Vertical bus
        self.vertical_line_positions = self.create_bus(layer="metal2",
                                                       offset=self.vertical_bus_offset,
                                                       bits=self.num_vertical_line,
                                                       height=self.vertical_bus_height,
                                                       rotate=0)
        
        # Horizontal bus
        self.horizontal_line_positions = self.create_bus(layer="metal3",
                                                         offset=self.horizontal_bus_offset,
                                                         bits=self.num_horizontal_line,
                                                         height=self.horizontal_bus_height,
                                                         rotate=270)
        for i in range(0, self.word_size):
            self.add_label(text="DATA[{0}]".format(i),
                           layer="metal3",
                           offset=self.horizontal_line_positions[i])

        self.width = 2*(self.bank_w + self.bank_to_bus_distance) + self.vertical_bus_width
        self.height = (self.num_banks/2)*(self.bank_h + self.bank_to_bus_distance) \
            + self.horizontal_bus_width + self.sram_power_rail_gap

        # Add Control logic for Bank = 2 and Bank =4

        control_bus_width = self.calculate_bus_width("metal1",
                                                     self.control_size + 2)
        control_bus_height = (self.vertical_line_positions[self.control_size - 1].x
                                  + drc["minwidth_metal2"])

        control_bus_offset = vector(0, self.height + control_bus_width 
                                           + 4*drc["minwidth_metal3"])
        self.control_bus_line_positions = self.create_bus(layer="metal1",
                                                          offset=control_bus_offset,
                                                          bits=self.control_size + 2,
                                                          height=control_bus_height,
                                                          rotate=270)

        if (self.num_banks == 2):
            self.control_position = vector(0, control_bus_offset.y 
                                                  + self.ms_flop_chars["width"])
            self.add_control_logic(self.control_position, "R0")

            self.CSb_position = self.control_position + self.control.CSb_position
            self.OEb_position = self.control_position + self.control.OEb_position
            self.WEb_position = self.control_position + self.control.WEb_position
            self.clk_position = self.control_position + self.control.clk_position
            # Max point
            self.max_point = self.control_position.y + self.ms_flop_chars["width"]

        # MSB address
        x_off = (self.bank_w + self.vertical_bus_width 
                     + 2 * self.bank_to_bus_distance
                     + self.power_rail_width 
                     + 4 * drc["minwidth_metal3"])
        y_off = self.height + 2 * self.ms_flop_chars["width"] + 4 * drc["minwidth_metal3"]
        self.msf_msb_address_position = vector(x_off, y_off)
        self.add_inst(name="msf_msb_address",
                      mod=self.msf_msb_address,
                      offset=self.msf_msb_address_position,
                      mirror="RO",
                      rotate=270)
        
        temp = []
        for i in range(self.num_banks/2):
            temp.append("ADDR[{0}]".format(self.bank.addr_size + i))
        if(self.num_banks == 4):
            for i in range(self.num_banks/2):
                temp.append("msb{0}".format(i))
                temp.append("msb{0}_bar".format(i))
        else:
            temp = temp + ["bank_select[1]", "bank_select[0]"]
        temp = temp + ["clk", "vdd", "gnd"]
        self.connect_inst(temp)

        self.add_banks_0and1()

        if (self.num_banks == 4):
            self.add_banks_2and3()

        # Extension of Vertical Rail
        self.create_bus(layer="metal2", 
                        offset=[self.vertical_bus_offset.x,
                                self.height],
                        bits=self.num_vertical_line,
                        height=self.max_point - self.height,
                        rotate=0)

        # Add ADDRESS labels to vertical line
        for i in range(self.addr_size - int(math.log(self.num_banks, 2))):
            index = self.control_size + int(math.log(self.num_banks, 2)) + i
            self.add_label(text="ADDR[{}]".format(i),
                           layer="metal2",
                           offset=[self.vertical_line_positions[index].x,
                                   self.max_point])

        for i in range(int(math.log(self.num_banks, 2))):
            self.add_label(text="ADDR[{}]".format(self.addr_size - i - 1),
                           layer="metal2",
                           offset=[self.vertical_line_positions[self.control_size + i].x,
                                   self.max_point])

    def add_modules(self):
        """ add all the modules """
        if (self.num_banks == 1):
            self.add_singlebank_modules()
        elif (self.num_banks == 2 or self.num_banks == 4):
            self.add_multibank_modules()

        self.add_labels()

    def add_banks_0and1(self):
        # Placement of bank 0
        self.bank_position_0 = vector(self.bank_w,
                                      self.bank_h + self.sram_power_rail_gap)
        self.add_bank(self.bank_position_0, -1, -1)

        # Placement of bank 1
        x_off = self.bank_w + self.vertical_bus_width + 2*self.bank_to_bus_distance
        self.bank_position_1 = vector(x_off, self.bank_position_0.y)
        self.add_bank(self.bank_position_1, -1, 1)

    def add_banks_2and3(self):
        # Placement of bank 2
        y_off = (self.bank_h + self.horizontal_bus_width 
                     +2 * self.bank_to_bus_distance 
                     + self.sram_power_rail_gap)
        bank_position_2 = vector(self.bank_position_0.x, y_off)
        self.add_bank(bank_position_2, 1, -1)

        # Placement of bank 3
        bank_position_3 = vector(self.bank_position_1.x, bank_position_2.y)
        self.add_bank(bank_position_3, 1, 1)
        
        self.msb_decoder_position = vector(bank_position_3.x + self.power_rail_width 
                                               + 4 * drc["minwidth_metal3"] 
                                               + self.msb_decoder.width,
                                           self.msf_msb_address_position.y 
                                               + 4 * drc["minwidth_metal3"])

        self.add_inst(name="msb_decoder",
                      mod=self.msb_decoder,
                      offset=self.msb_decoder_position,
                      mirror="MY")
        temp = ["msb0", "msb1", "bank_select[{0}]".format(0),
                "bank_select[{0}]".format(1), "bank_select[{0}]".format(2),
                "bank_select[{0}]".format(3),
                "vdd", "gnd"]
        self.connect_inst(temp)
        
        self.control_position = vector(0, self.msb_decoder_position.y
                                              + self.msb_decoder.height)
        self.add_control_logic(self.control_position, "R0")
                                         
        self.CSb_position = self.control_position + self.control.CSb_position
        self.OEb_position = self.control_position + self.control.OEb_position
        self.WEb_position = self.control_position + self.control.WEb_position
        self.clk_position = self.control_position + self.control.clk_position

        # Max point
        self.max_point = self.msb_decoder_position.y + self.msb_decoder.height

    def add_labels(self):
        """ Add the top-level labels for control and address """
        for label in ["CSb", "OEb", "WEb", "clk"]:
            offset = getattr(self, label+"_position")
            self.add_label(text=label,
                           layer="metal3",
                           offset=offset)

        # add address label
        for addr_pos_lst in self.sram_bank_adress_positions:
            for address, address_positions in enumerate(addr_pos_lst):
                self.add_label(text="ADDR[{0}]".format(address),
                               layer="metal3",
                               offset=address_positions)

    def route_2or4_banks(self):
        """ Routing between bank 2 or 4 bank modules """
        addr_start_index = len(self.sram_property) + (self.num_banks / 2)
        bank_select_index = addr_start_index + self.bank.addr_size

        # control, data , address and bank_select connection
        for i in range(self.num_banks / 2):
            left_bank_index = 2 * i
            right_bank_index = 2 * i + 1

            for attr_index in range(len(self.sram_property)):
                bank_attr = self.sram_property[attr_index]
                self.add_rect(layer="metal3",
                              offset=getattr(self,bank_attr)[left_bank_index], 
                              width=getattr(self,bank_attr)[right_bank_index].x - getattr(self,bank_attr)[left_bank_index].x,
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=[self.vertical_line_positions[attr_index].x,
                                     getattr(self,bank_attr)[left_bank_index].y])

            for addr_index in range(self.bank.addr_size):
                line_index = addr_start_index + addr_index
                self.add_rect(layer="metal3",
                              offset=self.sram_bank_adress_positions[left_bank_index][addr_index],
                              width=self.sram_bank_adress_positions[right_bank_index][addr_index].x \
                                  - self.sram_bank_adress_positions[left_bank_index][addr_index].x,
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=[self.vertical_line_positions[line_index].x, 
                                     self.sram_bank_adress_positions[left_bank_index][addr_index].y])

            # left bank_select
            self.add_rect(layer="metal3",
                          offset=self.sram_bank_select_positions[left_bank_index],
                          width=self.vertical_line_positions[bank_select_index + left_bank_index].x \
                              - self.sram_bank_select_positions[left_bank_index].x,
                          height=drc["minwidth_metal3"])
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=[self.vertical_line_positions[bank_select_index + left_bank_index].x,
                                 self.sram_bank_select_positions[left_bank_index].y])

            # right bank select
            x_off = self.vertical_line_positions[bank_select_index + right_bank_index].x
            contact_offset = vector(x_off,
                                    self.sram_bank_select_positions[right_bank_index].y)
            
            self.add_rect(layer="metal3",
                          offset=contact_offset,
                          width=self.sram_bank_select_positions[right_bank_index].x \
                              - contact_offset.x,
                          height=drc["minwidth_metal3"])
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=contact_offset)

            # Data connection on the horizontal bus
        if (self.num_banks == 4):
            data_connection_top = self.sram_bank_data_positions[2][0].y + self.m2m3_via.height 
        else:
            data_connection_top=self.horizontal_bus_offset.y

        data_connection_height = data_connection_top - self.sram_bank_data_positions[0][0].y

        for i in range(2):
            lower_bank_index = i
            upper_bank_index = i + 2

            for data_index in range(self.bank.word_size):
                line_index = addr_start_index + addr_index
                self.add_rect(layer="metal2",
                              offset=self.sram_bank_data_positions[lower_bank_index][data_index],
                              width=drc["minwidth_metal2"],
                              height=data_connection_height)
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=[self.sram_bank_data_positions[lower_bank_index][data_index].x,
                                     self.horizontal_line_positions[data_index].y])

    def route_4_banks(self):
        for i in range(2):
            lower_bank_index = i
            upper_bank_index = i + 2

            # Power rail connections
            self.add_rect(layer="metal1",
                          offset=self.sram_bank_right_vdd_positions[lower_bank_index],
                          width=self.power_rail_width,
                          height=self.sram_bank_right_vdd_positions[upper_bank_index].y \
                              - self.sram_bank_right_vdd_positions[lower_bank_index].y)
            self.add_rect(layer="metal1",
                          offset=self.sram_bank_left_vdd_positions[lower_bank_index],
                          width=self.power_rail_width,
                          height=self.sram_bank_left_vdd_positions[upper_bank_index].y \
                              - self.sram_bank_left_vdd_positions[lower_bank_index].y)
            self.add_rect(layer="metal2",
                          offset=self.sram_bank_left_gnd_positions[lower_bank_index],
                          width=self.power_rail_width,
                          height=self.sram_bank_left_gnd_positions[upper_bank_index].y \
                              - self.sram_bank_left_gnd_positions[lower_bank_index].y)

    def route_bank_and_control(self):
        """ Routing between banks and control """

        if (self.num_banks == 1):

            # FIXME what is this? add comments
            # 5 = clk
            # 4 = tri_en_bar
            # 3 = tri_en
            # 2 = clk_bar
            # 1 = w_en
            # 0 = s_en

            control_side = []
            control_side.append(self.control.clk_position.rotate_scale(-1, 1)
                                     + self.control_position)
            control_side.append(self.control.clk_bar_position.rotate_scale(-1, 1)
                                     + self.control_position)
            control_side.append(self.control.tri_en_position.rotate_scale(-1, 1)
                                     + self.control_position)
            control_side.append(self.control.tri_en_bar_position.rotate_scale(-1, 1)
                                     + self.control_position)
            control_side.append(self.control.w_en_position.rotate_scale(-1, 1)
                                     + self.control_position)
            control_side.append(self.control.s_en_position.rotate_scale(-1, 1)
                                     + self.control_position)

            bank_side = []

            for attr_name in (self.sram_property):
                bank_side.append(getattr(self,attr_name)[0])

            for i in range(len(control_side)):
                self.add_rect(layer="metal3",
                              offset=control_side[i],
                              width=bank_side[i].x - control_side[i].x,
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal2", "via2", "metal3"),
                              offset=[bank_side[i].x + drc["minwidth_metal2"],
                                      control_side[i].y],
                              mirror="R90")
        elif (self.num_banks == 2 or self.num_banks == 4):
            for i in range(self.control_size):
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[self.vertical_line_positions[i].x + drc["minwidth_metal2"],
                                     self.control_bus_line_positions[i].y],
                             mirror="R90")
                control_attr = self.bank_property[i]
                control_side_line_position = (getattr(self.control,control_attr)
                                                    +self.control_position)

                self.add_rect(layer="metal2",
                              offset=[control_side_line_position.x,
                                      self.control_bus_line_positions[i].y],
                              width=drc["minwidth_metal2"],
                              height=control_side_line_position.y 
                                         - self.control_bus_line_positions[i].y)
                self.add_via(layers=("metal1", "via1", "metal2"),
                              offset=[control_side_line_position.x 
                                          + drc["minwidth_metal2"],
                                      self.control_bus_line_positions[i].y],
                              mirror="R90")
            for i in range(self.num_banks/2):
                # MSB line connections
                msb_line = self.control_size + self.num_banks/2 - 1 - i
                bank_select_start_line = msb_line + 2 + self.bank_addr_size

                msf_msb_din = (self.msf_msb_address.din_positions[i].rotate_scale(1, -1)
                                   + self.msf_msb_address_position) 

                contact_pos = vector(self.vertical_line_positions[msb_line].x, 
                                     msf_msb_din.y - 0.5*self.m2m3_via.width)
                self.add_rect(layer="metal3",
                              offset=contact_pos,
                              width=msf_msb_din.x - contact_pos.x,
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=contact_pos)

            # msf_msb_address clk connection
            self.add_rect(layer="metal1",
                          offset=[self.vertical_line_positions[0].x,
                                  self.control_bus_line_positions[0].y],
                          width=self.msf_msb_address_position.x 
                                    + self.msf_msb_address.clk_positions[0].y 
                                    - self.vertical_line_positions[0].x,
                          height=drc["minwidth_metal1"])

            if(self.num_banks == 2):
                msb_msf_dout_position = (self.msf_msb_address.dout_positions[i].rotate_scale(1, -1)
                                             + self.msf_msb_address_position)
                msb_msf_dout_bar_position = (self.msf_msb_address.dout_bar_positions[i].rotate_scale(1, -1)
                                             + self.msf_msb_address_position)
                starts = [msb_msf_dout_bar_position,
                          msb_msf_dout_position]

                for i in range(2):
                    bank_select_line = (self.control_size + 1 
                                            + self.bank_addr_size + i)

                    start = starts[i]
                    mid1 = vector(self.msf_msb_address_position.x 
                                      + self.msf_msb_address.height 
                                      + 4 * (i + 1) * drc["minwidth_metal2"],
                                  start.y)
                    end = vector(mid1.x, self.msf_msb_address_position.y
                                             + 4 * (i + 1) * drc["minwidth_metal2"])
                    self.add_wire(("metal2", "via1", "metal1"), [start, mid1, end])

                    x_off = self.vertical_line_positions[bank_select_line].x
                    contact_pos = vector(x_off,
                                         end.y - drc["minwidth_metal1"])
                    self.add_rect(layer="metal1",
                                  offset=contact_pos,
                                  width=end.x - contact_pos.x 
                                            + 0.5 * drc["minwidth_metal1"],
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                  offset=contact_pos)

            if(self.num_banks == 4):
                for i in range(2):
                    msb_msf_out_position = (self.msf_msb_address.dout_positions[i].rotate_scale(1, -1)
                                             + self.msf_msb_address_position)
                    msb_decoder_in_position =(self.msb_decoder.A_positions[i].scale(-1, 1)
                                                  + self.msb_decoder_position
                                                  + vector(0, 0.5 * drc["minwidth_metal1"]))

                    start = msb_msf_out_position
                    mid1 = start + vector(4 * (i + 1) * drc["minwidth_metal1"], 0)
                    mid2 = vector(mid1.x, msb_decoder_in_position.y)
                    end = vector(self.msb_decoder_position.x 
                                     + 3*drc["minwidth_metal3"],
                                 mid2.y)

                    layer_stack = ("metal2", "via1", "metal1")
                    self.add_wire(layer_stack, [start, mid1, mid2, end])

                    self.add_rect(layer="metal1",
                                  offset=[msb_decoder_in_position.x,
                                          msb_decoder_in_position.y - 0.5 * drc["minwidth_metal1"]],
                                  width=end.x - msb_decoder_in_position.x,
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                 offset=end - vector(0, 0.5 * self.m1m2_via.width),
                                 mirror="R90")
                for i in range(4):
                    bank_select_line = self.control_size + 2 + self.bank_addr_size + i
                    msb_decoder_out = (self.msb_decoder_position
                                           + self.msb_decoder.decode_out_positions[i].scale(-1, 1)
                                           + vector(0, 0.5*drc["minwidth_metal1"]))

                    x_off = self.vertical_line_positions[bank_select_line].x
                    contact_pos = vector(x_off,
                                         msb_decoder_out.y - 0.5*drc["minwidth_metal1"])
                    self.add_rect(layer="metal1",
                                  offset=contact_pos,
                                  width=msf_msb_din.x - contact_pos.x,
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                  offset=contact_pos)

    def route_vdd_singlebank(self):
        """ Route the vdd for 1 bank SRAMs """
        
        # left vdd rail of bank
        self.vdd_offset = self.bank.left_vdd_position
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.vdd_offset)

        # Add label for right vdd  rail bank
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.sram_bank_right_vdd_positions[0])

        # control logic
        self.control_vdd1_position = (self.control_position
                                          + self.control.vdd1_position.rotate_scale(-1, 1))
        self.control_vdd2_position = (self.control_position
                                          + self.control.vdd2_position.rotate_scale(-1, 1))

        self.add_rect(layer="metal1",
                      offset=self.control_vdd1_position,
                      width=self.vdd_offset.x
                                - self.control_vdd1_position.x,
                      height=drc["minwidth_metal1"])

        self.add_rect(layer="metal2",
                      offset=self.control_vdd2_position,
                      width=self.vdd_offset.x
                                - self.control_vdd2_position.x,
                      height=drc["minwidth_metal2"])

        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[self.vdd_offset.x,
                              self.control_vdd2_position.y],
                      size=(2, 1))

    def route_vdd_multibank(self):
        """ Route the vdd for 2 and 4 bank SRAMs """
        # VDD routing between banks
        self.add_rect(layer="metal1",
                      offset=self.vdd_position,
                      width=self.width,
                      height=self.power_rail_width)
        for bank_index in range(2):
            self.add_rect(layer="metal1",
                          offset=[self.sram_bank_right_vdd_positions[bank_index].x,
                                  self.vdd_position.y],
                          width=self.power_rail_width,
                          height=self.sram_bank_right_vdd_positions[bank_index].y 
                                     - self.vdd_position.y)
            self.add_rect(layer="metal1",
                          offset=[self.sram_bank_left_vdd_positions[bank_index].x,
                                  self.vdd_position.y],
                          width=self.power_rail_width,
                          height=self.sram_bank_left_vdd_positions[bank_index].y 
                                      - self.vdd_position.y)

        # VDD routing to control
        control_vdd_supply = self.control_bus_line_positions[self.control_size + 1]
        control_vdd1_position = self.control_position + self.control.vdd1_position
        control_vdd2_position = self.control_position + self.control.vdd2_position

        # rail extension
        self.add_rect(layer="metal1",
                      offset=self.sram_bank_right_vdd_positions[0],
                      width=self.power_rail_width,
                      height=control_vdd_supply.y 
                                 - self.sram_bank_right_vdd_positions[0].y)

        # Control vdd1
        if (self.control.width <= self.bank.width):
            self.add_rect(layer="metal2",
                          offset=[control_vdd1_position.x,
                                  control_vdd_supply.y],
                          width=drc["minwidth_metal2"],
                          height=control_vdd1_position.y 
                                     - control_vdd_supply.y)
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=control_vdd1_position)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[control_vdd1_position.x + drc["minwidth_metal2"],
                                 control_vdd_supply.y],
                         mirror="R90")

        if (self.control.width > self.bank.width):
            last_bank = self.num_banks - 1
            self.add_rect(layer="metal1",
                          offset=control_vdd1_position,
                          width=self.sram_bank_right_vdd_positions[last_bank].x 
                              - control_vdd1_position.x,
                          height=drc["minwidth_metal2"])
            self.add_rect(layer="metal1",
                          offset=self.sram_bank_right_vdd_positions[last_bank],
                          width=10*drc["minwidth_metal2"],
                          height=control_vdd1_position.y 
                              - self.sram_bank_right_vdd_positions[last_bank].y 
                              + drc["minwidth_metal2"])
                          
        # Control vdd2
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[control_vdd2_position.x 
                                  + drc["minwidth_metal2"],
                              control_vdd_supply.y],
                      mirror="R90")

        self.add_layout_pin(text="vdd",
                            layer="metal2",
                            offset=[control_vdd2_position.x,
                                    control_vdd_supply.y],
                            width=drc["minwidth_metal2"],
                            height=control_vdd2_position.y
                                       - control_vdd_supply.y)

        # msf_msb_address
        start = msf_address_vdd_position = (self.msf_msb_address_position
                                                 + self.msf_msb_address.vdd_positions[0].rotate_scale(1,-1))
        mid1 = vector(start.x,
                      self.msf_msb_address_position.y 
                          - self.msf_msb_address.width 
                          - 2*drc["minwidth_metal3"])
        end = vector(self.sram_bank_left_vdd_positions[1].x,
                     mid1.y)

        self.add_path("metal1", [start, mid1, end])
        
        # rail extension
        self.add_rect(layer="metal1",
                      offset=self.sram_bank_left_vdd_positions[1],
                      width=self.power_rail_width,
                      height=end.y - self.sram_bank_left_vdd_positions[1].y)

        if(self.num_banks == 4):
            # msf_msb and msb_decoder VDD
            start = (self.msb_decoder_position
                         + self.msb_decoder.vdd_position.scale(-1, 1)
                         + vector(0, 0.5*drc["minwidth_metal1"]))
            mid1 = vector(msf_address_vdd_position.x,
                          start.y)
            end = msf_address_vdd_position
            
            self.add_path("metal1", [start, mid1, end])

        # Add vdd labels to horizotal and vertical lines
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.vdd_position)
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=[self.sram_bank_left_vdd_positions[0].x,
                               self.vdd_position.y])
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=[self.sram_bank_left_vdd_positions[1].x,
                               self.vdd_position.y])
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=[self.sram_bank_right_vdd_positions[1].x,
                               self.vdd_position.y])
        

    def route_gnd_singlebank(self):
        """ Route the gnd for 1 bank SRAMs """

        # left gnd rail of bank
        self.gnd_offset = self.bank.left_gnd_position
        self.add_label(text="gnd",
                       layer="metal2",
                       offset=self.gnd_offset)

        self.control_gnd_position = (self.control_position
                                        + self.control.gnd_position.rotate_scale(-1,1) 
                                        + vector(drc["minwidth_metal2"],0))

        self.add_rect(layer="metal3",
                      offset=self.control_gnd_position,
                      width=self.gnd_offset.x - self.control_gnd_position.x,
                      height=drc["minwidth_metal3"])

        self.add_via(layers=("metal2", "via2", "metal3"),
                      offset=[self.gnd_offset.x,
                              self.control_gnd_position.y],
                      size=(2,1))
        
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.control_gnd_position,
                     rotate=90)


    def route_gnd_multibank(self):
        """ Route the gnd for 2 and 4 bank SRAMs """
        self.add_rect(layer="metal2",
                      offset=self.gnd_position,
                      width=self.width,
                      height=self.power_rail_width)

        for bank_index in range(2):
            self.add_rect(layer="metal2",
                          offset=[self.sram_bank_left_gnd_positions[bank_index].x,
                                  self.gnd_position.y],
                          width=self.power_rail_width,
                          height=self.sram_bank_left_gnd_positions[bank_index].y 
                                     - self.gnd_position.y)

        # gnd routing to control
        control_gnd_supply = self.control_bus_line_positions[self.control_size]
        control_gnd_position = self.control_position + self.control.gnd_position

        # rail extension
        self.add_rect(layer="metal2",
                      offset=self.sram_bank_left_gnd_positions[0],
                      width=drc["minwidth_metal2"],
                      height=control_gnd_supply.y + drc["minwidth_metal1"]
                                 - self.sram_bank_left_gnd_positions[0].y)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.sram_bank_left_gnd_positions[0].x
                                  + drc["minwidth_metal2"],
                             control_gnd_supply.y],
                     mirror="R90")
        # Control gnd
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[control_gnd_position.x + drc["minwidth_metal2"],
                             control_gnd_supply.y],
                     mirror="R90")
        self.add_layout_pin(text="gnd",
                            layer="metal2",
                            offset=[control_gnd_position.x,
                                    control_gnd_supply.y],
                            width=drc["minwidth_metal2"],
                            height=control_gnd_position.y
                                       - control_gnd_supply.y)

        # msf_msb_address , msb_decoder gnd

        # left gnd rail extension of bank3
        self.add_rect(layer="metal2",
                      offset=self.sram_bank_left_gnd_positions[1],
                      width=self.power_rail_width,
                      height=self.max_point
                                 - self.sram_bank_left_gnd_positions[1].y)

        for p in self.msf_msb_address.gnd_positions:
            gnd_position = vector(self.msf_msb_address_position.x 
                                      + self.msf_msb_address.height,
                                  self.msf_msb_address_position.y 
                                      - p.x - 0.5*drc["minwidth_metal2"])
            self.add_rect(layer="metal2",
                          offset=gnd_position,
                          width=(self.sram_bank_left_gnd_positions[1].x 
                                     - gnd_position.x),
                          height=drc["minwidth_metal2"])

        if(self.num_banks == 4):
            # msb Decoder
            msb_decoder_gnd_position = (self.msb_decoder_position
                                            + self.msb_decoder.gnd_position.scale(-1,1))
            self.add_rect(layer="metal1",
                          offset=msb_decoder_gnd_position,
                          width=self.sram_bank_left_gnd_positions[3].x \
                              - msb_decoder_gnd_position.x \
                              + self.power_rail_width,
                          height=drc["minwidth_metal1"])

            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.sram_bank_left_gnd_positions[3].x,
                                 msb_decoder_gnd_position.y + drc["minwidth_metal1"]],
                         mirror="MX",
                         size=(2,1))
        
        # Add gnd labels to horizotal and vertical lines
        self.add_label(text="gnd",
                       layer="metal2",
                       offset=self.gnd_position)
        self.add_label(text="gnd",
                       layer="metal2",
                       offset=[self.sram_bank_left_gnd_positions[0].x,
                               0])
        self.add_label(text="gnd",
                       layer="metal2",
                       offset=[self.sram_bank_left_gnd_positions[1].x,
                               0])

    def route_supplies(self):
        """ vdd/gnd routing of all modules """

        if (self.num_banks == 1):
            self.route_vdd_singlebank()
            self.route_gnd_singlebank()
        elif (self.num_banks == 2 or self.num_banks == 4):
            self.route_vdd_multibank()
            self.route_gnd_multibank()
        else:
            debug.error("Incorrect number of banks.")


    def sp_write(self, sp_name):
        # Write the entire spice of the object to the file
        ############################################################
        # Spice circuit
        ############################################################
        sp = open(sp_name, 'w')

        sp.write("* OpenRAM generated memory.\n")
        # This causes unit test mismatch
        #sp.write("* Created: {0}\n".format(datetime.datetime.now()))
        sp.write("* User: {0}\n".format(getpass.getuser()))
        sp.write(".global {0} {1}\n".format(spice["vdd_name"], 
                                            spice["gnd_name"]))
        usedMODS = list()
        self.sp_write_file(sp, usedMODS)
        del usedMODS
        sp.close()
