# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import contact
import design
import debug
import math
from pgate import pgate
from tech import parameter, drc
from tech import layer_indices, layer_stacks
from vector import vector
from globals import OPTS
from sram_factory import factory
from tech import cell_properties as cell_props
from utils import round_to_grid


class precharge(design.design):
    """
    Creates a single precharge cell
    This module implements the precharge bitline cell used in the design.
    """
    def __init__(self, name, size=1, bitcell_bl="bl", bitcell_br="br"):

        debug.info(2, "creating precharge cell {0}".format(name))
        super().__init__(name)

        self.bitcell = factory.create(module_type=OPTS.bitcell)
        self.beta = parameter["beta"]
        self.ptx_width = self.beta * parameter["min_tx_size"]
        self.ptx_mults = 1
        if(cell_props.use_strap == True and OPTS.num_ports == 1):
            strap = factory.create(module_type=cell_props.strap_module, version=cell_props.strap_version)
            self.width = self.bitcell.width + strap.width
        else:
            self.width = self.bitcell.width
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br
        self.bitcell_bl_pin =self.bitcell.get_pin(self.bitcell_bl)
        self.bitcell_br_pin =self.bitcell.get_pin(self.bitcell_br)

        if self.bitcell_bl_pin.layer == "m1":
            self.bitline_layer = "m1"
            self.en_layer = "m2"
        else:
            self.bitline_layer = "m2"
            self.en_layer = "m1"

        # Creates the netlist and layout
        # Since it has variable height, it is not a pgate.
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            self.DRC_LVS()

    def get_bl_names(self):
        return "bl"

    def get_br_names(self):
        return "br"

    def create_netlist(self):
        self.add_pins()
        self.add_ptx()
        self.create_ptx()

    def create_layout(self):

        self.place_ptx()
        self.connect_poly()
        self.route_en()
        self.place_nwell_and_contact()
        self.route_vdd_rail()
        self.route_bitlines()
        self.connect_to_bitlines()
        self.add_boundary()

    def add_pins(self):
        self.add_pin_list(["bl", "br", "en_bar", "vdd"],
                          ["OUTPUT", "OUTPUT", "INPUT", "POWER"])

    def add_ptx(self):
        """
        Initializes the upper and lower pmos
        """
        if cell_props.ptx.bin_spice_models:
            self.ptx_width = pgate.nearest_bin("pmos", self.ptx_width)
        self.pmos = factory.create(module_type="ptx",
                                   width=self.ptx_width,
                                   mults=self.ptx_mults,
                                   tx_type="pmos")
        self.add_mod(self.pmos)

    def route_vdd_rail(self):
        """
        Adds a vdd rail at the top of the cell
        """

        # Adds the rail across the width of the cell
        vdd_position = vector(0.5 * self.width, self.height)
        layer_width = drc("minwidth_" + self.en_layer)
        self.add_rect_center(layer=self.en_layer,
                             offset=vdd_position,
                             width=self.width,
                             height=layer_width)

        pmos_pin = self.upper_pmos2_inst.get_pin("S")

        # center of vdd rail
        pmos_vdd_pos = vector(pmos_pin.cx(), vdd_position.y)
        self.add_path(self.en_layer, [pmos_pin.center(), pmos_vdd_pos])

        self.add_power_pin("vdd",
                           self.well_contact_pos)

        self.add_via_stack_center(from_layer=pmos_pin.layer,
                                  to_layer=self.en_layer,
                                  offset=pmos_pin.center())

    def create_ptx(self):
        """
        Create both the upper_pmos and lower_pmos to the module
        """

        self.lower_pmos_inst = self.add_inst(name="lower_pmos",
                                             mod=self.pmos)
        self.connect_inst(["bl", "en_bar", "br", "vdd"])

        self.upper_pmos1_inst = self.add_inst(name="upper_pmos1",
                                              mod=self.pmos)
        self.connect_inst(["bl", "en_bar", "vdd", "vdd"])

        self.upper_pmos2_inst = self.add_inst(name="upper_pmos2",
                                              mod=self.pmos)
        self.connect_inst(["br", "en_bar", "vdd", "vdd"])

    def place_ptx(self):
        """
        Place both the upper_pmos and lower_pmos to the module
        """

        # reserve some offset to jog the bitlines
        self.initial_yoffset = self.pmos.active_offset.y + self.m2_pitch
        # Compute the other pmos2 location,
        # but determining offset to overlap the source and drain pins
        overlap_offset = self.pmos.get_pin("D").ll() - self.pmos.get_pin("S").ll()

        # adds the lower pmos to layout
        self.lower_pmos_position = vector(self.well_enclose_active + 0.5 * self.m1_width,
                                          self.initial_yoffset)
        self.lower_pmos_inst.place(self.lower_pmos_position)

        # adds the upper pmos(s) to layout with 2 M2 tracks
        ydiff = self.pmos.height + 2 * self.m2_pitch
        self.upper_pmos1_pos = self.lower_pmos_position + vector(0, ydiff)
        self.upper_pmos1_inst.place(self.upper_pmos1_pos)

        # Second pmos to the right of the first
        self.upper_pmos2_pos = self.upper_pmos1_pos + overlap_offset
        self.upper_pmos2_inst.place(self.upper_pmos2_pos)

    def connect_poly(self):
        """
        Connects the upper and lower pmos together
        """

        offset = self.lower_pmos_inst.get_pin("G").ul()
        # connects the top and bottom pmos' gates together
        ylength = self.upper_pmos1_inst.get_pin("G").ll().y - offset.y
        self.add_rect(layer="poly",
                      offset=offset,
                      width=self.poly_width,
                      height=ylength)

        # connects the two poly for the two upper pmos(s)
        offset = offset + vector(0, ylength - self.poly_width)
        xlength = self.upper_pmos2_inst.get_pin("G").lx() \
                  - self.upper_pmos1_inst.get_pin("G").lx() \
                  + self.poly_width
        self.add_rect(layer="poly",
                      offset=offset,
                      width=xlength,
                      height=self.poly_width)

    def route_en(self):
        """
        Adds the en input rail, en contact/vias, and connects to the pmos
        """

        # adds the en contact to connect the gates to the en rail
        pin_offset = self.lower_pmos_inst.get_pin("G").lr()
        # This is an extra space down for some techs with contact to active spacing
        contact_space = max(self.poly_space,
                            self.poly_contact_to_gate) + 0.5 * contact.poly_contact.first_layer_height
        offset = pin_offset - vector(0, contact_space)
        self.add_via_stack_center(from_layer="poly",
                                  to_layer=self.en_layer,
                                  offset=offset)
        self.add_path("poly",
                      [self.lower_pmos_inst.get_pin("G").bc(), offset])
        # adds the en rail
        self.add_layout_pin_segment_center(text="en_bar",
                                           layer=self.en_layer,
                                           start=offset.scale(0, 1),
                                           end=offset.scale(0, 1) + vector(self.width, 0))

    def place_nwell_and_contact(self):
        """
        Adds a nwell tap to connect to the vdd rail
        """

        # adds the contact from active to metal1
        offset_height = self.upper_pmos1_inst.uy() + \
                        contact.active_contact.height + \
                        self.nwell_extend_active
        self.well_contact_pos = self.upper_pmos1_inst.get_pin("D").center().scale(1, 0) + \
                                vector(0, offset_height)
        self.well_contact = self.add_via_center(layers=self.active_stack,
                                                offset=self.well_contact_pos,
                                                implant_type="n",
                                                well_type="n")
        self.add_via_stack_center(from_layer=self.active_stack[2],
                                  to_layer=self.bitline_layer,
                                  offset=self.well_contact_pos)

        self.height = self.well_contact_pos.y + contact.active_contact.height + self.m1_space

        # nwell should span the whole design since it is pmos only
        self.add_rect(layer="nwell",
                      offset=vector(0, 0),
                      width=self.width,
                      height=self.height)

        # TSMC18 gate port hack
        if OPTS.tech_name in ["tsmc18", "lapis20", "rohm180"]:
            # Body connection
            min_area = drc["minarea_{}".format(self.active_stack[0])]
            height = round_to_grid(self.well_contact.mod.first_layer_width)
            width = round_to_grid(min_area / height)
            width_impl = width + 2 * drc("implant_enclose_active")
            height_impl = height + 2 * drc("implant_enclose_active") # contact.py:250
            width_well = width + 2 * self.well_contact.mod.well_enclose_active
            height_well = height + 2 * self.well_contact.mod.well_enclose_active # contact.py:264
            self.add_rect_center(layer=self.active_stack[0],
                                 offset=self.well_contact_pos,
                                 width=width,
                                 height=height)
            self.add_rect_center(layer="nimplant",
                                 offset=self.well_contact_pos,
                                 width=width_impl,
                                 height=height_impl)
            self.add_rect_center(layer="nwell",
                                 offset=self.well_contact_pos,
                                 width=width_well,
                                 height=height_well)

            # Span of the whole pimp
            left = min(self.lower_pmos_position.x,
                       self.upper_pmos1_pos.x ,
                       self.upper_pmos2_pos.x) - drc("implant_enclose_active")
            right = max(self.lower_pmos_position.x + self.pmos.active_width,
                       self.upper_pmos1_pos.x + self.pmos.active_width,
                       self.upper_pmos2_pos.x + self.pmos.active_width) + drc("implant_enclose_active")
            top = max(self.lower_pmos_position.y + self.pmos.active_height,
                       self.upper_pmos1_pos.y + self.pmos.active_height,
                       self.upper_pmos2_pos.y + self.pmos.active_height) + drc("implant_enclose_active")
            bottom = min(self.lower_pmos_position.y,
                       self.upper_pmos1_pos.y,
                       self.upper_pmos2_pos.y) - drc("implant_enclose_active")
            self.add_rect(layer="pimplant",
                          offset=vector(left, bottom),
                          width=right - left,
                          height=top - bottom)

    def route_bitlines(self):
        """
        Adds both bit-line and bit-line-bar to the module
        """
        layer_pitch = getattr(self, "{}_pitch".format(self.bitline_layer))

        # adds the BL
        self.bl_xoffset = layer_pitch
        top_pos = vector(self.bl_xoffset, self.height)
        pin_pos = vector(self.bl_xoffset, 0)
        self.add_path(self.bitline_layer, [top_pos, pin_pos])
        self.bl_pin = self.add_layout_pin_segment_center(text="bl",
                                                         layer=self.bitline_layer,
                                                         start=pin_pos,
                                                         end=top_pos)

        # adds the BR
        self.br_xoffset = self.width - layer_pitch
        top_pos = vector(self.br_xoffset, self.height)
        pin_pos = vector(self.br_xoffset, 0)
        self.add_path(self.bitline_layer, [top_pos, pin_pos])
        self.br_pin = self.add_layout_pin_segment_center(text="br",
                                                         layer=self.bitline_layer,
                                                         start=pin_pos,
                                                         end=top_pos)

    def connect_to_bitlines(self):
        """
        Connect the bitlines to the devices
        """
        self.add_bitline_contacts()
        self.connect_pmos(self.lower_pmos_inst.get_pin("S"),
                          self.bl_xoffset)
        self.connect_pmos(self.lower_pmos_inst.get_pin("D"),
                          self.br_xoffset)

        self.connect_pmos(self.upper_pmos1_inst.get_pin("S"),
                          self.bl_xoffset)
        self.connect_pmos(self.upper_pmos2_inst.get_pin("D"),
                          self.br_xoffset)

    # Helper function for adding minarea rectangles when via (only for tsmc18 for now)
    def helper_areas(self, from_layer, to_layer, contact_offset):
        cur_layer = from_layer
        while cur_layer != to_layer:
            from_id = layer_indices[cur_layer]
            to_id   = layer_indices[to_layer]

            if from_id < to_id: # grow the stack up
                search_id = 0
                next_id = 2
            else: # grow the stack down
                search_id = 2
                next_id = 0

            #vprint("Putting {}".format(cur_layer))
            min_area = drc["minarea_{}".format(cur_layer)]
            width = round_to_grid(math.sqrt(min_area))
            height = round_to_grid(min_area / width)
            self.add_rect_center(layer=cur_layer,
                                 offset=contact_offset,
                                 width=width,
                                 height=height)

            curr_stack = next(filter(lambda stack: stack[search_id] == cur_layer, layer_stacks), None)
            cur_layer = curr_stack[next_id]

    def add_bitline_contacts(self):
        """
        Adds contacts/via from metal1 to metal2 for bit-lines
        """

        # BL
        for lower_pin in [self.lower_pmos_inst.get_pin("S"), self.lower_pmos_inst.get_pin("D")]:
            self.add_via_stack_center(from_layer=lower_pin.layer,
                                      to_layer=self.bitline_layer,
                                      offset=lower_pin.center(),
                                      directions=("V", "V"))
            if OPTS.tech_name in ["tsmc18", "lapis20", "rohm180"]:
                self.helper_areas(lower_pin.layer, self.bitline_layer, lower_pin.center())

        # BR
        for upper_pin in [self.upper_pmos1_inst.get_pin("S"), self.upper_pmos2_inst.get_pin("D")]:
            self.add_via_stack_center(from_layer=upper_pin.layer,
                                      to_layer=self.bitline_layer,
                                      offset=upper_pin.center(),
                                      directions=("V", "V"))
            if OPTS.tech_name in ["tsmc18", "lapis20", "rohm180"]:
                self.helper_areas(lower_pin.layer, self.bitline_layer, upper_pin.center())

    def connect_pmos(self, pmos_pin, bit_xoffset):
        """
        Connect a pmos pin to bitline pin
        """

        left_pos = vector(min(pmos_pin.cx(), bit_xoffset), pmos_pin.cy())
        right_pos = vector(max(pmos_pin.cx(), bit_xoffset), pmos_pin.cy())

        self.add_path(self.bitline_layer,
                      [left_pos, right_pos],
                      width=pmos_pin.height())

