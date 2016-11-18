import contact
import design
import debug
from tech import drc, parameter
from ptx import ptx
from vector import vector
from math import ceil
from globals import OPTS

class pinv(design.design):
    """
    This module generates gds of a parametrically sized inverter.
    This model use ptx to generate a inverter within a cetrain height.
    The inverter's cell_height should be the same as the 6t library cell.
    """
    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)

    def __init__(self, name, nmos_width=1, beta=3, height=bitcell.chars["height"], route_output=True):
        design.design.__init__(self, name)
        debug.info(2, "create pinv strcuture {0} with size of {1}".format(name, nmos_width))

        self.nmos_width = nmos_width
        self.beta = beta
        self.height = height
        self.route_output = route_output

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """Adds pins for spice netlist processing"""
        self.add_pin_list(["A", "Z", "vdd", "gnd"])

    def create_layout(self):
        """Calls all functions related to the generation of the layout(gds)"""

        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact.contact(("poly", "contact", "metal1"))
        self.m1m2_via = contact.contact(("metal1", "via1", "metal2"))

        self.determine_tx_mults()
        self.create_ptx()
        self.setup_layout_constants()
        self.add_rails()
        self.add_ptx()

        # These aren't for instantiating, but we use them to get the dimensions
        self.nwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
                                                     dimensions=(1, self.pmos.num_of_tacts))
        self.pwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
                                                     dimensions=(1, self.nmos.num_of_tacts))

        self.extend_wells()
        self.extend_active()
        self.add_well_contacts()
        self.connect_well_contacts()
        self.connect_rails()
        self.connect_tx()
        self.route_pins()
        self.setup_layout_offsets()

    def determine_tx_mults(self):
        """Determines the number of fingers needed to achieve same size with a height constraint"""
        # check minimum distance between well
        minwidth_poly_contact = drc["minwidth_contact"] \
                                + 2 * drc["poly_enclosure_contact"]

        # this should be 2*poly extension beyond active?
        minwidth_box_poly = 2 * drc["minwidth_poly"] \
                            + drc["poly_to_poly"]
        well_to_well = max(drc["pwell_enclose_nwell"],
                           minwidth_poly_contact,
                           minwidth_box_poly)

        # determine both mos enclosure sizes
        bot_mos_enclosure = 2 * (drc["well_enclosure_active"])
        top_mos_enclosure = 2 * max(drc["well_enclosure_active"],
                                    drc["metal1_to_metal1"] + 0.5 * drc["minwidth_metal1"])

        self.nmos_size = parameter["min_tx_size"]
        self.pmos_size = parameter["min_tx_size"] * self.beta

        # use multi finger if the cell is not big enough
        if self.nmos_size <= self.nmos_width:
            self.tx_mults = int(ceil(self.nmos_width / self.nmos_size))
        else:
            self.tx_mults = 1

    def create_ptx(self):
        """Intiializes a ptx object"""
        self.nmos = ptx(name="inv_nmos1",
                        width=self.nmos_size,
                        mults=self.tx_mults,
                        tx_type="nmos")
        self.nmos.connect_fingered_poly()
        self.nmos.connect_fingered_active()
        self.add_mod(self.nmos)
        self.pmos = ptx(name="inv_pmos1",
                        width=self.pmos_size,
                        mults=self.tx_mults,
                        tx_type="pmos")
        self.pmos.connect_fingered_poly()
        self.pmos.connect_fingered_active()
        self.add_mod(self.pmos)

    def setup_layout_constants(self):
        """Sets up constant variables"""
        # the well width is determined the multi-finger PMOS device width plus
        # the well contact width and enclosure
        self.well_width = self.pmos.active_position.x \
                                  + self.pmos.active_width \
                                  + drc["active_to_body_active"] \
                                  + self.pmos.active_contact.width \
                                  + drc["well_enclosure_active"]
        self.width = self.well_width

    def add_rails(self):
        """Adds vdd/gnd rails to the layout"""
        rail_width = self.width
        rail_height = self.rail_height = drc["minwidth_metal1"]

        self.gnd_position = vector(0, - 0.5 * drc["minwidth_metal1"])  # for tiling purposes
        self.add_layout_pin(text="gnd",
                      layer="metal1",
                      offset=self.gnd_position,
                      width=rail_width,
                      height=rail_height)

        self.vdd_position = vector(0, self.height - 0.5 * drc["minwidth_metal1"])
        self.add_layout_pin(text="vdd",
                      layer="metal1",
                      offset=self.vdd_position,
                      width=rail_width,
                      height=rail_height)

    def add_ptx(self):
        """Adds pmos and nmos to the layout"""
        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        edge_to_nmos = max(drc["metal1_to_metal1"] \
                           - self.nmos.active_contact_positions[0].y,
                           0.5 * drc["poly_to_poly"] \
                           - 0.5 * drc["minwidth_metal1"] \
                           - self.nmos.poly_positions[0].y)
        self.nmos_position = vector(0, 0.5 * drc["minwidth_metal1"] + edge_to_nmos)
        offset = self.nmos_position + vector(0,self.nmos.height)
        self.add_inst(name="pinv_nmos",
                      mod=self.nmos,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["Z", "A", "gnd", "gnd"])

        # determines the spacing between the edge and pmos
        edge_to_pmos = max(drc["metal1_to_metal1"] \
                           - self.pmos.active_contact_positions[0].y,
                           0.5 * drc["poly_to_poly"] \
                           - 0.5 * drc["minwidth_metal1"] \
                           - self.pmos.poly_positions[0].y)
        self.pmos_position = vector(0,
                                    self.height - 0.5 * drc["minwidth_metal1"]
                                    - edge_to_pmos - self.pmos.height)
        self.add_inst(name="pinv_pmos",
                      mod=self.pmos,
                      offset=self.pmos_position)
        self.connect_inst(["Z", "A", "vdd", "vdd"])

    def extend_wells(self):
        """Extends the n/p wells to cover whole layout"""
        nmos_top_yposition = self.nmos_position.y + self.nmos.height
        # calculates the length between the pmos and nmos
        middle_length = self.pmos_position.y - nmos_top_yposition
        # calculate the middle point between the pmos and nmos
        middle_yposition = nmos_top_yposition + 0.5 * middle_length

        self.nwell_position = vector(0, middle_yposition)
        self.nwell_height = self.height - middle_yposition
        self.add_rect(layer="nwell",
                      offset=self.nwell_position,
                      width=self.well_width,
                      height=self.nwell_height)
        self.add_rect(layer="vtg",
                      offset=self.nwell_position,
                      width=self.well_width,
                      height=self.nwell_height)

        self.pwell_position = vector(0, 0)
        self.pwell_height = middle_yposition
        self.add_rect(layer="pwell",
                      offset=self.pwell_position, width=self.well_width,
                      height=self.pwell_height)
        self.add_rect(layer="vtg",
                      offset=self.pwell_position,
                      width=self.well_width,
                      height=self.pwell_height)

    def extend_active(self):
        """Extends the active area for n/p mos for the addition of the n/p well taps"""
        # calculates the new active width that includes the well_taps
        self.active_width = self.pmos.active_width \
                          + drc["active_to_body_active"] \
                          + self.pmos.active_contact.width

        # Calculates the coordinates of the bottom left corner of active area
        # of the pmos
        offset = self.pmos_position + self.pmos.active_position
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.pmos.active_height)

        # Determines where the active of the well portion starts to add the
        # implant
        offset = offset + vector(self.pmos.active_width,0)
        implant_width = self.active_width - self.pmos.active_width
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=implant_width,
                      height=self.pmos.active_height)

        # Calculates the coordinates of the bottom left corner of active area
        # of the nmos
        offset = self.nmos_position + self.nmos.active_position
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.nmos.active_height)

        # Determines where the active of the well portion starts to add the
        # implant
        offset = offset + vector(self.pmos.active_width,0)
        implant_width = self.active_width - self.nmos.active_width
        self.add_rect(layer="pimplant",
                      offset=offset,
                      width=implant_width,
                      height=self.nmos.active_height)

    def connect_poly(self):
        """Connects the poly from nmos to pmos (as well if it is multi-fingered)"""
        # Calculates the y-coordinate of the top of the poly of the nmos
        nmos_top_poly_yposition = self.nmos_position.y \
                                  + self.nmos.height \
                                  - self.nmos.poly_positions[0].y

        poly_length = self.pmos_position.y + self.pmos.poly_positions[0].y \
                      - nmos_top_poly_yposition
        for position in self.pmos.poly_positions:
            offset = [position.x, nmos_top_poly_yposition]
            self.add_rect(layer="poly",
                          offset=offset,
                          width=drc["minwidth_poly"],
                          height=poly_length)

    def connect_drains(self):
        """Connects the drains of the nmos/pmos together"""
        # Determines the top y-coordinate of the nmos drain metal layer
        yoffset = self.nmos.height \
                  - 0.5 * drc["minwidth_metal1"] \
                  - self.nmos.active_contact_positions[0].y
        drain_length = self.height - yoffset + drc["minwidth_metal1"] \
                       - (self.pmos.height
                          - self.pmos.active_contact_positions[0].y)
        for position in self.pmos.active_contact_positions[1:][::2]:
            offset = [position.x + self.pmos.active_contact.second_layer_position.x,
                      yoffset]
            self.drain_position = vector(offset)
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=self.nmos.active_contact.second_layer_width,
                          height=drain_length)

    def route_input_gate(self):
        """Routes the input gate to the left side of the cell for access"""

        xoffset = self.pmos.poly_positions[0].x
        # Determines the y-coordinate of where to place the gate input poly pin
        # (middle in between the pmos and nmos)
        yoffset = self.nmos.height + (self.height 
                     - self.pmos.height - self.nmos.height
                     - self.poly_contact.width) / 2
        offset = [xoffset, yoffset]
        self.add_contact(layers=("poly", "contact", "metal1"),
                      offset=offset,
                      rotate=90)

        # Determines the poly coordinate to connect to the poly contact
        offset = offset - self.poly_contact.first_layer_position.rotate_scale(1,0)
        self.add_rect(layer="poly",
                      offset=offset,
                      width=self.poly_contact.first_layer_position.y + drc["minwidth_poly"],
                      height=self.poly_contact.first_layer_width)

        input_length = self.pmos.poly_positions[0].x \
                       - self.poly_contact.height
        # Determine the y-coordinate for the placement of the metal1 via
        self.input_position = vector(0, .5*(self.height - drc["minwidth_metal1"] 
                                            + self.nmos.height - self.pmos.height))
        self.add_layout_pin(text="A",
                      layer="metal1",
                      offset=self.input_position,
                      width=input_length,
                      height=drc["minwidth_metal1"])

    def route_output_drain(self):
        """Routes the output (drain) to the right side of the cell for access"""
        # Determines the y-coordinate of the output metal1 via pin
        offset = vector(self.drain_position.x 
                        + self.nmos.active_contact.second_layer_width, 
                        self.input_position.y)
        output_length = self.width - offset.x
        if self.route_output == True:
            self.output_position = offset + vector(output_length,0)
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=output_length,
                          height=drc["minwidth_metal1"])
        else:
            self.output_position = offset
        self.add_label(text="Z",
                       layer="metal1",
                       offset=offset)

    def add_well_contacts(self):
        """Adds n/p well taps to the layout"""
        layer_stack = ("active", "contact", "metal1")
        # Same y-positions of the drain/source metals as the n/p mos
        well_contact_offset = vector(self.pmos.active_position.x 
                                         + self.active_width 
                                         - self.nwell_contact.width,
                                     self.pmos.active_contact_positions[0].y)
        self.nwell_contact_position = self.pmos_position + well_contact_offset
        self.nwell_contact=self.add_contact(layer_stack,self.nwell_contact_position,(1,self.pmos.num_of_tacts))

        well_contact_offset = vector(self.nmos.active_position.x 
                                               + self.active_width 
                                               - self.pwell_contact.width,
                                     self.nmos.active_contact_positions[0].y)
        self.pwell_contact_position = self.nmos_position + well_contact_offset
        self.pwell_contact=self.add_contact(layer_stack,self.pwell_contact_position,(1,self.nmos.num_of_tacts))

    def connect_well_contacts(self):
        """Connects the well taps to its respective power rails"""
        # calculates the length needed to connect the nwell_tap to vdd
        nwell_tap_length = self.height \
                           - 0.5 * drc["minwidth_metal1"] \
                           - self.nwell_contact_position.y
        # obtains the position for the metal 1 layer in the nwell_tap
        offset = self.nwell_contact_position + \
                 self.nwell_contact.second_layer_position.scale(1,0)
        self.add_rect(layer="metal1",
                      offset=offset, width=self.nwell_contact.second_layer_width,
                      height=nwell_tap_length)

        pwell_tap_length = self.pwell_contact_position.y \
                           + 0.5 * drc["minwidth_metal1"]
        offset = [self.pwell_contact_position.x
                  + self.pwell_contact.second_layer_position.x,
                  0.5 * drc["minwidth_metal1"]]
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=self.pwell_contact.second_layer_width,
                      height=pwell_tap_length)

    def connect_rails(self):
        """Connects the n/p mos to its respective power rails"""
        if self.tx_mults != 1:
            return
        # corrects offset to obtain real coordinates of the layer in question
        # in a contact object
        correct = vector(self.nmos.active_contact.width 
                          - self.nmos.active_contact.width,
                         - drc["minwidth_metal1"]).scale(.5,.5)    
        # nmos position of the source metals
        noffset = self.nmos_position + self.nmos.active_contact_positions[0] + correct
        offset = [self.nmos.active_contact.second_layer_position.x + noffset.x,
                0.5 * drc["minwidth_metal1"]]
        self.add_rect(layer="metal1", offset=offset, 
                      width=self.nmos.active_contact.second_layer_width,
                      height=noffset.y)
        # corrects offset to obtain real coordinates of the layer in question
        # in a contact object
        correct = vector(self.pmos.active_contact.width
                         - self.pmos.active_contact.width,
                         self.pmos.active_contact.second_layer_height).scale(.5,1)
        # pmos position of the source metals
        offset = self.pmos_position + self.pmos.active_contact_positions[0]\
               + correct + self.pmos.active_contact.second_layer_position
        temp_height = self.height - offset.y - 0.5 * drc["minwidth_metal1"]
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=self.pmos.active_contact.second_layer_width,
                      height=temp_height)

    def connect_tx(self):
        self.connect_poly()
        self.connect_drains()

    def route_pins(self):
        self.route_input_gate()
        self.route_output_drain()

    def setup_layout_offsets(self):
        self.A_position = self.input_position
        self.Z_position = self.output_position
