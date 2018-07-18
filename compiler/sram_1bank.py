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

        control_pos = vector(-self.control_logic.width - self.m3_pitch,
                             self.bank.bank_center.y - self.control_logic.control_logic_center.y)
        self.add_control_logic(position=control_pos)

        # Leave room for the control routes to the left of the flops
        row_addr_pos = vector(self.control_logic_inst.rx() - self.row_addr_dff.width,
                          control_pos.y + self.control_logic.height + self.m1_pitch)
        self.add_row_addr_dff(row_addr_pos)

        data_gap = -self.m2_pitch*(self.word_size+1)
        
        # Add the column address below the bank under the control
        # Keep it aligned with the data flops
        if self.col_addr_dff:
            col_addr_pos = vector(self.bank.bank_center.x - self.col_addr_dff.width - self.bank.central_bus_width,
                                  data_gap - self.col_addr_dff.height)
            self.add_col_addr_dff(col_addr_pos)
        
        # Add the data flops below the bank
        # This relies on the center point of the bank:
        # decoder in upper left, bank in upper right, sensing in lower right.
        # These flops go below the sensing and leave a gap to channel route to the
        # sense amps.
        data_pos = vector(self.bank.bank_center.x,
                          data_gap - self.data_dff.height)
        self.add_data_dff(data_pos)
        
        # two supply rails are already included in the bank, so just 2 here.
        self.width = self.bank.width + self.control_logic.width + 2*self.supply_rail_pitch
        self.height = self.bank.height 

    def add_layout_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """
        # Connect the control pins as inputs
        for n in self.control_logic_inputs + ["clk"]:
            self.copy_layout_pin(self.control_logic_inst, n)

        for i in range(self.word_size):
            self.copy_layout_pin(self.bank_inst, "DOUT[{}]".format(i))

        # Lower address bits
        for i in range(self.col_addr_size):
            self.copy_layout_pin(self.col_addr_dff_inst, "din[{}]".format(i),"ADDR[{}]".format(i))
        # Upper address bits
        for i in range(self.row_addr_size):
            self.copy_layout_pin(self.row_addr_dff_inst, "din[{}]".format(i),"ADDR[{}]".format(i+self.col_addr_size))

        for i in range(self.word_size):
            self.copy_layout_pin(self.data_dff_inst, "din[{}]".format(i),"DIN[{}]".format(i))
            
    def route(self):
        """ Route a single bank SRAM """

        self.add_layout_pins()

        self.route_vdd_gnd()

        self.route_clk()
        
        self.route_control_logic()
        
        self.route_row_addr_dff()

        if self.col_addr_dff:
            self.route_col_addr_dff()
        
        self.route_data_dff()

    def route_clk(self):
        """ Route the clock network """
        debug.warning("Clock is top-level must connect.")
        # For now, just have four clock pins for the address (x2), data, and control
        if self.col_addr_dff:
            self.copy_layout_pin(self.col_addr_dff_inst, "clk")
        self.copy_layout_pin(self.row_addr_dff_inst, "clk")
        self.copy_layout_pin(self.data_dff_inst, "clk")
        self.copy_layout_pin(self.control_logic_inst, "clk")
        
    def route_vdd_gnd(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        # These are the instances that every bank has
        top_instances = [self.bank_inst,
                         self.row_addr_dff_inst,
                         self.data_dff_inst,
                         self.control_logic_inst]
        if self.col_addr_dff:
            top_instances.append(self.col_addr_dff_inst)

                         
        for inst in top_instances:
            self.copy_layout_pin(inst, "vdd")
            self.copy_layout_pin(inst, "gnd")
        
    def route_control_logic(self):
        """ Route the outputs from the control logic module """
        for n in self.control_logic_outputs:
            src_pin = self.control_logic_inst.get_pin(n)
            dest_pin = self.bank_inst.get_pin(n)                
            self.connect_rail_from_left_m2m3(src_pin, dest_pin)
            self.add_via_center(layers=("metal1","via1","metal2"),
                                offset=src_pin.rc(),
                                rotate=90)
            

    def route_row_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """
        for i in range(self.row_addr_size):
            flop_name = "dout[{}]".format(i)
            bank_name = "A[{}]".format(i+self.col_addr_size)
            flop_pin = self.row_addr_dff_inst.get_pin(flop_name)
            bank_pin = self.bank_inst.get_pin(bank_name)
            flop_pos = flop_pin.center()
            bank_pos = bank_pin.center()
            mid_pos = vector(bank_pos.x,flop_pos.y)
            self.add_wire(("metal3","via2","metal2"),[flop_pos, mid_pos,bank_pos])
            self.add_via_center(layers=("metal2","via2","metal3"),
                                offset=flop_pos,
                                rotate=90)

    def route_col_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """

        bus_names = ["A[{}]".format(x) for x in range(self.col_addr_size)]        
        col_addr_bus_offsets = self.create_horizontal_bus(layer="metal1",
                                                          pitch=self.m1_pitch,
                                                          offset=self.col_addr_dff_inst.ul() + vector(0, self.m1_pitch),
                                                          names=bus_names,
                                                          length=self.col_addr_dff_inst.width)

        dff_names = ["dout[{}]".format(x) for x in range(self.col_addr_size)]
        data_dff_map = zip(dff_names, bus_names)
        self.connect_horizontal_bus(data_dff_map, self.col_addr_dff_inst, col_addr_bus_offsets)
        
        bank_names = ["A[{}]".format(x) for x in range(self.col_addr_size)]
        data_bank_map = zip(bank_names, bus_names)
        self.connect_horizontal_bus(data_bank_map, self.bank_inst, col_addr_bus_offsets)
        

    def route_data_dff(self):
        """ Connect the output of the data flops to the write driver """
        # Create a horizontal bus
        bus_names = ["data[{}]".format(x) for x in range(self.word_size)]        
        data_bus_offsets = self.create_horizontal_bus(layer="metal1",
                                                      pitch=self.m1_pitch,
                                                      offset=self.data_dff_inst.ul() + vector(0, self.m1_pitch),
                                                      names=bus_names,
                                                      length=self.data_dff_inst.width)


        dff_names = ["dout[{}]".format(x) for x in range(self.word_size)]
        data_dff_map = zip(dff_names, bus_names)
        self.connect_horizontal_bus(data_dff_map, self.data_dff_inst, data_bus_offsets)
        
        bank_names = ["BANK_DIN[{}]".format(x) for x in range(self.word_size)]
        data_bank_map = zip(bank_names, bus_names)
        self.connect_horizontal_bus(data_bank_map, self.bank_inst, data_bus_offsets)

                
            

    def add_lvs_correspondence_points(self):
        """ 
        This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        
        for n in self.control_logic_outputs:
            self.add_label(text=n,
                           layer="metal3",  
                           offset=self.control_logic_inst.get_pin(n).center())
