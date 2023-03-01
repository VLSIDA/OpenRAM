# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from math import ceil, log
from openram.sram_factory import factory
from openram.base import vector, design
from openram import OPTS
from openram.tech import drc

class rom_decoder(design):
    def __init__(self, num_outputs, fanout, strap_spacing, name="", route_layer="m1", output_layer="m1", invert_outputs=False):

        # word lines in the base array become the address lines/cols in the decoder
        # bit lines in the base array become the word lines/rows in the decoder
        # array gets rotated 90deg so rows/cols switch

        self.strap_spacing=strap_spacing
        self.num_outputs = num_outputs
        self.num_inputs = ceil(log(num_outputs, 2))
        self.create_decode_map()

        super().__init__(name)

        b = factory.create(module_type=OPTS.bitcell)
        self.cell_height = b.height
        self.route_layer = route_layer
        self.output_layer = output_layer
        self.inv_route_layer = "m2"
        self.fanout=fanout
        self.invert_outputs=invert_outputs
        self.create_netlist()

        self.width = self.array_mod.height + self.wordline_buf.width
        self.height = self.array_mod.width + self.control_array.height
        self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.setup_layout_constants()
        self.place_array()
        self.place_input_buffer()
        self.place_driver()
        self.route_outputs()

        self.connect_inputs()
        self.route_supplies()
        self.add_boundary()

    def add_boundary(self):
        ll = self.find_lowest_coords()
        m1_offset = self.m1_width
        self.translate_all(vector(0, ll.y))
        ur = self.find_highest_coords()

        ur = vector(ur.x, ur.y)
        super().add_boundary(ll, ur)
        self.width = ur.x
        self.height = ur.y

    def setup_layout_constants(self):
        self.inv_route_width = drc["minwidth_{}".format(self.inv_route_layer)]

    def create_decode_map(self):
        self.decode_map = []
        # create decoding map that will be the bitmap for the rom decoder
        # row/col order in the map will be switched in the placed decoder/
        for col in range(self.num_inputs):

            # odd cols are address
            # even cols are address bar
            col_array = []
            inv_col_array = []
            for row in range(self.num_outputs):

                addr_idx = -col - 1

                addr = format(row, 'b')
                if col >= len(addr) :
                    bin_digit = 0
                else:
                    bin_digit = int(addr[addr_idx])

                col_array.append(bin_digit)

                if bin_digit == 0 : inv_col_array.append(1)
                else : inv_col_array.append(0)

            self.decode_map.append(col_array)
            self.decode_map.append(inv_col_array)
        self.decode_map.reverse()

    def add_pins(self):
        for i in range(self.num_inputs):
            self.add_pin("A{0}".format(i), "INPUT")

        for j in range(self.num_outputs):
            self.add_pin("wl_{0}".format(j), "OUTPUT")
        self.add_pin("precharge", "INPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):

        self.control_array = factory.create(module_type="rom_address_control_array",
                                            cols=self.num_inputs)

        self.wordline_buf = factory.create(module_type="rom_wordline_driver_array", module_name="{}_wordline_buffer".format(self.name),
                                        rows=self.num_outputs,
                                        fanout=ceil(self.fanout),
                                        invert_outputs=self.invert_outputs,
                                        tap_spacing=self.strap_spacing)

        self.array_mod = factory.create(module_type="rom_base_array",
                                        module_name="{}_array".format(self.name),
                                        cols=self.num_outputs,
                                        rows=2 * self.num_inputs,
                                        bitmap=self.decode_map,
                                        strap_spacing = self.strap_spacing,
                                        bitline_layer=self.output_layer,
                                        tap_direction="col")

    def create_instances(self):

        self.create_array_inst()
        self.create_input_buffer()
        self.create_wordline_buffer()

    def create_input_buffer(self):
        name = "pre_control_array"
        self.buf_inst = self.add_inst(name=name, mod=self.control_array)

        control_pins = []

        for i in range(self.num_inputs):
            control_pins.append("A{0}".format(i))
        for i in range(self.num_inputs):
            control_pins.append("A_int_{0}".format(i))
        for i in range(self.num_inputs):
            control_pins.append("Ab_int_{0}".format(i))


        control_pins.append("clk")
        control_pins.append("vdd")
        control_pins.append("gnd")
        self.connect_inst(control_pins)

    def create_array_inst(self):
        self.array_inst = self.add_inst(name="decode_array_inst", mod=self.array_mod)

        array_pins = []

        for j in range(self.num_outputs):
            name = "wl_int{0}".format(j)
            array_pins.append(name)


        for i in reversed(range(self.num_inputs)):
            array_pins.append("Ab_int_{0}".format(i))
            array_pins.append("A_int_{0}".format(i))
        array_pins.append("precharge")
        array_pins.append("vdd")
        array_pins.append("gnd")
        self.connect_inst(array_pins)

    def create_wordline_buffer(self):
        self.wordline_buf_inst = self.add_inst("rom_wordline_driver", mod=self.wordline_buf)
        in_pins = ["wl_int{}".format(wl) for wl in range(self.num_outputs)]
        out_pins = ["wl_{}".format(wl) for wl in range(self.num_outputs)]
        pwr_pins = ["vdd", "gnd"]
        self.connect_inst(in_pins + out_pins + pwr_pins)

    def place_input_buffer(self):
        wl = self.array_mod.row_size - 1
        align = self.array_inst.get_pin(self.array_mod.wordline_names[0][wl]).cx() - self.buf_inst.get_pin("A0_out").cx()

        self.buf_inst.place(vector(align, 0))

        self.copy_layout_pin(self.buf_inst, "clk")

    def place_array(self):
        offset = vector(self.array_mod.height, self.control_array.height + self.m1_width + self.poly_contact.width)
        self.array_inst.place(offset, rotate=90)

    def place_driver(self):

        offset = vector(self.array_inst.height + self.m1_width, self.array_inst.by())
        self.wordline_buf_inst.place(offset)

        # calculate the offset between the decode array and the buffer inputs now that their zeros are aligned
        pin_offset = self.array_inst.get_pin("bl_0_0").cy() - self.wordline_buf_inst.get_pin("in_0").cy()
        self.wordline_buf_inst.place(offset + vector(0, pin_offset))

    def route_outputs(self):
        for j in range(self.num_outputs):

            self.copy_layout_pin(self.wordline_buf_inst, "out_{}".format(j), "wl_{}".format(j))
            offset = self.wordline_buf_inst.get_pin("out_{}".format(j)).center()

        array_pins = [self.array_inst.get_pin("bl_0_{}".format(bl)) for bl in range(self.num_outputs)]
        driver_pins = [self.wordline_buf_inst.get_pin("in_{}".format(bl)) for bl in range(self.num_outputs)]

        route_pins = array_pins + driver_pins
        self.connect_row_pins(self.output_layer, route_pins, round=True)

    def connect_inputs(self):

        self.copy_layout_pin(self.array_inst, "precharge")
        self.copy_layout_pin(self.array_inst, "precharge_r")
        for i in range(self.num_inputs):
            wl = (self.num_inputs - i) * 2 - 1
            wl_bar = wl - 1
            addr_pin = self.array_inst.get_pin(self.array_mod.wordline_names[0][wl])
            addr_bar_pin = self.array_inst.get_pin(self.array_mod.wordline_names[0][wl_bar])

            addr_out_pin = self.buf_inst.get_pin("A{}_out".format(i))
            addr_bar_out_pin = self.buf_inst.get_pin("Abar{}_out".format(i))

            addr_middle = vector(addr_pin.cx(), addr_out_pin.cy())

            addr_bar_middle = vector(addr_bar_pin.cx(), addr_bar_out_pin.cy())

            self.add_path(self.inv_route_layer, [addr_out_pin.center(), addr_middle, addr_pin.center()])
            self.add_path(self.inv_route_layer, [addr_bar_out_pin.center(), addr_bar_middle, addr_bar_pin.center()])
            self.copy_layout_pin(self.buf_inst, "A{}_in".format(i), "A{}".format(i))

    def route_supplies(self):

        self.copy_layout_pin(self.array_inst, "vdd")
        self.copy_layout_pin(self.wordline_buf_inst, "vdd")
        self.copy_layout_pin(self.buf_inst, "vdd")

        self.copy_layout_pin(self.array_inst, "gnd")
        self.copy_layout_pin(self.wordline_buf_inst, "gnd")
        self.copy_layout_pin(self.buf_inst, "gnd")