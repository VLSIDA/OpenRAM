# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram.base import design
from openram.base import logical_effort
from openram.base import vector
from openram.sram_factory import factory
from openram import OPTS


class control_logic_base(design):
    """
    Generic base class for SRAM control logic.
    """

    def __init__(self, num_rows, words_per_row, word_size, spare_columns=None, sram=None, port_type="rw", name=""):
        """ Constructor """
        name = "control_logic_" + port_type
        super().__init__(name)
        debug.info(1, "Creating {}".format(name))
        self.add_comment("num_rows: {0}".format(num_rows))
        self.add_comment("words_per_row: {0}".format(words_per_row))
        self.add_comment("word_size {0}".format(word_size))

        self.sram=sram
        self.num_rows = num_rows
        self.words_per_row = words_per_row
        self.word_size = word_size
        self.port_type = port_type

        if not spare_columns:
            self.num_spare_cols = 0
        else:
            self.num_spare_cols = spare_columns

        self.num_cols = word_size * words_per_row + self.num_spare_cols
        self.num_words = num_rows * words_per_row

        self.enable_delay_chain_resizing = False
        self.inv_parasitic_delay = logical_effort.pinv

        # Determines how much larger the sen delay should be. Accounts for possible error in model.
        # FIXME: This should be made a parameter
        self.wl_timing_tolerance = 1
        self.wl_stage_efforts = None
        self.sen_stage_efforts = None

        if self.port_type == "rw":
            self.num_control_signals = 2
        else:
            self.num_control_signals = 1

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.setup_signal_busses()
        self.add_pins()
        self.add_modules()
        self.create_instances()

    def create_layout(self):
        """ Create layout and route between modules """
        self.place_instances()
        self.route_all()
        # self.add_lvs_correspondence_points()
        self.add_boundary()
        self.DRC_LVS()

    def get_dynamic_delay_chain_size(self, previous_stages, previous_fanout):
        """Determine the size of the delay chain used for the Sense Amp Enable using path delays"""
        from math import ceil
        previous_delay_chain_delay = (previous_fanout + 1 + self.inv_parasitic_delay) * previous_stages
        debug.info(2, "Previous delay chain produced {} delay units".format(previous_delay_chain_delay))

        # This can be anything >=2
        delay_fanout = 3
        # The delay chain uses minimum sized inverters. There are (fanout+1)*stages inverters and each
        # inverter adds 1 unit of delay (due to minimum size). This also depends on the pinv value
        required_delay = self.wl_delay * self.wl_timing_tolerance - (self.sen_delay - previous_delay_chain_delay)
        debug.check(required_delay > 0, "Cannot size delay chain to have negative delay")
        delay_per_stage = delay_fanout + 1 + self.inv_parasitic_delay
        delay_stages = ceil(required_delay / delay_per_stage)
        # force an even number of stages.
        if delay_stages % 2 == 1:
            delay_stages += 1
            # Fanout can be varied as well but is a little more complicated but potentially optimal.
        debug.info(1, "Setting delay chain to {} stages with {} fanout to match {} delay".format(delay_stages, delay_fanout, required_delay))
        return (delay_stages, delay_fanout)

    def get_dynamic_delay_fanout_list(self, previous_stages, previous_fanout):
        """Determine the size of the delay chain used for the Sense Amp Enable using path delays"""

        previous_delay_per_stage = previous_fanout + 1 + self.inv_parasitic_delay
        previous_delay_chain_delay = previous_delay_per_stage * previous_stages
        debug.info(2, "Previous delay chain produced {} delay units".format(previous_delay_chain_delay))

        fanout_rise = fanout_fall = 2 # This can be anything >=2
        # The delay chain uses minimum sized inverters. There are (fanout+1)*stages inverters and each
        # inverter adds 1 unit of delay (due to minimum size). This also depends on the pinv value
        required_delay_fall = self.wl_delay_fall * self.wl_timing_tolerance - \
                              (self.sen_delay_fall - previous_delay_chain_delay / 2)
        required_delay_rise = self.wl_delay_rise * self.wl_timing_tolerance - \
                              (self.sen_delay_rise - previous_delay_chain_delay / 2)
        debug.info(2,
                   "Required delays from chain: fall={}, rise={}".format(required_delay_fall,
                                                                         required_delay_rise))

        # If the fanout is different between rise/fall by this amount. Stage algorithm is made more pessimistic.
        WARNING_FANOUT_DIFF = 5
        stages_close = False
        # The stages need to be equal (or at least a even number of stages with matching rise/fall delays)
        while True:
            stages_fall = self.calculate_stages_with_fixed_fanout(required_delay_fall,
                                                                  fanout_fall)
            stages_rise = self.calculate_stages_with_fixed_fanout(required_delay_rise,
                                                                  fanout_rise)
            debug.info(1,
                       "Fall stages={}, rise stages={}".format(stages_fall,
                                                               stages_rise))
            if abs(stages_fall - stages_rise) == 1 and not stages_close:
                stages_close = True
                safe_fanout_rise = fanout_rise
                safe_fanout_fall = fanout_fall

            if stages_fall == stages_rise:
                break
            elif abs(stages_fall - stages_rise) == 1 and WARNING_FANOUT_DIFF < abs(fanout_fall - fanout_rise):
                debug.info(1, "Delay chain fanouts between stages are large. Making chain size larger for safety.")
                fanout_rise = safe_fanout_rise
                fanout_fall = safe_fanout_fall
                break
            # There should also be a condition to make sure the fanout does not get too large.
            # Otherwise, increase the fanout of delay with the most stages, calculate new stages
            elif stages_fall>stages_rise:
                fanout_fall+=1
            else:
                fanout_rise+=1

        total_stages = max(stages_fall, stages_rise) * 2
        debug.info(1, "New Delay chain: stages={}, fanout_rise={}, fanout_fall={}".format(total_stages, fanout_rise, fanout_fall))

        # Creates interleaved fanout list of rise/fall delays. Assumes fall is the first stage.
        stage_list = [fanout_fall if i % 2==0 else fanout_rise for i in range(total_stages)]
        return stage_list

    def calculate_stages_with_fixed_fanout(self, required_delay, fanout):
        from math import ceil
        # Delay being negative is not an error. It implies that any amount of stages would have a negative effect on the overall delay
        # 3 is the minimum delay per stage (with pinv=0).
        if required_delay <= 3 + self.inv_parasitic_delay:
            return 1
        delay_per_stage = fanout + 1 + self.inv_parasitic_delay
        delay_stages = ceil(required_delay / delay_per_stage)
        return delay_stages

    def route_rails(self):
        """ Add the input signal inverted tracks """
        height = self.control_logic_center.y - self.m2_pitch
        # DFF spacing plus the power routing
        offset = vector(self.ctrl_dff_array.width + self.m4_pitch, 0)

        self.input_bus = self.create_vertical_bus("m2",
                                                  offset,
                                                  self.internal_bus_list,
                                                  height)

    def place_instances(self):
        """ Place all the instances """
        # Keep track of all right-most instances to determine row boundary
        # and add the vdd/gnd pins
        self.row_end_inst = []

        # Add the control flops on the left of the bus
        self.place_dffs()

        # All of the control logic is placed to the right of the DFFs and bus
        # as well as the power supply stripe
        self.control_x_offset = self.ctrl_dff_array.width + self.internal_bus_width + self.m4_pitch

        self.place_logic_rows()

        # Delay chain always gets placed at row 4
        self.place_delay(4)
        height = self.delay_inst.uy()

        # This offset is used for placement of the control logic in the SRAM level.
        self.control_logic_center = vector(self.ctrl_dff_inst.rx(), self.control_center_y)

        # Extra pitch on top and right
        self.height = height + 2 * self.m1_pitch
        # Max of modules or logic rows
        self.width = max([inst.rx() for inst in self.row_end_inst])
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.width = max(self.delay_inst.rx(), self.width)
        self.width += self.m2_pitch

    def place_delay(self, row):
        """ Place the delay chain """
        debug.check(row % 2 == 0, "Must place delay chain at even row for supply alignment.")

        # It is flipped on X axis
        y_off = row * self.and2.height + self.delay_chain.height

        # Add to the right of the control rows and routing channel
        offset = vector(0, y_off)
        self.delay_inst.place(offset, mirror="MX")

    def create_clk_buf_row(self):
        """ Create the multistage and gated clock buffer  """
        self.clk_buf_inst = self.add_inst(name="clkbuf",
                                          mod=self.clk_buf_driver)
        self.connect_inst(["clk", "clk_buf", "vdd", "gnd"])

    def place_clk_buf_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.clk_buf_inst, x_offset, row)

        self.row_end_inst.append(self.clk_buf_inst)

    def route_clk_buf(self):
        clk_pin = self.clk_buf_inst.get_pin("A")
        clk_pos = clk_pin.center()
        self.add_layout_pin_rect_center(text="clk",
                                        layer="m2",
                                        offset=clk_pos)
        self.add_via_stack_center(from_layer=clk_pin.layer,
                                  to_layer="m2",
                                  offset=clk_pos)

        self.route_output_to_bus_jogged(self.clk_buf_inst,
                                        "clk_buf")
        self.connect_output(self.clk_buf_inst, "Z", "clk_buf")

    def create_gated_clk_bar_row(self):
        self.clk_bar_inst = self.add_inst(name="inv_clk_bar",
                                            mod=self.inv)
        self.connect_inst(["clk_buf", "clk_bar", "vdd", "gnd"])

        self.gated_clk_bar_inst = self.add_inst(name="and2_gated_clk_bar",
                                                mod=self.and2)
        self.connect_inst(["clk_bar", "cs", "gated_clk_bar", "vdd", "gnd"])

    def place_gated_clk_bar_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.clk_bar_inst, x_offset, row)
        x_offset = self.place_util(self.gated_clk_bar_inst, x_offset, row)

        self.row_end_inst.append(self.gated_clk_bar_inst)

    def route_gated_clk_bar(self):
        clkbuf_map = zip(["A"], ["clk_buf"])
        self.connect_vertical_bus(clkbuf_map, self.clk_bar_inst, self.input_bus)

        out_pin = self.clk_bar_inst.get_pin("Z")
        out_pos = out_pin.center()
        in_pin = self.gated_clk_bar_inst.get_pin("A")
        in_pos = in_pin.center()
        self.add_zjog(out_pin.layer, out_pos, in_pos)
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer=in_pin.layer,
                                  offset=in_pos)


        # This is the second gate over, so it needs to be on M3
        clkbuf_map = zip(["B"], ["cs"])
        self.connect_vertical_bus(clkbuf_map,
                                  self.gated_clk_bar_inst,
                                  self.input_bus,
                                  self.m2_stack[::-1])
        # The pin is on M1, so we need another via as well
        b_pin = self.gated_clk_bar_inst.get_pin("B")
        self.add_via_stack_center(from_layer=b_pin.layer,
                                  to_layer="m3",
                                  offset=b_pin.center())

        # This is the second gate over, so it needs to be on M3
        self.route_output_to_bus_jogged(self.gated_clk_bar_inst,
                                        "gated_clk_bar")

    def create_gated_clk_buf_row(self):
        self.gated_clk_buf_inst = self.add_inst(name="and2_gated_clk_buf",
                                                mod=self.and2)
        self.connect_inst(["clk_buf", "cs", "gated_clk_buf", "vdd", "gnd"])

    def place_gated_clk_buf_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.gated_clk_buf_inst, x_offset, row)

        self.row_end_inst.append(self.gated_clk_buf_inst)

    def route_gated_clk_buf(self):
        clkbuf_map = zip(["A", "B"], ["clk_buf", "cs"])
        self.connect_vertical_bus(clkbuf_map,
                                  self.gated_clk_buf_inst,
                                  self.input_bus)

        clkbuf_map = zip(["Z"], ["gated_clk_buf"])
        self.connect_vertical_bus(clkbuf_map,
                                  self.gated_clk_buf_inst,
                                  self.input_bus,
                                  self.m2_stack[::-1])
        # The pin is on M1, so we need another via as well
        z_pin = self.gated_clk_buf_inst.get_pin("Z")
        self.add_via_stack_center(from_layer=z_pin.layer,
                                  to_layer="m2",
                                  offset=z_pin.center())

    def create_dffs(self):
        self.ctrl_dff_inst=self.add_inst(name="ctrl_dffs",
                                         mod=self.ctrl_dff_array)
        inst_pins = self.input_list + self.dff_output_list + ["clk_buf"] + self.supply_list
        self.connect_inst(inst_pins)

    def place_dffs(self):
        self.ctrl_dff_inst.place(vector(0, 0))

    def route_dffs(self):
        if self.port_type == "rw":
            dff_out_map = zip(["dout_bar_0", "dout_bar_1", "dout_1"], ["cs", "we", "we_bar"])
        else:
            dff_out_map = zip(["dout_bar_0"], ["cs"])
        self.connect_vertical_bus(dff_out_map, self.ctrl_dff_inst, self.input_bus, self.m2_stack[::-1])

        # Connect the clock rail to the other clock rail
        # by routing in the supply rail track to avoid channel conflicts
        in_pos = self.ctrl_dff_inst.get_pin("clk").uc()
        mid_pos = vector(in_pos.x, self.gated_clk_buf_inst.get_pin("vdd").cy() - self.m1_pitch)
        rail_pos = vector(self.input_bus["clk_buf"].cx(), mid_pos.y)
        self.add_wire(self.m1_stack, [in_pos, mid_pos, rail_pos])
        self.add_via_center(layers=self.m1_stack,
                            offset=rail_pos)

        self.copy_layout_pin(self.ctrl_dff_inst, "din_0", "csb")
        if (self.port_type == "rw"):
            self.copy_layout_pin(self.ctrl_dff_inst, "din_1", "web")

    def get_offset(self, row):
        """ Compute the y-offset and mirroring """
        y_off = row * self.and2.height
        if row % 2:
            y_off += self.and2.height
            mirror="MX"
        else:
            mirror="R0"

        return (y_off, mirror)

    def connect_output(self, inst, pin_name, out_name):
        """ Create an output pin on the right side from the pin of a given instance. """

        out_pin = inst.get_pin(pin_name)
        out_pos = out_pin.center()
        right_pos = out_pos + vector(self.width - out_pin.cx(), 0)

        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer="m2",
                                  offset=out_pos)
        self.add_layout_pin_segment_center(text=out_name,
                                           layer="m2",
                                           start=out_pos,
                                           end=right_pos)

    def route_supplies(self):
        """ Add vdd and gnd to the instance cells """

        pin_layer = self.dff.get_pin("vdd").layer
        supply_layer = self.supply_stack[2]


        # FIXME: We should be able to replace this with route_vertical_pins instead
        # but we may have to make the logic gates a separate module so that they
        # have row pins of the same width
        max_row_x_loc = max([inst.rx() for inst in self.row_end_inst])
        min_row_x_loc = self.control_x_offset

        vdd_pin_locs = []
        gnd_pin_locs = []

        last_via = None
        for inst in self.row_end_inst:
            pins = inst.get_pins("vdd")
            for pin in pins:
                if pin.layer == pin_layer:
                    row_loc = pin.rc()
                    pin_loc = vector(max_row_x_loc, pin.rc().y)
                    vdd_pin_locs.append(pin_loc)
                    last_via = self.add_via_stack_center(from_layer=pin_layer,
                                                         to_layer=supply_layer,
                                                         offset=pin_loc,
                                                         min_area=True)
                    self.add_path(pin_layer, [row_loc, pin_loc])

            pins = inst.get_pins("gnd")
            for pin in pins:
                if pin.layer == pin_layer:
                    row_loc = pin.rc()
                    pin_loc = vector(min_row_x_loc, pin.rc().y)
                    gnd_pin_locs.append(pin_loc)
                    last_via = self.add_via_stack_center(from_layer=pin_layer,
                                                         to_layer=supply_layer,
                                                         offset=pin_loc,
                                                         min_area=True)
                    self.add_path(pin_layer, [row_loc, pin_loc])

        if last_via:
            via_height=last_via.mod.second_layer_height
            via_width=last_via.mod.second_layer_width
        else:
            via_height=None
            via_width=0

        min_y = min([x.y for x in vdd_pin_locs])
        max_y = max([x.y for x in vdd_pin_locs])
        bot_pos = vector(max_row_x_loc, min_y - 0.5 * via_height)
        top_pos = vector(max_row_x_loc, max_y + 0.5 * via_height)
        self.add_layout_pin_segment_center(text="vdd",
                                           layer=supply_layer,
                                           start=bot_pos,
                                           end=top_pos,
                                           width=via_width)

        min_y = min([x.y for x in gnd_pin_locs])
        max_y = max([x.y for x in gnd_pin_locs])
        bot_pos = vector(min_row_x_loc, min_y - 0.5 * via_height)
        top_pos = vector(min_row_x_loc, max_y + 0.5 * via_height)
        self.add_layout_pin_segment_center(text="gnd",
                                           layer=supply_layer,
                                           start=bot_pos,
                                           end=top_pos,
                                           width=via_width)

        self.copy_layout_pin(self.delay_inst, "gnd")
        self.copy_layout_pin(self.delay_inst, "vdd")

        self.copy_layout_pin(self.ctrl_dff_inst, "gnd")
        self.copy_layout_pin(self.ctrl_dff_inst, "vdd")

    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong.
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # pin=self.clk_inv1.get_pin("Z")
        # self.add_label_pin(text="clk1_bar",
        #                    layer="m1",
        #                    offset=pin.ll(),
        #                    height=pin.height(),
        #                    width=pin.width())

        # pin=self.clk_inv2.get_pin("Z")
        # self.add_label_pin(text="clk2",
        #                    layer="m1",
        #                    offset=pin.ll(),
        #                    height=pin.height(),
        #                    width=pin.width())

        pin=self.delay_inst.get_pin("out")
        self.add_label_pin(text="out",
                           layer=pin.layer,
                           offset=pin.ll(),
                           height=pin.height(),
                           width=pin.width())

    def graph_exclude_dffs(self):
        """Exclude dffs from graph as they do not represent critical path"""

        self.graph_inst_exclude.add(self.ctrl_dff_inst)
        if self.port_type=="rw" or self.port_type=="w":
            self.graph_inst_exclude.add(self.w_en_gate_inst)

    def place_util(self, inst, x_offset, row):
        """ Utility to place a row and compute the next offset """

        (y_offset, mirror) = self.get_offset(row)
        offset = vector(x_offset, y_offset)
        inst.place(offset, mirror)
        return x_offset + inst.width

    def route_output_to_bus_jogged(self, inst, name):
        # Connect this at the bottom of the buffer
        out_pin = inst.get_pin("Z")
        out_pos = out_pin.center()
        mid1 = vector(out_pos.x, out_pos.y - 0.3 * inst.mod.height)
        mid2 = vector(self.input_bus[name].cx(), mid1.y)
        bus_pos = self.input_bus[name].center()
        self.add_wire(self.m2_stack[::-1], [out_pos, mid1, mid2, bus_pos])
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer="m2",
                                  offset=out_pos)

    def get_left_pins(self, name):
        """
        Return the left side supply pins to connect to a vertical stripe.
        """
        return(self.cntrl_dff_inst.get_pins(name) + self.delay_inst.get_pins(name))
