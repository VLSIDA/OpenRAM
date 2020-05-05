# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import contact
import design
import debug
import math
from bisect import bisect_left
from tech import layer, drc
from vector import vector
from globals import OPTS

if(OPTS.tech_name == "s8"):
    from tech import nmos_bins, pmos_bins, accuracy_requirement

class pgate(design.design):
    """
    This is a module that implements some shared
    functions for parameterized gates.
    """

    def __init__(self, name, height=None):
        """ Creates a generic cell """
        design.design.__init__(self, name)

        if height:
            self.height = height
        elif not height:
            # By default, we make it 10 M1 pitch tall
            self.height = 10*self.m1_pitch
            
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            self.add_boundary()
            self.DRC_LVS()

    def create_netlist(self):
        """ Pure virtual function """
        debug.error("Must over-ride create_netlist.", -1)
        
    def create_layout(self):
        """ Pure virtual function """
        debug.error("Must over-ride create_layout.", -1)

    def connect_pin_to_rail(self, inst, pin, supply):
        """ Connects a ptx pin to a supply rail. """
        source_pin = inst.get_pin(pin)
        supply_pin = self.get_pin(supply)
        if supply_pin.overlaps(source_pin):
            return
            
        if supply == "gnd":
            height = supply_pin.by() - source_pin.by()
        elif supply == "vdd":
            height = supply_pin.uy() - source_pin.by()
        else:
            debug.error("Invalid supply name.", -1)
        
        if abs(height) > 0:
            self.add_rect(layer="m1",
                          offset=source_pin.ll(),
                          height=height,
                          width=source_pin.width())
    
    def route_input_gate(self, pmos_inst, nmos_inst, ypos, name, position="left"):
        """
        Route the input gate to the left side of the cell for access.
        Position specifies to place the contact the left, center, or
        right of gate.
        """

        nmos_gate_pin = nmos_inst.get_pin("G")
        pmos_gate_pin = pmos_inst.get_pin("G")

        # Check if the gates are aligned and give an error if they aren't!
        if nmos_gate_pin.ll().x != pmos_gate_pin.ll().x:
            self.gds_write("unaliged_gates.gds")
        debug.check(nmos_gate_pin.ll().x == pmos_gate_pin.ll().x,
                    "Connecting unaligned gates not supported. See unaligned_gates.gds.")
        
        # Pick point on the left of NMOS and up to PMOS
        nmos_gate_pos = nmos_gate_pin.ul() + vector(0.5 * self.poly_width, 0)
        pmos_gate_pos = vector(nmos_gate_pos.x, pmos_gate_pin.bc().y)
        self.add_path("poly", [nmos_gate_pos, pmos_gate_pos])

        # Add the via to the cell midpoint along the gate
        left_gate_offset = vector(nmos_gate_pin.lx(), ypos)

        # Center is completely symmetric.
        contact_width = contact.poly_contact.width
        contact_m1_width = contact.poly_contact.second_layer_width
        contact_m1_height = contact.poly_contact.second_layer_height
            
        if position == "center":
            contact_offset = left_gate_offset \
                             + vector(0.5 * self.poly_width, 0)
        elif position == "farleft":
            contact_offset = left_gate_offset \
                             - vector(0.5 * contact.poly_contact.width, 0)
        elif position == "left":
            contact_offset = left_gate_offset \
                             - vector(0.5 * contact_width - 0.5 * self.poly_width, 0)
        elif position == "right":
            contact_offset = left_gate_offset \
                             + vector(0.5 * contact_width + 0.5 * self.poly_width, 0)
        else:
            debug.error("Invalid contact placement option.", -1)

        if hasattr(self, "li_stack"):
            self.add_via_center(layers=self.li_stack,
                                offset=contact_offset)
            
        self.add_via_center(layers=self.poly_stack,
                            offset=contact_offset)

        self.add_layout_pin_rect_center(text=name,
                                        layer="m1",
                                        offset=contact_offset,
                                        width=contact_m1_width,
                                        height=contact_m1_height)
        # This is to ensure that the contact is
        # connected to the gate
        mid_point = contact_offset.scale(0.5, 1) \
                    + left_gate_offset.scale(0.5, 0)
        self.add_rect_center(layer="poly",
                             offset=mid_point,
                             height=contact.poly_contact.first_layer_width,
                             width=left_gate_offset.x - contact_offset.x)

    def extend_wells(self):
        """ Extend the n/p wells to cover whole cell """

        # This should match the cells in the cell library
        self.nwell_y_offset = 0.48 * self.height
        full_height = self.height + 0.5* self.m1_width
        
        # FIXME: float rounding problem
        if "nwell" in layer:
            # Add a rail width to extend the well to the top of the rail
            nwell_max_offset = max(self.find_highest_layer_coords("nwell").y,
                                   full_height)
            nwell_position = vector(0, self.nwell_y_offset) - vector(self.well_extend_active, 0)
            nwell_height = nwell_max_offset - self.nwell_y_offset
            self.add_rect(layer="nwell",
                          offset=nwell_position,
                          width=self.well_width,
                          height=nwell_height)
            if "vtg" in layer:
                self.add_rect(layer="vtg",
                              offset=nwell_position,
                              width=self.well_width,
                              height=nwell_height)

        # Start this half a rail width below the cell
        if "pwell" in layer:
            pwell_min_offset = min(self.find_lowest_layer_coords("pwell").y,
                                   -0.5 * self.m1_width)
            pwell_position = vector(-self.well_extend_active, pwell_min_offset)
            pwell_height = self.nwell_y_offset - pwell_position.y
            self.add_rect(layer="pwell",
                          offset=pwell_position,
                          width=self.well_width,
                          height=pwell_height)
            if "vtg" in layer:
                self.add_rect(layer="vtg",
                              offset=pwell_position,
                              width=self.well_width,
                              height=pwell_height)

    def add_nwell_contact(self, pmos, pmos_pos):
        """ Add an nwell contact next to the given pmos device. """
        
        layer_stack = self.active_stack
        
        # To the right a spacing away from the pmos right active edge
        contact_xoffset = pmos_pos.x + pmos.active_width \
                          + self.active_space
        
        # Must be at least an well enclosure of active down
        # from the top of the well
        # OR align the active with the top of PMOS active.
        max_y_offset = self.height + 0.5 * self.m1_width
        contact_yoffset = min(pmos_pos.y + pmos.active_height - pmos.active_contact.first_layer_height,
                              max_y_offset - pmos.active_contact.first_layer_height / 2 - self.nwell_enclose_active)
        contact_offset = vector(contact_xoffset, contact_yoffset)
        # Offset by half a contact in x and y
        contact_offset += vector(0.5 * pmos.active_contact.first_layer_width,
                                 0.5 * pmos.active_contact.first_layer_height)
        self.nwell_contact = self.add_via_center(layers=layer_stack,
                                                 offset=contact_offset,
                                                 implant_type="n",
                                                 well_type="n")
        if hasattr(self, "li_stack"):
            self.add_via_center(layers=self.li_stack,
                                offset=contact_offset)
        
        self.add_rect_center(layer="m1",
                             offset=contact_offset + vector(0, 0.5 * (self.height - contact_offset.y)),
                             width=self.nwell_contact.mod.second_layer_width,
                             height=self.height - contact_offset.y)
        
        # Now add the full active and implant for the PMOS
        # active_offset = pmos_pos + vector(pmos.active_width,0)
        # This might be needed if the spacing between the actives
        # is not satisifed
        # self.add_rect(layer="active",
        #               offset=active_offset,
        #               width=pmos.active_contact.width,
        #               height=pmos.active_height)

        # we need to ensure implants don't overlap and are
        # spaced far enough apart
        # implant_spacing = self.implant_space+self.implant_enclose_active
        # implant_offset = active_offset + vector(implant_spacing,0) \
        # - vector(0,self.implant_enclose_active)
        # implant_width = pmos.active_contact.width \
        # + 2*self.implant_enclose_active
        # implant_height = pmos.active_height + 2*self.implant_enclose_active
        # self.add_rect(layer="nimplant",
        #               offset=implant_offset,
        #               width=implant_width,
        #               height=implant_height)

        # Return the top of the well

    def add_pwell_contact(self, nmos, nmos_pos):
        """ Add an pwell contact next to the given nmos device. """

        layer_stack = self.active_stack

        # To the right a spacing away from the nmos right active edge
        contact_xoffset = nmos_pos.x + nmos.active_width \
                          + self.active_space
        # Must be at least an well enclosure of active up
        # from the bottom of the well
        contact_yoffset = max(nmos_pos.y,
                              self.nwell_enclose_active \
                              - nmos.active_contact.first_layer_height / 2)
        contact_offset = vector(contact_xoffset, contact_yoffset)

        # Offset by half a contact
        contact_offset += vector(0.5 * nmos.active_contact.first_layer_width,
                                 0.5 * nmos.active_contact.first_layer_height)
        self.pwell_contact= self.add_via_center(layers=layer_stack,
                                                offset=contact_offset,
                                                implant_type="p",
                                                well_type="p")

        if hasattr(self, "li_stack"):
            self.add_via_center(layers=self.li_stack,
                                offset=contact_offset)

        self.add_rect_center(layer="m1",
                             offset=contact_offset.scale(1, 0.5),
                             width=self.pwell_contact.mod.second_layer_width,
                             height=contact_offset.y)
        
        # Now add the full active and implant for the NMOS
        # active_offset = nmos_pos + vector(nmos.active_width,0)
        # This might be needed if the spacing between the actives
        # is not satisifed
        # self.add_rect(layer="active",
        #               offset=active_offset,
        #               width=nmos.active_contact.width,
        #               height=nmos.active_height)

        # implant_spacing = self.implant_space+self.implant_enclose_active
        # implant_offset = active_offset + vector(implant_spacing,0) \
        # - vector(0,self.implant_enclose_active)
        # implant_width = nmos.active_contact.width \
        # + 2*self.implant_enclose_active
        # implant_height = nmos.active_height + 2*self.implant_enclose_active
        # self.add_rect(layer="pimplant",
        #               offset=implant_offset,
        #               width=implant_width,
        #               height=implant_height)

    def determine_width(self):
        """ Determine the width based on the well contacts (assumed to be on the right side) """
        # Width is determined by well contact and spacing and allowing a supply via between each cell
        self.width = max(self.nwell_contact.rx(), self.pwell_contact.rx()) + self.m1_space + 0.5 * contact.m1_via.width
        self.well_width = self.width + 2 * self.nwell_enclose_active
        # Height is an input parameter, so it is not recomputed.

    @staticmethod
    def bin_width(tx_type, target_width):
        
        if tx_type == "nmos":
            bins = nmos_bins[drc("minwidth_poly")]
        elif tx_type == "pmos":
            bins = pmos_bins[drc("minwidth_poly")]
        else:
            debug.error("invalid tx type")
        
        bins = bins[0:bisect_left(bins, target_width) + 1]
        if len(bins) == 1:
            selected_bin = bins[0]
            scaling_factor = math.ceil(target_width / selected_bin)
            scaled_bin = bins[0] * scaling_factor
            
        else:
            scaled_bins = []
            scaling_factors = []
            scaled_bins.append(bins[-1])
            scaling_factors.append(1)
            for width in bins[0:-1]:
                m = math.ceil(target_width / width)
                scaling_factors.append(m)
                scaled_bins.append(m * width)

            select = bisect_left(scaled_bins, target_width)
            scaling_factor = scaling_factors[select]
            scaled_bin = scaled_bins[select]
            select = (select + 1) % len(scaled_bins)
            selected_bin = bins[select]

        debug.info(2, "binning {0} tx, target: {4}, found {1} x {2} = {3}".format(tx_type, selected_bin, scaling_factor, scaled_bin, target_width))

        return(selected_bin, scaling_factor)

    def permute_widths(self, tx_type, target_width):

        if tx_type == "nmos":
            bins = nmos_bins[drc("minwidth_poly")]
        elif tx_type == "pmos":
            bins = pmos_bins[drc("minwidth_poly")]
        else:
            debug.error("invalid tx type")       
        bins = bins[0:bisect_left(bins, target_width) + 1]
        if len(bins) == 1:
            scaled_bins = [(bins[0], math.ceil(target_width / bins[0]))]
        else:
            scaled_bins = []
            scaled_bins.append((bins[-1], 1))
            for width in bins[:-1]:
                m = math.ceil(target_width / width)
                scaled_bins.append((m * width, m))

        return(scaled_bins)
        
    def bin_accuracy(self, ideal_width, width):
        return abs(1-(ideal_width - width)/ideal_width)