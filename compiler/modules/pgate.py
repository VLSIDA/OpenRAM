# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from bisect import bisect_left
from openram import debug
from openram.base import design
from openram.base import vector
from openram.tech import layer, drc
from openram.tech import cell_properties as cell_props
from openram import OPTS

if cell_props.ptx.bin_spice_models:
    from openram.tech import nmos_bins, pmos_bins


class pgate(design):
    """
    This is a module that implements some shared
    functions for parameterized gates.
    """

    def __init__(self, name, height=None, add_wells=True):
        """ Creates a generic cell """
        super().__init__(name)

        if height:
            self.height = height
        elif not height:
            # By default, something simple
            self.height = 14 * self.m1_pitch
        self.add_wells = add_wells

        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"
        self.route_layer_width = getattr(self, "{}_width".format(self.route_layer))
        self.route_layer_space = getattr(self, "{}_space".format(self.route_layer))
        self.route_layer_pitch = getattr(self, "{}_pitch".format(self.route_layer))

        # hack for enclosing input pin with npc
        self.input_pin_vias = []

        # This is the space from a S/D contact to the supply rail
        contact_to_vdd_rail_space = 0.5 * self.route_layer_width + self.route_layer_space
        # This is a poly-to-poly of a flipped cell
        poly_to_poly_gate_space = self.poly_extend_active + 0.5 * self.poly_space

        self.top_bottom_space = max(contact_to_vdd_rail_space,
                                    poly_to_poly_gate_space)

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

    def connect_pin_to_rail(self, inst, pin_name, supply_name):
        """ Connects a ptx pin to a supply rail. """
        supply_pin = self.get_pin(supply_name)

        source_pins = inst.get_pins(pin_name)
        for source_pin in source_pins:

            if supply_name == "gnd":
                height = supply_pin.by() - source_pin.by()
            elif supply_name == "vdd":
                height = supply_pin.uy() - source_pin.by()
            else:
                debug.error("Invalid supply name.", -1)

            debug.check(supply_pin.layer == source_pin.layer, "Supply pin is not on correct layer.")
            self.add_rect(layer=source_pin.layer,
                          offset=source_pin.ll(),
                          height=height,
                          width=source_pin.width())

    def route_input_gate(self, pmos_inst, nmos_inst, ypos, name, position="left", directions=None):
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
        contact_width = self.poly_contact.width

        if position == "center":
            contact_offset = left_gate_offset \
                             + vector(0.5 * self.poly_width, 0)
        elif position == "farleft":
            contact_offset = left_gate_offset \
                             - vector(0.5 * self.poly_contact.width, 0)
        elif position == "left":
            contact_offset = left_gate_offset \
                             - vector(0.5 * contact_width - 0.5 * self.poly_width, 0)
        elif position == "right":
            contact_offset = left_gate_offset \
                             + vector(0.5 * contact_width + 0.5 * self.poly_width, 0)
        else:
            debug.error("Invalid contact placement option.", -1)

        via = self.add_via_stack_center(from_layer="poly",
                                        to_layer=self.route_layer,
                                        offset=contact_offset,
                                        directions=directions)

        self.add_layout_pin_rect_center(text=name,
                                        layer=self.route_layer,
                                        offset=contact_offset,
                                        width=via.mod.second_layer_width,
                                        height=via.mod.second_layer_height)
        # This is to ensure that the contact is
        # connected to the gate
        mid_point = contact_offset.scale(0.5, 1) \
                    + left_gate_offset.scale(0.5, 0)
        self.add_rect_center(layer="poly",
                             offset=mid_point,
                             height=self.poly_contact.first_layer_width,
                             width=left_gate_offset.x - contact_offset.x)

        return via

    def extend_wells(self):
        """ Extend the n/p wells to cover whole cell """

        # This should match the cells in the cell library
        self.nwell_yoffset = 0.48 * self.height
        full_height = self.height + 0.5 * self.m1_width


        # FIXME: float rounding problem
        if "nwell" in layer:
            # Add a rail width to extend the well to the top of the rail
            nwell_max_offset = max(self.find_highest_layer_coords("nwell").y,
                                   full_height)
            nwell_position = vector(0, self.nwell_yoffset) - vector(self.well_extend_active, 0)
            nwell_height = nwell_max_offset - self.nwell_yoffset
            self.add_rect(layer="nwell",
                          offset=nwell_position,
                          width=self.width + 2 * self.well_extend_active,
                          height=nwell_height)
            if "vtg" in layer:
                self.add_rect(layer="vtg",
                              offset=nwell_position,
                              width=self.width + 2 * self.well_extend_active,
                              height=nwell_height)

        # Start this half a rail width below the cell
        if "pwell" in layer:
            pwell_min_offset = min(self.find_lowest_layer_coords("pwell").y,
                                   -0.5 * self.m1_width)
            pwell_position = vector(-self.well_extend_active, pwell_min_offset)
            pwell_height = self.nwell_yoffset - pwell_position.y
            self.add_rect(layer="pwell",
                          offset=pwell_position,
                          width=self.width + 2 * self.well_extend_active,
                          height=pwell_height)
            if "vtg" in layer:
                self.add_rect(layer="vtg",
                              offset=pwell_position,
                              width=self.width + 2 * self.well_extend_active,
                              height=pwell_height)

        if cell_props.pgate.add_implants:
            self.extend_implants()

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
        contact_yoffset = min(self.height - 0.5 * self.implant_width,
                              self.get_tx_insts("pmos")[0].uy()) \
                             - pmos.active_contact.first_layer_height \
                             - self.implant_enclose_active
        contact_offset = vector(contact_xoffset, contact_yoffset)
        # Offset by half a contact in x and y
        contact_offset += vector(0.5 * pmos.active_contact.first_layer_width,
                                 0.5 * pmos.active_contact.first_layer_height)
        # This over-rides the default one with a custom direction
        self.nwell_contact = self.add_via_center(layers=layer_stack,
                                                 offset=contact_offset,
                                                 implant_type="n",
                                                 well_type="n",
                                                 directions=("V", "V"))

        self.add_rect_center(layer=self.route_layer,
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

    def extend_implants(self):
        """
        Add top-to-bottom implants for adjacency issues in s8.
        """
        if self.add_wells:
            rightx = None
        else:
            rightx = self.width

        nmos_insts = self.get_tx_insts("nmos")
        if len(nmos_insts) > 0:
            self.add_enclosure(nmos_insts,
                               layer="nimplant",
                               extend=self.implant_enclose_active,
                               leftx=0,
                               rightx=rightx,
                               boty=0)

        pmos_insts = self.get_tx_insts("pmos")
        if len(pmos_insts) > 0:
            self.add_enclosure(pmos_insts,
                               layer="pimplant",
                               extend=self.implant_enclose_active,
                               leftx=0,
                               rightx=rightx,
                               topy=self.height)

        self.add_rect(layer="pimplant",
                      offset=vector(0, self.height - 0.5 * self.implant_width),
                      width=self.width,
                      height=self.implant_width)
        self.add_rect(layer="nimplant",
                      offset=vector(0, -0.5 * self.implant_width),
                      width=self.width,
                      height=self.implant_width)


#        try:
#            ntap_insts = [self.nwell_contact]
#            self.add_enclosure(ntap_insts,
#                               layer="nimplant",
#                               extend=self.implant_enclose_active,
#                               rightx=self.width,
#                               topy=self.height)
#        except AttributeError:
#            pass
#        try:
#            ptap_insts = [self.pwell_contact]
#            self.add_enclosure(ptap_insts,
#                               layer="pimplant",
#                               extend=self.implant_enclose_active,
#                               rightx=self.width,
#                               boty=0)
#        except AttributeError:
#            pass

    def add_pwell_contact(self, nmos, nmos_pos):
        """ Add an pwell contact next to the given nmos device. """

        layer_stack = self.active_stack

        # To the right a spacing away from the nmos right active edge
        contact_xoffset = nmos_pos.x + nmos.active_width \
                          + self.active_space
        # Allow an nimplant below it under the rail
        contact_yoffset = max(0.5 * self.implant_width + self.implant_enclose_active,
                              self.get_tx_insts("nmos")[0].by())
        contact_offset = vector(contact_xoffset, contact_yoffset)

        # Offset by half a contact
        contact_offset += vector(0.5 * nmos.active_contact.first_layer_width,
                                 0.5 * nmos.active_contact.first_layer_height)
        self.pwell_contact= self.add_via_center(layers=layer_stack,
                                                offset=contact_offset,
                                                implant_type="p",
                                                well_type="p",
                                                directions=("V", "V"))

        self.add_rect_center(layer=self.route_layer,
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

    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top and bottom. """
        self.add_layout_pin_rect_center(text="gnd",
                                        layer=self.route_layer,
                                        offset=vector(0.5 * self.width, 0),
                                        width=self.width)

        self.add_layout_pin_rect_center(text="vdd",
                                        layer=self.route_layer,
                                        offset=vector(0.5 * self.width, self.height),
                                        width=self.width)

    def determine_width(self):
        """ Determine the width based on the well contacts (assumed to be on the right side) """

        # It was already set or is left as default (minimum)
        # Width is determined by well contact and spacing and allowing a supply via between each cell
        if self.add_wells:
            width = max(self.nwell_contact.rx(), self.pwell_contact.rx()) + self.m1_space + 0.5 * self.m1_via.width
            # Height is an input parameter, so it is not recomputed.
        else:
            max_active_xoffset = self.find_highest_layer_coords("active").x
            max_route_xoffset = self.find_highest_layer_coords(self.route_layer).x + 0.5 * self.m1_space
            width = max(max_active_xoffset, max_route_xoffset)

        self.width = width

    @staticmethod
    def best_bin(tx_type, target_width):
        """
        Determine the width transistor that meets the accuracy requirement and is larger than target_width.
        """

        # Find all of the relavent scaled bins and multiples
        scaled_bins = pgate.scaled_bins(tx_type, target_width)

        for (scaled_width, multiple) in scaled_bins:
            if abs(target_width - scaled_width) / target_width <= 1 - OPTS.accuracy_requirement:
                break
        else:
            debug.error("failed to bin tx size {}, try reducing accuracy requirement".format(target_width), 1)

        debug.info(2, "binning {0} tx, target: {4}, found {1} x {2} = {3}".format(tx_type,
                                                                                  multiple,
                                                                                  scaled_width / multiple,
                                                                                  scaled_width,
                                                                                  target_width))

        return(scaled_width / multiple, multiple)

    @staticmethod
    def scaled_bins(tx_type, target_width):
        """
        Determine a set of widths and multiples that could be close to the right size
        sorted by the fewest number of fingers.
        """
        if tx_type == "nmos":
            bins = nmos_bins[drc("minwidth_poly")]
        elif tx_type == "pmos":
            bins = pmos_bins[drc("minwidth_poly")]
        else:
            debug.error("invalid tx type")

        # Prune out bins that are too big, except for one bigger
        bins = bins[0:bisect_left(bins, target_width) + 1]

        # Determine multiple of target width for each bin
        if len(bins) == 1:
            scaled_bins = [(bins[0], math.ceil(target_width / bins[0]))]
        else:
            scaled_bins = []
            # Add the biggest size as 1x multiple
            scaled_bins.append((bins[-1], 1))
            # Compute discrete multiple of other sizes
            for width in reversed(bins[:-1]):
                multiple = math.ceil(target_width / width)
                scaled_bins.append((multiple * width, multiple))

        return(scaled_bins)

    @staticmethod
    def nearest_bin(tx_type, target_width):
        """
        Determine the nearest width to the given target_width
        while assuming a single multiple.
        """
        if tx_type == "nmos":
            bins = nmos_bins[drc("minwidth_poly")]
        elif tx_type == "pmos":
            bins = pmos_bins[drc("minwidth_poly")]
        else:
            debug.error("invalid tx type")

        # Find the next larger bin
        bin_loc = bisect_left(bins, target_width)
        if bin_loc < len(bins):
            return bins[bin_loc]
        else:
            return bins[-1]

    @staticmethod
    def bin_accuracy(ideal_width, width):
        return 1 - abs((ideal_width - width) / ideal_width)
