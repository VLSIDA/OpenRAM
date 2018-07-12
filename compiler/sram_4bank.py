import sys
from tech import drc, spice
import debug
from math import log,sqrt,ceil
import datetime
import getpass
from vector import vector
from globals import OPTS, print_time

from sram_base import sram_base
from bank import bank
from dff_buf_array import dff_buf_array
from dff_array import dff_array

class sram_4bank(sram_base):
    """
    Procedures specific to a four bank SRAM.
    """
    def __init__(self, word_size, num_words, name):
        sram_base.__init__(self, word_size, num_words, 4, name)

    def whoami(self):
        print("4bank")
        
    def compute_bank_offsets(self):
        """ Compute the overall offsets for a four bank SRAM """

        # The main difference is that the four bank SRAM has the data bus in the middle of the four banks
        # as opposed to the top of the banks.
        
        # In 4 bank SRAM, the height is determined by the bank decoder and address flop
        self.vertical_bus_height = 2*self.bank.height + 4*self.bank_to_bus_distance + self.data_bus_height \
                                   + self.supply_bus_height + self.msb_decoder.height + self.msb_address.width 
        # The address bus extends down through the power rails, but control and bank_sel bus don't
        self.addr_bus_height = self.vertical_bus_height

        self.vertical_bus_offset = vector(self.bank.width + self.bank_to_bus_distance, 0)
        self.data_bus_offset = vector(0, self.bank.height + self.bank_to_bus_distance)
        self.supply_bus_offset = vector(0, self.data_bus_offset.y + self.data_bus_height \
                                        + self.bank.height + 2*self.bank_to_bus_distance)        
        self.control_bus_offset = vector(0, self.supply_bus_offset.y + self.supply_bus_height)
        self.bank_sel_bus_offset = self.vertical_bus_offset + vector(self.m2_pitch*self.control_size,0)
        self.addr_bus_offset = self.bank_sel_bus_offset.scale(1,0) + vector(self.m2_pitch*self.num_banks,0)

        # Control is placed at the top above the control bus and everything
        self.control_logic_position = vector(0, self.control_bus_offset.y + self.control_bus_height + self.m1_pitch)

        # Bank select flops get put to the right of control logic above bank1 and the buses
        # Leave a pitch to get the vdd rails up to M2
        self.msb_address_position = vector(self.bank_inst[1].lx() + 3*self.supply_rail_pitch,
                                           self.supply_bus_offset.y + self.supply_bus_height \
                                           + 2*self.m1_pitch + self.msb_address.width)

        # Decoder goes above the MSB address flops, and is flipped in Y
        # separate the two by a bank to bus distance for nwell rules, just in case
        self.msb_decoder_position = self.msb_address_position + vector(self.msb_decoder.width, self.bank_to_bus_distance)

    
    def add_modules(self):
        """ Adds the modules and the buses to the top level """

        self.compute_bus_sizes()

        self.add_banks()

        self.compute_bank_offsets()

        self.add_busses()

        self.add_logic()
        
        self.width = self.bank_inst[1].ur().x
        self.height = max(self.control_logic_inst.uy(),self.msb_decoder_inst.uy())

    def add_banks(self):
        
        # Placement of bank 0 (upper left)
        bank_position_0 = vector(self.bank.width,
                                 self.bank.height + self.data_bus_height + 2*self.bank_to_bus_distance)
        self.bank_inst=[self.add_bank(0, bank_position_0, 1, -1)]

        # Placement of bank 1 (upper right)
        x_off = self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance
        bank_position_1 = vector(x_off, bank_position_0.y)
        self.bank_inst.append(self.add_bank(1, bank_position_1, 1, 1))

        # Placement of bank 2 (bottom left)
        y_off = self.bank.height
        bank_position_2 = vector(bank_position_0.x, y_off)
        self.bank_inst.append(self.add_bank(2, bank_position_2, -1, -1))

        # Placement of bank 3 (bottom right)
        bank_position_3 = vector(bank_position_1.x, bank_position_2.y)
        self.bank_inst.append(self.add_bank(3, bank_position_3, -1, 1))
        

        
    def add_logic(self):
        """ Add the control and MSB decode/bank select logic for four banks """


        self.add_control_logic(position=self.control_logic_position)

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

        self.route_double_msb_address_supplies()
        
    def route_double_msb_address_supplies(self):
        """ Route the vdd/gnd bits of the 2-bit bank decoder. """
        
        # Route the right-most vdd/gnd of the right upper bank to the top of the decoder
        vdd_pins = self.bank_inst[1].get_pins("vdd")
        left_bank_vdd_pin = None
        right_bank_vdd_pin = None
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal2":
                continue
            if left_bank_vdd_pin == None or vdd_pin.lx()<left_bank_vdd_pin.lx():
                left_bank_vdd_pin = vdd_pin
            if right_bank_vdd_pin == None or vdd_pin.lx()>right_bank_vdd_pin.lx():
                right_bank_vdd_pin = vdd_pin
            # Route to top
            self.add_rect(layer="metal2",
                          offset=vdd_pin.ul(),
                          height=self.height-vdd_pin.uy(),
                          width=vdd_pin.width())

        gnd_pins = self.bank_inst[1].get_pins("gnd")
        left_bank_gnd_pin = None
        right_bank_gnd_pin = None
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal2":
                continue
            if left_bank_gnd_pin == None or gnd_pin.lx()<left_bank_gnd_pin.lx():
                left_bank_gnd_pin = gnd_pin
            if right_bank_gnd_pin == None or gnd_pin.lx()>right_bank_gnd_pin.lx():
                right_bank_gnd_pin = gnd_pin
            # Route to top
            self.add_rect(layer="metal2",
                          offset=gnd_pin.ul(),
                          height=self.height-gnd_pin.uy(),
                          width=gnd_pin.width())
        
        # Connect bank decoder vdd/gnd supplies using the previous bank pins
        vdd_pins = self.msb_decoder_inst.get_pins("vdd")
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal1":
                continue
            rail1_pos = vector(left_bank_vdd_pin.cx(),vdd_pin.cy())
            rail2_pos = vector(right_bank_vdd_pin.cx(),vdd_pin.cy())
            self.add_path("metal1",[rail1_pos,rail2_pos])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=rail1_pos,
                                rotate=90,
                                size=[1,3])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=rail2_pos,
                                rotate=90,
                                size=[1,3])
        gnd_pins = self.msb_decoder_inst.get_pins("gnd")
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal1":
                continue
            rail1_pos = vector(left_bank_gnd_pin.cx(),gnd_pin.cy())
            rail2_pos = vector(right_bank_gnd_pin.cx(),gnd_pin.cy())
            self.add_path("metal1",[rail1_pos,rail2_pos])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=rail1_pos,
                                rotate=90,
                                size=[1,3])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=rail2_pos,
                                rotate=90,
                                size=[1,3])
        
        # connect the bank MSB flop supplies
        vdd_pins = self.msb_address_inst.get_pins("vdd")
        # vdd pins go down to the rail
        for vdd_pin in vdd_pins:
            if vdd_pin.layer != "metal1":
                continue
            vdd_pos = vdd_pin.bc()
            down_pos = vdd_pos - vector(0,self.m1_pitch)
            rail_pos = vector(vdd_pos.x,self.horz_control_bus_positions["vdd"].y)
            self.add_path("metal1",[vdd_pos,down_pos])            
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=down_pos,
                                rotate=90)   
            self.add_path("metal2",[down_pos,rail_pos])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=rail_pos)        
        # gnd pins go right to the rail
        gnd_pins = self.msb_address_inst.get_pins("gnd")
        for gnd_pin in gnd_pins:
            if gnd_pin.layer != "metal2":
                continue
            rail1_pos = vector(left_bank_gnd_pin.cx(),gnd_pin.cy())
            self.add_path("metal1",[rail1_pos,gnd_pin.lc()])
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=gnd_pin.lc(),
                                rotate=90)
            self.add_via_center(layers=("metal1","via1","metal2"),
                         offset=rail1_pos,
                         rotate=90,
                         size=[1,3])            
        
        
    def route(self):
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
            

        self.route_bank_supply_rails(left_banks=[0,2], bottom_banks=[2,3])


