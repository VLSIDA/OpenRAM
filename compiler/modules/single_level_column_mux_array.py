# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from math import log
import design
import contact
from tech import drc
import debug
import math
from vector import vector
from sram_factory import factory
from globals import OPTS
import logical_effort

class single_level_column_mux_array(design.design):
    """
    Dynamically generated column mux array.
    Array of column mux to read the bitlines through the 6T.
    """

    def __init__(self, name, columns, word_size, bitcell_bl="bl", bitcell_br="br"):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("cols: {0} word_size: {1} bl: {2} br: {3}".format(columns, word_size, bitcell_bl, bitcell_br))
        
        self.columns = columns
        self.word_size = word_size
        self.words_per_row = int(self.columns / self.word_size)
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def get_bl_name(self):
        bl_name = self.mux.get_bl_names()
        return bl_name

    def get_br_name(self, port=0):
        br_name = self.mux.get_br_names()
        return br_name

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_array()
        
    def create_layout(self):
        self.setup_layout_constants()
        self.place_array()
        self.add_routing()
        # Find the highest shapes to determine height before adding well
        highest = self.find_highest_coords()
        self.height = highest.y 
        self.add_layout_pins()
        self.add_enclosure(self.mux_inst, "pwell")

        self.add_boundary()
        self.DRC_LVS()
        
    def add_pins(self):
        for i in range(self.columns):
            self.add_pin("bl_{}".format(i))
            self.add_pin("br_{}".format(i))
        for i in range(self.words_per_row):
            self.add_pin("sel_{}".format(i))
        for i in range(self.word_size):
            self.add_pin("bl_out_{}".format(i))
            self.add_pin("br_out_{}".format(i))
        self.add_pin("gnd")


    def add_modules(self):
        self.mux = factory.create(module_type="single_level_column_mux",
                                  bitcell_bl=self.bitcell_bl,
                                  bitcell_br=self.bitcell_br)
        self.add_mod(self.mux)


    def setup_layout_constants(self):
        self.column_addr_size = num_of_inputs = int(self.words_per_row / 2)
        self.width = self.columns * self.mux.width
        # one set of metal1 routes for select signals and a pair to interconnect the mux outputs bl/br
        # one extra route pitch is to space from the sense amp
        self.route_height = (self.words_per_row + 3)*self.m1_pitch
        

        
    def create_array(self):
        self.mux_inst = []
        # For every column, add a pass gate
        for col_num in range(self.columns):
            name = "XMUX{0}".format(col_num)
            self.mux_inst.append(self.add_inst(name=name,
                                               mod=self.mux))
            
            self.connect_inst(["bl_{}".format(col_num),
                               "br_{}".format(col_num),
                               "bl_out_{}".format(int(col_num/self.words_per_row)),
                               "br_out_{}".format(int(col_num/self.words_per_row)),
                               "sel_{}".format(col_num % self.words_per_row),
                               "gnd"])

    def place_array(self):
        from tech import cell_properties
        # For every column, add a pass gate
        for col_num in range(self.columns):
            xoffset = col_num * self.mux.width
            if cell_properties.bitcell.mirror.y and col_num % 2:
                mirror = "MY"
                xoffset = xoffset + self.mux.width
            else:
                mirror = ""

            name = "XMUX{0}".format(col_num)
            offset = vector(xoffset, self.route_height)
            self.mux_inst[col_num].place(offset=offset, mirror=mirror)
            

    def add_layout_pins(self):
        """ Add the pins after we determine the height. """
        # For every column, add a pass gate
        for col_num in range(self.columns):
            mux_inst = self.mux_inst[col_num]
            offset = mux_inst.get_pin("bl").ll()
            self.add_layout_pin(text="bl_{}".format(col_num),
                                layer="m2",
                                offset=offset,
                                height=self.height-offset.y)

            offset = mux_inst.get_pin("br").ll()
            self.add_layout_pin(text="br_{}".format(col_num),
                                layer="m2",
                                offset=offset,
                                height=self.height-offset.y)

        for inst in self.mux_inst:
            self.copy_layout_pin(inst, "gnd")


    def add_routing(self):
        self.add_horizontal_input_rail()
        self.add_vertical_poly_rail()
        self.route_bitlines()

    def add_horizontal_input_rail(self):
        """ Create address input rails on M1 below the mux transistors  """
        for j in range(self.words_per_row):
            offset = vector(0, self.route_height + (j-self.words_per_row)*self.m1_pitch)
            self.add_layout_pin(text="sel_{}".format(j),
                                layer="m1",
                                offset=offset,
                                width=self.mux.width * self.columns)

    def add_vertical_poly_rail(self):
        """  Connect the poly to the address rails """
        
        # Offset to the first transistor gate in the pass gate
        for col in range(self.columns):
            # which select bit should this column connect to depends on the position in the word
            sel_index = col % self.words_per_row
            # Add the column x offset to find the right select bit
            gate_offset = self.mux_inst[col].get_pin("sel").bc()
            # height to connect the gate to the correct horizontal row
            sel_height = self.get_pin("sel_{}".format(sel_index)).by()
            # use the y offset from the sel pin and the x offset from the gate
            offset = vector(gate_offset.x,self.get_pin("sel_{}".format(sel_index)).cy())
            # Add the poly contact with a shift to account for the rotation
            self.add_via_center(layers=("m1", "contact", "poly"),
                                offset=offset)
            self.add_path("poly", [offset, gate_offset])

    def route_bitlines(self):
        """  Connect the output bit-lines to form the appropriate width mux """
        from tech import cell_properties
        for j in range(self.columns):
            bl_offset = self.mux_inst[j].get_pin("bl_out").bc()
            br_offset = self.mux_inst[j].get_pin("br_out").bc()

            bl_out_offset = bl_offset - vector(0,(self.words_per_row+1)*self.m1_pitch)
            br_out_offset = br_offset - vector(0,(self.words_per_row+2)*self.m1_pitch)

            bl_out_offset_end = bl_out_offset + vector(0,self.route_height)
            br_out_offset_end = br_out_offset + vector(0,self.route_height)

            if cell_properties.bitcell.mirror.y and j % 2:
                tmp_bl_out_end = br_out_offset_end
                tmp_br_out_end = bl_out_offset_end
            else:
                tmp_bl_out_end = bl_out_offset_end
                tmp_br_out_end = br_out_offset_end

            if (j % self.words_per_row) == 0:
                # Create the metal1 to connect the n-way mux output from the pass gate
                # These will be located below the select lines. Yes, these are M2 width
                # to ensure vias are enclosed and M1 min width rules.
                width = self.m2_width + self.mux.width * (self.words_per_row - 1)

                if cell_properties.bitcell.mirror.y and (j % 2) == 0:
                    bl = self.mux.get_pin("bl")
                    br = self.mux.get_pin("br")
                    dist = abs(bl.ll().x - br.ll().x)
                else:
                    dist = 0

                self.add_path("m1", [bl_out_offset, bl_out_offset+vector(width+dist,0)])
                self.add_path("m1", [br_out_offset, br_out_offset+vector(width-dist,0)])

                # Extend the bitline output rails and gnd downward on the first bit of each n-way mux
                self.add_layout_pin_segment_center(text="bl_out_{}".format(int(j/self.words_per_row)),
                                                   layer="m2",
                                                   start=bl_out_offset,
                                                   end=tmp_bl_out_end)
                self.add_layout_pin_segment_center(text="br_out_{}".format(int(j/self.words_per_row)),
                                                   layer="m2",
                                                   start=br_out_offset,
                                                   end=tmp_br_out_end)
                                                   

                # This via is on the right of the wire                
                self.add_via_center(layers=self.m1_stack,
                                    offset=bl_out_offset)

                # This via is on the left of the wire
                self.add_via_center(layers=self.m1_stack,
                                    offset=br_out_offset)

            else:
                
                self.add_path("m2", [ bl_out_offset, tmp_bl_out_end])
                self.add_path("m2", [ br_out_offset, tmp_br_out_end])
                                          
                # This via is on the right of the wire
                self.add_via_center(layers=self.m1_stack,
                                    offset=bl_out_offset)
                # This via is on the left of the wire                
                self.add_via_center(layers=self.m1_stack,
                                    offset=br_out_offset)

    def get_drain_cin(self):
        """Get the relative capacitance of the drain of the NMOS pass TX"""
        from tech import parameter
        #Bitcell drain load being used to estimate mux NMOS drain load
        drain_load = logical_effort.convert_farad_to_relative_c(parameter['bitcell_drain_cap'])
        return drain_load      
