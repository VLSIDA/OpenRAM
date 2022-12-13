# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from openram.base import design
from openram.sram_factory import factory
from openram.base import vector
from openram.tech import layer, drc



class rom_inv_array(design):
    """
    An array of inverters to create the inverted address lines for the rom decoder
    """
    def __init__(self, cols, inv_size=None, name="", route_layer="m1"):
        self.cols = cols
        self.route_layer = route_layer
        dff = factory.create(module_type="dff")
        if name=="":
            name = "rom_inv_array_{0}".format(cols)
        if inv_size == None:
            self.inv_size = dff.height * 0.5
        else: 
            self.inv_size = inv_size


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
        self.width = self.cols * self.poly_tap.height * 2
        self.height = self.inv_mod.height
        self.setup_layout_constants()
        self.place_instances()
        self.place_vias()
        self.route_sources()
        self.add_boundary()


    def create_modules(self):

        self.inv_mod = factory.create(module_type="pinv", module_name="inv_array_mod", height=self.inv_size, add_wells=False)
        self.end_inv = factory.create(module_type="pinv", module_name="inv_array_end_mod", height=self.inv_size)
        # For layout constants
        self.poly_tap = factory.create(module_type="rom_poly_tap", strap_length=0)

    def add_pins(self):
        for col in range(self.cols):
            self.add_pin("inv{0}_in".format(col), "INPUT")
            self.add_pin("inv{0}_out".format(col), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        self.inv_insts = []

        for col in range(self.cols):
            name = "Xinv_c{0}".format(col)
            if col == self.cols - 1:
                print("TAP ME DOWN")
                self.inv_insts.append(self.add_inst(name=name, mod=self.end_inv))
            else:
                self.inv_insts.append(self.add_inst(name=name, mod=self.inv_mod))
            inst_A = "inv{0}_in".format(col)
            inst_Z = "inv{0}_out".format(col)
            self.connect_inst([inst_A, inst_Z, "vdd", "gnd"])

    def setup_layout_constants(self):
        input_pin = self.inv_insts[0].get_pin("A")
        output_pin = self.inv_insts[0].get_pin("Z")

        # NEED TO OFFSET OUTPUT VIA IN ORDER TO ALIGN WITH PITCH OF ADDRESS INPUTS TO ARRAY
        
        # print(self.poly_tap.get_pin("poly_tap").center())
        
        # distance between input and output pins of inverter
        in_out_distance =  output_pin.cx() - input_pin.cx()
        # distance from left edge of inverter to input plus right edge to output
        edge_to_pins_distance = input_pin.cx() - self.inv_insts[0].lx() + self.inv_insts[0].rx() - output_pin.cx()

        self.alignment_offset = edge_to_pins_distance - in_out_distance

    def place_instances(self):
        self.add_label("ZERO", self.route_layer)
        for col in range(self.cols):
            # base = vector(col*(self.inv_mod.width - self.alignment_offset), 0)
            base = vector(col*(self.poly_tap.height * 2), 0)
            self.inv_insts[col].place(offset=base)
        #vdd_pin = self.inv_insts[0].get_pin("vdd").center()
        #self.add_layout_pin_rect_center("vdd_align", self.inv_layer, vdd_pin, 0, 0)

    def place_vias(self):
        for i in range(self.cols):
            input_pin = self.inv_insts[i].get_pin("A")
            output_pin = self.inv_insts[i].get_pin("Z")

            self.add_via_stack_center(input_pin.center(), self.inv_mod.route_layer, self.route_layer)
            self.add_via_stack_center(output_pin.center(), self.inv_mod.route_layer, self.route_layer)
            self.add_layout_pin_rect_center("inv{}_in".format(i), offset=input_pin.center(), layer=self.route_layer)
            self.add_layout_pin_rect_center("inv{}_out".format(i), offset=output_pin.center(), layer=self.route_layer)

    def route_sources(self):

        vdd_start = self.inv_insts[0].get_pin("vdd")
        vdd_end = self.inv_insts[-1].get_pin("vdd")

        gnd_start = self.inv_insts[0].get_pin("gnd")
        gnd_end = self.inv_insts[-1].get_pin("gnd")

        self.copy_layout_pin(self.inv_insts[0], "vdd")
        self.copy_layout_pin(self.inv_insts[0], "gnd")
        # self.vdd = self.add_layout_pin_rect_ends("vdd", self.inv_layer, vdd_start.center(), vdd_end.center())[-1]
        # self.gnd = self.add_layout_pin_rect_ends("gnd", self.inv_layer, gnd_start.center(), gnd_end.center())[-1]

