# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from .rom_dummy_cell import rom_dummy_cell
from base import vector
from globals import OPTS
from sram_factory import factory

from tech import drc


class rom_base_cell(rom_dummy_cell):

    def __init__(self, name="", cell_name=None, add_source_contact=False, add_drain_contact=False, route_layer="m1"):
        super().__init__(name, cell_name, add_source_contact, add_drain_contact, route_layer)
        #self.route_layer= route_layer
        #self.create_netlist()
        #self.create_layout()


    def create_netlist(self):        
        self.add_pins()
        self.add_nmos()
        self.create_nmos()
        
        
    def create_layout(self):
        self.setup_drc_offsets()
        self.place_nmos()
        self.add_boundary()


    def create_nmos(self):
        self.cell_inst = self.add_inst( name=self.name + "_nmos",
                                        mod=self.nmos, 
                                        )
        self.connect_inst(["bl_h", "wl", "bl_l", "gnd"])

        
    def add_pins(self):   
        pin_list = ["bl_h", "bl_l", "wl", "gnd"]
        dir_list = ["INOUT", "INOUT", "INPUT", "GROUND"]

        self.add_pin_list(pin_list, dir_list) 

    def place_nmos(self):

        # 0.5 * self.nmos.active_contact.width + self.nmos.active_contact_to_gate
        poly_offset = vector(self.poly_extend_active_spacing * 0.5 + self.nmos.height + 2 * self.poly_extend_active, self.nmos.width * 0.5 - 0.5 * self.nmos.contact_width - self.active_enclose_contact)

        # nmos_offset = vector(- 0.5 * self.nmos.contact_width - self.active_enclose_contact, self.nmos.poly_extend_active)
        print("{} poly spacing".format(self.poly_extend_active_spacing))

        nmos_offset = vector(self.nmos.poly_extend_active + self.nmos.height ,- 0.5 * self.nmos.contact_width - self.active_enclose_contact)
        # add rect of poly to account for offset from drc spacing
        self.add_rect_center("poly", poly_offset, self.poly_extend_active_spacing, self.nmos.poly_width)
        
        self.cell_inst.place(nmos_offset, rotate=90)
        # self.add_label("CELL ZERO", self.route_layer)
        self.copy_layout_pin(self.cell_inst, "S", "S")
        self.copy_layout_pin(self.cell_inst, "D", "D")
        self.source_pos = self.cell_inst.get_pin("S").center()
        # if self.add_source_contact != False:
        #     # drain_x = 0
        #     # drain_y = 0.5 * (self.width - self.poly_extend_active_spacing)

            
        #     print("drained")
        #     print(drain_pos)
        #     self.add_layout_pin_rect_center("S", self.route_layer, drain_pos)
        # self.add_label("S", self.route_layer, self.cell_inst.get_pin("S").center())
        
        


        

    
