import sys
from tech import drc, parameter
import debug
import design
import math
from math import log,sqrt,ceil
from contact import contact
from pinv import pinv
from nand_2 import nand_2
from nor_2 import nor_2
from vector import vector
from globals import OPTS

class bank(design.design):
    """
    Dynamically generated a single Bank including bitcell array,
    hierarchical_decoder, precharge, column_mux, write driver and sense amplifiers.
    """

    def __init__(self, word_size, num_words, words_per_row, num_banks=1, name=""):

        mod_list = ["tri_gate", "bitcell", "decoder", "ms_flop_array", "wordline_driver",
                    "bitcell_array",   "sense_amp_array",    "precharge_array",
                    "column_mux_array","write_driver_array", "tri_gate_array"]
        for mod_name in mod_list:
            config_mod_name = getattr(OPTS.config, mod_name)
            class_file = reload(__import__(config_mod_name))
            mod_class = getattr(class_file , config_mod_name)
            setattr (self, "mod_"+mod_name, mod_class)

        self.bitcell_height = self.mod_bitcell.chars["height"]
        self.tri_gate_chars = self.mod_tri_gate.chars

        if name == "":
            self.name = "bank_{0}_{1}".format(word_size, num_words)
        else:
            self.name = name
        design.design.__init__(self, self.name)
        debug.info(2, "create sram of size {0} with {1} num of words".format(word_size,num_words))

        self.word_size = word_size
        self.num_words = num_words
        self.words_per_row = words_per_row
        self.num_banks = num_banks

        self.compute_sizes()
        self.add_pins()
        self.create_modules()
        self.add_modules()
        self.setup_layout_constraints()

        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for Bank module"""
        for i in range(self.word_size):
            self.add_pin("DATA[{0}]".format(i))
        for i in range(self.addr_size):
            self.add_pin("ADDR[{0}]".format(i))

        if(self.num_banks > 1):
            self.add_pin("bank_select")
            self.add_pin("gated_s_en")
            self.add_pin("gated_w_en")
            self.add_pin("gated_tri_en_bar")
            self.add_pin("gated_tri_en")
            self.add_pin("gated_clk_bar")
            self.add_pin("gated_clk")
        else:
            self.add_pin("s_en")
            self.add_pin("w_en")
            self.add_pin("tri_en_bar")
            self.add_pin("tri_en")
            self.add_pin("clk_bar")
            self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        """ Create routing amoung the modules """
        self.create_central_bus()
        self.route_pre_charge_to_bitcell_array()
        self.route_between_sense_amp_and_tri_gate()
        self.route_tri_gate_out()

        self.route_between_wordline_driver_and_bitcell_array()
        self.route_column_address_lines()
        self.route_msf_address_to_row_decoder()
        self.route_control_lines()
        if(self.num_banks > 1):
            self.route_bank_select_or2_gates()
        self.route_power_rail_vdd()
        self.route_power_rail_gnd()

        self.offset_all_coordinates()

    def add_modules(self):
        """ Add modules. The order should be maintained."""
        self.add_bitcell_array()
        self.add_precharge_array()
        self.add_column_mux_array()
        self.add_sense_amp_array()
        self.add_write_driver_array()
        self.add_msf_data_in()
        self.add_tri_gate_array()
        self.add_hierarchical_decoder()
        self.add_wordline_driver()
        self.add_msf_address()
        self.add_column_line_decoder()
        self.add_bank_select_or2_gates()

    def compute_sizes(self):
        """  Computes the required sizes to create the bank """

        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words / self.words_per_row

        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.addr_size = self.col_addr_size + self.row_addr_size

        assert self.num_rows*self.num_cols, self.word_size*self.num_words
        assert self.addr_size, self.col_addr_size + self.row_addr_size

        self.power_rail_width = 10*drc["minwidth_metal1"]

        # Width for left gnd rail
        self.power_rail_width = 10*drc["minwidth_metal2"]
        self.left_gnd_rail_gap = 4*drc["minwidth_metal2"]

        # Number of control lines in the bus
        self.number_of_control_lines = 6

        self.num_central_bus = (2 * self.col_addr_size + self.row_addr_size 
                                    + self.number_of_control_lines)

        # bus gap is choosen 2 times the minimum width to eliminate drc between
        # contact on one bus and the adjacent bus
        self.width_central_bus = drc["minwidth_metal2"]
        self.gap_central_bus = 2*drc["metal2_to_metal2"]

        # Overall central bus gap. It includes all the column mux lines, 6
        # control lines, address flop to decoder lines and a GND power rail in M2
        central_bus_gap = ((self.gap_central_bus + self.width_central_bus)
                               *(self.num_central_bus + 2))
        self.overall_central_bus_gap = (central_bus_gap + self.power_rail_width 
                                        + self.left_gnd_rail_gap)

        self.start_of_right_central_bus = self.gap_central_bus
        control_gap = ((self.gap_central_bus + self.width_central_bus)
                             * self.number_of_control_lines)
        self.start_of_left_central_bus = (control_gap + self.power_rail_width
                                              + self.left_gnd_rail_gap 
                                              + self.start_of_right_central_bus)


        # Array for control lines
        self.control_bus = []
        self.control_signals = ["s_en", "w_en",
                                "clk_bar",
                                "tri_en", "tri_en_bar",
                                "clk"]
        self.gated_control_signals = ["gated_s_en", "gated_w_en",
                                      "gated_clk_bar",
                                      "gated_tri_en", "gated_tri_en_bar",
                                      "gated_clk"]

        # Array for bank address positions
        self.address_positions = []

        # Array for bank data positions
        self.data_positions = []

    def create_modules(self):
        """ Create all the modules using the class loader """
        self.bitcell_array = self.mod_bitcell_array(name="bitcell_array", 
                                              cols=self.num_cols,
                                              rows=self.num_rows)
        self.add_mod(self.bitcell_array)

        self.precharge_array = self.mod_precharge_array(name="precharge_array", 
                                                        columns=self.num_cols,
                                                        ptx_width=drc["minwidth_tx"])
        self.add_mod(self.precharge_array)

        if(self.col_addr_size > 0):
            self.column_mux_array = self.mod_column_mux_array(rows=self.num_rows,
                                                              columns=self.num_cols, 
                                                              word_size=self.word_size)
            self.add_mod(self.column_mux_array)


        self.sens_amp_array = self.mod_sense_amp_array(word_size=self.word_size, 
                                                       words_per_row=self.words_per_row)
        self.add_mod(self.sens_amp_array)

        self.write_driver_array = self.mod_write_driver_array(columns=self.num_cols,
                                                              word_size=self.word_size)
        self.add_mod(self.write_driver_array)

        self.decoder = self.mod_decoder(nand2_nmos_width=2*drc["minwidth_tx"],
                                        nand3_nmos_width=3*drc["minwidth_tx"], 
                                        rows=self.num_rows)
        self.add_mod(self.decoder)

        self.msf_address = self.mod_ms_flop_array(name="msf_address", 
                                                  array_type="address", 
                                                  columns=self.row_addr_size+self.col_addr_size, 
                                                  word_size=self.row_addr_size+self.col_addr_size)
        self.add_mod(self.msf_address)
        
        self.msf_data_in = self.mod_ms_flop_array(name="msf_data_in", 
                                                  array_type="data_in", 
                                                  columns=self.num_cols, 
                                                  word_size=self.word_size)
        self.add_mod(self.msf_data_in)
        
        self.msf_data_out = self.mod_ms_flop_array(name="msf_data_out", 
                                                   array_type="data_out", 
                                                   columns=self.num_cols, 
                                                   word_size=self.word_size)
        self.add_mod(self.msf_data_out)

        self.tri_gate_array = self.mod_tri_gate_array(columns=self.num_cols, 
                                                      word_size=self.word_size)
        self.add_mod(self.tri_gate_array)

        self.wordline_driver = self.mod_wordline_driver(name="wordline_driver", 
                                                        rows=self.num_rows)
        #self.wordline_driver.logic_effort_sizing(self.num_cols)
        self.add_mod(self.wordline_driver)

        self.inv = pinv(name="pinv",
                        nmos_width=drc["minwidth_tx"], 
                        beta=parameter["pinv_beta"], 
                        height=self.bitcell_height)
        self.add_mod(self.inv)
        
    # 4x Inverter
        self.inv4x = pinv(name="pinv4x",
                          nmos_width=4*drc["minwidth_tx"], 
                          beta=parameter["pinv_beta"], 
                          height=self.bitcell_height)
        self.add_mod(self.inv4x)

        self.NAND2 = nand_2(name="pnand2_x1", 
                            nmos_width=2*drc["minwidth_tx"], 
                            height=self.bitcell_height)
        self.add_mod(self.NAND2)

        self.NOR2 = nor_2(name="pnor2_x1",
                          nmos_width=drc["minwidth_tx"], 
                          height=self.bitcell_height)
        self.add_mod(self.NOR2)

        # These aren't for instantiating, but we use them to get the dimensions
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))

        # Vertical metal rail gap definition
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height 
                                          - self.m1m2_via.contact_width) / 2
        self.gap_between_rails = self.metal2_extend_contact + drc["metal2_to_metal2"]
        self.gap_between_rail_offset = self.gap_between_rails + drc["minwidth_metal2"]
        self.via_shift = (self.m1m2_via.second_layer_width 
                              - self.m1m2_via.first_layer_width) / 2

    def add_bitcell_array(self):
        """ Adding Bitcell Array """

        self.module_offset = vector(0, 0)
        self.bitcell_array_position = self.module_offset
        self.add_inst(name="bitcell_array", 
                      mod=self.bitcell_array,
                      offset=self.module_offset)
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for j in range(self.num_rows):
            temp.append("wl[{0}]".format(j))
        temp = temp + ["vdd", "gnd"]
        self.connect_inst(temp)

    def add_precharge_array(self):
        """ Adding Pre-charge """

        self.gap_between_precharge_and_bitcell = 5 * drc["minwidth_metal2"]

        y_off = self.bitcell_array.height + self.gap_between_precharge_and_bitcell
        self.precharge_array_position = vector(0, y_off)
        self.add_inst(name="precharge_array",
                      mod=self.precharge_array, 
                      offset=self.precharge_array_position)
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        temp = temp + ["clk_bar", "vdd"]
        self.connect_inst(temp)

    def add_column_mux_array(self):
        """ Adding Column Mux when words_per_row > 1 . """

        if(self.col_addr_size != 0):
            self.module_offset = vector(0, -self.column_mux_array.height)
            self.column_mux_array_position = self.module_offset 
            self.add_inst(name="column_mux_array",
                          mod=self.column_mux_array,
                          offset=self.column_mux_array_position)
            temp = []
            for i in range(self.num_cols):
                temp.append("bl[{0}]".format(i))
                temp.append("br[{0}]".format(i))
            for j in range(self.word_size):
                temp.append("bl_out[{0}]".format(
                    j*self.words_per_row))
                temp.append("br_out[{0}]".format(
                    j*self.words_per_row))
            for k in range(self.words_per_row):
                temp.append("sel[{0}]".format(k))
            temp.append("gnd")
            self.connect_inst(temp)

    def add_sense_amp_array(self):
        """ Adding Sense amp  """

        self.module_offset = vector(0, self.module_offset.y - self.sens_amp_array.height)
        self.sens_amp_array_position = self.module_offset 
        self.add_inst(name="sense_amp_array",
                      mod=self.sens_amp_array,
                      offset=self.sens_amp_array_position)
        temp = []
        if (self.words_per_row == 1):
            for j in range(self.word_size):
                temp.append("bl[{0}]".format(j*self.words_per_row))
                temp.append("br[{0}]".format(j*self.words_per_row))
        else:
            for j in range(self.word_size):
                temp.append("bl_out[{0}]".format(j*self.words_per_row))
                temp.append("br_out[{0}]".format(j*self.words_per_row))

        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
        temp = temp + ["s_en", "vdd", "gnd"]
        self.connect_inst(temp)

    def add_write_driver_array(self):
        """ Adding Write Driver  """

        self.module_offset = vector(0, self.module_offset.y - self.write_driver_array.height)
        self.write_driver_array_position = self.module_offset
        self.add_inst(name="write_driver_array", 
                      mod=self.write_driver_array, 
                      offset=self.write_driver_array_position)

        temp = []
        for i in range(self.word_size):
            temp.append("data_in[{0}]".format(i))
        if (self.words_per_row == 1):
            for j in range(self.word_size):
                temp.append("bl[{0}]".format(j*self.words_per_row))
                temp.append("br[{0}]".format(j*self.words_per_row))
        else:
            for j in range(self.word_size):
                temp.append("bl_out[{0}]".format(j*self.words_per_row))
                temp.append("br_out[{0}]".format(j*self.words_per_row))
        temp = temp + ["w_en", "vdd", "gnd"]
        self.connect_inst(temp)

    def add_msf_data_in(self):
        """ data_in flip_flop """

        self.module_offset = vector(0, self.module_offset.y - self.msf_data_in.height)
        self.ms_flop_data_in_offset = self.module_offset 
        self.add_inst(name="data_in_flop_array", 
                      mod=self.msf_data_in, 

                      offset=self.ms_flop_data_in_offset)

        temp = []
        for i in range(self.word_size):
            temp.append("DATA[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("data_in[{0}]".format(i))
            temp.append("data_in_bar[{0}]".format(i))
        temp = temp + ["clk_bar", "vdd", "gnd"]
        self.connect_inst(temp)

    def add_tri_gate_array(self):
        """ data tri gate to drive the data bus """

        self.module_offset = vector(0, self.module_offset.y)
        self.tri_gate_array_offset = self.module_offset 
        self.add_inst(name="trigate_data_array", 
                      mod=self.tri_gate_array, 
                      offset=self.tri_gate_array_offset, 
                      mirror="MX")
        temp = []
        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("DATA[{0}]".format(i))
        temp = temp + ["tri_en", "tri_en_bar", "vdd", "gnd"]
        self.connect_inst(temp)

    def add_hierarchical_decoder(self):
        """  Hierarchical Decoder  """

        """ creating space for address bus before we add Decoder. 
        The bus will be in between decoder and the main Memory array part
        This bus will route decoder input and column mux inputs. 
        For convenient the space is created first so that placement of decoder and address FFs gets easier.
        The wires are actually routed after we placed the stuffs on both side"""

        self.module_offset = vector(self.decoder.width + self.overall_central_bus_gap,
                                    self.decoder.predecoder_height).scale(-1, -1)
        self.decoder_position = self.module_offset 
        self.add_inst(name="address_decoder", 
                      mod=self.decoder, 
                      offset=self.decoder_position)

        temp = []
        for i in range(self.row_addr_size):
            temp.append("A[{0}]".format(i))
        for j in range(self.num_rows):
            temp.append("decode_out[{0}]".format(j))
        temp = temp + ["vdd", "gnd"]
        self.connect_inst(temp)

    def add_wordline_driver(self):
        """ Wordline Driver """

        x_off = self.decoder_position.x + self.decoder.row_decoder_width
        self.module_offset = vector(x_off, 0)
        self.wordline_driver_position = self.module_offset 
        self.add_inst(name="wordline_driver", 
                      mod=self.wordline_driver, 
                      offset=self.wordline_driver_position)

        temp = []
        for i in range(self.num_rows):
            temp.append("decode_out[{0}]".format(i))
        for i in range(self.num_rows):
            temp.append("wl[{0}]".format(i))

        if(self.num_banks > 1):
            temp.append("gated_clk")
        else:
            temp.append("clk")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

    def add_msf_address(self):
        """ Adding address Flip-flops """

        gap = max(drc["pwell_enclose_nwell"],
                  2*drc["minwidth_metal2"])

        self.module_offset = vector(-self.overall_central_bus_gap 
                                        - self.msf_address.height
                                        - 4*drc["minwidth_metal2"], 
                                    self.decoder_position.y - gap 
                                        - drc["minwidth_metal2"])
        self.msf_address_offset = self.module_offset 
        self.add_inst(name="address_flop_array", 
                      mod=self.msf_address, 
                      offset=self.msf_address_offset, 
                      mirror="R270")
        if(self.col_addr_size == 1):
            temp = []
            for i in range(self.row_addr_size):
                temp.append("ADDR[{0}]".format(i))
            temp.append("ADDR[{0}]".format(self.row_addr_size))

            for i in range(self.row_addr_size):
                temp.append("A[{0}]".format(i))
                temp.append("A_bar[{0}]".format(i))
            temp.append("sel[1]")
            temp.append("sel[0]")
            if(self.num_banks > 1):
                temp = temp + ["gated_clk", "vdd", "gnd"]
            else:
                temp = temp + ["clk", "vdd", "gnd"]
            self.connect_inst(temp)
        else:
            temp = []
            for i in range(self.row_addr_size + self.col_addr_size):
                temp.append("ADDR[{0}]".format(i))
            for i in range(self.row_addr_size + self.col_addr_size):
                temp.append("A[{0}]".format(i))
                temp.append("A_bar[{0}]".format(i))
            if(self.num_banks > 1):
                temp = temp + ["gated_clk", "vdd", "gnd"]
            else:
                temp = temp + ["clk", "vdd", "gnd"]
            self.connect_inst(temp)

        # update the min_point
        self.min_point = (self.msf_address_offset.y - self.msf_address.width
                              - 4*drc["minwidth_metal1"])

    def add_column_line_decoder(self):
        """ Create a 2:4 decoder to decode colum select lines if the col_addr_size = 4 """

        if(self.col_addr_size == 2):
            vertical_gap = max(drc["pwell_enclose_nwell"] + drc["minwidth_metal2"],
                               3 * drc["minwidth_metal2"] + 3 * drc["metal2_to_metal2"])
            self.col_decoder = self.decoder.pre2_4
            x_off = (self.gap_central_bus + self.width_central_bus 
                         + self.overall_central_bus_gap 
                         + self.col_decoder.width)
            y_off =(self.msf_address_offset.y - self.msf_address.width 
                        - self.col_decoder.height - vertical_gap)
            self.module_offset = vector(-x_off, y_off)
            self.col_decoder_position = self.module_offset
            self.add_inst(name="col_address_decoder", 
                          mod=self.decoder.pre2_4, 
                          offset=self.col_decoder_position)
            addr_index = self.row_addr_size
            temp = []
            for i in range(2):
                temp.append("A[{0}]".format(i + self.row_addr_size))
            for j in range(4):
                temp.append("sel[{0}]".format(j))
            temp = temp + ["vdd", "gnd"]
            self.connect_inst(temp)

            # update the min_point
            self.min_point = self.col_decoder_position.y

    def add_bank_select_or2_gates(self):
        """ Create an array of and gates to gate the control signals in case 
        of multiple banks are created in upper level SRAM module """
        
        if(self.num_banks > 1):
            # update the min_point
            self.min_point = (self.min_point - 3*drc["minwidth_metal1"]
                                  - self.number_of_control_lines * self.bitcell_height)
            xoffset_nor = (- self.start_of_left_central_bus - self.NOR2.width
                               - self.inv4x.width)
            xoffset_inv = xoffset_nor + self.NOR2.width
            self.bank_select_or_position = vector(xoffset_nor, self.min_point)

            # bank select inverter
            self.bank_select_inv_position = vector(self.bank_select_or_position.x
                                                       - 5 * drc["minwidth_metal2"]
                                                       - self.inv4x.width, 
                                                   self.min_point)
            self.add_inst(name="bank_select_inv", 
                          mod=self.inv4x, 
                          offset=self.bank_select_inv_position)
            self.connect_inst(["bank_select", "bank_select_bar", "vdd", "gnd"])

            for i in range(self.number_of_control_lines):
                # central control bus index
                # 5 = clk,4 = tri_en_bar,3 = tri_en,2 = clk_bar,1 = w_en,0 = s_en
                name_nor = "bank_selector_nor_{0}".format(i)
                name_inv = "bank_selector_inv_{0}".format(i)
                nor2_inv_connection_height = (self.inv4x.A_position.y 
                                                  - self.NOR2.Z_position.y 
                                                  + 0.5 * drc["minwidth_metal1"])

                if (i % 2):
                    y_offset = self.min_point + self.inv.height*(i + 1)
                    mod_dir = "MX"
                    # nor2 output to inv input
                    y_correct = (self.NOR2.Z_position.y + nor2_inv_connection_height
                                     - 0.5 * drc["minwidth_metal1"])
                else:
                    y_offset = self.min_point + self.inv.height*i
                    mod_dir = "R0"
                    # nor2 output to inv input
                    y_correct = 0.5 * drc["minwidth_metal1"] - self.NOR2.Z_position.y
                connection = vector(xoffset_inv, y_offset - y_correct)

                if i == 3:
                    self.add_inst(name=name_nor, 
                                  mod=self.NOR2, 
                                  offset=[xoffset_nor, y_offset], 
                                  mirror=mod_dir)
                    self.connect_inst(["gated_tri_en_bar",
                                       "bank_select_bar", 
                                       self.control_signals[i].format(i),
                                       "vdd",
                                       "gnd"])
                    # connect the metal1 layer to connect to the old inv output
                    offset = connection - vector(0, 0.5*drc["minwidth_metal1"])
                    self.add_rect(layer="metal1", 
                                  offset=offset, 
                                  width=self.inv4x.width, 
                                  height=drc["minwidth_metal1"])
                elif i == 5:
                    offset = [xoffset_nor, y_offset - self.NOR2.A_position.y 
                                  - 0.5*drc["minwidth_metal1"]]
                    self.add_rect(layer="metal1", 
                                  offset=offset, 
                                  width=self.NOR2.width + self.inv4x.width, 
                                  height=drc["minwidth_metal1"])
                else:
                    self.add_inst(name=name_nor, 
                                  mod=self.NOR2, 
                                  offset=[xoffset_nor, y_offset], 
                                  mirror=mod_dir)
                    self.connect_inst([self.gated_control_signals[i], 
                                       "bank_select_bar", 
                                       "net_block_nor_inv[{0}]".format(i),
                                       "vdd",
                                       "gnd"])

                    self.add_inst(name=name_inv, 
                                  mod=self.inv4x, 
                                  offset=[xoffset_inv, y_offset], 
                                  mirror=mod_dir)
                    self.connect_inst(["net_block_nor_inv[{0}]".format(i), 
                                       self.control_signals[i],
                                       "vdd",
                                       "gnd"])

            # nor2 output to inv input
            for i in range(self.number_of_control_lines -1) :
                nor2_inv_connection_height = (self.inv4x.A_position.y 
                                                  - self.NOR2.Z_position.y 
                                                  + 0.5 * drc["minwidth_metal1"])
                
                if (i % 2):
                    y_offset = self.min_point + self.inv.height * (i + 1)
                    mod_dir = "MX"
                    y_correct = (-self.NOR2.Z_position.y + 0.5 * drc["minwidth_metal1"] 
                                      - nor2_inv_connection_height)
                else:
                    y_offset = self.min_point + self.inv.height*i
                    mod_dir = "R0"
                    y_correct = self.NOR2.Z_position.y - 0.5 * drc["minwidth_metal1"]
                # nor2 output to inv input
                connection = vector(xoffset_inv, y_offset + y_correct)
                self.add_rect(layer="metal1", 
                              offset=connection, 
                              width=drc["minwidth_metal1"], 
                              height=nor2_inv_connection_height)

    def setup_layout_constraints(self):
        """ Calculating layout constraints, width, hwight etc """

        tri_gate_min_point = (self.tri_gate_array_offset.y - 6 * drc["minwidth_metal3"]
                                  - self.tri_gate_array.height) 

        self.min_point = min(tri_gate_min_point, self.min_point)
        self.max_point = self.precharge_array_position.y + self.precharge_array.height

        # VDD constraints
        gap_between_bitcell_array_and_vdd = 3 * drc["minwidth_metal1"]
        self.right_vdd_x_offset = self.bitcell_array.width + gap_between_bitcell_array_and_vdd
        self.right_vdd_position = vector(self.right_vdd_x_offset, self.min_point)
        self.add_layout_pin(text="vdd",
                            layer="metal1", 
                            offset=[self.right_vdd_x_offset, self.min_point], 
                            width=self.power_rail_width,
                            height=self.max_point - self.min_point)
        # the width of the metal rail is 10 times minwidth metal1 and the gap
        # from the edge of the decoder is another 2 times minwidth metal1

        self.left_vdd_x_offset = (- 14 * drc["minwidth_metal1"]
                                      + min(self.msf_address_offset.x, 
                                            self.decoder_position.x))
        self.left_vdd_position = vector(self.left_vdd_x_offset, self.min_point)
        self.add_layout_pin(text="vdd",
                            layer="metal1", 
                            offset=[self.left_vdd_x_offset, self.min_point], 
                            width=self.power_rail_width,
                            height=self.max_point - self.min_point)

        self.left_gnd_x_offset = (self.left_gnd_rail_gap / 2
                                      - self.start_of_left_central_bus)
        self.left_gnd_position = vector(self.left_gnd_x_offset, self.min_point)
        self.add_layout_pin(text="gnd",
                            layer="metal2", 
                            offset=self.left_gnd_position , 
                            width=self.power_rail_width,
                            height=self.max_point - self.min_point)

        # Height and Width of the entire bank
        self.height = self.max_point - self.min_point
        self.width = (self.right_vdd_x_offset - self.left_vdd_x_offset
                          + self.power_rail_width)

    def create_central_bus(self):
        """ Calculating the offset for placing VDD and GND power rails. 
        Here we determine the lowest point in the layout """
            
        """ central Control lines central line connection 2*col_addr_size 
         number of connections for the column mux and row_addr_size number 
         of connections for the row address""" 

        self.central_line_xoffset = []
        msf_to_central_line = (self.row_addr_size * self.msf_address.width 
                                   / (self.row_addr_size + self.col_addr_size))
        self.central_line_y_offset = self.msf_address_offset.y - msf_to_central_line
        self.central_line_height = self.max_point - self.min_point

        # Creating the central bus
        # Control lines
        for i in range(self.number_of_control_lines):
            x_offset = (i + 1) * (self.gap_central_bus + self.width_central_bus)
            x_offset = -x_offset - self.start_of_right_central_bus
            self.central_line_xoffset.append(x_offset)
            self.control_bus.append(x_offset)
            self.add_rect(layer="metal2",  
                          offset=[x_offset, self.min_point], 
                          width=self.width_central_bus, 
                          height=self.central_line_height)

        # column mux lines if there is column mux [2 or 4 lines]
        for i in range(2 * self.col_addr_size):
            x_offset = (i + 1) * (self.gap_central_bus + self.width_central_bus) 
            x_offset = -x_offset - self.start_of_left_central_bus
            self.central_line_xoffset.append(x_offset)
            self.add_rect(layer="metal2",  
                          offset=[x_offset, self.central_line_y_offset], 
                          width=self.width_central_bus, 
                          height=-self.central_line_y_offset - 4 * drc["minwidth_metal2"])

        # row adress lines
        for i in range(self.row_addr_size):
            x_offset = ((self.gap_central_bus + self.width_central_bus) 
                            * (i + 1 + 2*self.col_addr_size))
            x_offset = - x_offset -  self.start_of_left_central_bus
            self.central_line_xoffset.append(x_offset)    
            self.add_rect(layer="metal2",  
                          offset=[x_offset, self.central_line_y_offset], 
                          width=self.width_central_bus, 
                          height=-self.central_line_y_offset - 4*drc["minwidth_metal2"])

    def route_pre_charge_to_bitcell_array(self):
        """ Routing of BL and BR between pre-charge and bitcell array """
        for i in range(self.num_cols):
            BL_position = self.precharge_array_position + self.precharge_array.BL_positions[i]
            BR_position = self.precharge_array_position + self.precharge_array.BR_positions[i]
            correct = vector(0.5*drc["minwidth_metal2"],
                             self.gap_between_precharge_and_bitcell
                                 -self.precharge_array_position.y)
            # these two rectangles cannot be replaced with add_path. They are not connected together. 
            self.add_rect(layer="metal2", 
                          offset=BL_position.scale(1,0) - correct, 
                          width=drc["minwidth_metal2"], 
                          height=self.gap_between_precharge_and_bitcell)
            self.add_rect(layer="metal2", 
                          offset=BR_position.scale(1,0) - correct,
                          width=drc["minwidth_metal2"],
                          height=self.gap_between_precharge_and_bitcell)

    def route_between_sense_amp_and_tri_gate(self):
        """ Routing of sense amp output to tri_gate input """
        for i in range(self.word_size):
            # Connection of data_out of sense amp to data_ in of msf_data_out
            tri_gate_in_position = (self.tri_gate_array.tri_in_positions[i].scale(1,-1) 
                                        + self.tri_gate_array_offset)
            sa_data_out_position = (self.sens_amp_array_position
                                        + self.sens_amp_array.Data_out_positions[i])

            startY = (self.tri_gate_array_offset.y - self.tri_gate_array.height
                          - 2 * drc["minwidth_metal3"] 
                          + 0.5 * drc["minwidth_metal1"])
            start = vector(tri_gate_in_position.x - 3 * drc["minwidth_metal3"], 
                           startY)

            m3_min = vector([drc["minwidth_metal3"]] * 2)
            mid1 = (tri_gate_in_position.scale(1,0) 
                        + sa_data_out_position.scale(0,1) + m3_min.scale(-3, 1))
            mid2 = sa_data_out_position + m3_min.scale(0.5, 1)
            self.add_path("metal3", [start, mid1, mid2])

            mid3 = [tri_gate_in_position.x, startY]
            self.add_path("metal2", [start, mid3, tri_gate_in_position])

            offset = start - vector([0.5*drc["minwidth_metal3"]] * 2)
            self.add_via(("metal2", "via2", "metal3"),offset)

    def route_tri_gate_out(self):
        """ Metal 3 routing of tri_gate output data """
        for i in range(self.word_size):
            tri_gate_out_position = (self.tri_gate_array.DATA_positions[i].scale(1,-1)
                                        + self.tri_gate_array_offset)
            data_line_position = [tri_gate_out_position.x - 0.5 * drc["minwidth_metal3"], 
                                  self.min_point]
            # save data line position
            self.data_positions.append(data_line_position)
            self.add_via(("metal2", "via2", "metal3"), data_line_position)
            self.add_rect(layer="metal3", 
                          offset=data_line_position, 
                          width=drc["minwidth_metal3"], 
                          height=tri_gate_out_position.y - self.min_point)

    def route_between_wordline_driver_and_bitcell_array(self):
        """ Connecting Wordline driver output to Bitcell WL connection  """
        WL_horizontal_distance = (- self.wordline_driver.WL_positions[0].x
                                      - self.wordline_driver_position.x)
        via_shift = (self.m1m2_via.second_layer_width 
                         - self.m1m2_via.first_layer_width) / 2

        for i in range(self.num_rows):
            bitcell_WL_position = (self.bitcell_array.WL_positions[i] 
                                       + vector(0.5 * drc["minwidth_metal1"], 0))
            worldline_WL_position = (self.wordline_driver.WL_positions[i]
                                         + self.wordline_driver_position)
            worldline_decode_out_position = (self.wordline_driver.decode_out_positions[i]
                                                 + self.wordline_driver_position)
            decoder_decode_out_position = (self.decoder.decode_out_positions[i]
                                               + self.decoder_position)

            WL_vertical_distance = worldline_WL_position.y - bitcell_WL_position.y
            decode_out_height = abs(worldline_decode_out_position.y
                                        - decoder_decode_out_position.y) + drc["minwidth_metal1"]

            if(WL_vertical_distance > 0):
                y_dir = 1
            else:
                y_dir = -1
            WL_vertical_distance += 2 * y_dir * drc["minwidth_metal1"]
            self.add_rect(layer="metal1", 
                          offset=decoder_decode_out_position, 
                          width=drc["minwidth_metal1"],
                          height=y_dir * decode_out_height)

            mid = bitcell_WL_position - vector(WL_horizontal_distance, 0)
            target = bitcell_WL_position + vector(- WL_horizontal_distance,
                                                  WL_vertical_distance)
            self.add_path("metal1", [bitcell_WL_position, mid, target])

        # Connecting the vdd of the word line driver to the vdd of the bitcell array.
        power_rail_width = (self.bitcell_array.vdd_positions[0].x
                                - self.wordline_driver.vdd_positions[0].x 
                                - self.wordline_driver_position.x)
        for i, offset in enumerate(self.wordline_driver.vdd_positions):
            vdd_offset = self.wordline_driver_position + offset
            if(i % 2 == 0):
                self.add_rect(layer="metal1",  
                              offset=vdd_offset, 
                              width=power_rail_width, 
                              height=drc["minwidth_metal1"])

    def route_column_address_lines(self):
        """ Connecting the select lines of column mux to the address bus """
        for i in range(2*self.col_addr_size):
            line_index = i + self.number_of_control_lines
            col_addr_line_position = (self.column_mux_array.addr_line_positions[i]
                                          + self.column_mux_array_position) 
            
            contact_offset = [self.central_line_xoffset[line_index], 
                              col_addr_line_position.y]
            connection_width = (col_addr_line_position.x 
                                    - self.central_line_xoffset[line_index])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=contact_offset)
            self.add_rect(layer="metal1", 
                          offset=contact_offset,
                          width=connection_width, 
                          height=drc["minwidth_metal1"])

        # Take care of the column address decoder routing
        # If there is a 2:4 decoder for column select lines
        if(self.col_addr_size == 2):

            # The snake connection between last two address flop to the input
            # of the 2:4 column_mux line decoder

            for i in range(2):
                ff_index = i + self.row_addr_size
                current_dout = self.msf_address.dout_positions[ff_index]
                msf_row_addr_line_position = (current_dout.rotate_scale(1,-1)
                                                  + self.msf_address_offset)

                line_index = self.num_central_bus - 2 + i
                line_offset = self.central_line_xoffset[line_index]
                y_offset = (self.col_decoder_position.y + self.col_decoder.height
                                + (i + 1) * drc["metal2_to_metal2"]
                                + i * drc["minwidth_metal2"])

                gap = drc["minwidth_metal2"] + 2 * drc["metal2_to_metal2"]
                input_rail_x = self.col_decoder_position.x - (i + 1) * gap 
                A_position = (self.col_decoder_position 
                                  + self.col_decoder.A_positions[i])
                offset = [input_rail_x - 0.5 * drc["minwidth_metal2"], 
                          A_position.y]
                self.add_rect(layer="metal1",  
                              offset=offset, 
                              width=A_position.x - input_rail_x, 
                              height=drc["minwidth_metal1"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=offset)

                source = msf_row_addr_line_position
                mid1 = [line_offset, msf_row_addr_line_position.y]
                mid2 = [line_offset, y_offset]
                mid3 = [input_rail_x, y_offset]
                target = [input_rail_x, self.col_decoder_position.y]
                self.add_path("metal2", [source, mid1, mid2, mid3, target])
                
            # connections between outputs of 2:4 decoder to the extension of
            # main address bus
            for i in range(4):
                line_index = i + self.number_of_control_lines
                x_offset = self.central_line_xoffset[line_index]
                y_offset = self.col_decoder_position.y
                contact_offset = vector(x_offset,y_offset)

                col_decoder_out_position =(self.col_decoder_position
                                            + self.col_decoder.decode_out_positions[i]
                                            + vector(0, 0.5 * drc["minwidth_metal1"])) 
                connection_width = (x_offset - col_decoder_out_position.x 
                                        + 0.5 * drc["minwidth_metal2"]) 
                mid1 = col_decoder_out_position + vector(connection_width,0)
                mid2 = col_decoder_out_position + vector(connection_width,
                                                         -self.central_line_y_offset)

                self.add_wire(layers=("metal1", "via1", "metal2"),
                              coordinates=[col_decoder_out_position,mid1,mid2],
                              offset=col_decoder_out_position)
                
        # if there are only two column select lines we just connect the dout_bar of the last FF 
        # to only select line and dout of that FF to the other select line
        elif(self.col_addr_size == 1):
            ff_index = self.row_addr_size
            base = self.msf_address_offset - vector(0, 0.5 * drc["minwidth_metal3"])
            dout_position = (self.msf_address.dout_positions[ff_index].rotate_scale(1,-1)
                                 + base)
            dout_bar_position = (self.msf_address.dout_bar_positions[ff_index].rotate_scale(1,-1)
                                     + base)

            y_offset = self.msf_address_offset.y - self.msf_address.width
            height = self.central_line_y_offset - y_offset

            for i in range(2):
                self.add_rect(layer="metal2",  
                              offset=[self.central_line_xoffset[i + self.number_of_control_lines],
                                      y_offset], 
                              width=self.width_central_bus, 
                              height=height)

            # dout connection to column select 1
            line_offset = self.central_line_xoffset[self.number_of_control_lines + 1]
            connection_width = line_offset - dout_position.x + drc["minwidth_metal2"]
            self.add_rect(layer="metal3",  
                          offset=dout_position,
                          width=connection_width, 
                          height=drc["minwidth_metal3"])
            # two m2m3_via contancts on both end
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=[line_offset, 
                                 dout_position.y + drc["minwidth_metal3"]], 
                         mirror="R270")
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=dout_position, 
                         mirror="R90")
            # dout_bar connection to column select 0
            line_offset = self.central_line_xoffset[self.number_of_control_lines]
            connection_width = line_offset - dout_bar_position.x + drc["minwidth_metal2"]
            self.add_rect(layer="metal3",  
                          offset=dout_bar_position,
                          width=connection_width, 
                          height=drc["minwidth_metal3"])
            # two m2m3_via contancts on both end
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=[line_offset, dout_bar_position.y])
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=(dout_bar_position 
                                     + vector(drc["minwidth_metal2"], 0)), 
                         mirror="R90")
            
    def route_msf_address_to_row_decoder(self):
        """ Routing the row address lines from the address ms-flop array to the row-decoder  """
        for i in range(self.row_addr_size):
            decoder_row_addr_line_position = (self.decoder_position
                                                  + self.decoder.A_positions[i])

            line_index = i + 2*self.col_addr_size + self.number_of_control_lines
            connection_width = (self.central_line_xoffset[line_index] + drc["minwidth_metal2"]
                                    - decoder_row_addr_line_position.x) 
            first_contact_offset = [self.central_line_xoffset[line_index], 
                                    decoder_row_addr_line_position.y]

            self.add_rect(layer="metal1", 
                          offset=decoder_row_addr_line_position,
                          width=connection_width, 
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=first_contact_offset)

            # addres translation should take care of the 270 degree CCW  rotation
            # addres translation should take care of the 270 degree CCW  rotation
            msf_row_addr_line_position = (self.msf_address.dout_positions[i].rotate_scale(1,-1)
                                              + self.msf_address_offset
                                              - vector(0, 0.5 * drc["minwidth_metal3"]))
            connection_width = (self.central_line_xoffset[line_index] + drc["minwidth_metal2"]
                                    - msf_row_addr_line_position.x) 
            second_contact_offset = [self.central_line_xoffset[line_index], 
                                     msf_row_addr_line_position.y]

            self.add_rect(layer="metal3", 
                          offset=msf_row_addr_line_position,
                          width=connection_width, 
                          height=drc["minwidth_metal3"])
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=second_contact_offset)
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=msf_row_addr_line_position, 
                          mirror="R90")

        for i in range(self.addr_size):
            # Route msf address inputs
            msf_din_position = (self.msf_address.din_positions[i].rotate_scale(1,-1) 
                                    + self.msf_address_offset
                                    - vector(0, 0.5 * drc["minwidth_metal3"]))
            address_position = vector(self.left_vdd_x_offset, 
                                      msf_din_position.y)
            self.address_positions.append(address_position)
            self.add_rect(layer="metal3", 
                          offset=address_position, 
                          width=msf_din_position.x - self.left_vdd_x_offset, 
                          height=drc["minwidth_metal3"])

    def route_control_lines(self):
        """ Routing of control lines """
       # 5 = clk, 4 = tri_en_bar, 3 = tri_en, 2 = clk_bar, 1 = w_en, 0 = s_en

        self.clk_position = [self.central_line_xoffset[5], 0]
        self.tri_en_bar_position = [self.central_line_xoffset[4], 0]
        self.tri_en_position = [self.central_line_xoffset[3], 0]
        self.clk_bar_position = [self.central_line_xoffset[2], 0]
        self.w_en_position = [self.central_line_xoffset[1], 0]
        self.s_en_position = [self.central_line_xoffset[0], 0]

        right_hand_mapping = [2, 4, 3, 2, 1, 0]

        right_side = []
        right_side.append(self.ms_flop_data_in_offset
                              + self.msf_data_in.clk_positions[0]
                              - vector(0, 0.5 * drc["minwidth_metal1"]))
        right_side.append(self.tri_gate_array_offset
                              + vector(1,-1).scale(self.tri_gate_chars["en_bar"])
                              - vector(0, 0.5 * drc["minwidth_metal1"]))
        right_side.append(self.tri_gate_array_offset
                              + vector(1,-1).scale(self.tri_gate_chars["en"])
                              - vector(0, 0.5 * drc["minwidth_metal1"]))
        right_side.append(self.precharge_array_position
                              + self.precharge_array.pclk_position)
        right_side.append(self.write_driver_array_position
                              + self.write_driver_array.wen_positions[0])
        right_side.append(self.sens_amp_array_position 
                              + self.sens_amp_array.SCLK_positions[0])
  
        """ Routing control signals through the central bus.
        Connection of control signal input to the central bus is in metal1
        Connection from the central bus to the main control block crosses
        pre-decoder and this connections are in metal3"""

        control_line_offsets = []
        """ Connecting right hand side [sense amp. write_driver , tri state
        gates, ffs] to the central bus""" 
        
        for i in range(len(right_side)):
            bus_line_index = right_hand_mapping[i]

            x_offset = self.central_line_xoffset[bus_line_index]
            y_offset = self.tri_gate_array_offset.y
            height = self.central_line_y_offset - y_offset
            right_side_connection_width = right_side[i].x - self.central_line_xoffset[bus_line_index]
            right_side_contact_offset = [self.central_line_xoffset[bus_line_index],
                                         right_side[i].y]
            self.add_rect(layer="metal1", 
                          offset=right_side_contact_offset,
                          width=right_side_connection_width, 
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=right_side_contact_offset)

            if(right_side[i].y > 0):
                self.add_rect(layer="metal2", 
                              offset=[self.central_line_xoffset[bus_line_index], 0], 
                              width=drc["minwidth_metal2"], 
                              height=right_side[i].y + 2*drc["minwidth_metal2"])

        """ CLK connection from central bus to MSF address
        should we move this somewhere else hard to find when modify""" 
        msf_address_clk_position = (self.msf_address_offset 
                                        + self.msf_address.clk_positions[0].rotate_scale(1,-1) 
                                        + vector(- 0.5 * drc["minwidth_metal1"], 
                                                 2 * drc["minwidth_metal2"]))
        clk_connection_position = (self.msf_address_offset 
                                       + vector(self.msf_address.clk_positions[0].y, 
                                                2 * drc["minwidth_metal3"]))

        connection_width = self.central_line_xoffset[5] - clk_connection_position.x
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=msf_address_clk_position, 
                      mirror="R90")
        self.add_via(layers=("metal2", "via2", "metal3"),
                      offset=msf_address_clk_position, 
                      mirror="R90")

        mid_base = vector(msf_address_clk_position.x, clk_connection_position.y)
        mid1 = mid_base + vector(0, 0.5 * drc["minwidth_metal3"])
        mid2 = (mid_base + vector([0.5 * drc["minwidth_metal3"]] * 2) 
                   + vector(connection_width, 0))      
        self.add_path(layer="metal3",
                      coordinates=[msf_address_clk_position,mid1,mid2], 
                      width=drc["minwidth_metal3"])
       
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=[self.central_line_xoffset[5], 
                             clk_connection_position.y])

        # Clk connection from central Bus to wordline_driver
        wl_clk_position = (self.wordline_driver_position 
                               + self.wordline_driver.clk_positions[0])
        connection_width = (self.central_line_xoffset[5] - wl_clk_position.x
                                + drc["minwidth_metal1"])
        y_off = self.max_point - 2.5 * drc["minwidth_metal1"]
        start = wl_clk_position + vector(0.5 * drc["minwidth_metal1"], 0)
        mid1 = [wl_clk_position.x, y_off]
        mid2 = mid1 + vector(connection_width, 0)
        self.add_path(layer="metal1",
                      coordinates=[wl_clk_position, mid1, mid2], 
                      width=drc["minwidth_metal1"],
                      offset=start)
        
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.central_line_xoffset[5], 
                             self.max_point - 3*drc["minwidth_metal1"]])

    def route_bank_select_or2_gates(self):
        """ Route array of or gates to gate the control signals in case 
            of multiple banks are created in upper level SRAM module """
        bank_select_line_xoffset = (self.bank_select_or_position.x 
                                        - 3*drc["minwidth_metal2"])
        self.add_rect(layer="metal2", 
                      offset=[bank_select_line_xoffset, 
                              self.bank_select_or_position.y], 
                      width=drc["minwidth_metal2"],  
                      height=self.number_of_control_lines*self.inv.height)
        
        # bank select inverter routing
        # output side
        start = self.bank_select_inv_position +  self.inv4x.Z_position
        end = self.bank_select_or_position + self.NOR2.B_position
        mid = vector(start.x, end.y)
        self.add_path("metal1", [start, mid, end])
        
        # input side
        start = self.bank_select_inv_position + self.inv4x.A_position
        end = vector(self.left_vdd_x_offset, start.y + 3 * drc["minwidth_metal3"])
        mid = vector(start.x, end.y)
        self.add_wire(("metal2", "via1", "metal1"), [start, mid, end])

        # save position
        self.bank_select_position = end - vector(0, 0.5 * drc["minwidth_metal2"])
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.bank_select_position)

        x_offset = (self.bank_select_or_position.x + self.NOR2.width
                        + self.inv4x.width - drc["minwidth_metal1"])
        for i in range(self.number_of_control_lines):
            base = self.bank_select_or_position.y + self.inv.height * i
            if(i % 2):
                Z_y_offset = (base + self.inv.height - self.inv4x.Z_position.y 
                                - drc["minwidth_metal1"])
                B_y_offset = (base + self.inv.height - self.NOR2.B_position.y 
                              - 0.5 * drc["minwidth_metal1"])
                A_y_offset = (base + self.inv.height - self.NOR2.A_position.y 
                              - 0.5 * drc["minwidth_metal1"])
            else:
                Z_y_offset = (base + self.inv4x.Z_position.y)
                B_y_offset = (base + self.NOR2.B_position.y 
                                  - 0.5 * drc["minwidth_metal1"])
                A_y_offset = (base + self.NOR2.A_position.y  
                                  + 0.5 * drc["minwidth_metal1"]
                                  - self.m1m2_via.width)

            # output
            self.add_rect(layer="metal3", 
                          offset=[x_offset, Z_y_offset], 
                          width=self.central_line_xoffset[i] - x_offset,  
                          height=drc["minwidth_metal3"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=[x_offset, Z_y_offset])
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=[x_offset, Z_y_offset])
            self.add_via(layers=("metal2", "via2", "metal3"),
                          offset=[self.central_line_xoffset[i], Z_y_offset])

            # B_input
            if i != 5:
                self.add_rect(layer="metal1", 
                              offset=[bank_select_line_xoffset, B_y_offset], 
                              width=(self.bank_select_or_position.x 
                                         - bank_select_line_xoffset),  
                              height=drc["minwidth_metal1"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[bank_select_line_xoffset, B_y_offset])

            # A_input
            if i != 3:
                self.add_rect(layer="metal3", 
                              offset=[self.left_vdd_x_offset, A_y_offset], 
                              width=(self.bank_select_or_position.x
                                         - self.left_vdd_x_offset),  
                              height=drc["minwidth_metal3"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                              offset=[self.bank_select_or_position.x
                                          + drc["minwidth_metal1"],
                                      A_y_offset], 
                              mirror="R90")
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=[self.bank_select_or_position.x 
                                         + drc["minwidth_metal1"],
                                     A_y_offset], 
                             mirror="R90")
            else:
                # connect A to last A, both are tri_en_bar
                via_offset = vector(self.bank_select_or_position.x 
                                        + drc["minwidth_metal1"], 
                                    A_y_offset)
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=via_offset,
                             mirror="R90")
                self.add_via(layers=("metal2", "via2", "metal3"),
                             offset=via_offset, 
                             mirror="R90")

                start = via_offset + vector(0, 0.5 * self.m1m2_via.width)
                mid = [self.left_vdd_x_offset - self.left_vdd_x_offset 
                           - drc["minwidth_metal2"] - drc["metal2_to_metal2"] 
                           + bank_select_line_xoffset,
                       start.y]
                correct_y = (2 * self.NOR2.A_position.y + drc["minwidth_metal1"]
                                 - self.m1m2_via.width)
                end = start +  vector(0, correct_y)
                self.add_wire(("metal3", "via2", "metal2"), [start, mid, end])

            # Save position
            setattr(self,"{0}_position".format(self.control_signals[i]),
                    [self.left_vdd_x_offset, A_y_offset])

    def route_power_rail_vdd(self):
        """ Routing of VDD for all modules """

        # RIGHT HAND SIDE VDD RAIL CONNECTIONS
        # Connecting Bitcell-array VDDs
        for i,offset in enumerate(self.bitcell_array.vdd_positions):
            if (i % 2 == 0):
                self.add_rect(layer="metal1", 
                              offset=offset - vector(0, 0.5 * drc["minwidth_metal1"]), 
                              width=self.right_vdd_x_offset - offset.x, 
                              height=drc["minwidth_metal1"])

        # Connecting Pre-charge VDD
        for offset in self.precharge_array.vdd_positions:
            self.add_rect(layer="metal1", 
                          offset=self.precharge_array_position + offset, 
                          width=(self.right_vdd_x_offset - offset.x
                                     - self.precharge_array_position.x), 
                          height=drc["minwidth_metal1"])

        # Connecting Sense Amp VDD
        for offset in self.sens_amp_array.vdd_positions:
            self.add_rect(layer="metal1", 
                          offset=self.sens_amp_array_position + offset, 
                          width=(self.right_vdd_x_offset - offset.x
                                    - self.sens_amp_array_position.x), 
                          height=drc["minwidth_metal1"])

        # Connecting Write Driver VDD
        for offset in self.write_driver_array.vdd_positions:
            self.add_rect(layer="metal1", 
                          offset=self.write_driver_array_position + offset, 
                          width=(self.right_vdd_x_offset - offset.x
                                    - self.write_driver_array_position.x), 
                          height=drc["minwidth_metal1"])

        # Connecting msf_data_in VDD
        for offset in self.msf_data_in.vdd_positions:
            self.add_rect(layer="metal1", 
                          offset=(self.ms_flop_data_in_offset + offset 
                                  -vector(0, 0.5 * drc["minwidth_metal1"])), 
                          width=self.right_vdd_x_offset \
                              - (self.ms_flop_data_in_offset.x + offset.x), 
                          height=drc["minwidth_metal1"])

        # Connecting tri_gate VDD
        for offset in self.tri_gate_array.vdd_positions:
            self.add_rect(layer="metal1", 
                          offset=(self.tri_gate_array_offset + offset.scale(1,-1) 
                                      - vector(0, 0.5 * drc["minwidth_metal1"])), 
                          width=(self.right_vdd_x_offset - offset.x
                                     - self.tri_gate_array_offset.x), 
                          height=drc["minwidth_metal1"])

        # LEFT HAND SIDE VDD RAIL CONNECTIONS

        # Connecting decoder VDD
        for i, offset in enumerate(self.decoder.vdd_positions):
            decoder_vdd_offset = self.decoder_position + offset
            if(i % 2 == 0):
                self.add_rect(layer="metal1",  
                              offset=decoder_vdd_offset,  
                              width=self.left_vdd_x_offset - decoder_vdd_offset.x, 
                              height=drc["minwidth_metal1"])

        # Connecting pre-decoder vdds
        for offset in self.decoder.pre_decoder_vdd_positions:
            preedecoder_vdd_offset = self.decoder_position + offset
            self.add_rect(layer="metal1",  
                          offset=[self.left_vdd_x_offset, 
                                  preedecoder_vdd_offset.y],  
                          width=preedecoder_vdd_offset.x - self.left_vdd_x_offset, 
                          height=drc["minwidth_metal1"])

        # Connecting column_decoder vdd [Its the 2:4 decoder]
        if(self.col_addr_size == 2):
            col_vdd_offset = self.col_decoder_position + self.col_decoder.vdd_position
            self.add_rect(layer="metal1",  
                          offset=[self.left_vdd_x_offset, 
                                  col_vdd_offset.y],  
                          width=col_vdd_offset.x - self.left_vdd_x_offset, 
                          height=drc["minwidth_metal1"])

        # Connecting address Flip-flop VDD
        for offset in self.msf_address.vdd_positions:
            ms_addres_gnd_y = (self.msf_address_offset.y - self.msf_address.width
                                   - 0.5 * drc["minwidth_metal1"])
            y_offset = ms_addres_gnd_y - 2.5*drc["minwidth_metal1"]
            vdd_connection = vector(self.left_vdd_x_offset, y_offset)
            mid1 = vdd_connection - vector(0, 0.5 * drc["minwidth_metal1"])
            mid2 = vector(self.msf_address_offset.x + offset.y,
                          mid1.y)
            mid3 = vector(mid2.x, ms_addres_gnd_y)
            self.add_path(layer="metal1",
                          coordinates=[mid1, mid2, mid3], 
                          width=drc["minwidth_metal1"],
                          offset = vdd_connection)

        # Connecting bank_select_and2_array vdd
        if(self.num_banks > 1):
            for i in range(self.number_of_control_lines):
                if(i % 2):
                    self.add_rect(layer="metal1", 
                                  offset=[self.left_vdd_x_offset,
                                          self.bank_select_or_position.y
                                              + i * self.inv.height
                                              - 0.5 * drc["minwidth_metal1"]], 
                                  width=(self.bank_select_or_position.x
                                             - self.left_vdd_x_offset),  
                                  height=drc["minwidth_metal1"])

    def route_power_rail_gnd(self):
        """ Routing of GND for all modules """
        # FIRST HORIZONTAL GND RAIL BETWEEN PRECHARGE AND BITCELL
        yoffset = self.bitcell_array.height + 2*drc["minwidth_metal1"]
        # Add gnd via
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.left_gnd_x_offset, yoffset],
                     size=(2,1))
        self.add_rect(layer="metal1",  
                      offset=[self.left_gnd_x_offset, yoffset],  
                      width=self.bitcell_array.width - self.left_gnd_x_offset, 
                      height=drc["minwidth_metal1"])

        for offset in self.bitcell_array.gnd_positions:
            #print self.bitcell_array.gnd_positions
            self.add_rect(layer="metal2", 
                          offset=[offset.x - 0.5*drc["minwidth_metal2"], 
                                  self.bitcell_array.height], 
                          width=drc["minwidth_metal2"], 
                          height= yoffset + drc["minwidth_metal1"] \
                              - self.bitcell_array.height)
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=[offset.x + drc["minwidth_metal2"], yoffset], 
                          mirror="R90")
       
        # GND connectiontions for the left side of bitcell-array
        self.add_rect(layer="metal2",  
                      offset=[-drc["minwidth_metal2"], 0],
                      width=drc["minwidth_metal2"],  
                      height=yoffset + drc["minwidth_metal1"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[0, yoffset], 
                     mirror="R90")

        # LEFT HAND SIDE GND RAIL CONNECTIONS
        # Connections of Tri_gate GND to the left hand GND rail

        # This is only used to compute teh sizes below
        gnd_contact = contact(layer_stack=("metal1", "via1", "metal2"), 
                              dimensions=(2, 1))

        x_off = (self.left_gnd_x_offset + self.power_rail_width 
                                - gnd_contact.width)
        y_off = (self.tri_gate_array_offset.y - self.tri_gate_array.height 
                    - drc["minwidth_metal1"])
        tri_gate_gnd_offset = vector(x_off, y_off)
        self.add_rect(layer="metal1", 
                      offset=tri_gate_gnd_offset, 
                      width=(self.tri_gate_array_offset.x 
                                 + self.tri_gate_array.width 
                                 - tri_gate_gnd_offset.x), 
                      height=drc["minwidth_metal1"])
        # Add gnd via
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=tri_gate_gnd_offset,
                     size=(2,1))

        for offset in self.tri_gate_array.gnd_positions:
            tri_gate_gnd_position = vector(self.tri_gate_array_offset.x + offset.x,            
                                           tri_gate_gnd_offset.y)
            offset = tri_gate_gnd_position - vector(0.5 * self.m1m2_via.width, 0)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset)

        # Connecting decoder GND
        for i,offset in enumerate(self.wordline_driver.gnd_positions):
            wordline_driver_gnd_offset = self.wordline_driver_position + offset
            even_row = (i % 2 == 0 and i != 0)
            last_row = (i == self.num_rows - 1)
            if even_row or last_row:
                if even_row:
                    correct = vector(0,0)
                # Connection of the last GND rail [The top most gnd of decoder]
                if last_row:
                    correct = vector(0, drc["minwidth_metal1"])
                self.add_rect(layer="metal2",  
                              offset=wordline_driver_gnd_offset - correct,
                              width=(self.left_gnd_x_offset 
                                         - wordline_driver_gnd_offset.x), 
                              height=drc["minwidth_metal2"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[self.wordline_driver_position.x 
                                         + self.wordline_driver.width 
                                         + 0.5*drc["minwidth_metal2"],
                                     wordline_driver_gnd_offset.y 
                                         - correct.y], 
                             mirror="R90")

        # Connecting Pre-decoder gnd rail
        for i in range(len(self.decoder.pre_decoder_gnd_positions)):
            offset = self.decoder.pre_decoder_gnd_positions[i]
            preedecoder_gnd_offset = self.decoder_position + offset
            self.add_rect(layer="metal1",  
                          offset=preedecoder_gnd_offset,  
                          width=self.left_gnd_x_offset - preedecoder_gnd_offset.x,
                          height=drc["minwidth_metal1"])
            # Add gnd via
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.left_gnd_x_offset, 
                                 preedecoder_gnd_offset.y + drc["minwidth_metal1"]], 
                         mirror="MX",
                         size=(2,1))

        # Connecting column_decoder gnd [Its the 2:4 decoder]
        if(self.col_addr_size == 2):
            col_gnd_offset = self.col_decoder_position + self.col_decoder.gnd_position
            self.add_rect(layer="metal1",  
                          offset=col_gnd_offset, 
                          width=self.left_gnd_x_offset - col_gnd_offset.x, 
                          height=drc["minwidth_metal1"])
            # Add gnd via
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.left_gnd_x_offset, col_gnd_offset.y],
                         size=(2,1))

        # Connecting address FF GND
        for offset in self.msf_address.gnd_positions:
            correct = vector(self.msf_address.height, 
                             - offset.x - 0.5*drc["minwidth_metal1"])
            ms_addres_gnd_offset = self.msf_address_offset + correct
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=(ms_addres_gnd_offset  
                                     + vector(drc["minwidth_metal1"], 0)), 
                         mirror="R90")
            self.add_rect(layer="metal1",  
                          offset=ms_addres_gnd_offset,  
                          width=self.left_gnd_x_offset - ms_addres_gnd_offset.x, 
                          height=drc["minwidth_metal1"])
            # Add gnd via
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.left_gnd_x_offset, 
                                 ms_addres_gnd_offset.y],
                         size=(2,1))

        # Connecting bank_select_or2_array gnd
        if(self.num_banks > 1):
            self.bank_select_inv_position
            self.add_rect(layer="metal1", 
                          offset=(self.bank_select_inv_position
                                       + self.inv4x.gnd_position), 
                          width=(self.bank_select_or_position.x
                                     - self.bank_select_inv_position.x),  
                          height=drc["minwidth_metal1"])

            x_offset = (self.bank_select_or_position.x 
                            + self.NOR2.width + self.inv4x.width)
            for i in range(self.number_of_control_lines):
                if(i % 2 == 0):
                    y_offset = self.bank_select_or_position.y + i*self.inv.height \
                        - 0.5*drc["minwidth_metal1"]
                    #both M1 & M2 are horizontal, cannot be  replaced with wire
                    self.add_rect(layer="metal1", 
                                  offset=[x_offset,  y_offset], 
                                  width=drc["minwidth_metal1"],  
                                  height=drc["minwidth_metal1"])
                    self.add_rect(layer="metal2", 
                                  offset=[x_offset,  y_offset], 
                                  width=self.left_gnd_x_offset \
                                      - x_offset + self.power_rail_width,  
                                  height=drc["minwidth_metal2"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                 offset=[x_offset + drc["minwidth_metal1"],  
                                         y_offset], 
                                 mirror="R90")

    def delay(self, slope):
        """ return  analytical delay of the bank"""
        msf_addr_delay = self.msf_address.delay(slope, 
                                                self.decoder.input_load())

        decoder_delay = self.decoder.delay(msf_addr_delay.slope,
                                           self.wordline_driver.input_load())

        word_driver_delay = self.wordline_driver.delay(decoder_delay.slope,
                                                       self.bitcell_array.input_load())

        bitcell_array_delay = self.bitcell_array.delay(word_driver_delay.slope)

        bl_t_data_out_delay = self.sens_amp_array.delay(bitcell_array_delay.slope,
                                                        self.bitcell_array.output_load())
        # output load of bitcell_array is set to be only small part of bl for sense amp.

        data_t_DATA_delay = self.tri_gate_array.delay(bl_t_data_out_delay.slope)

        result = msf_addr_delay + decoder_delay + word_driver_delay \
                 + bitcell_array_delay + bl_t_data_out_delay + data_t_DATA_delay
        return result
