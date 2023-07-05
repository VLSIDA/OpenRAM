# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import math
from openram import debug
from openram import OPTS
from openram.base import design
from openram.base import vector
from openram.base import logical_effort, convert_farad_to_relative_c
from openram.tech import drc, spice
from openram.sram_factory import factory
from .control_logic_base import control_logic_base


class control_logic_delay(control_logic_base):
    """
    Dynamically generated Control logic for the total SRAM circuit.
    Variant: delay-based
    """

    def __init__(self, num_rows, words_per_row, word_size, spare_columns=None, sram=None, port_type="rw", name=""):
        """ Constructor """
        super().__init__(num_rows, words_per_row, word_size, spare_columns, sram, port_type, name)

    def add_pins(self):
        """ Add the pins to the control logic module. """
        self.add_pin_list(self.input_list + ["clk"], "INPUT")
        self.add_pin_list(self.output_list, "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        """ Add all the required modules """

        self.dff = factory.create(module_type="dff_buf")
        dff_height = self.dff.height

        self.ctrl_dff_array = factory.create(module_type="dff_buf_array",
                                             rows=self.num_control_signals,
                                             columns=1)

        self.and2 = factory.create(module_type="pand2",
                                   size=12,
                                   height=dff_height)

        # clk_buf drives a flop for every address
        addr_flops = math.log(self.num_words, 2) + math.log(self.words_per_row, 2)
        # plus data flops and control flops
        num_flops = addr_flops + self.word_size + self.num_spare_cols + self.num_control_signals
        # each flop internally has a FO 5 approximately
        # plus about 5 fanouts for the control logic
        clock_fanout = 5 * num_flops + 5
        self.clk_buf_driver = factory.create(module_type="pdriver",
                                             fanout=clock_fanout,
                                             height=dff_height)

        # We will use the maximum since this same value is used to size the wl_en
        # and the p_en_bar drivers
        # max_fanout = max(self.num_rows, self.num_cols)

        # wl_en drives every row in the bank
        # this calculation is from the rbl control logic, it may not be optimal in this circuit
        size_list = [max(int(self.num_rows / 9), 1), max(int(self.num_rows / 3), 1)]
        self.wl_en_driver = factory.create(module_type="pdriver",
                                           size_list=size_list,
                                           height=dff_height)

        # this is the weak timing signal that feeds wl_en_driver
        self.wl_en_and = factory.create(module_type="pand2",
                                        size=1,
                                        height=dff_height)

        # w_en drives every write driver
        self.wen_and = factory.create(module_type="pand3",
                                      size=self.word_size + 8,
                                      height=dff_height)

        # s_en drives every sense amp
        self.sen_and3 = factory.create(module_type="pand3",
                                       size=self.word_size + self.num_spare_cols,
                                       height=dff_height)

        # used to generate inverted signals with low fanout
        self.inv = factory.create(module_type="pinv",
                                  size=1,
                                  height=dff_height)

        # p_en_bar drives every column in the bitcell array
        # but it is sized the same as the wl_en driver with
        # prepended 3 inverter stages to guarantee it is slower and odd polarity
        self.p_en_bar_driver = factory.create(module_type="pdriver",
                                              fanout=self.num_cols,
                                              height=dff_height)

        self.nand2 = factory.create(module_type="pnand2",
                                    height=dff_height)

        self.compute_delay_chain_size()
        self.delay_chain = factory.create(module_type="multi_delay_chain",
                                          fanout_list=self.delay_chain_fanout_list,
                                          pinout_list=self.delay_chain_pinout_list)

    def compute_delay_chain_size(self):
        """
        calculate the pinouts needed for the delay chain based on
        wordline, bitline, and precharge delays
        delays 0 & 1 need to be even for polarity
        delays 2 - 4 need to be odd for polarity
        """
        bitcell = factory.create(module_type=OPTS.bitcell)
        # TODO: check that these spice values are up to date in tech files and if not figure out how to update them
        # 2 access tx gate per cell
        wordline_area = bitcell.width * drc("minwidth_m1")
        wordline_cap_ff = self.num_cols * (2 * spice["min_tx_gate_c"] + spice["wire_unit_c"] * 1e15 * wordline_area)
        wordline_cap = convert_farad_to_relative_c(wordline_cap_ff)
        # 1 access tx drain per cell
        bitline_area = bitcell.height * drc("minwidth_m2")
        bitline_cap_ff = self.num_rows * (spice["min_tx_drain_c"] + spice["wire_unit_c"] * 1e15 * bitline_area)
        bitline_cap = convert_farad_to_relative_c(bitline_cap_ff)
        # 3 pmos gate per cell
        pen_cap_ff = self.num_cols * (3 * spice["min_tx_gate_c"] + spice["wire_unit_c"] * 1e15 * wordline_area)
        pen_cap = convert_farad_to_relative_c(pen_cap_ff)
        # number of stages in the p_en driver
        pen_stages = self.p_en_bar_driver.num_stages

        inverter_stage_delay = logical_effort("inv", 1, 1, OPTS.delay_chain_fanout_per_stage, 1, True).get_absolute_delay()
        # model precharge as a minimum sized inverter with the bitline as its load
        precharge_delay = logical_effort("precharge", 1, 1, bitline_cap, 1, True).get_absolute_delay()
        # exponential horn delay from logical effort paper (converted to absolute delay)
        pen_signal_delay = logical_effort.tau * (pen_stages * (pen_cap ** (1 / pen_stages) + 1))
        # size is a pessimistic version of wordline_driver module's FO4 sizing
        wordline_driver_size = int(self.num_cols / 4) + 1
        wordline_delay = logical_effort("wordline", wordline_driver_size, 1, wordline_cap, 1, True).get_absolute_delay()
        # wl_en driver is always two stages so add each independently?
        wlen_signal_delay = logical_effort("wlen_driver", self.wl_en_driver.size_list[0], 1, self.wl_en_driver.size_list[1], 1, True).get_absolute_delay()
        wlen_signal_delay += logical_effort("wlen_driver", self.wl_en_driver.size_list[1], 1, wordline_driver_size * self.num_rows, 1, True).get_absolute_delay()
        # time for bitline to drop from vdd by threshold voltage once wordline enabled
        bitline_vth_swing = (spice["nom_supply_voltage"] - spice["nom_threshold"]) / spice["nom_supply_voltage"]
        bitline_vth_delay = abs(math.log(1 - bitline_vth_swing)) * spice["wire_unit_r"] * bitline_area * bitline_cap_ff
        # print("delays: delay_stage {} precharge {} pen {} wl {} wlen {} vth {}".format(inverter_stage_delay, precharge_delay, pen_signal_delay, wordline_delay, wlen_signal_delay, bitline_vth_delay))

        delays = [None] * 5
        # keepout between p_en rising and wl_en falling
        delays[0] = (wlen_signal_delay + wordline_delay) / inverter_stage_delay # could possibly subtract pen_signal_delay?
        delays[0] = int(delays[0] * OPTS.delay_control_scaling_factor)
        # round up to nearest even integer
        delays[0] += delays[0] % 2
        delays[2] = delays[0] + (pen_signal_delay + precharge_delay) / inverter_stage_delay
        delays[2] *= OPTS.delay_control_scaling_factor
        # round up to nearest odd integer
        delays[2] = int(1 - (2 * ((1 - delays[2]) // 2)))
        # delays[1] can be any even value less than delays[2]
        delays[1] = delays[2] - 1
        # keepout between p_en falling and wl_en rising
        delays[3] = delays[2] + pen_signal_delay / inverter_stage_delay
        delays[3] *= OPTS.delay_control_scaling_factor
        delays[3] = int(1 - (2 * ((1 - delays[3]) // 2)))
        delays[4] = delays[3] + (wlen_signal_delay + wordline_delay + bitline_vth_delay) / inverter_stage_delay
        delays[4] *= OPTS.delay_control_scaling_factor
        delays[4] = int(1 - (2 * ((1 - delays[4]) // 2)))
        self.delay_chain_pinout_list = delays
        # FIXME: fanout should be used to control delay chain height
        # for now, use default/user-defined fanout constant
        self.delay_chain_fanout_list = self.delay_chain_pinout_list[-1] * [OPTS.delay_chain_fanout_per_stage]

    def setup_signal_busses(self):
        """ Setup bus names, determine the size of the busses etc """

        # List of input control signals
        if self.port_type == "rw":
            self.input_list = ["csb", "web"]
        else:
            self.input_list = ["csb"]

        if self.port_type == "rw":
            self.dff_output_list = ["cs_bar", "cs", "we_bar", "we"]
        else:
            self.dff_output_list = ["cs_bar", "cs"]

        # list of output control signals (for making a vertical bus)
        if self.port_type == "rw":
            self.internal_bus_list = ["glitch1", "glitch2", "delay0", "delay1", "delay2", "delay3", "delay4", "gated_clk_bar", "gated_clk_buf", "we", "we_bar", "clk_buf", "cs"]
        else:
            self.internal_bus_list = ["glitch1", "glitch2", "delay0", "delay1", "delay2", "delay3", "delay4", "gated_clk_bar", "gated_clk_buf", "clk_buf", "cs"]
        # leave space for the bus plus one extra space
        self.internal_bus_width = (len(self.internal_bus_list) + 1) * self.m2_pitch

        # Outputs to the bank
        if self.port_type == "rw":
            self.output_list = ["s_en", "w_en"]
        elif self.port_type == "r":
            self.output_list = ["s_en"]
        else:
            self.output_list = ["w_en"]
        self.output_list.append("p_en_bar")
        self.output_list.append("wl_en")
        self.output_list.append("clk_buf")

        self.supply_list = ["vdd", "gnd"]

    def create_instances(self):
        """ Create all the instances """
        self.create_dffs()
        self.create_clk_buf_row()
        self.create_gated_clk_bar_row()
        self.create_gated_clk_buf_row()
        self.create_delay()
        self.create_glitches()
        self.create_wlen_row()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.create_wen_row()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.create_sen_row()
        self.create_pen_row()

    def place_logic_rows(self):
        row = 0
        self.place_clk_buf_row(row)
        row += 1
        self.place_gated_clk_bar_row(row)
        row += 1
        self.place_gated_clk_buf_row(row)
        row += 1
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.place_sen_row(row)
            row += 1
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.place_wen_row(row)
            row += 1
        self.place_pen_row(row)
        row += 1
        self.place_wlen_row(row)
        row += 1
        self.place_glitch1_row(row)
        row += 1
        self.place_glitch2_row(row)

        self.control_center_y = self.glitch2_nand_inst.uy() + self.m3_pitch

    def route_all(self):
        """ Routing between modules """
        self.route_rails()
        self.route_dffs()
        self.route_wlen()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.route_wen()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.route_sen()
        self.route_delay()
        self.route_pen()
        self.route_glitches()
        self.route_clk_buf()
        self.route_gated_clk_bar()
        self.route_gated_clk_buf()
        self.route_supplies()

    def create_delay(self):
        """ Create the delay chain """
        self.delay_inst=self.add_inst(name="multi_delay_chain",
                                      mod=self.delay_chain)
        self.connect_inst(["gated_clk_buf", "delay0", "delay1", "delay2", "delay3", "delay4", "vdd", "gnd"])

    def route_delay(self):
        # this is a bit of a hack because I would prefer to just name these pins delay in the layout
        # instead I have this which duplicates the out_pin naming logic from multi_delay_chain.py
        out_pins = ["out{}".format(str(pin)) for pin in self.delay_chain.pinout_list]
        delay_map = zip(["in", out_pins[0], out_pins[1], out_pins[2], out_pins[3], out_pins[4]], \
            ["gated_clk_buf", "delay0", "delay1", "delay2", "delay3", "delay4"])

        self.connect_vertical_bus(delay_map,
                                  self.delay_inst,
                                  self.input_bus,
                                  self.m2_stack[::-1])

    # glitch{0-2} are internal timing signals based on different in/out
    # points on the delay chain for adjustable start time and duration
    def create_glitches(self):
        self.glitch0_nand_inst = self.add_inst(name="nand2_glitch0",
                                               mod=self.nand2)
        self.connect_inst(["delay0", "delay2", "glitch0", "vdd", "gnd"])

        self.glitch1_nand_inst = self.add_inst(name="nand2_glitch1",
                                               mod=self.nand2)
        self.connect_inst(["gated_clk_buf", "delay3", "glitch1", "vdd", "gnd"])

        self.glitch2_nand_inst = self.add_inst(name="nand2_glitch2",
                                               mod=self.nand2)
        self.connect_inst(["delay1", "delay4", "glitch2", "vdd", "gnd"])

    # glitch0 is placed in place_pen_row()

    def place_glitch1_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.glitch1_nand_inst, x_offset, row)

        self.row_end_inst.append(self.glitch1_nand_inst)

    def place_glitch2_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.glitch2_nand_inst, x_offset, row)

        self.row_end_inst.append(self.glitch2_nand_inst)

    def route_glitches(self):
        glitch1_map = zip(["A", "B", "Z"], ["gated_clk_buf", "delay3", "glitch1"])

        self.connect_vertical_bus(glitch1_map, self.glitch1_nand_inst, self.input_bus)

        glitch2_map = zip(["A", "B", "Z"], ["delay1", "delay4", "glitch2"])

        self.connect_vertical_bus(glitch2_map, self.glitch2_nand_inst, self.input_bus)

    def create_wlen_row(self):
        self.wl_en_unbuf_and_inst = self.add_inst(name="and_wl_en_unbuf",
                                                  mod=self.wl_en_and)
        self.connect_inst(["cs", "glitch1", "wl_en_unbuf", "vdd", "gnd"])

        self.wl_en_driver_inst=self.add_inst(name="buf_wl_en",
                                      mod=self.wl_en_driver)
        self.connect_inst(["wl_en_unbuf", "wl_en", "vdd", "gnd"])

    def place_wlen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.wl_en_unbuf_and_inst, x_offset, row)
        x_offset = self.place_util(self.wl_en_driver_inst, x_offset, row)

        self.row_end_inst.append(self.wl_en_driver_inst)

    def route_wlen(self):
        in_map = zip(["A", "B"], ["cs", "glitch1"])
        self.connect_vertical_bus(in_map, self.wl_en_unbuf_and_inst, self.input_bus)

        out_pin = self.wl_en_unbuf_and_inst.get_pin("Z")
        out_pos = out_pin.center()
        in_pin = self.wl_en_driver_inst.get_pin("A")
        in_pos = in_pin.center()
        mid1 = vector(out_pos.x, in_pos.y)
        self.add_path(out_pin.layer, [out_pos, mid1, in_pos])
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer=in_pin.layer,
                                  offset=in_pin.center())
        self.connect_output(self.wl_en_driver_inst, "Z", "wl_en")

    def create_pen_row(self):
        self.p_en_bar_driver_inst=self.add_inst(name="buf_p_en_bar",
                                                mod=self.p_en_bar_driver)
        self.connect_inst(["glitch0", "p_en_bar", "vdd", "gnd"])

    def place_pen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.glitch0_nand_inst, x_offset, row)
        x_offset = self.place_util(self.p_en_bar_driver_inst, x_offset, row)

        self.row_end_inst.append(self.p_en_bar_driver_inst)

    def route_pen(self):
        in_map = zip(["A", "B"], ["delay0", "delay2"])
        self.connect_vertical_bus(in_map, self.glitch0_nand_inst, self.input_bus)

        out_pin = self.glitch0_nand_inst.get_pin("Z") # same code here as wl_en, refactor?
        out_pos = out_pin.center()
        in_pin = self.p_en_bar_driver_inst.get_pin("A")
        in_pos = in_pin.center()
        mid1 = vector(in_pos.x, out_pos.y)
        self.add_path(out_pin.layer, [out_pos, mid1, in_pos])
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer=in_pin.layer,
                                  offset=in_pin.center())

        self.connect_output(self.p_en_bar_driver_inst, "Z", "p_en_bar")

    def create_sen_row(self):
        if self.port_type=="rw":
            input_name = "we_bar"
        else:
            input_name = "cs"

        self.s_en_gate_inst = self.add_inst(name="and_s_en",
                                            mod=self.sen_and3)
        self.connect_inst(["glitch2", "gated_clk_bar", input_name, "s_en", "vdd", "gnd"])

    def place_sen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.s_en_gate_inst, x_offset, row)

        self.row_end_inst.append(self.s_en_gate_inst)

    def route_sen(self):

        if self.port_type=="rw": # this is repeated many times in here, refactor?
            input_name = "we_bar"
        else:
            input_name = "cs"

        sen_map = zip(["A", "B", "C"], ["glitch2", "gated_clk_bar", input_name])
        self.connect_vertical_bus(sen_map, self.s_en_gate_inst, self.input_bus)

        self.connect_output(self.s_en_gate_inst, "Z", "s_en")

    def create_wen_row(self):
        self.glitch2_bar_inv_inst = self.add_inst(name="inv_glitch2_bar",
                                                  mod=self.inv)
        self.connect_inst(["glitch2", "glitch2_bar", "vdd", "gnd"])

        if self.port_type == "rw":
            input_name = "we"
        else:
            input_name = "cs"

        self.w_en_gate_inst = self.add_inst(name="and_w_en",
                                            mod=self.wen_and)
        self.connect_inst([input_name, "glitch1", "glitch2_bar", "w_en", "vdd", "gnd"])

    def place_wen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.glitch2_bar_inv_inst, x_offset, row)
        x_offset = self.place_util(self.w_en_gate_inst, x_offset, row)

        self.row_end_inst.append(self.w_en_gate_inst)

    def route_wen(self): # w_en comes from a 3and but one of the inputs needs to be inverted
        glitch2_map = zip(["A"], ["glitch2"])
        self.connect_vertical_bus(glitch2_map, self.glitch2_bar_inv_inst, self.input_bus)

        out_pin = self.glitch2_bar_inv_inst.get_pin("Z")
        out_pos = out_pin.center()
        in_pin = self.w_en_gate_inst.get_pin("C")
        in_pos = in_pin.center()
        mid1 = vector(in_pos.x, out_pos.y)
        self.add_path(out_pin.layer, [out_pos, mid1, in_pos])
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer=in_pin.layer,
                                  offset=in_pos)

        if self.port_type == "rw":
            input_name = "we"
        else:
            input_name = "cs"

        # This is the second gate over, so it needs to be on M3
        wen_map = zip(["A", "B"], [input_name, "glitch1"])
        self.connect_vertical_bus(wen_map,
                                  self.w_en_gate_inst,
                                  self.input_bus,
                                  self.m2_stack[::-1])

        # The pins are on M1, so we need more vias as well
        a_pin = self.w_en_gate_inst.get_pin("A")
        self.add_via_stack_center(from_layer=a_pin.layer,
                                  to_layer="m3",
                                  offset=a_pin.center())

        b_pin = self.w_en_gate_inst.get_pin("B")
        self.add_via_stack_center(from_layer=b_pin.layer,
                                  to_layer="m3",
                                  offset=b_pin.center())

        self.connect_output(self.w_en_gate_inst, "Z", "w_en")
