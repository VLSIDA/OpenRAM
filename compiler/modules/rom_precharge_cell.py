# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from .rom_base_cell import rom_base_cell
from openram.base import vector
from openram import OPTS
from openram.sram_factory import factory
from openram.tech import drc


class rom_precharge_cell(rom_base_cell):

    def __init__(self, name="", route_layer="m1"):

        super().__init__(name=name, bitline_layer=route_layer)



    # def create_netlist(self):        
    #     self.add_pins()
    #     self.add_modules()
    #     self.create_tx()
        
        
    def create_layout(self):
        super().create_layout()
        self.extend_well()



    def add_modules(self):

        self.pmos  = factory.create(module_type="ptx",
                                    module_name="pre_pmos_mod",
                                    tx_type="pmos"
                                    )

    def create_tx(self):
        self.cell_inst = self.add_inst( name="precharge_pmos",
                                        mod=self.pmos, 
                                        )
        self.connect_inst(["bitline", "gate", "vdd", "body"])

        
    def add_pins(self):   
        pin_list = ["vdd", "gate", "bitline", "body"]
        dir_list = ["POWER", "INPUT", "OUTPUT", "POWER"]

        self.add_pin_list(pin_list, dir_list) 

    def setup_drc_offsets(self):

        self.poly_size = (self.cell_inst.width + self.active_space) - (self.cell_inst.height + 2 * self.poly_extend_active)

    

        #contact to contact distance, minimum cell width before drc offsets 
        self.base_width = self.pmos.width - 2 * self.active_enclose_contact - self.pmos.contact_width

        # width offset to account for poly-active spacing between base and dummy cells on the same bitline
        self.poly_active_offset = 0.5 * (self.base_width - (self.poly_width + 2 * self.active_enclose_contact + self.pmos.contact_width)) - self.poly_to_active

        #so that the poly taps are far enough apart 
        self.poly_tap_offset = (self.base_width - self.poly_contact.width - self.poly_active_offset) - drc("poly_to_poly")


    def extend_well(self):
        self.pmos

        well_y = - (0.5 * self.nwell_width)
        well_ll = vector(0, well_y)
        # height = self.active_width + 2 * self.well_enclose_active
        height = self.height + 0.5 * self.nwell_width
        self.add_rect("nwell", well_ll, self.width , height)
    # def place_tx(self):

    #     pmos_offset = vector(self.pmos.poly_extend_active + self.pmos.height, 0)
        
    #     self.cell_inst.place(pmos_offset, rotate=90)
    #     self.add_label("inst_zero", self.bitline_layer)
    #     self.add_layout_pin_rect_center("S", self.bitline_layer, self.cell_inst.get_pin("S").center())
    #     self.add_layout_pin_rect_center("D", self.bitline_layer, self.cell_inst.get_pin("D").center())


    # def place_poly(self):
    #     poly_size = (self.cell_inst.width + self.active_space) - (self.cell_inst.rx() + self.poly_extend_active)
    #     poly_offset = vector(self.cell_inst.rx() + self.poly_extend_active, self.cell_inst.width * 0.5 )

    #     start = poly_offset
    #     end = poly_offset + vector(poly_size, 0)
    #     self.add_segment_center("poly", start, end)
    # def add_boundary(self):

    #     #cell width with offsets applied, height becomes width when the cells are rotated 
    #     self.width = self.pmos.height + self.poly_extend_active_spacing + 2 * self.pmos.poly_extend_active

    #     # cell height with offsets applied, width becomes height when the cells are rotated, if the offsets are positive (greater than 0) they are not applied
    #     # self.height = self.base_width - min(self.poly_active_offset, 0) - min(self.poly_tap_offset, 0)

    #     super().add_boundary()
        
