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


class rom_base_cell(design):

    def __init__(self, name="", bitline_layer="li", bit_value=1, add_well=False):
        super().__init__(name)
        self.bit_value = bit_value
        self.bitline_layer = bitline_layer
        self.add_well=add_well
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()

    def create_layout(self):

        self.create_tx()
        self.setup_drc_offsets()
        self.add_boundary()
        self.place_tx()
        self.place_bitline()
        self.place_poly()
        if self.bit_value == 0:
            self.short_gate()

    # Calculates offsets of cell width and height so that tiling of cells does not violate any drc rules
    def setup_drc_offsets(self):

        self.poly_size = (self.cell_inst.width + self.active_space) - (self.cell_inst.height + 2 * self.poly_extend_active)

    def add_boundary(self):

        height = self.cell_inst.width + self.active_space

        #cell width with offsets applied, height becomes width when the cells are rotated
        width = self.cell_inst.height + 2 * self.poly_extend_active


        # make the cells square so the pitch of wordlines will match bitlines

        if width > height:
            self.width = width
            self.height = width
        else:
            self.width = height
            self.height = height

        super().add_boundary()


    def add_modules(self):

        self.nmos  = factory.create(module_type="ptx",
                                    module_name="nmos_rom_mod",
                                    tx_type="nmos",
                                    add_source_contact=self.bitline_layer,
                                    add_drain_contact=self.bitline_layer
                                    )


    def create_tx(self):
        self.cell_inst = self.add_inst( name=self.name + "_nmos",
                                        mod=self.nmos,
                                        )
        if self.bit_value == 0:
            self.connect_inst(["bl", "wl", "bl", "gnd"])
        else:
            self.connect_inst(["bl_h", "wl", "bl_l", "gnd"])


    def add_pins(self):
        if self.bit_value == 0 :
            pin_list = ["bl", "wl", "gnd"]
            dir_list = ["INOUT", "INPUT", "GROUND"]
        else:
            pin_list = ["bl_h", "bl_l", "wl", "gnd"]
            dir_list = ["INOUT", "INOUT", "INPUT", "GROUND"]

        self.add_pin_list(pin_list, dir_list)

    def place_tx(self):

        # sizing_offset = self.cell_inst.height - drc["minwidth_tx"]
        tx_offset = vector(self.poly_extend_active + self.cell_inst.height + self.poly_size,- 0.5 * self.contact_width - self.active_enclose_contact)
        # add rect of poly to account for offset from drc spacing
        # self.add_rect_center("poly", poly_offset, self.poly_extend_active_spacing, self.poly_width)

        self.cell_inst.place(tx_offset, rotate=90)

        self.copy_layout_pin(self.cell_inst, "S", "S")
        self.copy_layout_pin(self.cell_inst, "D", "D")
        self.source_pos = self.cell_inst.get_pin("S").center()

    def place_poly(self):
        poly_offset = vector(0, self.cell_inst.width * 0.5 - 0.5 * self.contact_width - self.active_enclose_contact)

        start = poly_offset
        end = poly_offset + vector(self.poly_size, 0)
        self.add_segment_center("poly", start, end)


    def place_bitline(self):

        start = self.get_pin("D").center()
        end = start + vector(0, 2 * self.active_enclose_contact + 0.5 * self.contact_width + self.active_space)
        self.add_segment_center(self.bitline_layer, start, end)

    def short_gate(self):

        self.add_segment_center(self.bitline_layer, self.get_pin("D").center(), self.get_pin("S").center())