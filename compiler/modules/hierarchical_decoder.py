# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from tech import drc
import debug
import design
from math import log
from math import sqrt
import math
import contact
from sram_factory import factory
from vector import vector
from globals import OPTS

class hierarchical_decoder(design.design):
    """
    Dynamically generated hierarchical decoder.
    """
    def __init__(self, name, rows, height=None):
        design.design.__init__(self, name)

        self.NAND_FORMAT = "DEC_NAND_{0}"
        self.INV_FORMAT = "DEC_INV_{0}"
        
        self.pre2x4_inst = []
        self.pre3x8_inst = []

        self.cell_height = height        
        self.rows = rows
        self.num_inputs = int(math.log(self.rows, 2))
        (self.no_of_pre2x4,self.no_of_pre3x8)=self.determine_predecodes(self.num_inputs)

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
        self.route_input_rails()
        self.route_predecode_rails()
        self.route_vdd_gnd()
        self.offset_all_coordinates()
        self.add_boundary()
        self.DRC_LVS()
                
    def add_modules(self):
        self.inv = factory.create(module_type="pinv",
                                  height=self.cell_height)
        self.add_mod(self.inv)
        self.nand2 = factory.create(module_type="pnand2",
                                    height=self.cell_height)
        self.add_mod(self.nand2)
        self.nand3 = factory.create(module_type="pnand3",
                                    height=self.cell_height)
        self.add_mod(self.nand3)
        
        self.add_decoders()

    def add_decoders(self):
        """ Create the decoders based on the number of pre-decodes """
        self.pre2_4 = factory.create(module_type="hierarchical_predecode2x4",
                                     height=self.cell_height)
        self.add_mod(self.pre2_4)
        
        self.pre3_8 = factory.create(module_type="hierarchical_predecode3x8",
                                     height=self.cell_height)
        self.add_mod(self.pre3_8)

    def determine_predecodes(self,num_inputs):
        """ Determines the number of 2:4 pre-decoder and 3:8 pre-decoder
        needed based on the number of inputs """
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

    def setup_netlist_constants(self):
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


    def setup_layout_constants(self):
        """ Calculate the overall dimensions of the hierarchical decoder """

        # If we have 4 or fewer rows, the predecoder is the decoder itself
        if self.num_inputs>=4:
            self.total_number_of_predecoder_outputs = 4*self.no_of_pre2x4 + 8*self.no_of_pre3x8
        else:
            self.total_number_of_predecoder_outputs = 0            
            debug.error("Not enough rows ({}) for a hierarchical decoder. Non-hierarchical not supported yet.".format(self.num_inputs),-1)

        # Calculates height and width of pre-decoder,
        if self.no_of_pre3x8 > 0:
            self.predecoder_width = self.pre3_8.width 
        else:
            self.predecoder_width = self.pre2_4.width
            
        self.predecoder_height = self.pre2_4.height*self.no_of_pre2x4 + self.pre3_8.height*self.no_of_pre3x8

        # Calculates height and width of row-decoder 
        if (self.num_inputs == 4 or self.num_inputs == 5):
            nand_width = self.nand2.width
        else:
            nand_width = self.nand3.width 
        self.internal_routing_width = self.m2_pitch*self.total_number_of_predecoder_outputs
        self.row_decoder_height = self.inv.height * self.rows

        self.input_routing_width = (self.num_inputs+1) * self.m2_pitch        
        # Calculates height and width of hierarchical decoder 
        self.height = self.row_decoder_height
        self.width = self.input_routing_width + self.predecoder_width \
            + self.internal_routing_width + nand_width + self.inv.width
        
    def route_input_rails(self):
        """ Create input rails for the predecoders """
        # inputs should be as high as the decoders
        input_height = self.no_of_pre2x4*self.pre2_4.height + self.no_of_pre3x8*self.pre3_8.height

        # Find the left-most predecoder
        min_x = 0
        if self.no_of_pre2x4 > 0:
            min_x = min(min_x, -self.pre2_4.width)
        if self.no_of_pre3x8 > 0:
            min_x = min(min_x, -self.pre3_8.width)
        input_offset=vector(min_x - self.input_routing_width,0)

        input_bus_names = ["addr_{0}".format(i) for i in range(self.num_inputs)]
        self.input_rails = self.create_vertical_pin_bus(layer="metal2",
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

                input_pos = self.input_rails["addr_{}".format(index)]

                in_name = "in_{}".format(i)
                decoder_pin = self.pre2x4_inst[pre_num].get_pin(in_name)

                # To prevent conflicts, we will offset each input connect so
                # that it aligns with the vdd/gnd rails
                decoder_offset = decoder_pin.bc() + vector(0,(i+1)*self.inv.height)
                input_offset = input_pos.scale(1,0) + decoder_offset.scale(0,1)
                
                self.route_input_rail(decoder_offset, input_offset) 

            
        for pre_num in range(self.no_of_pre3x8):
            for i in range(3):
                index = pre_num * 3 + i + self.no_of_pre2x4 * 2
                
                input_pos = self.input_rails["addr_{}".format(index)]

                in_name = "in_{}".format(i)
                decoder_pin = self.pre3x8_inst[pre_num].get_pin(in_name)

                # To prevent conflicts, we will offset each input connect so
                # that it aligns with the vdd/gnd rails
                decoder_offset = decoder_pin.bc() + vector(0,(i+1)*self.inv.height)
                input_offset = input_pos.scale(1,0) + decoder_offset.scale(0,1)
                
                self.route_input_rail(decoder_offset, input_offset) 
    

    def route_input_rail(self, input_offset, output_offset):
        """ Route a vertical M2 coordinate to another vertical M2 coordinate to the predecode inputs """
        
        self.add_via_center(layers=("metal2", "via2", "metal3"),
                            offset=input_offset)
        self.add_via_center(layers=("metal2", "via2", "metal3"),
                            offset=output_offset)
        self.add_path(("metal3"), [input_offset, output_offset])

    
    def add_pins(self):
        """ Add the module pins """
        
        for i in range(self.num_inputs):
            self.add_pin("addr_{0}".format(i), "INPUT")

        for j in range(self.rows):
            self.add_pin("decode_{0}".format(j), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def create_pre_decoder(self):
        """ Creates pre-decoder and places labels input address [A] """
        
        for i in range(self.no_of_pre2x4):
            self.create_pre2x4(i)
            
        for i in range(self.no_of_pre3x8):
            self.create_pre3x8(i)

    def create_pre2x4(self,num):
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

        
    def create_pre3x8(self,num):
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

    def place_pre2x4(self,num):
        """ Place 2x4 predecoder to the left of the origin """
        
        if (self.num_inputs == 2):
            base = vector(-self.pre2_4.width,0)
        else:
            base= vector(-self.pre2_4.width, num * self.pre2_4.height)

        self.pre2x4_inst[num].place(base)

        
    def place_pre3x8(self,num):
        """ Place 3x8 predecoder to the left of the origin and above any 2x4 decoders """
        if (self.num_inputs == 3):
            offset = vector(-self.pre_3_8.width,0)
            mirror ="R0"
        else:
            height = self.no_of_pre2x4*self.pre2_4.height + num*self.pre3_8.height
            offset = vector(-self.pre3_8.width, height)

        self.pre3x8_inst[num].place(offset)


    def create_row_decoder(self):
        """ Create the row-decoder by placing NAND2/NAND3 and Inverters
        and add the primary decoder output pins. """
        if (self.num_inputs >= 4):
            self.create_decoder_nand_array()
            self.create_decoder_inv_array()


    def create_decoder_nand_array(self):
        """ Add a column of NAND gates for final decode """

        self.nand_inst = []
        
        # Row Decoder NAND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    row = len(self.predec_groups[0])*j + i
                    name = self.NAND_FORMAT.format(row)
                    self.nand_inst.append(self.add_inst(name=name,
                                                        mod=self.nand2))
                    pins =["out_{0}".format(i),
                           "out_{0}".format(j + len(self.predec_groups[0])),
                           "Z_{0}".format(row),
                           "vdd", "gnd"]
                    self.connect_inst(pins)


        # Row Decoder NAND GATE array for address inputs >5.
        elif (self.num_inputs > 5):
            for i in range(len(self.predec_groups[0])):
                for j in range(len(self.predec_groups[1])):
                    for k in range(len(self.predec_groups[2])):
                        row = (len(self.predec_groups[0])*len(self.predec_groups[1])) * k \
                            + len(self.predec_groups[0])*j + i

                        name = self.NAND_FORMAT.format(row)
                        self.nand_inst.append(self.add_inst(name=name,
                                                            mod=self.nand3))
                        
                        pins = ["out_{0}".format(i),
                                "out_{0}".format(j + len(self.predec_groups[0])),
                                "out_{0}".format(k + len(self.predec_groups[0]) + len(self.predec_groups[1])),
                                "Z_{0}".format(row),
                                "vdd", "gnd"]
                        self.connect_inst(pins)


    def create_decoder_inv_array(self):
        """ 
        Add a column of INV gates for the decoder.
        """
        
        self.inv_inst = []
        for row in range(self.rows):
            name = self.INV_FORMAT.format(row)
            self.inv_inst.append(self.add_inst(name=name,
                                               mod=self.inv))
            self.connect_inst(args=["Z_{0}".format(row),
                                    "decode_{0}".format(row),
                                    "vdd", "gnd"])


    def place_decoder_inv_array(self):
        """
        Place the column of INV gates for the decoder above the predecoders
        and to the right of the NAND decoders.
        """
        
        z_pin = self.inv.get_pin("Z")
        
        if (self.num_inputs == 4 or self.num_inputs == 5):
            x_off = self.internal_routing_width + self.nand2.width
        else:
            x_off = self.internal_routing_width + self.nand3.width

        for row in range(self.rows):
            if (row % 2 == 0):
                inv_row_height = self.inv.height * row
                mirror = "R0"
                y_dir = 1
            else:
                inv_row_height = self.inv.height * (row + 1)
                mirror = "MX"
                y_dir = -1
            y_off = inv_row_height
            offset = vector(x_off,y_off)
            self.inv_inst[row].place(offset=offset,
                                     mirror=mirror)

    def place_row_decoder(self):
        """ 
        Place the row-decoder by placing NAND2/NAND3 and Inverters
        and add the primary decoder output pins. 
        """
        if (self.num_inputs >= 4):
            self.place_decoder_nand_array()
            self.place_decoder_inv_array()
            self.route_decoder()


    def place_decoder_nand_array(self):
        """ Add a column of NAND gates for final decode """
        
        # Row Decoder NAND GATE array for address inputs <5.
        if (self.num_inputs == 4 or self.num_inputs == 5):
            self.place_nand_array(nand_mod=self.nand2)

        # Row Decoder NAND GATE array for address inputs >5.
        # FIXME: why this correct offset?)
        elif (self.num_inputs > 5):
            self.place_nand_array(nand_mod=self.nand3)

    def place_nand_array(self, nand_mod):
        """ Add a column of NAND gates for the decoder above the predecoders."""
        
        for row in range(self.rows):
            name = self.NAND_FORMAT.format(row)
            if ((row % 2) == 0):
                y_off = nand_mod.height*row
                y_dir = 1
                mirror = "R0"
            else:
                y_off = nand_mod.height*(row + 1)
                y_dir = -1
                mirror = "MX"

            self.nand_inst[row].place(offset=[self.internal_routing_width, y_off],
                                      mirror=mirror)

            


    def route_decoder(self):
        """ Route the nand to inverter in the decoder and add the pins. """

        for row in range(self.rows):

            # route nand output to output inv input
            zr_pos = self.nand_inst[row].get_pin("Z").rc()
            al_pos = self.inv_inst[row].get_pin("A").lc()
            # ensure the bend is in the middle 
            mid1_pos = vector(0.5*(zr_pos.x+al_pos.x), zr_pos.y)
            mid2_pos = vector(0.5*(zr_pos.x+al_pos.x), al_pos.y)
            self.add_path("metal1", [zr_pos, mid1_pos, mid2_pos, al_pos])
            
            z_pin = self.inv_inst[row].get_pin("Z")
            self.add_layout_pin(text="decode_{0}".format(row),
                                layer="metal1",
                                offset=z_pin.ll(),
                                width=z_pin.width(),
                                height=z_pin.height())
        


    def route_predecode_rails(self):
        """ Creates vertical metal 2 rails to connect predecoder and decoder stages."""

        # This is not needed for inputs <4 since they have no pre/decode stages.
        if (self.num_inputs >= 4):
            input_offset = vector(0.5*self.m2_width,0)
            input_bus_names = ["predecode_{0}".format(i) for i in range(self.total_number_of_predecoder_outputs)]
            self.predecode_rails = self.create_vertical_pin_bus(layer="metal2",
                                                                pitch=self.m2_pitch,
                                                                offset=input_offset,
                                                                names=input_bus_names,
                                                                length=self.height)
            

            self.route_rails_to_predecodes()
            self.route_rails_to_decoder()

    def route_rails_to_predecodes(self):
        """ Iterates through all of the predecodes and connects to the rails including the offsets """

        # FIXME: convert to connect_bus
        for pre_num in range(self.no_of_pre2x4):
            for i in range(4):
                predecode_name = "predecode_{}".format(pre_num * 4 + i)
                out_name = "out_{}".format(i)
                pin = self.pre2x4_inst[pre_num].get_pin(out_name)
                self.route_predecode_rail_m3(predecode_name, pin) 

            
        # FIXME: convert to connect_bus
        for pre_num in range(self.no_of_pre3x8):
            for i in range(8):
                predecode_name = "predecode_{}".format(pre_num * 8 + i + self.no_of_pre2x4 * 4)
                out_name = "out_{}".format(i)
                pin = self.pre3x8_inst[pre_num].get_pin(out_name)
                self.route_predecode_rail_m3(predecode_name, pin) 
            
                

    def route_rails_to_decoder(self):
        """ Use the self.predec_groups to determine the connections to the decoder NAND gates.
        Inputs of NAND2/NAND3 gates come from different groups.
        For example for these groups [ [0,1,2,3] ,[4,5,6,7],
        [8,9,10,11,12,13,14,15] ] the first NAND3 inputs are connected to
        [0,4,8] and second NAND3 is connected to [0,4,9]  ........... and the
        128th NAND3 is connected to [3,7,15]
        """
        row_index = 0
        if (self.num_inputs == 4 or self.num_inputs == 5):
            for index_B in self.predec_groups[1]:
                for index_A in self.predec_groups[0]:
                    # FIXME: convert to connect_bus?
                    predecode_name = "predecode_{}".format(index_A)
                    self.route_predecode_rail(predecode_name, self.nand_inst[row_index].get_pin("A"))
                    predecode_name = "predecode_{}".format(index_B)                    
                    self.route_predecode_rail(predecode_name, self.nand_inst[row_index].get_pin("B"))
                    row_index = row_index + 1

        elif (self.num_inputs > 5):
            for index_C in self.predec_groups[2]:
                for index_B in self.predec_groups[1]:
                    for index_A in self.predec_groups[0]:
                        # FIXME: convert to connect_bus?
                        predecode_name = "predecode_{}".format(index_A) 
                        self.route_predecode_rail(predecode_name, self.nand_inst[row_index].get_pin("A"))
                        predecode_name = "predecode_{}".format(index_B) 
                        self.route_predecode_rail(predecode_name, self.nand_inst[row_index].get_pin("B"))
                        predecode_name = "predecode_{}".format(index_C) 
                        self.route_predecode_rail(predecode_name, self.nand_inst[row_index].get_pin("C"))
                        row_index = row_index + 1

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # The vias will be placed in the center and right of the cells, respectively.
        xoffset = self.nand_inst[0].cx()
        for num in range(0,self.rows):
            for pin_name in ["vdd", "gnd"]:
                # The nand and inv are the same height rows...
                supply_pin = self.nand_inst[num].get_pin(pin_name)
                pin_pos = vector(xoffset, supply_pin.cy())
                self.add_power_pin(name=pin_name,
                                   loc=pin_pos)

        # Make a redundant rail too
        for num in range(0,self.rows,2):
            for pin_name in ["vdd", "gnd"]:
                start = self.nand_inst[num].get_pin(pin_name).lc()
                end = self.inv_inst[num].get_pin(pin_name).rc()
                mid = (start+end).scale(0.5,0.5)
                self.add_rect_center(layer="metal1",
                                     offset=mid,
                                     width=end.x-start.x)
                
                
        # Copy the pins from the predecoders
        for pre in self.pre2x4_inst + self.pre3x8_inst:
            self.copy_layout_pin(pre, "vdd")
            self.copy_layout_pin(pre, "gnd")
        

    def route_predecode_rail(self, rail_name, pin):
        """ Connect the routing rail to the given metal1 pin  """
        rail_pos = vector(self.predecode_rails[rail_name].x,pin.lc().y)
        self.add_path("metal1", [rail_pos, pin.lc()])
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=rail_pos)


    def route_predecode_rail_m3(self, rail_name, pin):
        """ Connect the routing rail to the given metal1 pin  """
        # This routes the pin up to the rail, basically, to avoid conflicts.
        # It would be fixed with a channel router.
        mid_point = vector(pin.cx(), pin.cy()+self.inv.height/2)
        rail_pos = vector(self.predecode_rails[rail_name].x,mid_point.y)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=pin.center())
        self.add_wire(("metal3","via2","metal2"), [rail_pos, mid_point, pin.uc()])
        self.add_via_center(layers=("metal2", "via2", "metal3"),
                            offset=rail_pos)

    def input_load(self):
        if self.determine_predecodes(self.num_inputs)[1]==0:
            pre = self.pre2_4
        else:
            pre = self.pre3_8
        return pre.input_load()
        
