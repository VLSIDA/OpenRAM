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
from openram.tech import layer_properties as layer_props
from openram import OPTS


class wordline_driver(design):
    """
    This is an AND (or NAND) with configurable drive strength to drive the wordlines.
    It is matched to the bitcell height.
    """
    def __init__(self, name, cols, height=None):
        debug.info(1, "Creating wordline_driver {}".format(name))
        self.add_comment("cols: {}".format(cols))
        super().__init__(name)

        if height is None:
            b = factory.create(module_type=OPTS.bitcell)
            self.height = b.height
        else:
            self.height = height
        self.cols = cols

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

        local_array_size = OPTS.local_array_size
        if local_array_size > 0:
            driver_size = max(int(self.cols / local_array_size), 1)
        else:
            # Defautl to FO4
            driver_size = max(int(self.cols / 4), 1)

        # The polarity must be switched if we have a hierarchical wordline
        # to compensate for the local array inverters
        if local_array_size > 0:
            self.driver = factory.create(module_type="buf_dec",
                                         size=driver_size,
                                         height=self.nand.height)
        else:
            self.driver = factory.create(module_type="inv_dec",
                                         size=driver_size,
                                         height=self.nand.height)

    def create_layout(self):
        self.width = self.nand.width + self.driver.width
        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"

        self.place_insts()
        self.route_wires()
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
        self.nand_inst = self.add_inst(name="wld_nand",
                                       mod=self.nand)
        self.connect_inst(["A", "B", "zb_int", "vdd", "gnd"])

        self.driver_inst = self.add_inst(name="wl_driver",
                                         mod=self.driver)
        self.connect_inst(["zb_int", "Z", "vdd", "gnd"])

    def place_insts(self):
        # Add NAND to the right
        self.nand_inst.place(offset=vector(0, 0))

        # Add INV to the right
        self.driver_inst.place(offset=vector(self.nand_inst.rx(), 0))

    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top, (middle), and bottom. """
        if layer_props.wordline_driver.vertical_supply:
            for name in ["vdd", "gnd"]:
                for inst in [self.nand_inst, self.driver_inst]:
                    self.copy_layout_pin(inst, name)
        else:
            self.add_layout_pin_rect_center(text="gnd",
                                            layer=self.route_layer,
                                            offset=vector(0.5 * self.width, 0),
                                            width=self.width)

            y_offset = self.height
            self.add_layout_pin_rect_center(text="vdd",
                                            layer=self.route_layer,
                                            offset=vector(0.5 * self.width, y_offset),
                                            width=self.width)

    def route_wires(self):

        # nand Z to inv A
        z1_pin = self.nand_inst.get_pin("Z")
        a2_pin = self.driver_inst.get_pin("A")
        if OPTS.tech_name == "sky130":
            mid1_point = vector(a2_pin.cx(), z1_pin.cy())
        else:
            mid1_point = vector(z1_pin.cx(), a2_pin.cy())
        self.add_path(self.route_layer,
                      [z1_pin.center(), mid1_point, a2_pin.center()])

    def add_layout_pins(self):
        pin = self.driver_inst.get_pin("Z")
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
