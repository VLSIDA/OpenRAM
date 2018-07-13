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


class sram_1bank(sram_base):
    """
    Procedures specific to a one bank SRAM.
    """
    def __init__(self, word_size, num_words, name):
        sram_base.__init__(self, word_size, num_words, 1, name)

    def add_modules(self):
        """ 
        This adds the moduels for a single bank SRAM with control
        logic. 
        """
        
        # No orientation or offset
        self.bank_inst = self.add_bank(0, [0, 0], 1, 1)

        # 3/5/18 MRG: Cannot reference positions inside submodules because boundaries
        # are not recomputed using instance placement. So, place the control logic such that it aligns
        # with the top of the SRAM.
        control_pos = vector(-self.control_logic.width - self.m3_pitch,
                             3*self.supply_rail_width)
        self.add_control_logic(position=control_pos)

        # Leave room for the control routes to the left of the flops
        addr_pos = vector(self.control_logic_inst.lx() + 4*self.m2_pitch,
                          control_pos.y + self.control_logic.height + self.m1_pitch)
        self.add_addr_dff(addr_pos)

        # Leave room for the control routes to the left of the flops
        data_pos = vector(self.control_logic_inst.lx() + 4*self.m2_pitch,
                          control_pos.y + self.control_logic.height + self.m1_pitch)
        self.add_addr_dff(addr_pos)
        
        # two supply rails are already included in the bank, so just 2 here.
        self.width = self.bank.width + self.control_logic.width + 2*self.supply_rail_pitch
        self.height = self.bank.height 

    def add_layout_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """

        for i in range(self.word_size):
            self.copy_layout_pin(self.bank_inst, "DOUT[{}]".format(i))
            
        for i in range(self.addr_size):
            self.copy_layout_pin(self.addr_dff_inst, "din[{}]".format(i),"ADDR[{}]".format(i))

        for i in range(self.word_size):
            self.copy_layout_pin(self.addr_dff_inst, "din[{}]".format(i),"ADDR[{}]".format(i))
            
    def route(self):
        """ Route a single bank SRAM """

        self.add_layout_pins()
        
        # Route the outputs from the control logic module
        for n in self.control_logic_outputs:
            src_pin = self.control_logic_inst.get_pin(n)
            dest_pin = self.bank_inst.get_pin(n)                
            self.connect_rail_from_left_m2m3(src_pin, dest_pin)
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=src_pin.rc(),
                                rotate=90)
            

        # Connect the output of the flops to the bank pins
        for i in range(self.addr_size):
            flop_name = "dout[{}]".format(i)
            bank_name = "A[{}]".format(i)
            flop_pin = self.addr_dff_inst.get_pin(flop_name)
            bank_pin = self.bank_inst.get_pin(bank_name)
            flop_pos = flop_pin.center()
            bank_pos = vector(bank_pin.cx(),flop_pos.y)
            self.add_path("metal3",[flop_pos, bank_pos])
            self.add_via_center(layers=("metal2","via2","metal3"),
                                offset=flop_pos,
                                rotate=90)
            self.add_via_center(layers=("metal2","via2","metal3"),
                                offset=bank_pos,
                                rotate=90)

        # Connect the control pins as inputs
        for n in self.control_logic_inputs + ["clk"]:
            self.copy_layout_pin(self.control_logic_inst, n)

        # Connect the clock between the flops and control module
        flop_pin = self.addr_dff_inst.get_pin("clk")
        ctrl_pin = self.control_logic_inst.get_pin("clk_buf")
        flop_pos = flop_pin.uc()
        ctrl_pos = ctrl_pin.bc()
        mid_ypos = 0.5*(ctrl_pos.y+flop_pos.y)
        mid1_pos = vector(flop_pos.x, mid_ypos)
        mid2_pos = vector(ctrl_pos.x, mid_ypos)                
        self.add_wire(("metal1","via1","metal2"),[flop_pin.uc(), mid1_pos, mid2_pos, ctrl_pin.bc()])  

