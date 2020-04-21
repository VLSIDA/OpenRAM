# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import pgate
import debug
from tech import drc, layer
from vector import vector
from sram_factory import factory
import logical_effort


class single_level_column_mux(pgate.pgate):
    """
    This module implements the columnmux bitline cell used in the design.
    Creates a single columnmux cell with the given integer size relative
    to minimum size. Default is 8x. Per Samira and Hodges-Jackson book:
    Column-mux transistors driven by the decoder must be sized
    for optimal speed
    """
    def __init__(self, name, tx_size=8, bitcell_bl="bl", bitcell_br="br"):

        debug.info(2, "creating single column mux cell: {0}".format(name))

        self.tx_size = int(tx_size)
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br

        pgate.pgate.__init__(self, name)

    def get_bl_names(self):
        return "bl"

    def get_br_names(self):
        return "br"

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.add_ptx()

    def create_layout(self):

        self.pin_height = 2 * self.m2_width
        self.width = self.bitcell.width
        self.height = self.nmos_upper.uy() + self.pin_height
        self.connect_poly()
        self.add_bitline_pins()
        self.connect_bitlines()
        self.add_wells()

    def add_modules(self):
        self.bitcell = factory.create(module_type="bitcell")

        # Adds nmos_lower,nmos_upper to the module
        self.ptx_width = self.tx_size * drc("minwidth_tx")
        self.nmos = factory.create(module_type="ptx",
                                    width=self.ptx_width,
                                    add_source_contact=False,
                                    add_drain_contact=False)
        self.add_mod(self.nmos)

    def add_pins(self):
        self.add_pin_list(["bl", "br", "bl_out", "br_out", "sel", "gnd"])

    def add_bitline_pins(self):
        """ Add the top and bottom pins to this cell """

        bl_pin=self.bitcell.get_pin(self.bitcell_bl)
        br_pin=self.bitcell.get_pin(self.bitcell_br)

        bl_pos = vector(bl_pin.lx(), 0)
        br_pos = vector(br_pin.lx(), 0)

        # bl and br
        self.add_layout_pin(text="bl",
                            layer=bl_pin.layer,
                            offset=bl_pos + vector(0, self.height - self.pin_height),
                            height=self.pin_height)
        self.add_layout_pin(text="br",
                            layer=br_pin.layer,
                            offset=br_pos + vector(0, self.height - self.pin_height),
                            height=self.pin_height)

        # bl_out and br_out
        self.add_layout_pin(text="bl_out",
                            layer=bl_pin.layer,
                            offset=bl_pos,
                            height=self.pin_height)
        self.add_layout_pin(text="br_out",
                            layer=br_pin.layer,
                            offset=br_pos,
                            height=self.pin_height)

    def add_ptx(self):
        """ Create the two pass gate NMOS transistors to switch the bitlines"""

        # Space it in the center
        nmos_lower_position = self.nmos.active_offset.scale(0,1) \
                              + vector(0.5 * self.bitcell.width- 0.5 * self.nmos.active_width, 0)
        self.nmos_lower = self.add_inst(name="mux_tx1",
                                        mod=self.nmos,
                                        offset=nmos_lower_position)
        self.connect_inst(["bl", "sel", "bl_out", "gnd"])

        # This aligns it directly above the other tx with gates abutting
        nmos_upper_position = nmos_lower_position \
                                + vector(0, self.nmos.active_height + max(self.active_space,self.poly_space))
        self.nmos_upper = self.add_inst(name="mux_tx2",
                                        mod=self.nmos,
                                        offset=nmos_upper_position)
        self.connect_inst(["br", "sel", "br_out", "gnd"])

    def connect_poly(self):
        """ Connect the poly gate of the two pass transistors """

        # offset is the top of the lower nmos' diffusion
        # height is the distance between the nmos' diffusions, which depends on max(self.active_space,self.poly_space)
        offset = self.nmos_lower.get_pin("G").ul() - vector(0,self.poly_extend_active)
        height = self.nmos_upper.get_pin("G").by() + self.poly_extend_active - offset.y
        self.add_layout_pin(text="sel",
                            layer="poly",
                            offset=offset,
                            height=height)

    def connect_bitlines(self):
        """ Connect the bitlines to the mux transistors """
        # These are on metal2
        bl_pin = self.get_pin("bl")
        br_pin = self.get_pin("br")
        bl_out_pin = self.get_pin("bl_out")
        br_out_pin = self.get_pin("br_out")

        # These are on metal1
        nmos_lower_s_pin = self.nmos_lower.get_pin("S")
        nmos_lower_d_pin = self.nmos_lower.get_pin("D")
        nmos_upper_s_pin = self.nmos_upper.get_pin("S")
        nmos_upper_d_pin = self.nmos_upper.get_pin("D")

        # If li exists, use li and m1 for the mux, otherwise use m1 and m2
        if "li" in layer:
            col_mux_stack = self.li_stack
        else:
            col_mux_stack = self.m1_stack

        # Add vias to bl, br_out, nmos_upper/S, nmos_lower/D
        self.add_via_center(layers=col_mux_stack,
                            offset=bl_pin.bc(),
                            directions=("V", "V"))
        self.add_via_center(layers=col_mux_stack,
                            offset=br_out_pin.uc(),
                            directions=("V", "V"))
        self.add_via_center(layers=col_mux_stack,
                            offset=nmos_upper_s_pin.center(),
                            directions=("V", "V"))
        self.add_via_center(layers=col_mux_stack,
                            offset=nmos_lower_d_pin.center(),
                            directions=("V", "V"))

        # Add diffusion contacts
        # These were previously omitted with the options: add_source_contact=False, add_drain_contact=False
        # They are added now and not previously due to a s8 tech special case in which the contacts intersected the mux intraconnect
        self.add_via_center(layers=self.active_stack,
                            offset=nmos_upper_d_pin.center(),
                            directions=("V", "V"),
                            implant_type="n",
                            well_type="nwell")
        self.add_via_center(layers=self.active_stack,
                            offset=nmos_lower_s_pin.center(),
                            directions=("V", "V"),
                            implant_type="n",
                            well_type="nwell")
        self.add_via_center(layers=self.active_stack,
                            offset=nmos_upper_s_pin.center(),
                            directions=("V", "V"),
                            implant_type="n",
                            well_type="nwell")
        self.add_via_center(layers=self.active_stack,
                            offset=nmos_lower_d_pin.center(),
                            directions=("V", "V"),
                            implant_type="n",
                            well_type="nwell")

        # bl -> nmos_upper/D on metal1
        # bl_out -> nmos_upper/S on metal2
        self.add_path(col_mux_stack[0],
                      [bl_pin.ll(), vector(nmos_upper_d_pin.cx(), bl_pin.by()),
                       nmos_upper_d_pin.center()])
        # halfway up, move over
        mid1 = bl_out_pin.uc().scale(1, 0.4) \
               + nmos_upper_s_pin.bc().scale(0, 0.4)
        mid2 = bl_out_pin.uc().scale(0, 0.4) \
               + nmos_upper_s_pin.bc().scale(1, 0.4)
        self.add_path(col_mux_stack[2],
                      [bl_out_pin.uc(), mid1, mid2, nmos_upper_s_pin.center()])

        # br -> nmos_lower/D on metal2
        # br_out -> nmos_lower/S on metal1
        self.add_path(col_mux_stack[0],
                      [br_out_pin.uc(),
                       vector(nmos_lower_s_pin.cx(), br_out_pin.uy()),
                       nmos_lower_s_pin.center()])
        # halfway up, move over
        mid1 = br_pin.bc().scale(1,0.5) \
               + nmos_lower_d_pin.uc().scale(0,0.5)
        mid2 = br_pin.bc().scale(0,0.5) \
               + nmos_lower_d_pin.uc().scale(1,0.5)
        self.add_path(col_mux_stack[2],
                      [br_pin.bc(), mid1, mid2, nmos_lower_d_pin.center()])

    def add_wells(self):
        """
        Add a well and implant over the whole cell. Also, add the
        pwell contact (if it exists)
        """

        # Add it to the right, aligned in between the two tx
        active_pos = vector(self.bitcell.width,
                            self.nmos_upper.by() - 0.5 * self.poly_space)
        self.add_via_center(layers=self.active_stack,
                            offset=active_pos,
                            implant_type="p",
                            well_type="p")

        # Add the M1->..->power_grid_layer stack
        self.add_power_pin(name = "gnd",
                           loc = active_pos,
                           start_layer="m1")

        # Add well enclosure over all the tx and contact
        if "pwell" in layer:
            self.add_rect(layer="pwell",
                          offset=vector(0, 0),
                          width=self.bitcell.width,
                          height=self.height)

    def get_stage_effort(self, corner, slew, load):
        """
        Returns relative delay that the column mux.
        Difficult to convert to LE model.
        """
        parasitic_delay = 1
        # This is not CMOS, so using this may be incorrect.
        cin = 2 * self.tx_size
        return logical_effort.logical_effort("column_mux",
                                             self.tx_size,
                                             cin,
                                             load,
                                             parasitic_delay,
                                             False)
