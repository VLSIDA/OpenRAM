# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.base import design
from openram.base import vector
from openram import OPTS
from openram.sram_factory import factory
from openram.tech import drc

class rom_poly_tap(design):

    def __init__(self, name="", cell_name=None, tx_type="nmos", strap_layer="m2", add_active_tap=False, place_poly=None):
        super().__init__(name, cell_name)
        self.strap_layer=strap_layer
        self.tx_type = tx_type
        self.add_tap = add_active_tap
        if place_poly is None:
            self.place_poly = add_active_tap
        else:
            self.place_poly = place_poly
        self.pitch_offset = 0
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        #for layout constants
        self.dummy = factory.create(module_type="rom_base_cell")

        self.pmos = factory.create(module_type="ptx", tx_type="pmos")

    def create_layout(self):

        self.place_via()
        self.add_boundary()
        if self.add_tap or self.place_poly:
            self.place_active_tap()
            self.extend_poly()

    def add_boundary(self):
        contact_width = self.poly_contact.width
        self.height = self.dummy.height
        self.width = contact_width + self.pitch_offset

        super().add_boundary()

    def place_via(self):

        contact_width = self.poly_contact.width

        contact_y = self.dummy.cell_inst.width * 0.5 - 0.5 * self.contact_width - self.active_enclose_contact

        self.contact_x_offset = 0


        contact_x = contact_width * 0.5 + self.contact_x_offset
        self.contact_offset = vector(contact_x, contact_y)

        self.via = self.add_via_stack_center(from_layer="poly",
                                  to_layer=self.strap_layer,
                                  offset=self.contact_offset)
        self.add_layout_pin_rect_center("poly_tap", self.strap_layer, self.contact_offset)

    def extend_poly(self):
        y_offset = 0
        if self.tx_type == "pmos":
            y_offset = -self.height
        start = self.via.center() + vector(0, y_offset)

        self.add_segment_center("poly", start, vector(self.via.cx() + self.pitch_offset, self.via.cy() + y_offset))
        self.add_segment_center("poly", start, vector(0, self.via.cy() + y_offset))

    def place_active_tap(self):
        gap = self.poly_extend_active - 0.5 * ( self.active_contact.height - self.poly_contact.width )
        offset = self.active_space - gap
        tap_x = self.via.cx() + offset
        tap_y = self.via.cy() + self.dummy.width * 0.5
        contact_pos = vector(tap_x, tap_y)

        # edge of the next nmos
        active_edge = self.dummy.width - self.dummy.cell_inst.height - self.poly_extend_active

        # edge of the active contact
        tap_edge = tap_x + 0.5 * self.active_contact.height
        self.pitch_offset += (self.active_space * 2) - (tap_edge - active_edge) + self.contact_x_offset

        if self.tx_type == "nmos" and self.add_tap:
            self.add_via_center(layers=self.active_stack,
                                offset=contact_pos,
                                implant_type="p",
                                well_type="p",
                                directions="nonpref")
            self.add_layout_pin_rect_center("active_tap", self.active_stack[2], contact_pos)