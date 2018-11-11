import sys
from tech import drc, spice
import debug
from math import log,sqrt,ceil
import datetime
import getpass
import numpy as np
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
    def __init__(self, name, sram_config):
        sram_base.__init__(self, name, sram_config)
        

    def create_netlist(self):
        sram_base.create_netlist(self)
        self.create_modules()

    def create_modules(self):
        """ 
        This adds the modules for a single bank SRAM with control
        logic. 
        """
        
        self.bank_inst=self.create_bank(0)

        self.control_logic_inst = self.create_control_logic()

        self.row_addr_dff_inst = self.create_row_addr_dff()

        if self.col_addr_dff:
            self.col_addr_dff_inst = self.create_col_addr_dff()
        
        self.data_dff_inst = self.create_data_dff()
        
    def place_modules(self):
        """ 
        This places the modules for a single bank SRAM with control
        logic. 
        """
        
        # No orientation or offset
        self.place_bank(self.bank_inst, [0, 0], 1, 1)

        # The control logic is placed such that the vertical center (between the delay/RBL and
        # the actual control logic is aligned with the vertical center of the bank (between
        # the sense amps/column mux and cell array)
        # The x-coordinate is placed to allow a single clock wire (plus an extra pitch)
        # up to the row address DFFs.
        for port in self.all_ports:
            control_pos = vector(-self.control_logic.width - 2*self.m2_pitch,
                                 self.bank.bank_center.y - self.control_logic.control_logic_center.y)
            self.control_logic_inst[port].place(control_pos)

            # The row address bits are placed above the control logic aligned on the right.
            row_addr_pos = vector(self.control_logic_inst[0].rx() - self.row_addr_dff.width,
                                  self.control_logic_inst[0].uy())
            self.row_addr_dff_inst[port].place(row_addr_pos)

            # This is M2 pitch even though it is on M1 to help stem via spacings on the trunk
            data_gap = -self.m2_pitch*(self.word_size+1)
            
            # Add the column address below the bank under the control
            # The column address flops are aligned with the data flops
            if self.col_addr_dff:
                col_addr_pos = vector(self.bank.bank_center.x - self.col_addr_dff.width - self.bank.central_bus_width,
                                      data_gap - self.col_addr_dff.height)
                self.col_addr_dff_inst[port].place(col_addr_pos)
            
            # Add the data flops below the bank to the right of the center of bank:
            # This relies on the center point of the bank:
            # decoder in upper left, bank in upper right, sensing in lower right.
            # These flops go below the sensing and leave a gap to channel route to the
            # sense amps.
            data_pos = vector(self.bank.bank_center.x,
                              data_gap - self.data_dff.height)
            self.data_dff_inst[port].place(data_pos)
            
            # two supply rails are already included in the bank, so just 2 here.
            # self.width = self.bank.width + self.control_logic.width + 2*self.supply_rail_pitch
            # self.height = self.bank.height 
        
    def add_layout_pins(self):
        """
        Add the top-level pins for a single bank SRAM with control.
        """
        for port in self.all_ports:
            # Connect the control pins as inputs
            for signal in self.control_logic_inputs[port] + ["clk"]:
                self.copy_layout_pin(self.control_logic_inst[port], signal, signal+"{}".format(port))

            if port in self.read_ports:
                for bit in range(self.word_size):
                    self.copy_layout_pin(self.bank_inst, "dout{0}_{1}".format(port,bit), "DOUT{0}[{1}]".format(port,bit))

            # Lower address bits
            for bit in range(self.col_addr_size):
                self.copy_layout_pin(self.col_addr_dff_inst[port], "din_{}".format(bit),"ADDR{0}[{1}]".format(port,bit))
            # Upper address bits
            for bit in range(self.row_addr_size):
                self.copy_layout_pin(self.row_addr_dff_inst[port], "din_{}".format(bit),"ADDR{0}[{1}]".format(port,bit+self.col_addr_size))

            if port in self.write_ports:
                for bit in range(self.word_size):
                    self.copy_layout_pin(self.data_dff_inst[port], "din_{}".format(bit), "DIN{0}[{1}]".format(port,bit))
            
    def route(self):
        """ Route a single bank SRAM """

        self.add_layout_pins()

        self.route_clk()
        
        self.route_control_logic()
        
        self.route_row_addr_dff()

        if self.col_addr_dff:
            self.route_col_addr_dff()
        
        self.route_data_dff()

    def route_clk(self):
        """ Route the clock network """

        # This is the actual input to the SRAM
        for port in self.all_ports:
            self.copy_layout_pin(self.control_logic_inst[port], "clk", "clk{}".format(port))

            # Connect all of these clock pins to the clock in the central bus
            # This is something like a "spine" clock distribution. The two spines
            # are clk_buf and clk_buf_bar
            
            bank_clk_buf_pin = self.bank_inst.get_pin("clk_buf{}".format(port))
            bank_clk_buf_pos = bank_clk_buf_pin.center()
            bank_clk_buf_bar_pin = self.bank_inst.get_pin("clk_buf_bar{}".format(port))
            bank_clk_buf_bar_pos = bank_clk_buf_bar_pin.center()

            if self.col_addr_dff:
                dff_clk_pin = self.col_addr_dff_inst[port].get_pin("clk")
                dff_clk_pos = dff_clk_pin.center()
                mid_pos = vector(bank_clk_buf_pos.x, dff_clk_pos.y)
                self.add_wire(("metal3","via2","metal2"),[dff_clk_pos, mid_pos, bank_clk_buf_pos])
            
            data_dff_clk_pin = self.data_dff_inst[port].get_pin("clk")
            data_dff_clk_pos = data_dff_clk_pin.center()
            mid_pos = vector(bank_clk_buf_pos.x, data_dff_clk_pos.y)
            self.add_wire(("metal3","via2","metal2"),[data_dff_clk_pos, mid_pos, bank_clk_buf_pos])

            # This uses a metal2 track to the right of the control/row addr DFF
            # to route vertically.
            control_clk_buf_pin = self.control_logic_inst[port].get_pin("clk_buf")
            control_clk_buf_pos = control_clk_buf_pin.rc()
            row_addr_clk_pin = self.row_addr_dff_inst[port].get_pin("clk")
            row_addr_clk_pos = row_addr_clk_pin.rc()
            mid1_pos = vector(self.row_addr_dff_inst[port].rx() + self.m2_pitch,
                              row_addr_clk_pos.y)
            mid2_pos = vector(mid1_pos.x,
                              control_clk_buf_pos.y)
            # Note, the via to the control logic is taken care of when we route
            # the control logic to the bank
            self.add_wire(("metal3","via2","metal2"),[row_addr_clk_pos, mid1_pos, mid2_pos, control_clk_buf_pos])
        
            
    def route_control_logic(self):
        """ Route the outputs from the control logic module """
        for port in self.all_ports:
            for signal in self.control_logic_outputs[port]:
                src_pin = self.control_logic_inst[port].get_pin(signal)
                dest_pin = self.bank_inst.get_pin(signal+"{}".format(port))                
                self.connect_rail_from_left_m2m3(src_pin, dest_pin)
                self.add_via_center(layers=("metal1","via1","metal2"),
                                    offset=src_pin.rc(),
                                    rotate=90)
            

    def route_row_addr_dff(self):
        """ Connect the output of the row flops to the bank pins """
        for port in self.all_ports:
            for bit in range(self.row_addr_size):
                flop_name = "dout_{}".format(bit)
                bank_name = "addr{0}_{1}".format(port,bit+self.col_addr_size)
                flop_pin = self.row_addr_dff_inst[port].get_pin(flop_name)
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
        for port in self.all_ports:
            bus_names = ["addr_{}".format(x) for x in range(self.col_addr_size)]        
            col_addr_bus_offsets = self.create_horizontal_bus(layer="metal1",
                                                              pitch=self.m1_pitch,
                                                              offset=self.col_addr_dff_inst[port].ul() + vector(0, self.m1_pitch),
                                                              names=bus_names,
                                                              length=self.col_addr_dff_inst[port].width)

            dff_names = ["dout_{}".format(x) for x in range(self.col_addr_size)]
            data_dff_map = zip(dff_names, bus_names)
            self.connect_horizontal_bus(data_dff_map, self.col_addr_dff_inst[port], col_addr_bus_offsets)
            
            bank_names = ["addr{0}_{1}".format(port,x) for x in range(self.col_addr_size)]
            data_bank_map = zip(bank_names, bus_names)
            self.connect_horizontal_bus(data_bank_map, self.bank_inst, col_addr_bus_offsets)
        

    def route_data_dff(self):
        """ Connect the output of the data flops to the write driver """
        # This is where the channel will start (y-dimension at least)
        for port in self.write_ports:
            offset = self.data_dff_inst[port].ul() + vector(0, 2*self.m1_pitch)

            dff_names = ["dout_{}".format(x) for x in range(self.word_size)]
            bank_names = ["din{0}_{1}".format(port,x) for x in range(self.word_size)]

            route_map = list(zip(bank_names, dff_names))
            dff_pins = {key: self.data_dff_inst[port].get_pin(key) for key in dff_names }
            bank_pins = {key: self.bank_inst.get_pin(key) for key in bank_names }
            # Combine the dff and bank pins into a single dictionary of pin name to pin.
            all_pins = {**dff_pins, **bank_pins}
            self.create_horizontal_channel_route(route_map, all_pins, offset)
                
            

    def add_lvs_correspondence_points(self):
        """ 
        This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        
        for n in self.control_logic_outputs[0]:
            pin = self.control_logic_inst[0].get_pin(n)
            self.add_label(text=n,
                           layer=pin.layer,
                           offset=pin.center())
