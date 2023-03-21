# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.base import design
from openram.sram_factory import factory
from openram.base import vector
from openram.tech import layer, drc



class rom_address_control_array(design):
    """
    Takes the input address lines and creates the address and address bar lines for the decoder.
    Adds control logic for the precharge cycle so that all address lines are high before the read cycle
    """
    def __init__(self, cols, inv_height=None, inv_size=1, name="", route_layer="m1"):
        self.size=inv_size
        self.cols = cols
        self.route_layer = route_layer
        dff = factory.create(module_type="dff")
        if name=="":
            name = "rom_inv_array_{0}".format(cols)
        if inv_height == None:
            self.inv_height = dff.height * 0.5
        else:
            self.inv_height = inv_height


        if "li" in layer:
            self.inv_layer = "li"
        else:
            self.inv_layer = "m1"
        super().__init__(name)
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.create_modules()
        self.add_pins()
        self.create_instances()


    def create_layout(self):
        self.width = self.cols * self.addr_control.width
        self.height = self.addr_control.height
        self.setup_layout_constants()
        self.place_instances()
        self.route_clk()
        self.route_sources()
        self.copy_pins()
        self.add_boundary()


    def create_modules(self):
        self.addr_control = factory.create(module_type="rom_address_control_buf", size=self.inv_height)


    def add_pins(self):
        for col in range(self.cols):
            self.add_pin("A{0}_in".format(col), "INPUT")
        for col in range(self.cols):
            self.add_pin("A{0}_out".format(col), "OUTPUT")
        for col in range(self.cols):
            self.add_pin("Abar{0}_out".format(col), "OUTPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):

        self.buf_insts = []

        for col in range(self.cols):

            name = "Xaddr_buf_{0}".format(col)
            addr_buf = self.add_inst(name=name, mod=self.addr_control)

            A_in = "A{0}_in".format(col)
            Aout = "A{0}_out".format(col)
            Abar_out = "Abar{0}_out".format(col)
            self.connect_inst([A_in, Aout, Abar_out, "clk", "vdd", "gnd"])

            self.buf_insts.append(addr_buf)

    def setup_layout_constants(self):
        self.route_width = drc["minwidth_{}".format(self.route_layer)]

    def place_instances(self):
        for col in range(self.cols):
            base = vector((col+1)*(self.addr_control.width), 0)

            self.buf_insts[col].place(offset=base, mirror="MY")

    def copy_pins(self):
        for i in range(self.cols):
            self.copy_layout_pin(self.buf_insts[i], "A_out", "A{0}_out".format(i))
            self.copy_layout_pin(self.buf_insts[i], "Abar_out", "Abar{0}_out".format(i))
            self.copy_layout_pin(self.buf_insts[i], "A_in", "A{0}_in".format(i))

    def route_clk(self):
        self.route_horizontal_pins("clk", insts=self.buf_insts, layer=self.route_layer)

    def route_sources(self):

        self.route_horizontal_pins("vdd", insts=self.buf_insts, layer=self.route_layer)
        self.route_horizontal_pins("gnd", insts=self.buf_insts, layer=self.route_layer)

        tmp_pins = []
        for pin in self.get_pins("vdd"):
            edge = vector(pin.lx() + 0.5 * self.route_width, pin.cy())
            tmp_pins.append(self.add_layout_pin_rect_center("vdd_edge", layer=self.route_layer, offset=edge))
        self.copy_layout_pin_shapes("vdd")
        self.remove_layout_pin("vdd")

        for pin in tmp_pins:
            self.copy_layout_pin(self, "vdd_edge", "vdd")
        self.remove_layout_pin("vdd_edge")