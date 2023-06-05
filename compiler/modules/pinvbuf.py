# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer
from .pgate import *


class pinvbuf(pgate):
    """
    This is a simple inverter/buffer used for driving loads. It is
    used in the column decoder for 1:2 decoding and as the clock buffer.
    """
    def __init__(self, name, size=4, height=None):

        debug.info(1, "creating pinvbuf {}".format(name))
        self.add_comment("size: {}".format(size))

        self.stage_effort = 4
        self.row_height = height
        # FIXME: Change the number of stages to support high drives.

        # stage effort of 4 or less
        # The pinvbuf has a FO of 2 for the first stage, so the second stage
        # should be sized "half" to prevent loading of the first stage
        self.size = size
        self.predriver_size = max(int(self.size / (self.stage_effort / 2)), 1)

        # Creates the netlist and layout
        super().__init__(name)

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_insts()

    def create_layout(self):

        self.width = 2 * self.inv1.width + self.inv2.width
        self.height = 2 * self.inv1.height

        self.place_modules()
        self.route_wires()
        self.add_layout_pins()
        self.add_boundary()

        self.offset_all_coordinates()

    def add_pins(self):
        self.add_pin("A")
        self.add_pin("Zb")
        self.add_pin("Z")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):

        # Shield the cap, but have at least a stage effort of 4
        input_size = max(1, int(self.predriver_size / self.stage_effort))
        self.inv = factory.create(module_type="pinv",
                                  size=input_size,
                                  height=self.row_height)

        self.inv1 = factory.create(module_type="pinv",
                                   size=self.predriver_size,
                                   height=self.row_height)

        self.inv2 = factory.create(module_type="pinv",
                                   size=self.size,
                                   height=self.row_height)

    def create_insts(self):
        # Create INV1 (capacitance shield)
        self.inv1_inst = self.add_inst(name="buf_inv1",
                                       mod=self.inv)
        self.connect_inst(["A", "zb_int", "vdd", "gnd"])

        self.inv2_inst = self.add_inst(name="buf_inv2",
                                       mod=self.inv1)
        self.connect_inst(["zb_int", "z_int", "vdd", "gnd"])

        self.inv3_inst = self.add_inst(name="buf_inv3",
                                       mod=self.inv2)
        self.connect_inst(["z_int", "Zb", "vdd", "gnd"])

        self.inv4_inst = self.add_inst(name="buf_inv4",
                                       mod=self.inv2)
        self.connect_inst(["zb_int", "Z", "vdd", "gnd"])

    def place_modules(self):
        # Add INV1 to the left (capacitance shield)
        self.inv1_inst.place(vector(0, 0))

        # Add INV2 to the right of INV1
        self.inv2_inst.place(vector(self.inv1_inst.rx(), 0))

        # Add INV3 to the right of INV2
        self.inv3_inst.place(vector(self.inv2_inst.rx(), 0))

        # Add INV4 flipped to the bottom aligned with INV2
        self.inv4_inst.place(offset=vector(self.inv2_inst.rx(),
                                           2 * self.inv2.height),
                             mirror="MX")

    def route_wires(self):
        if "li" in layer:
            route_stack = self.li_stack
        else:
            route_stack = self.m1_stack

        # inv1 Z to inv2 A
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        mid_point = vector(z1_pin.cx(), a2_pin.cy())
        self.add_path(z1_pin.layer, [z1_pin.center(), mid_point, a2_pin.center()])
        self.add_via_stack_center(from_layer=z1_pin.layer,
                                  to_layer=a2_pin.layer,
                                  offset=a2_pin.center())

        # inv2 Z to inv3 A
        z2_pin = self.inv2_inst.get_pin("Z")
        a3_pin = self.inv3_inst.get_pin("A")
        mid_point = vector(z2_pin.cx(), a3_pin.cy())
        self.add_path(z2_pin.layer, [z2_pin.center(), mid_point, a3_pin.center()])
        self.add_via_stack_center(from_layer=z2_pin.layer,
                                  to_layer=a3_pin.layer,
                                  offset=a3_pin.center())

        z1_pin = self.inv1_inst.get_pin("Z")
        a4_pin = self.inv4_inst.get_pin("A")

        # inv1 Z to inv4 A (up and over)
        mid_point = vector(z1_pin.cx(), a4_pin.cy())
        self.add_wire(route_stack,
                    [z1_pin.center(), mid_point, a4_pin.center()])
        self.add_via_stack_center(from_layer=z1_pin.layer,
                                to_layer=route_stack[2],
                                offset=z1_pin.center())

    def add_layout_pins(self):

        # Continous vdd rail along with label.
        vdd_pin = self.inv1_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer=vdd_pin.layer,
                            offset=vdd_pin.ll().scale(0, 1),
                            width=self.width,
                            height=vdd_pin.height())

        # Continous vdd rail along with label.
        gnd_pin = self.inv4_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer=gnd_pin.layer,
                            offset=gnd_pin.ll().scale(0, 1),
                            width=self.width,
                            height=gnd_pin.height())

        # Continous gnd rail along with label.
        gnd_pin = self.inv1_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer=gnd_pin.layer,
                            offset=gnd_pin.ll().scale(0, 1),
                            width=self.width,
                            height=vdd_pin.height())

        z_pin = self.inv4_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=z_pin.layer,
                                        offset=z_pin.center())

        zb_pin = self.inv3_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Zb",
                                        layer=zb_pin.layer,
                                        offset=zb_pin.center())

        a_pin = self.inv1_inst.get_pin("A")
        self.add_layout_pin_rect_center(text="A",
                                        layer=a_pin.layer,
                                        offset=a_pin.center())
