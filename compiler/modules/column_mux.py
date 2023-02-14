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


class column_mux(pgate):
    """
    This module implements the columnmux bitline cell used in the design.
    Creates a single column mux cell with the given integer size relative
    to minimum size. Default is 8x. Per Samira and Hodges-Jackson book:
    Column-mux transistors driven by the decoder must be sized
    for optimal speed
    """
    def __init__(self, name, tx_size=8, bitcell_bl="bl", bitcell_br="br"):

        debug.info(2, "creating single column mux cell: {0}".format(name))

        self.tx_size = int(tx_size)
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br

        super().__init__(name)

    def get_bl_names(self):
        return "bl"

    def get_br_names(self):
        return "br"

    def create_netlist(self):
        self.add_pins()
        self.add_ptx()

    def create_layout(self):

        # If li exists, use li and m1 for the mux, otherwise use m1 and m2
        if "li" in layer:
            self.col_mux_stack = self.li_stack
        else:
            self.col_mux_stack = self.m1_stack
        self.pin_layer = self.bitcell.get_pin(self.bitcell_bl).layer
        self.pin_pitch = getattr(self, "{}_pitch".format(self.pin_layer))
        self.pin_width = getattr(self, "{}_width".format(self.pin_layer))
        self.pin_height = 2 * self.pin_width

        self.place_ptx()

        cell = factory.create(module_type=OPTS.bitcell)
        if(cell_props.use_strap == True and OPTS.num_ports == 1):
            strap = factory.create(module_type=cell_props.strap_module, version=cell_props.strap_version)
            precharge_width = cell.width + strap.width
        else:
            precharge_width = cell.width
        self.width = precharge_width
        self.height = self.nmos_upper.uy() + self.pin_height

        self.connect_poly()
        self.add_bitline_pins()
        self.connect_bitlines()
        self.add_pn_wells()

    def add_ptx(self):
        self.bitcell = factory.create(module_type=OPTS.bitcell)

        # Adds nmos_lower,nmos_upper to the module
        self.ptx_width = self.tx_size * drc("minwidth_tx")
        self.nmos = factory.create(module_type="ptx",
                                    width=self.ptx_width)

        # Space it in the center
        self.nmos_lower = self.add_inst(name="mux_tx1",
                                        mod=self.nmos)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])

        # This aligns it directly above the other tx with gates abutting
        self.nmos_upper = self.add_inst(name="mux_tx2",
                                        mod=self.nmos)
        self.connect_inst(["br", "sel", "br_out", "gnd"])

    def add_pins(self):
        self.add_pin_list(["bl", "br", "bl_out", "br_out", "sel", "gnd"])

    def add_bitline_pins(self):
        """ Add the top and bottom pins to this cell """

        bl_pos = vector(self.pin_pitch, 0)
        br_pos = vector(self.width - self.pin_pitch, 0)

        # bl and br
        self.add_layout_pin(text="bl",
                            layer=self.pin_layer,
                            offset=bl_pos + vector(0, self.height - self.pin_height),
                            height=self.pin_height)
        self.add_layout_pin(text="br",
                            layer=self.pin_layer,
                            offset=br_pos + vector(0, self.height - self.pin_height),
                            height=self.pin_height)

        # bl_out and br_out
        self.add_layout_pin(text="bl_out",
                            layer=self.pin_layer,
                            offset=bl_pos,
                            height=self.pin_height)
        self.add_layout_pin(text="br_out",
                            layer=self.pin_layer,
                            offset=br_pos,
                            height=self.pin_height)

    def place_ptx(self):
        """ Create the two pass gate NMOS transistors to switch the bitlines"""

        # Space it in the center
        nmos_lower_position = self.nmos.active_offset.scale(0, 1) \
                              + vector(0.5 * self.bitcell.width- 0.5 * self.nmos.active_width, 0)
        self.nmos_lower.place(nmos_lower_position)

        # This aligns it directly above the other tx with gates abutting
        nmos_upper_position = nmos_lower_position \
                              + vector(0, self.nmos.active_height + max(self.active_space, self.poly_space))
        self.nmos_upper.place(nmos_upper_position)

        if cell_props.pgate.add_implants:
            self.extend_implants()

    def connect_poly(self):
        """ Connect the poly gate of the two pass transistors """

        # offset is the top of the lower nmos' diffusion
        # height is the distance between the nmos' diffusions, which depends on max(self.active_space,self.poly_space)
        offset = self.nmos_lower.get_pin("G").ul() - vector(0, self.poly_extend_active)
        height = self.nmos_upper.get_pin("G").by() + self.poly_extend_active - offset.y
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
        br_pin = self.get_pin("br")
        bl_out_pin = self.get_pin("bl_out")
        br_out_pin = self.get_pin("br_out")

        nmos_lower_s_pin = self.nmos_lower.get_pin("S")
        nmos_lower_d_pin = self.nmos_lower.get_pin("D")
        nmos_upper_s_pin = self.nmos_upper.get_pin("S")
        nmos_upper_d_pin = self.nmos_upper.get_pin("D")

        # Add vias to bl, br_out, nmos_upper/S, nmos_lower/D
        self.add_via_stack_center(from_layer=bl_pin.layer,
                                  to_layer=self.col_mux_stack[0],
                                  offset=bl_pin.bc())
        self.add_via_stack_center(from_layer=br_out_pin.layer,
                                  to_layer=self.col_mux_stack[0],
                                  offset=br_out_pin.uc())
        self.add_via_stack_center(from_layer=nmos_upper_s_pin.layer,
                                  to_layer=self.col_mux_stack[2],
                                  offset=nmos_upper_s_pin.center())
        self.add_via_stack_center(from_layer=nmos_lower_d_pin.layer,
                                  to_layer=self.col_mux_stack[2],
                                  offset=nmos_lower_d_pin.center())

        # bl -> nmos_upper/D on metal1
        # bl_out -> nmos_upper/S on metal2
        self.add_path(self.col_mux_stack[0],
                      [bl_pin.ll(), vector(nmos_upper_d_pin.cx(), bl_pin.by()),
                       nmos_upper_d_pin.center()])
        # halfway up, move over
        mid1 = bl_out_pin.uc().scale(1, 0.4) \
               + nmos_upper_s_pin.bc().scale(0, 0.4)
        mid2 = bl_out_pin.uc().scale(0, 0.4) \
               + nmos_upper_s_pin.bc().scale(1, 0.4)
        self.add_path(self.col_mux_stack[2],
                      [bl_out_pin.uc(), mid1, mid2, nmos_upper_s_pin.center()])

        # br -> nmos_lower/D on metal2
        # br_out -> nmos_lower/S on metal1
        self.add_path(self.col_mux_stack[0],
                      [br_out_pin.uc(),
                       vector(nmos_lower_s_pin.cx(), br_out_pin.uy()),
                       nmos_lower_s_pin.center()])
        # halfway up, move over
        mid1 = br_pin.bc().scale(1, 0.5) \
               + nmos_lower_d_pin.uc().scale(0, 0.5)
        mid2 = br_pin.bc().scale(0, 0.5) \
               + nmos_lower_d_pin.uc().scale(1, 0.5)
        self.add_path(self.col_mux_stack[2],
                      [br_pin.bc(), mid1, mid2, nmos_lower_d_pin.center()])

    def extend_implants(self):
        """
        Add top-to-bottom implants for adjacency issues in s8.
        """
        # Route to the bottom
        ll = (self.nmos_lower.ll() - vector(2 * [self.implant_enclose_active])).scale(1, 0)
        # Don't route to the top
        ur = self.nmos_upper.ur() + vector(self.implant_enclose_active, 0)
        self.add_rect("nimplant",
                      ll,
                      ur.x - ll.x,
                      ur.y - ll.y)

    def add_pn_wells(self):
        """
        Add a well and implant over the whole cell. Also, add the
        pwell contact (if it exists)
        """
        if(cell_props.use_strap == True and OPTS.num_ports == 1):
            strap = factory.create(module_type=cell_props.strap_module, version=cell_props.strap_version)
            rbc_width = self.bitcell.width + strap.width
        else:
            rbc_width = self.bitcell.width
        # Add it to the right, aligned in between the two tx
        active_pos = vector(rbc_width,
                            self.nmos_upper.by() - 0.5 * self.poly_space)

        self.add_via_center(layers=self.active_stack,
                            offset=active_pos,
                            implant_type="p",
                            well_type="p")

        # If there is a li layer, include it in the power stack
        self.add_via_center(layers=self.col_mux_stack,
                            offset=active_pos)

        self.add_layout_pin_rect_center(text="gnd",
                                        layer="m1",
                                        offset=active_pos)

        # Add well enclosure over all the tx and contact
        if "pwell" in layer:
            self.add_rect(layer="pwell",
                          offset=vector(0, 0),
                          width=rbc_width,
                          height=self.height)
