import contact
import design
import debug
from tech import drc
from ptx import ptx
from vector import vector
from tech import parameter, spice
from globals import OPTS

class nand_3(design.design):
    """
    This module generates gds of a parametrically sized 3_input nand.

    This model use ptx to generate a 3_input nand within a cetrain height.
    The 3_input nand's cell_height should be the same as the 6t library cell.
    This module doesn't generate multi_finger 3_input nand gate, 
    It generate only the minimum size 3_input nand gate
    """
    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)


    def __init__(self, name, nmos_width=1, height=bitcell.chars["height"]):
        """Constructor : Creates a pcell for a simple 3_input nand"""

        design.design.__init__(self, name)
        debug.info(2, "create nand_3 strcuture {0} with size of {1}".format(name, nmos_width))

        self.nmos_width = nmos_width
        self.height =  height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ add pics for this module """
        self.add_pin_list(["A", "B", "C", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ create layout """
        self.determine_sizes()
        self.create_ptx()
        self.setup_layout_constants()
        self.add_rails()
        self.add_ptx()
        self.add_well_contacts()

        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact.contact(("poly", "contact", "metal1"))
        self.m1m2_via = contact.contact(("metal1", "via1", "metal2"))

        self.connect_tx()
        self.connect_well_contacts()
        self.extend_wells()
        self.extend_active()
        self.connect_rails()
        self.route_pins()
        self.setup_layout_offsets()

    def determine_sizes(self):
        """ Determine the size of the transistors used in this module """
        self.nmos_size = self.nmos_width
        self.pmos_size = 2 * self.nmos_width / 3
        self.tx_mults = 1

    def create_ptx(self):
        """ Create ptx  but not yet placed"""
        self.nmos1 = ptx(width=self.nmos_size,
                         mults=self.tx_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos1)
        self.nmos2 = ptx(width=self.nmos_size,
                         mults=self.tx_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos2)
        self.nmos3 = ptx(width=self.nmos_size,
                         mults=self.tx_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos3)

        self.pmos1 = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos1)
        self.pmos2 = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos2)
        self.pmos3 = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos3)

    def setup_layout_constants(self):
        """ setup layout constraints """
        self.well_width = self.nmos1.active_position.x \
            + 3 * self.pmos1.active_width + drc["active_to_body_active"] \
            + drc["well_enclosure_active"] - self.nmos3.active_contact.width \
            + self.pmos1.active_contact.height + drc["minwidth_metal1"] \
            + (drc["metal1_to_metal1"] - drc["well_enclosure_active"])
        self.width = self.width = self.well_width

    def add_rails(self):
        """ Add VDD and GND rails """
        rail_width = self.width
        self.rail_height = rail_height = drc["minwidth_metal1"]

        # Relocate the origin
        self.gnd_position = vector(0 , - 0.5 * drc["minwidth_metal1"])
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
        """  transistors are added and placed inside the layout  """
        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        self.edge_to_nmos = max(drc["metal1_to_metal1"]
                                    - self.nmos1.active_contact_positions[0].y,
                                0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"]
                                    - self.nmos1.poly_positions[0].y)

        # Extra offset is calculated to make room for B and C contancts
        xoffset = (self.nmos1.active_contact.width
                        + drc["minwidth_metal1"] 
                        + (drc["metal1_to_metal1"] - drc["well_enclosure_active"]))

        # determine the position of the first transistor from the left
        self.nmos_position1 = vector(xoffset, 
                                     0.5 * drc["minwidth_metal1"] + self.edge_to_nmos)
        offset = self.nmos_position1 + vector(0,self.nmos1.height)
        self.add_inst(name="nmos1",
                      mod=self.nmos1,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net2", "A", "gnd", "gnd"])

        self.nmos_position2 = (self.nmos_position1 
                                  + vector(self.nmos2.active_width,0)
                                  - vector(self.nmos2.active_contact.width,0))
        offset = self.nmos_position2 + vector(0, self.nmos2.height)
        self.add_inst(name="nmos2",
                      mod=self.nmos2,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net1", "B", "net2", "gnd"])

        p2tp3 = vector(self.nmos3.active_width - self.nmos3.active_contact.width,
                       self.nmos3.height)
        self.nmos_position3 = self.nmos_position2 + p2tp3
        self.add_inst(name="nmos3",
                      mod=self.nmos3,
                      offset=self.nmos_position3,
                      mirror="MX")
        self.connect_inst(["Z", "C", "net1", "gnd"])

        # determines the spacing between the edge and pmos
        self.edge_to_pmos = max(drc["metal1_to_metal1"] 
                                    - self.pmos1.active_contact_positions[0].y,
                                0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"]
                                    - self.pmos1.poly_positions[0].y)

        self.pmos_position1 = vector(self.nmos_position1.x, 
                                     self.height - 0.5 * drc["minwidth_metal1"] 
                                         - self.pmos1.height - self.edge_to_pmos)
        self.add_inst(name="pmos1",
                      mod=self.pmos1,
                      offset=self.pmos_position1)
        self.connect_inst(["Z", "A", "vdd", "vdd"])

        self.pmos_position2 = vector(self.nmos_position2.x, self.pmos_position1.y)
        self.add_inst(name="pmos2",
                      mod=self.pmos2,
                      offset=self.pmos_position2)
        self.connect_inst(["vdd", "B", "Z", "vdd"])

        self.pmos_position3 = vector(self.nmos_position3.x, self.pmos_position1.y)
        self.add_inst(name="pmos3",
                      mod=self.pmos3,
                      offset=self.pmos_position3)
        self.connect_inst(["Z", "C", "vdd", "vdd"])

    def add_well_contacts(self):
        """ create well contacts """
        layer_stack = ("active", "contact", "metal1")

        xoffset = (self.nmos_position3.x + self.pmos1.active_position.x
                       + self.pmos1.active_width + drc["active_to_body_active"])
        yoffset = self.pmos_position1.y + self.pmos1.active_contact_positions[0].y
        self.nwell_contact_position = vector(xoffset, yoffset)
        self.nwell_contact=self.add_contact(layer_stack,self.nwell_contact_position,(1,self.pmos1.num_of_tacts))

        xoffset = self.nmos_position3.x + (self.nmos1.active_position.x 
                                           + self.nmos1.active_width 
                                           + drc["active_to_body_active"])
        yoffset = self.nmos_position1.y + (self.nmos1.height 
                                           - self.nmos1.active_contact_positions[0].y 
                                           - self.nmos1.active_contact.height)
        self.pwell_contact_position = vector(xoffset, yoffset)
        self.pwell_contact=self.add_contact(layer_stack,self.pwell_contact_position,(1,self.nmos1.num_of_tacts))

    def connect_well_contacts(self):
        """ Connect well contacts to vdd and gnd rail """
        well_tap_length = self.height - self.nwell_contact_position.y
        xoffset = (self.nwell_contact_position.x 
                        + self.nwell_contact.second_layer_position.x 
                        - self.nwell_contact.first_layer_position.x)
        offset = [xoffset, self.nwell_contact_position.y]
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=well_tap_length)

        well_tap_length = self.nmos1.active_height
        offset = vector(self.pwell_contact_position
                            + self.pwell_contact.second_layer_position
                            - self.pwell_contact.first_layer_position).scale(1,0)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=well_tap_length)

    def connect_rails(self):
        """  Connect transistor pmos drains to vdd and nmos drains to gnd rail """
        correct = vector(self.pmos1.active_contact.width - drc["minwidth_metal1"],
                         0).scale(0.5,0)
        poffset = self.pmos_position1 + self.pmos1.active_contact_positions[0] + correct
        temp_height = self.height - poffset.y
        self.add_rect(layer="metal1",
                      offset=poffset,
                      width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = [self.pmos_position3.x + self.pmos3.active_contact_positions[0].x + correct.x,
                   poffset.y]
        self.add_rect(layer="metal1",
                      offset=poffset,
                      width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = self.nmos_position1 + self.nmos1.active_contact_positions[0] + correct
        self.add_rect(layer="metal1",
                      offset=poffset.scale(1,0),
                      width=drc["minwidth_metal1"],
                      height=temp_height)

    def connect_tx(self):
        """ poly and drain connections  """
        self.connect_poly()
        self.connect_drains()

    def connect_poly(self):
        """ Connect poly """
        yoffset_nmos1 = (self.nmos_position1.y + self.nmos1.poly_positions[0].y 
                             + self.nmos1.poly_height)
        poly_length = (self.pmos_position1.y + self.pmos1.poly_positions[0].y 
                           - yoffset_nmos1 + drc["minwidth_poly"])

        offset = vector(self.nmos_position1.x + self.nmos1.poly_positions[0].x,
                  yoffset_nmos1 - drc["minwidth_poly"])
        self.add_rect(layer="poly",
                      offset=offset,
                      width=drc["minwidth_poly"],
                      height=poly_length)
        self.add_rect(layer="poly",
                      offset=[offset.x + self.pmos1.active_contact.width + 2 * drc["minwidth_poly"],
                              offset.y],
                      width=drc["minwidth_poly"],
                      height=poly_length)
        self.add_rect(layer="poly",
                      offset=[offset.x + 2 * self.pmos1.active_contact.width + 4 * drc["minwidth_poly"],
                              offset.y],
                      width=drc["minwidth_poly"],
                      height=poly_length)

    def connect_drains(self):
        """  Connect pmos and nmos drains. The output will be routed to this connection point. """
        yoffset = drc["minwidth_metal1"] + (self.nmos1.active_contact_positions[0].y 
                                                - drc["well_enclosure_active"]
                                                + drc["metal1_to_metal1"])
        drain_length = (self.height - yoffset + 0.5 * drc["minwidth_metal1"]
            - (self.pmos1.height - self.pmos1.active_contact_positions[0].y))
        layer_stack = ("metal1", "via1", "metal2")
        for position in self.pmos1.active_contact_positions[1:][::2]:
            diff_active_via = self.pmos2.active_contact.width - self.m1m2_via.second_layer_width
            offset = (self.pmos_position2 + self.pmos2.active_contact_positions[0]
                          + vector(diff_active_via / 2,0))
            self.add_via(layer_stack,offset)

            width = (2 * self.pmos3.active_width 
                         - self.pmos3.active_contact.width 
                         - (self.pmos2.active_contact.width 
                                - self.m1m2_via.second_layer_width))
            self.add_rect(layer="metal2",
                          offset=offset,
                          width=width,
                          height=self.m1m2_via.second_layer_width) 

            xoffset = (self.pmos_position3.x + self.pmos3.active_contact_positions[1].x
                           + diff_active_via / 2)
            self.add_via(layer_stack,[xoffset,offset.y])

            xoffset = (self.nmos_position3.x + self.nmos3.active_position.x
                + self.nmos3.active_width - self.nmos3.active_contact.width / 2)
            self.drain_position = vector(xoffset,
                                         drc["minwidth_metal1"] + drc["metal1_to_metal1"])
            length = self.height - 2 * (drc["minwidth_metal1"] + drc["metal1_to_metal1"])
            self.add_rect(layer="metal1",
                          offset=self.drain_position,
                          width=drc["minwidth_metal1"],
                          height=length)

    def route_pins(self):
        """ input anbd output routing """
        self.route_input_gate_A()
        self.route_input_gate_B()
        self.route_input_gate_C()
        self.route_output()

    def route_input_gate_A(self):
        """  routing for input A """

        offset = (self.pmos_position1 
                      + self.pmos1.poly_positions[0] 
                      - vector(drc["minwidth_poly"] / 2, self.poly_contact.width))
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         rotate=90)
        self.add_rect(layer="poly",
                      offset=offset + vector(drc["minwidth_poly"] / 2,0),
                      width=-(self.poly_contact.first_layer_position.y + drc["minwidth_poly"]),
                      height=self.poly_contact.first_layer_width)

        offset = vector(offset.x,
                        self.pmos_position1.y + self.pmos1.poly_positions[0].y)
        self.add_layout_pin(text="A",
                      layer="metal1",
                      offset=offset,
                      width=-offset.x,
                      height=-drc["minwidth_metal1"])
        self.A_position = vector(0, offset.y - drc["minwidth_metal1"])


    def route_input_gate_B(self):
        """  routing for input B """
        xoffset = self.pmos2.poly_positions[0].x \
            + self.pmos_position2.x - drc["minwidth_poly"]
        yoffset = self.nmos_position1.y + self.nmos1.height \
            - drc["well_enclosure_active"] + (self.nmos1.active_contact.height \
                                                       - self.nmos1.active_height) / 2 \
                                                       + drc["metal1_to_metal1"]
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=[xoffset,yoffset])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[xoffset,yoffset])

        xoffset = self.pmos2.poly_positions[0].x + self.pmos_position2.x \
            - drc["minwidth_poly"] + self.m1m2_via.width
        length = -xoffset + self.m1m2_via.width
        self.add_rect(layer="metal2",
                      offset=[xoffset, yoffset],
                      width=length,
                      height=-drc["minwidth_metal2"])

        self.B_position = vector(0, yoffset - drc["minwidth_metal1"])
        self.add_label(text="B",
                       layer="metal1",
                       offset=self.B_position)

        xoffset = self.pmos_position1.x + self.pmos1.active_position.x \
            - drc["metal1_to_metal1"] + (self.pmos1.active_contact.width \
                                             - self.m1m2_via.second_layer_width) / 2
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[xoffset,yoffset - drc["minwidth_metal2"]],
                     rotate=90)
        self.add_rect(layer="metal1",
                      offset=[xoffset, yoffset],
                      width=-xoffset,
                      height=-drc["minwidth_metal1"])

    def route_input_gate_C(self):
        """  routing for input A """
        xoffset = self.pmos3.poly_positions[0].x \
            + self.pmos_position3.x - drc["minwidth_poly"]
        yoffset = self.nmos_position1.y + self.nmos1.height \
            - drc["well_enclosure_active"] + (self.nmos1.active_contact.height \
                                                  - self.nmos1.active_height) / 2 + drc["metal1_to_metal1"]

        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=[xoffset,yoffset])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[xoffset,yoffset])

        xoffset = self.pmos3.poly_positions[0].x \
            + self.pmos_position3.x - drc["minwidth_poly"] \
            + self.m1m2_via.width
        length = -xoffset + self.m1m2_via.width
        self.add_rect(layer="metal2",
                      offset=[xoffset,
                              yoffset - drc["minwidth_metal2"] - drc["metal2_to_metal2"]],
                      width=length,
                      height=-drc["minwidth_metal2"])

        # FIXME: Convert to add_layout_pin?
        self.add_rect(layer="metal2",
                      offset=[xoffset - self.m1m2_via.width,
                              yoffset],
                      width=self.m1m2_via.width,
                      height=-drc["minwidth_metal2"] - drc["metal2_to_metal2"])
        self.C_position = vector(0,
                                 self.B_position.y - drc["metal2_to_metal2"] - drc["minwidth_metal1"] \
                                    - (self.m1m2_via.second_layer_width 
                                           - self.m1m2_via.first_layer_width))
        self.add_label(text="C",
                       layer="metal1",
                       offset=self.C_position)

        xoffset = self.pmos_position1.x + self.pmos1.active_position.x \
            - drc["metal1_to_metal1"] + (self.pmos1.active_contact.width \
                                                  - self.m1m2_via.second_layer_width) / 2
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[xoffset,
                             yoffset - 2 * drc["minwidth_metal2"] - self.m1m2_via.width],
                     rotate=90)
        self.add_rect(layer="metal1",
                      offset=[xoffset,
                              yoffset - 2 * drc["minwidth_metal2"]],
                      width=-xoffset,
                      height=-drc["minwidth_metal1"])

    def route_output(self):
        """  routing for output Z """
        xoffset = self.nmos_position3.x + self.nmos3.active_position.x \
            + self.nmos3.active_width - self.nmos3.active_contact.width / 2
        yoffset = (self.nmos1.height + (self.height - drc["minwidth_metal1"] 
                                            - self.pmos1.height - self.nmos1.height) / 2
                                     - (drc["minwidth_metal1"] / 2))
        # FIXME Convert to add_layout_pin?
        self.add_rect(layer="metal1",
                      offset=[xoffset, yoffset],
                      width=self.well_width - xoffset,
                      height=drc["minwidth_metal1"])

        self.Z_position = vector(self.well_width, yoffset)
        self.add_label(text="Z",
                       layer="metal1",
                       offset=self.Z_position)

    def extend_wells(self):
        """  extension of well """
        middle_point = self.nmos_position1.y + self.nmos1.pwell_position.y \
            + self.nmos1.well_height + (self.pmos_position1.y 
                                            + self.pmos1.nwell_position.y 
                                            - self.nmos_position1.y 
                                            - self.nmos1.pwell_position.y 
                                            - self.nmos1.well_height) / 2
        offset = self.nwell_position = vector(0, middle_point)
        self.nwell_height = self.height - middle_point
        self.add_rect(layer="nwell",
                      offset=offset,
                      width=self.well_width,
                      height=self.nwell_height)
        self.add_rect(layer="vtg",
                      offset=offset,
                      width=self.well_width,
                      height=self.nwell_height)

        offset = self.pwell_position = vector(0, 0)
        self.pwell_height = middle_point
        self.add_rect(layer="pwell",
                      offset=offset, width=self.well_width,
                      height=self.pwell_height)
        self.add_rect(layer="vtg",
                      offset=offset,
                      width=self.well_width,
                      height=self.pwell_height)

    def extend_active(self):
        """  extension of active region """
        self.active_width = self.pmos1.active_width \
            + drc["active_to_body_active"] + self.pmos1.active_contact.width
        offset = (self.pmos1.active_position+self.pmos_position3.scale(1,0)
                      + self.pmos_position1.scale(0,1))
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.pmos1.active_height)

        offset = offset + vector(self.pmos1.active_width,0)                  
        width = self.active_width - self.pmos1.active_width
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=width,
                      height=self.pmos1.active_height)

        offset = [self.nmos_position3.x + self.nmos1.active_position.x,
                  self.nmos_position1.y + self.nmos1.height 
                      - self.nmos1.active_position.y - self.nmos1.active_height]
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.nmos1.active_height)

        offset = offset + vector(self.nmos1.active_width,0)
        width = self.active_width - self.nmos1.active_width
        self.add_rect(layer="pimplant",
                      offset=offset,
                      width=width,
                      height=self.nmos1.active_height)

    def setup_layout_offsets(self):
        """ Defining the position of i/o pins for the three input nand gate """
        self.A_position = self.A_position
        self.B_position = self.B_position
        self.C_position = self.C_position
        self.Z_position = self.Z_position
        self.vdd_position = self.vdd_position
        self.gnd_position = self.gnd_position

    def input_load(self):
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def delay(self, slope, load=0.0):
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_c_para"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slope =slope)
