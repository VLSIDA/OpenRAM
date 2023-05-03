# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import logical_effort
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer, drc, spice
from openram.tech import cell_properties as cell_props
from openram import OPTS


class ptx(design):
    """
    This module generates gds and spice of a parametrically NMOS or
    PMOS sized transistor.  Pins are accessed as D, G, S, B.  Width is
    the transistor width. Mults is the number of transistors of the
    given width. Total width is therefore mults*width.  Options allow
    you to connect the fingered gates and active for parallel devices.
    The add_*_contact option tells which layer to bring source/drain up to.

    ll, ur, width and height refer to the active area.
    Wells and poly may extend beyond this.

    """
    def __init__(self,
                 name="",
                 width=drc("minwidth_tx"),
                 mults=1,
                 tx_type="nmos",
                 add_source_contact=None,
                 add_drain_contact=None,
                 series_devices=False,
                 connect_drain_active=False,
                 connect_source_active=False,
                 connect_poly=False,
                 num_contacts=None,
                 ):

        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"

        # Default contacts are the lowest layer
        if add_source_contact == None:
            add_source_contact = self.route_layer

        # Default contacts are the lowest layer
        if add_drain_contact == None:
            add_drain_contact = self.route_layer

        # We need to keep unique names because outputting to GDSII
        # will use the last record with a given name. I.e., you will
        # over-write a design in GDS if one has and the other doesn't
        # have poly connected, for example.
        name = "{0}_m{1}_w{2:.3f}".format(tx_type, mults, width)
        name += "_s{}".format(add_source_contact)
        name += "_d{}".format(add_drain_contact)
        if series_devices:
            name += "_sd"
        if connect_drain_active:
            name += "_da"
        if connect_source_active:
            name += "_sa"
        if connect_poly:
            name += "_p"
        if num_contacts:
            name += "_c{}".format(num_contacts)
        # replace periods with underscore for newer spice compatibility
        name = name.replace('.', '_')
        debug.info(3, "creating ptx {0}".format(name))
        super().__init__(name)

        self.tx_type = tx_type
        self.mults = mults
        self.tx_width = width
        self.connect_drain_active = connect_drain_active
        self.connect_source_active = connect_source_active
        self.connect_poly = connect_poly
        self.add_source_contact = add_source_contact
        self.add_drain_contact = add_drain_contact
        self.series_devices = series_devices
        self.num_contacts = num_contacts

        self.route_layer_width = drc("minwidth_{}".format(self.route_layer))
        self.route_layer_space = drc("{0}_to_{0}".format(self.route_layer))

        # Since it has variable height, it is not a pgate.
        self.create_netlist()
        # We must always create ptx layout for pbitcell
        # some transistor sizes in other netlist depend on pbitcell
        self.create_layout()

        ll = self.find_lowest_coords()
        ur = self.find_highest_coords()
        self.add_boundary(ll, ur)

        # (0,0) will be the corner of the active area (not the larger well)
        self.translate_all(self.active_offset)

    def create_layout(self):
        """Calls all functions related to the generation of the layout"""
        self.setup_layout_constants()
        self.add_active()
        self.add_well_implant()
        self.add_poly()
        self.add_active_contacts()

        # for run-time, we won't check every transitor DRC independently
        # but this may be uncommented for debug purposes
        # self.DRC()

    def create_netlist(self):
        pin_list = ["D", "G", "S", "B"]
        if self.tx_type == "nmos":
            body_dir = "GROUND"
        else:
            body_dir = "POWER"
        dir_list = ["INOUT", "INPUT", "INOUT", body_dir]
        self.add_pin_list(pin_list, dir_list)

        # Just make a guess since these will actually
        # be decided in the layout later.
        area_sd = 2.5 * self.poly_width * self.tx_width
        perimeter_sd = 2 * self.poly_width + 2 * self.tx_width
        if cell_props.ptx.model_is_subckt:
            # sky130
            main_str = "X{{0}} {{1}} {0} m={1} w={2} l={3} ".format(spice[self.tx_type],
                                                                    self.mults,
                                                                    self.tx_width,
                                                                    drc("minwidth_poly"))
            # Perimeters are in microns
            # Area is in u since it is microns square
            area_str = "pd={0:.2f} ps={0:.2f} as={1:.2f}u ad={1:.2f}u".format(perimeter_sd,
                                                                              area_sd)
        else:
            main_str = "M{{0}} {{1}} {0} m={1} w={2}u l={3}u ".format(spice[self.tx_type],
                                                                      self.mults,
                                                                      self.tx_width,
                                                                      drc("minwidth_poly"))
            area_str = "pd={0:.2f}u ps={0:.2f}u as={1:.2f}p ad={1:.2f}p".format(perimeter_sd,
                                                                                area_sd)
        self.spice_device = main_str + area_str
        self.spice.append("\n* spice ptx " + self.spice_device)

        if cell_props.ptx.model_is_subckt and OPTS.lvs_exe and OPTS.lvs_exe[0] == "calibre":
            # sky130 requires mult parameter too. It is not the same as m, but I don't understand it.
            # self.lvs_device = "X{{0}} {{1}} {0} m={1} w={2} l={3} mult=1".format(spice[self.tx_type],
            #                                                                        self.mults,
            #                                                                        self.tx_width,
            #                                                                        drc("minwidth_poly"))
            # TEMP FIX: Use old device names if using Calibre.

            self.lvs_device = "M{{0}} {{1}} {0} m={1} w={2} l={3} mult=1".format("nshort" if self.tx_type == "nmos" else "pshort",
                                                                                 self.mults,
                                                                                 self.tx_width,
                                                                                 drc("minwidth_poly"))
        elif cell_props.ptx.model_is_subckt:
            self.lvs_device = "X{{0}} {{1}} {0} m={1} w={2}u l={3}u".format(spice[self.tx_type],
                                                                            self.mults,
                                                                            self.tx_width,
                                                                            drc("minwidth_poly"))
        else:
            self.lvs_device = "M{{0}} {{1}} {0} m={1} w={2}u l={3}u ".format(spice[self.tx_type],
                                                                             self.mults,
                                                                             self.tx_width,
                                                                             drc("minwidth_poly"))

    def setup_layout_constants(self):
        """
        Pre-compute some handy layout parameters.
        """

        if not self.num_contacts:
            self.num_contacts = self.calculate_num_contacts()

        # Determine layer types needed
        if self.tx_type == "nmos":
            self.implant_type = "n"
            self.well_type = "p"
        elif self.tx_type == "pmos":
            self.implant_type = "p"
            self.well_type = "n"
        else:
            self.error("Invalid transitor type.", -1)

        # This is not actually instantiated but used for calculations
        self.active_contact = factory.create(module_type="contact",
                                             layer_stack=self.active_stack,
                                             directions=("V", "V"),
                                             dimensions=(1, self.num_contacts))

        # This is the extra poly spacing due to the poly contact to poly contact pitch
        # of contacted gates
        extra_poly_contact_width = self.poly_contact.width - self.poly_width

        # This is the spacing between S/D contacts
        # This is the spacing between the poly gates
        self.min_poly_pitch = self.poly_space + self.poly_width
        self.contacted_poly_pitch = self.poly_space + self.poly_contact.width
        self.contact_pitch = 2 * self.active_contact_to_gate + self.poly_width + self.contact_width
        self.poly_pitch = max(self.min_poly_pitch,
                              self.contacted_poly_pitch,
                              self.contact_pitch)

        self.end_to_contact = 0.5 * self.active_contact.width

        # Active width is determined by enclosure on both ends and contacted pitch,
        # at least one poly and n-1 poly pitches
        self.active_width = 2 * self.end_to_contact + self.active_contact.width \
                            + 2 * self.active_contact_to_gate + self.poly_width + (self.mults - 1) * self.poly_pitch

        # Active height is just the transistor width
        self.active_height = self.tx_width

        # Poly height must include poly extension over active
        self.poly_height = self.tx_width + 2 * self.poly_extend_active

        self.active_offset = vector([self.well_enclose_active] * 2)

        # Well enclosure of active, ensure minwidth as well
        well_name = "{}well".format(self.well_type)
        if well_name in layer:
            well_width_rule = drc("minwidth_" + well_name)
            self.well_width = max(self.active_width + 2 * self.well_enclose_active,
                                  well_width_rule)
            self.well_height = max(self.active_height + 2 * self.well_enclose_active,
                                   well_width_rule)
        else:
            self.well_height = self.height
            self.well_width = self.width

        # We are going to shift the 0,0, so include that in the width and height
        self.height = self.active_height
        self.width = self.active_width

        # This is the center of the first active contact offset (centered vertically)
        self.contact_offset = self.active_offset + vector(0.5 * self.active_contact.width,
                                                          0.5 * self.active_height)

        # Min area results are just flagged for now.
        debug.check(self.active_width * self.active_height >= self.minarea_active,
                    "Minimum active area violated.")
        # We do not want to increase the poly dimensions to fix
        # an area problem as it would cause an LVS issue.
        debug.check(self.poly_width * self.poly_height >= self.minarea_poly,
                    "Minimum poly area violated.")

    def connect_fingered_poly(self, poly_positions):
        """
        Connect together the poly gates and create the single gate pin.
        The poly positions are the center of the poly gates
        and we will add a single horizontal connection.
        """
        # Nothing to do if there's one poly gate
        if len(poly_positions)<2:
            return

        # The width of the poly is from the left-most to right-most poly gate
        poly_width = poly_positions[-1].x - poly_positions[0].x + self.poly_width
        if self.tx_type == "pmos":
            # This can be limited by poly to active spacing
            # or the poly extension
            distance_below_active = self.poly_width + max(self.poly_to_active,
                                                          0.5 * self.poly_height)
            poly_offset = poly_positions[0] - vector(0.5 * self.poly_width,
                                                     distance_below_active)
        else:
            # This can be limited by poly to active spacing
            # or the poly extension
            distance_above_active = max(self.poly_to_active,
                                        0.5 * self.poly_height)
            poly_offset = poly_positions[0] + vector(-0.5 * self.poly_width,
                                                     distance_above_active)
        # Remove the old pin and add the new one
        # only keep the main pin
        self.remove_layout_pin("G")
        self.add_layout_pin(text="G",
                            layer="poly",
                            offset=poly_offset,
                            width=poly_width,
                            height=self.poly_width)

    def connect_fingered_active(self, positions, pin_name, top):
        """
        Connect each contact  up/down to a source or drain pin
        """

        if len(positions) <= 1:
            return

        layer_space = getattr(self, "{}_space".format(self.route_layer))
        layer_width = getattr(self, "{}_width".format(self.route_layer))

        # This is the distance that we must route up or down from the center
        # of the contacts to avoid DRC violations to the other contacts
        pin_offset = vector(0,
                            0.5 * self.active_contact.second_layer_height + layer_space + 0.5 * layer_width)
        # This is the width of a m1 extend the ends of the pin
        end_offset = vector(layer_width / 2.0, 0)

        # We move the opposite direction from the bottom
        if not top:
            offset = pin_offset.scale(-1, -1)
        else:
            offset = pin_offset

        # remove the individual connections
        self.remove_layout_pin(pin_name)
        # Add each vertical segment
        for a in positions:
            self.add_path(self.route_layer,
                          [a, a + offset])
        # Add a single horizontal pin
        self.add_layout_pin_segment_center(text=pin_name,
                                           layer=self.route_layer,
                                           start=positions[0] + offset - end_offset,
                                           end=positions[-1] + offset + end_offset)

    def add_poly(self):
        """
        Add the poly gates(s) and (optionally) connect them.
        """
        # poly is one contacted spacing from the end and down an extension
        poly_offset = self.contact_offset \
                      + vector(0.5 * self.active_contact.width + 0.5 * self.poly_width + self.active_contact_to_gate, 0)

        # poly_positions are the bottom center of the poly gates
        self.poly_positions = []
        self.poly_gates = []

        # It is important that these are from left to right,
        # so that the pins are in the right
        # order for the accessors
        for i in range(0, self.mults):
            # Add this duplicate rectangle in case we remove
            # the pin when joining fingers
            self.add_rect_center(layer="poly",
                                 offset=poly_offset,
                                 height=self.poly_height,
                                 width=self.poly_width)
            gate = self.add_layout_pin_rect_center(text="G",
                                                   layer="poly",
                                                   offset=poly_offset,
                                                   height=self.poly_height,
                                                   width=self.poly_width)
            self.poly_positions.append(poly_offset)
            self.poly_gates.append(gate)

            poly_offset = poly_offset + vector(self.poly_pitch, 0)

        if self.connect_poly:
            self.connect_fingered_poly(self.poly_positions)

    def add_active(self):
        """
        Adding the diffusion (active region = diffusion region)
        """
        self.active = self.add_rect(layer="active",
                                    offset=self.active_offset,
                                    width=self.active_width,
                                    height=self.active_height)
        # If the implant must enclose the active, shift offset
        # and increase width/height
        enclose_width = self.implant_enclose_active
        enclose_offset = [enclose_width] * 2
        self.implant = self.add_rect(layer="{}implant".format(self.implant_type),
                                     offset=self.active_offset - enclose_offset,
                                     width=self.active_width + 2 * enclose_width,
                                     height=self.active_height + 2 * enclose_width)

    def add_well_implant(self):
        """
        Add an (optional) well and implant for the type of transistor.
        """
        well_name = "{}well".format(self.well_type)
        if not (well_name in layer or "vtg" in layer):
            return

        center_pos = self.active_offset + vector(0.5 * self.active_width,
                                                 0.5 * self.active_height)
        well_ll = center_pos - vector(0.5 * self.well_width,
                                      0.5 * self.well_height)
        if well_name in layer:
            well = self.add_rect(layer=well_name,
                                 offset=well_ll,
                                 width=self.well_width,
                                 height=self.well_height)
            setattr(self, well_name, well)

        if "vtg" in layer:
            self.add_rect(layer="vtg",
                          offset=well_ll,
                          width=self.well_width,
                          height=self.well_height)

    def calculate_num_contacts(self):
        """
        Calculates the possible number of source/drain contacts in a finger.
        For now, it is hard set as 1.
        """
        return 1

    def add_active_contacts(self):
        """
        Add the active contacts to the transistor.
        """
        drain_positions = []
        source_positions = []

        # Keep a list of the source/drain contacts
        self.source_contacts = []
        self.drain_contacts = []

        # First one is always a SOURCE
        label = "S"
        pos = self.contact_offset
        if self.add_source_contact:
            contact = self.add_diff_contact(label, pos)
            self.source_contacts.append(contact)
        else:
            self.add_layout_pin_rect_center(text=label,
                                            layer="active",
                                            offset=pos)
        source_positions.append(pos)

        # Skip these if they are going to be in series
        if not self.series_devices:
            for (poly1, poly2) in zip(self.poly_positions, self.poly_positions[1:]):
                pos = vector(0.5 * (poly1.x + poly2.x),
                             self.contact_offset.y)
                # Alternate source and drains
                if label == "S":
                    label = "D"
                    drain_positions.append(pos)
                else:
                    label = "S"
                    source_positions.append(pos)

                if (label=="S" and self.add_source_contact):
                    contact = self.add_diff_contact(label, pos)
                    self.source_contacts.append(contact)
                elif (label=="D" and self.add_drain_contact):
                    contact = self.add_diff_contact(label, pos)
                    self.drain_contacts.append(contact)
                else:
                    self.add_layout_pin_rect_center(text=label,
                                                    layer="active",
                                                    offset=pos)

        pos = vector(self.active_offset.x + self.active_width - 0.5 * self.active_contact.width,
                     self.contact_offset.y)
        # Last one is the opposite of previous
        if label == "S":
            label = "D"
            drain_positions.append(pos)
        else:
            label = "S"
            source_positions.append(pos)

        if (label=="S" and self.add_source_contact):
            contact = self.add_diff_contact(label, pos)
            self.source_contacts.append(contact)
        elif (label=="D" and self.add_drain_contact):
            contact = self.add_diff_contact(label, pos)
            self.drain_contacts.append(contact)
        else:
            self.add_layout_pin_rect_center(text=label,
                                            layer="active",
                                            offset=pos)

        if self.connect_source_active:
            self.connect_fingered_active(source_positions, "S", top=(self.tx_type=="pmos"))

        if self.connect_drain_active:
            self.connect_fingered_active(drain_positions, "D", top=(self.tx_type=="nmos"))

    def get_stage_effort(self, cout):
        """Returns an object representing the parameters for delay in tau units."""

        # FIXME: Using the same definition as the pinv.py.
        parasitic_delay = 1
        size = self.mults * self.tx_width / drc("minwidth_tx")
        return logical_effort(self.name,
                              size,
                              self.input_load(),
                              cout,
                              parasitic_delay)

    def input_load(self):
        """
        Returns the relative gate cin of the tx
        """

        # FIXME: this will be applied for the loads of the drain/source
        return self.mults * self.tx_width / drc("minwidth_tx")

    def add_diff_contact(self, label, pos):

        if label == "S":
            layer = self.add_source_contact
        elif label == "D":
            layer = self.add_drain_contact
        else:
            debug.error("Invalid source drain name.")

        if layer != "active":
            via=self.add_via_stack_center(offset=pos,
                                          from_layer="active",
                                          to_layer=layer,
                                          size=(1, self.num_contacts),
                                          directions=("V", "V"),
                                          implant_type=self.implant_type,
                                          well_type=self.well_type)

            pin_height = via.mod.second_layer_height
            pin_width = via.mod.second_layer_width
        else:
            via = None

            pin_height = None
            pin_width = None

        # Source drain vias are all vertical
        self.add_layout_pin_rect_center(text=label,
                                        layer=layer,
                                        offset=pos,
                                        width=pin_width,
                                        height=pin_height)

        return(via)

    def get_cin(self):
        """Returns the relative gate cin of the tx"""
        return self.tx_width / drc("minwidth_tx")

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)

    def is_non_inverting(self):
        """Return input to output polarity for module"""

        return True

    def get_on_resistance(self):
        """On resistance of pinv, defined by single nmos"""
        is_nchannel = (self.tx_type == "nmos")
        stack = 1
        is_cell = False
        return self.tr_r_on(self.tx_width, is_nchannel, stack, is_cell)

    def get_input_capacitance(self):
        """Input cap of input, passes width of gates to gate cap function"""
        return self.gate_c(self.tx_width)

    def get_intrinsic_capacitance(self):
        """Get the drain capacitances of the TXs in the gate."""
        return self.drain_c_(self.tx_width*self.mults,
                             1,
                             self.mults)
