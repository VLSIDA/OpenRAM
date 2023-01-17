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
from .pgate import *


class pbuf_dec(pgate):
    """
    This is a simple buffer used for driving wordlines.
    """
    def __init__(self, name, size=4, height=None, add_wells=True):

        debug.info(1, "creating {0} with size of {1}".format(name, size))
        self.add_comment("size: {}".format(size))

        self.stage_effort = 4
        self.size = size
        self.height = height

        # Creates the netlist and layout
        pgate.__init__(self, name, height, add_wells)

    def create_netlist(self):
        self.add_pins()
        self.create_modules()
        self.create_insts()

    def create_layout(self):
        self.width = self.inv1.width + self.inv2.width
        self.place_insts()
        self.add_wires()
        self.add_layout_pins()
        self.route_supply_rails()
        self.add_boundary()

    def add_pins(self):
        self.add_pin("A", "INPUT")
        self.add_pin("Z", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_modules(self):
        # Shield the cap, but have at least a stage effort of 4
        input_size = max(1, int(self.size / self.stage_effort))
        self.inv1 = factory.create(module_type="pinv_dec",
                                   size=input_size,
                                   height=self.height,
                                   add_wells=self.add_wells)

        self.inv2 = factory.create(module_type="pinv_dec",
                                   size=self.size,
                                   height=self.height,
                                   add_wells=self.add_wells)

    def create_insts(self):
        self.inv1_inst = self.add_inst(name="buf_inv1",
                                       mod=self.inv1)
        self.connect_inst(["A", "zb_int", "vdd", "gnd"])

        self.inv2_inst = self.add_inst(name="buf_inv2",
                                       mod=self.inv2)
        self.connect_inst(["zb_int", "Z", "vdd", "gnd"])

    def place_insts(self):
        # Add INV1 to the right
        self.inv1_inst.place(vector(0, 0))

        # Add INV2 to the right
        self.inv2_inst.place(vector(self.inv1_inst.rx(), 0))

    def add_wires(self):
        # inv1 Z to inv2 A
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        mid_loc = vector(a2_pin.cx(), z1_pin.cy())
        self.add_path(self.route_layer,
                      [z1_pin.rc(), mid_loc, a2_pin.lc()],
                      width=a2_pin.width())

    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top, (middle), and bottom. """
        self.copy_layout_pin(self.inv1_inst, "vdd")
        self.copy_layout_pin(self.inv1_inst, "gnd")
        self.copy_layout_pin(self.inv2_inst, "vdd")
        self.copy_layout_pin(self.inv2_inst, "gnd")

    def add_layout_pins(self):
        z_pin = self.inv2_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=z_pin.layer,
                                        offset=z_pin.center(),
                                        width=z_pin.width(),
                                        height=z_pin.height())

        a_pin = self.inv1_inst.get_pin("A")
        self.add_layout_pin_rect_center(text="A",
                                        layer=a_pin.layer,
                                        offset=a_pin.center(),
                                        width=a_pin.width(),
                                        height=a_pin.height())
