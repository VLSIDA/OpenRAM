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

        c = reload(__import__(OPTS.config.control_logic))
        self.mod_control_logic = getattr(c, OPTS.config.control_logic)
        
        c = reload(__import__(OPTS.config.ms_flop_array))
        self.mod_ms_flop_array = getattr(c, OPTS.config.ms_flop_array)
        
        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell = self.mod_bitcell()

        c = reload(__import__(OPTS.config.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.config.ms_flop)
        self.ms_flop = self.mod_ms_flop()
        

        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        import design
        design.design.name_map=[]

        self.word_size = word_size
        self.num_words = num_words
        self.num_banks = num_banks

        debug.info(2, "create sram of size {0} with {1} num of words".format(self.word_size, 
                                                                             self.num_words))

        design.design.__init__(self, name)

        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact(layer_stack=("poly", "contact", "metal1"))
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.m2m3_via = contact(layer_stack=("metal2", "via2", "metal3"))

        # For different layer width vias
        self.m2m3_offset_fix = vector(0,0.5*(drc["minwidth_metal3"]-drc["minwidth_metal2"]))
        
        self.m1_width = drc["minwidth_metal1"]        
        self.m2_width = drc["minwidth_metal2"]
        self.m3_width = drc["minwidth_metal3"]        

        # M1/M2 routing pitch is based on contacted pitch of the biggest layer
        self.m1_pitch = max(self.m1m2_via.width,self.m1m2_via.height) + max(drc["metal1_to_metal1"],drc["metal2_to_metal2"])
        self.m2_pitch = max(self.m2m3_via.width,self.m2m3_via.height) + max(drc["metal2_to_metal2"],drc["metal3_to_metal3"])
        self.m3_pitch = max(self.m2m3_via.width,self.m2m3_via.height) + max(drc["metal2_to_metal2"],drc["metal3_to_metal3"])
        

        self.control_size = 6
        self.bank_to_bus_distance = 5*drc["minwidth_metal3"]
        
        self.compute_sizes()
        self.add_pins()
        self.create_layout()
        
        # Can remove the following, but it helps for debug!
        self.add_lvs_correspondence_points()
        
        self.DRC_LVS()

    def compute_sizes(self):
        """  Computes the organization of the memory using bitcell size by trying to make it square."""

        debug.check(self.num_banks in [1,2,4], "Valid number of banks are 1 , 2 and 4.")

        self.num_words_per_bank = self.num_words/self.num_banks
        self.num_bits_per_bank = self.word_size*self.num_words_per_bank

        # Compute the area of the bitcells and estimate a square bank (excluding auxiliary circuitry)
        self.bank_area = self.bitcell.width*self.bitcell.height*self.num_bits_per_bank
        self.bank_side_length = math.sqrt(self.bank_area)

        # Estimate the words per row given the height of the bitcell and the square side length
        self.tentative_num_cols = int(self.bank_side_length/self.bitcell.width)
        self.words_per_row = self.estimate_words_per_row(self.tentative_num_cols, self.word_size)

        # Estimate the number of rows given the tentative words per row
        self.tentative_num_rows = self.num_bits_per_bank / (self.words_per_row*self.word_size)
        self.words_per_row = self.amend_words_per_row(self.tentative_num_rows, self.words_per_row)
        
        # Fix the number of columns and rows
        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words_per_bank/self.words_per_row

        # Compute the address and bank sizes
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(math.log(self.num_banks, 2))
        

    def estimate_words_per_row(self,tentative_num_cols, word_size):
        """This provides a heuristic rounded estimate for the number of words
        per row."""

        if tentative_num_cols < 1.5*word_size:
            return 1
        elif tentative_num_cols > 3*word_size:
            return 4
        else:
            return 2

    def amend_words_per_row(self,tentative_num_rows, words_per_row):
        """This picks the number of words per row more accurately by limiting
        it to a minimum and maximum.
        """
        # Recompute the words per row given a hard max
        if(tentative_num_rows > 512):
            debug.check(tentative_num_rows*words_per_row <= 2048, "Number of words exceeds 2048")
            return words_per_row*tentative_num_rows/512
        # Recompute the words per row given a hard min
        if(tentative_num_rows < 16):
            debug.check(tentative_num_rows*words_per_row >= 16, "Minimum number of rows is 16, but given {0}".format(tentative_num_rows))
            return words_per_row*tentative_num_rows/16
            
        return words_per_row

    def add_pins(self):
        """ Add pins for entire SRAM. """

        for i in range(self.word_size):
            self.add_pin("DATA[{0}]".format(i))
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i))

        self.control_logic_inputs=["CSb", "WEb",  "OEb", "clk"]
        self.control_logic_outputs=["s_en", "w_en", "tri_en", "tri_en_bar", "clk_bar", "clk_buf"]
        
        for pin in self.control_logic_inputs+["vdd","gnd"]:
            self.add_pin(pin)

    def create_layout(self):
        """ Layout creation """
        
        self.create_modules()

        if self.num_banks == 1:
            self.add_single_bank_modules()
            self.add_single_bank_pins()
            self.route_single_bank()
        elif self.num_banks == 2:
            self.add_two_bank_modules()
            self.route_two_banks()
        else:
            self.add_multi_bank_modules()
            self.add_multi_bank_pins()
            return
            self.route_2or4_banks()
            if self.num_banks > 2:
                self.route_4_banks()
                
            self.route_bank_and_control()
            self.route_supplies()

    def add_two_bank_modules(self):
        """ Adds the modules and the buses to the top level """


        ########################
        # First, compute all of the offsets
        ########################        
        self.num_vertical_line = self.bank_addr_size + self.control_size + self.num_banks + 1
        self.num_horizontal_line = self.word_size

        self.vertical_bus_width = self.m2_pitch*self.num_vertical_line
        self.data_bus_height = self.m3_pitch*self.num_horizontal_line
        self.control_bus_height = self.m1_pitch*(self.control_size+2) 
        self.supply_bus_height = self.m1_pitch*2 # 2 for vdd/gnd placed with control bus

        # Sanity check to ensure we can fit the control logic above a single bank (0.9 is a hack really)
        debug.check(self.bank.width + self.vertical_bus_width > 0.9*self.control_logic.width, "Bank is too small compared to control logic.")
        
        # This depends on the bus widths, but nothing else
        self.add_top_banks()
        
        self.vertical_bus_height = self.bank.height + self.bank_to_bus_distance + self.data_bus_height + self.control_bus_height
        self.vertical_bus_offset = vector(self.bank.width + self.bank_to_bus_distance, 2*self.power_rail_pitch)

        self.data_bus_width = 2*(self.bank.width + self.bank_to_bus_distance) + self.vertical_bus_width 
        self.data_bus_offset = vector(0, 2*self.power_rail_pitch + self.bank.height + self.bank_to_bus_distance)

        self.supply_bus_width = self.data_bus_width
        self.supply_bus_offset = vector(0, self.data_bus_offset.y + self.data_bus_height)        

        self.control_bus_width = self.bank.width + self.bank_to_bus_distance + self.vertical_bus_width
        self.control_bus_offset = vector(0, self.supply_bus_offset.y + self.supply_bus_height)
        
        self.bank_sel_bus_offset = self.vertical_bus_offset + vector(self.m2_pitch*self.control_size,0)

        # The address bus extends down through the power rails, but control and bank_sel bus don't
        self.addr_bus_height = self.vertical_bus_height + 2*self.power_rail_pitch
        self.addr_bus_offset = self.bank_sel_bus_offset.scale(1,0) + vector(self.m2_pitch*self.num_banks,0)
        


        # Control is placed at the top above the control bus and everything
        self.control_logic_position = vector(0, self.control_bus_offset.y + self.control_bus_height + self.m1_pitch)

        # Bank select flops get put to the right of control logic above bank1 and the buses
        # Leave a pitch to get the vdd rails up to M2
        self.msb_address_position = vector(max(self.bank_inst[1].lx(),self.control_logic.width),
                                           self.supply_bus_offset.y+self.supply_bus_height + 2*self.m1_pitch + self.msb_address.width)

        
        ########################
        # Second, place the buses
        ########################        
        # Vertical bus
        # The order of the control signals on the control bus:
        self.control_bus_names = ["clk_buf", "tri_en_bar", "tri_en", "clk_bar", "w_en", "s_en"]
        self.vert_control_bus_positions = self.create_bus(layer="metal2",
                                                          pitch=self.m2_pitch,
                                                          offset=self.vertical_bus_offset,
                                                          names=self.control_bus_names,
                                                          length=self.vertical_bus_height,
                                                          vertical=True)
        self.addr_bus_names=[]
        for i in range(self.addr_size):
            self.addr_bus_names.append("ADDR[{}]".format(i))
        self.vert_control_bus_positions.update(self.create_bus(layer="metal2",
                                                               pitch=self.m2_pitch,
                                                               offset=self.addr_bus_offset,
                                                               names=self.addr_bus_names,
                                                               length=self.addr_bus_height,
                                                               vertical=True,
                                                               make_pins=True))
            
        self.bank_sel_bus_names = ["bank_sel[0]","bank_sel[1]"]
        self.vert_control_bus_positions.update(self.create_bus(layer="metal2",
                                                               pitch=self.m2_pitch,
                                                               offset=self.bank_sel_bus_offset,
                                                               names=self.bank_sel_bus_names,
                                                               length=self.vertical_bus_height,
                                                               vertical=True))
        

        # Horizontal data bus
        self.data_bus_names = []
        for i in range(0, self.word_size):
            self.data_bus_names.append("DATA[{}]".format(i))
        self.data_bus_positions = self.create_bus(layer="metal3",
                                                  pitch=self.m3_pitch,
                                                  offset=self.data_bus_offset,
                                                  names=self.data_bus_names,
                                                  length=self.data_bus_width,
                                                  vertical=False,
                                                  make_pins=True)

        # Horizontal control logic bus
        # vdd/gnd in bus go along whole SRAM
        # FIXME: Fatten these wires?
        self.horz_control_bus_positions = self.create_bus(layer="metal1",
                                                          pitch=self.m1_pitch,
                                                          offset=self.supply_bus_offset,
                                                          names=["vdd", "gnd"],
                                                          length=self.supply_bus_width,
                                                          vertical=False)
        self.horz_control_bus_positions.update(self.create_bus(layer="metal1",
                                                               pitch=self.m1_pitch,
                                                               offset=self.control_bus_offset,
                                                               names=self.control_bus_names,
                                                               length=self.control_bus_width,
                                                               vertical=False))

        ########################
        # Third, place the other logic (banks are done first to anchor the design)
        ########################        
        self.add_control_logic(position=self.control_logic_position, rotate=0)

        self.msb_address_inst = self.add_inst(name="msb_address",
                                              mod=self.msb_address,
                                              offset=self.msb_address_position,
                                              rotate=270)
        self.msb_bank_sel_addr = "ADDR[{}]".format(self.addr_size-1)
        self.connect_inst([self.msb_bank_sel_addr,"bank_sel[1]","bank_sel[0]","clk_buf", "vdd", "gnd"])
        
        
        self.width= self.data_bus_width
        self.height = self.control_logic_inst.uy()
    
    def route_two_banks(self):
        """ Route all of the signals for the two bank SRAM. """

        # create the input control pins
        for n in self.control_logic_inputs:
            self.copy_layout_pin(self.control_logic_inst, n.lower(), n)
            
        # connect the control logic to the control bus
        for n in self.control_logic_outputs + ["vdd", "gnd"]:
            pins = self.control_logic_inst.get_pins(n)
            for pin in pins:
                if pin.layer=="metal2":
                    pin_pos = pin.bc()
                    break
            rail_pos = vector(pin_pos.x,self.horz_control_bus_positions[n].y)
            self.add_path("metal2",[pin_pos,rail_pos])
            self.add_center_via(("metal1","via1","metal2"),rail_pos)

        # connect the control logic cross bar
        for n in self.control_logic_outputs:
            cross_pos = vector(self.vert_control_bus_positions[n].x,self.horz_control_bus_positions[n].y)
            self.add_center_via(("metal1","via1","metal2"),cross_pos)
            
        # connect the horizontal control bus to the vertical bus
        # connect the data output to the data bus
        for n in self.data_bus_names:
            for i in range(2):
                pin_pos = self.bank_inst[i].get_pin(n).uc()
                rail_pos = vector(pin_pos.x,self.data_bus_positions[n].y)
                self.add_path("metal2",[pin_pos,rail_pos])
                self.add_center_via(("metal2","via2","metal3"),rail_pos)

        self.route_single_msb_address()

        # connect the banks to the vertical address bus
        # connect the banks to the vertical control bus
        for n in self.addr_bus_names + self.control_bus_names:
            # Skip these from the horizontal bus
            if n in ["vdd", "gnd"]: continue
            # This will be the bank select, so skip it
            if n == self.msb_bank_sel_addr: continue
            pin0_pos = self.bank_inst[0].get_pin(n).rc()
            pin1_pos = self.bank_inst[1].get_pin(n).lc()
            rail_pos = vector(self.vert_control_bus_positions[n].x,pin0_pos.y)
            self.add_path("metal3",[pin0_pos,pin1_pos])
            self.add_center_via(("metal2","via2","metal3"),rail_pos)

        # connect the bank select signals to the vertical bus
        for i in range(2):
            pin = self.bank_inst[i].get_pin("bank_sel")
            pin_pos = pin.rc() if i==0 else pin.lc()
            rail_pos = vector(self.vert_control_bus_positions["bank_sel[{}]".format(i)].x,pin_pos.y)
            self.add_path("metal3",[pin_pos,rail_pos])
            self.add_center_via(("metal2","via2","metal3"),rail_pos)

        self.route_two_bank_supplies()
        

    def route_two_bank_supplies(self):
        """ Finish routing the power supplies for a 2-bank SRAM """
        # control logic supplies done with control signals
        

        self.route_major_supply_rails()
            

    def route_single_msb_address(self):
        """ Route one MSB address bit for 2-bank SRAM """

        # connect the bank MSB flop supplies
        vdd_pins = self.msb_address_inst.get_pins("vdd")
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal1": continue
            vdd_pos = vdd_pin.bc()
            down_pos = vdd_pos - vector(0,self.m1_pitch)
            rail_pos = vector(vdd_pos.x,self.horz_control_bus_positions["vdd"].y)
            self.add_path("metal1",[vdd_pos,down_pos])            
            self.add_center_via(("metal1","via1","metal2"),down_pos,rotate=90)   
            self.add_path("metal2",[down_pos,rail_pos])
            self.add_center_via(("metal1","via1","metal2"),rail_pos)
        
        gnd_pins = self.msb_address_inst.get_pins("gnd")
        # Only add the ground connection to the lowest metal2 rail in the flop array
        # FIXME: SCMOS doesn't have a vertical rail in the cell, or we could use those
        lowest_y = None
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal2": continue
            if lowest_y==None or gnd_pin.by()<lowest_y:
                lowest_y=gnd_pin.by()
                gnd_pos = gnd_pin.ur()
        rail_pos = vector(gnd_pos.x,self.horz_control_bus_positions["gnd"].y)
        self.add_path("metal2",[gnd_pos,rail_pos])
        self.add_center_via(("metal1","via1","metal2"),rail_pos)            
        
        # connect the MSB flop to the address input bus 
        msb_pins = self.msb_address_inst.get_pins("din[0]")
        for msb_pin in msb_pins:
            if msb_pin.layer == "metal3":
                msb_pin_pos = msb_pin.lc()
                break
        rail_pos = vector(self.vert_control_bus_positions[self.msb_bank_sel_addr].x,msb_pin_pos.y)
        self.add_path("metal3",[msb_pin_pos,rail_pos])
        self.add_center_via(("metal2","via2","metal3"),rail_pos)

        # Connect the output bar to select 0
        msb_out_pin = self.msb_address_inst.get_pin("dout_bar[0]")
        msb_out_pos = msb_out_pin.rc()
        out_extend_right_pos = msb_out_pos + vector(self.m2_pitch,0)
        out_extend_up_pos = out_extend_right_pos + vector(0,self.m2_width)
        rail_pos = vector(self.vert_control_bus_positions["bank_sel[0]"].x,out_extend_up_pos.y)
        self.add_path("metal2",[msb_out_pos,out_extend_right_pos,out_extend_up_pos])
        self.add_wire(("metal3","via2","metal2"),[out_extend_right_pos,out_extend_up_pos,rail_pos])
        self.add_center_via(("metal2","via2","metal3"),rail_pos)
        
        # Connect the output to select 1
        msb_out_pin = self.msb_address_inst.get_pin("dout[0]")
        msb_out_pos = msb_out_pin.rc()
        out_extend_right_pos = msb_out_pos + vector(self.m2_pitch,0)
        out_extend_down_pos = out_extend_right_pos - vector(0,2*self.m1_pitch)
        rail_pos = vector(self.vert_control_bus_positions["bank_sel[1]"].x,out_extend_down_pos.y)
        self.add_path("metal2",[msb_out_pos,out_extend_right_pos,out_extend_down_pos])
        self.add_wire(("metal3","via2","metal2"),[out_extend_right_pos,out_extend_down_pos,rail_pos])
        self.add_center_via(("metal2","via2","metal3"),rail_pos)
        
        # Connect clk
        clk_pin = self.msb_address_inst.get_pin("clk")
        clk_pos = clk_pin.bc()
        rail_pos = self.horz_control_bus_positions["clk_buf"]
        bend_pos = vector(clk_pos.x,self.horz_control_bus_positions["clk_buf"].y)
        self.add_path("metal1",[clk_pos,bend_pos,rail_pos])
        

    def route_major_supply_rails(self):
        """ Create rails at bottom. Connect veritcal rails to top and bottom. """
        
        self.add_layout_pin(text="gnd",
                            layer="metal3",
                            offset=vector(0,0),
                            height=self.power_rail_width,
                            width=self.width)

        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vector(0,self.power_rail_pitch),
                            height=self.power_rail_width,
                            width=self.width)

        # route bank vertical rails to top and bottom
        for i in range(2):
            vdd_pins = self.bank_inst[i].get_pins("vdd")
            for vdd_pin in vdd_pins:
                vdd_pos = vdd_pin.ul()
                # Route to top
                self.add_rect(layer="metal1",
                              offset=vdd_pos,
                              height=self.horz_control_bus_positions["vdd"].y-vdd_pos.y+0.5*self.m1_width,
                              width=vdd_pin.width())
                # Route to bottom
                self.add_rect(layer="metal1",
                              offset=vector(vdd_pos.x,self.power_rail_pitch),
                              height=self.bank_inst[0].by(),
                              width=vdd_pin.width())

            gnd_pins = self.bank_inst[i].get_pins("gnd")
            for gnd_pin in gnd_pins:
                # Route to top
                gnd_pos = gnd_pin.ul()
                self.add_rect(layer="metal2",
                              offset=gnd_pos,
                              height=self.horz_control_bus_positions["gnd"].y-gnd_pos.y+0.5*self.m1_width,
                              width=gnd_pin.width())
                # Add two vias for right now, should be right size power via
                right_rail_pos = vector(gnd_pin.ur().x,self.horz_control_bus_positions["gnd"].y)            
                self.add_via(layers=("metal1","via1","metal2"),
                             offset=right_rail_pos - vector(0,0.5*self.m1_width),
                             rotate=90,
                             size=[1,3]) 

                # Route to bottom
                self.add_rect(layer="metal2",
                              offset=vector(gnd_pos.x,0),
                              height=self.bank_inst[0].by(),
                              width=gnd_pin.width())
                # Add two vias for right now, should be right size power via
                right_rail_pos = vector(gnd_pin.lr().x,0)          
                self.add_via(layers=("metal2","via2","metal3"),
                             offset=right_rail_pos,
                             rotate=90,
                             size=[2,3]) 
                
        # connect the vertical rails along bottom of SRAM
        pass
        
        
    def create_multi_bank_modules(self):
        """ Create the multibank address flops and bank decoder """
        
        self.msb_address = self.mod_ms_flop_array(name="msb_address",
                                                  columns=1,
                                                  word_size=self.num_banks/2)
        self.add_mod(self.msb_address)

        if self.num_banks>2:
            self.msb_decoder = self.bank.decoder.pre2_4
            self.add_mod(self.msb_decoder)

    def create_modules(self):
        """ Create all the modules that will be used """

        # Create the control logic module
        self.control_logic = self.mod_control_logic(num_rows=self.num_rows)
        self.add_mod(self.control_logic)

        # Create the bank module (up to four are instantiated)
        self.bank = bank(word_size=self.word_size,
                         num_words=self.num_words_per_bank,
                         words_per_row=self.words_per_row,
                         num_banks=self.num_banks,
                         name="bank")
        self.add_mod(self.bank)

        # Conditionally create the 
        if(self.num_banks > 1):
            self.create_multi_bank_modules()

        self.bank_count = 0

        self.power_rail_width = self.bank.vdd_rail_width
        # Leave some extra space for the pitch
        self.power_rail_pitch = self.bank.vdd_rail_width + 2*drc["metal3_to_metal3"]



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
            temp.append("DATA[{0}]".format(i))
        for i in range(self.bank_addr_size):
            temp.append("ADDR[{0}]".format(i))
        if(self.num_banks > 1):
            temp.append("bank_sel[{0}]".format(bank_num))
        temp.extend(["s_en", "w_en", "tri_en_bar", "tri_en",
                     "clk_bar","clk_buf" , "vdd", "gnd"])
        self.connect_inst(temp)

        return bank_inst

    # FIXME: This should be in geometry.py or it's own class since it is
    # reusable
    def create_bus(self, layer, pitch, offset, names, length, vertical=False, make_pins=False):
        """ Create a horizontal or vertical bus. It can be either just rectangles, or actual
        layout pins. It returns an map of line center line positions indexed by name.  """

        # half minwidth so we can return the center line offsets
        half_minwidth = 0.5*drc["minwidth_{}".format(layer)]
        
        line_positions = {}
        if vertical:
            for i in range(len(names)):
                line_offset = offset + vector(i*pitch,0)
                if make_pins:
                    self.add_layout_pin(text=names[i],
                                        layer=layer,
                                        offset=line_offset,
                                        height=length)
                else:
                    self.add_rect(layer=layer,
                                  offset=line_offset,
                                  height=length)
                line_positions[names[i]]=line_offset+vector(half_minwidth,0)
        else:
            for i in range(len(names)):
                line_offset = offset + vector(0,i*pitch + half_minwidth)
                if make_pins:
                    self.add_layout_pin(text=names[i],
                                        layer=layer,
                                        offset=line_offset,
                                        width=length)
                else:
                    self.add_rect(layer=layer,
                                  offset=line_offset,
                                  width=length)
                line_positions[names[i]]=line_offset+vector(0,half_minwidth)

        return line_positions


    def add_control_logic(self, position, rotate):
        """ Add and place control logic """
        self.control_logic_inst=self.add_inst(name="control",
                                              mod=self.control_logic,
                                              offset=position,
                                              rotate=rotate)
        self.connect_inst(self.control_logic_inputs + self.control_logic_outputs + ["vdd", "gnd"])


    def add_lvs_correspondence_points(self):
        for n in self.control_bus_names:
            self.add_label(text=n,
                           layer="metal2",  
                           offset=self.vert_control_bus_positions[n])
        for n in self.bank_sel_bus_names:
            self.add_label(text=n,
                           layer="metal2",  
                           offset=self.vert_control_bus_positions[n])

    def add_single_bank_modules(self):
        """ 
        This adds the moduels for a single bank SRAM with control
        logic. 
        """
        
        # No orientation or offset
        self.bank_inst = self.add_bank(0, [0, 0], 1, 1)
        
        # Control logic is placed to the left of the blank even with the
        # decoder bottom. A small gap is in the x-dimension.
        control_gap = 2*drc["minwidth_metal3"]
        pos = vector(-control_gap,
                     self.bank.row_decoder_inst.by() + 2*drc["minwidth_metal3"])
        self.add_control_logic(position=pos,
                               rotate=90)

        self.width = self.bank.width + self.control_logic.height + control_gap
        self.height = self.bank.height

    def add_single_bank_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """

        for i in range(self.word_size):
            self.copy_layout_pin(self.bank_inst, "DATA[{}]".format(i))

        for i in range(self.addr_size):
            self.copy_layout_pin(self.bank_inst, "ADDR[{}]".format(i))            

        for (old,new) in zip(["csb","web","oeb","clk"],["CSb","WEb","OEb","clk"]):
            self.copy_layout_pin(self.control_logic_inst, old, new)

        self.copy_layout_pin(self.bank_inst, "vdd")
        self.copy_layout_pin(self.bank_inst, "gnd")


    def add_top_banks(self):
        # Placement of bank 0
        self.bank_position_0 = vector(self.bank.width,
                                      self.bank.height + 2*self.power_rail_pitch)
        self.bank_inst=[self.add_bank(0,self.bank_position_0, -1, -1)]

        # Placement of bank 1
        x_off = self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance
        self.bank_position_1 = vector(x_off, self.bank_position_0.y)
        self.bank_inst.append(self.add_bank(1,self.bank_position_1, -1, 1))

    def add_bottom_banks(self):
        # Placement of bank 2
        y_off = self.bank.height + self.horizontal_bus_width + 2*self.bank_to_bus_distance + self.power_rail_pitch
        bank_position_2 = vector(self.bank_position_0.x, y_off)
        self.bank2=self.add_bank(bank_position_2, 1, -1)

        # Placement of bank 3
        bank_position_3 = vector(self.bank_position_1.x, bank_position_2.y)
        self.bank3=self.add_bank(bank_position_3, 1, 1)
        
        self.msb_decoder_position = vector(bank_position_3.x + self.power_rail_width + 4*drc["minwidth_metal3"] + self.msb_decoder.width,
                                           self.msf_msb_address_position.y + 4*drc["minwidth_metal3"])

        self.add_inst(name="msb_decoder",
                      mod=self.msb_decoder,
                      offset=self.msb_decoder_position,
                      mirror="MY")
        temp = ["msb0", "msb1"]
        for i in range(4):
            temp.append("bank_sel[{}]".format(i))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)
        
        self.control_position = vector(0, self.msb_decoder_position.y + self.msb_decoder.height)
        self.add_control_logic(self.control_position, 0)

        # Max point
        self.max_point = self.msb_decoder_position.y + self.msb_decoder.height


    def route_2or4_banks(self):
        """ Routing of top two banks """
        return
        addr_start_index = len(self.sram_property) + self.num_banks/2
        bank_select_index = addr_start_index + self.bank.addr_size

        # control, data , address and bank_select connection
        for i in range(self.num_banks / 2):
            left_bank_index = 2*i
            right_bank_index = 2*i + 1

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
        if self.num_banks == 4:
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

    def route_bottom_banks(self):
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

    def connect_rail_from_left_m2m3(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = vector(dest_pin.cx(), in_pos.y)
        self.add_wire(("metal3","via2","metal2"),[in_pos, out_pos, out_pos - vector(0,self.m2_pitch)])
        self.add_via(layers=("metal2","via2","metal3"),
                     offset=src_pin.lr() - self.m2m3_offset_fix,
                     rotate=90)
        
    def connect_rail_from_left_m2m1(self, src_pin, dest_pin):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = src_pin.rc()
        out_pos = vector(dest_pin.cx(), in_pos.y)
        self.add_wire(("metal2","via1","metal1"),[in_pos, out_pos, out_pos - vector(0,self.m2_pitch)])

    def route_single_bank(self):
        """ Route a single bank SRAM """
        for n in self.control_logic_outputs:
            src_pin = self.control_logic_inst.get_pin(n)
            dest_pin = self.bank_inst.get_pin(n)                
            self.connect_rail_from_left_m2m3(src_pin, dest_pin)

        src_pins = self.control_logic_inst.get_pins("vdd")
        for src_pin in src_pins:
            if src_pin.layer != "metal2":
                continue
            dest_pin = self.bank_inst.get_pins("vdd")[1]
            self.connect_rail_from_left_m2m1(src_pin,dest_pin)
            
        src_pins = self.control_logic_inst.get_pins("gnd")
        for src_pin in src_pins:            
            if src_pin.layer != "metal2":
                continue
            dest_pin = self.bank_inst.get_pin("gnd")
            self.connect_rail_from_left_m2m3(src_pin,dest_pin)
        
    def route_bank_and_control(self):
        """ Routing between banks and control """

        if self.num_banks == 1:
            pass
        elif self.num_banks == 2 or self.num_banks == 4:
            for i in range(self.control_size):
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[self.vertical_line_positions[i].x + drc["minwidth_metal2"],
                                     self.control_bus_line_positions[i].y],
                             rotate=90)
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
                              rotate=90)
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
                                 rotate=90)
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


    def route_vdd_multi_bank(self):
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
                         rotate=90)

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
                      rotate=90)

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
        


    def route_gnd_multi_bank(self):
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
                     rotate=90)
        # Control gnd
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[control_gnd_position.x + drc["minwidth_metal2"],
                             control_gnd_supply.y],
                     rotate=90)
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
        return
        if (self.num_banks == 1):
            pass
        elif (self.num_banks == 2 or self.num_banks == 4):
            self.route_vdd_multi_bank()
            self.route_gnd_multi_bank()
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

    def analytical_model(self,slews,loads):
        LH_delay = []
        HL_delay = []
        LH_slew = []
        HL_slew = []
        for slew in slews:
            for load in loads:
                bank_delay = self.bank.delay(slew,load)
                # Convert from ps to ns
                LH_delay.append(bank_delay.delay/1e3)
                HL_delay.append(bank_delay.delay/1e3)
                LH_slew.append(bank_delay.slew/1e3)
                HL_slew.append(bank_delay.slew/1e3)
        
        data = {"min_period": 0, 
                "delay1": LH_delay,
                "delay0": HL_delay,
                "slew1": LH_slew,
                "slew0": HL_slew,
                "read0_power": 0,
                "read1_power": 0,
                "write0_power": 0,
                "write1_power": 0
                }
        return data
