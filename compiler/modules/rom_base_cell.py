# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#


import math
from .rom_dummy_cell import rom_dummy_cell
from base import design
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
        print("using base cell netlist creation")
        
        self.add_pins()
        self.add_nmos()
        self.create_nmos()
        
        
    def create_layout(self):
        self.setup_drc_offsets()
        self.place_nmos()
        self.add_boundary()

        print(self.height)
        print(self.width)

    def add_pins(self):   
        pin_list = ["bl_h", "bl_l", "wl"]
        dir_list = ["INOUT", "GROUND", "INPUT"]

        self.add_pin_list(pin_list, dir_list) 


    def create_nmos(self):
        self.cell_inst = self.add_inst( name=self.name,
                                        mod=self.nmos, 
                                        )
        self.connect_inst(["bl_h", "wl", "bl_l", "gnd"])

        

    def place_nmos(self):

        
        poly_offset = vector(0.5 * self.nmos.active_contact.width + self.nmos.active_contact_to_gate,
                                 self.nmos.poly_height)

        nmos_offset = vector(- 0.5 * self.nmos.contact_width - self.active_enclose_contact, self.nmos.poly_extend_active)

        # add rect of poly to account for offset from drc spacing
        self.add_rect("poly", poly_offset, self.nmos.poly_width, self.poly_extend_active_spacing )
        
        self.cell_inst.place(nmos_offset)

        self.add_label("S", self.route_layer, self.cell_inst.get_pin("S").center())
        self.add_label("D", self.route_layer, self.cell_inst.get_pin("D").center())
        
        


        

    
