import contact
import design
import debug
from tech import drc, parameter, spice
from ptx import ptx
from vector import vector
from globals import OPTS

class nand_2(design.design):
    """
    This module generates gds of a parametrically sized 2_input nand.
    This model use ptx to generate a 2_input nand within a cetrain height.
    The 2_input nand's cell_height should be the same as the 6t library cell
    This module doesn't generate multi_finger 2_input nand gate, 
    It generate only the minimum size 2_input nand gate.
    Creates a pcell for a simple 2_input nand
    """

    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)

    unique_id = 1
    
    def __init__(self, nmos_width=2*drc["minwidth_tx"], height=bitcell.height):
        """Constructor : Creates a cell for a simple 2 input nand"""
        name = "nand2_{0}".format(nand_2.unique_id)
        nand_2.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "create nand_2 structure {0} with size of {1}".format(name, nmos_width))

        self.nmos_size = nmos_width
        # FIXME why is this?
        self.pmos_size = nmos_width
        self.tx_mults = 1
        self.height = height

        self.add_pins()
        self.create_layout()
        #self.DRC_LVS()

    def add_pins(self):
        """ Add pins """
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ Layout """
        self.create_ptx()
        self.setup_layout_constants()
        self.add_rails()
        self.add_ptx()
        self.add_well_contacts()

        # This isn't instantiated, but we use it to get the dimensions
        self.poly_contact = contact.contact(("poly", "contact", "metal1"))

        self.connect_well_contacts()
        self.connect_rails()
        self.connect_tx()
        self.route_pins()
        self.extend_wells()
        self.extend_active()

    # transistors are created here but not yet placed or added as a module
    def create_ptx(self):
        """ Add required modules """
        self.nmos = ptx(width=self.nmos_size,
                        mults=self.tx_mults,
                        tx_type="nmos")
        self.add_mod(self.nmos)

        self.pmos = ptx(width=self.pmos_size,
                        mults=self.tx_mults,
                        tx_type="pmos")
        self.add_mod(self.pmos)

    def setup_layout_constants(self):
        """ Calculate the layout constraints """
        self.well_width = self.pmos.active_position.x \
            + 2 * self.pmos.active_width \
            + drc["active_to_body_active"] + \
            drc["well_enclosure_active"]

        self.width = self.well_width

    def add_rails(self):
        """ add power rails """
        rail_width = self.width
        rail_height = drc["minwidth_metal1"]
        self.rail_height = rail_height
        # Relocate the origin
        self.gnd_loc = vector(0, - 0.5 * drc["minwidth_metal1"])
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
        """  transistors are added and placed inside the layout         """

        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        edge_to_nmos = max(drc["metal1_to_metal1"]
                            - self.nmos.active_contact_positions[0].y,
                           0.5 * (drc["poly_to_poly"] - drc["minwidth_metal1"])
                             - self.nmos.poly_positions[0].y)

        # determine the position of the first transistor from the left
        self.nmos_position1 = vector(0, 0.5 * drc["minwidth_metal1"] + edge_to_nmos)
        offset = self.nmos_position1+ vector(0,self.nmos.height)
        self.add_inst(name="nmos1",
                      mod=self.nmos,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["Z", "A", "net1", "gnd"])

        self.nmos_position2 = vector(self.nmos.active_width - self.nmos.active_contact.width, 
                                     self.nmos_position1.y)
        offset = self.nmos_position2 + vector(0,self.nmos.height)
        self.add_inst(name="nmos2",
                      mod=self.nmos,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net1", "B", "gnd", "gnd"])

        # determines the spacing between the edge and pmos
        edge_to_pmos = max(drc["metal1_to_metal1"] \
                               - self.pmos.active_contact_positions[0].y,
                           0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"] \
                               - self.pmos.poly_positions[0].y)

        self.pmos_position1 = vector(0, self.height - 0.5 * drc["minwidth_metal1"] 
                                         - edge_to_pmos - self.pmos.height)
        self.add_inst(name="pmos1",
                      mod=self.pmos,
                      offset=self.pmos_position1)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos_position2 = vector(self.nmos_position2.x, self.pmos_position1.y)
        self.add_inst(name="pmos2",
                      mod=self.pmos,
                      offset=self.pmos_position2)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

    def add_well_contacts(self):
        """  Create and add well copntacts """
        # create well contacts
        layer_stack = ("active", "contact", "metal1")

        xoffset = (self.nmos_position2.x + self.pmos.active_position.x 
                   + self.pmos.active_width + drc["active_to_body_active"])
        yoffset = (self.pmos_position1.y +
                  self.pmos.active_contact_positions[0].y)
        offset = self.nwell_contact_position = vector(xoffset, yoffset)
        self.pwell_contact=self.add_contact(layer_stack,offset,(1,self.nmos.num_contacts))

        xoffset = (self.nmos_position2.x + self.nmos.active_position.x
                   + self.nmos.active_width + drc["active_to_body_active"])
        yoffset = (self.nmos_position1.y + self.nmos.height
                   - self.nmos.active_contact_positions[0].y
                   - self.nmos.active_contact.height)
        offset = self.pwell_contact_position = vector(xoffset, yoffset)
        self.nwell_contact=self.add_contact(layer_stack,offset,(1,self.pmos.num_contacts))

    def connect_well_contacts(self):
        """  Connect well contacts to vdd and gnd rail """
        well_tap_length = (self.height - self.nwell_contact_position.y)
        offset = vector(self.nwell_contact_position.x 
                        + self.nwell_contact.second_layer_position.x 
                        - self.nwell_contact.first_layer_position.x,
                        self.nwell_contact_position.y)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=well_tap_length)

        well_tap_length = self.nmos.active_height
        offset = (self.pwell_contact_position.scale(1,0) 
                        + self.pwell_contact.second_layer_position.scale(1,0) 
                        - self.pwell_contact.first_layer_position.scale(1,0)) 
        self.add_rect(layer="metal1",
                      offset=offset, width=drc["minwidth_metal1"],
                      height=well_tap_length)

    def connect_rails(self):
        """  Connect transistor pmos drains to vdd and nmos drains to gnd rail """
        correct = vector(self.pmos.active_contact.width - drc["minwidth_metal1"],
                         0).scale(.5,0)
        poffset = self.pmos_position1 + self.pmos.active_contact_positions[0] + correct
        temp_height = self.height - poffset.y
        self.add_rect(layer="metal1",
                      offset=poffset, width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = vector(2 * self.pmos_position2.x + correct.x
                         + self.pmos.active_contact_positions[0].x , poffset.y)
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
        """ Connect tx poly znd drains """
        self.connect_poly()
        self.connect_drains()

    def connect_poly(self):
        """ poly connection """
        yoffset_nmos1 = (self.nmos_position1.y 
                            + self.nmos.poly_positions[0].y 
                            + self.nmos.poly_height)
        poly_length = (self.pmos_position1.y + self.pmos.poly_positions[0].y 
                          - yoffset_nmos1 + drc["minwidth_poly"])
        for position in self.pmos.poly_positions:
            offset = vector(position.x,
                            yoffset_nmos1 - 0.5 * drc["minwidth_poly"])
            self.add_rect(layer="poly",
                          offset=offset, width=drc["minwidth_poly"],
                          height=poly_length)
            self.add_rect(layer="poly",
                          offset=[offset.x + self.pmos.active_contact.width + 2 * drc["minwidth_poly"],
                                  offset.y],
                          width=drc["minwidth_poly"],
                          height=poly_length)

    def connect_drains(self):
        """  Connect pmos and nmos drains. The output will be routed to this connection point. """
        yoffset = self.nmos_position1.y + self.nmos.active_contact_positions[0].y
        drain_length = (self.height + self.pmos.active_contact_positions[0].y 
                        - yoffset - self.pmos.height + 0.5 * drc["minwidth_metal2"])

        for position in self.pmos.active_contact_positions[1:][::2]:
            start = self.drain_position = vector(position.x + 0.5 * drc["minwidth_metal1"] 
                                                + self.pmos_position2.x 
                                                + self.pmos.active_contact.first_layer_position.x 
                                                + self.pmos.active_contact.width / 2, 
                                           yoffset)
            mid1 = vector(start.x,
                    self.height - drc["minwidth_metal2"] - drc["metal2_to_metal2"] -
                    self.pmos_size - drc["metal1_to_metal1"] - 0.5 * drc["minwidth_metal1"])
            end = vector(position.x + 0.5 * drc["minwidth_metal1"]
                       + self.pmos.active_contact.second_layer_position.x,
                   self.pmos_position1.y + self.pmos.active_contact_positions[0].y)
            mid2 = vector(end.x, mid1.y)

            self.add_path("metal1",[start, mid1, mid2, end])

    def route_pins(self):
        """ Routing """
        self.route_input_gate()
        self.route_output()

    def route_input_gate(self):
        """ Gate routing """
        self.route_input_gate_A()
        self.route_input_gate_B()

    def route_input_gate_A(self):
        """ routing for input A """

        xoffset = self.pmos.poly_positions[0].x
        yoffset = (self.height 
                       - (drc["minwidth_metal1"] 
                              + drc["metal1_to_metal1"] 
                              + self.pmos.active_height 
                              + drc["metal1_to_metal1"] 
                              + self.pmos.active_contact.second_layer_width))
        if (self.nmos_size == drc["minwidth_tx"]):
            yoffset = (self.pmos_position1.y 
                        + self.pmos.poly_positions[0].y
                        + drc["poly_extend_active"] 
                        - (self.pmos.active_contact.height 
                               - self.pmos.active_height) / 2 
                        - drc["metal1_to_metal1"]  
                        - self.poly_contact.width)

        offset = [xoffset, yoffset]
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         size=(1,1),
                         rotate=90)

        offset = offset - self.poly_contact.first_layer_position.rotate_scale(1,0)
        self.add_rect(layer="poly",
                      offset=offset,
                      width=self.poly_contact.first_layer_position.y + drc["minwidth_poly"],
                      height=self.poly_contact.first_layer_width)

        input_length = (self.pmos.poly_positions[0].x 
                        - self.poly_contact.height)
        yoffset += self.poly_contact.via_layer_position.x
        offset = self.input_position1 = vector(0, yoffset)
        self.add_layout_pin(text="A",
                            layer="metal1",
                            offset=offset,
                            width=input_length,
                            height=drc["minwidth_metal1"])

    def route_input_gate_B(self):
        """ routing for input B """
        xoffset = (self.pmos.poly_positions[0].x
                       + self.pmos_position2.x + drc["minwidth_poly"])
        yoffset = (drc["minwidth_metal1"] 
                       + drc["metal1_to_metal1"]
                       + self.nmos.active_height
                       + drc["minwidth_metal1"])
        if (self.nmos_size == drc["minwidth_tx"]):
            yoffset = (self.nmos_position1.y 
                        + self.nmos.poly_positions[0].y 
                        + self.nmos.poly_height 
                        + drc["metal1_to_metal1"])
        offset = [xoffset, yoffset]
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         size=(1,1),
                         rotate=90)

        input_length = self.pmos.poly_positions[0].x - self.poly_contact.height
        input_position2 = vector(xoffset - self.poly_contact.width, 
                                 yoffset + self.poly_contact.via_layer_position.x)
        self.add_layout_pin(text="B",
                            layer="metal1",
                            offset=input_position2.scale(0,1),
                            width=(input_length + self.pmos_position2.x + drc["minwidth_poly"]),
                            height=drc["minwidth_metal1"])

    def route_output(self):
        """ routing for output Z """
        yoffset = (self.nmos.height - 2 * drc["minwidth_metal1"] / 3 + 
            (self.height - self.pmos.height - self.nmos.height - drc["minwidth_metal1"]) / 2 )
        xoffset = self.drain_position.x
        offset = vector(xoffset, yoffset)
        output_length = self.width - xoffset
        self.add_layout_pin(text="Z",
                            layer="metal1",
                            offset=offset,
                            width=output_length,
                            height=drc["minwidth_metal1"])

    def extend_wells(self):
        """ Extension of well """
        middle_point = (self.nmos_position1.y + self.nmos.pwell_position.y
                           + self.nmos.well_height
                           + (self.pmos_position1.y + self.pmos.nwell_position.y
                               - self.nmos_position1.y - self.nmos.pwell_position.y
                               - self.nmos.well_height) / 2)
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
                      offset=offset,
                      width=self.well_width,
                      height=self.pwell_height)
        self.add_rect(layer="vtg",
                      offset=offset,
                      width=self.well_width,
                      height=self.pwell_height)

    def extend_active(self):
        """ Extension of active region """
        self.active_width = (self.pmos.active_width
                                + drc["active_to_body_active"] 
                                + self.pmos.active_contact.width)
        offset = (self.pmos.active_position
                     + self.pmos_position2.scale(1,0)
                     + self.pmos_position1.scale(0,1))
        self.add_rect(layer="active",
                      offset=offset,
                      width=self.active_width,
                      height=self.pmos.active_height)

        offset = offset + vector(self.pmos.active_width, 0)
        width = self.active_width - self.pmos.active_width
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=width,
                      height=self.pmos.active_height)

        offset = vector(self.nmos_position2.x + self.nmos.active_position.x,
                        self.nmos_position1.y - self.nmos.active_height
                            - self.nmos.active_position.y + self.nmos.height)
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
        from tech import spice
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def analytical_delay(self, slew, load=0.0):
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
