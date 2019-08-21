# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
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

class sram_2bank(sram_base):
    """
    Procedures specific to a two bank SRAM.
    """
    def __init__(self, name, sram_config):
        sram_base.__init__(self, name, sram_config)

    def compute_bank_offsets(self):
        """ Compute the overall offsets for a two bank SRAM """

        # In 2 bank SRAM, the height is determined by the control bus which is higher than the msb address
        self.vertical_bus_height = self.bank.height + 2*self.bank_to_bus_distance + self.data_bus_height + self.control_bus_height
        # The address bus extends down through the power rails, but control and bank_sel bus don't
        self.addr_bus_height = self.vertical_bus_height 
        
        self.vertical_bus_offset = vector(self.bank.width + self.bank_to_bus_distance, 0)
        self.data_bus_offset = vector(0, self.bank.height + self.bank_to_bus_distance)
        self.supply_bus_offset = vector(0, self.data_bus_offset.y + self.data_bus_height)        
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
    
    def add_modules(self):
        """ Adds the modules and the buses to the top level """

        self.compute_bus_sizes()

        self.add_banks()
        
        self.compute_bank_offsets()

        self.add_busses()

        self.add_logic()

        self.width = self.bank_inst[1].ur().x
        self.height = self.control_logic_inst.uy()



    def add_banks(self):
        # Placement of bank 0 (left)
        bank_position_0 = vector(self.bank.width,
                                 self.bank.height)
        self.bank_inst=[self.add_bank(0, bank_position_0, -1, -1)]

        # Placement of bank 1 (right)
        x_off = self.bank.width + self.vertical_bus_width + 2*self.bank_to_bus_distance
        bank_position_1 = vector(x_off, bank_position_0.y)
        self.bank_inst.append(self.add_bank(1, bank_position_1, -1, 1))

    def add_logic(self):
        """ Add the control and MSB logic """

        self.add_control_logic(position=self.control_logic_position)

        self.msb_address_inst = self.add_inst(name="msb_address",
                                              mod=self.msb_address,
                                              offset=self.msb_address_position,
                                              rotate=270)
        self.msb_bank_sel_addr = "addr[{}]".format(self.addr_size-1)
        self.connect_inst([self.msb_bank_sel_addr,"bank_sel[1]","bank_sel[0]","clk_buf", "vdd", "gnd"])
        

    def route_shared_banks(self):
        """ Route the shared signals for two and four bank configurations. """

        # create the input control pins
        for n in self.control_logic_inputs + ["clk"]:
            self.copy_layout_pin(self.control_logic_inst, n)
            
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
        

            
    def route(self):
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


        
    def add_lvs_correspondence_points(self):
        """ 
        This adds some points for easier debugging if LVS goes wrong. 
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
