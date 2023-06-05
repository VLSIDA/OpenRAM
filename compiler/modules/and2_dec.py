# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.base import design
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS


class and2_dec(design):
    """
    This is an AND with configurable drive strength.
    """
    def __init__(self, name, size=1, height=None, add_wells=True):

        design.__init__(self, name)

        debug.info(1, "Creating and2_dec {}".format(name))
        self.add_comment("size: {}".format(size))
        self.size = size
        self.height = height

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.create_modules()
        self.create_insts()

    def create_modules(self):
        self.nand = factory.create(module_type="nand2_dec",
                                   height=self.height)

        self.inv = factory.create(module_type="inv_dec",
                                  height=self.height,
                                  size=self.size)

    def create_layout(self):

        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"
        self.width = self.nand.width + self.inv.width
        self.height = self.nand.height

        self.place_insts()
        self.add_wires()
        self.add_layout_pins()
        self.route_supply_rails()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        self.add_pin("A", "INPUT")
        self.add_pin("B", "INPUT")
        self.add_pin("Z", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_insts(self):
        self.nand_inst = self.add_inst(name="pand2_dec_nand",
                                       mod=self.nand)
        self.connect_inst(["A", "B", "zb_int", "vdd", "gnd"])

        self.inv_inst = self.add_inst(name="pand2_dec_inv",
                                      mod=self.inv)
        self.connect_inst(["zb_int", "Z", "vdd", "gnd"])

    def place_insts(self):
        # Add NAND to the right
        self.nand_inst.place(offset=vector(0, 0))

        # Add INV to the right
        self.inv_inst.place(offset=vector(self.nand_inst.rx(), 0))

    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top, (middle), and bottom. """
        if OPTS.tech_name == "sky130":
            for name in ["vdd", "gnd"]:
                for inst in [self.nand_inst, self.inv_inst]:
                    self.copy_layout_pin(inst, name)
        else:
            self.add_layout_pin_rect_center(text="gnd",
                                            layer=self.route_layer,
                                            offset=vector(0.5 * self.width, 0),
                                            width=self.width)
            self.add_layout_pin_rect_center(text="vdd",
                                            layer=self.route_layer,
                                            offset=vector(0.5 * self.width, self.height),
                                            width=self.width)

    def add_wires(self):
        # nand Z to inv A
        z1_pin = self.nand_inst.get_pin("Z")
        a2_pin = self.inv_inst.get_pin("A")
        if OPTS.tech_name == "sky130":
            mid1_point = vector(a2_pin.cx(), z1_pin.cy())
        else:
            mid1_point = vector(z1_pin.cx(), a2_pin.cy())
        self.add_path(self.route_layer,
                      [z1_pin.center(), mid1_point, a2_pin.center()])

    def add_layout_pins(self):
        pin = self.inv_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=pin.layer,
                                        offset=pin.center(),
                                        width=pin.width(),
                                        height=pin.height())

        for pin_name in ["A", "B"]:
            pin = self.nand_inst.get_pin(pin_name)
            self.add_layout_pin_rect_center(text=pin_name,
                                            layer=pin.layer,
                                            offset=pin.center(),
                                            width=pin.width(),
                                            height=pin.height())
