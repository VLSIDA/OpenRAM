import contact
import pgate
import debug
from tech import drc, parameter
from ptx import ptx
from vector import vector
from globals import OPTS

class precharge(pgate.pgate):
    """
    Creates a single precharge cell
    This module implements the precharge bitline cell used in the design.
    """

    def __init__(self, name, size=1):
        pgate.pgate.__init__(self, name)
        debug.info(2, "create single precharge cell: {0}".format(name))

        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()
        
        self.beta = parameter["beta"]
        self.ptx_width = self.beta*parameter["min_tx_size"]
        self.width = self.bitcell.width

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        self.add_pin_list(["bl", "br", "en", "vdd"])

    def create_layout(self):
        self.create_ptx()
        self.add_ptx()
        self.connect_poly()
        self.add_en()
        self.add_nwell_and_contact()
        self.add_vdd_rail()
        self.add_bitlines()
        self.connect_to_bitlines()

    def create_ptx(self):
        """Initializes the upper and lower pmos"""
        self.pmos = ptx(width=self.ptx_width,
                        tx_type="pmos")
        self.add_mod(self.pmos)

        # Compute the other pmos2 location, but determining offset to overlap the
        # source and drain pins
        self.overlap_offset = self.pmos.get_pin("D").ll() - self.pmos.get_pin("S").ll()
        


    def add_vdd_rail(self):
        """Adds a vdd rail at the top of the cell"""
        # adds the rail across the width of the cell
        vdd_position = vector(0, self.height - self.m1_width)
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_position,
                            width=self.width,
                            height=self.m1_width)

        self.connect_pin_to_rail(self.upper_pmos2_inst,"S","vdd")
        
    def add_ptx(self):
        """Adds both the upper_pmos and lower_pmos to the module"""
        # adds the lower pmos to layout
        #base = vector(self.width - 2*self.pmos.width + self.overlap_offset.x, 0)
        self.lower_pmos_position = vector(self.bitcell.get_pin("BL").lx(),
                                          self.pmos.active_offset.y)
        self.lower_pmos_inst=self.add_inst(name="lower_pmos",
                                           mod=self.pmos,
                                           offset=self.lower_pmos_position)
        self.connect_inst(["bl", "en", "BR", "vdd"])

        # adds the upper pmos(s) to layout
        ydiff = self.pmos.height + 2*self.m1_space + contact.poly.width
        self.upper_pmos1_pos = self.lower_pmos_position + vector(0, ydiff)
        self.upper_pmos1_inst=self.add_inst(name="upper_pmos1",
                                            mod=self.pmos,
                                            offset=self.upper_pmos1_pos)
        self.connect_inst(["bl", "en", "vdd", "vdd"])

        upper_pmos2_pos = self.upper_pmos1_pos + self.overlap_offset
        self.upper_pmos2_inst=self.add_inst(name="upper_pmos2",
                                            mod=self.pmos,
                                            offset=upper_pmos2_pos)
        self.connect_inst(["br", "en", "vdd", "vdd"])

    def connect_poly(self):
        """Connects the upper and lower pmos together"""

        offset = self.lower_pmos_inst.get_pin("G").ll()
        # connects the top and bottom pmos' gates together
        ylength = self.upper_pmos1_inst.get_pin("G").ll().y - offset.y
        self.add_rect(layer="poly",
                      offset=offset,
                      width=self.poly_width,
                      height=ylength)

        # connects the two poly for the two upper pmos(s)
        offset = offset + vector(0, ylength - self.poly_width)
        xlength = self.upper_pmos2_inst.get_pin("G").lx() - self.upper_pmos1_inst.get_pin("G").lx() + self.poly_width
        self.add_rect(layer="poly",
                      offset=offset,
                      width=xlength,
                      height=self.poly_width)

    def add_en(self):
        """Adds the en input rail, en contact/vias, and connects to the pmos"""
        # adds the en contact to connect the gates to the en rail on metal1
        offset = self.lower_pmos_inst.get_pin("G").ul() + vector(0,0.5*self.poly_space)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                offset=offset,
                                rotate=90)

        # adds the en rail on metal1
        self.add_layout_pin_center_segment(text="en",
                                           layer="metal1",
                                           start=offset.scale(0,1),
                                           end=offset.scale(0,1)+vector(self.width,0))

                     
    def add_nwell_and_contact(self):
        """Adds a nwell tap to connect to the vdd rail"""
        # adds the contact from active to metal1
        well_contact_pos = self.upper_pmos1_inst.get_pin("D").center().scale(1,0) \
                           + vector(0, self.upper_pmos1_inst.uy() + contact.well.height/2 + drc["well_extend_active"])
        self.add_contact_center(layers=("active", "contact", "metal1"),
                                offset=well_contact_pos,
                                implant_type="n",
                                well_type="n")


        self.height = well_contact_pos.y + contact.well.height

        self.add_rect(layer="nwell",
                      offset=vector(0,0),
                      width=self.width,
                      height=self.height)


    def add_bitlines(self):
        """Adds both bit-line and bit-line-bar to the module"""
        # adds the BL on metal 2
        offset = vector(self.bitcell.get_pin("BL").cx(),0) - vector(0.5 * self.m2_width,0)
        self.add_layout_pin(text="bl",
                            layer="metal2",
                            offset=offset,
                            width=drc['minwidth_metal2'],
                            height=self.height)

        # adds the BR on metal 2
        offset = vector(self.bitcell.get_pin("BR").cx(),0) - vector(0.5 * self.m2_width,0)
        self.add_layout_pin(text="br",
                            layer="metal2",
                            offset=offset,
                            width=drc['minwidth_metal2'],
                            height=self.height)

    def connect_to_bitlines(self):
        self.add_bitline_contacts()
        self.connect_pmos(self.lower_pmos_inst.get_pin("S"),self.get_pin("bl"))
        self.connect_pmos(self.lower_pmos_inst.get_pin("D"),self.get_pin("br"))        
        self.connect_pmos(self.upper_pmos1_inst.get_pin("S"),self.get_pin("bl"))        
        self.connect_pmos(self.upper_pmos2_inst.get_pin("D"),self.get_pin("br"))        
        

    def add_bitline_contacts(self):
        """Adds contacts/via from metal1 to metal2 for bit-lines"""

        stack=("metal1", "via1", "metal2")
        pos = self.lower_pmos_inst.get_pin("S").center()
        self.add_contact_center(layers=stack,
                                offset=pos)
        pos = self.lower_pmos_inst.get_pin("D").center()
        self.add_contact_center(layers=stack,
                                offset=pos)
        pos = self.upper_pmos1_inst.get_pin("S").center()
        self.add_contact_center(layers=stack,
                                offset=pos)
        pos = self.upper_pmos2_inst.get_pin("D").center()
        self.add_contact_center(layers=stack,
                                offset=pos)

    def connect_pmos(self, pmos_pin, bit_pin):
        """ Connect pmos pin to bitline pin """

        ll_pos = vector(min(pmos_pin.lx(),bit_pin.lx()), pmos_pin.by())
        ur_pos = vector(max(pmos_pin.rx(),bit_pin.rx()), pmos_pin.uy())

        width = ur_pos.x-ll_pos.x
        height = ur_pos.y-ll_pos.y
        self.add_rect(layer="metal2",
                      offset=ll_pos,
                      width=width,
                      height=height)
        
