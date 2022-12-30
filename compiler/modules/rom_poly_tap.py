# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from openram.base import design
from openram.base import vector
from openram import OPTS
from openram.sram_factory import factory

class rom_poly_tap(design):

    def __init__(self, name="", strap_length=0, cell_name=None, prop=None, tx_type="nmos", strap_layer="m1"):
        super().__init__(name, cell_name, prop)
        self.strap_layer=strap_layer
        self.length = strap_length
        self.tx_type = tx_type
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        #for layout constants
        self.dummy = factory.create(module_type="rom_dummy_cell")
        self.pmos = factory.create(module_type="ptx", tx_type="pmos")

    def create_layout(self):

        self.place_via()
        # if self.tx_type == "pmos":
        self.extend_poly()
        self.add_boundary()
        if self.length != 0:
            self.place_strap()

    
    def add_boundary(self):
        contact_width = self.poly_contact.width + 2 * self.contact_x_offset 

        offset = self.active_space - (contact_width - self.active_enclose_contact - self.active_extend_contact)
        print("THINGY {}".format(offset))
        self.height = self.dummy.height
        self.width = contact_width + self.pitch_offset

        print("poly height: {0}, width: {1}".format(self.height, self.width))
        super().add_boundary()

    def place_via(self):
        
        contact_width = self.poly_contact.width

        # DRC rule here is hard coded since licon.9 isnt included in skywater130 tech file

        # poly contact spacing to P-diffusion < 0.235um (licon.9 + psdm.5a)
        if OPTS.tech_name == "sky130":
            self.contact_x_offset =  0.235 - (contact_width - self.pmos.contact_width) * 0.5 - self.poly_extend_active
        else:
            assert(False)

        if self.tx_type == "nmos":
            
            contact_y = self.dummy.poly.cy()
            # contact_y = self.dummy.poly.offset.x + (self.poly_width * 0.5)
            # self.contact_x_offset = 0
        else:
            contact_y = self.pmos.poly_positions[0].x - self.pmos.active_offset.x

        # contact_x = - contact_width * 0.5 - self.contact_x_offset
        contact_x =  contact_width * 0.5 + self.contact_x_offset
        self.contact_offset = vector(contact_x, contact_y)

        self.via = self.add_via_stack_center(from_layer="poly",
                                  to_layer=self.strap_layer,
                                  offset=self.contact_offset)
        self.add_layout_pin_rect_center("via", self.strap_layer, self.contact_offset)




    def place_strap(self):

        strap_start = vector(self.via.lx() , self.via.cy())

        strap_end = vector( self.dummy.width * (self.length + 1), self.via.cy())

        self.strap = self.add_path(self.strap_layer, (strap_start, strap_end))

    def extend_poly(self):

        base_contact_width = self.poly_contact.width + 2 * self.contact_x_offset 

        self.pitch_offset = (base_contact_width - self.active_enclose_contact - self.active_extend_contact) - self.active_space


        poly_x = self.poly_contact.width + self.contact_x_offset
        poly_y = self.contact_offset.y - self.poly_width * 0.5
        extend_offset = vector(poly_x, poly_y)

        self.add_rect("poly", extend_offset, self.contact_x_offset + self.pitch_offset, self.poly_width)

        poly_x = 0
        extend_offset = vector(poly_x, poly_y)

        self.add_rect("poly", extend_offset, self.contact_x_offset , self.poly_width)
        

