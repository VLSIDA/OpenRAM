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
from openram.tech import drc


class rom_precharge_cell(design):

    def __init__(self, name="", cell_name=None, route_layer="m1"):

        super().__init__(name, cell_name)
        self.route_layer = route_layer
        self.create_netlist()
        self.create_layout()

        #self.route_layer= route_layer
        #self.create_netlist()
        #self.create_layout()


    def create_netlist(self):        
        self.add_pins()
        self.add_pmos()
        self.create_pmos()
        
        
    def create_layout(self):
        self.setup_layout_constants()
        self.place_pmos()
        self.add_boundary()


    def add_pmos(self):

        self.pmos  = factory.create(module_type="ptx",
                                    module_name="pre_pmos_mod",
                                    tx_type="pmos"
                                    )

    def create_pmos(self):
        self.cell_inst = self.add_inst( name="precharge_pmos",
                                        mod=self.pmos, 
                                        )
        self.connect_inst(["bitline", "gate", "vdd", "vdd"])

        
    def add_pins(self):   
        pin_list = ["vdd", "gate", "bitline", "vdd"]
        dir_list = ["OUTPUT", "INPUT", "OUTPUT", "POWER"]

        self.add_pin_list(pin_list, dir_list) 

    def setup_layout_constants(self):
    
        #pmos contact to gate distance
        self.contact_to_gate = 0.5 * (self.pmos.width - 2 * self.pmos.contact_width - self.pmos.poly_width - 2 * self.active_enclose_contact) 

        #height offset to account for active-to-active spacing between adjacent bitlines
        self.poly_extend_active_spacing = abs( 2 * self.pmos.poly_extend_active - drc("active_to_active") )

        #contact to contact distance, minimum cell width before drc offsets 
        self.base_width = self.pmos.width - 2 * self.active_enclose_contact - self.pmos.contact_width

        # width offset to account for poly-active spacing between base and dummy cells on the same bitline
        self.poly_active_offset = 0.5 * (self.base_width - (self.poly_width + 2 * self.active_enclose_contact + self.pmos.contact_width)) - self.poly_to_active

        #so that the poly taps are far enough apart 
        self.poly_tap_offset = (self.base_width - self.poly_contact.width - self.poly_active_offset) - drc("poly_to_poly")


    def place_pmos(self):

        poly_offset = vector(self.poly_extend_active_spacing * 0.5 + self.pmos.height + 2 * self.poly_extend_active, 0.5 * self.pmos.width)

        # pmos_offset = vector(self.pmos.poly_extend_active, - 0.5 * self.pmos.contact_width - self.active_enclose_contact)

        # pmos_offset = vector(-self.pmos.poly_extend_active - self.poly_extend_active_spacing, 0)
        pmos_offset = vector(self.pmos.poly_extend_active + self.pmos.height, 0)
        # add rect of poly to account for offset from drc spacing
        self.add_rect_center("poly", poly_offset, self.poly_extend_active_spacing, self.pmos.poly_width )
        
        self.cell_inst.place(pmos_offset, rotate=90)
        # self.add_label("CELL ZERO", self.route_layer)
        self.add_label("inst_zero", self.route_layer)
        self.add_layout_pin_rect_center("S", self.route_layer, self.cell_inst.get_pin("S").center())
        self.add_layout_pin_rect_center("D", self.route_layer, self.cell_inst.get_pin("D").center())

    def add_boundary(self):

        #cell width with offsets applied, height becomes width when the cells are rotated 
        self.width = self.pmos.height + self.poly_extend_active_spacing + 2 * self.pmos.poly_extend_active

        # cell height with offsets applied, width becomes height when the cells are rotated, if the offsets are positive (greater than 0) they are not applied
        self.height = self.base_width - min(self.poly_active_offset, 0) - min(self.poly_tap_offset, 0)

        super().add_boundary()
        
