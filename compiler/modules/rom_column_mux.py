# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import drc, layer
from openram.tech import cell_properties as cell_props
from openram import OPTS
from .pgate import *


class rom_column_mux(pgate):
    """
    This module implements the columnmux bitline cell used in the design.
    Creates a single column mux cell with the given integer size relative
    to minimum size. Default is 8x. Per Samira and Hodges-Jackson book:
    Column-mux transistors driven by the decoder must be sized
    for optimal speed
    """
    def __init__(self, name, tx_size=8, input_layer="m2", output_layer="m1"):

        debug.info(2, "creating single ROM column mux cell: {0}".format(name))
        self.tx_size = int(tx_size)
        self.input_layer = input_layer
        self.output_layer= output_layer
        super().__init__(name)

    def create_netlist(self):
        self.add_pins()
        self.add_ptx()

    def create_layout(self):

        self.pin_layer = self.input_layer
        self.pin_pitch = getattr(self, "{}_pitch".format(self.pin_layer))
        self.pin_width = getattr(self, "{}_width".format(self.pin_layer))
        self.pin_height = 2 * self.pin_width

        # If li exists, use li and m1 for the mux, otherwise use m1 and m2
        if self.output_layer == "li" :
            self.col_mux_stack = self.li_stack
        else:
            self.col_mux_stack = self.m1_stack

        self.place_ptx()

        self.width = self.bitcell.width
        self.height = self.nmos_lower.uy() + self.pin_height

        self.connect_poly()
        self.add_bitline_pins()
        self.connect_bitlines()
        self.add_pn_wells()

    def add_ptx(self):
        self.bitcell = factory.create(module_type="rom_base_cell")

        # Adds nmos_lower,nmos_upper to the module
        self.ptx_width = self.tx_size * drc("minwidth_tx")
        self.nmos = factory.create(module_type="ptx",
                                    width=self.ptx_width)

        # Space it in the center
        self.nmos_lower = self.add_inst(name="mux_tx1",
                                        mod=self.nmos)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])


    def add_pins(self):
        self.add_pin_list(["bl", "bl_out", "sel", "gnd"])

    def add_bitline_pins(self):
        """ Add the top and bottom pins to this cell """

        bl_pos = vector(self.pin_pitch, 0)

        # bl and br
        self.add_layout_pin(text="bl",
                            layer=self.pin_layer,
                            offset=bl_pos + vector(0, self.height - self.pin_height),
                            height=self.pin_height)

        # bl_out and br_out
        self.add_layout_pin(text="bl_out",
                            layer=self.col_mux_stack[0],
                            offset=bl_pos,
                            height=self.pin_height)


    def place_ptx(self):
        """ Create the pass gate NMOS transistor to switch the bitline """

        # Space it in the center
        nmos_lower_position = self.nmos.active_offset.scale(0, 1) \
                              + vector(0.5 * self.bitcell.width- 0.5 * self.nmos.active_width, 0)
        self.nmos_lower.place(nmos_lower_position)

    def connect_poly(self):
        """ Connect the poly gate of the two pass transistors """

        # offset is the top of the lower nmos' diffusion
        # height is the distance between the nmos' diffusions, which depends on max(self.active_space,self.poly_space)
        offset = self.nmos_lower.get_pin("G").ul() - vector(0, self.poly_extend_active)
        height =  self.poly_extend_active - offset.y
        self.add_rect(layer="poly",
                            offset=offset,
                            height=height)

        # Add the sel pin to the bottom of the mux
        self.add_layout_pin(text="sel",
                            layer="poly",
                            offset=self.nmos_lower.get_pin("G").ll(),
                            height=self.poly_extend_active)

    def connect_bitlines(self):
        """ Connect the bitlines to the mux transistors """

        bl_pin = self.get_pin("bl")
        bl_out_pin = self.get_pin("bl_out")

        nmos_lower_s_pin = self.nmos_lower.get_pin("S")
        nmos_lower_d_pin = self.nmos_lower.get_pin("D")
        self.add_via_stack_center(from_layer=nmos_lower_s_pin.layer,
                                  to_layer=self.input_layer,
                                  offset=nmos_lower_s_pin.center())

        self.add_via_stack_center(from_layer=nmos_lower_d_pin.layer,
                                  to_layer=self.output_layer,
                                  offset=nmos_lower_d_pin.center())

        # bl -> nmos_upper/D on metal1
        # bl_out -> nmos_upper/S on metal2
        mid1 = bl_pin.bc().scale(1, 0.4) \
               + nmos_lower_s_pin.uc().scale(0, 0.5)
        mid2 = bl_pin.bc().scale(0, 0.4) \
               + nmos_lower_s_pin.uc().scale(1, 0.5)
        self.add_path(self.input_layer,
                      [bl_pin.bc(), mid1, mid2, nmos_lower_s_pin.center()])
        # halfway up, move over
        mid1 = bl_out_pin.uc().scale(1, 0.4) \
               + nmos_lower_d_pin.bc().scale(0, 0.4)
        mid2 = bl_out_pin.uc().scale(0, 0.4) \
               + nmos_lower_d_pin.bc().scale(1, 0.4)
        self.add_path(self.output_layer,
                      [bl_out_pin.uc(), mid1, mid2, nmos_lower_d_pin.center()])

    def add_pn_wells(self):
        """
        Add a well and implant over the whole cell. Also, add the
        pwell contact (if it exists)
        """
        # Add it to the right, aligned in between the two tx
        active_pos = vector(self.bitcell.width,
                            self.nmos_lower.uy() + self.active_contact.height + self.active_space)

        self.add_via_center(layers=self.active_stack,
                            offset=active_pos,
                            implant_type="p",
                            well_type="p")

        # If there is a li layer, include it in the power stack
        self.add_via_stack_center(from_layer=self.active_stack[2],
                                  to_layer=self.pin_layer,
                                  offset=active_pos)

        self.add_layout_pin_rect_center(text="gnd",
                                        layer=self.pin_layer,
                                        offset=active_pos)