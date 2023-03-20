# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from openram.sram_factory import factory
from openram.base import vector, design
from openram.tech import layer, drc


class rom_control_logic(design):

    def __init__(self, num_outputs, clk_fanout, name="", height=None):
        self.output_size = num_outputs
        super().__init__(name, prop=False)
        self.height = height
        if self.height is not None:

            self.driver_height = 0.5 * self.height
            self.gate_height = 0.5 * self.height
        else:
            self.gate_height = 20 * self.m1_pitch
            self.driver_height = self.gate_height


        self.clk_fanout = clk_fanout

        if "li" in layer:
            self.route_stack = self.li_stack
        else:
            self.route_stack = self.m1_stack

        self.create_netlist()
        self.create_layout()
        self.add_boundary()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()

    def create_layout(self):
        self.create_instances()
        self.height=self.driver_inst.height + self.buf_inst.height
        self.width= max(self.nand_inst.width + self.buf_inst.width, self.driver_inst.width)
        self.place_instances()
        self.route_insts()

    def add_modules(self):
        self.buf_mod = factory.create(module_type="pdriver",
                                      module_name="rom_clock_driver",
                                      height=self.gate_height,
                                      fanout=self.clk_fanout + 2,
                                      add_wells=True,
                                      )
        self.nand_mod = factory.create(module_type="pnand2",
                                       module_name="rom_control_nand",
                                       height=self.gate_height,
                                       add_wells=False)
        self.driver_mod = factory.create(module_type="pdriver",
                                         module_name="rom_precharge_driver",
                                         inverting=True,
                                         fanout=self.output_size,
                                         height=self.driver_height,
                                         add_wells=True)

    def add_pins(self):
        self.add_pin("clk_in", "INPUT")
        self.add_pin("CS", "INPUT")
        self.add_pin("prechrg", "OUTPUT")
        self.add_pin("clk_out", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):

        self.buf_inst = self.add_inst(name="clk_driver", mod=self.buf_mod)
        self.connect_inst(["clk_in", "clk_out", "vdd", "gnd"])

        self.nand_inst = self.add_inst(name="control_nand", mod=self.nand_mod)
        self.connect_inst(["CS", "clk_out", "pre_drive", "vdd", "gnd"])

        self.driver_inst = self.add_inst(name="precharge_driver", mod=self.driver_mod)
        self.connect_inst(["pre_drive", "prechrg", "vdd", "gnd"])


    def place_instances(self):
        self.nand_inst.place(offset=[self.buf_inst.width, 0])
        self.driver_inst.place(offset=[0, self.buf_inst.height + self.driver_inst.height], mirror="MX")

        # hack to get around the fact these modules dont tile properly
        offset = self.driver_inst.get_pin("vdd").cy() - self.nand_inst.get_pin("vdd").cy()
        self.driver_inst.place(offset=[0, self.buf_inst.height + self.driver_inst.height - offset], mirror="MX")

    def route_insts(self):

        route_width = drc["minwidth_{}".format(self.route_stack[2])]
        self.copy_layout_pin(self.buf_inst, "A", "clk_in")
        self.copy_layout_pin(self.buf_inst, "Z", "clk_out")
        self.copy_layout_pin(self.driver_inst, "Z", "prechrg")
        self.copy_layout_pin(self.nand_inst, "A", "CS")

        self.copy_power_pin(self.buf_inst.get_pin("gnd"), directions="nonpref")
        self.copy_power_pin(self.driver_inst.get_pin("gnd"), directions="nonpref")
        self.copy_power_pin(self.buf_inst.get_pin("vdd"), directions="nonpref")
        clk = self.buf_inst.get_pin("Z")

        nand_B = self.nand_inst.get_pin("B")


        # Connect buffered clock bar to nand input

        mid = vector(clk.lx() - route_width - 2 * self.m1_space)
        self.add_path(self.route_stack[2], [clk.center(), nand_B.center()])

        self.add_via_stack_center(from_layer=clk.layer,
                                to_layer=self.route_stack[2],
                                offset=clk.center())
        self.add_via_stack_center(from_layer=nand_B.layer,
                                to_layer=self.route_stack[2],
                                offset=nand_B.center())


        # Connect nand output to precharge driver
        nand_Z = self.nand_inst.get_pin("Z")

        driver_A = self.driver_inst.get_pin("A")

        mid = vector(driver_A.cx(), driver_A.cy() - 4 * route_width)

        self.add_path(self.route_stack[2], [nand_Z.center(), mid, driver_A.center()])

        self.add_via_stack_center(from_layer=nand_Z.layer,
                                to_layer=self.route_stack[2],
                                offset=nand_Z.center())

        self.add_via_stack_center(from_layer=driver_A.layer,
                                to_layer=self.route_stack[2],
                                offset=driver_A.center())