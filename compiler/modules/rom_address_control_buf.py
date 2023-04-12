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



class rom_address_control_buf(design):
    """
    Takes the input address lines and creates the address and address bar lines for the decoder.
    Adds control logic for the precharge cycle so that all address lines are high before the read cycle
    """
    def __init__(self, size, name="", route_layer="m1", add_wells=False):

        self.route_layer = route_layer
        self.add_wells = add_wells
        self.size = size
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
        self.width =  self.cell.height * 2
        self.height = self.inv.width + 2 * self.nand.width
        self.setup_layout_constants()
        self.place_instances()
        self.route_gates()
        self.route_sources()
        self.add_boundary()

    def create_modules(self):

        self.inv = factory.create(module_type="pinv_dec", module_name="inv_array_mod", add_wells=False, size=self.size)
        self.nand = factory.create(module_type="nand2_dec", height=self.inv.height)
        # For layout constants
        self.cell = factory.create(module_type="rom_base_cell")

    def add_pins(self):

        self.add_pin("A_in", "INPUT")
        self.add_pin("A_out", "INOUT")
        self.add_pin("Abar_out", "OUTPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):

        name = "XinvAbar"

        self.inv_inst = self.add_inst(name=name, mod=self.inv)
        inst_A = "A_in"
        inst_Z = "Abar_internal"
        self.connect_inst([inst_A, inst_Z, "vdd", "gnd"])

        name = "Xnand_addr"

        self.addr_nand = self.add_inst(name=name, mod=self.nand)
        inst_A = "clk"
        inst_B = "Abar_internal"
        inst_Z = "A_out"
        self.connect_inst([inst_A, inst_B, inst_Z, "vdd", "gnd"])

        name = "Xnand_addr_bar"

        self.addr_bar_nand = self.add_inst(name=name, mod=self.nand)
        inst_A = "clk"
        inst_B = "A_out"
        inst_Z = "Abar_out"
        self.connect_inst([inst_A, inst_B, inst_Z, "vdd", "gnd"])

    def setup_layout_constants(self):
        self.route_width = drc["minwidth_{}".format(self.route_layer)]
        self.interconnect_width = drc["minwidth_{}".format(self.inv_layer)]

    def place_instances(self):
        self.inv_inst.place(offset=vector(self.inv_inst.height,0), rotate=90)
        self.addr_nand.place(offset=vector(self.addr_nand.height , self.inv_inst.width + self.route_width ), rotate=90)
        self.addr_bar_nand.place(offset=vector( self.addr_bar_nand.height, self.addr_nand.width + self.inv_inst.width + self.route_width), rotate=90)

    def route_gates(self):
        clk1_pin = self.addr_nand.get_pin("A")
        clk2_pin = self.addr_bar_nand.get_pin("A")

        Abar_out = self.addr_bar_nand.get_pin("Z")
        A_out = self.addr_nand.get_pin("Z")

        Abar_in = self.addr_nand.get_pin("B")
        Abar_int_out = self.inv_inst.get_pin("Z")

        Aint_in = self.addr_bar_nand.get_pin("B")
        A_in = self.inv_inst.get_pin("A")


        # Find the center of the pmos poly/gate
        poly_right = clk1_pin.cx() + self.poly_enclose_contact + 0.5 * self.contact_width

        ppoly_center = poly_right - 0.7 * self.poly_width

        contact_offset = vector(ppoly_center, clk2_pin.cy())

        # Route the two shared clk inputs together by connecting poly
        self.add_segment_center("poly", contact_offset, vector(ppoly_center, A_out.cy()))


        clk_offset = vector(clk2_pin.cx(), self.addr_nand.uy())
        self.add_layout_pin_rect_center("clk", offset=clk_offset, layer=self.route_layer)

        self.add_via_stack_center(from_layer=self.inv_layer, to_layer=self.route_layer, offset=self.addr_bar_nand.get_pin("A").center())
        self.add_segment_center(self.route_layer, clk_offset, vector(clk_offset.x, clk2_pin.cy()))

        # Route first NAND output to second NAND input
        start = A_out.center()
        end = Aint_in.center()
        self.add_path("m2", [start, end])
        self.add_via_stack_center(Aint_in.center(), self.inv_layer, "m2")
        self.add_via_stack_center(A_out.center(), self.inv_layer, "m2")

        # Route first NAND to output pin
        self.add_segment_center("m2", end, vector(end.x, self.addr_bar_nand.uy()))
        self.add_layout_pin_rect_center("A_out", offset=vector(end.x, self.addr_bar_nand.uy() - 0.5 * self.m2_width), layer="m2")

        # Route second NAND to output pin
        self.add_via_stack_center(Abar_out.center(), self.inv_layer, "m2")
        self.add_segment_center("m2", Abar_out.center(), vector(Abar_out.cx(), self.addr_bar_nand.uy()))
        self.add_layout_pin_rect_center("Abar_out", offset=vector(Abar_out.cx(), self.addr_bar_nand.uy() - 0.5 * self.m2_width), layer="m2")

        # Route inverter output to NAND
        end = vector(Abar_int_out.cx(), Abar_in.cy() + 0.5 * self.interconnect_width)
        self.add_segment_center(self.inv_layer, Abar_int_out.center(), end)
        self.copy_layout_pin(self.inv_inst, "A", "A_in")

    def route_sources(self):

        self.copy_layout_pin(self.addr_nand, "vdd")
        self.copy_layout_pin(self.addr_bar_nand, "vdd")
        self.copy_layout_pin(self.inv_inst, "vdd")

        self.copy_layout_pin(self.addr_bar_nand, "gnd")
        self.copy_layout_pin(self.addr_nand, "gnd")
        self.copy_layout_pin(self.inv_inst, "gnd")


        """ Add n/p well taps to the layout and connect to supplies """

        source_pin = self.inv_inst.get_pin("vdd")
        gnd_pin = self.inv_inst.get_pin("gnd")

        left_edge = self.inv_inst.get_pin("Z").cx() - 2 * self.contact_width - 2 * self.active_contact_to_gate - 4 * self.active_enclose_contact - self.poly_width - self.active_space

        contact_pos = vector(left_edge, source_pin.cy())

        self.add_via_center(layers=self.active_stack,
                            offset=contact_pos,
                            implant_type="n",
                            well_type="n")
        self.add_via_stack_center(offset=contact_pos,
                                  from_layer=self.active_stack[2],
                                  to_layer=self.route_layer)

        contact_pos = vector(left_edge, gnd_pin.cy())
        self.add_via_center(layers=self.active_stack,
                            offset=contact_pos,
                            implant_type="p",
                            well_type="p")
        self.add_via_stack_center(offset=contact_pos,
                                  from_layer=self.active_stack[2],
                                  to_layer=self.route_layer)