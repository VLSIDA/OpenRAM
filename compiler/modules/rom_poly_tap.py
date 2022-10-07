

from base import design
from base import vector
from sram_factory import factory

class rom_poly_tap(design):

    def __init__(self, name, strap_length=0, cell_name=None, prop=None, strap_layer="m2"):
        super().__init__(name, cell_name, prop)
        self.strap_layer=strap_layer
        self.length = strap_length
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):


        #for layout constants
        self.dummy = factory.create(module_type="rom_dummy_cell")

    def create_layout(self):

        self.place_via()
        self.add_boundary()
        if self.length != 0:
            self.place_strap(self.length)
    
    def add_boundary(self):
        self.height = self.dummy.height
        self.width = self.poly_contact.width
        super().add_boundary()

    def place_via(self):

        contact_width = self.poly_contact.width
        
        contact_x = - contact_width * 0.5 - self.dummy.width
        contact_y = self.dummy.poly.offset.x + (self.poly_width * 0.5)

        contact_offset = vector(contact_x, contact_y)
        self.via = self.add_via_stack_center(from_layer="poly",
                                  to_layer=self.strap_layer,
                                  offset=contact_offset)

    def place_strap(self, length):

        strap_start = vector(self.via.cx(), self.via.cy())

        strap_end = vector( self.dummy.width * length, self.via.cy())

        self.strap = self.add_path(self.strap_layer, (strap_start, strap_end))

