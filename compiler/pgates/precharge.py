# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import contact
import design
import debug
from tech import drc, parameter
from vector import vector
from globals import OPTS
from sram_factory import factory

class precharge(design.design):
    """
    Creates a single precharge cell
    This module implements the precharge bitline cell used in the design.
    """
    def __init__(self, name, size=1, bitcell_bl="bl", bitcell_br="br"):

        debug.info(2, "creating precharge cell {0}".format(name))
        design.design.__init__(self, name)

        self.bitcell = factory.create(module_type="bitcell")
        self.beta = parameter["beta"]
        self.ptx_width = self.beta*parameter["min_tx_size"]
        self.width = self.bitcell.width
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br
        
        
        # Creates the netlist and layout
        # Since it has variable height, it is not a pgate.
        self.create_netlist()
        if not OPTS.netlist_only:        
            self.create_layout()
            self.DRC_LVS()

    def create_netlist(self):
        self.add_pins()
        self.add_ptx()
        self.create_ptx()
        
    def create_layout(self):
        self.place_ptx()
        self.connect_poly()
        self.route_en()
        self.place_nwell_and_contact()
        self.route_vdd_rail()
        self.route_bitlines()
        self.connect_to_bitlines()

    def add_pins(self):
        self.add_pin_list(["bl", "br", "en_bar", "vdd"], ["OUTPUT", "OUTPUT", "INPUT", "POWER"])

    def add_ptx(self):
        """
        Initializes the upper and lower pmos
        """
        self.pmos = factory.create(module_type="ptx",
                                   width=self.ptx_width,
                                   tx_type="pmos")
        self.add_mod(self.pmos)

        


    def route_vdd_rail(self):
        """
        Adds a vdd rail at the top of the cell
        """
        
        # Adds the rail across the width of the cell
        vdd_position = vector(0.5*self.width, self.height)
        self.add_rect_center(layer="metal1",
                             offset=vdd_position,
                             width=self.width,
                             height=self.m1_width)

        pmos_pin = self.upper_pmos2_inst.get_pin("S")
        # center of vdd rail
        pmos_vdd_pos = vector(pmos_pin.cx(), vdd_position.y)
        self.add_path("metal1", [pmos_pin.uc(), pmos_vdd_pos])

        # Add vdd pin above the transistor
        self.add_power_pin("vdd", pmos_pin.center(), vertical=True)
        
        
    def create_ptx(self):
        """
        Create both the upper_pmos and lower_pmos to the module
        """

        self.lower_pmos_inst=self.add_inst(name="lower_pmos",
                                           mod=self.pmos)
        self.connect_inst(["bl", "en_bar", "br", "vdd"])

        self.upper_pmos1_inst=self.add_inst(name="upper_pmos1",
                                            mod=self.pmos)
        self.connect_inst(["bl", "en_bar", "vdd", "vdd"])

        self.upper_pmos2_inst=self.add_inst(name="upper_pmos2",
                                            mod=self.pmos)
        self.connect_inst(["br", "en_bar", "vdd", "vdd"])
        

    def place_ptx(self):
        """
        Place both the upper_pmos and lower_pmos to the module
        """

        # Compute the other pmos2 location, but determining offset to overlap the
        # source and drain pins
        overlap_offset = self.pmos.get_pin("D").ll() - self.pmos.get_pin("S").ll()
        # This is how much the contact is placed inside the ptx active
        contact_xdiff = self.pmos.get_pin("S").lx()
        
        # adds the lower pmos to layout
        bl_xoffset = self.bitcell.get_pin(self.bitcell_bl).lx()
        self.lower_pmos_position = vector(max(bl_xoffset - contact_xdiff, self.well_enclose_active),
                                          self.pmos.active_offset.y)
        self.lower_pmos_inst.place(self.lower_pmos_position)

        # adds the upper pmos(s) to layout
        ydiff = self.pmos.height + 2*self.m1_space + contact.poly.width
        self.upper_pmos1_pos = self.lower_pmos_position + vector(0, ydiff)
        self.upper_pmos1_inst.place(self.upper_pmos1_pos)

        upper_pmos2_pos = self.upper_pmos1_pos + overlap_offset
        self.upper_pmos2_inst.place(upper_pmos2_pos)
        
    def connect_poly(self):
        """
        Connects the upper and lower pmos together
        """

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

    def route_en(self):
        """
        Adds the en input rail, en contact/vias, and connects to the pmos
        """
        
        # adds the en contact to connect the gates to the en rail on metal1
        offset = self.lower_pmos_inst.get_pin("G").ul() + vector(0,0.5*self.poly_space)
        self.add_via_center(layers=("poly", "contact", "metal1"),
                            offset=offset)

        # adds the en rail on metal1
        self.add_layout_pin_segment_center(text="en_bar",
                                           layer="metal1",
                                           start=offset.scale(0,1),
                                           end=offset.scale(0,1)+vector(self.width,0))

                     
    def place_nwell_and_contact(self):
        """
        Adds a nwell tap to connect to the vdd rail
        """
        
        # adds the contact from active to metal1
        well_contact_pos = self.upper_pmos1_inst.get_pin("D").center().scale(1,0) \
                           + vector(0, self.upper_pmos1_inst.uy() + contact.well.height/2 + drc("well_extend_active"))
        self.add_via_center(layers=("active", "contact", "metal1"),
                            offset=well_contact_pos,
                            implant_type="n",
                            well_type="n")

        # leave an extra pitch for the height
        self.height = well_contact_pos.y + contact.well.height + self.m1_pitch

        # nwell should span the whole design since it is pmos only
        self.add_rect(layer="nwell",
                      offset=vector(0,0),
                      width=self.width,
                      height=self.height)


    def route_bitlines(self):
        """
        Adds both bit-line and bit-line-bar to the module
        """
        
        # adds the BL on metal 2
        offset = vector(self.bitcell.get_pin(self.bitcell_bl).cx(),0) - vector(0.5 * self.m2_width,0)
        self.bl_pin = self.add_layout_pin(text="bl",
                                          layer="metal2",
                                          offset=offset,
                                          width=drc("minwidth_metal2"),
                                          height=self.height)

        # adds the BR on metal 2
        offset = vector(self.bitcell.get_pin(self.bitcell_br).cx(),0) - vector(0.5 * self.m2_width,0)
        self.br_pin = self.add_layout_pin(text="br",
                                          layer="metal2",
                                          offset=offset,
                                          width=drc("minwidth_metal2"),
                                          height=self.height)

    def connect_to_bitlines(self):
        """
        Connect the bitlines to the devices
        """
        self.add_bitline_contacts()
        self.connect_pmos_m2(self.lower_pmos_inst.get_pin("S"),self.get_pin("bl"))
        self.connect_pmos_m2(self.upper_pmos1_inst.get_pin("S"),self.get_pin("bl"))        
        self.connect_pmos_m1(self.lower_pmos_inst.get_pin("D"),self.get_pin("br"))        
        self.connect_pmos_m1(self.upper_pmos2_inst.get_pin("D"),self.get_pin("br"))
        

    def add_bitline_contacts(self):
        """
        Adds contacts/via from metal1 to metal2 for bit-lines
        """

        stack=("metal1", "via1", "metal2")
        upper_pin = self.upper_pmos1_inst.get_pin("S")
        lower_pin = self.lower_pmos_inst.get_pin("S")
        
        # BL goes up to M2 at the transistor
        self.bl_contact=self.add_via_center(layers=stack,
                                            offset=upper_pin.center(),
                                            directions=("V","V"))
        self.add_via_center(layers=stack,
                            offset=lower_pin.center(),
                            directions=("V","V"))

        # BR routes over on M1 first
        self.add_via_center(layers=stack,
                            offset = vector(self.br_pin.cx(), upper_pin.cy()),
                            directions=("V","V"))
        self.add_via_center(layers=stack,
                            offset = vector(self.br_pin.cx(), lower_pin.cy()),
                            directions=("V","V"))

    def connect_pmos_m1(self, pmos_pin, bit_pin):
        """ 
        Connect a pmos pin to bitline pin 
        """

        left_pos = vector(min(pmos_pin.cx(),bit_pin.cx()), pmos_pin.cy())
        right_pos = vector(max(pmos_pin.cx(),bit_pin.cx()), pmos_pin.cy())

        self.add_path("metal1", [ left_pos, right_pos] )

    def connect_pmos_m2(self, pmos_pin, bit_pin):
        """ 
        Connect a pmos pin to bitline pin 
        """

        left_pos = vector(min(pmos_pin.cx(),bit_pin.cx()), pmos_pin.cy())
        right_pos = vector(max(pmos_pin.cx(),bit_pin.cx()), pmos_pin.cy())

        self.add_path("metal2", [ left_pos, right_pos], self.bl_contact.height)
        
    def get_en_cin(self):
        """Get the relative capacitance of the enable in the precharge cell"""    
        #The enable connect to three pmos gates. They all use the same size pmos.
        pmos_cin = self.pmos.get_cin()
        return 3*pmos_cin
        
