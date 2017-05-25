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

    def __init__(self, nand2_nmos_width, nand3_nmos_width, rows):
        design.design.__init__(self, "hierarchical_decoder")

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_height = self.mod_bitcell.chars["height"]

        self.rows = rows
        self.nand2_nmos_width = nand2_nmos_width
        self.nand3_nmos_width = nand3_nmos_width
        self.num_inputs = int(math.log(self.rows, 2))
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        self.add_modules()
        self.setup_layout_offsets()
        self.setup_layout_constants()
        self.create_decoder()
        # We only need to call the offset_all_coordinate function when there
        # are vertical metal rails.
        if (self.num_inputs >= 4):
            self.offset_all_coordinates()

    def create_decoder(self):
        self.add_pins()
        self.dimensions_hierarchy_decoder()
        self.create_pre_decoder()
        self.create_row_decoder()
        self.create_vertical_rail()

    def add_modules(self):
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        # Vertical metal rail gap definition
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height - self.m1m2_via.contact_width) / 2
        self.gap_between_rails = self.metal2_extend_contact  + drc["metal2_to_metal2"]
        self.gap_between_rail_offset = self.gap_between_rails + drc["minwidth_metal2"]
        self.via_shift = (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) / 2
        # used to shift contact when connecting to NAND3 C pin down
        self.contact_shift = (self.m1m2_via.first_layer_width - self.m1m2_via.contact_width) / 2

        self.inv = pinv(name="pinverter",
                        nmos_width=drc["minwidth_tx"],
                        beta=2,
                        height=self.bitcell_height)
        self.add_mod(self.inv)
        self.nand2 = nand_2(name="pnand2",
                            nmos_width=self.nand2_nmos_width,
                            height=self.bitcell_height)
        self.add_mod(self.nand2)
        self.nand3 = nand_3(name="pnand3",
                            nmos_width=self.nand3_nmos_width,
                            height=self.bitcell_height)
        self.add_mod(self.nand3)

        # CREATION OF PRE-DECODER
        self.pre2_4 = pre2x4(self.nand2_nmos_width,
                             "pre2x4")
        self.add_mod(self.pre2_4)
        self.pre3_8 = pre3x8(self.nand3_nmos_width,
                             "pre3x8")
        self.add_mod(self.pre3_8)

    def setup_layout_offsets(self):
        self.vdd_positions = []
        self.gnd_positions = []
        self.decode_out_positions = []
        self.A_positions = []

        self.pre_decoder_vdd_positions = []
        self.pre_decoder_gnd_positions = []

    def determine_predecodes(self,num_inputs):
        # Determines the number of 2:4 pre-decoder and 3:8 pre-decoder needed
        # based on the number of inputs
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
            debug.error("Invalid number of inputs for hierarchical decoder")

    def setup_layout_constants(self):
        (p2x4,p3x8)=self.determine_predecodes(self.num_inputs)
        self.no_of_pre2x4=p2x4
        self.no_of_pre3x8=p3x8

        # Stromg the index of the vertical rails in different groups. These
        # vertical lines is used to connect pre-decoder to row-decoder
        self.predecoder_output_groups = []  # This array is a 2D array.
        self.group_sizes = []

        # Distributing vertical rails to different groups. One group belongs to one pre-decoder.
        # For example, for two 2:4 pre-decoder and one 3:8 pre-decoder, we will
        # have total 16 output lines out of these 3 pre-decoders and they will
        # be distributed as [ [0,1,2,3] ,[4,5,6,7], [8,9,10,11,12,13,14,15] ]
        # in self.predecoder_output_groups
        index = 0
        for i in range(self.no_of_pre2x4):
            lines = []
            for j in range(4):
                lines.append(index)
                index = index + 1
            self.predecoder_output_groups.append(lines)
            self.group_sizes.append(4)

        for i in range(self.no_of_pre3x8):
            lines = []
            for j in range(8):
                lines.append(index)
                index = index + 1
            self.predecoder_output_groups.append(lines)
            self.group_sizes.append(8)

    def add_pins(self):
        for i in range(self.num_inputs):
            self.add_pin("A[{0}]".format(i))

        if(self.num_inputs >= 4):
            for j in range(self.rows):
                self.add_pin("decode_out[{0}]".format(j))
        else:
            for j in range(self.rows):
                self.add_pin("out[{0}]".format(j))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def dimensions_hierarchy_decoder(self):
        self.total_number_of_predecoder_outputs = (4 * self.no_of_pre2x4 
                                                       + 8 * self.no_of_pre3x8) 

        # Calculates height and width of pre-decoder,
        if(self.no_of_pre3x8 > 0):
            self.predecoder_width = self.pre3_8.width 
        else:
            self.predecoder_width = self.pre2_4.width
        self.predecoder_height = (self.pre2_4.height * self.no_of_pre2x4 
                                      + self.pre3_8.height * self.no_of_pre3x8)

        # Calculates height and width of row-decoder 
        if (self.num_inputs == 4 or self.num_inputs == 5):
            nand_width = self.nand2.width
        else:
            nand_width = self.nand3.width 
        total_gap = (self.gap_between_rail_offset 
                        * self.total_number_of_predecoder_outputs)
        self.row_decoder_width = (nand_width  + total_gap
                                      + self.inv.width) 
        self.row_decoder_height = self.inv.height * self.rows

        # Calculates height and width of hierarchical decoder 
        self.height = (self.predecoder_height 
                           + self.row_decoder_height)
        self.width = self.predecoder_width + total_gap

    def create_pre_decoder(self):
        """ Creates pre-decoder and places labels input address [A] """
        for i in range(self.no_of_pre2x4):
            self.add_pre2x4(i)
            self.add_lables_pre2x4(i)
        for j in range(self.no_of_pre3x8):
            pre3x8_yoffset=self.add_pre3x8(j)
            self.add_lables_pre3x8(j,pre3x8_yoffset)

    def add_pre2x4(self,i):
        if (self.num_inputs == 2):
            base = vector(0,0)
            mod_dir = vector(1,1)
            mirror = "RO"
            index_off1 = index_off2 = 0
        else:
            base= vector(self.pre2_4.width, i * self.pre2_4.height)
            mod_dir = vector(-1,1)
            mirror = "MY"
            index_off1 = i * 2
            index_off2 = i * 4

        pins = []
        for input_index in range(2):
            pins.append("A[{0}]".format(input_index + index_off1))
        for output_index in range(4):
            pins.append("out[{0}]".format(output_index + index_off2))
        pins = pins + ["vdd", "gnd"]

        self.add_inst(name="pre[{0}]".format(i),
                      mod=self.pre2_4,
                      offset=base,
                      mirror=mirror)
        self.connect_inst(pins)

        vdd_offset = base + self.pre2_4.vdd_position.scale(mod_dir)
        self.pre_decoder_vdd_positions.append(vdd_offset)
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=vdd_offset)

        gnd_offset = base + self.pre2_4.gnd_position.scale(mod_dir)
        self.pre_decoder_gnd_positions.append(gnd_offset)
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=gnd_offset)

    def add_lables_pre2x4(self,i):
        pre2_4_base = i * self.pre2_4.height
        # ADDING LABELS FOR INPUT SIDE OF THE 2:4 PRE-DECODER
        if (self.num_inputs == 2):
            xoffset = self.pre2_4.x_off_inv_1
        else:
            xoffset = self.pre2_4.width - self.pre2_4.x_off_inv_1
        for inv_2x4 in range(2):
            if (inv_2x4 % 2 == 0):
                pin_y = self.inv.A_position.y
            else:
                pin_y = (self.inv.height - self.inv.A_position.y
                             - drc["metal1_to_metal1"])  
            yoffset = pre2_4_base + inv_2x4 * self.inv.height + pin_y
            self.add_label(text="A[{0}]".format(inv_2x4 + i * 2),
                           layer="metal1", 
                           offset=[xoffset, yoffset])
            self.A_positions.append(vector(xoffset, yoffset))

        # ADDING LABELS FOR OUTPUT SIDE OF THE 2:4 PRE-DECODER
        for inv_2x4 in range(4):
            if (self.num_inputs == 2):
                xoffset = self.pre2_4.x_off_inv_2 + self.inv.Z_position.x
            else:
                xoffset = 0
            if (inv_2x4 % 2 == 0):
                pin_y =  self.inv.Z_position.y
            else:
                pin_y = self.inv.height - self.inv.Z_position.y
            yoffset = pre2_4_base + inv_2x4 * self.inv.height + pin_y   
            self.add_label(text="out[{0}]".format(inv_2x4 + i * 4),
                           layer="metal1",
                           offset=[xoffset, yoffset])

    def add_pre3x8(self,j):
        if (self.num_inputs == 3):
            offset = vector(0,0)
            mirror ="R0"
            mod_dir = vector(1,1)
            index_off1 = index_off2 = 0
        else:
            offset = vector(self.pre3_8.width,
                            self.no_of_pre2x4 * self.pre2_4.height
                                + j * self.pre3_8.height)
            mirror="MY"
            mod_dir = vector(-1,1)
            index_off1 = j * 3 + self.no_of_pre2x4 * 2
            index_off2 = j * 8 + self.no_of_pre2x4 * 4

        pins = []
        for input_index in range(3):
            pins.append("A[{0}]".format(input_index + index_off1))
        for output_index in range(8):
            pins.append("out[{0}]".format(output_index + index_off2))
        pins = pins + ["vdd", "gnd"]

        self.add_inst(name="pre3x8[{0}]".format(j), 
                      mod=self.pre3_8,
                      offset=offset,
                      mirror=mirror)
        self.connect_inst(pins)

        vdd_offset = offset + self.pre3_8.vdd_position.scale(mod_dir)
        self.pre_decoder_vdd_positions.append(vdd_offset)
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=vdd_offset)

        gnd_offset = offset + self.pre3_8.gnd_position.scale(mod_dir)
        self.pre_decoder_gnd_positions.append(gnd_offset)
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=gnd_offset)
        return offset.y

    def add_lables_pre3x8(self,j,pre3x8_yoffset):
        # ADDING LABELS FOR INPUT SIDE OF THE 3:8 PRE-DECODER
        if (self.num_inputs == 3):
            xoffset = self.pre3_8.x_off_inv_1
        else:
            xoffset = self.pre3_8.width - self.pre3_8.x_off_inv_1
        for inv_3x8 in range(3):
            if (inv_3x8 % 2 == 0):
                pin_y = self.inv.A_position.y
            else:
                pin_y = (self.inv.height - self.inv.Z_position.y 
                          -drc["minwidth_metal1"])
            yoffset = pre3x8_yoffset + inv_3x8 * (self.inv.height) + pin_y
            A_index = self.no_of_pre2x4 * 2 + inv_3x8 + j * 3
            self.add_label(text="A[{0}]".format(A_index),
                           layer="metal1",
                           offset=[xoffset, yoffset])
            self.A_positions.append(vector(xoffset, yoffset))

        # ADDING LABELS FOR OUTPUT SIDE OF THE 3:8 PRE-DECODER
        for inv_3x8 in range(8):
            if (self.num_inputs == 3):
                xoffset = self.pre3_8.x_off_inv_2 + self.inv.Z_position.x
            else:
                xoffset = 0

            if (inv_3x8 % 2 == 0):
                pin_y = self.inv.Z_position.y
            else:
                pin_y = self.inv.height - self.inv.Z_position.y
            yoffset = pre3x8_yoffset + inv_3x8 * self.inv.height + pin_y
            out_index = self.no_of_pre2x4 * 4 + inv_3x8 + j * 8
            self.add_label(text="out[{0}]".format(out_index),
                           layer="metal1",
                           offset=[xoffset,  yoffset])

    def create_row_decoder(self):
        # Create the row-decoder using NAND2/NAND3 and Inverter and places the
        # output labels [out/decode_out]
        if (self.num_inputs >= 4):
            self.add_decoder_nand_array_and_labels()
            self.add_decoder_inv_array_and_labels()

    def add_decoder_nand_array_and_labels(self):
        # Row Decoder NAND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            nand = self.nand2
            correct = 0
            nand_name ="NAND2"
            self.add_nand_array(nand,correct,nand_name)
            # FIXME: Can we convert this to the connect_inst with checks?
            for i in range(self.group_sizes[0]):
                for j in range(self.group_sizes[1]):
                    pins =["out[{0}]".format(i),
                           "out[{0}]".format(j + self.group_sizes[0]),
                           "Z[{0}]".format(self.group_sizes[1] * i + j),
                           "vdd", "gnd"]
                    self.connect_inst(args=pins, check=False)

        # Row Decoder NAND GATE array for address inputs >5.
        elif (self.num_inputs > 5):
            nand = self.nand3
            correct = drc["minwidth_metal1"]
            nand_name ="NAND3"
            self.add_nand_array(nand,correct,nand_name)
            # This will not check that the inst connections match.
            for i in range(self.group_sizes[0]):
                for j in range(self.group_sizes[1]):
                    for k in range(self.group_sizes[2]):
                        Z_index = (self.group_sizes[1] * self.group_sizes[2]* i 
                                       + self.group_sizes[2] * j + k)
                        pins = ["out[{0}]".format(i),
                                "out[{0}]".format(j + self.group_sizes[0]),
                                "out[{0}]".format(k + self.group_sizes[0] + self.group_sizes[1]),
                                "Z[{0}]".format(Z_index),
                                "vdd", "gnd"]
                        self.connect_inst(args=pins, check=False)

    def add_nand_array(self,nand,correct,nand_name):
        for row in range(self.rows):
            name = nand_name+"_[{0}]".format(row)
            if ((row % 2) == 0):
                y_off = self.predecoder_height + (nand.height) * (row)
                y_dir = 1
                mirror = "R0"
            else:
                y_off = self.predecoder_height + (nand.height) * (row + 1)
                y_dir = - 1
                mirror = "MX"

            self.add_inst(name=name,
                          mod=nand,
                          offset=[0, y_off],
                          mirror=mirror)
            self.add_rect(layer="metal1",
                          offset=[nand.width - correct,
                                  y_off + y_dir * (nand.Z_position.y-correct)],
                          width=drc["minwidth_metal1"],
                          height=y_dir * drc["minwidth_metal1"])

    def add_decoder_inv_array_and_labels(self):
        # Row Decoder INVERTER array insts.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            x_off = self.nand2.width
        else:
            x_off = self.nand3.width
        for row in range(self.rows):
            name = "INVERTER_[{0}]".format(row)
            if ((row % 2) == 0):
                inv_row_height = self.inv.height * row
                mirror = "R0"
            else:
                inv_row_height = self.inv.height * (row + 1)
                mirror = "MX"
            y_off = self.predecoder_height + inv_row_height

            self.add_inst(name=name,
                          mod=self.inv,
                          offset=[x_off, y_off],
                          mirror=mirror)
            # This will not check that the inst connections match.
            self.connect_inst(args=["Z[{0}]".format(row),
                                    "decode_out[{0}]".format(row),
                                    "vdd", "gnd"],
                              check=False)

        # add vdd and gnd label
        for row in range(self.rows):
            if ((row % 2) == 0):
                offset = vector(0, self.predecoder_height + row*(self.inv.height))
                vdd_offset = offset + self.inv.vdd_position.scale(0,1)
                gnd_offset = offset + self.inv.gnd_position.scale(0,1)
            else:
                offset = vector(0, self.predecoder_height + (row+1)*(self.inv.height))
                vdd_offset = offset + self.inv.vdd_position.scale(0, -1)
                gnd_offset = offset + self.inv.gnd_position.scale(0, -1)
            self.vdd_positions.append(vdd_offset)
            self.add_label(text="vdd", 
                           layer="metal1",
                           offset=vdd_offset)
            self.gnd_positions.append(gnd_offset)
            self.add_label(text="gnd",
                           layer="metal1",
                           offset=gnd_offset)

        # add output label for Row Decoder INVERTER array.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            x_off = self.nand2.width + self.inv.Z_position.x
        else:
            x_off = self.nand3.width  + self.inv.Z_position.x

        for row in range(self.rows):
            if ((row % 2) == 0):
                pin_y = row * self.inv.height + self.inv.Z_position.y
            else:
                pin_y = (row+1)*self.inv.height - self.inv.Z_position.y
            y_off = self.predecoder_height + pin_y 

            self.add_label(text="decode_out[{0}]".format(row),
                           layer="metal1",
                           offset=[x_off, y_off])
            self.decode_out_positions.append(vector(x_off, y_off))

    def create_vertical_rail(self):
        # VERTICAL METAL RAILS TO CONNECT PREDECODER TO DECODE STAGE
        if (self.num_inputs >= 4):
            # Array for saving the X offsets of the vertical rails. These rail
            # offsets are accessed with indices.
            vertical_rail_x_offsets = []
            for i in range(self.total_number_of_predecoder_outputs):
                vertical_rail_x_offsets.append(-self.gap_between_rail_offset \
                                                    * (self.total_number_of_predecoder_outputs - i))
                self.add_rect(layer="metal2",
                              offset=[-self.gap_between_rail_offset * (i + 1), 
                                       0],
                              width=drc["minwidth_metal2"],
                              height=self.height)

            # Horizontal metal extensions from pre-decoder 2x4ouput.
            for i in range(self.no_of_pre2x4):
                self.extend_horizontal_to_pre2x4(i,vertical_rail_x_offsets)

            # Horizontal metal extensions from pre-decoder 3x8 ouput.
            for i in range(self.no_of_pre3x8):
                self.extend_horizontal_to_pre3x8(i,vertical_rail_x_offsets)

            self.connect_vertial_rails_to_decoder(vertical_rail_x_offsets)

    def extend_horizontal_to_pre2x4(self, output_index, vertical_rail_x_offsets):
        for inv_2x4 in range(4):
            line_index = output_index * 4 + inv_2x4
            current_inv_height = (output_index * self.pre2_4.height
                                      + inv_2x4 * (self.inv.height))

            if (inv_2x4 % 2 == 0):
                pin_y = self.inv.Z_position.y
            else:
                pin_y = (self.inv.height - drc["minwidth_metal1"]
                             - self.inv.Z_position.y)
            yoffset = current_inv_height + pin_y

            self.add_extend_rails(yoffset = yoffset, 
                                  xoffset = vertical_rail_x_offsets[line_index])

    def extend_horizontal_to_pre3x8(self, output_index, vertical_rail_x_offsets):
        for inv_3x8 in range(8):
            line_index = output_index * 8 + inv_3x8 + self.no_of_pre2x4 * 4
            current_inv_height = output_index * (self.pre3_8.height) \
                + inv_3x8 * (self.inv.height) \
                + self.no_of_pre2x4 * self.pre2_4.height

            if (inv_3x8 % 2 == 0):
                pin_y = self.inv.Z_position.y
            else:
                pin_y = (self.inv.height - drc["minwidth_metal1"] 
                         - self.inv.Z_position.y)
            yoffset = current_inv_height + pin_y

            self.add_extend_rails(yoffset = yoffset, 
                                  xoffset = vertical_rail_x_offsets[line_index])

    def connect_vertial_rails_to_decoder(self, vertical_rail_x_offsets):
        # METAL CONNECTION FROM THE VERTICAL RAIL TOWARDS THE DECODER.
        # PRE-DECODER OUTPUT ARE CONNECTED TO THIS SAME RAIL ALSO
        # To makes these connections groups of line index that was stored in 
        # self.predecoder_output_groups are used
        # Inputs of NAND2/NAND3 gates come from diffrent groups.
        # For example for these groups [ [0,1,2,3] ,[4,5,6,7],
        # [8,9,10,11,12,13,14,15] ] the first NAND3 inputs are connected to
        # [0,4,8] and second NAND3 is connected to [0,4,9]  ........... and the
        # 128th NAND3 is connected to [3,7,15]
        row_index = 0
        if (self.num_inputs == 4 or self.num_inputs == 5):
            for line_index_A in self.predecoder_output_groups[0]:
                for line_index_B in self.predecoder_output_groups[1]:

                    current_inv_height = self.predecoder_height + row_index * (self.inv.height)
                    if (row_index % 2 == 0):
                        yoffset_A = current_inv_height + self.nand2.A_position.y
                        yoffset_B = current_inv_height + self.nand2.B_position.y

                    else:
                        base = current_inv_height + self.inv.height - drc["minwidth_metal1"]
                        yoffset_A = base - self.nand2.A_position.y
                        yoffset_B = base - self.nand2.B_position.y

                    row_index = row_index + 1
                    self.add_extend_rails(yoffset =yoffset_A, 
                                          xoffset =vertical_rail_x_offsets[line_index_A])
                    self.add_extend_rails(yoffset =yoffset_B, 
                                          xoffset =vertical_rail_x_offsets[line_index_B])

        elif (self.num_inputs > 5):
            for line_index_A in self.predecoder_output_groups[0]:
                for line_index_B in self.predecoder_output_groups[1]:
                    for line_index_C in self.predecoder_output_groups[2]:

                        current_inv_height = self.predecoder_height + row_index * (self.inv.height)

                        if (row_index % 2 == 0):
                            yoffset_A = current_inv_height + self.nand3.A_position.y
                            yoffset_B = current_inv_height + self.nand3.B_position.y
                            yoffset_C = current_inv_height + self.nand3.C_position.y
                            contact_C_yoffset = yoffset_C - self.contact_shift
                        else:
                            base = current_inv_height + self.inv.height - drc["minwidth_metal1"]
                            yoffset_A = base - self.nand3.A_position.y
                            yoffset_B = base - self.nand3.B_position.y
                            yoffset_C = base - self.nand3.C_position.y
                            contact_C_yoffset = yoffset_C

                        row_index = row_index + 1

                        self.add_extend_rails(yoffset =yoffset_A, 
                                              xoffset =vertical_rail_x_offsets[line_index_A])
                        self.add_extend_rails(yoffset =yoffset_B, 
                                              xoffset =vertical_rail_x_offsets[line_index_B])
                        self.add_extend_rails(yoffset =yoffset_C, 
                                              xoffset =vertical_rail_x_offsets[line_index_C],
                                              contact_yoffset = contact_C_yoffset)            

    def add_extend_rails(self, yoffset, xoffset, contact_yoffset=0):
        self.add_rect(layer="metal1",
                      offset=[xoffset, yoffset],
                      width=-xoffset,
                      height=drc["minwidth_metal1"])

        if contact_yoffset!=0:
            yoffset = contact_yoffset

        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[xoffset + self.gap_between_rails,
                             yoffset - self.via_shift],
                     rotate=90)

    def delay(self, slope, load = 0.0):
        # A -> out
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
            nand = self.nand2
        else:
            pre = self.pre3_8
            nand = self.nand3
        a_t_out_delay = pre.delay(slope=slope,load = nand.input_load())

        # out -> z
        out_t_z_delay = nand.delay(slope= a_t_out_delay.slope,
                                  load = self.inv.input_load())
        result = a_t_out_delay + out_t_z_delay

        # Z -> decode_out
        z_t_decodeout_delay = self.inv.delay(slope = out_t_z_delay.slope , load = load)
        result = result + z_t_decodeout_delay
        return result

    def input_load(self):
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
        else:
            pre = self.pre3_8
        return pre.input_load()
