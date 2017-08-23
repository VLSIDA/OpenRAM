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
        self.bitcell = self.mod_bitcell()
        
        self.ptx_width = tx_size * drc["minwidth_tx"]
        self.add_pin_list(["bl", "br", "bl_out", "br_out", "sel", "gnd"])
        self.create_layout()

    def create_layout(self):

        # This is not instantiated and used for calculations only.
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.well_contact = contact(layer_stack=("active", "contact", "metal1"))

        self.create_ptx()

        self.width = self.bitcell.width
        # The height is bigger than necessary.
        self.height = 2*self.nmos.height 
        self.connect_poly()
        self.connect_to_bitlines()
        self.add_gnd_rail()
        self.add_well_contacts()
        
        


    def create_ptx(self):
        """ Create the two pass gate NMOS transistors to switch the bitlines"""
        
        # Adds nmos1,nmos2 to the module
        self.nmos = ptx(width=self.ptx_width)
        self.add_mod(self.nmos)

        self.nmos1_position = vector(drc["minwidth_metal1"], drc["poly_extend_active"]) \
                              - vector([drc["well_enclosure_active"]]*2)
        self.add_inst(name="mux_tx1",
                      mod=self.nmos,
                      offset=self.nmos1_position)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])

        nmos2_to_nmos1 = vector(self.nmos.active_width,
                                self.nmos.active_height + drc["minwidth_poly"] + 2*drc["poly_extend_active"])
        self.nmos2_position = self.nmos1_position + nmos2_to_nmos1
        self.add_inst(name="mux_tx2",
                      mod=self.nmos,
                      offset=self.nmos2_position)
        self.connect_inst(["br", "sel", "br_out", "gnd"])


    def connect_poly(self):
        """ Connect the poly gate of the two pass transistors """
        
        self.poly_offset = self.nmos1_position + self.nmos.poly_positions[0] \
                           + vector(0,self.nmos.poly_height)
        width=self.nmos2_position.x - self.nmos1_position.x + drc["minwidth_poly"]
        self.add_layout_pin(text="col_addr",
                            layer="poly",
                            offset=self.poly_offset,
                            width=width,
                            height=drc["minwidth_poly"])

    def connect_to_bitlines(self):
        """ """

        # place the contact at the top of the src/drain
        offset = self.nmos1_position + vector(self.nmos.active_contact_positions[0].x + 0.5*self.m1m2_via.contact_width
                                              + 3 * (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width),
                                              self.nmos.active_position.y + self.nmos.active_height - self.m1m2_via.height)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)

        bl_offset = vector(self.bitcell.get_pin("BL").lx(),self.height)
        self.add_layout_pin(text="bl",
                            layer="metal2",
                            offset=bl_offset - vector(0, 2*drc["minwidth_metal2"]),
                            width=drc["minwidth_metal2"],
                            height=2*drc["minwidth_metal2"])
        # draw an enclosing rectangle for the small jog
        start = offset + vector(0.5*self.m1m2_via.width,0.5*self.m1m2_via.height)
        end = self.get_pin("bl").bc()
        mid1 = vector(start.x,0.5*(start.y+end.y))
        mid2 = vector(end.x,mid1.y)
        self.add_path("metal2",[start,mid1,mid2,end])

        # place the contact at the bottom of the src/drain
        offset = self.nmos1_position + self.nmos.active_contact_positions[1]
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)
        self.add_rect(layer="metal2",
                      offset=[self.bitcell.get_pin("BL").lx(), offset.y],
                      width=(offset.x - self.bitcell.get_pin("BL").lx() + 2*drc["minwidth_metal2"]),
                      height=drc["minwidth_metal2"])
        self.add_layout_pin(text="bl_out",
                      layer="metal2",
                      offset=[self.bitcell.get_pin("BL").lx(), 0],
                      width=drc["minwidth_metal2"],
                      height=drc["minwidth_metal2"] + offset.y)

        BL_out_position = vector(self.bitcell.get_pin("BL").lx()- 0.5*self.m1m2_via.width, 0)


        # place the contact at the top of the src/drain
        offset = self.nmos2_position + vector(self.nmos.active_contact_positions[1].x - 0.5*self.m1m2_via.contact_width
                                              - 2 * (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width),
                                              self.nmos.active_position.y + self.nmos.active_height - self.m1m2_via.height)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)
 
        br_offset = vector(self.bitcell.get_pin("BR").lx(),self.height) - vector(0,2*drc["minwidth_metal2"])
        self.add_layout_pin(text="br",
                            layer="metal2",
                            offset=br_offset,
                            width=drc["minwidth_metal2"],
                            height=2*drc["minwidth_metal2"])

        # draw an enclosing rectangle for the small jog
        ll = vector(min(offset.x,br_offset.x),min(offset.y,br_offset.y))
        ur = vector(max(offset.x+self.m1m2_via.width,br_offset.x+drc["minwidth_metal2"]),
                    max(offset.y+self.m1m2_via.height,br_offset.y+2*drc["minwidth_metal2"]))
        self.add_rect(layer="metal2",
                      offset=ll,
                      width=ur.x-ll.x,
                      height=ur.y-ll.y)


        # place the contact in the bottom
        offset = self.nmos2_position + self.nmos.active_contact_positions[0]
        BR_out_position = vector(self.bitcell.get_pin("BR").lx(), 0)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)
        self.add_rect(layer="metal2",
                      offset=offset,
                      width=BR_out_position.x - offset.x,
                      height=drc["minwidth_metal2"])
        self.add_layout_pin(text="br_out",
                            layer="metal2",
                            offset=[BR_out_position.x, 0],
                            height=offset.y+ drc["minwidth_metal2"])

    def add_gnd_rail(self):
        gnd_pins = self.bitcell.get_pins("gnd")
        for gnd_pin in gnd_pins:
            # only use vertical gnd pins that span the whole cell
            if gnd_pin.layer == "metal2" and gnd_pin.height >= self.bitcell.height:
                gnd_position = vector(gnd_pin.lx(), 0)
                self.add_layout_pin(text="gnd",
                                    layer="metal2",
                                    offset=gnd_position,
                                    height=self.get_pin("bl").uy())
        
    def add_well_contacts(self):
        # find right most gnd rail
        gnd_pins = self.bitcell.get_pins("gnd")
        right_gnd = None
        for gnd_pin in gnd_pins:
            if right_gnd == None or gnd_pin.lx()>right_gnd.lx():
                right_gnd = gnd_pin
                
        # Add to the right (first) gnd rail
        m1m2_offset = right_gnd.ll() + vector(-0.5*self.m1m2_via.width,self.nmos.poly_height/2)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=m1m2_offset)
        active_offset = right_gnd.ll() + vector(-self.m1m2_via.width,self.nmos.poly_height/2)
        self.add_contact(layers=("active", "contact", "metal1"),
                         offset=active_offset)

        offset_implant = active_offset + vector([drc["implant_to_contact"]]*2).scale(-1,-1)
        implant_width = 2*drc["implant_to_contact"] + self.well_contact.width
        implant_height = 2*drc["implant_to_contact"] + self.well_contact.height        
        self.add_rect(layer="pimplant",
                      offset=offset_implant,
                      width=implant_width,
                      height=implant_height)

        offset_well = self.nmos1_position + vector(self.nmos.width, 0)
        self.add_rect(layer="pwell",
                      offset=offset_well,
                      width=offset_implant.x + implant_width + drc["well_enclosure_active"] - offset_well.x,
                      height=self.nmos2_position.y)
        self.add_rect(layer="vtg",
                      offset=offset_well,
                      width=offset_implant.x + implant_width + drc["well_enclosure_active"] - offset_well.x,
                      height=self.nmos2_position.y)

