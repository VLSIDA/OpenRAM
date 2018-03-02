import sys
from tech import drc, spice
import debug
import design
from math import log,sqrt,ceil
import contact
from bank import bank
import datetime
import getpass
from vector import vector
from globals import OPTS, print_time

    
class sram(design.design):
    """
    Dynamically generated SRAM by connecting banks to control logic. The
    number of banks should be 1 , 2 or 4
    """

    def __init__(self, word_size, num_words, num_banks, name):

        c = reload(__import__(OPTS.control_logic))
        self.mod_control_logic = getattr(c, OPTS.control_logic)
        
        c = reload(__import__(OPTS.ms_flop_array))
        self.mod_ms_flop_array = getattr(c, OPTS.ms_flop_array)
        
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()

        c = reload(__import__(OPTS.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.ms_flop)
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
        start_time = datetime.datetime.now()

        design.design.__init__(self, name)

        # For different layer width vias
        self.m2m3_offset_fix = vector(0,0.5*(self.m3_width-self.m2_width))
        
        # M1/M2 routing pitch is based on contacted pitch of the biggest layer
        self.m1_pitch = max(contact.m1m2.width,contact.m1m2.height) + max(self.m1_space,self.m2_space)
        self.m2_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(self.m2_space,self.m3_space)
        self.m3_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(self.m2_space,self.m3_space)
        

        self.control_size = 6
        self.bank_to_bus_distance = 5*self.m3_width
        
        self.compute_sizes()
        self.add_pins()
        self.create_layout()
        
        # Can remove the following, but it helps for debug!
        self.add_lvs_correspondence_points()
        
        self.offset_all_coordinates()
        sizes = self.find_highest_coords()
        self.width = sizes[0]
        self.height = sizes[1]
        
        self.DRC_LVS(final_verification=True)

        if not OPTS.is_unit_test:
            print_time("SRAM creation", datetime.datetime.now(), start_time)


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
        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words_per_bank/self.words_per_row

        # Compute the address and bank sizes
        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.bank_addr_size = self.col_addr_size + self.row_addr_size
        self.addr_size = self.bank_addr_size + int(log(self.num_banks, 2))
        
        debug.info(1,"Words per row: {}".format(self.words_per_row))

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
            self.add_pin("DATA[{0}]".format(i),"INOUT")
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i),"INPUT")

        # These are used to create the physical pins too
        self.control_logic_inputs=["CSb", "WEb",  "OEb", "clk"]
        self.control_logic_outputs=["s_en", "w_en", "tri_en", "tri_en_bar", "clk_bar", "clk_buf"]
        
        self.add_pin_list(self.control_logic_inputs,"INPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

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
        elif self.num_banks == 4:
            self.add_four_bank_modules()
            self.route_four_banks()
        else:
            debug.error("Invalid number of banks.",-1)


    def add_four_bank_modules(self):
        """ Adds the modules and the buses to the top level """

        self.compute_four_bank_offsets()

        self.add_four_banks()

        self.add_busses()

        self.add_four_bank_logic()
        
        self.width = self.bank_inst[1].ur().x
        self.height = max(self.control_logic_inst.uy(),self.msb_decoder_inst.uy())


    def add_two_bank_modules(self):
        """ Adds the modules and the buses to the top level """

        self.compute_two_bank_offsets()

        self.add_two_banks()
        
        self.add_busses()

        self.add_two_bank_logic()

        self.width = self.bank_inst[1].ur().x
        self.height = self.control_logic_inst.uy()
        
        
    def route_shared_banks(self):
        """ Route the shared signals for two and four bank configurations. """

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
            self.add_via_center(("metal1","via1","metal2"),rail_pos)
        
        # connect the control logic cross bar
        for n in self.control_logic_outputs:
            cross_pos = vector(self.vert_control_bus_positions[n].x,self.horz_control_bus_positions[n].y)
            self.add_via_center(("metal1","via1","metal2"),cross_pos)

        # connect the bank select signals to the vertical bus
        for i in range(self.num_banks):
            pin = self.bank_inst[i].get_pin("bank_sel")
            pin_pos = pin.rc() if i==0 else pin.lc()
            rail_pos = vector(self.vert_control_bus_positions["bank_sel[{}]".format(i)].x,pin_pos.y)
            self.add_path("metal3",[pin_pos,rail_pos])
            self.add_via_center(("metal2","via2","metal3"),rail_pos)

        
            
    def route_four_banks(self):
        """ Route all of the signals for the four bank SRAM. """
        
        self.route_shared_banks()

        # connect the data output to the data bus
        for n in self.data_bus_names:
            for i in [0,1]:
                pin_pos = self.bank_inst[i].get_pin(n).bc()
                rail_pos = vector(pin_pos.x,self.data_bus_positions[n].y)
                self.add_path("metal2",[pin_pos,rail_pos])
                self.add_via_center(("metal2","via2","metal3"),rail_pos)

            for i in [2,3]:
                pin_pos = self.bank_inst[i].get_pin(n).uc()
                rail_pos = vector(pin_pos.x,self.data_bus_positions[n].y)
                self.add_path("metal2",[pin_pos,rail_pos])
                self.add_via_center(("metal2","via2","metal3"),rail_pos)
                
        # route msb address bits
        # route 2:4 decoder
        self.route_double_msb_address()

        # connect the banks to the vertical address bus
        # connect the banks to the vertical control bus
        for n in self.addr_bus_names + self.control_bus_names:
            # Skip these from the horizontal bus
            if n in ["vdd", "gnd"]: continue
            # This will be the bank select, so skip it
            if n in self.msb_bank_sel_addr: continue

            for bank_id in [0,2]:
                pin0_pos = self.bank_inst[bank_id].get_pin(n).rc()
                pin1_pos = self.bank_inst[bank_id+1].get_pin(n).lc()
                rail_pos = vector(self.vert_control_bus_positions[n].x,pin0_pos.y)
                self.add_path("metal3",[pin0_pos,pin1_pos])
                self.add_via_center(("metal2","via2","metal3"),rail_pos)
            

        self.route_bank_supply_rails(bottom_banks=[2,3])



        

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
        debug.check(self.bank.width + self.vertical_bus_width > 0.9*self.control_logic.width, "Bank is too small compared to control logic.")
        
        
    def compute_four_bank_offsets(self):
        """ Compute the overall offsets for a four bank SRAM """

        # The main difference is that the four bank SRAM has the data bus in the middle of the four banks
        # as opposed to the top of the banks.
        
        self.compute_bus_sizes()
        
        # In 4 bank SRAM, the height is determined by the bank decoder and address flop
        self.vertical_bus_height = 2*self.bank.height + 4*self.bank_to_bus_distance + self.data_bus_height \
                                   + self.supply_bus_height + self.msb_decoder.height + self.msb_address.width 
        # The address bus extends down through the power rails, but control and bank_sel bus don't
        self.addr_bus_height = self.vertical_bus_height + 2*self.power_rail_pitch

        self.vertical_bus_offset = vector(self.bank.width + self.bank_to_bus_distance, 2*self.power_rail_pitch)
        self.data_bus_offset = vector(0, 2*self.power_rail_pitch + self.bank.height + self.bank_to_bus_distance)
        self.supply_bus_offset = vector(0, self.data_bus_offset.y + self.data_bus_height + self.bank.height + 2*self.bank_to_bus_distance)        
        self.control_bus_offset = vector(0, self.supply_bus_offset.y + self.supply_bus_height)
        self.bank_sel_bus_offset = self.vertical_bus_offset + vector(self.m2_pitch*self.control_size,0)
        self.addr_bus_offset = self.bank_sel_bus_offset.scale(1,0) + vector(self.m2_pitch*self.num_banks,0)

        # Control is placed at the top above the control bus and everything
        self.control_logic_position = vector(0, self.control_bus_offset.y + self.control_bus_height + self.m1_pitch)

        # Bank select flops get put to the right of control logic above bank1 and the buses
        # Leave a pitch to get the vdd rails up to M2
        self.msb_address_position = vector(max(self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance, self.control_logic.width),
                                           self.supply_bus_offset.y + self.supply_bus_height + 2*self.m1_pitch + self.msb_address.width)

        # Decoder goes above the MSB address flops, and is flipped in Y
        # separate the two by a bank to bus distance for nwell rules, just in case
        self.msb_decoder_position = self.msb_address_position + vector(self.msb_decoder.width, self.bank_to_bus_distance)


    def compute_two_bank_offsets(self):
        """ Compute the overall offsets for a two bank SRAM """

        self.compute_bus_sizes()

        # In 2 bank SRAM, the height is determined by the control bus which is higher than the msb address
        self.vertical_bus_height = self.bank.height + 2*self.bank_to_bus_distance + self.data_bus_height + self.control_bus_height
        # The address bus extends down through the power rails, but control and bank_sel bus don't
        self.addr_bus_height = self.vertical_bus_height + 2*self.power_rail_pitch
        
        self.vertical_bus_offset = vector(self.bank.width + self.bank_to_bus_distance, 2*self.power_rail_pitch)
        self.data_bus_offset = vector(0, 2*self.power_rail_pitch + self.bank.height + self.bank_to_bus_distance)
        self.supply_bus_offset = vector(0, self.data_bus_offset.y + self.data_bus_height)        
        self.control_bus_offset = vector(0, self.supply_bus_offset.y + self.supply_bus_height)
        self.bank_sel_bus_offset = self.vertical_bus_offset + vector(self.m2_pitch*self.control_size,0)
        self.addr_bus_offset = self.bank_sel_bus_offset.scale(1,0) + vector(self.m2_pitch*self.num_banks,0)

        # Control is placed at the top above the control bus and everything
        self.control_logic_position = vector(0, self.control_bus_offset.y + self.control_bus_height + self.m1_pitch)

        # Bank select flops get put to the right of control logic above bank1 and the buses
        # Leave a pitch to get the vdd rails up to M2
        self.msb_address_position = vector(max(self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance,self.control_logic.width),
                                           self.supply_bus_offset.y+self.supply_bus_height + 2*self.m1_pitch + self.msb_address.width)
        
    def add_busses(self):
        """ Add the horizontal and vertical busses """
        # Vertical bus
        # The order of the control signals on the control bus:
        self.control_bus_names = ["clk_buf", "tri_en_bar", "tri_en", "clk_bar", "w_en", "s_en"]
        self.vert_control_bus_positions = self.create_bus(layer="metal2",
                                                          pitch=self.m2_pitch,
                                                          offset=self.vertical_bus_offset,
                                                          names=self.control_bus_names,
                                                          length=self.vertical_bus_height,
                                                          vertical=True)

        self.addr_bus_names=["ADDR[{}]".format(i) for i in range(self.addr_size)]
        self.vert_control_bus_positions.update(self.create_bus(layer="metal2",
                                                               pitch=self.m2_pitch,
                                                               offset=self.addr_bus_offset,
                                                               names=self.addr_bus_names,
                                                               length=self.addr_bus_height,
                                                               vertical=True,
                                                               make_pins=True))

        
        self.bank_sel_bus_names = ["bank_sel[{}]".format(i) for i in range(self.num_banks)]
        self.vert_control_bus_positions.update(self.create_bus(layer="metal2",
                                                               pitch=self.m2_pitch,
                                                               offset=self.bank_sel_bus_offset,
                                                               names=self.bank_sel_bus_names,
                                                               length=self.vertical_bus_height,
                                                               vertical=True))
        

        # Horizontal data bus
        self.data_bus_names = ["DATA[{}]".format(i) for i in range(self.word_size)]
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
                                                          names=["vdd"],
                                                          length=self.supply_bus_width,
                                                          vertical=False)
        # The gnd rail must not be the entire width since we protrude the right-most vdd rail up for
        # the decoder in 4-bank SRAMs
        self.horz_control_bus_positions.update(self.create_bus(layer="metal1",
                                                               pitch=self.m1_pitch,
                                                               offset=self.supply_bus_offset+vector(0,self.m1_pitch),
                                                               names=["gnd"],
                                                               length=self.supply_bus_width-2*self.power_rail_width,
                                                               vertical=False))
        self.horz_control_bus_positions.update(self.create_bus(layer="metal1",
                                                               pitch=self.m1_pitch,
                                                               offset=self.control_bus_offset,
                                                               names=self.control_bus_names,
                                                               length=self.control_bus_width,
                                                               vertical=False))
        
    def add_two_bank_logic(self):
        """ Add the control and MSB logic """

        self.add_control_logic(position=self.control_logic_position, rotate=0)

        self.msb_address_inst = self.add_inst(name="msb_address",
                                              mod=self.msb_address,
                                              offset=self.msb_address_position,
                                              rotate=270)
        self.msb_bank_sel_addr = "ADDR[{}]".format(self.addr_size-1)
        self.connect_inst([self.msb_bank_sel_addr,"bank_sel[1]","bank_sel[0]","clk_buf", "vdd", "gnd"])

    def add_four_bank_logic(self):
        """ Add the control and MSB decode/bank select logic for four banks """


        self.add_control_logic(position=self.control_logic_position, rotate=0)

        self.msb_address_inst = self.add_inst(name="msb_address",
                                              mod=self.msb_address,
                                              offset=self.msb_address_position,
                                              rotate=270)

        self.msb_bank_sel_addr = ["ADDR[{}]".format(i) for i in range(self.addr_size-2,self.addr_size,1)]        
        temp = list(self.msb_bank_sel_addr)
        temp.extend(["msb{0}[{1}]".format(j,i) for i in range(2) for j in ["","_bar"]])
        temp.extend(["clk_buf", "vdd", "gnd"])
        self.connect_inst(temp)
        
        self.msb_decoder_inst = self.add_inst(name="msb_decoder",
                                              mod=self.msb_decoder,
                                              offset=self.msb_decoder_position,
                                              mirror="MY")
        temp = ["msb[{}]".format(i) for i in range(2)]
        temp.extend(["bank_sel[{}]".format(i) for i in range(4)])
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)
        
        
    def route_two_banks(self):
        """ Route all of the signals for the two bank SRAM. """

        self.route_shared_banks()
            
        # connect the horizontal control bus to the vertical bus
        # connect the data output to the data bus
        for n in self.data_bus_names:
            for i in [0,1]:
                pin_pos = self.bank_inst[i].get_pin(n).uc()
                rail_pos = vector(pin_pos.x,self.data_bus_positions[n].y)
                self.add_path("metal2",[pin_pos,rail_pos])
                self.add_via_center(("metal2","via2","metal3"),rail_pos)

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
            self.add_via_center(("metal2","via2","metal3"),rail_pos)


        self.route_bank_supply_rails(bottom_banks=[0,1])
        
        
    def route_double_msb_address(self):
        """ Route two MSB address bits and the bank decoder for 4-bank SRAM """
        


        # connect the MSB flops to the address input bus
        for i in [0,1]:
            msb_pins = self.msb_address_inst.get_pins("din[{}]".format(i))
            for msb_pin in msb_pins:
                if msb_pin.layer == "metal3":
                    msb_pin_pos = msb_pin.lc()
                    break
            rail_pos = vector(self.vert_control_bus_positions[self.msb_bank_sel_addr[i]].x,msb_pin_pos.y)
            self.add_path("metal3",[msb_pin_pos,rail_pos])
            self.add_via_center(("metal2","via2","metal3"),rail_pos)
        
        # Connect clk
        clk_pin = self.msb_address_inst.get_pin("clk")
        clk_pos = clk_pin.bc()
        rail_pos = self.horz_control_bus_positions["clk_buf"]
        bend_pos = vector(clk_pos.x,self.horz_control_bus_positions["clk_buf"].y)
        self.add_path("metal1",[clk_pos,bend_pos,rail_pos])

        # Connect bank decoder outputs to the bank select vertical bus wires
        for i in range(self.num_banks):
            msb_pin = self.msb_decoder_inst.get_pin("out[{}]".format(i))
            msb_pin_pos = msb_pin.lc()
            rail_pos = vector(self.vert_control_bus_positions["bank_sel[{}]".format(i)].x,msb_pin_pos.y)
            self.add_path("metal1",[msb_pin_pos,rail_pos])
            self.add_via_center(("metal1","via1","metal2"),rail_pos)

        # connect MSB flop outputs to the bank decoder inputs
        msb_pin = self.msb_address_inst.get_pin("dout[0]")
        msb_pin_pos = msb_pin.rc()
        in_pin = self.msb_decoder_inst.get_pin("in[0]")
        in_pos = in_pin.bc() + vector(0,1*self.m2_pitch,) # pin is up from bottom
        out_pos = msb_pin_pos + vector(1*self.m2_pitch,0) # route out to the right
        up_pos = vector(out_pos.x,in_pos.y) # and route up to the decoer
        self.add_wire(("metal1","via1","metal2"),[msb_pin_pos,out_pos,up_pos,in_pos])
        self.add_via_center(("metal1","via1","metal2"),in_pos)
        self.add_via_center(("metal1","via1","metal2"),msb_pin_pos,rotate=90)
            
        msb_pin = self.msb_address_inst.get_pin("dout[1]")
        msb_pin_pos = msb_pin.rc()
        in_pin = self.msb_decoder_inst.get_pin("in[1]")
        in_pos = in_pin.bc() + vector(0,self.bitcell.height+self.m2_pitch) # route the next row up
        out_pos = msb_pin_pos + vector(2*self.m2_pitch,0) # route out to the right
        up_pos = vector(out_pos.x,in_pos.y) # and route up to the decoer
        self.add_wire(("metal1","via1","metal2"),[msb_pin_pos,out_pos,up_pos,in_pos])
        self.add_via_center(("metal1","via1","metal2"),in_pos)
        self.add_via_center(("metal1","via1","metal2"),msb_pin_pos,rotate=90)
        
        # Route the right-most vdd/gnd of the right upper bank to the top of the decoder
        vdd_pins = self.bank_inst[1].get_pins("vdd")
        highest_x = None
        for bank_vdd_pin in vdd_pins:
            if highest_x == None or bank_vdd_pin.lx()>highest_x:
                highest_x = bank_vdd_pin.lx()
                bank_vdd_pos = bank_vdd_pin.ul()
        # Route to top
        self.add_rect(layer="metal1",
                      offset=bank_vdd_pos,
                      height=self.height-bank_vdd_pos.y,
                      width=bank_vdd_pin.width())

        gnd_pins = self.bank_inst[1].get_pins("gnd")
        highest_x = None
        for bank_gnd_pin in gnd_pins:
            if highest_x == None or bank_gnd_pin.lx()>highest_x:
                highest_x = bank_gnd_pin.lx()
                bank_gnd_pos = bank_gnd_pin.ul()
        # Route to top
        self.add_rect(layer="metal2",
                      offset=bank_gnd_pos,
                      height=self.height-bank_gnd_pos.y,
                      width=bank_gnd_pin.width())
        
        # Connect bank decoder vdd/gnd supplies using the previous bank_vdd_pos and bank_gnd_pos
        vdd_pins = self.msb_decoder_inst.get_pins("vdd")
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal1": continue
            vdd_pos = vdd_pin.rc()
            rail_pos = vector(bank_vdd_pos.x+bank_vdd_pin.width(),vdd_pos.y)
            self.add_path("metal1",[vdd_pos,rail_pos])
        gnd_pins = self.msb_decoder_inst.get_pins("gnd")
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal1": continue
            gnd_pos = gnd_pin.rc()
            rail_pos = vector(bank_gnd_pos.x+bank_gnd_pin.width(),gnd_pos.y)
            self.add_path("metal1",[gnd_pos,rail_pos])
            self.add_via(("metal1","via1","metal2"),rail_pos- vector(0,0.5*self.m1_width),rotate=90,size=[1,3])
        
        # connect the bank MSB flop supplies
        vdd_pins = self.msb_address_inst.get_pins("vdd")
        # vdd pins go down to the rail
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal1": continue
            vdd_pos = vdd_pin.bc()
            down_pos = vdd_pos - vector(0,self.m1_pitch)
            rail_pos = vector(vdd_pos.x,self.horz_control_bus_positions["vdd"].y)
            self.add_path("metal1",[vdd_pos,down_pos])            
            self.add_via_center(("metal1","via1","metal2"),down_pos,rotate=90)   
            self.add_path("metal2",[down_pos,rail_pos])
            self.add_via_center(("metal1","via1","metal2"),rail_pos)        
        # gnd pins go right to the rail
        gnd_pins = self.msb_address_inst.get_pins("gnd")
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal2": continue
            gnd_pos = gnd_pin.rc()
            rail_pos = vector(bank_gnd_pos.x+bank_gnd_pin.width(),gnd_pos.y)
            self.add_path("metal1",[gnd_pos,rail_pos])
            self.add_via_center(("metal1","via1","metal2"),gnd_pos,rotate=90)
            self.add_via(("metal1","via1","metal2"),rail_pos- vector(0,0.5*self.m1_width),rotate=90,size=[1,3])            
        
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
            self.add_via_center(("metal1","via1","metal2"),down_pos,rotate=90)   
            self.add_path("metal2",[down_pos,rail_pos])
            self.add_via_center(("metal1","via1","metal2"),rail_pos)
        
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
        self.add_via_center(("metal1","via1","metal2"),rail_pos)            
        
        # connect the MSB flop to the address input bus 
        msb_pins = self.msb_address_inst.get_pins("din[0]")
        for msb_pin in msb_pins:
            if msb_pin.layer == "metal3":
                msb_pin_pos = msb_pin.lc()
                break
        rail_pos = vector(self.vert_control_bus_positions[self.msb_bank_sel_addr].x,msb_pin_pos.y)
        self.add_path("metal3",[msb_pin_pos,rail_pos])
        self.add_via_center(("metal2","via2","metal3"),rail_pos)

        # Connect the output bar to select 0
        msb_out_pin = self.msb_address_inst.get_pin("dout_bar[0]")
        msb_out_pos = msb_out_pin.rc()
        out_extend_right_pos = msb_out_pos + vector(2*self.m2_pitch,0)
        out_extend_up_pos = out_extend_right_pos + vector(0,self.m2_width)
        rail_pos = vector(self.vert_control_bus_positions["bank_sel[0]"].x,out_extend_up_pos.y)
        self.add_path("metal2",[msb_out_pos,out_extend_right_pos,out_extend_up_pos])
        self.add_wire(("metal3","via2","metal2"),[out_extend_right_pos,out_extend_up_pos,rail_pos])
        self.add_via_center(("metal2","via2","metal3"),rail_pos)
        
        # Connect the output to select 1
        msb_out_pin = self.msb_address_inst.get_pin("dout[0]")
        msb_out_pos = msb_out_pin.rc()
        out_extend_right_pos = msb_out_pos + vector(2*self.m2_pitch,0)
        out_extend_down_pos = out_extend_right_pos - vector(0,2*self.m1_pitch)
        rail_pos = vector(self.vert_control_bus_positions["bank_sel[1]"].x,out_extend_down_pos.y)
        self.add_path("metal2",[msb_out_pos,out_extend_right_pos,out_extend_down_pos])
        self.add_wire(("metal3","via2","metal2"),[out_extend_right_pos,out_extend_down_pos,rail_pos])
        self.add_via_center(("metal2","via2","metal3"),rail_pos)
        
        # Connect clk
        clk_pin = self.msb_address_inst.get_pin("clk")
        clk_pos = clk_pin.bc()
        rail_pos = self.horz_control_bus_positions["clk_buf"]
        bend_pos = vector(clk_pos.x,self.horz_control_bus_positions["clk_buf"].y)
        self.add_path("metal1",[clk_pos,bend_pos,rail_pos])
        


    def route_bank_supply_rails(self, bottom_banks):
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


        # route bank vertical rails to bottom
        for i in bottom_banks:
            vdd_pins = self.bank_inst[i].get_pins("vdd")
            for vdd_pin in vdd_pins:
                vdd_pos = vdd_pin.ul()
                # Route to bottom
                self.add_rect(layer="metal1",
                              offset=vector(vdd_pos.x,self.power_rail_pitch),
                              height=self.horz_control_bus_positions["vdd"].y-self.power_rail_pitch, 
                              width=vdd_pin.width())

            gnd_pins = self.bank_inst[i].get_pins("gnd")
            for gnd_pin in gnd_pins:
                gnd_pos = gnd_pin.ul()                
                # Route to bottom
                self.add_rect(layer="metal2",
                              offset=vector(gnd_pos.x,0),
                              height=self.horz_control_bus_positions["gnd"].y, # route to the top bank
                              width=gnd_pin.width())
                # Add vias at top
                right_rail_pos = vector(gnd_pin.ur().x,self.horz_control_bus_positions["gnd"].y)            
                self.add_via(layers=("metal1","via1","metal2"),
                             offset=right_rail_pos - vector(0,0.5*self.m1_width),
                             rotate=90,
                             size=[1,3]) 
                # Add vias at bottom 
                right_rail_pos = vector(gnd_pin.lr().x,0)          
                self.add_via(layers=("metal2","via2","metal3"),
                             offset=right_rail_pos,
                             rotate=90,
                             size=[2,3]) 
                
        
        
    def create_multi_bank_modules(self):
        """ Create the multibank address flops and bank decoder """
        self.msb_address = self.mod_ms_flop_array(name="msb_address",
                                                  columns=self.num_banks/2,
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
        self.power_rail_pitch = self.bank.vdd_rail_width + 2*self.m3_space



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

    def add_single_bank_modules(self):
        """ 
        This adds the moduels for a single bank SRAM with control
        logic. 
        """
        
        # No orientation or offset
        self.bank_inst = self.add_bank(0, [0, 0], 1, 1)
        
        # Control logic is placed to the left of the blank even with the
        # decoder bottom. A small gap is in the x-dimension.
        control_gap = 2*self.m3_width
        pos = vector(-control_gap,
                     self.bank.row_decoder_inst.by() + 2*self.m3_width)
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


    def add_two_banks(self):
        # Placement of bank 0 (left)
        bank_position_0 = vector(self.bank.width,
                                 self.bank.height + 2*self.power_rail_pitch)
        self.bank_inst=[self.add_bank(0, bank_position_0, -1, -1)]

        # Placement of bank 1 (right)
        x_off = self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance
        bank_position_1 = vector(x_off, bank_position_0.y)
        self.bank_inst.append(self.add_bank(1, bank_position_1, -1, 1))


    def add_four_banks(self):
        
        # Placement of bank 0 (upper left)
        bank_position_0 = vector(self.bank.width,
                                 self.bank.height + self.data_bus_height + 2*self.bank_to_bus_distance + 2*self.power_rail_pitch)
        self.bank_inst=[self.add_bank(0, bank_position_0, 1, -1)]

        # Placement of bank 1 (upper right)
        x_off = self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance
        bank_position_1 = vector(x_off, bank_position_0.y)
        self.bank_inst.append(self.add_bank(1, bank_position_1, 1, 1))

        # Placement of bank 2 (bottom left)
        y_off = self.bank.height + 2*self.power_rail_pitch
        bank_position_2 = vector(bank_position_0.x, y_off)
        self.bank_inst.append(self.add_bank(2, bank_position_2, -1, -1))

        # Placement of bank 3 (bottom right)
        bank_position_3 = vector(bank_position_1.x, bank_position_2.y)
        self.bank_inst.append(self.add_bank(3, bank_position_3, -1, 1))
        

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

    def save_output(self):
        """ Save all the output files while reporting time to do it as well. """

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.name + ".sp"
        print("SP: Writing to {0}".format(spname))
        self.sp_write(spname)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            sp_file = OPTS.output_path + "temp_pex.sp"
            verify.run_pex(self.name, gdsname, spname, output=sp_file)
            print_time("Extraction", datetime.datetime.now(), start_time)
        else:
            # Use generated spice file for characterization
            sp_file = spname
        
        # Characterize the design
        start_time = datetime.datetime.now()        
        from characterizer import lib
        print("LIB: Characterizing... ")
        if OPTS.analytical_delay:
            print("Using analytical delay models (no characterization)")
        else:
            if OPTS.spice_name!="":
                print("Performing simulation-based characterization with {}".format(OPTS.spice_name))
            if OPTS.trim_netlist:
                print("Trimming netlist to speed up characterization.")
        lib.lib(out_dir=OPTS.output_path, sram=self, sp_file=sp_file)
        print_time("Characterization", datetime.datetime.now(), start_time)

        # Write the layout
        start_time = datetime.datetime.now()
        gdsname = OPTS.output_path + self.name + ".gds"
        print("GDS: Writing to {0}".format(gdsname))
        self.gds_write(gdsname)
        print_time("GDS", datetime.datetime.now(), start_time)

        # Create a LEF physical model
        start_time = datetime.datetime.now()
        lefname = OPTS.output_path + self.name + ".lef"
        print("LEF: Writing to {0}".format(lefname))
        self.lef_write(lefname)
        print_time("LEF", datetime.datetime.now(), start_time)

        # Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + self.name + ".v"
        print("Verilog: Writing to {0}".format(vname))
        self.verilog_write(vname)
        print_time("Verilog", datetime.datetime.now(), start_time)
