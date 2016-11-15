import design
import debug
from tech import drc
from vector import vector
from contact import contact
from ptx import ptx
from globals import OPTS

class single_level_column_mux(design.design):
    """
    This module implements the columnmux bitline cell used in the design.
    Creates a single columnmux cell.
    """

    def __init__(self, name, tx_size):
        design.design.__init__(self, name)
        debug.info(2, "create single columnmux cell: {0}".format(name))

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        self.tx_size = tx_size
        self.ptx_width = self.tx_size * drc["minwidth_tx"]
        self.add_pins()
        self.create_layout()

    def add_pins(self):
        self.add_pin_list(["bl", "br", "bl_out", "br_out", "sel", "gnd"])

    def create_layout(self):

        # This is not instantiated and used for calculations only.
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.pwell_contact = contact(layer_stack=("active", "contact", "metal1"))

        self.create_ptx()
        self.add_ptx()
        self.connect_poly()
        self.connect_to_bitlines()
        self.add_gnd_rail()
        self.add_well_contacts()
        self.setup_layout_constants()

    def create_ptx(self):
        """Initializes the nmos1 and nmos2 transistors"""
        self.nmos1 = ptx(name="nmos1",
                         width=self.ptx_width,
                         mults=1,
                         tx_type="nmos")
        self.add_mod(self.nmos1)
        self.nmos2 = ptx(name="nmos2",
                         width=self.ptx_width,
                         mults=1,
                         tx_type="nmos")
        self.nmos2 = self.nmos2        
        self.add_mod(self.nmos2)

    def add_ptx(self):
        # Adds nmos1,nmos2 to the module
        self.nmos1_position = (vector(drc["minwidth_metal1"],
                                      drc["poly_extend_active"])
                                   - vector([drc["well_enclosure_active"]]*2))
        self.add_inst(name="M_1",
                      mod=self.nmos1,
                      offset=self.nmos1_position)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])

        nmos2_to_nmos1 = vector(self.nmos1.active_width,
                                self.nmos1.active_height + drc["minwidth_poly"] 
                                   + 2* drc["poly_extend_active"])
        self.nmos2_position = self.nmos1_position + nmos2_to_nmos1
        self.add_inst(name="M_2",
                      mod=self.nmos2,
                      offset=self.nmos2_position)
        self.connect_inst(["br", "sel", "br_out", "gnd"])

    def connect_poly(self):
        self.poly_offset = (self.nmos1_position 
                                + self.nmos1.poly_positions[0]
                                + vector(0,self.nmos1.poly_height))
        width=self.nmos2_position.x- self.nmos1_position.x+ drc["minwidth_poly"]
        self.poly = self.add_rect(layer="poly",
                                  offset=self.poly_offset,
                                  width=width,
                                  height=drc["minwidth_poly"])
        self.add_label(text="col_addr",
                       layer="poly",
                       offset=self.poly_offset)

    def connect_to_bitlines(self):
        offset = [self.nmos1.active_contact_positions[0].x + self.m1m2_via.contact_width / 2 
                  + 3 * (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) / 2,
                  self.nmos1.active_position.y+ self.nmos1.active_height]
        offset = self.nmos1_position + offset
        connection = vector(0, 
                            self.nmos2.active_height+ 2 * drc["poly_extend_active"] \
                            + drc["minwidth_poly"] + drc["minwidth_metal2"])
        self.add_rect(layer="metal2",
                      offset=offset,
                      width=drc["minwidth_metal2"],
                      height=connection.y - drc["minwidth_metal2"])

        self.BL_position = (vector(self.bitcell_chars["BL"][0]- 0.5 * self.m1m2_via.width,
                                   offset.y)
                                + connection)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset,
                     mirror="MX")
        self.add_label(text="bl",
                       layer="metal2",
                       offset=self.BL_position)

        self.add_rect(layer="metal2",
                      offset=self.BL_position - vector(0, 2 * drc["minwidth_metal2"]),
                      width=drc["minwidth_metal2"],
                      height=2 * drc["minwidth_metal2"])

        width = self.bitcell_chars["BL"][0]- 0.5 * self.m1m2_via.width - offset.x+ drc["minwidth_metal2"]
        self.add_rect(layer="metal2",
                      offset=[offset[0],
                              self.BL_position.y- 2*drc["minwidth_metal2"]],
                      width=width,
                      height=drc["minwidth_metal2"])

        offset = self.nmos1_position + self.nmos1.active_contact_positions[1]
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)
        self.add_rect(layer="metal2",
                      offset=[self.bitcell_chars["BL"][0]- 0.5 * self.m1m2_via.width,
                              0],
                      width=drc["minwidth_metal2"],
                      height=(drc["minwidth_metal2"] + offset[1]))
        self.add_rect(layer="metal2",
                      offset=[self.bitcell_chars["BL"][0]- 0.5 * self.m1m2_via.width,
                              offset[1]],
                      width=(offset.x- self.bitcell_chars["BL"][0]- 0.5 * self.m1m2_via.width
                             + 2 * drc["minwidth_metal2"]),
                      height=drc["minwidth_metal2"])
        self.BL_out_position = vector(self.bitcell_chars["BL"][0]- 0.5*  self.m1m2_via.width, 
                                      0)
        self.add_label(text="bl_out",
                       layer="metal2",
                       offset=self.BL_out_position)

        offset = [self.nmos2.active_contact_positions[1].x - self.m1m2_via.contact_width / 2,
                  self.nmos2.active_position.y+ self.nmos2.active_height]
        offset = self.nmos2_position + offset
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset,
                     mirror="MX")
        mid = offset + vector(drc["minwidth_metal2"],0)
        self.add_rect(layer="metal2",
                      offset= mid,
                      width= (self.bitcell_chars["BR"][0]- mid.x+ 0.5*self.m1m2_via.width),
                      height=-drc["minwidth_metal2"])
        self.add_rect(layer="metal2",
                      offset=[self.bitcell_chars["BR"][0]- 0.5*self.m1m2_via.width,
                              offset.y- drc["metal1_to_metal1"]],
                      width=drc["minwidth_metal2"],
                      height=2*drc["minwidth_metal2"])
        self.BR_position = vector(self.bitcell_chars["BR"][0]- 0.5 * self.m1m2_via.width,
                                  self.BL_position.y)
        self.add_label(text="br",
                       layer="metal2",
                       offset=self.BR_position)

        offset = self.nmos2_position + self.nmos2.active_contact_positions[0]
        self.BR_out_position = vector(self.bitcell_chars["BR"][0]- 0.5 * self.m1m2_via.width,
                                      0)
        self.add_label(text="br_out",
                       layer="metal2",
                       offset=self.BR_out_position)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)
        self.add_rect(layer="metal2",
                      offset=offset,
                      width=self.BR_out_position.x - offset[0],
                      height=drc["minwidth_metal2"])
        self.add_rect(layer="metal2",
                      offset=[self.BR_out_position.x,
                              offset.y+ drc["minwidth_metal2"]],
                      width=drc["minwidth_metal2"],
                      height=-(offset.y+ drc["minwidth_metal2"]))

    def add_gnd_rail(self):
        self.gnd_position = vector(self.bitcell_chars["gnd"][0]- 0.5 * self.m1m2_via.width,
                                   0)
        self.add_layout_pin(text="gnd",
                      layer="metal2",
                      offset=self.gnd_position,
                      width=drc["minwidth_metal2"],
                      height=self.BL_position[1])

    def add_well_contacts(self):
        offset = vector(self.gnd_position.x+ drc["minwidth_metal2"],
                        self.nmos1.poly_height / 2)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset - vector(self.m1m2_via.width / 2, 0),
                     mirror="MY")
        self.add_contact(layers=("active", "contact", "metal1"),
                         offset=offset - vector(self.m1m2_via.width, 0),
                         mirror="MY")
        temp = vector(self.m1m2_via.width,
                      (self.pwell_contact.first_layer_height - self.pwell_contact.second_layer_height) / 2)
        offset_implant = offset - temp + vector([drc["implant_to_contact"]]*2).scale(1,-1)
        self.add_rect(layer="pimplant",
                      offset=offset_implant,
                      width=-(2*drc["implant_to_contact"] + self.pwell_contact.first_layer_width),
                      height=2*drc["implant_to_contact"] + self.pwell_contact.width)

        offset_well = self.nmos1_position + vector(self.nmos1.width, 0)
        self.add_rect(layer="pwell",
                      offset=offset_well,
                      width=self.gnd_position.x+ drc["minwidth_metal2"] - offset_well[0],
                      height=self.nmos1.height + drc["minwidth_poly"])
        self.add_rect(layer="vtg",
                      offset=offset_well,
                      width=self.gnd_position.x+ drc["minwidth_metal2"] - offset_well[0],
                      height=self.nmos1.height + drc["minwidth_poly"])

    def setup_layout_constants(self):
        self.width = self.width = self.bitcell_chars["width"]
        self.height = self.height = self.BL_position[1]
