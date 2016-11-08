from math import log
import design
from single_level_column_mux import single_level_column_mux 
from contact import contact
from tech import drc
import debug
import math
from vector import vector


class single_level_column_mux_array(design.design):
    """
    Dynamically generated column mux array.
    Array of column mux to read the bitlines through the 6T.
    """

    def __init__(self, rows, columns, word_size):
        design.design.__init__(self, "columnmux_array")
        debug.info(1, "Creating {0}".format(self.name))
        self.rows = rows
        self.columns = columns
        self.word_size = word_size
        self.words_per_row = self.columns / self.word_size
        self.row_addr_size = self.decoder_inputs = int(math.log(self.rows, 2))
        self.add_pins()
        self.create_layout()
        self.offset_all_coordinates()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.columns):
            self.add_pin("bl[{0}]".format(i))
            self.add_pin("br[{0}]".format(i))
        for i in range(self.columns / self.words_per_row):
            self.add_pin("bl_out[{0}]".format(i * self.words_per_row))
            self.add_pin("br_out[{0}]".format(i * self.words_per_row))
        for i in range(self.words_per_row):
            self.add_pin("sel[{0}]".format(i))
        self.add_pin("gnd")

    def create_layout(self):
        self.add_modules()
        self.setup_layout_constants()
        self.create_array()
        self.add_routing()

    def add_modules(self):
        self.mux = single_level_column_mux(name="single_level_column_mux",
                                           tx_size=8)
        self.single_mux = self.mux
        self.add_mod(self.mux)

        # This is not instantiated and used for calculations only.
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))


    def setup_layout_constants(self):
        self.column_addr_size = num_of_inputs = int(self.words_per_row / 2)
        self.width = (self.columns * self.mux.width)
        self.gnd_positions = []
        self.BL_out_positions = []
        self.BR_out_positions = []
        self.BL_positions = []
        self.BR_positions = []
        self.addr_line_positions = []

        spacing = self.m1m2_via.width + drc['metal1_to_metal1']  
        self.height = self.mux.height + spacing + 4 * drc['metal2_to_metal2']
        if (self.words_per_row > 1):
            # 1 for BL and another for BR
            self.height = self.height + (self.words_per_row + 1) * spacing

    def create_array(self):
        for i in range(self.columns):
            name = "XMUX{0}".format(i)
            x_off = vector(i * self.mux.width, 0)
            self.add_inst(name=name,
                          mod=self.mux,
                          offset=x_off)

            """ draw a vertical m2 rail to extend BL BR & gnd on top of the cell """
            # FIXME: These are just min metal squares, are they needed?
            self.add_rect(layer="metal2",
                          offset=x_off + self.mux.BL_position,
                          width=drc['minwidth_metal2'],
                          height=drc['minwidth_metal2'])
            self.add_rect(layer="metal2",
                          offset=x_off + self.mux.BR_position,
                          width=drc['minwidth_metal2'],
                          height=drc['minwidth_metal2'])
            self.add_rect(layer="metal2",
                          offset=x_off + self.mux.gnd_position,
                          width=drc['minwidth_metal2'],
                          height=drc['minwidth_metal2'])

            """ add labels for the column_mux array """
            BL = self.mux.BL_position + vector(i * self.mux.width, 0)
            self.BL_positions.append(BL)
            self.add_label(text="bl[{0}]".format(i),
                           layer="metal2",
                           offset=BL)

            BR = self.mux.BR_position + vector(i * self.mux.width, 0)
            self.BR_positions.append(BR)
            self.add_label(text="br[{0}]".format(i),
                           layer="metal2",
                           offset=BR)

            gnd = self.mux.gnd_position + vector(i * self.mux.width, 0)
            self.gnd_positions.append(gnd)
            self.add_label(text="gnd",
                           layer="metal2",
                           offset=gnd)

        for i in range(self.word_size):
            base =vector(i * self.words_per_row * self.mux.width, 0)
            BL_out = base + self.mux.BL_out_position
            BR_out = base + self.mux.BR_out_position
            self.add_label(text="bl_out[{0}]".format(i * self.words_per_row),
                           layer="metal2",
                           offset=BL_out)
            self.add_label(text="br_out[{0}]".format(i * self.words_per_row),
                           layer="metal2",
                           offset=BR_out)
            self.BL_out_positions.append(BL_out)
            self.BR_out_positions.append(BR_out)

        if(self.words_per_row == 2):
            for i in range(self.columns / 2):
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(2 * i),
                                        "br[{0}]".format(2 * i),
                                        "bl_out[{0}]".format(2 * i),
                                        "br_out[{0}]".format(2 * i),
                                        "sel[{0}]".format(0), "gnd"],
                                  check=False)
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(2 * i + 1),
                                        "br[{0}]".format(2 * i + 1),
                                        "bl_out[{0}]".format(2 * i),
                                        "br_out[{0}]".format(2 * i),
                                        "sel[{0}]".format(1), "gnd"],
                                  check=False)
        if(self.words_per_row == 4):
            for i in range(self.columns / 4):
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(4 * i),
                                        "br[{0}]".format(4 * i),
                                        "bl_out[{0}]".format(4 * i),
                                        "br_out[{0}]".format(4 * i),
                                        "sel[{0}]".format(0), "gnd"],
                                  check=False)
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(4 * i + 1),
                                        "br[{0}]".format(4 * i + 1),
                                        "bl_out[{0}]".format(4 * i),
                                        "br_out[{0}]".format(4 * i),
                                        "sel[{0}]".format(1), "gnd"],
                                  check=False)
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(4 * i + 2),
                                        "br[{0}]".format(4 * i + 2),
                                        "bl_out[{0}]".format(4 * i),
                                        "br_out[{0}]".format(4 * i),
                                        "sel[{0}]".format(2), "gnd"],
                                  check=False)
                # This will not check that the inst connections match.
                self.connect_inst(args=["bl[{0}]".format(4 * i + 3),
                                        "br[{0}]".format(4 * i + 3),
                                        "bl_out[{0}]".format(4 * i),
                                        "br_out[{0}]".format(4 * i),
                                        "sel[{0}]".format(3), "gnd"],
                                  check=False)

    def add_routing(self):
        self.add_horizontal_input_rail()
        self.add_vertical_poly_rail()
        self.routing_BL_BR()

    def add_horizontal_input_rail(self):
        """ HORIZONTAL ADDRESS INPUTS TO THE COLUMN MUX ARRAY """
        if (self.words_per_row > 1):
            for j in range(self.words_per_row):
                offset = vector(0, -(j + 1) * self.m1m2_via.width
                                       - j * drc['metal1_to_metal1'])
                self.add_rect(layer="metal1",
                              offset=offset,
                              width=self.mux.width * self.columns,
                              height=self.m1m2_via.width)
                self.addr_line_positions.append(offset)

    def add_vertical_poly_rail(self):
        """  VERTICAL POLY METAL EXTENSION AND POLY CONTACT """
        for j1 in range(self.columns):
            pattern = math.floor(j1 / self.words_per_row) * self.words_per_row 
            height = ((self.m1m2_via.width + drc['metal1_to_metal1'])
                           *(pattern - j1))
            nmos1_poly = self.mux.nmos1_position + self.mux.nmos1.poly_positions[0]
            offset = nmos1_poly.scale(1, 0) + vector(j1 * self.mux.width, 0)
            self.add_rect(layer="poly",
                          offset=offset,
                          width=drc["minwidth_poly"],
                          height= height -self.m1m2_via.width)

            # This is not instantiated and used for calculations only.
            poly_contact = contact(layer_stack=("metal1", "contact", "poly"))
            offset = offset.scale(1, 0) + vector(0, height - poly_contact.width)
            self.add_contact(layers=("metal1", "contact", "poly"),
                             offset=offset,
                             mirror="MX",
                             rotate=90)

    def routing_BL_BR(self):
        """  OUTPUT BIT-LINE CONNECTIONS (BL_OUT, BR_OUT) """
        if (self.words_per_row > 1):
            for j in range(self.columns / self.words_per_row):
                base = vector(self.mux.width * self.words_per_row * j,
                              self.m1m2_via.width + drc['metal1_to_metal1'])
                width = self.m1m2_via.width + self.mux.width * (self.words_per_row - 1)
                self.add_rect(layer="metal1",
                              offset=base.scale(1,-self.words_per_row) + self.mux.BL_position.scale(1,0),
                              width=width,
                              height=-self.m1m2_via.width)
                self.add_rect(layer="metal1",
                              offset=base.scale(1,-self.words_per_row-1) + self.mux.BR_position.scale(1,0),
                              width=width,
                              height=-self.m1m2_via.width)

                height = base.y * (self.words_per_row + 2) + 3 * drc['metal2_to_metal2']
                base = vector(base.x, - height)
                self.add_rect(layer="metal2",
                              offset=base + self.mux.BL_position.scale(1,0),
                              width=drc['minwidth_metal2'],
                              height=height)
                self.add_rect(layer="metal2",
                              offset=base + self.mux.BR_position.scale(1,0),
                              width=drc['minwidth_metal2'],
                              height=height)
                self.add_rect(layer="metal2",
                              offset=base + self.mux.gnd_position.scale(1,0),
                              width=drc['minwidth_metal2'],
                              height=height)

            for j in range(self.columns):
                """ adding vertical metal rails to route BL_out and BR_out vertical rails """
                contact_spacing = self.m1m2_via.width + drc['metal1_to_metal1']
                height = self.words_per_row * contact_spacing + self.m1m2_via.width
                offset = vector(self.mux.BL_position.x + self.mux.width * j, 0)
                self.add_rect(layer="metal2",
                              offset=offset,
                              width=drc['minwidth_metal2'], 
                              height=-height)
                offset = offset + vector(self.m1m2_via.height, - height)
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate=90)

                offset = vector(self.mux.BR_position.x + self.mux.width * j, 0)
                height = height + contact_spacing
                self.add_rect(layer="metal2",
                              offset=offset,
                              width=drc['minwidth_metal2'],
                              height= - height)
                offset = offset + vector(self.m1m2_via.height/2, - height)
                layer_diff = (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) 
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset= offset + vector(layer_diff, 0),
                             rotate=90)

        self.add_label(text="COLUMN_MUX",
                       layer="text",
                       offset=[self.width / 2.0, self.height / 2.0])
