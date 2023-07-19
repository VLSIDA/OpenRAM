# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import datetime
from math import ceil, log
from openram.base import vector
from openram.base import design
from openram.base import rom_verilog
from openram import OPTS, print_time
from openram.sram_factory import factory
from openram.tech import drc, layer, parameter
from openram.router import router_tech


class rom_bank(design,rom_verilog):

    """
    Rom data bank with row and column decoder + control logic

    word size is in bytes
    """

    def __init__(self, name, rom_config):
        super().__init__(name=name)
        self.rom_config = rom_config
        rom_config.set_local_config(self)

        self.word_size = self.word_bits
        self.num_outputs = self.rows
        self.num_inputs = ceil(log(self.rows, 2))
        self.col_bits = ceil(log(self.words_per_row, 2))
        self.row_bits = self.num_inputs

        self.tap_spacing = self.strap_spacing

        try:
            from openram.tech import power_grid
            self.supply_stack = power_grid
        except ImportError:
            # if no power_grid is specified by tech we use sensible defaults
            # Route a M3/M4 grid
            self.supply_stack = self.m3_stack

        self.interconnect_layer = "m1"
        self.bitline_layer = "m1"
        self.wordline_layer = "m2"

        if "li" in layer:
            self.route_stack = self.m1_stack
        else:
            self.route_stack = self.m2_stack
        self.route_layer = self.route_stack[0]

        if OPTS.is_unit_test:
            self.create_netlist()
            self.create_layout()


    def create_netlist(self):
        start_time = datetime.datetime.now()
        self.add_modules()
        self.add_pins()
        self.create_instances()
        if not OPTS.is_unit_test:
            print_time("Submodules", datetime.datetime.now(), start_time)

    def create_layout(self):

        start_time = datetime.datetime.now()

        self.setup_layout_constants()
        self.place_instances()
        if not OPTS.is_unit_test:
            print_time("Placement", datetime.datetime.now(), start_time)

        self.add_boundary()

        start_time = datetime.datetime.now()
        self.route_layout()
        if not OPTS.is_unit_test:
            print_time("Routing", datetime.datetime.now(), start_time)

        start_time = datetime.datetime.now()
        if not OPTS.is_unit_test:
            # We only enable final verification if we have routed the design
            # Only run this if not a unit test, because unit test will also verify it.
            self.DRC_LVS(final_verification=OPTS.route_supplies, force_check=OPTS.check_lvsdrc)
            print_time("Verification", datetime.datetime.now(), start_time)

    def add_boundary(self):

        ll = self.find_lowest_coords()
        m1_offset = self.m1_width
        self.translate_all(vector(0, ll.y))
        ur = self.find_highest_coords()
        ur = vector(ur.x, ur.y)
        super().add_boundary(vector(0, 0), ur)
        self.width = ur.x
        self.height = ur.y

    def route_layout(self):
        self.route_decode_outputs()
        self.route_precharge()
        self.route_clock()
        self.route_array_outputs()
        self.place_top_level_pins()
        self.route_output_buffers()

        rt = router_tech(self.supply_stack, 1)
        init_bbox = self.get_bbox(side="ring",
                                  margin=rt.track_width)
        self.route_supplies(init_bbox)
        # We need the initial bbox for the supply rings later
        # because the perimeter pins will change the bbox
        # Route the pins to the perimeter
        if OPTS.perimeter_pins:
            # We now route the escape routes far enough out so that they will
            # reach past the power ring or stripes on the sides
            bbox = self.get_bbox(side="ring",
                                 margin=11*rt.track_width)
            self.route_escape_pins(bbox)




    def setup_layout_constants(self):
        self.route_layer_width = drc["minwidth_{}".format(self.route_stack[0])]
        self.route_layer_pitch = drc["{0}_to_{0}".format(self.route_stack[0])]

        self.interconnect_layer_width = drc["minwidth_{}".format(self.interconnect_layer)]
        self.interconnect_layer_pitch = drc["{0}_to_{0}".format(self.interconnect_layer)]

    def add_pins(self):

        self.add_pin("clk", "INPUT")
        self.add_pin("cs", "INPUT")

        for i in range(self.row_bits + self.col_bits):
            self.add_pin("addr[{}]".format(i), "INPUT")

        out_pins = []
        for j in range(self.word_size):
            out_pins.append("dout[{}]".format(j))
        self.add_pin_list(out_pins, "OUTPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def add_modules(self):

        # TODO: provide technology-specific calculation of these parameters
        # in sky130 the address control buffer is composed of 2 size 2 NAND gates,
        # with a beta of 3, each of these gates has gate capacitance of 2 min sized inverters, therefor a load of 4


        addr_control_buffer_effort = parameter['beta'] + 1
        # a single min sized nmos makes up 1/4 of the input capacitance of a min sized inverter
        bitcell_effort = 0.25

        # Takes into account inverter sizing
        wordline_effort = bitcell_effort * 0.5

        # a single min sized pmos plus a single min sized nmos have approximately half the gate capacitance of a min inverter
        # an additional 0.2 accounts for the long wire capacitance and add delay to gaurentee the read timing
        precharge_cell_effort = 0.5 + 0.2

        self.array = factory.create(module_type="rom_base_array",
                                    cols=self.cols,
                                    rows=self.rows,
                                    strap_spacing=self.strap_spacing,
                                    bitmap=self.data,
                                    bitline_layer=self.bitline_layer,
                                    wordline_layer=self.wordline_layer,
                                    pitch_match=True,
                                    tap_spacing=self.tap_spacing)


        self.decode_array = factory.create(module_name="rom_row_decode",
                                           module_type="rom_decoder",
                                           num_outputs=self.rows,
                                           strap_spacing=self.strap_spacing,
                                           route_layer=self.route_layer,
                                           fanout=(self.cols)*wordline_effort )


        self.column_mux = factory.create(module_type="rom_column_mux_array",
                                         columns=self.cols,
                                         word_size=self.word_size,
                                         tap_spacing=self.strap_spacing,
                                         bitline_layer=self.interconnect_layer,
                                         input_layer=self.bitline_layer)

        self.column_decode = factory.create(module_name="rom_column_decode",
                                            module_type="rom_decoder",
                                            num_outputs=self.words_per_row,
                                            strap_spacing=self.strap_spacing,
                                            route_layer=self.route_layer,
                                            fanout=2,
                                            invert_outputs=True )

        self.control_logic = factory.create(module_type="rom_control_logic",
                                            num_outputs=(self.cols + self.words_per_row * precharge_cell_effort) \
                                                         + (addr_control_buffer_effort * self.col_bits),
                                            clk_fanout=(self.row_bits * addr_control_buffer_effort) + (precharge_cell_effort * self.rows),
                                            height=self.column_decode.height )

        self.bitline_inv = factory.create(module_type="rom_wordline_driver_array",
                                            module_name="rom_bitline_inverter",
                                            rows=self.cols,
                                            fanout=4,
                                            invert_outputs=True,
                                            tap_spacing=0,
                                            flip_io=True)
        self.output_inv = factory.create(module_type="rom_wordline_driver_array",
                                            module_name="rom_output_buffer",
                                            rows=self.word_size,
                                            fanout=4,
                                            tap_spacing=1,
                                            invert_outputs=True)


    def create_instances(self):
        gnd = ["gnd"]
        vdd = ["vdd"]
        prechrg = ["precharge"]
        clk = ["clk_int"]

        bitlines = ["bl_{}".format(bl) for bl in range(self.cols)]
        wordlines = ["wl_{}".format(wl) for wl in range(self.rows)]

        addr_msb = ["addr[{}]".format(addr + self.col_bits) for addr in range(self.row_bits)]
        addr_lsb = ["addr[{}]".format(addr) for addr in range(self.col_bits)]

        select_lines = ["word_sel_{}".format(word) for word in range(self.words_per_row)]

        bitline_bar = ["bl_b_{}".format(bl) for bl in range(self.cols)]
        pre_buf_outputs = ["rom_out_prebuf_{}".format(bit) for bit in range(self.word_size)]
        outputs = ["dout[{}]".format(bl) for bl in range(self.word_size)]


        array_pins = bitlines + wordlines + prechrg + vdd + gnd

        row_decode_pins = addr_msb + wordlines + clk + clk + vdd + gnd
        col_decode_pins = addr_lsb + select_lines + prechrg + prechrg + vdd + gnd

        col_mux_pins = bitline_bar + select_lines + pre_buf_outputs + gnd

        bitline_inv_pins = bitlines + bitline_bar + vdd + gnd

        output_buf_pins = pre_buf_outputs + outputs + vdd + gnd

        self.array_inst = self.add_inst(name="rom_bit_array", mod=self.array)
        self.connect_inst(array_pins)

        self.decode_inst = self.add_inst(name="rom_row_decoder", mod=self.decode_array)
        self.connect_inst(row_decode_pins)

        self.control_inst = self.add_inst(name="rom_control", mod=self.control_logic)
        self.connect_inst(["clk", "cs", "precharge", "clk_int", "vdd", "gnd"])

        self.mux_inst = self.add_inst(name="rom_column_mux", mod=self.column_mux)
        self.connect_inst(col_mux_pins)

        self.col_decode_inst = self.add_inst(name="rom_column_decoder", mod=self.column_decode)
        self.connect_inst(col_decode_pins)

        self.bitline_inv_inst = self.add_inst(name="rom_bitline_inverter", mod=self.bitline_inv)
        self.connect_inst(bitline_inv_pins)

        self.output_inv_inst = self.add_inst(name="rom_output_inverter", mod=self.output_inv)
        self.connect_inst(output_buf_pins)

    def place_instances(self):
        self.place_row_decoder()
        self.place_data_array()
        self.place_bitline_inverter()
        self.place_col_mux()
        self.place_col_decoder()
        self.place_control_logic()
        self.place_output_buffer()


    def place_row_decoder(self):
        self.decode_offset = vector(0, self.control_inst.height )
        self.decode_inst.place(offset=self.decode_offset)

    def place_data_array(self):
        # We approximate the correct position for the array
        array_x = self.decode_inst.width + (2) * ( self.route_layer_width + self.route_layer_pitch )
        array_y = self.decode_array.buf_inst.height - self.array.precharge_inst.cy() - self.array.zero_cell.height * 0.5
        self.array_offset = vector(array_x ,array_y)
        self.array_inst.place(offset=self.array_offset)

        # now move array to correct alignment with decoder
        array_align = self.decode_inst.get_pin("wl_0").cy() - self.array_inst.get_pin("wl_0_0").cy()
        self.array_inst.place(offset=(self.array_offset + vector(0, array_align)))

    def place_bitline_inverter(self):
        self.bitline_inv_inst.place(offset=[0,0], rotate=90)
        inv_y_offset = self.array_inst.by() - self.bitline_inv_inst.width - 2 * self.m1_pitch

        inv_x_offset = self.array_inst.get_pin("bl_0_0").cx() - self.bitline_inv_inst.get_pin("out_0").cx()
        self.inv_offset = vector(inv_x_offset, inv_y_offset)
        self.bitline_inv_inst.place(offset=self.inv_offset, rotate=90)

    def place_control_logic(self):

        self.control_offset = vector(self.col_decode_inst.lx() - self.control_inst.width - 3 * self.m1_pitch, self.decode_inst.by() - self.control_logic.height - self.m1_pitch)
        self.control_inst.place(offset=self.control_offset)

    def place_col_decoder(self):
        col_decode_y = self.mux_inst.get_pin("sel_0").cy() - self.col_decode_inst.get_pin("wl_0").cy()
        self.col_decode_offset = vector(self.decode_inst.width - self.col_decode_inst.width, col_decode_y)
        self.col_decode_inst.place(offset=self.col_decode_offset)

    def place_col_mux(self):
        mux_y_offset = self.bitline_inv_inst.by() - self.mux_inst.height - 5 * self.route_layer_pitch

        mux_x_offset = self.bitline_inv_inst.get_pin("out_0").cx() - self.mux_inst.get_pin("bl_0").cx()
        self.mux_offset = vector(mux_x_offset, mux_y_offset)
        self.mux_inst.place(offset=self.mux_offset)

    def place_output_buffer(self):
        output_x = self.col_decode_inst.rx() + self.output_inv_inst.height
        output_y = self.mux_inst.by() - self.word_size * self.m1_pitch
        self.output_inv_offset = vector(output_x, output_y)
        self.output_inv_inst.place(offset=self.output_inv_offset, rotate=270)

    def route_decode_outputs(self):
        # for the row decoder
        route_pins = [self.array_inst.get_pin("wl_0_{}".format(wl)) for wl in range(self.rows)]
        decode_pins = [self.decode_inst.get_pin("wl_{}".format(wl)) for wl in range(self.rows)]
        route_pins.extend(decode_pins)
        self.connect_row_pins(self.interconnect_layer, route_pins, round=True)


        # then for the column decoder
        col_decode_pins = [self.col_decode_inst.get_pin("wl_{}".format(wl)) for wl in range(self.words_per_row)]
        sel_pins = [self.mux_inst.get_pin("sel_{}".format(wl)) for wl in range(self.words_per_row)]
        sel_pins.extend(col_decode_pins)
        self.connect_row_pins(self.wordline_layer, sel_pins, round=True)

    def route_array_inputs(self):

        for wl in range(self.rows):
            array_wl = self.array.wordline_names[0][wl]
            array_wl_pin = self.array_inst.get_pin(array_wl)

            wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

            end = array_wl_pin.center()
            start = vector(wl_bus_wire.cx(), end.y)

            self.add_segment_center(self.interconnect_layer, start, end)


    def route_precharge(self):

        prechrg_control = self.control_inst.get_pin("prechrg")

        col_decode_prechrg = self.col_decode_inst.get_pin("precharge_r")
        col_decode_clk = self.col_decode_inst.get_pin("clk")
        array_prechrg = self.array_inst.get_pin("precharge")

        self.add_via_stack_center(from_layer=self.route_stack[0],
                                  to_layer=prechrg_control.layer,
                                  offset=prechrg_control.center())

        # Route precharge to col decoder
        start = prechrg_control.center()
        mid1 = vector(self.control_inst.rx() + self.interconnect_layer_pitch, prechrg_control.cy())
        mid2 = vector(self.control_inst.rx() + self.interconnect_layer_pitch, col_decode_prechrg.cy())
        end = col_decode_prechrg.center()
        self.add_path(self.route_stack[0], [start, mid1, mid2, end])

        self.add_via_stack_center(from_layer=self.route_stack[0],
                                  to_layer=col_decode_prechrg.layer,
                                  offset=end)

        start = mid1
        mid1 = vector(self.control_inst.rx() + self.interconnect_layer_pitch, start.y)
        mid2 = vector(mid1.x, col_decode_clk.cy())
        end = col_decode_clk.center()
        self.add_path(self.route_stack[0], [start, mid1, mid2, end])


        # Route precharge to main array
        mid = vector(col_decode_prechrg.cx(), array_prechrg.cy() )
        self.add_path(self.route_stack[0], [array_prechrg.center(), mid, col_decode_prechrg.center()])


    def route_clock(self):
        clk_out = self.control_inst.get_pin("clk_out")
        row_decode_clk = self.decode_inst.get_pin("clk")

        self.add_via_stack_center(from_layer=self.route_stack[2],
                                  to_layer=clk_out.layer,
                                  offset=clk_out.center())

        # Route clock to row decoder
        mid = vector(self.control_inst.rx() + self.m1_pitch, clk_out.cy())

        addr_control_clk = row_decode_clk.rc() + vector( 2 * self.route_layer_pitch + self.route_layer_width, 0)
        row_decode_prechrg = self.decode_inst.get_pin("precharge")

        self.add_path(self.route_stack[2], [clk_out.center(), mid, addr_control_clk, row_decode_prechrg.center()])

        self.add_via_stack_center(from_layer=self.route_stack[2],
                                  to_layer=row_decode_clk.layer,
                                  offset=addr_control_clk)

        self.add_segment_center(row_decode_clk.layer, addr_control_clk, row_decode_clk.rc())

    def route_array_outputs(self):
        array_out_pins = [self.array_inst.get_pin("bl_0_{}".format(bl)) for bl in range(self.cols)]
        inv_in_pins = [self.bitline_inv_inst.get_pin("in_{}".format(bl)) for bl in range(self.cols)]
        inv_out_pins = [self.bitline_inv_inst.get_pin("out_{}".format(bl)) for bl in range(self.cols)]
        mux_pins = [self.mux_inst.get_pin("bl_{}".format(bl)) for bl in range(self.cols)]

        self.connect_col_pins(self.interconnect_layer, array_out_pins + inv_in_pins, round=True, directions="nonpref")
        self.connect_col_pins(self.interconnect_layer, inv_out_pins + mux_pins, round=True, directions="nonpref")

    def route_output_buffers(self):
        mux = self.mux_inst
        buf = self.output_inv_inst
        route_nets = [ [mux.get_pin("bl_out_{}".format(bit)), buf.get_pin("in_{}".format(bit))] for bit in range(self.word_size)]

        channel_ll = vector( route_nets[0][0].cx(), route_nets[0][1].cy() + self.m1_pitch * 3)
        self.create_horizontal_channel_route(netlist=route_nets, offset=channel_ll, layer_stack=self.m1_stack)

    def place_top_level_pins(self):
        self.add_io_pin(self.control_inst, "CS", "cs")
        self.add_io_pin(self.control_inst, "clk_in", "clk")

        for i in range(self.word_size):
            self.add_io_pin(self.output_inv_inst, "out_{}".format(i), "dout[{}]".format(i), directions="nonpref")

        for lsb in range(self.col_bits):
            name = "addr[{}]".format(lsb)
            self.add_io_pin(self.col_decode_inst, "A{}".format(lsb), name)

        for msb in range(self.col_bits, self.row_bits + self.col_bits):
            name = "addr[{}]".format(msb)
            pin_num = msb - self.col_bits
            self.add_io_pin(self.decode_inst, "A{}".format(pin_num), name)

    def route_supplies(self, bbox=None):

        for pin_name in ["vdd", "gnd"]:
            for inst in self.insts:
                self.copy_power_pins(inst, pin_name)

        if not OPTS.route_supplies:
            # Do not route the power supply (leave as must-connect pins)
            return
        elif OPTS.route_supplies == "grid":
            from openram.router import supply_grid_router as router
        else:
            from openram.router import supply_tree_router as router
        rtr=router(layers=self.supply_stack,
                   design=self,
                   bbox=bbox,
                   pin_type=OPTS.supply_pin_type)

        rtr.route()

        if OPTS.supply_pin_type in ["left", "right", "top", "bottom", "ring"]:
            # Find the lowest leftest pin for vdd and gnd
            for pin_name in ["vdd", "gnd"]:
                # Copy the pin shape(s) to rectangles
                for pin in self.get_pins(pin_name):
                    self.add_rect(layer=pin.layer,
                                  offset=pin.ll(),
                                  width=pin.width(),
                                  height=pin.height())

                # Remove the pin shape(s)
                self.remove_layout_pin(pin_name)

                # Get new pins
                pins = rtr.get_new_pins(pin_name)
                for pin in pins:
                    self.add_layout_pin(pin_name,
                                        pin.layer,
                                        pin.ll(),
                                        pin.width(),
                                        pin.height())

    def route_escape_pins(self, bbox):
        pins_to_route = []

        for bit in range(self.col_bits):
            pins_to_route.append("addr[{0}]".format(bit))

        for bit in range(self.row_bits):
            pins_to_route.append("addr[{0}]".format(bit + self.col_bits))

        for bit in range(self.word_size):
            pins_to_route.append("dout[{0}]".format(bit))

        pins_to_route.append("clk")
        pins_to_route.append("cs")
        from openram.router import signal_escape_router as router
        rtr=router(layers=self.m3_stack,
                   design=self,
                   bbox=bbox)
        rtr.escape_route(pins_to_route)
