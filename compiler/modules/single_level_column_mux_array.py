from math import log
import design
from single_level_column_mux import single_level_column_mux 
import contact
from tech import drc
import debug
import math
from vector import vector


class single_level_column_mux_array(design.design):
    """
    Dynamically generated column mux array.
    Array of column mux to read the bitlines through the 6T.
    """

    def __init__(self, columns, word_size):
        design.design.__init__(self, "columnmux_array")
        debug.info(1, "Creating {0}".format(self.name))
        self.columns = columns
        self.word_size = word_size
        self.words_per_row = self.columns / self.word_size
        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.columns):
            self.add_pin("bl[{}]".format(i))
            self.add_pin("br[{}]".format(i))
        for i in range(self.words_per_row):
            self.add_pin("sel[{}]".format(i))
        for i in range(self.word_size):
            self.add_pin("bl_out[{}]".format(i))
            self.add_pin("br_out[{}]".format(i))
        self.add_pin("gnd")

    def create_layout(self):
        self.add_modules()
        self.setup_layout_constants()
        self.create_array()
        self.add_routing()
        # Find the highest shapes to determine height before adding well
        highest = self.find_highest_coords()
        self.height = highest.y 
        self.add_layout_pins()
        self.add_enclosure(self.mux_inst, "pwell")

        

    def add_modules(self):
        # FIXME: Why is this 8x?
        self.mux = single_level_column_mux(tx_size=8)
        self.add_mod(self.mux)


    def setup_layout_constants(self):
        self.column_addr_size = num_of_inputs = int(self.words_per_row / 2)
        self.width = self.columns * self.mux.width
        self.m1_pitch = contact.m1m2.width + max(drc["metal1_to_metal1"],drc["metal2_to_metal2"])
        # one set of metal1 routes for select signals and a pair to interconnect the mux outputs bl/br
        # one extra route pitch is to space from the sense amp
        self.route_height = (self.words_per_row + 3)*self.m1_pitch
        

        
    def create_array(self):
        self.mux_inst = []

        # For every column, add a pass gate
        for col_num in range(self.columns):
            name = "XMUX{0}".format(col_num)
            x_off = vector(col_num * self.mux.width, self.route_height)
            self.mux_inst.append(self.add_inst(name=name,
                                               mod=self.mux,
                                               offset=x_off))
            
            self.connect_inst(["bl[{}]".format(col_num),
                               "br[{}]".format(col_num),
                               "bl_out[{}]".format(int(col_num/self.words_per_row)),
                               "br_out[{}]".format(int(col_num/self.words_per_row)),
                               "sel[{}]".format(col_num % self.words_per_row),
                               "gnd"])


    def add_layout_pins(self):
        """ Add the pins after we determine the height. """
        # For every column, add a pass gate
        for col_num in range(self.columns):
            mux_inst = self.mux_inst[col_num]
            offset = mux_inst.get_pin("bl").ll()
            self.add_layout_pin(text="bl[{}]".format(col_num),
                                layer="metal2",
                                offset=offset,
                                height=self.height-offset.y)

            offset = mux_inst.get_pin("br").ll()
            self.add_layout_pin(text="br[{}]".format(col_num),
                                layer="metal2",
                                offset=offset,
                                height=self.height-offset.y)

            gnd_pins = mux_inst.get_pins("gnd")
            for gnd_pin in gnd_pins:
                # only do even colums to avoid duplicates
                offset = gnd_pin.ll()
                if col_num % 2 == 0: 
                    self.add_layout_pin(text="gnd",
                                        layer="metal2",
                                        offset=offset.scale(1,0),
                                        height=self.height)
        

    def add_routing(self):
        self.add_horizontal_input_rail()
        self.add_vertical_poly_rail()
        self.route_bitlines()

    def add_horizontal_input_rail(self):
        """ Create address input rails on M1 below the mux transistors  """
        for j in range(self.words_per_row):
            offset = vector(0, self.route_height - (j+1)*self.m1_pitch)
            self.add_layout_pin(text="sel[{}]".format(j),
                                layer="metal1",
                                offset=offset,
                                width=self.mux.width * self.columns,
                                height=contact.m1m2.width)

    def add_vertical_poly_rail(self):
        """  Connect the poly to the address rails """
        
        # Offset to the first transistor gate in the pass gate
        for col in range(self.columns):
            # which select bit should this column connect to depends on the position in the word
            sel_index = col % self.words_per_row
            # Add the column x offset to find the right select bit
            gate_offset = self.mux_inst[col].get_pin("sel").bc()
            # height to connect the gate to the correct horizontal row
            sel_height = self.get_pin("sel[{}]".format(sel_index)).by()
            # use the y offset from the sel pin and the x offset from the gate
            offset = vector(gate_offset.x,self.get_pin("sel[{}]".format(sel_index)).cy())
            # Add the poly contact with a shift to account for the rotation
            self.add_via_center(layers=("metal1", "contact", "poly"),
                                offset=offset,
                                rotate=90)
            self.add_path("poly", [offset, gate_offset])

    def route_bitlines(self):
        """  Connect the output bit-lines to form the appropriate width mux """
        for j in range(self.columns):
            bl_offset = self.mux_inst[j].get_pin("bl_out").ll()
            br_offset = self.mux_inst[j].get_pin("br_out").ll()

            bl_out_offset = bl_offset - vector(0,(self.words_per_row+1)*self.m1_pitch)
            br_out_offset = br_offset - vector(0,(self.words_per_row+2)*self.m1_pitch)

            if (j % self.words_per_row) == 0:
                # Create the metal1 to connect the n-way mux output from the pass gate
                # These will be located below the select lines. Yes, these are M2 width
                # to ensure vias are enclosed and M1 min width rules.
                width = contact.m1m2.width + self.mux.width * (self.words_per_row - 1)
                self.add_rect(layer="metal1",
                              offset=bl_out_offset,
                              width=width,
                              height=drc["minwidth_metal2"])
                self.add_rect(layer="metal1",
                              offset=br_out_offset,
                              width=width,
                              height=drc["minwidth_metal2"])
                          

                # Extend the bitline output rails and gnd downward on the first bit of each n-way mux
                self.add_layout_pin(text="bl_out[{}]".format(int(j/self.words_per_row)),
                                    layer="metal2",
                                    offset=bl_out_offset.scale(1,0),
                                    width=drc['minwidth_metal2'],
                                    height=self.route_height)
                self.add_layout_pin(text="br_out[{}]".format(int(j/self.words_per_row)),
                                    layer="metal2",
                                    offset=br_out_offset.scale(1,0),
                                    width=drc['minwidth_metal2'],
                                    height=self.route_height)

                # This via is on the right of the wire                
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=bl_out_offset + vector(contact.m1m2.height,0),
                             rotate=90)
                # This via is on the left of the wire
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset= br_out_offset,
                             rotate=90)

            else:
                
                self.add_rect(layer="metal2",
                              offset=bl_out_offset,
                              width=drc['minwidth_metal2'],
                              height=self.route_height-bl_out_offset.y)
                # This via is on the right of the wire
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=bl_out_offset + vector(contact.m1m2.height,0),
                             rotate=90)
                self.add_rect(layer="metal2",
                              offset=br_out_offset,
                              width=drc['minwidth_metal2'],
                              height=self.route_height-br_out_offset.y)
                # This via is on the left of the wire                
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset= br_out_offset,
                             rotate=90)

                
            
