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

    def __init__(self, nmos_width=1, height=bitcell.chars["height"]):
        """ Constructor """
        name = "nand2_{0}".format(nand_2.unique_id)
        nand_2.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "create nand_2 strcuture {0} with size of {1}".format(
            name, nmos_width))

        self.nmos_width = nmos_width
        self.mults = int(self.nmos_width/(2*drc["minwidth_tx"])) 
        self.height = height

        self.add_pins()
        self.create_unit()
        self.add_nand()
        if self.mults >1:
            self.connect_A()
            self.connect_B()
            self.connect_Z()
        self.A_position = self.nand_2_sub.A_position
        self.B_position = self.nand_2_sub.B_position
        self.Z_position = vector((self.mults-1)* self.nand_2_sub.width,0) + self.nand_2_sub.Z_position
        self.vdd_position = self.nand_2_sub.vdd_position
        self.gnd_position = self.nand_2_sub.gnd_position
        self.width = self.mults * self.nand_2_sub.width
        self.height = self.nand_2_sub.height
        self.DRC_LVS()

    def add_pins(self):
        """ Add pins """
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_unit(self):
        self.nand_2_sub = nand_2_unit(nmos_width=2 *drc["minwidth_tx"])
        self.add_mod(self.nand_2_sub)

    def add_nand(self):
        for  i in range(self.mults):
            nand2_offset_i = vector(self.nand_2_sub.width*i,0)   
            self.add_inst(name=self.name+"sub"+str(i),
                          mod=self.nand_2_sub,
                          offset=nand2_offset_i)
            self.connect_inst(["A", "B", "Z", "vdd", "gnd"])

    def connect_A(self):
        for i in range(self.mults):
            offset = self.nand_2_sub.A_position + vector(i* self.nand_2_sub.width,0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate = 90,
                             mirror = "MX")
        start = self.nand_2_sub.A_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal2",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal2"])


    def connect_B(self):
        for i in range(self.mults):
            offset = self.nand_2_sub.B_position + vector(i* self.nand_2_sub.width,0)
            self.add_contact(layers=("metal1", "via1", "metal2"),
                             offset=offset,
                             rotate = 270,
                             mirror = "MY")
        start = self.nand_2_sub.B_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal2",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal2"])


    def connect_Z(self):
        start = self.nand_2_sub.Z_position
        end = start + vector((self.mults-1)* self.nand_2_sub.width,0)
        self.add_rect(layer="metal1",
                      offset = start,
                      width = (self.mults-1)* self.nand_2_sub.width,
                      height = drc["minwidth_metal1"])

    def input_load(self):
        from tech import parameter
        return (self.nmos_width/parameter["min_tx_size"])*0.5

    def delay(self, slew, load=0.0):
        from tech import parameter
        r = 9250.0/(self.nmos_width/parameter["min_tx_size"])
        c_para = 0.7*(self.nmos_width/parameter["min_tx_size"])#ff
        if isinstance(load, float):
            result = self.cal_delay_with_rc(r = r, c =  c_para+load, slew =slew)
        else:
            driver = [r,c_para]
            result= self.wire_delay(slew=slew, driver=driver, wire=load)
        return result

class nand_2_unit(design.design):
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
    
    def __init__(self, nmos_width=1, height=bitcell.chars["height"]):
        """Constructor : Creates a cell for a simple 2 input nand"""
        name = "nand2_{0}_unit".format(nand_2.unique_id)
        nand_2.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "create nand_2 structure {0} with size of {1}".format(
            name, nmos_width))

        self.nmos_width = nmos_width
        self.height = height

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        """ Add pins """
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ Layout """
        self.determine_sizes()
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
        self.setup_layout_offsets()

    # Determine transistor size
    def determine_sizes(self):
        """ Determine the size of the transistors """
        self.nmos_size = self.nmos_width
        self.pmos_size = self.nmos_width
        self.tx_mults = 1

    # transistors are created here but not yet placed or added as a module
    def create_ptx(self):
        """ Add required modules """
        self.nmos1 = ptx(width=self.nmos_size,
                         mults=self.tx_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos1)
        self.nmos2 = ptx(width=self.nmos_size,
                         mults=self.tx_mults,
                         tx_type="nmos")
        self.add_mod(self.nmos2)

        self.pmos1 = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos1)
        self.pmos2 = ptx(width=self.pmos_size,
                         mults=self.tx_mults,
                         tx_type="pmos")
        self.add_mod(self.pmos2)

    def setup_layout_constants(self):
        """ Calculate the layout constraints """
        self.well_width = self.pmos1.active_position.x \
            + 2 * self.pmos1.active_width \
            + drc["active_to_body_active"] + \
            drc["well_enclosure_active"]

        self.width = self.well_width

    def add_rails(self):
        """ add power rails """
        rail_width = self.width
        rail_height = drc["minwidth_metal1"]
        self.rail_height = rail_height
        # Relocate the origin
        self.gnd_position = vector(0, - 0.5 * drc["minwidth_metal1"])
        self.add_rect(layer="metal1",
                      offset=self.gnd_position,
                      width=rail_width,
                      height=rail_height)
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=self.gnd_position)

        self.vdd_position = vector(0, self.height - 0.5 * drc["minwidth_metal1"])
        self.add_rect(layer="metal1", 
                      offset=self.vdd_position,
                      width=rail_width,
                      height=rail_height)
        self.add_label(text="vdd",
                       layer="metal1", 
                       offset=self.vdd_position)

    def add_ptx(self):
        """  transistors are added and placed inside the layout         """

        # determines the spacing between the edge and nmos (rail to active
        # metal or poly_to_poly spacing)
        edge_to_nmos = max(drc["metal1_to_metal1"]
                            - self.nmos1.active_contact_positions[0].y,
                           0.5 * (drc["poly_to_poly"] - drc["minwidth_metal1"])
                             - self.nmos1.poly_positions[0].y)

        # determine the position of the first transistor from the left
        self.nmos_position1 = vector(0, 0.5 * drc["minwidth_metal1"] + edge_to_nmos)
        offset = self.nmos_position1+ vector(0,self.nmos1.height)
        self.add_inst(name="nmos1",
                      mod=self.nmos1,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["Z", "A", "net1", "gnd"])

        self.nmos_position2 = vector(self.nmos2.active_width - self.nmos2.active_contact.width, 
                                     self.nmos_position1.y)
        offset = self.nmos_position2 + vector(0,self.nmos2.height)
        self.add_inst(name="nmos2",
                      mod=self.nmos2,
                      offset=offset,
                      mirror="MX")
        self.connect_inst(["net1", "B", "gnd", "gnd"])

        # determines the spacing between the edge and pmos
        edge_to_pmos = max(drc["metal1_to_metal1"] \
                               - self.pmos1.active_contact_positions[0].y,
                           0.5 * drc["poly_to_poly"] - 0.5 * drc["minwidth_metal1"] \
                               - self.pmos1.poly_positions[0].y)

        self.pmos_position1 = vector(0, self.height - 0.5 * drc["minwidth_metal1"] 
                                         - edge_to_pmos - self.pmos1.height)
        self.add_inst(name="pmos1",
                      mod=self.pmos1,
                      offset=self.pmos_position1)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos_position2 = vector(self.nmos_position2.x, self.pmos_position1.y)
        self.add_inst(name="pmos2",
                      mod=self.pmos2,
                      offset=self.pmos_position2)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

    def add_well_contacts(self):
        """  Create and add well copntacts """
        # create well contacts
        layer_stack = ("active", "contact", "metal1")

        xoffset = (self.nmos_position2.x + self.pmos1.active_position.x 
                   + self.pmos1.active_width + drc["active_to_body_active"])
        yoffset = (self.pmos_position1.y +
                  self.pmos1.active_contact_positions[0].y)
        offset = self.nwell_contact_position = vector(xoffset, yoffset)
        self.pwell_contact=self.add_contact(layer_stack,offset,(1,self.nmos1.num_of_tacts))

        xoffset = (self.nmos_position2.x + self.nmos1.active_position.x
                   + self.nmos1.active_width + drc["active_to_body_active"])
        yoffset = (self.nmos_position1.y + self.nmos1.height
                   - self.nmos1.active_contact_positions[0].y
                   - self.nmos1.active_contact.height)
        offset = self.pwell_contact_position = vector(xoffset, yoffset)
        self.nwell_contact=self.add_contact(layer_stack,offset,(1,self.pmos1.num_of_tacts))

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

        well_tap_length = self.nmos1.active_height
        offset = (self.pwell_contact_position.scale(1,0) 
                        + self.pwell_contact.second_layer_position.scale(1,0) 
                        - self.pwell_contact.first_layer_position.scale(1,0)) 
        self.add_rect(layer="metal1",
                      offset=offset, width=drc["minwidth_metal1"],
                      height=well_tap_length)

    def connect_rails(self):
        """  Connect transistor pmos drains to vdd and nmos drains to gnd rail """
        correct = vector(self.pmos1.active_contact.width - drc["minwidth_metal1"],
                         0).scale(.5,0)
        poffset = self.pmos_position1 + self.pmos1.active_contact_positions[0] + correct
        temp_height = self.height - poffset.y
        self.add_rect(layer="metal1",
                      offset=poffset, width=drc["minwidth_metal1"],
                      height=temp_height)

        poffset = vector(2 * self.pmos_position2.x + correct.x
                         + self.pmos2.active_contact_positions[0].x , poffset.y)
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
        """ Connect tx poly znd drains """
        self.connect_poly()
        self.connect_drains()

    def connect_poly(self):
        """ poly connection """
        yoffset_nmos1 = (self.nmos_position1.y 
                            + self.nmos1.poly_positions[0].y 
                            + self.nmos1.poly_height)
        poly_length = (self.pmos_position1.y + self.pmos1.poly_positions[0].y 
                          - yoffset_nmos1 + drc["minwidth_poly"])
        for position in self.pmos1.poly_positions:
            offset = vector(position.x,
                            yoffset_nmos1 - 0.5 * drc["minwidth_poly"])
            self.add_rect(layer="poly",
                          offset=offset, width=drc["minwidth_poly"],
                          height=poly_length)
            self.add_rect(layer="poly",
                          offset=[offset.x + self.pmos1.active_contact.width + 2 * drc["minwidth_poly"],
                                  offset.y],
                          width=drc["minwidth_poly"],
                          height=poly_length)

    def connect_drains(self):
        """  Connect pmos and nmos drains. The output will be routed to this connection point. """
        yoffset = self.nmos_position1.y + self.nmos1.active_contact_positions[0].y
        drain_length = (self.height + self.pmos1.active_contact_positions[0].y 
                        - yoffset - self.pmos1.height + 0.5 * drc["minwidth_metal2"])

        for position in self.pmos1.active_contact_positions[1:][::2]:
            start = self.drain_position = vector(position.x + 0.5 * drc["minwidth_metal1"] 
                                                + self.pmos_position2.x 
                                                + self.pmos2.active_contact.first_layer_position.x 
                                                + self.pmos2.active_contact.width / 2, 
                                           yoffset)
            mid1 = vector(start.x,
                    self.height - drc["minwidth_metal2"] - drc["metal2_to_metal2"] -
                    self.pmos_size - drc["metal1_to_metal1"] - 0.5 * drc["minwidth_metal1"])
            end = vector(position.x + 0.5 * drc["minwidth_metal1"]
                       + self.pmos2.active_contact.second_layer_position.x,
                   self.pmos_position1.y + self.pmos1.active_contact_positions[0].y)
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

        xoffset = self.pmos1.poly_positions[0].x
        yoffset = (self.height 
                       - (drc["minwidth_metal1"] 
                              + drc["metal1_to_metal1"] 
                              + self.pmos2.active_height 
                              + drc["metal1_to_metal1"] 
                              + self.pmos2.active_contact.second_layer_width))
        if (self.nmos_width == drc["minwidth_tx"]):
            yoffset = (self.pmos_position1.y 
                        + self.pmos1.poly_positions[0].y
                        + drc["poly_extend_active"] 
                        - (self.pmos1.active_contact.height 
                               - self.pmos1.active_height) / 2 
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

        input_length = (self.pmos1.poly_positions[0].x 
                        - self.poly_contact.height)
        yoffset += self.poly_contact.via_layer_position.x
        offset = self.input_position1 = vector(0, yoffset)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=input_length,
                      height=drc["minwidth_metal1"])
        self.add_label(text="A",
                       layer="metal1",
                       offset=offset)

    def route_input_gate_B(self):
        """ routing for input B """
        xoffset = (self.pmos2.poly_positions[0].x
                       + self.pmos_position2.x + drc["minwidth_poly"])
        yoffset = (drc["minwidth_metal1"] 
                       + drc["metal1_to_metal1"]
                       + self.nmos2.active_height
                       + drc["minwidth_metal1"])
        if (self.nmos_width == drc["minwidth_tx"]):
            yoffset = (self.nmos_position1.y 
                        + self.nmos1.poly_positions[0].y 
                        + self.nmos1.poly_height 
                        + drc["metal1_to_metal1"])
        offset = [xoffset, yoffset]
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         size=(1,1),
                         rotate=90)

        input_length = self.pmos2.poly_positions[0].x - self.poly_contact.height
        self.input_position2 = vector(xoffset - self.poly_contact.width, 
                                      yoffset + self.poly_contact.via_layer_position.x)
        self.add_layout_pin(text="B",
                            layer="metal1",
                            offset=self.input_position2.scale(0,1),
                            width=(input_length + self.pmos_position2.x + drc["minwidth_poly"]),
                            height=drc["minwidth_metal1"])

    def route_output(self):
        """ routing for output Z """
        yoffset = (self.nmos1.height - 2 * drc["minwidth_metal1"] / 3 + 
            (self.height - self.pmos1.height - self.nmos1.height - drc["minwidth_metal1"]) / 2 )
        xoffset = self.drain_position.x
        offset = self.output_position = vector(xoffset, yoffset)
        output_length = self.width - xoffset
        self.add_layout_pin(text="Z",
                      layer="metal1",
                      offset=offset,
                      width=output_length,
                      height=drc["minwidth_metal1"])

    def extend_wells(self):
        """ Extension of well """
        middle_point = (self.nmos_position1.y + self.nmos1.pwell_position.y
                           + self.nmos1.well_height
                           + (self.pmos_position1.y + self.pmos1.nwell_position.y
                               - self.nmos_position1.y - self.nmos1.pwell_position.y
                               - self.nmos1.well_height) / 2)
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
        self.active_width = (self.pmos1.active_width
                                + drc["active_to_body_active"] 
                                + self.pmos1.active_contact.width)
        offset = (self.pmos1.active_position
                     + self.pmos_position2.scale(1,0)
                     + self.pmos_position1.scale(0,1))
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

        offset = vector(self.nmos_position2.x + self.nmos1.active_position.x,
                        self.nmos_position1.y - self.nmos1.active_height
                            - self.nmos1.active_position.y + self.nmos1.height)
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
        """ Defining the position of i/o pins for the two input nand gate """
        self.A_position = self.A_position = self.input_position1
        self.B_position = self.B_position = self.input_position2
        self.Z_position = self.Z_position = self.output_position
        self.vdd_position = self.vdd_position
        self.gnd_position = self.gnd_position

    def input_load(self):
        from tech import spice
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def delay(self, slew, load=0.0):
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
