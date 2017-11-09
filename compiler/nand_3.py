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

    unique_id = 1
    
    def __init__(self, nmos_width=3*drc["minwidth_tx"], height=bitcell.height):
        """Constructor : Creates a cell for a simple 3 input nand"""
        name = "nand3_{0}".format(nand_3.unique_id)
        nand_3.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "create nand_3 structure {0} with size of {1}".format(name, nmos_width))

        self.nmos_size = nmos_width
        # FIXME: Why is this??
        self.pmos_size = 2 * nmos_width / 3
        self.tx_mults = 1
        self.height =  height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ add pics for this module """
        self.add_pin_list(["A", "B", "C", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ create layout """
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

    def create_ptx(self):
        """ Create ptx  but not yet placed"""
        # If full contacts, this will interfere with the C input in SCMOS
        self.nmos = ptx(width=self.nmos_size,
                        mults=self.tx_mults,
                        tx_type="nmos",
                        num_contacts=1)
        self.add_mod(self.nmos)

        self.pmos = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos)

    def setup_layout_constants(self):
        """ setup layout constraints """
        self.well_width = self.nmos.active_position.x \
            + 3 * self.pmos.active_width + drc["active_to_body_active"] \
            + drc["well_enclosure_active"] - self.nmos.active_contact.width \
            + self.pmos.active_contact.height + drc["minwidth_metal1"] \
            + (drc["metal1_to_metal1"] - drc["well_enclosure_active"])
        self.width = self.width = self.well_width

    def add_rails(self):
        """ Add VDD and GND rails """
        rail_width = self.width
        self.rail_height = rail_height = drc["minwidth_metal1"]

        # Relocate the origin
        self.gnd_loc = vector(0 , - 0.5 * drc["minwidth_metal1"])
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=self.gnd_loc,
                            width=rail_width,
                            height=rail_height)

        self.vdd_loc = vector(0, self.height - 0.5 * drc["minwidth_metal1"])
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=self.vdd_loc,
                            width=rail_width,
                            height=rail_height)

    def add_ptx(self):
        """  transistors are added and placed inside the layout  """
        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        self.edge_to_nmos = max(drc["metal1_to_metal1"]
                                    - self.nmos.active_contact_positions[0].y,
                                0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"]
                                    - self.nmos.poly_positions[0].y)

        # Extra offset is calculated to make room for B and C contancts
        xoffset = (self.nmos.active_contact.width
                        + drc["minwidth_metal1"] 
                        + (drc["metal1_to_metal1"] - drc["well_enclosure_active"]))

        # determine the position of the first transistor from the left
        self.nmos_position1 = vector(xoffset, 
                                     0.5 * drc["minwidth_metal1"] + self.edge_to_nmos)
        offset = self.nmos_position1 + vector(0,self.nmos.height)
        self.add_inst(name="nmos",
                      mod=self.nmos,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net2", "A", "gnd", "gnd"])

        self.nmos_position2 = (self.nmos_position1 
                                  + vector(self.nmos.active_width,0)
                                  - vector(self.nmos.active_contact.width,0))
        offset = self.nmos_position2 + vector(0, self.nmos.height)
        self.add_inst(name="nmos2",
                      mod=self.nmos,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net1", "B", "net2", "gnd"])

        p2tp3 = vector(self.nmos.active_width - self.nmos.active_contact.width,
                       self.nmos.height)
        self.nmos_position3 = self.nmos_position2 + p2tp3
        self.add_inst(name="nmos3",
                      mod=self.nmos,
                      offset=self.nmos_position3,
                      mirror="MX")
        self.connect_inst(["Z", "C", "net1", "gnd"])

        # determines the spacing between the edge and pmos
        self.edge_to_pmos = max(drc["metal1_to_metal1"] 
                                    - self.pmos.active_contact_positions[0].y,
                                0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"]
                                    - self.pmos.poly_positions[0].y)

        self.pmos_position1 = vector(self.nmos_position1.x, 
                                     self.height - 0.5 * drc["minwidth_metal1"] 
                                         - self.pmos.height - self.edge_to_pmos)
        self.add_inst(name="pmos1",
                      mod=self.pmos,
                      offset=self.pmos_position1)
        self.connect_inst(["Z", "A", "vdd", "vdd"])

        self.pmos_position2 = vector(self.nmos_position2.x, self.pmos_position1.y)
        self.add_inst(name="pmos2",
                      mod=self.pmos,
                      offset=self.pmos_position2)
        self.connect_inst(["vdd", "B", "Z", "vdd"])

        self.pmos_position3 = vector(self.nmos_position3.x, self.pmos_position1.y)
        self.add_inst(name="pmos3",
                      mod=self.pmos,
                      offset=self.pmos_position3)
        self.connect_inst(["Z", "C", "vdd", "vdd"])

    def add_well_contacts(self):
        """ create well contacts """
        layer_stack = ("active", "contact", "metal1")

        xoffset = (self.nmos_position3.x + self.pmos.active_position.x
                       + self.pmos.active_width + drc["active_to_body_active"])
        yoffset = self.pmos_position1.y + self.pmos.active_contact_positions[0].y
        self.nwell_contact_position = vector(xoffset, yoffset)
        self.nwell_contact=self.add_contact(layer_stack,self.nwell_contact_position,(1,self.pmos.num_contacts))

        xoffset = self.nmos_position3.x + (self.nmos.active_position.x 
                                           + self.nmos.active_width 
                                           + drc["active_to_body_active"])
        yoffset = self.nmos_position1.y + (self.nmos.height 
                                           - self.nmos.active_contact_positions[0].y 
                                           - self.nmos.active_contact.height)
        self.pwell_contact_position = vector(xoffset, yoffset)
        self.pwell_contact=self.add_contact(layer_stack,self.pwell_contact_position,(1,self.nmos.num_contacts))

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

        well_tap_length = self.nmos.active_height
        offset = vector(self.pwell_contact_position
                            + self.pwell_contact.second_layer_position
                            - self.pwell_contact.first_layer_position).scale(1,0)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=well_tap_length)

    def connect_rails(self):
        """  Connect transistor pmos drains to vdd and nmos drains to gnd rail """
        correct = vector(self.pmos.active_contact.width - drc["minwidth_metal1"],
                         0).scale(0.5,0)
        poffset = self.pmos_position1 + self.pmos.active_contact_positions[0] + correct
        temp_height = self.height - poffset.y
        self.add_rect(layer="metal1",
                      offset=poffset,
                      width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = [self.pmos_position3.x + self.pmos.active_contact_positions[0].x + correct.x,
                   poffset.y]
        self.add_rect(layer="metal1",
                      offset=poffset,
                      width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = self.nmos_position1 + self.nmos.active_contact_positions[0] + correct
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
        yoffset_nmos = (self.nmos_position1.y + self.nmos.poly_positions[0].y 
                             + self.nmos.poly_height)
        poly_length = (self.pmos_position1.y + self.pmos.poly_positions[0].y 
                           - yoffset_nmos + drc["minwidth_poly"])

        offset = vector(self.nmos_position1.x + self.nmos.poly_positions[0].x,
                  yoffset_nmos - drc["minwidth_poly"])
        self.add_rect(layer="poly",
                      offset=offset,
                      width=drc["minwidth_poly"],
                      height=poly_length)
        self.add_rect(layer="poly",
                      offset=[offset.x + self.pmos.active_contact.width + 2 * drc["minwidth_poly"],
                              offset.y],
                      width=drc["minwidth_poly"],
                      height=poly_length)
        self.add_rect(layer="poly",
                      offset=[offset.x + 2 * self.pmos.active_contact.width + 4 * drc["minwidth_poly"],
                              offset.y],
                      width=drc["minwidth_poly"],
                      height=poly_length)

    def connect_drains(self):
        """  Connect pmos and nmos drains. The output will be routed to this connection point. """
        yoffset = drc["minwidth_metal1"] + (self.nmos.active_contact_positions[0].y 
                                                - drc["well_enclosure_active"]
                                                + drc["metal1_to_metal1"])
        drain_length = (self.height - yoffset + 0.5 * drc["minwidth_metal1"]
            - (self.pmos.height - self.pmos.active_contact_positions[0].y))
        layer_stack = ("metal1", "via1", "metal2")
        for position in self.pmos.active_contact_positions[1:][::2]:
            diff_active_via = self.pmos.active_contact.width - self.m1m2_via.second_layer_width
            offset = (self.pmos_position2 + self.pmos.active_contact_positions[0]
                          + vector(diff_active_via / 2,0))
            self.add_via(layer_stack,offset)

            width = (2 * self.pmos.active_width 
                         - self.pmos.active_contact.width 
                         - (self.pmos.active_contact.width 
                                - self.m1m2_via.second_layer_width))
            self.add_rect(layer="metal2",
                          offset=offset,
                          width=width,
                          height=self.m1m2_via.second_layer_width) 

            xoffset = (self.pmos_position3.x + self.pmos.active_contact_positions[1].x
                           + diff_active_via / 2)
            self.add_via(layer_stack,[xoffset,offset.y])

            xoffset = (self.nmos_position3.x + self.nmos.active_position.x
                + self.nmos.active_width - self.nmos.active_contact.width / 2)
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
        offset = self.pmos_position1 + self.pmos.poly_positions[0] - vector(0,self.poly_contact.height)
        via_offset = offset + self.poly_contact.first_layer_position.scale(-1,0) - vector(self.poly_contact.first_layer_width,0) + vector(drc["minwidth_poly"],0)

        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=via_offset)

        self.add_layout_pin(text="A",
                            layer="metal1",
                            offset=offset.scale(0,1),
                            width=offset.x,
                            height=drc["minwidth_metal1"])


    def route_input_gate_B(self):
        """  routing for input B """
        offset = self.pmos_position2 + self.pmos.poly_positions[0] - vector(0,self.poly_contact.height+1*(self.m1m2_via.width+drc["metal1_to_metal1"]))
        via_offset = offset + self.poly_contact.first_layer_position.scale(-1,0) - vector(self.poly_contact.first_layer_width,0) + vector(drc["minwidth_poly"],0)

        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=via_offset)

        self.add_layout_pin(text="B",
                            layer="metal1",
                            offset=offset.scale(0,1),
                            width=offset.x,
                            height=drc["minwidth_metal1"])
    

    def route_input_gate_C(self):
        """  routing for input C """ 
        offset = self.pmos_position3 + self.pmos.poly_positions[0] - vector(0,self.poly_contact.height+2*(self.m1m2_via.width+drc["metal1_to_metal1"]))
        via_offset = offset + self.poly_contact.first_layer_position.scale(-1,0) - vector(self.poly_contact.first_layer_width,0) + vector(drc["minwidth_poly"],0)

        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=via_offset)


        self.add_layout_pin(text="C",
                            layer="metal1",
                            offset=offset.scale(0,1),
                            width=offset.x,
                            height=drc["minwidth_metal1"])

    def route_output(self):
        """  routing for output Z """
        xoffset = self.nmos_position3.x + self.nmos.active_position.x \
            + self.nmos.active_width - self.nmos.active_contact.width / 2
        yoffset = (self.nmos.height + (self.height - drc["minwidth_metal1"] 
                                            - self.pmos.height - self.nmos.height) / 2
                                     - (drc["minwidth_metal1"] / 2))
        self.add_layout_pin(text="Z",
                            layer="metal1",
                            offset=vector(xoffset, yoffset),
                            width=self.well_width - xoffset,
                            height=drc["minwidth_metal1"])


    def extend_wells(self):
        """  extension of well """
        middle_point = self.nmos_position1.y + self.nmos.pwell_position.y \
            + self.nmos.well_height + (self.pmos_position1.y 
                                            + self.pmos.nwell_position.y 
                                            - self.nmos_position1.y 
                                            - self.nmos.pwell_position.y 
                                            - self.nmos.well_height) / 2
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
        self.active_width = self.pmos.active_width \
            + drc["active_to_body_active"] + self.pmos.active_contact.width
        offset = (self.pmos.active_position+self.pmos_position3.scale(1,0)
                      + self.pmos_position1.scale(0,1))
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.pmos.active_height)

        offset = offset + vector(self.pmos.active_width,0)                  
        width = self.active_width - self.pmos.active_width
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=width,
                      height=self.pmos.active_height)

        offset = [self.nmos_position3.x + self.nmos.active_position.x,
                  self.nmos_position1.y + self.nmos.height 
                      - self.nmos.active_position.y - self.nmos.active_height]
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.nmos.active_height)

        offset = offset + vector(self.nmos.active_width,0)
        width = self.active_width - self.nmos.active_width
        self.add_rect(layer="pimplant",
                      offset=offset,
                      width=width,
                      height=self.nmos.active_height)


    def input_load(self):
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def analytical_delay(self, slew, load=0.0):
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
