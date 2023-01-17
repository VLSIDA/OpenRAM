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


class rom_dummy_cell(design):

    def __init__(self, name="", cell_name=None, add_source_contact=False, add_drain_contact=False, route_layer="m1"):
        super().__init__(name, cell_name)
        self.route_layer = route_layer
        self.add_source_contact="li"
        self.add_drain_contact="li"
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        #creates nmos for layout dimensions
        self.add_nmos()

        #set height and width such that the cell will tile perfectly by only ofsetting in the array by its width and height
        
    

    def create_layout(self):
        
        
        self.setup_drc_offsets()
        
        self.add_boundary()
        self.add_poly()
        self.add_metal()
        #self.add_label("0,0", self.route_layer)

    

    def add_poly(self):

        poly_x = 0.5 * (self.nmos.poly_height + self.poly_extend_active_spacing)
        # 0.5 * self.nmos.contact_width + self.contact_to_gate

        self.poly = self.add_rect_center("poly", vector(poly_x, self.base_width * 0.5), 2 * poly_x, self.poly_width)

    def add_metal(self):

        if self.route_layer == "li":
            via = "mcon"
        else:
            via = "via{}".format(self.route_layer[len(self.route_layer) - 1])
        wire_y =  self.height + drc["minwidth_{}".format(via)] * 0.5
        wire_x = 0.5 * (self.width - self.poly_extend_active_spacing)

        wire_start = vector( wire_x, 0)
        wire_end = vector(wire_x, wire_y)

        # if self.route_layer == 'm1':

        #     if self.drain_contact:
        #         self.add_via_center(self.li_stack, [wire_x, wire_y])
        #     if self.source_contact:
        #         self.add_via_center(self.li_stack, [self.width, wire_y])

        self.add_path(self.route_layer, [wire_start, wire_end])   

        # drain_x = 0
        # drain_y = 0.5 * (self.width)
        source_x = 0.5 * (self.width - self.poly_extend_active_spacing)
        source_y = 0
        source_pos = vector(source_x, source_y)
        self.add_layout_pin_rect_center("S", self.route_layer, source_pos)

        drain_pos = vector(source_x, self.height)
        self.add_layout_pin_rect_center("D", self.route_layer, drain_pos)
        
            

        
    
