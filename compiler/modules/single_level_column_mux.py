import design
import debug
from tech import drc, info
from vector import vector
import contact
from ptx import ptx
from globals import OPTS

class single_level_column_mux(design.design):
    """
    This module implements the columnmux bitline cell used in the design.
    Creates a single columnmux cell.
    """

    def __init__(self, tx_size):
        name="single_level_column_mux_{}".format(tx_size)
        design.design.__init__(self, name)
        debug.info(2, "create single column mux cell: {0}".format(name))

        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()
        
        self.ptx_width = tx_size * drc["minwidth_tx"]
        self.add_pin_list(["bl", "br", "bl_out", "br_out", "sel", "gnd"])
        self.create_layout()

    def create_layout(self):

        self.add_ptx()
        self.pin_height = 2*self.m2_width
        self.width = self.bitcell.width
        self.height = self.nmos2.uy() + self.pin_height
        self.connect_poly()
        self.add_gnd_rail()
        self.add_bitline_pins()
        self.connect_bitlines()
        self.add_wells()
        
    def add_bitline_pins(self):
        """ Add the top and bottom pins to this cell """

        bl_pos = vector(self.bitcell.get_pin("BL").lx(), 0)
        br_pos = vector(self.bitcell.get_pin("BR").lx(), 0)

        # bl and br
        self.add_layout_pin(text="bl",
                            layer="metal2",
                            offset=bl_pos + vector(0,self.height - self.pin_height),
                            height=self.pin_height)
        self.add_layout_pin(text="br",
                            layer="metal2",
                            offset=br_pos + vector(0,self.height - self.pin_height),
                            height=self.pin_height)
        
        # bl_out and br_out
        self.add_layout_pin(text="bl_out",
                            layer="metal2",
                            offset=bl_pos,
                            height=self.pin_height)
        self.add_layout_pin(text="br_out",
                            layer="metal2",
                            offset=br_pos,
                            height=self.pin_height)


    def add_ptx(self):
        """ Create the two pass gate NMOS transistors to switch the bitlines"""
        
        # Adds nmos1,nmos2 to the module
        self.nmos = ptx(width=self.ptx_width)
        self.add_mod(self.nmos)

        # Space it in the center
        nmos1_position = self.nmos.active_offset.scale(0,1) + vector(0.5*self.bitcell.width-0.5*self.nmos.active_width,0)
        self.nmos1=self.add_inst(name="mux_tx1",
                                 mod=self.nmos,
                                 offset=nmos1_position)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])

        # This aligns it directly above the other tx with gates abutting
        nmos2_position = nmos1_position + vector(0,self.nmos.active_height + self.poly_space)
        self.nmos2=self.add_inst(name="mux_tx2",
                                 mod=self.nmos,
                                 offset=nmos2_position)
        self.connect_inst(["br", "sel", "br_out", "gnd"])


    def connect_poly(self):
        """ Connect the poly gate of the two pass transistors """
        
        height=self.nmos2.get_pin("G").uy() - self.nmos1.get_pin("G").by()
        self.add_layout_pin(text="sel",
                            layer="poly",
                            offset=self.nmos1.get_pin("G").ll(),
                            height=height)


    def connect_bitlines(self):
        """ Connect the bitlines to the mux transistors """
        # These are on metal2
        bl_pin = self.get_pin("bl")
        br_pin = self.get_pin("br")
        bl_out_pin = self.get_pin("bl_out")
        br_out_pin = self.get_pin("br_out")

        # These are on metal1
        nmos1_s_pin = self.nmos1.get_pin("S")
        nmos1_d_pin = self.nmos1.get_pin("D")
        nmos2_s_pin = self.nmos2.get_pin("S")
        nmos2_d_pin = self.nmos2.get_pin("D")

        # Add vias to bl, br_out, nmos2/S, nmos1/D
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=bl_pin.bc())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=br_out_pin.uc())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=nmos2_s_pin.center())
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=nmos1_d_pin.center())
        
        # bl -> nmos2/D on metal1
        # bl_out -> nmos2/S on metal2
        self.add_path("metal1",[bl_pin.ll(), vector(nmos2_d_pin.cx(),bl_pin.by()), nmos2_d_pin.center()])
        # halfway up, move over
        mid1 = bl_out_pin.uc().scale(1,0.5)+nmos2_s_pin.bc().scale(0,0.5)
        mid2 = bl_out_pin.uc().scale(0,0.5)+nmos2_s_pin.bc().scale(1,0.5)        
        self.add_path("metal2",[bl_out_pin.uc(), mid1, mid2, nmos2_s_pin.bc()])
        
        # br -> nmos1/D on metal2
        # br_out -> nmos1/S on metal1
        self.add_path("metal1",[br_out_pin.uc(), vector(nmos1_s_pin.cx(),br_out_pin.uy()), nmos1_s_pin.center()])
        # halfway up, move over
        mid1 = br_pin.bc().scale(1,0.5)+nmos1_d_pin.uc().scale(0,0.5)
        mid2 = br_pin.bc().scale(0,0.5)+nmos1_d_pin.uc().scale(1,0.5)
        self.add_path("metal2",[br_pin.bc(), mid1, mid2, nmos1_d_pin.uc()])        
        

    def add_gnd_rail(self):
        """ Add the gnd rails through the cell to connect to the bitcell array """
        
        gnd_pins = self.bitcell.get_pins("gnd")
        for gnd_pin in gnd_pins:
            # only use vertical gnd pins that span the whole cell
            if gnd_pin.layer == "metal2" and gnd_pin.height >= self.bitcell.height:
                gnd_position = vector(gnd_pin.lx(), 0)
                self.add_layout_pin(text="gnd",
                                    layer="metal2",
                                    offset=gnd_position,
                                    height=self.height)
        
    def add_wells(self):
        """ Add a well and implant over the whole cell. Also, add the pwell contact (if it exists) """
        
        # find right most gnd rail
        gnd_pins = self.bitcell.get_pins("gnd")
        right_gnd = None
        for gnd_pin in gnd_pins:
            if right_gnd == None or gnd_pin.lx()>right_gnd.lx():
                right_gnd = gnd_pin
                
        # Add to the right (first) gnd rail
        m1m2_offset = right_gnd.bc() + vector(0,0.5*self.nmos.poly_height)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=m1m2_offset)
        active_offset = right_gnd.bc() + vector(0,0.5*self.nmos.poly_height)
        self.add_via_center(layers=("active", "contact", "metal1"),
                            offset=active_offset,
                            implant_type="p",
                            well_type="p")


