

from openram.base import design
from openram.base import vector
from openram.sram_factory import factory

class rom_array_gnd_tap(design):

    def __init__(self, name, length, cell_name=None, prop=None):
        super().__init__(name, cell_name, prop)
        self.length = length
        self.create_layout()

    def create_layout(self):

        self.add_cell()
        self.add_boundary()
        self.place_gnd_rail()


    def add_boundary(self):
        self.height = self.dummy.height
        self.width = self.dummy.width 
        super().add_boundary()

    def add_cell(self):
        self.dummy = factory.create(module_type="rom_dummy_cell")

    def place_gnd_rail(self):
        rail_start = vector(-self.dummy.width / 2 ,0)
        rail_end = vector(self.dummy.width * self.length, 0)

        self.add_layout_pin_rect_ends(  name="gnd",
                                        layer="m1",
                                        start=rail_start,
                                        end=rail_end)

        

