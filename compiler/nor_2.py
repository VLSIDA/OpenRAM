import contact
import design
import debug
from tech import drc
from ptx import ptx
from vector import vector
from globals import OPTS

class nor_2(design.design):
    """
    This module generates gds of a parametrically sized 2_input nor.

    This model use ptx to generate a 2_input nand within a cetrain height.
    The 2_input nor cell_height should be the same as the 6t library cell.
    If pmos can not fit in the given vertical space, it will be folded 
    based so that it takes minmium horiztonal space.
    """
    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)

    def __init__(self, name, nmos_width=1, height=bitcell.chars["height"]):
        """init function"""
        design.design.__init__(self, name)
        debug.info(2, "create nand_2 strcuture {0} with size of {1}".format(name, nmos_width))

        self.nmos_width = nmos_width
        self.height = height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_layout(self):
        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact.contact(("poly", "contact", "metal1"))
        self.m1m2_via = contact.contact(("metal1", "via1", "metal2"))

        self.determine_sizes()
        self.create_modules()

        # These aren't for instantiating, but we use them to get the dimensions
        self.nwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
                                                     dimensions=(1, self.pmos1.num_of_tacts))
        self.pwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
                                                     dimensions=(1, self.nmos1.num_of_tacts))

        self.setup_layout_constants()
        self.add_rails()
        self.add_ptx()
        self.add_well_contacts()
        self.extend_wells()
        self.extend_active()
        self.route()

    def determine_sizes(self, beta=4):
        """Determine transistor size"""
        nmos_mults = 1
        for pmos_mults in range(1, 5):
            nmos_size = self.nmos_width
            pmos_size = 4 * self.nmos_width / pmos_mults
            test_nmos = ptx(width=nmos_size,
                            mults=nmos_mults,
                            tx_type="nmos")
            test_pmos = ptx(width=pmos_size,
                            mults=pmos_mults,
                            tx_type="nmos")
            
            # this how the position is done for now
            # postion noms and pmos and put A at 0.3 of the margin of it and put B and the 3rd m1 track above it
            # if there is no left space then it means the nmos is too big, we
            # need to increase the mults number
            gate_to_gate = drc["poly_to_poly"] - drc["minwidth_metal1"]
            edge_to_nmos = max(drc["metal1_to_metal1"] - test_nmos.active_contact_positions[0].y,
                               0.5 * gate_to_gate - test_nmos.poly_positions[0].y)
            edge_to_pmos = max(drc["metal1_to_metal1"] - test_pmos.active_contact_positions[0].y,
                               0.5 * gate_to_gate - test_pmos.poly_positions[0].y)
            route_margin = .5 * (self.poly_contact.second_layer_width 
                                 + drc["minwidth_metal1"]) + drc["metal1_to_metal1"]
            pmos_position = vector(0, self.height - 0.5 * drc["minwidth_metal1"]
                                      - edge_to_pmos - test_pmos.height)
            nmos_position = vector(0, 0.5 * drc["minwidth_metal1"] + edge_to_nmos)
            leftspace = (0.7 * (pmos_position.y - nmos_position.y) 
                         - 3 * route_margin - 2 * drc["metal1_to_metal1"])
            if leftspace >= 0:
                break

        self.nmos_size = nmos_size
        self.pmos_size = pmos_size
        self.nmos_mults = nmos_mults
        self.pmos_mults = pmos_mults

    def create_modules(self):
        """transistors are created as modules"""
        self.nmos1 = ptx(width=self.nmos_size,
                         mults=self.nmos_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos1)
        self.nmos2 = ptx(width=self.nmos_size,
                         mults=self.nmos_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos2)

        self.pmos1 = ptx(width=self.pmos_size,
                         mults=self.pmos_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos1)
        self.pmos2 = ptx(width=self.pmos_size,
                         mults=self.pmos_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos2)


    def setup_layout_constants(self):
        """ calcuate the transistor spacing and cell size"""
        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        half_gate_to_gate = 0.5 * (drc["poly_to_poly"] - drc["minwidth_metal1"])
        edge_to_nmos = max(drc["metal1_to_metal1"] - self.nmos1.active_contact_positions[0].y,
                           half_gate_to_gate - self.nmos1.poly_positions[0].y)

        # determine the position of the first transistor from the left
        self.nmos_position1 = vector(0,
                                     0.5 * drc["minwidth_metal1"] + edge_to_nmos)
        offset = self.nmos_position1 + vector(0,self.nmos1.height)

        x = vector(self.nmos2.active_width - self.nmos2.active_contact.width, 0)
        self.nmos_position2 = x + self.nmos_position1.scale(0,1)

        # determines the spacing between the edge and pmos
        edge_to_pmos = max(drc["metal1_to_metal1"] - self.pmos1.active_contact_positions[0].y,
                           half_gate_to_gate - self.pmos1.poly_positions[0].y)
        self.pmos_position1 = vector(0,
                                     self.height - 0.5 * drc["minwidth_metal1"]
                                         - edge_to_pmos - self.pmos1.height)
        self.pmos_position2 = self.pmos_position1 + vector(self.pmos1.width,0)

        self.well_width = max(self.pmos_position2.x + self.pmos2.active_position.x
                                      + self.pmos2.active_width
                                      + drc["active_to_body_active"] + self.nwell_contact.width 
                                      + drc["well_enclosure_active"],
                              self.nmos_position2.x + self.nmos2.active_position.x 
                                      + self.nmos2.active_width 
                                      + drc["active_to_body_active"] + drc["well_enclosure_active"])
        self.width = self.well_width

    def add_rails(self):
        rail_width = self.width
        rail_height = drc["minwidth_metal1"]
        self.rail_height = rail_height
        # Relocate the origin
        self.gnd_position = vector(0, - 0.5 * drc["minwidth_metal1"])
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=self.gnd_position,
                            width=rail_width,
                            height=rail_height)

        self.vdd_position = self.gnd_position + vector(0, self.height)
        self.add_layout_pin(text="vdd",
                      layer="metal1",
                      offset=self.vdd_position,
                      width=rail_width,
                      height=rail_height)

    def add_ptx(self):
        """ transistors are  placed in the layout"""
        offset = self.nmos_position1 + vector(0, self.nmos1.height)
        self.add_inst(name="nmos1",
                      mod=self.nmos1,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["Z", "A", "gnd", "gnd"])

        offset = self.nmos_position2 + vector(0, self.nmos2.height)
        self.add_inst(name="nmos2",
                      mod=self.nmos2,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["Z", "B", "gnd", "gnd"])

        offset = self.pmos_position1
        self.add_inst(name="pmos1",
                      mod=self.pmos1,
                      offset=offset)
        self.connect_inst(["vdd", "A", "net1", "vdd"])

        offset = self.pmos_position2
        self.add_inst(name="pmos2",
                      mod=self.pmos2,
                      offset=offset)
        self.connect_inst(["net1", "B", "Z", "vdd"])

    def add_well_contacts(self):
        layer_stack = ("active", "contact", "metal1")

        xoffset = (self.pmos_position2.x + self.pmos1.active_position.x
                   + self.pmos1.active_width + drc["active_to_body_active"])
        yoffset = (self.pmos_position1.y 
                   + self.pmos1.active_contact_positions[0].y)
        self.nwell_contact_position = vector(xoffset, yoffset)
        self.nwell_contact=self.add_contact(layer_stack,self.nwell_contact_position,(1,self.pmos1.num_of_tacts))

        xoffset = self.nmos_position2.x + (self.nmos1.active_position.x 
                                                + self.nmos1.active_width 
                                                + drc["active_to_body_active"])
        yoffset = (self.nmos_position1.y + self.nmos1.height 
                       - self.nmos1.active_contact_positions[0].y
                       - self.nmos1.active_contact.height)
        self.pwell_contact_position = vector(xoffset, yoffset)
        self.pwell_contact=self.add_contact(layer_stack,self.pwell_contact_position,(1,self.nmos1.num_of_tacts))


    def route(self):
        self.route_pins()
        self.connect_well_contacts()
        M1_track = (self.B_position.y + drc["metal1_to_metal1"]
                        + .5 * (self.poly_contact.second_layer_width 
                                    + drc["minwidth_metal1"]))
        self.connect_tx(M1_track)
        self.connect_poly()

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

        offset = (self.pwell_contact_position.scale(1,0)
                      + self.pwell_contact.second_layer_position.scale(1,0)
                      - self.pwell_contact.first_layer_position.scale(1,0))
        well_tap_length = self.pwell_contact_position.y
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=well_tap_length)

    def connect_tx(self, M1_track):
        """Connect transistor pmos drains to vdd and nmos drains to gnd rail"""
        # the first pmos drain to Vdd
        for i in range(len(self.pmos1.active_contact_positions)):
            contact_pos = self.pmos_position1 + self.pmos1.active_contact_positions[i]
            if i % 2 == 0:
                correct = self.pmos1.active_contact.second_layer_position.scale(1,0)    
                drain_posistion = contact_pos + correct  
                height = self.vdd_position.y - drain_posistion.y
                self.add_rect(layer="metal1",
                              offset=drain_posistion,
                              width=drc["minwidth_metal1"],
                              height=height)
            else:
                # source to pmos2
                correct = (self.pmos1.active_contact.second_layer_position.scale(1,0)
                               + vector(self.pmos1.active_contact.second_layer_width,
                                        0).scale(.5,0))
                source_position = contact_pos + correct
                mid = [self.pmos_position2.x, M1_track]
                self.add_path("metal1", [source_position, mid])

        # the second pmos
        for i in range(len(self.pmos2.active_contact_positions)):
            if i % 2 == 0:
                # source to pmos2
                pmos_active =self.pmos_position2+self.pmos2.active_contact_positions[i]
                correct= (self.pmos2.active_contact.second_layer_position.scale(1,0)
                              + vector(0.5 * self.pmos2.active_contact.second_layer_width,0))
                source_position = pmos_active + correct
                mid = [self.pmos_position2.x, M1_track]
                self.add_path("metal1", [source_position, mid])
        # two nmos source to gnd
        source_posistion1 = (self.nmos_position1
                                 + self.nmos1.active_contact_positions[0]
                                 + self.nmos1.active_contact.second_layer_position.scale(1,0))
        height = self.gnd_position.y - source_posistion1.y
        self.add_rect(layer="metal1",
                      offset=source_posistion1,
                      width=drc["minwidth_metal1"],
                      height=height)

        source_posistion2 = (self.nmos_position2
                                 + self.nmos2.active_contact_positions[1]
                                 + self.nmos2.active_contact.second_layer_position.scale(1,0))        
        height = self.gnd_position.y - source_posistion2.y
        self.add_rect(layer="metal1",
                      offset=source_posistion2,
                      width=drc["minwidth_metal1"],
                      height=height)

    def connect_poly(self):
        """connect connect poly between nmos and pmos"""
        # connect pmos1 poly
        nmos_gate = (self.nmos_position1 
                     + self.nmos1.poly_positions[0]
                     + vector(0.5 * drc["minwidth_poly"], 0))
        for i in range(len(self.pmos1.poly_positions)):
            pmos_gate = (self.pmos_position1 
                             + self.pmos1.poly_positions[i]
                             + vector(0.5 * drc["minwidth_poly"], 0))
            mid1 = [pmos_gate.x, pmos_gate.y - drc["poly_to_active"]]
            self.add_path("poly", [nmos_gate, mid1, pmos_gate])

        # connect pmos2 poly
        nmos_gate = vector(self.nmos_position2[0] 
                               + self.nmos2.poly_positions[0].x
                               + 0.5 * drc["minwidth_poly"], 
                           self.nmos_position1.y 
                               + self.nmos1.poly_positions[0].y)
        for i in range(len(self.pmos2.poly_positions)):
            pmos_gate = (self.pmos_position2
                             + self.pmos2.poly_positions[i]
                             + vector(0.5 * drc["minwidth_poly"], 0))
            mid1 = vector(pmos_gate.x,
                          nmos_gate.y + self.nmos2.height 
                              + drc["poly_to_active"])
            self.add_path("poly", [nmos_gate, mid1, pmos_gate])

    def route_pins(self):
        self.route_input_gate()
        self.route_output()

    def route_input_gate(self):
        self.route_input_A()
        self.route_input_B()

    def route_input_A(self):
        """create input A layout"""
        xoffset = self.nmos1.poly_positions[0].x
        yoffset = self.nmos_position1.y + self.nmos1.height \
                  + 0.3 * (self.pmos_position1.y - self.nmos_position1.y \
                           - self.nmos1.height)
        self.A_position = vector(xoffset, yoffset)
        # gate input
        offset = self.A_position - vector(0, 0.5 * self.poly_contact.width)
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         rotate=90)

        # connect gate input to tx gate
        offset = self.A_position - vector(self.poly_contact.first_layer_position.y,
                                          0.5 * self.poly_contact.width)
        self.add_rect(layer="poly",
                      offset=offset,
                      width=self.poly_contact.first_layer_position.y + drc["minwidth_poly"],
                      height=self.poly_contact.first_layer_width)
        # extend the metal to the boundary of the cell
        input_length = self.A_position.x
        offset = [0, self.A_position.y - 0.5 * drc["minwidth_metal1"]]
        self.add_layout_pin(text="A",
                      layer="metal1",
                      offset=offset,
                      width=input_length,
                      height=drc["minwidth_metal1"])

    def route_input_B(self):
        """create input B layout """
        xoffset = self.pmos2.poly_positions[0].x \
                  + self.pmos_position2.x
        yoffset = self.A_position.y \
                  + 0.5 * (self.poly_contact.second_layer_width \
                           + drc["minwidth_metal1"]) + drc["metal1_to_metal1"]
        self.B_position = vector(xoffset, yoffset)
        offset = self.B_position - vector(0, 0.5 * self.poly_contact.width)     
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         rotate=90)

        self.add_rect(layer="poly",
                      offset=offset,
                      width=-(self.poly_contact.first_layer_position.y + drc["minwidth_poly"]),
                      height=self.poly_contact.first_layer_width)
        self.add_layout_pin(text="B",
                      layer="metal1",
                      offset=[0,
                              self.B_position.y - 0.5 * drc["minwidth_metal1"]],
                      width=self.B_position.x,
                      height=drc["minwidth_metal1"])

    def route_output(self):
        """route the output to nmos pmos """
        self.Z_position = vector(self.width, self.A_position.y)
        # route nmos drain to Z
        nmos_contact = (self.nmos_position1 
                            + self.nmos1.active_contact_positions[1] 
                            + self.nmos1.active_contact.second_layer_position
                            + vector(self.nmos1.active_contact.second_layer_width,
                                     0).scale(0.5, 0))
        mid = [nmos_contact.x, self.A_position.y]
        self.add_path("metal1", [self.Z_position, mid, nmos_contact])

        for i in range(len(self.pmos2.poly_positions) + 1):
            if i % 2 == 1:
                # pmos2 drain to Z
                pmos_contact = (self.pmos_position2
                                    + self.pmos1.active_contact_positions[i]
                                    + self.pmos2.active_contact.second_layer_position.scale(1, 0)
                                    + vector(self.pmos2.active_contact.second_layer_width,
                                             0).scale(0.5, 0))
                offset = pmos_contact - vector(0.5 * self.m1m2_via.width, 0)
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=offset)
                mid = [pmos_contact.x, self.Z_position.y]
                self.add_wire(("metal1", "via1", "metal2"),
                              [self.Z_position, mid, pmos_contact])

    def extend_wells(self):
        """ extend well for well contact"""
        middle_point = (self.nmos_position1.y 
                            + self.nmos1.pwell_position.y 
                            + self.nmos1.well_height 
                            + (self.pmos_position1.y
                                   + self.pmos1.nwell_position.y 
                                   - self.nmos_position1.y 
                                   - self.nmos1.pwell_position.y 
                                   - self.nmos1.well_height) / 2 )
        self.nwell_position = vector(0, middle_point)
        self.nwell_height = self.height - middle_point
        self.add_rect(layer="nwell",
                      offset=self.nwell_position,
                      width=self.well_width,
                      height=self.nwell_height)
        self.add_rect(layer="vtg",
                      offset=self.nwell_position,
                      width=self.well_width,
                      height=self.nwell_height)

        self.pwell_position = vector(0, 0)
        self.pwell_height = middle_point
        self.add_rect(layer="pwell",
                      offset=self.pwell_position,
                      width=self.well_width,
                      height=self.pwell_height)
        self.add_rect(layer="vtg",
                      offset=self.pwell_position, 
                      width=self.well_width,
                      height=self.pwell_height)

    def extend_active(self):
        """ extend active for well contact"""
        self.active_width = self.pmos1.active_width \
                                    + drc["active_to_body_active"] \
                                    + self.pmos1.active_contact.width
        offset = (self.pmos_position2.scale(1,0)
                     + self.pmos_position1.scale(0,1)
                     + self.pmos1.active_position)
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.pmos1.active_height)
        offset = offset + vector(self.pmos1.active_width, 0)
        width = self.active_width - self.pmos1.active_width
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=width,
                      height=self.pmos1.active_height)

        offset = (self.nmos1.active_position.scale(1,-1)
                      + self.nmos_position2.scale(1,0)
                      + self.nmos_position1.scale(0,1)
                      + vector(0, self.nmos1.height - self.nmos1.active_height))                 
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
