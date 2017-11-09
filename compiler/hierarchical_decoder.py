from tech import drc
import debug
import design
from math import log
from math import sqrt
import math
from contact import contact 
from nand_2 import nand_2
from nand_3 import nand_3 
from pinv import pinv 
from hierarchical_predecode2x4 import hierarchical_predecode2x4 as pre2x4
from hierarchical_predecode3x8 import hierarchical_predecode3x8 as pre3x8
from vector import vector
from globals import OPTS

class hierarchical_decoder(design.design):
    """
    Dynamically generated hierarchical decoder.
    """

    def __init__(self, rows):
        design.design.__init__(self, "hierarchical_decoder_{0}rows".format(rows))

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_height = self.mod_bitcell.height

        self.pre2x4_inst = []
        self.pre3x8_inst = []

        self.rows = rows
        self.num_inputs = int(math.log(self.rows, 2))
        (self.no_of_pre2x4,self.no_of_pre3x8)=self.determine_predecodes(self.num_inputs)
        
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        self.add_modules()
        self.setup_layout_constants()
        self.add_pins()
        self.create_pre_decoder()
        self.create_row_decoder()
        self.create_vertical_rail()
        self.route_vdd_gnd()
        # We only need to call the offset_all_coordinate function when there
        # are vertical metal rails.
        #if (self.num_inputs >= 4):
        #    self.offset_all_coordinates()

    def add_modules(self):
        self.inv = pinv()
        self.add_mod(self.inv)
        self.nand2 = nand_2()
        self.add_mod(self.nand2)
        self.nand3 = nand_3()
        self.add_mod(self.nand3)

        # CREATION OF PRE-DECODER
        self.pre2_4 = pre2x4()
        self.add_mod(self.pre2_4)
        self.pre3_8 = pre3x8()
        self.add_mod(self.pre3_8)

    def determine_predecodes(self,num_inputs):
        """Determines the number of 2:4 pre-decoder and 3:8 pre-decoder
        needed based on the number of inputs"""
        if (num_inputs == 2):
            return (1,0)
        elif (num_inputs == 3):
            return(0,1)
        elif (num_inputs == 4):
            return(2,0)
        elif (num_inputs == 5):
            return(1,1)
        elif (num_inputs == 6):
            return(3,0)
        elif (num_inputs == 7):
            return(2,1)
        elif (num_inputs == 8):
            return(1,2)
        elif (num_inputs == 9):
            return(0,3)
        else:
            debug.error("Invalid number of inputs for hierarchical decoder",-1)

    def setup_layout_constants(self):
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        # Vertical metal rail gap definition
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height - self.m1m2_via.contact_width) / 2
        self.metal2_spacing = self.metal2_extend_contact  + drc["metal2_to_metal2"]
        self.metal2_pitch = self.metal2_spacing + drc["minwidth_metal2"]
        self.via_shift = (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) / 2

        self.predec_groups = []  # This array is a 2D array.

        # Distributing vertical rails to different groups. One group belongs to one pre-decoder.
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

        self.calculate_dimensions()

        
    def add_pins(self):
        """ Add the module pins """
        
        for i in range(self.num_inputs):
            self.add_pin("A[{0}]".format(i))

        for j in range(self.rows):
            self.add_pin("decode[{0}]".format(j))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def calculate_dimensions(self):
        """ Calculate the overal dimensions of the hierarchical decoder """

        # If we have 4 or fewer rows, the predecoder is the decoder itself
        if self.num_inputs>=4:
            self.total_number_of_predecoder_outputs = 4*self.no_of_pre2x4 + 8*self.no_of_pre3x8
        else:
            self.total_number_of_predecoder_outputs = 0            
            debug.error("Not enough rows for a hierarchical decoder. Non-hierarchical not supported yet.",-1)

        # Calculates height and width of pre-decoder,
        if(self.no_of_pre3x8 > 0):
            self.predecoder_width = self.pre3_8.width 
        else:
            self.predecoder_width = self.pre2_4.width
        self.predecoder_height = self.pre2_4.height*self.no_of_pre2x4 + self.pre3_8.height*self.no_of_pre3x8

        # Calculates height and width of row-decoder 
        if (self.num_inputs == 4 or self.num_inputs == 5):
            nand_width = self.nand2.width
        else:
            nand_width = self.nand3.width 
        self.routing_width = self.metal2_pitch*self.total_number_of_predecoder_outputs
        self.row_decoder_width = nand_width  + self.routing_width + self.inv.width
        self.row_decoder_height = self.inv.height * self.rows

        # Calculates height and width of hierarchical decoder 
        self.height = self.predecoder_height + self.row_decoder_height
        self.width = self.predecoder_width + self.routing_width

    def create_pre_decoder(self):
        """ Creates pre-decoder and places labels input address [A] """
        
        for i in range(self.no_of_pre2x4):
            self.add_pre2x4(i)
            
        for i in range(self.no_of_pre3x8):
            self.add_pre3x8(i)

    def add_pre2x4(self,num):
        """ Add a 2x4 predecoder """
        
        if (self.num_inputs == 2):
            base = vector(self.routing_width,0)
            mirror = "RO"
            index_off1 = index_off2 = 0
        else:
            base= vector(self.routing_width+self.pre2_4.width, num * self.pre2_4.height)
            mirror = "MY"
            index_off1 = num * 2
            index_off2 = num * 4

        pins = []
        for input_index in range(2):
            pins.append("A[{0}]".format(input_index + index_off1))
        for output_index in range(4):
            pins.append("out[{0}]".format(output_index + index_off2))
        pins.extend(["vdd", "gnd"])

        self.pre2x4_inst.append(self.add_inst(name="pre[{0}]".format(num),
                                                 mod=self.pre2_4,
                                                 offset=base,
                                                 mirror=mirror))
        self.connect_inst(pins)

        self.add_pre2x4_pins(num)

                            

    def add_pre2x4_pins(self,num):
        """ Add the input pins to the 2x4 predecoder """

        for i in range(2):
            pin = self.pre2x4_inst[num].get_pin("in[{}]".format(i))
            pin_offset = pin.ll()
            
            pin = self.pre2_4.get_pin("in[{}]".format(i))
            self.add_layout_pin(text="A[{0}]".format(i + 2*num ),
                                layer="metal2", 
                                offset=pin_offset,
                                width=pin.width(),
                                height=pin.height())

        
    def add_pre3x8(self,num):
        """ Add 3x8 numbered predecoder """
        if (self.num_inputs == 3):
            offset = vector(self.routing_width,0)
            mirror ="R0"
        else:
            height = self.no_of_pre2x4*self.pre2_4.height + num*self.pre3_8.height
            offset = vector(self.routing_width+self.pre3_8.width, height)
            mirror="MY"

        # If we had 2x4 predecodes, those are used as the lower
        # decode output bits
        in_index_offset = num * 3 + self.no_of_pre2x4 * 2
        out_index_offset = num * 8 + self.no_of_pre2x4 * 4

        pins = []
        for input_index in range(3):
            pins.append("A[{0}]".format(input_index + in_index_offset))
        for output_index in range(8):
            pins.append("out[{0}]".format(output_index + out_index_offset))
        pins.extend(["vdd", "gnd"])

        self.pre3x8_inst.append(self.add_inst(name="pre3x8[{0}]".format(num), 
                                              mod=self.pre3_8,
                                              offset=offset,
                                              mirror=mirror))
        self.connect_inst(pins)

        # The 3x8 predecoders will be stacked, so use yoffset
        self.add_pre3x8_pins(num,offset)

    def add_pre3x8_pins(self,num,offset):
        """ Add the input pins to the 3x8 predecoder at the given offset """

        for i in range(3):            
            pin = self.pre3x8_inst[num].get_pin("in[{}]".format(i))
            pin_offset = pin.ll()
            self.add_layout_pin(text="A[{0}]".format(i + 3*num + 2*self.no_of_pre2x4),
                                layer="metal2", 
                                offset=pin_offset,
                                width=pin.width(),
                                height=pin.height())



    def create_row_decoder(self):
        """ Create the row-decoder by placing NAND2/NAND3 and Inverters
        and add the primary decoder output pins. """
        if (self.num_inputs >= 4):
            self.add_decoder_nand_array()
            self.add_decoder_inv_array_and_pins()

    def add_decoder_nand_array(self):
        """ Add a column of NAND gates for final decode """
        
        # Row Decoder NAND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            self.add_nand_array(nand_mod=self.nand2)
            # FIXME: Can we convert this to the connect_inst with checks?
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    pins =["out[{0}]".format(i),
                           "out[{0}]".format(j + len(self.predec_groups[0])),
                           "Z[{0}]".format(len(self.predec_groups[1])*i + j),
                           "vdd", "gnd"]
                    self.connect_inst(args=pins, check=False)

        # Row Decoder NAND GATE array for address inputs >5.
        elif (self.num_inputs > 5):
            self.add_nand_array(nand_mod=self.nand3,
                                correct=drc["minwidth_metal1"])
            # This will not check that the inst connections match.
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    for k in range(len(self.predec_groups[2])):
                        Z_index = len(self.predec_groups[1])*len(self.predec_groups[2]) * i \
                                  + len(self.predec_groups[2])*j + k
                        pins = ["out[{0}]".format(i),
                                "out[{0}]".format(j + len(self.predec_groups[0])),
                                "out[{0}]".format(k + len(self.predec_groups[0]) + len(self.predec_groups[1])),
                                "Z[{0}]".format(Z_index),
                                "vdd", "gnd"]
                        self.connect_inst(args=pins, check=False)

    def add_nand_array(self, nand_mod, correct=0):
        """ Add a column of NAND gates for the decoder above the predecoders."""
        
        z_pin = nand_mod.get_pin("Z")
        a_pin = self.inv.get_pin("A")
        rect_height = z_pin.uy()-a_pin.by()
        
        for row in range(self.rows):
            name = "DEC_NAND[{0}]".format(row)
            if ((row % 2) == 0):
                y_off = self.predecoder_height + nand_mod.height*row
                y_dir = 1
                mirror = "R0"
                rect_offset = vector(self.routing_width + nand_mod.width, y_off + z_pin.uy() - rect_height)
                
            else:
                y_off = self.predecoder_height + nand_mod.height*(row + 1)
                y_dir = -1
                mirror = "MX"
                rect_offset =vector(self.routing_width + nand_mod.width, y_off - z_pin.uy())

            self.add_inst(name=name,
                          mod=nand_mod,
                          offset=[self.routing_width, y_off],
                          mirror=mirror)

            self.add_rect(layer="metal1",
                          offset=rect_offset,
                          width=drc["minwidth_metal1"],
                          height=rect_height)
            

    def add_decoder_inv_array_and_pins(self):
        """Add a column of INV gates for the decoder above the predecoders
        and to the right of the NAND decoders."""
        
        z_pin = self.inv.get_pin("Z")
        
        if (self.num_inputs == 4 or self.num_inputs == 5):
            x_off = self.routing_width + self.nand2.width
        else:
            x_off = self.routing_width + self.nand3.width
            
        for row in range(self.rows):
            name = "DEC_INV_[{0}]".format(row)
            if (row % 2 == 0):
                inv_row_height = self.inv.height * row
                mirror = "R0"
                y_dir = 1
            else:
                inv_row_height = self.inv.height * (row + 1)
                mirror = "MX"
                y_dir = -1
            y_off = self.predecoder_height + inv_row_height
            offset = vector(x_off,y_off)
            
            self.add_inst(name=name,
                          mod=self.inv,
                          offset=offset,
                          mirror=mirror)
            # This will not check that the inst connections match.
            self.connect_inst(args=["Z[{0}]".format(row),
                                    "decode[{0}]".format(row),
                                    "vdd", "gnd"],
                              check=False)

            self.add_layout_pin(text="decode[{0}]".format(row),
                                layer="metal1",
                                offset=offset+z_pin.ll().scale(1,y_dir),
                                width=z_pin.width(),
                                height=y_dir*z_pin.height())



    def create_vertical_rail(self):
        """ Creates vertical metal 2 rails to connect predecoder and decoder stages."""

        # This is not needed for inputs <4 since they have no pre/decode stages.
        if (self.num_inputs >= 4):
            # Array for saving the X offsets of the vertical rails. These rail
            # offsets are accessed with indices.
            self.rail_x_offsets = []
            for i in range(self.total_number_of_predecoder_outputs):
                # The offsets go into the negative x direction
                # assuming the predecodes are placed at (self.routing_width,0)
                x_offset = self.metal2_pitch * i
                self.rail_x_offsets.append(x_offset)
                self.add_rect(layer="metal2",
                              offset=vector(x_offset,0),
                              width=drc["minwidth_metal2"],
                              height=self.height)

            self.connect_rails_to_predecodes()
            self.connect_rails_to_decoder()

    def connect_rails_to_predecodes(self):
        """ Iterates through all of the predecodes and connects to the rails including the offsets """

        for i in range(self.no_of_pre2x4):
            self.connect_rails_to_pre2x4(i)
            
        for i in range(self.no_of_pre3x8):
            self.connect_rails_to_pre3x8(i)


    def connect_rails_to_pre2x4(self, predecode_num):
        """ Connects the 2x4 predecoder outputs to the vertical rails """
        
        z_pin = self.inv.get_pin("Z")
        pin = z_pin.ll()
        for i in range(4):
            index = predecode_num * 4 + i
            current_inv_height = predecode_num*self.pre2_4.height + i*self.inv.height

            if (i % 2 == 0):
                pin_y = pin.y
            else:
                pin_y = self.inv.height - drc["minwidth_metal1"] - pin.y

            self.connect_rail(vector(self.rail_x_offsets[index], current_inv_height + pin_y))
                              
    def connect_rails_to_pre3x8(self, predecode_num):
        """ Connects the 3x8 predecoder outputs to the vertical rails """

        z_pin = self.inv.get_pin("Z")
        pin = z_pin.ll()
        for i in range(8):
            index = predecode_num * 8 + i + self.no_of_pre2x4 * 4
            current_inv_height = predecode_num*self.pre3_8.height \
                                 + i*self.inv.height \
                                 + self.no_of_pre2x4*self.pre2_4.height

            if (i % 2 == 0):
                pin_y = pin.y
            else:
                pin_y = self.inv.height - drc["minwidth_metal1"] - pin.y
            
            self.connect_rail(vector(self.rail_x_offsets[index], current_inv_height + pin_y))

    def connect_rails_to_decoder(self):
        """ Use the self.predec_groups to determine the connections to the decoder NAND gates.
        Inputs of NAND2/NAND3 gates come from different groups.
        For example for these groups [ [0,1,2,3] ,[4,5,6,7],
        [8,9,10,11,12,13,14,15] ] the first NAND3 inputs are connected to
        [0,4,8] and second NAND3 is connected to [0,4,9]  ........... and the
        128th NAND3 is connected to [3,7,15]
        """
        row_index = 0
        if (self.num_inputs == 4 or self.num_inputs == 5):
            a_pin = self.nand2.get_pin("A")
            b_pin = self.nand2.get_pin("B")
        
            for index_A in self.predec_groups[0]:
                for index_B in self.predec_groups[1]:

                    current_inv_height = self.predecoder_height + row_index*self.inv.height
                    if (row_index % 2 == 0):
                        yoffset_A = current_inv_height + a_pin.by()
                        yoffset_B = current_inv_height + b_pin.by()

                    else:
                        base = current_inv_height + self.inv.height - drc["minwidth_metal1"]
                        yoffset_A = base - a_pin.by()
                        yoffset_B = base - b_pin.by()

                    row_index = row_index + 1
                    self.connect_rail(vector(self.rail_x_offsets[index_A], yoffset_A))
                    self.connect_rail(vector(self.rail_x_offsets[index_B], yoffset_B))

        elif (self.num_inputs > 5):
            a_pin = self.nand3.get_pin("A")
            b_pin = self.nand3.get_pin("B")
            c_pin = self.nand3.get_pin("C")
            
            for index_A in self.predec_groups[0]:
                for index_B in self.predec_groups[1]:
                    for index_C in self.predec_groups[2]:

                        current_inv_height = self.predecoder_height + row_index*self.inv.height

                        if (row_index % 2 == 0):
                            yoffset_A = current_inv_height + a_pin.by()
                            yoffset_B = current_inv_height + b_pin.by()
                            yoffset_C = current_inv_height + c_pin.by()
                        else:
                            base = current_inv_height + self.inv.height - drc["minwidth_metal1"]
                            yoffset_A = base - a_pin.by()
                            yoffset_B = base - b_pin.by()
                            yoffset_C = base - c_pin.by()

                        row_index = row_index + 1

                        self.connect_rail(vector(self.rail_x_offsets[index_A], yoffset_A))
                        self.connect_rail(vector(self.rail_x_offsets[index_B], yoffset_B))
                        self.connect_rail(vector(self.rail_x_offsets[index_C], yoffset_C))

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        for num in range(0,self.total_number_of_predecoder_outputs + self.rows):
            # this will result in duplicate polygons for rails, but who cares
            
            # use the inverter offset even though it will be the nand's too
            (gate_offset, y_dir) = self.get_gate_offset(0, self.inv.height, num)
            # route vdd
            vdd_offset = gate_offset + self.inv.get_pin("vdd").ll().scale(1,y_dir) 
            self.add_layout_pin(text="vdd",
                                layer="metal1",
                                offset=vdd_offset,
                                width=self.width,
                                height=drc["minwidth_metal1"])

            # route gnd
            gnd_offset = gate_offset+self.inv.get_pin("gnd").ll().scale(1,y_dir)
            self.add_layout_pin(text="gnd",
                                layer="metal1",
                                offset=gnd_offset,
                                width=self.width,
                                height=drc["minwidth_metal1"])
        

    def connect_rail(self, offset,contact_yoffset=0):
        """ Adds a via at location and extends to self.routing_width """
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=self.routing_width-offset.x,
                      height=drc["minwidth_metal1"])

        if contact_yoffset!=0:
            yoffset = contact_yoffset

        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset + vector(self.metal2_spacing,-self.via_shift),
                     rotate=90)

    def analytical_delay(self, slew, load = 0.0):
        # A -> out
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
            nand = self.nand2
        else:
            pre = self.pre3_8
            nand = self.nand3
        a_t_out_delay = pre.analytical_delay(slew=slew,load = nand.input_load())

        # out -> z
        out_t_z_delay = nand.analytical_delay(slew= a_t_out_delay.slew,
                                  load = self.inv.input_load())
        result = a_t_out_delay + out_t_z_delay

        # Z -> decode_out
        z_t_decodeout_delay = self.inv.analytical_delay(slew = out_t_z_delay.slew , load = load)
        result = result + z_t_decodeout_delay
        return result

    def input_load(self):
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
        else:
            pre = self.pre3_8
        return pre.input_load()
