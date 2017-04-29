from contact import contact
import design
import debug
from tech import drc
from ptx import ptx
from vector import vector
from globals import OPTS

class precharge(design.design):
    """
    Creates a single precharge cell
    This module implements the precharge bitline cell used in the design.
    """

    def __init__(self, name, ptx_width, beta=2):
        design.design.__init__(self, name)
        debug.info(2, "create single precharge cell: {0}".format(name))

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        self.ptx_width = ptx_width
        self.beta = beta

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        self.add_pin_list(["bl", "br", "clk", "vdd"])

    def create_layout(self):
        self.create_ptx()
        self.create_contacts()
        self.setup_layout_constants()
        self.add_ptx()
        self.connect_poly()
        self.add_pclk()
        self.add_nwell_contact()
        self.extend_nwell()
        self.add_vdd_rail()
        self.add_bitlines()
        self.connect_to_bitlines()

    def create_ptx(self):
        """Initializes the upper and lower pmos"""
        self.lower_pmos = ptx(width=self.ptx_width,
                              mults=1, 
                              tx_type="pmos")
        self.add_mod(self.lower_pmos)
        self.upper_pmos = ptx(width=self.beta * self.ptx_width,
                              mults=1,
                              tx_type="pmos")
        self.upper_pmos = self.upper_pmos
        self.add_mod(self.upper_pmos)
        self.temp_pmos = ptx(width=self.beta * self.ptx_width,
                             mults=2,
                             tx_type="pmos")
        self.temp_pmos.remove_source_connect()
        self.temp_pmos.remove_drain_connect()

    def create_contacts(self):
        """Initializes all required contacts/vias for this module"""
        # These aren't for instantiating, but we use them to get the dimensions
        self.nwell_contact = contact(layer_stack=("active", "contact", "metal1"))
        self.poly_contact = contact(layer_stack=("poly", "contact", "metal1"))
        self.upper_dimensions = self.upper_pmos.active_contact.dimensions
        self.lower_dimensions = self.lower_pmos.active_contact.dimensions
        self.upper_contact = contact(layer_stack=("metal1", "via1", "metal2"),
                                     dimensions=self.upper_dimensions)
        self.lower_contact = contact(layer_stack=("metal1", "via1", "metal2"),
                                     dimensions=self.lower_dimensions)

    def setup_layout_constants(self):
        self.width = self.bitcell_chars["width"]
        self.BL_position = vector(self.bitcell_chars["BL"][0], 0)
        self.BR_position = vector(self.bitcell_chars["BR"][0], 0)

    def add_ptx(self):
        """Adds both the upper_pmos and lower_pmos to the module"""
        # adds the lower pmos to layout
        base = vector(self.width - self.temp_pmos.width, 0).scale(0.5,0)
        self.lower_pmos_position = base + vector([drc["metal1_to_metal1"]]*2)
        self.add_inst(name="lower_pmos",
                      mod=self.lower_pmos,
                      offset=self.lower_pmos_position)
        self.connect_inst(["bl", "clk", "br", "vdd"])

        # adds the upper pmos(s) to layout
        ydiff = (self.lower_pmos.height 
                     + 2 * drc["metal1_to_metal1"] 
                     + self.poly_contact.width)
        self.upper_pmos_position = self.lower_pmos_position + vector(0, ydiff)
        self.add_inst(name="upper_pmos1",
                      mod=self.upper_pmos,
                      offset=self.upper_pmos_position)
        self.connect_inst(["bl", "clk", "vdd", "vdd"])

        xdiff =(self.upper_pmos.active_contact_positions[-1].x 
                   - self.upper_pmos.active_contact_positions[0].x)
        self.upper_pmos_position2 = self.upper_pmos_position + vector(xdiff, 0)
        self.add_inst(name="upper_pmos2",
                      mod=self.upper_pmos,
                      offset=self.upper_pmos_position2)
        self.connect_inst(["br", "clk", "vdd", "vdd"])

    def connect_poly(self):
        """Connects the upper and lower pmos together"""
        offset = (self.lower_pmos_position 
                      + self.lower_pmos.poly_positions[0]
                      + vector(0,self.lower_pmos.poly_height))
        # connects the top and bottom pmos' gates together
        ylength = (self.upper_pmos_position.y 
                       + self.upper_pmos.poly_positions[0].y
                       - offset.y) 
        self.add_rect(layer="poly",
                      offset=offset,
                      width=drc["minwidth_poly"],
                      height=ylength)

        # connects the two poly for the two upper pmos(s)
        offset = offset + vector(0, ylength - drc["minwidth_poly"])
        xlength = (self.temp_pmos.poly_positions[-1].x 
                       - self.temp_pmos.poly_positions[0].x
                       + drc["minwidth_poly"])
        self.add_rect(layer="poly",
                      offset=offset,
                      width=xlength,
                      height=drc["minwidth_poly"])

    def add_pclk(self):
        """Adds the pclk input rail, pclk contact/vias, and connects to the pmos"""
        # adds the pclk contact to connect the gates to the pclk rail on metal1
        offset = vector(self.lower_pmos_position.x + self.lower_pmos.poly_positions[0].x 
                            + 0.5 * self.poly_contact.height, 
                        self.upper_pmos_position.y - drc["metal1_to_metal1"] \
                            - self.poly_contact.width)
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=offset,
                         rotate=90)

        # adds the pclk rail on metal1
        offset.y= offset.y + self.poly_contact.second_layer_position.x
        self.pclk_position = vector(0, offset.y)
        self.add_layout_pin(text="clk",
                          layer="metal1",
                          offset=self.pclk_position,
                          width=self.width,
                          height=drc["minwidth_metal1"])
                     
    def add_nwell_contact(self):
        """Adds a nwell tap to connect to the vdd rail"""
        # adds the contact from active to metal1
        offset = vector(self.temp_pmos.active_contact_positions[1].x,
                        self.upper_pmos.height + drc["well_extend_active"] 
                            - self.nwell_contact.first_layer_position.y)
        self.nwell_contact_position = offset + self.upper_pmos_position
        self.add_contact(layers=("active", "contact", "metal1"),
                         offset=self.nwell_contact_position)

        # adds the implant to turn the contact into a nwell tap
        offset = self.nwell_contact_position + self.nwell_contact.first_layer_position
        xlength = self.nwell_contact.first_layer_width
        ylength = self.nwell_contact.first_layer_height
        self.add_rect(layer="nimplant",
                      offset=offset,
                      width=xlength,
                      height=ylength)

    def extend_nwell(self):
        """Extends the nwell for the whole module"""
        self.nwell_position = self.pclk_position.scale(1,0)
        self.height = (self.nwell_contact_position.y + self.nwell_contact.height 
                           - self.nwell_contact.first_layer_position.y
                           + drc["well_extend_active"])
        self.add_rect(layer="nwell",
                      offset=self.nwell_position,
                      width=self.width,
                      height=self.height)

    def add_vdd_rail(self):
        """Adds a vdd rail at the top of the cell"""
        # adds the rail across the width of the cell
        self.vdd_position = vector(self.pclk_position.x,
                                   self.height - drc["minwidth_metal1"])
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=self.vdd_position,
                            width=self.width,
                            height=drc["minwidth_metal1"])

        # connects the upper pmos(s) to the vdd rail
        upper_pmos_contact = (self.upper_pmos.active_contact_positions[1]
                                     + self.upper_pmos_position)
        ylength = self.height - upper_pmos_contact.y
        offset = vector(self.nwell_contact_position.x
                            + self.nwell_contact.second_layer_position.x, 
                        self.upper_pmos.active_contact.second_layer_position.y
                            + upper_pmos_contact.y)
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=drc["minwidth_metal1"],
                      height=ylength)

    def add_bitlines(self):
        """Adds both bit-line and bit-line-bar to the module"""
        # adds the BL on metal 2
        offset = self.BL_position - vector(0.5 * drc["minwidth_metal2"],0)
        self.add_layout_pin(text="bl",
                            layer="metal2",
                            offset=offset,
                            width=drc['minwidth_metal2'],
                            height=self.height)

        # adds the BR on metal 2
        offset = self.BR_position - vector(0.5 * drc["minwidth_metal2"],0)
        self.add_layout_pin(text="br",
                            layer="metal2",
                            offset=offset,
                            width=drc['minwidth_metal2'],
                            height=self.height)

    def connect_to_bitlines(self):
        self.add_bitline_contacts()
        dest =[self.upper_pmos,self.upper_pmos_position,self.upper_contact]
        correct_x = self.xcorrect_upper + self.upper_contact.second_layer_position.x
        self.connect_pmos_to_BL(correct_x,dest)
        correct_x = correct_x + self.temp_pmos.active_contact_positions[-1].x
        self.connect_pmos_to_BR(correct_x,dest)

        dest =[self.lower_pmos,self.lower_pmos_position,self.lower_contact]
        correct_x = self.xcorrect_lower + self.lower_contact.first_layer_position.x
        self.connect_pmos_to_BL(correct_x,dest)
        correct_x = correct_x + self.lower_pmos.active_contact_positions[-1].x
        self.connect_pmos_to_BR(correct_x,dest)

    def add_bitline_contacts(self):
        """Adds contacts/via from metal1 to metal2 for bit-lines"""
        # helps centers the via over the underneath contact
        self.xcorrect_upper = 0.5 * abs(self.upper_contact.width 
                                        - self.upper_pmos.active_contact.width)
        self.xcorrect_lower = 0.5 * abs(self.lower_contact.width 
                                        - self.lower_pmos.active_contact.width)

        # adds contacts from metal1 to metal2 over the active contacts for the
        # upper pmos(s)
        offset = (self.upper_pmos_position  
                      + self.upper_pmos.active_contact_positions[0]
                      + vector(self.xcorrect_upper,0))
        self.add_contact(layers=("metal1", "via1", "metal2"),
                         offset=offset,
                         size=self.upper_dimensions)
        offset.x = (self.upper_pmos_position.x
                        + self.temp_pmos.active_contact_positions[-1].x
                        + self.xcorrect_upper)
        self.add_contact(layers=("metal1", "via1", "metal2"),
                         offset=offset,
                         size=self.upper_dimensions)

        # adds contacts from metal1 to metal 2 over active contacts for the
        # lower pmos
        offset = (self.lower_pmos_position 
                      + self.lower_pmos.active_contact_positions[0]
                      + vector(self.xcorrect_upper,0))
        self.add_contact(layers=("metal1", "via1", "metal2"),
                         offset=offset,
                         size=self.lower_dimensions)
        offset.x = (self.lower_pmos_position.x
                        + self.lower_pmos.active_contact_positions[-1].x
                        + self.xcorrect_lower)
        self.add_contact(layers=("metal1", "via1", "metal2"),
                         offset=offset,
                         size=self.lower_dimensions)

    def connect_pmos_to_BL(self,correct_x,dest):
        """Connects bit-lines to lower_pmos"""
        mos,mos_pos,contact = dest
        mos_active = (mos_pos + mos.active_contact_positions[0])
        offset = vector(self.BL_position.x, mos_active.y)
        xlength = (mos_active.x + correct_x - self.BL_position.x 
                       + 0.5 * drc["minwidth_metal2"])
        self.add_rect(layer="metal2",
                      offset=offset,
                      width=xlength,
                      height=contact.height)

    def connect_pmos_to_BR(self,correct_x,dest):
        """Connects bit-lines to the upper_pmos"""
        mos,mos_pos,contact = dest
        offset = mos_pos + vector(correct_x,
                                  mos.active_contact_positions[0].y)
        xlength = self.BR_position.x - offset.x - 0.5 * drc["minwidth_metal2"] 
        self.add_rect(layer="metal2",
                      offset=offset,
                      width=xlength,
                      height=contact.height)
