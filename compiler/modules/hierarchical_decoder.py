# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
import math
from sram_factory import factory
from vector import vector
from globals import OPTS


class hierarchical_decoder(design.design):
    """
    Dynamically generated hierarchical decoder.
    """
    def __init__(self, name, num_outputs):
        super().__init__(name)

        self.AND_FORMAT = "DEC_AND_{0}"
        
        self.pre2x4_inst = []
        self.pre3x8_inst = []

        b = factory.create(module_type="bitcell")
        self.cell_height = b.height
            
        self.num_outputs = num_outputs
        self.num_inputs = math.ceil(math.log(self.num_outputs, 2))
        (self.no_of_pre2x4, self.no_of_pre3x8)=self.determine_predecodes(self.num_inputs)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        self.add_modules()
        self.setup_netlist_constants()
        self.add_pins()
        self.create_pre_decoder()
        self.create_row_decoder()

    def create_layout(self):
        self.setup_layout_constants()
        self.place_pre_decoder()
        self.place_row_decoder()
        
        self.height = max(self.predecoder_height, self.row_decoder_height) + self.bus_space
        
        self.route_inputs()
        self.route_outputs()
        self.route_decoder_bus()
        self.route_vdd_gnd()
        
        self.offset_all_coordinates()
        
        self.width = self.and_inst[0].rx() + self.m1_space
        
        self.add_boundary()
        self.DRC_LVS()
                
    def add_modules(self):
        self.and2 = factory.create(module_type="and2_dec",
                                   height=self.cell_height)
        self.add_mod(self.and2)
        
        self.and3 = factory.create(module_type="and3_dec",
                                   height=self.cell_height)
        self.add_mod(self.and3)
        # TBD
        # self.and4 = factory.create(module_type="and4_dec")
        # self.add_mod(self.and4)
        
        self.add_decoders()

    def add_decoders(self):
        """ Create the decoders based on the number of pre-decodes """
        self.pre2_4 = factory.create(module_type="hierarchical_predecode2x4",
                                     height=self.cell_height)
        self.add_mod(self.pre2_4)
        
        self.pre3_8 = factory.create(module_type="hierarchical_predecode3x8",
                                     height=self.cell_height)
        self.add_mod(self.pre3_8)

    def determine_predecodes(self, num_inputs):
        """ Determines the number of 2:4 pre-decoder and 3:8 pre-decoder
        needed based on the number of inputs """
        if (num_inputs == 2):
            return (1, 0)
        elif (num_inputs == 3):
            return(0, 1)
        elif (num_inputs == 4):
            return(2, 0)
        elif (num_inputs == 5):
            return(1, 1)
        elif (num_inputs == 6):
            return(3, 0)
        elif (num_inputs == 7):
            return(2, 1)
        elif (num_inputs == 8):
            return(1, 2)
        elif (num_inputs == 9):
            return(0, 3)
        else:
            debug.error("Invalid number of inputs for hierarchical decoder", -1)

    def setup_netlist_constants(self):
        self.predec_groups = []  # This array is a 2D array.

        # Distributing vertical bus to different groups. One group belongs to one pre-decoder.
        # For example, for two 2:4 pre-decoder and one 3:8 pre-decoder, we will
        # have total 16 output lines out of these 3 pre-decoders and they will
        # be distributed as [ [0,1,2,3] ,[4,5,6,7], [8,9,10,11,12,13,14,15] ]
        # in self.predec_groups
        index = 0
        for i in range(self.no_of_pre2x4):
            lines = []
            for j in range(4):
                lines.append(index)
                index = index + 1
            self.predec_groups.append(lines)

        for i in range(self.no_of_pre3x8):
            lines = []
            for j in range(8):
                lines.append(index)
                index = index + 1
            self.predec_groups.append(lines)

    def setup_layout_constants(self):
        """ Calculate the overall dimensions of the hierarchical decoder """

        # If we have 4 or fewer rows, the predecoder is the decoder itself
        if self.num_inputs>=4:
            self.total_number_of_predecoder_outputs = 4 * self.no_of_pre2x4 + 8 * self.no_of_pre3x8
        else:
            self.total_number_of_predecoder_outputs = 0
            debug.error("Not enough rows ({}) for a hierarchical decoder. Non-hierarchical not supported yet.".format(self.num_inputs),
                        -1)

        # Calculates height and width of pre-decoder,
        # FIXME: Update with 4x16
        if self.no_of_pre3x8 > 0 and self.no_of_pre2x4 > 0:
            self.predecoder_width = max(self.pre3_8.width, self.pre2_4.width)
        elif self.no_of_pre3x8 > 0:
            self.predecoder_width = self.pre3_8.width
        else:
            self.predecoder_width = self.pre2_4.width

        # How much space between each predecoder
        self.predecoder_spacing = 2 * self.and2.height
        self.predecoder_height = self.pre2_4.height * self.no_of_pre2x4 + self.pre3_8.height * self.no_of_pre3x8 \
                                 + (self.no_of_pre2x4 + self.no_of_pre3x8 - 1) * self.predecoder_spacing

        # Inputs to cells are on input layer
        # Outputs from cells are on output layer
        if OPTS.tech_name == "sky130":
            self.bus_layer = "m1"
            self.bus_directions = "nonpref"
            self.bus_pitch = self.m1_pitch
            self.bus_space = self.m2_space
            self.input_layer = "m2"
            self.output_layer = "li"
            self.output_layer_pitch = self.li_pitch
        else:
            self.bus_layer = "m2"
            self.bus_directions = "pref"
            self.bus_pitch = self.m2_pitch
            self.bus_space = self.m2_space
            # These two layers being the same requires a special jog
            # to ensure to conflicts with the output layers
            self.input_layer = "m1"
            self.output_layer = "m3"
            self.output_layer_pitch = self.m3_pitch

        # Two extra pitches between modules on left and right
        self.internal_routing_width = self.total_number_of_predecoder_outputs * self.bus_pitch + self.bus_pitch
        self.row_decoder_height = self.and2.height * self.num_outputs

        # Extra bus space for supply contacts
        self.input_routing_width = self.num_inputs * self.bus_pitch + self.bus_space

    def route_inputs(self):
        """ Create input bus for the predecoders """
        # Find the left-most predecoder
        min_x = 0
        if self.no_of_pre2x4 > 0:
            min_x = min(min_x, self.pre2x4_inst[0].lx())
        if self.no_of_pre3x8 > 0:
            min_x = min(min_x, self.pre3x8_inst[0].lx())
        input_offset=vector(min_x - self.input_routing_width, 0)

        input_bus_names = ["addr_{0}".format(i) for i in range(self.num_inputs)]
        self.input_bus = self.create_vertical_pin_bus(layer=self.bus_layer,
                                                      offset=input_offset,
                                                      names=input_bus_names,
                                                      length=self.predecoder_height)
        
        self.route_input_to_predecodes()

    def route_input_to_predecodes(self):
        """ Route the vertical input rail to the predecoders """
        for pre_num in range(self.no_of_pre2x4):
            for i in range(2):
                index = pre_num * 2 + i

                input_pos = self.input_bus["addr_{}".format(index)].center()

                in_name = "in_{}".format(i)
                decoder_pin = self.pre2x4_inst[pre_num].get_pin(in_name)

                decoder_offset = decoder_pin.center()
                input_offset = input_pos.scale(1, 0) + decoder_offset.scale(0, 1)
                
                self.route_input_bus(decoder_offset, input_offset)
            
        for pre_num in range(self.no_of_pre3x8):
            for i in range(3):
                index = pre_num * 3 + i + self.no_of_pre2x4 * 2
                
                input_pos = self.input_bus["addr_{}".format(index)].center()

                in_name = "in_{}".format(i)
                decoder_pin = self.pre3x8_inst[pre_num].get_pin(in_name)

                decoder_offset = decoder_pin.center()
                input_offset = input_pos.scale(1, 0) + decoder_offset.scale(0, 1)
                
                self.route_input_bus(decoder_offset, input_offset)

    def route_input_bus(self, input_offset, output_offset):
        """
        Route a vertical M2 coordinate to another
        vertical M2 coordinate to the predecode inputs
        """
        
        self.add_via_stack_center(from_layer=self.bus_layer,
                                  to_layer=self.input_layer,
                                  offset=input_offset)
        self.add_via_stack_center(from_layer=self.bus_layer,
                                  to_layer=self.input_layer,
                                  offset=output_offset,
                                  directions=self.bus_directions)
        self.add_path(self.input_layer, [input_offset, output_offset])
    
    def add_pins(self):
        """ Add the module pins """
        
        for i in range(self.num_inputs):
            self.add_pin("addr_{0}".format(i), "INPUT")

        for j in range(self.num_outputs):
            self.add_pin("decode_{0}".format(j), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_pre_decoder(self):
        """ Creates pre-decoder and places labels input address [A] """
        
        for i in range(self.no_of_pre2x4):
            self.create_pre2x4(i)
            
        for i in range(self.no_of_pre3x8):
            self.create_pre3x8(i)

    def create_pre2x4(self, num):
        """ Add a 2x4 predecoder to the left of the origin """
        
        if (self.num_inputs == 2):
            index_off1 = index_off2 = 0
        else:
            index_off1 = num * 2
            index_off2 = num * 4

        pins = []
        for input_index in range(2):
            pins.append("addr_{0}".format(input_index + index_off1))
        for output_index in range(4):
            pins.append("out_{0}".format(output_index + index_off2))
        pins.extend(["vdd", "gnd"])

        self.pre2x4_inst.append(self.add_inst(name="pre_{0}".format(num),
                                              mod=self.pre2_4))
        self.connect_inst(pins)

    def create_pre3x8(self, num):
        """ Add 3x8 predecoder to the left of the origin and above any 2x4 decoders """
        # If we had 2x4 predecodes, those are used as the lower
        # decode output bits
        in_index_offset = num * 3 + self.no_of_pre2x4 * 2
        out_index_offset = num * 8 + self.no_of_pre2x4 * 4

        pins = []
        for input_index in range(3):
            pins.append("addr_{0}".format(input_index + in_index_offset))
        for output_index in range(8):
            pins.append("out_{0}".format(output_index + out_index_offset))
        pins.extend(["vdd", "gnd"])

        self.pre3x8_inst.append(self.add_inst(name="pre3x8_{0}".format(num),
                                              mod=self.pre3_8))
        self.connect_inst(pins)

    def place_pre_decoder(self):
        """ Creates pre-decoder and places labels input address [A] """
        
        for i in range(self.no_of_pre2x4):
            self.place_pre2x4(i)
            
        for i in range(self.no_of_pre3x8):
            self.place_pre3x8(i)

        self.predecode_height = 0
        if self.no_of_pre2x4 > 0:
            self.predecode_height = self.pre2x4_inst[-1].uy()
        if self.no_of_pre3x8 > 0:
            self.predecode_height = self.pre3x8_inst[-1].uy()

    def place_pre2x4(self, num):
        """ Place 2x4 predecoder to the left of the origin """
        
        base= vector(-self.pre2_4.width, num * (self.pre2_4.height + self.predecoder_spacing))
        self.pre2x4_inst[num].place(base)
        
    def place_pre3x8(self, num):
        """ Place 3x8 predecoder to the left of the origin and above any 2x4 decoders """
        height = self.no_of_pre2x4 * (self.pre2_4.height + self.predecoder_spacing) \
                 + num * (self.pre3_8.height + self.predecoder_spacing)
        offset = vector(-self.pre3_8.width, height)
        self.pre3x8_inst[num].place(offset)

    def create_row_decoder(self):
        """ Create the row-decoder by placing AND2/AND3 and Inverters
        and add the primary decoder output pins. """
        if (self.num_inputs >= 4):
            self.create_decoder_and_array()

    def create_decoder_and_array(self):
        """ Add a column of AND gates for final decode """

        self.and_inst = []
        
        # Row Decoder AND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    output = len(self.predec_groups[0]) * j + i
                    if (output < self.num_outputs):
                        name = self.AND_FORMAT.format(output)
                        self.and_inst.append(self.add_inst(name=name,
                                                           mod=self.and2))
                        pins =["out_{0}".format(i),
                               "out_{0}".format(j + len(self.predec_groups[0])),
                               "decode_{0}".format(output),
                               "vdd", "gnd"]
                        self.connect_inst(pins)

        # Row Decoder AND GATE array for address inputs >5.
        elif (self.num_inputs > 5):
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    for k in range(len(self.predec_groups[2])):
                        output = (len(self.predec_groups[0]) * len(self.predec_groups[1])) * k \
                                 + len(self.predec_groups[0]) * j + i

                        if (output < self.num_outputs):
                            name = self.AND_FORMAT.format(output)
                            self.and_inst.append(self.add_inst(name=name,
                                                               mod=self.and3))
                        
                            pins = ["out_{0}".format(i),
                                    "out_{0}".format(j + len(self.predec_groups[0])),
                                    "out_{0}".format(k + len(self.predec_groups[0]) + len(self.predec_groups[1])),
                                    "decode_{0}".format(output),
                                    "vdd", "gnd"]
                            self.connect_inst(pins)

    def place_row_decoder(self):
        """
        Place the row-decoder by placing AND2/AND3 and Inverters
        and add the primary decoder output pins.
        """
        if (self.num_inputs >= 4):
            self.place_decoder_and_array()

    def place_decoder_and_array(self):
        """
        Add a column of AND gates for final decode.
        This may have more than one decoder per row to match the bitcell height.
        """
        
        # Row Decoder AND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            self.place_and_array(and_mod=self.and2)

        # Row Decoder AND GATE array for address inputs >5.
        # FIXME: why this correct offset?)
        elif (self.num_inputs > 5):
            self.place_and_array(and_mod=self.and3)

    def place_and_array(self, and_mod):
        """
        Add a column of AND gates for the decoder above the predecoders.
        """

        for row in range(self.num_outputs):
            if ((row % 2) == 0):
                y_off = and_mod.height * row
                mirror = "R0"
            else:
                y_off = and_mod.height * (row + 1)
                mirror = "MX"

            x_off = self.internal_routing_width
            self.and_inst[row].place(offset=vector(x_off, y_off),
                                     mirror=mirror)

    def route_outputs(self):
        """ Add the pins. """

        for row in range(self.num_outputs):
            and_inst = self.and_inst[row]
            self.copy_layout_pin(and_inst, "Z", "decode_{0}".format(row))
        
    def route_decoder_bus(self):
        """
        Creates vertical metal 2 bus to connect predecoder and decoder stages.
        """

        # This is not needed for inputs <4 since they have no pre/decode stages.
        if (self.num_inputs >= 4):
            # This leaves an offset for the predecoder output jogs
            input_bus_names = ["predecode_{0}".format(i) for i in range(self.total_number_of_predecoder_outputs)]
            self.predecode_bus = self.create_vertical_pin_bus(layer=self.bus_layer,
                                                              pitch=self.bus_pitch,
                                                              offset=vector(self.bus_pitch, 0),
                                                              names=input_bus_names,
                                                              length=self.height)

            self.route_predecodes_to_bus()
            self.route_bus_to_decoder()

    def route_predecodes_to_bus(self):
        """
        Iterates through all of the predecodes
        and connects to the rails including the offsets
        """
        # FIXME: convert to connect_bus
        for pre_num in range(self.no_of_pre2x4):
            for i in range(4):
                predecode_name = "predecode_{}".format(pre_num * 4 + i)
                out_name = "out_{}".format(i)
                pin = self.pre2x4_inst[pre_num].get_pin(out_name)
                x_offset = self.pre2x4_inst[pre_num].rx() + self.output_layer_pitch
                y_offset = self.pre2x4_inst[pre_num].by() + i * self.cell_height
                self.route_predecode_bus_inputs(predecode_name, pin, x_offset, y_offset)
            
        # FIXME: convert to connect_bus
        for pre_num in range(self.no_of_pre3x8):
            for i in range(8):
                predecode_name = "predecode_{}".format(pre_num * 8 + i + self.no_of_pre2x4 * 4)
                out_name = "out_{}".format(i)
                pin = self.pre3x8_inst[pre_num].get_pin(out_name)
                x_offset = self.pre3x8_inst[pre_num].rx() + self.output_layer_pitch
                y_offset = self.pre3x8_inst[pre_num].by() + i * self.cell_height
                self.route_predecode_bus_inputs(predecode_name, pin, x_offset, y_offset)
            
    def route_bus_to_decoder(self):
        """
        Use the self.predec_groups to determine the connections to the decoder AND gates.
        Inputs of AND2/AND3 gates come from different groups.
        For example for these groups
        [ [0,1,2,3] ,[4,5,6,7], [8,9,10,11,12,13,14,15] ]
        the first AND3 inputs are connected to [0,4,8],
        second AND3 is connected to [0,4,9],
        ...
        and the 128th AND3 is connected to [3,7,15]
        """
        output_index = 0
            
        if (self.num_inputs == 4 or self.num_inputs == 5):
            for index_B in self.predec_groups[1]:
                for index_A in self.predec_groups[0]:
                    # FIXME: convert to connect_bus?
                    if (output_index < self.num_outputs):
                        predecode_name = "predecode_{}".format(index_A)
                        self.route_predecode_bus_outputs(predecode_name,
                                                         self.and_inst[output_index].get_pin("A"),
                                                         output_index)
                        predecode_name = "predecode_{}".format(index_B)
                        self.route_predecode_bus_outputs(predecode_name,
                                                         self.and_inst[output_index].get_pin("B"),
                                                         output_index)
                    output_index = output_index + 1

        elif (self.num_inputs > 5):
            for index_C in self.predec_groups[2]:
                for index_B in self.predec_groups[1]:
                    for index_A in self.predec_groups[0]:
                        # FIXME: convert to connect_bus?
                        if (output_index < self.num_outputs):
                            predecode_name = "predecode_{}".format(index_A)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("A"),
                                                             output_index)
                            predecode_name = "predecode_{}".format(index_B)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("B"),
                                                             output_index)
                            predecode_name = "predecode_{}".format(index_C)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("C"),
                                                             output_index)
                        output_index = output_index + 1

    def route_vdd_gnd(self):
        """
        Add a pin for each row of vdd/gnd which are
        must-connects next level up.
        """
                
        if OPTS.tech_name == "sky130":
            for n in ["vdd", "gnd"]:
                pins = self.and_inst[0].get_pins(n)
                for pin in pins:
                    self.add_rect(layer=pin.layer,
                                  offset=pin.ll() + vector(0, self.bus_space),
                                  width=pin.width(),
                                  height=self.height - 2 * self.bus_space)

                # This adds power vias at the top of each cell
                # (except the last to keep them inside the boundary)
                for i in self.and_inst[:-1]:
                    pins = i.get_pins(n)
                    for pin in pins:
                        self.add_power_pin(name=n,
                                           loc=pin.uc(),
                                           start_layer=pin.layer)
                        self.add_power_pin(name=n,
                                           loc=pin.uc(),
                                           start_layer=pin.layer)

                for i in self.pre2x4_inst + self.pre3x8_inst:
                    self.copy_layout_pin(i, n)
        else:
            # The vias will be placed at the right of the cells.
            xoffset = max(x.rx() for x in self.and_inst) + 0.5 * self.m1_space
            for row in range(0, self.num_outputs):
                for pin_name in ["vdd", "gnd"]:
                    # The nand and inv are the same height rows...
                    supply_pin = self.and_inst[row].get_pin(pin_name)
                    pin_pos = vector(xoffset, supply_pin.cy())
                    self.add_power_pin(name=pin_name,
                                       loc=pin_pos,
                                       start_layer=supply_pin.layer)

                # Copy the pins from the predecoders
                for pre in self.pre2x4_inst + self.pre3x8_inst:
                    for pin_name in ["vdd", "gnd"]:
                        self.copy_layout_pin(pre, pin_name)
        
    def route_predecode_bus_outputs(self, rail_name, pin, row):
        """
        Connect the routing rail to the given metal1 pin
        using a routing track at the given y_offset
        """

        pin_pos = pin.center()
        rail_pos = vector(self.predecode_bus[rail_name].cx(), pin_pos.y)
        self.add_path(self.input_layer, [rail_pos, pin_pos])
        
        self.add_via_stack_center(from_layer=self.bus_layer,
                                  to_layer=self.input_layer,
                                  offset=rail_pos,
                                  directions=self.bus_directions)
        
        self.add_via_stack_center(from_layer=pin.layer,
                                  to_layer=self.input_layer,
                                  offset=pin_pos,
                                  directions=("H", "H"))
        
    def route_predecode_bus_inputs(self, rail_name, pin, x_offset, y_offset):
        """
        Connect the routing rail to the given metal1 pin using a jog
        to the right of the cell at the given x_offset.
        """
        # This routes the pin up to the rail, basically, to avoid conflicts.
        # It would be fixed with a channel router.
        pin_pos = pin.rc()
        mid_point1 = vector(x_offset, pin_pos.y)
        mid_point2 = vector(x_offset, y_offset)
        rail_pos = vector(self.predecode_bus[rail_name].cx(), mid_point2.y)
        self.add_path(self.output_layer, [pin_pos, mid_point1, mid_point2, rail_pos])

        # pin_pos = pin.center()
        # rail_pos = vector(self.predecode_bus[rail_name].cx(), pin_pos.y)
        # self.add_path(self.output_layer, [pin_pos, rail_pos])
        self.add_via_stack_center(from_layer=pin.layer,
                                  to_layer=self.output_layer,
                                  offset=pin_pos)
        self.add_via_stack_center(from_layer=self.bus_layer,
                                  to_layer=self.output_layer,
                                  offset=rail_pos,
                                  directions=self.bus_directions)

    def input_load(self):
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
        else:
            pre = self.pre3_8
        return pre.input_load()
        
