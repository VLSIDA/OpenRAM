# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from tech import cell_properties as props
import debug
from sram_factory import factory
import math
from vector import vector
from globals import OPTS
import logical_effort


class control_logic(design.design):
    """
    Dynamically generated Control logic for the total SRAM circuit.
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
        self.inv_parasitic_delay = logical_effort.logical_effort.pinv
        
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

    def add_pins(self):
        """ Add the pins to the control logic module. """
        self.add_pin_list(self.input_list + ["clk"] + self.rbl_list, "INPUT")
        self.add_pin_list(self.output_list, "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        """ Add all the required modules """
        
        dff = factory.create(module_type="dff_buf")
        dff_height = dff.height
        
        self.ctrl_dff_array = factory.create(module_type="dff_buf_array",
                                             rows=self.num_control_signals,
                                             columns=1)
                                             
        self.add_mod(self.ctrl_dff_array)
        
        self.and2 = factory.create(module_type="pand2",
                                   size=12,
                                   height=dff_height)
        self.add_mod(self.and2)

        self.rbl_driver = factory.create(module_type="pbuf",
                                         size=self.num_cols,
                                         height=dff_height)
        self.add_mod(self.rbl_driver)
        
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
        
        self.add_mod(self.clk_buf_driver)

        # We will use the maximum since this same value is used to size the wl_en
        # and the p_en_bar drivers
        max_fanout = max(self.num_rows, self.num_cols)
        
        # wl_en drives every row in the bank
        self.wl_en_driver = factory.create(module_type="pdriver",
                                           fanout=self.num_rows,
                                           height=dff_height)
        self.add_mod(self.wl_en_driver)

        # w_en drives every write driver
        self.wen_and = factory.create(module_type="pand3",
                                       size=self.word_size + 8,
                                       height=dff_height)
        self.add_mod(self.wen_and)

        # s_en drives every sense amp
        self.sen_and3 = factory.create(module_type="pand3",
                                       size=self.word_size + self.num_spare_cols,
                                       height=dff_height)
        self.add_mod(self.sen_and3)

        # used to generate inverted signals with low fanout
        self.inv = factory.create(module_type="pinv",
                                  size=1,
                                  height=dff_height)
        self.add_mod(self.inv)
        
        # p_en_bar drives every column in the bitcell array
        # but it is sized the same as the wl_en driver with
        # prepended 3 inverter stages to guarantee it is slower and odd polarity
        self.p_en_bar_driver = factory.create(module_type="pdriver",
                                              fanout=self.num_cols,
                                              height=dff_height)
        self.add_mod(self.p_en_bar_driver)

        self.nand2 = factory.create(module_type="pnand2",
                                    height=dff_height)
        self.add_mod(self.nand2)
        
        # if (self.port_type == "rw") or (self.port_type == "r"):
        #     from importlib import reload
        #     self.delay_chain_resized = False
        #     c = reload(__import__(OPTS.replica_bitline))
        #     replica_bitline = getattr(c, OPTS.replica_bitline)
        #     bitcell_loads = int(math.ceil(self.num_rows * OPTS.rbl_delay_percentage))
        #     #Use a model to determine the delays with that heuristic
        #     if OPTS.use_tech_delay_chain_size: #Use tech parameters if set.
        #         fanout_list = OPTS.delay_chain_stages*[OPTS.delay_chain_fanout_per_stage]
        #         debug.info(1, "Using tech parameters to size delay chain: fanout_list={}".format(fanout_list))
        #         self.replica_bitline = factory.create(module_type="replica_bitline",
        #                                               delay_fanout_list=fanout_list,
        #                                               bitcell_loads=bitcell_loads)
        #         if self.sram != None: #Calculate model value even for specified sizes
        #             self.set_sen_wl_delays()
                
        #     else: #Otherwise, use a heuristic and/or model based sizing.
        #         #First use a heuristic
        #         delay_stages_heuristic, delay_fanout_heuristic = self.get_heuristic_delay_chain_size()
        #         self.replica_bitline = factory.create(module_type="replica_bitline",
        #                                               delay_fanout_list=[delay_fanout_heuristic]*delay_stages_heuristic,
        #                                               bitcell_loads=bitcell_loads)
        #         #Resize if necessary, condition depends on resizing method
        #         if self.sram != None and self.enable_delay_chain_resizing and not self.does_sen_rise_fall_timing_match():
        #             #This resizes to match fall and rise delays, can make the delay chain weird sizes.
        #             stage_list = self.get_dynamic_delay_fanout_list(delay_stages_heuristic, delay_fanout_heuristic)
        #             self.replica_bitline = factory.create(module_type="replica_bitline",
        #                                                   delay_fanout_list=stage_list,
        #                                                   bitcell_loads=bitcell_loads)
                    
        #             #This resizes based on total delay.
        #             # delay_stages, delay_fanout = self.get_dynamic_delay_chain_size(delay_stages_heuristic, delay_fanout_heuristic)
        #             # self.replica_bitline = factory.create(module_type="replica_bitline",
        #                                                   # delay_fanout_list=[delay_fanout]*delay_stages,
        #                                                   # bitcell_loads=bitcell_loads)
                    
        #             self.sen_delay_rise,self.sen_delay_fall = self.get_delays_to_sen() #get the new timing
        #             self.delay_chain_resized = True

        debug.check(OPTS.delay_chain_stages % 2,
                    "Must use odd number of delay chain stages for inverting delay chain.")
        self.delay_chain=factory.create(module_type="delay_chain",
                                        fanout_list = OPTS.delay_chain_stages * [ OPTS.delay_chain_fanout_per_stage ])
        self.add_mod(self.delay_chain)

    def get_heuristic_delay_chain_size(self):
        """Use a basic heuristic to determine the size of the delay chain used for the Sense Amp Enable """
        # FIXME: The minimum was 2 fanout, now it will not pass DRC unless it is 3. Why?
        delay_fanout = 3 # This can be anything >=3
        # Model poorly captures delay of the column mux. Be pessismistic for column mux
        if self.words_per_row >= 2:
            delay_stages = 8
        else:
            delay_stages = 2
        
        # Read ports have a shorter s_en delay. The model is not accurate enough to catch this difference
        # on certain sram configs.
        if self.port_type == "r":
            delay_stages+=2
        
        return (delay_stages, delay_fanout)
        
    def set_sen_wl_delays(self):
        """Set delays for wordline and sense amp enable"""
        self.wl_delay_rise, self.wl_delay_fall = self.get_delays_to_wl()
        self.sen_delay_rise, self.sen_delay_fall = self.get_delays_to_sen()
        self.wl_delay = self.wl_delay_rise + self.wl_delay_fall
        self.sen_delay = self.sen_delay_rise + self.sen_delay_fall
        
    def does_sen_rise_fall_timing_match(self):
        """Compare the relative rise/fall delays of the sense amp enable and wordline"""
        self.set_sen_wl_delays()
        # This is not necessarily more reliable than total delay in some cases.
        if (self.wl_delay_rise * self.wl_timing_tolerance >= self.sen_delay_rise or
            self.wl_delay_fall * self.wl_timing_tolerance >= self.sen_delay_fall):
            return False
        else:
            return True
    
    def does_sen_total_timing_match(self):
        """Compare the total delays of the sense amp enable and wordline"""
        self.set_sen_wl_delays()
        # The sen delay must always be bigger than than the wl
        # delay. This decides how much larger the sen delay must be
        # before a re-size is warranted.
        if self.wl_delay * self.wl_timing_tolerance >= self.sen_delay:
            return False
        else:
            return True
          
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
    
    def calculate_stage_list(self, total_stages, fanout_rise, fanout_fall):
        """
        Produces a list of fanouts which determine the size of the delay chain.
        List length is the number of stages.
        Assumes the first stage is falling.
        """
        stage_list = []
        for i in range(total_stages):
            if i % 2 == 0:
                stage_list.append()
                
    def setup_signal_busses(self):
        """ Setup bus names, determine the size of the busses etc """

        # List of input control signals
        if self.port_type == "rw":
            self.input_list = ["csb", "web"]
            self.rbl_list = ["rbl_bl"]
        else:
            self.input_list = ["csb"]
            self.rbl_list = ["rbl_bl"]

        if self.port_type == "rw":
            self.dff_output_list = ["cs_bar", "cs", "we_bar", "we"]
        else:
            self.dff_output_list = ["cs_bar", "cs"]
        
        # list of output control signals (for making a vertical bus)
        if self.port_type == "rw":
            self.internal_bus_list = ["rbl_bl_delay_bar", "rbl_bl_delay", "gated_clk_bar", "gated_clk_buf", "we", "we_bar", "clk_buf", "cs"]
        elif self.port_type == "r":
            self.internal_bus_list = ["rbl_bl_delay_bar", "rbl_bl_delay", "gated_clk_bar", "gated_clk_buf", "clk_buf", "cs_bar", "cs"]
        else:
            self.internal_bus_list = ["rbl_bl_delay_bar", "rbl_bl_delay", "gated_clk_bar", "gated_clk_buf", "clk_buf", "cs"]
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

    def route_rails(self):
        """ Add the input signal inverted tracks """
        height = self.control_logic_center.y - self.m2_pitch
        offset = vector(self.ctrl_dff_array.width, 0)
        
        self.input_bus = self.create_vertical_bus("m2",
                                                  offset,
                                                  self.internal_bus_list,
                                                  height)

    def create_instances(self):
        """ Create all the instances """
        self.create_dffs()
        self.create_clk_buf_row()
        self.create_gated_clk_bar_row()
        self.create_gated_clk_buf_row()
        self.create_wlen_row()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.create_rbl_delay_row()
            self.create_wen_row()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.create_sen_row()
        self.create_delay()
        self.create_pen_row()

    def place_instances(self):
        """ Place all the instances """
        # Keep track of all right-most instances to determine row boundary
        # and add the vdd/gnd pins
        self.row_end_inst = []

        # Add the control flops on the left of the bus
        self.place_dffs()

        # All of the control logic is placed to the right of the DFFs and bus
        self.control_x_offset = self.ctrl_dff_array.width + self.internal_bus_width
        
        row = 0
        # Add the logic on the right of the bus
        self.place_clk_buf_row(row)
        row += 1
        self.place_gated_clk_bar_row(row)
        row += 1
        self.place_gated_clk_buf_row(row)
        row += 1
        self.place_wlen_row(row)
        row += 1
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.place_wen_row(row)
            height = self.w_en_gate_inst.uy()
            control_center_y = self.w_en_gate_inst.uy()
            row += 1
        self.place_pen_row(row)
        row += 1
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.place_rbl_delay_row(row)
            row += 1
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.place_sen_row(row)
            row += 1
        self.place_delay(row)
        height = self.delay_inst.uy()
        control_center_y = self.delay_inst.by()

        # This offset is used for placement of the control logic in the SRAM level.
        self.control_logic_center = vector(self.ctrl_dff_inst.rx(), control_center_y)

        # Extra pitch on top and right
        self.height = height + 2 * self.m1_pitch
        # Max of modules or logic rows
        self.width = max([inst.rx() for inst in self.row_end_inst])
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.width = max(self.delay_inst.rx(), self.width)
        self.width += self.m2_pitch

    def route_all(self):
        """ Routing between modules """
        self.route_rails()
        self.route_dffs()
        self.route_wlen()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.route_rbl_delay()
            self.route_wen()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.route_sen()
        self.route_delay()
        self.route_pen()
        self.route_clk_buf()
        self.route_gated_clk_bar()
        self.route_gated_clk_buf()
        self.route_supply()

    def create_delay(self):
        """ Create the replica bitline """
        self.delay_inst=self.add_inst(name="delay_chain",
                                      mod=self.delay_chain)
        # rbl_bl_delay is asserted (1) when the bitline has been discharged
        self.connect_inst(["rbl_bl", "rbl_bl_delay", "vdd", "gnd"])

    def place_delay(self, row):
        """ Place the replica bitline """
        y_off = row * self.and2.height + 2 * self.m1_pitch

        # Add the RBL above the rows
        # Add to the right of the control rows and routing channel
        offset = vector(self.delay_chain.width, y_off)
        self.delay_inst.place(offset, mirror="MY")
        
    def route_delay(self):

        out_pos = self.delay_inst.get_pin("out").bc()
        # Connect to the rail level with the vdd rail
        # Use pen since it is in every type of control logic
        vdd_ypos = self.p_en_bar_nand_inst.get_pin("vdd").by()
        in_pos = vector(self.input_bus["rbl_bl_delay"].cx(), vdd_ypos)
        mid1 = vector(out_pos.x, in_pos.y)
        self.add_wire(self.m1_stack, [out_pos, mid1, in_pos])
        self.add_via_center(layers=self.m1_stack,
                            offset=in_pos)
        
        # Input from RBL goes to the delay line for futher delay
        self.copy_layout_pin(self.delay_inst, "in", "rbl_bl")
        
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
        
    def create_wlen_row(self):
        # input pre_p_en, output: wl_en
        self.wl_en_inst=self.add_inst(name="buf_wl_en",
                                      mod=self.wl_en_driver)
        self.connect_inst(["gated_clk_bar", "wl_en", "vdd", "gnd"])

    def place_wlen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.wl_en_inst, x_offset, row)

        self.row_end_inst.append(self.wl_en_inst)

    def route_wlen(self):
        wlen_map = zip(["A"], ["gated_clk_bar"])
        self.connect_vertical_bus(wlen_map, self.wl_en_inst, self.input_bus)
        
        self.connect_output(self.wl_en_inst, "Z", "wl_en")

    def create_pen_row(self):
        self.p_en_bar_nand_inst=self.add_inst(name="nand_p_en_bar",
                                              mod=self.nand2)
        # We use the rbl_bl_delay here to ensure that the p_en is only asserted when the
        # bitlines have already been discharged. Otherwise, it is a combination loop.
        self.connect_inst(["gated_clk_buf", "rbl_bl_delay", "p_en_bar_unbuf", "vdd", "gnd"])

        self.p_en_bar_driver_inst=self.add_inst(name="buf_p_en_bar",
                                                mod=self.p_en_bar_driver)
        self.connect_inst(["p_en_bar_unbuf", "p_en_bar", "vdd", "gnd"])
        
    def place_pen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.p_en_bar_nand_inst, x_offset, row)
        x_offset = self.place_util(self.p_en_bar_driver_inst, x_offset, row)

        self.row_end_inst.append(self.p_en_bar_driver_inst)

    def route_pen(self):
        in_map = zip(["A", "B"], ["gated_clk_buf", "rbl_bl_delay"])
        self.connect_vertical_bus(in_map, self.p_en_bar_nand_inst, self.input_bus)

        out_pin = self.p_en_bar_nand_inst.get_pin("Z")
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
        """ Create the sense enable buffer. """
        if self.port_type=="rw":
            input_name = "we_bar"
        else:
            input_name = "cs"
        # GATE FOR S_EN
        self.s_en_gate_inst = self.add_inst(name="buf_s_en_and",
                                            mod=self.sen_and3)
        # s_en is asserted in the second half of the cycle during a read.
        # we also must wait until the bitline has been discharged enough for proper sensing
        # hence we use rbl_bl_delay as well.
        self.connect_inst(["rbl_bl_delay", "gated_clk_bar", input_name, "s_en", "vdd", "gnd"])
        
    def place_sen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.s_en_gate_inst, x_offset, row)
        
        self.row_end_inst.append(self.s_en_gate_inst)
        
    def route_sen(self):

        if self.port_type=="rw":
            input_name = "we_bar"
        else:
            input_name = "cs"
            
        sen_map = zip(["A", "B", "C"], ["rbl_bl_delay", "gated_clk_bar", input_name])
        self.connect_vertical_bus(sen_map, self.s_en_gate_inst, self.input_bus)
        
        self.connect_output(self.s_en_gate_inst, "Z", "s_en")

    def create_rbl_delay_row(self):

        self.rbl_bl_delay_inv_inst = self.add_inst(name="rbl_bl_delay_inv",
                                                   mod=self.inv)
        self.connect_inst(["rbl_bl_delay", "rbl_bl_delay_bar", "vdd", "gnd"])

    def place_rbl_delay_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.rbl_bl_delay_inv_inst, x_offset, row)
        
        self.row_end_inst.append(self.rbl_bl_delay_inv_inst)
        
    def route_rbl_delay(self):
        # Connect from delay line
        # Connect to rail

        self.route_output_to_bus_jogged(self.rbl_bl_delay_inv_inst, "rbl_bl_delay_bar")
        
        rbl_map = zip(["A"], ["rbl_bl_delay"])
        self.connect_vertical_bus(rbl_map, self.rbl_bl_delay_inv_inst, self.input_bus)

    def create_wen_row(self):

        # input: we (or cs) output: w_en
        if self.port_type == "rw":
            input_name = "we"
        else:
            # No we for write-only reports, so use cs
            input_name = "cs"

        # GATE THE W_EN
        self.w_en_gate_inst = self.add_inst(name="w_en_and",
                                            mod=self.wen_and)
        # Only drive the writes in the second half of the clock cycle during a write operation.
        self.connect_inst([input_name, "rbl_bl_delay_bar", "gated_clk_bar", "w_en", "vdd", "gnd"])
        
    def place_wen_row(self, row):
        x_offset = self.control_x_offset

        x_offset = self.place_util(self.w_en_gate_inst, x_offset, row)
        
        self.row_end_inst.append(self.w_en_gate_inst)
        
    def route_wen(self):
        if self.port_type == "rw":
            input_name = "we"
        else:
            # No we for write-only reports, so use cs
            input_name = "cs"
            
        wen_map = zip(["A", "B", "C"], [input_name, "rbl_bl_delay_bar", "gated_clk_bar"])
        self.connect_vertical_bus(wen_map, self.w_en_gate_inst, self.input_bus)

        self.connect_output(self.w_en_gate_inst, "Z", "w_en")
        
    def create_dffs(self):
        self.ctrl_dff_inst=self.add_inst(name="ctrl_dffs",
                                         mod=self.ctrl_dff_array)
        inst_pins = self.input_list + self.dff_output_list + ["clk_buf"] + self.supply_list
        if props.dff_buff_array.add_body_contacts:
            inst_pins.append("vpb")
            inst_pins.append("vnb")
        self.connect_inst(inst_pins)

    def place_dffs(self):
        self.ctrl_dff_inst.place(vector(0, 0))
        
    def route_dffs(self):
        if self.port_type == "rw":
            dff_out_map = zip(["dout_bar_0", "dout_bar_1", "dout_1"], ["cs", "we", "we_bar"])
        elif self.port_type == "r":
            dff_out_map = zip(["dout_bar_0", "dout_0"], ["cs", "cs_bar"])
        else:
            dff_out_map = zip(["dout_bar_0"], ["cs"])
        self.connect_vertical_bus(dff_out_map, self.ctrl_dff_inst, self.input_bus, self.m2_stack[::-1])
        
        # Connect the clock rail to the other clock rail
        # by routing in the supply rail track to avoid channel conflicts
        in_pos = self.ctrl_dff_inst.get_pin("clk").uc()
        mid_pos = in_pos + vector(0, self.and2.height)
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

    def route_supply(self):
        """ Add vdd and gnd to the instance cells """

        if OPTS.tech_name == "sky130":
            supply_layer = "li"
        else:
            supply_layer = "m1"
        max_row_x_loc = max([inst.rx() for inst in self.row_end_inst])
        for inst in self.row_end_inst:
            pins = inst.get_pins("vdd")
            for pin in pins:
                if pin.layer == supply_layer:
                    row_loc = pin.rc()
                    pin_loc = vector(max_row_x_loc, pin.rc().y)
                    self.add_power_pin("vdd", pin_loc, start_layer=pin.layer)
                    self.add_path(supply_layer, [row_loc, pin_loc])

            pins = inst.get_pins("gnd")
            for pin in pins:
                if pin.layer == supply_layer:
                    row_loc = pin.rc()
                    pin_loc = vector(max_row_x_loc, pin.rc().y)
                    self.add_power_pin("gnd", pin_loc, start_layer=pin.layer)
                    self.add_path(supply_layer, [row_loc, pin_loc])
            
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

    def get_delays_to_wl(self):
        """Get the delay (in delay units) of the clk to a wordline in the bitcell array"""
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        self.wl_stage_efforts = self.get_wordline_stage_efforts()
        clk_to_wl_rise, clk_to_wl_fall = logical_effort.calculate_relative_rise_fall_delays(self.wl_stage_efforts)
        total_delay = clk_to_wl_rise + clk_to_wl_fall
        debug.info(1,
                   "Clock to wl delay is rise={:.3f}, fall={:.3f}, total={:.3f} in delay units".format(clk_to_wl_rise,
                                                                                                       clk_to_wl_fall,
                                                                                                       total_delay))
        return clk_to_wl_rise, clk_to_wl_fall
     
    def get_wordline_stage_efforts(self):
        """Follows the gated_clk_bar -> wl_en -> wordline signal for the total path efforts"""
        stage_effort_list = []
        
        # Initial direction of gated_clk_bar signal for this path
        is_clk_bar_rise = True
        
        # Calculate the load on wl_en within the module and add it to external load
        external_cout = self.sram.get_wl_en_cin()
        # First stage is the clock buffer
        stage_effort_list += self.clk_buf_driver.get_stage_efforts(external_cout, is_clk_bar_rise)
        last_stage_is_rise = stage_effort_list[-1].is_rise
        
        # Then ask the sram for the other path delays (from the bank)
        stage_effort_list += self.sram.get_wordline_stage_efforts(last_stage_is_rise)
        
        return stage_effort_list
        
    def get_delays_to_sen(self):
        """
        Get the delay (in delay units) of the clk to a sense amp enable.
        This does not incorporate the delay of the replica bitline.
        """
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        self.sen_stage_efforts = self.get_sa_enable_stage_efforts()
        clk_to_sen_rise, clk_to_sen_fall = logical_effort.calculate_relative_rise_fall_delays(self.sen_stage_efforts)
        total_delay = clk_to_sen_rise + clk_to_sen_fall
        debug.info(1,
                   "Clock to s_en delay is rise={:.3f}, fall={:.3f}, total={:.3f} in delay units".format(clk_to_sen_rise,
                                                                                                         clk_to_sen_fall,
                                                                                                         total_delay))
        return clk_to_sen_rise, clk_to_sen_fall
          
    def get_sa_enable_stage_efforts(self):
        """Follows the gated_clk_bar signal to the sense amp enable signal adding each stages stage effort to a list"""
        stage_effort_list = []
        
        # Initial direction of clock signal for this path
        last_stage_rise = True
        
        # First stage, gated_clk_bar -(and2)-> rbl_in. Only for RW ports.
        if self.port_type == "rw":
            stage1_cout = self.replica_bitline.get_en_cin()
            stage_effort_list += self.and2.get_stage_efforts(stage1_cout, last_stage_rise)
            last_stage_rise = stage_effort_list[-1].is_rise
        
        # Replica bitline stage, rbl_in -(rbl)-> pre_s_en
        stage2_cout = self.sen_and2.get_cin()
        stage_effort_list += self.replica_bitline.determine_sen_stage_efforts(stage2_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        # buffer stage, pre_s_en -(buffer)-> s_en
        stage3_cout = self.sram.get_sen_cin()
        stage_effort_list += self.s_en_driver.get_stage_efforts(stage3_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        return stage_effort_list

    def get_wl_sen_delays(self):
        """ Gets a list of the stages and delays in order of their path. """

        if self.sen_stage_efforts == None or self.wl_stage_efforts == None:
            debug.error("Model delays not calculated for SRAM.", 1)
        wl_delays = logical_effort.calculate_delays(self.wl_stage_efforts)
        sen_delays = logical_effort.calculate_delays(self.sen_stage_efforts)
        return wl_delays, sen_delays
        
    def analytical_delay(self, corner, slew, load):
        """ Gets the analytical delay from clk input to wl_en output """

        stage_effort_list = []
        # Calculate the load on clk_buf_bar
        # ext_clk_buf_cout = self.sram.get_clk_bar_cin()
        
        # Operations logic starts on negative edge
        last_stage_rise = False
        
        # First stage(s), clk -(pdriver)-> clk_buf.
        # clk_buf_cout = self.replica_bitline.get_en_cin()
        clk_buf_cout = 0
        stage_effort_list += self.clk_buf_driver.get_stage_efforts(clk_buf_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        # Second stage, clk_buf -(inv)-> clk_bar
        clk_bar_cout = self.and2.get_cin()
        stage_effort_list += self.and2.get_stage_efforts(clk_bar_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        # Third stage clk_bar -(and)-> gated_clk_bar
        gated_clk_bar_cin = self.get_gated_clk_bar_cin()
        stage_effort_list.append(self.inv.get_stage_effort(gated_clk_bar_cin, last_stage_rise))
        last_stage_rise = stage_effort_list[-1].is_rise

        # Stages from gated_clk_bar -------> wordline
        stage_effort_list += self.get_wordline_stage_efforts()
        return stage_effort_list
       
    def get_clk_buf_cin(self):
        """
        Get the loads that are connected to the buffered clock.
        Includes all the DFFs and some logic.
        """
       
        # Control logic internal load
        int_clk_buf_cap = self.inv.get_cin() + self.ctrl_dff_array.get_clk_cin() + self.and2.get_cin()

        # Control logic external load (in the other parts of the SRAM)
        ext_clk_buf_cap = self.sram.get_clk_bar_cin()
       
        return int_clk_buf_cap + ext_clk_buf_cap
        
    def get_gated_clk_bar_cin(self):
        """Get intermediates net gated_clk_bar's capacitance"""
        
        total_cin = 0
        total_cin += self.wl_en_driver.get_cin()
        if self.port_type == 'rw':
            total_cin += self.and2.get_cin()
        return total_cin
        
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
        mid1 = vector(out_pos.x, out_pos.y - 0.4 * inst.mod.height)
        mid2 = vector(self.input_bus[name].cx(), mid1.y)
        bus_pos = self.input_bus[name].center()
        self.add_wire(self.m2_stack[::-1], [out_pos, mid1, mid2, bus_pos])
        self.add_via_stack_center(from_layer=out_pin.layer,
                                  to_layer="m2",
                                  offset=out_pos)
    
