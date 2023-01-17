# See LICENSE for licensing information.
#
# Copyright (c) 2016-2022 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from openram.sram_factory import factory
from openram.base import vector, design


class rom_control_logic(design):
    def __init__(self, num_outputs, name="", height=None):
        self.output_size = num_outputs
        self.mod_height = height

        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"

        # dff = factory.create(module_type="dff")
        
        # if height == None:
        #     self.mod_height = dff.height * 0.5
        # else: 
        #     self.mod_height = height

        super().__init__(name)
        self.create_netlist()
        self.create_layout()
        self.add_boundary()
        

    def create_netlist(self):
        self.add_modules()
        self.add_pins()

    def create_layout(self):
        self.create_instances()
        self.height=self.nand_inst.height
        self.width=self.nand_inst.width + self.inv_inst.width + self.driver_inst.width
        self.place_instances()
        self.route_insts()

    def add_modules(self):

        self.inv_mod = factory.create(module_type="pinv", module_name="rom_control_logic_pinv", height=self.mod_height)
        self.nand_mod = factory.create(module_type="pnand2", module_name="rom_control_nand", height=self.mod_height)
        self.driver_mod = factory.create(module_type="pdriver", inverting=True, fanout=self.output_size, height=self.mod_height, add_wells=True)
        
        
    def add_pins(self):
        self.add_pin("clk", "INPUT")
        self.add_pin("CS", "INPUT")
        self.add_pin("prechrg", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        
        self.inv_inst = self.add_inst(name="read_signal_inv", mod=self.inv_mod)
        self.connect_inst(["clk", "clk_bar", "vdd", "gnd"])

        self.nand_inst = self.add_inst(name="control_nand", mod=self.nand_mod)
        self.connect_inst(["CS", "clk_bar", "pre_drive", "vdd", "gnd"])

        self.driver_inst = self.add_inst(name="driver_inst", mod=self.driver_mod)
        self.connect_inst(["pre_drive", "prechrg", "vdd", "gnd"])


    def place_instances(self):
        self.nand_inst.place(offset=[self.inv_inst.width, 0])
        self.driver_inst.place(offset=[self.nand_inst.width + self.inv_inst.width, 0])

    def route_insts(self):

        self.copy_layout_pin(self.inv_inst, "A", "READ")
        self.copy_layout_pin(self.driver_inst, "Z", "prechrg")
        self.copy_layout_pin(self.nand_inst, "B", "CS")

        self.add_path(self.route_layer, [self.inv_inst.get_pin("Z").center(), self.nand_inst.get_pin("A").center()])

        self.add_path(self.route_layer, [self.nand_inst.get_pin("Z").center(), self.driver_inst.get_pin("A").center()])
         