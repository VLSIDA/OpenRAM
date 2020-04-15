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
from errors import drc_error
from tech import cell_properties


class hierarchical_decoder(design.design):
    """
    Dynamically generated hierarchical decoder.
    """
    def __init__(self, name, num_outputs):
        design.design.__init__(self, name)

        self.AND_FORMAT = "DEC_AND_{0}"
        
        self.pre2x4_inst = []
        self.pre3x8_inst = []

        b = factory.create(module_type="bitcell")
        try:
            self.cell_multiple = cell_properties.bitcell.decoder_bitcell_multiple
        except AttributeError:
            self.cell_multiple = 1
        # For debugging
        self.cell_height = self.cell_multiple * b.height
        
        self.num_outputs = num_outputs
        self.num_inputs = math.ceil(math.log(self.num_outputs, 2))
        (self.no_of_pre2x4, self.no_of_pre3x8)=self.determine_predecodes(self.num_inputs)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def find_decoder_height(self):
        """
        Dead code. This would dynamically determine the bitcell multiple,
        but I just decided to hard code it in the tech file if it is not 1
        because a DRC tool would be required even to run in front-end mode.
        """
        b = factory.create(module_type="bitcell")
    
        # Old behavior
        if OPTS.netlist_only:
            return (b.height, 1)

        # Search for the smallest multiple that works
        cell_multiple = 1
        while cell_multiple < 5:
            cell_height = cell_multiple * b.height
            # debug.info(2,"Trying mult = {0} height={1}".format(cell_multiple, cell_height))
            try:
                and3 = factory.create(module_type="pand3",
                                      height=cell_height)
            except drc_error:
                # debug.info(1, "Incrementing decoder height by 1 bitcell height {}".format(b.height))
                pass
            else:
                (drc_errors, lvs_errors) = and3.DRC_LVS(force_check=True)
                total_errors = drc_errors + lvs_errors
                if total_errors == 0:
                    debug.info(1, "Decoder height is multiple of {} bitcells.".format(cell_multiple))
                    return (cell_height, cell_multiple)

            cell_multiple += 1
            
        else:
            debug.error("Couldn't find a valid decoder height multiple.", -1)
        
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
        self.route_inputs()
        self.route_decoder_bus()
        self.route_vdd_gnd()
        self.offset_all_coordinates()
        self.add_boundary()
        self.DRC_LVS()
                
    def add_modules(self):
        self.inv = factory.create(module_type="pinv",
                                  height=self.cell_height)
        self.add_mod(self.inv)
        self.and2 = factory.create(module_type="pand2",
                                   height=self.cell_height)
        self.add_mod(self.and2)
        self.and3 = factory.create(module_type="pand3",
                                    height=self.cell_height)
        self.add_mod(self.and3)
        
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
        if self.no_of_pre3x8 > 0:
            self.predecoder_width = self.pre3_8.width
        else:
            self.predecoder_width = self.pre2_4.width
            
        self.predecoder_height = self.pre2_4.height * self.no_of_pre2x4 + self.pre3_8.height * self.no_of_pre3x8

        # We may have more than one bitcell per decoder row
        self.num_rows = math.ceil(self.num_outputs / self.cell_multiple)
        # We will place this many final decoders per row
        self.decoders_per_row = math.ceil(self.num_outputs / self.num_rows)
        
        # Calculates height and width of row-decoder
        if (self.num_inputs == 4 or self.num_inputs == 5):
            nand_width = self.and2.width
        else:
            nand_width = self.and3.width
        self.internal_routing_width = self.m2_pitch * (self.total_number_of_predecoder_outputs + 1)
        self.row_decoder_height = self.inv.height * self.num_rows

        self.input_routing_width = (self.num_inputs + 1) * self.m2_pitch
        # Calculates height and width of hierarchical decoder
        # Add extra pitch for good measure
        self.height = max(self.predecoder_height, self.row_decoder_height) + self.m3_pitch
        self.width = self.input_routing_width + self.predecoder_width \
                     + self.internal_routing_width \
                     + self.decoders_per_row * nand_width + self.inv.width
        
    def route_inputs(self):
        """ Create input bus for the predecoders """
        # inputs should be as high as the decoders
        input_height = self.no_of_pre2x4 * self.pre2_4.height + self.no_of_pre3x8 * self.pre3_8.height

        # Find the left-most predecoder
        min_x = 0
        if self.no_of_pre2x4 > 0:
            min_x = min(min_x, self.pre2x4_inst[0].lx())
        if self.no_of_pre3x8 > 0:
            min_x = min(min_x, self.pre3x8_inst[0].lx())
        input_offset=vector(min_x - self.input_routing_width, 0)

        input_bus_names = ["addr_{0}".format(i) for i in range(self.num_inputs)]
        self.input_bus = self.create_vertical_pin_bus(layer="m2",
                                                      pitch=self.m2_pitch,
                                                      offset=input_offset,
                                                      names=input_bus_names,
                                                      length=input_height)
        
        self.route_input_to_predecodes()

    def route_input_to_predecodes(self):
        """ Route the vertical input rail to the predecoders """
        for pre_num in range(self.no_of_pre2x4):
            for i in range(2):
                index = pre_num * 2 + i

                input_pos = self.input_bus["addr_{}".format(index)]

                in_name = "in_{}".format(i)
                decoder_pin = self.pre2x4_inst[pre_num].get_pin(in_name)

                # To prevent conflicts, we will offset each input connect so
                # that it aligns with the vdd/gnd rails
                decoder_offset = decoder_pin.bc() + vector(0, (i + 1) * self.inv.height)
                input_offset = input_pos.scale(1, 0) + decoder_offset.scale(0, 1)
                
                self.route_input_bus(decoder_offset, input_offset)
            
        for pre_num in range(self.no_of_pre3x8):
            for i in range(3):
                index = pre_num * 3 + i + self.no_of_pre2x4 * 2
                
                input_pos = self.input_bus["addr_{}".format(index)]

                in_name = "in_{}".format(i)
                decoder_pin = self.pre3x8_inst[pre_num].get_pin(in_name)

                # To prevent conflicts, we will offset each input connect so
                # that it aligns with the vdd/gnd rails
                decoder_offset = decoder_pin.bc() + vector(0, (i + 1) * self.inv.height)
                input_offset = input_pos.scale(1, 0) + decoder_offset.scale(0, 1)
                
                self.route_input_bus(decoder_offset, input_offset)

    def route_input_bus(self, input_offset, output_offset):
        """
        Route a vertical M2 coordinate to another
        vertical M2 coordinate to the predecode inputs
        """
        
        self.add_via_center(layers=self.m2_stack,
                            offset=input_offset)
        self.add_via_center(layers=self.m2_stack,
                            offset=output_offset)
        self.add_path(("m3"), [input_offset, output_offset])
    
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

    def place_pre2x4(self, num):
        """ Place 2x4 predecoder to the left of the origin """
        
        if (self.num_inputs == 2):
            base = vector(-self.pre2_4.width, 0)
        else:
            base= vector(-self.pre2_4.width, num * self.pre2_4.height)

        self.pre2x4_inst[num].place(base - vector(2 * self.m2_pitch, 0))
        
    def place_pre3x8(self, num):
        """ Place 3x8 predecoder to the left of the origin and above any 2x4 decoders """
        if (self.num_inputs == 3):
            offset = vector(-self.pre_3_8.width, 0)
        else:
            height = self.no_of_pre2x4 * self.pre2_4.height + num * self.pre3_8.height
            offset = vector(-self.pre3_8.width, height)

        self.pre3x8_inst[num].place(offset - vector(2 * self.m2_pitch, 0))

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
            self.route_decoder()

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

        for inst_index in range(self.num_outputs):
            row = math.floor(inst_index / self.decoders_per_row)
            dec = inst_index % self.decoders_per_row
            if ((row % 2) == 0):
                y_off = and_mod.height * row
                mirror = "R0"
            else:
                y_off = and_mod.height * (row + 1)
                mirror = "MX"

            x_off = self.internal_routing_width + dec * and_mod.width
            self.and_inst[inst_index].place(offset=vector(x_off, y_off),
                                            mirror=mirror)

    def route_decoder(self):
        """ Add the pins. """

        for output in range(self.num_outputs):
            z_pin = self.and_inst[output].get_pin("Z")
            self.add_layout_pin(text="decode_{0}".format(output),
                                layer="m1",
                                offset=z_pin.ll(),
                                width=z_pin.width(),
                                height=z_pin.height())
        
    def route_decoder_bus(self):
        """
        Creates vertical metal 2 bus to connect predecoder and decoder stages.
        """

        # This is not needed for inputs <4 since they have no pre/decode stages.
        if (self.num_inputs >= 4):
            # This leaves an offset for the predecoder output jogs
            input_bus_names = ["predecode_{0}".format(i) for i in range(self.total_number_of_predecoder_outputs)]
            self.predecode_bus = self.create_vertical_pin_bus(layer="m2",
                                                              pitch=self.m2_pitch,
                                                              offset=vector(0, 0),
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
                x_offset = self.pre2x4_inst[pre_num].rx() + self.m2_pitch
                self.route_predecode_bus_inputs(predecode_name, pin, x_offset)
            
        # FIXME: convert to connect_bus
        for pre_num in range(self.no_of_pre3x8):
            for i in range(8):
                predecode_name = "predecode_{}".format(pre_num * 8 + i + self.no_of_pre2x4 * 4)
                out_name = "out_{}".format(i)
                pin = self.pre3x8_inst[pre_num].get_pin(out_name)
                x_offset = self.pre3x8_inst[pre_num].rx() + self.m2_pitch
                self.route_predecode_bus_inputs(predecode_name, pin, x_offset)
            
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
                        row_index = math.floor(output_index / self.decoders_per_row)
                        row_remainder = (output_index % self.decoders_per_row)
                        row_offset = row_index * self.and_inst[0].height + (2 * row_remainder + 1) * self.m3_pitch
                        predecode_name = "predecode_{}".format(index_A)
                        self.route_predecode_bus_outputs(predecode_name,
                                                         self.and_inst[output_index].get_pin("A"),
                                                         row_offset)
                        predecode_name = "predecode_{}".format(index_B)
                        self.route_predecode_bus_outputs(predecode_name,
                                                         self.and_inst[output_index].get_pin("B"),
                                                         row_offset + self.m3_pitch)
                    output_index = output_index + 1

        elif (self.num_inputs > 5):
            for index_C in self.predec_groups[2]:
                for index_B in self.predec_groups[1]:
                    for index_A in self.predec_groups[0]:
                        # FIXME: convert to connect_bus?
                        if (output_index < self.num_outputs):
                            row_index = math.floor(output_index / self.decoders_per_row)
                            row_remainder = (output_index % self.decoders_per_row)
                            row_offset = row_index * self.and_inst[0].height + (3 * row_remainder + 1) * self.m3_pitch
                            predecode_name = "predecode_{}".format(index_A)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("A"),
                                                             row_offset)
                            predecode_name = "predecode_{}".format(index_B)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("B"),
                                                             row_offset + self.m3_pitch)
                            predecode_name = "predecode_{}".format(index_C)
                            self.route_predecode_bus_outputs(predecode_name,
                                                             self.and_inst[output_index].get_pin("C"),
                                                             row_offset + 2 * self.m3_pitch)
                        output_index = output_index + 1

    def route_vdd_gnd(self):
        """
        Add a pin for each row of vdd/gnd which are
        must-connects next level up.
        """

        # The vias will be placed at the right of the cells.
        xoffset = max(x.rx() for x in self.and_inst)
        for num in range(0, self.num_outputs):
            # Only add the power pin for the 1st in each row
            if num % self.decoders_per_row:
                continue
                
            for pin_name in ["vdd", "gnd"]:
                # The nand and inv are the same height rows...
                supply_pin = self.and_inst[num].get_pin(pin_name)
                pin_pos = vector(xoffset, supply_pin.cy())
                self.add_path("m1",
                              [supply_pin.lc(), vector(xoffset, supply_pin.cy())])
                self.add_power_pin(name=pin_name,
                                   loc=pin_pos)
                
        # Copy the pins from the predecoders
        for pre in self.pre2x4_inst + self.pre3x8_inst:
            self.copy_layout_pin(pre, "vdd")
            self.copy_layout_pin(pre, "gnd")
        
    def route_predecode_bus_outputs(self, rail_name, pin, y_offset):
        """
        Connect the routing rail to the given metal1 pin
        using a routing track at the given y_offset
        
        """
        pin_pos = pin.center()
        # If we have a single decoder per row, we can route on M1
        if self.decoders_per_row == 1:
            rail_pos = vector(self.predecode_bus[rail_name].x, pin_pos.y)
            self.add_path("m1", [rail_pos, pin_pos])
            self.add_via_center(layers=self.m1_stack,
                                offset=rail_pos)
        # If not, we must route over the decoder cells on M3
        else:
            rail_pos = vector(self.predecode_bus[rail_name].x, y_offset)
            mid_pos = vector(pin_pos.x, rail_pos.y)
            self.add_wire(self.m2_stack[::-1], [rail_pos, mid_pos, pin_pos])
            self.add_via_center(layers=self.m2_stack,
                                offset=rail_pos)
            self.add_via_center(layers=self.m1_stack,
                                offset=pin_pos)

    def route_predecode_bus_inputs(self, rail_name, pin, x_offset):
        """
        Connect the routing rail to the given metal1 pin using a jog
        to the right of the cell at the given x_offset.
        """
        # This routes the pin up to the rail, basically, to avoid conflicts.
        # It would be fixed with a channel router.
        pin_pos = pin.center()
        mid_point1 = vector(x_offset, pin_pos.y)
        mid_point2 = vector(x_offset, pin_pos.y + self.inv.height / 2)
        rail_pos = vector(self.predecode_bus[rail_name].x, mid_point2.y)
        self.add_wire(self.m1_stack, [pin_pos, mid_point1, mid_point2, rail_pos])
        self.add_via_center(layers=self.m1_stack,
                            offset=rail_pos)

    def input_load(self):
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
        else:
            pre = self.pre3_8
        return pre.input_load()
        
