# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
import debug
from tech import layer, drc, spice
from vector import vector
from sram_factory import factory


class ptx(design.design):
    """
    This module generates gds and spice of a parametrically NMOS or
    PMOS sized transistor.  Pins are accessed as D, G, S, B.  Width is
    the transistor width. Mults is the number of transistors of the
    given width. Total width is therefore mults*width.  Options allow
    you to connect the fingered gates and active for parallel devices.

    """
    def __init__(self,
                 name="",
                 width=drc("minwidth_tx"),
                 mults=1,
                 tx_type="nmos",
                 connect_active=False,
                 connect_poly=False,
                 num_contacts=None):
        # We need to keep unique names because outputting to GDSII
        # will use the last record with a given name. I.e., you will
        # over-write a design in GDS if one has and the other doesn't
        # have poly connected, for example.
        name = "{0}_m{1}_w{2:.3f}".format(tx_type, mults, width)
        if connect_active:
            name += "_a"
        if connect_poly:
            name += "_p"
        if num_contacts:
            name += "_c{}".format(num_contacts)
        # replace periods with underscore for newer spice compatibility
        name = name.replace('.', '_')
        debug.info(3, "creating ptx {0}".format(name))
        design.design.__init__(self, name)

        self.tx_type = tx_type
        self.mults = mults
        self.tx_width = width
        self.connect_active = connect_active
        self.connect_poly = connect_poly
        self.num_contacts = num_contacts

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
            body_dir = 'GROUND'
        else:
            # Assumed that the check for either pmos or nmos is done elsewhere.
            body_dir = 'POWER'
        dir_list = ['INOUT', 'INPUT', 'INOUT', body_dir]
        self.add_pin_list(pin_list, dir_list)
        
        # self.spice.append("\n.SUBCKT {0} {1}".format(self.name,
        #                                              " ".join(self.pins)))
        # Just make a guess since these will actually
        # be decided in the layout later.
        area_sd = 2.5 * self.poly_width * self.tx_width
        perimeter_sd = 2 * self.poly_width + 2 * self.tx_width
        main_str = "M{{0}} {{1}} {0} m={1} w={2}u l={3}u ".format(spice[self.tx_type],
                                                                  self.mults,
                                                                  self.tx_width,
                                                                  drc("minwidth_poly"))
        area_str = "pd={0:.2f}u ps={0:.2f}u as={1:.2f}p ad={1:.2f}p".format(perimeter_sd,
                                                                            area_sd)
        self.spice_device = main_str + area_str
        self.spice.append("\n* ptx " + self.spice_device)
        # self.spice.append(".ENDS {0}".format(self.name))

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

        # The contacted poly pitch
        self.poly_pitch = max(2 * self.contact_to_gate + self.contact_width + self.poly_width,
                              self.poly_space)

        # The contacted poly pitch
        self.contact_spacing = 2 * self.contact_to_gate + \
                               self.contact_width + self.poly_width

        # This is measured because of asymmetric enclosure rules
        active_enclose_contact = 0.5*(self.active_contact.width - self.contact_width)
        
        # This is the distance from the side of
        # poly gate to the contacted end of active
        # (i.e. the "outside" contacted diffusion sizes)
        self.end_to_poly = self.active_contact.width - active_enclose_contact + \
                           self.contact_to_gate
        
        # Active width is determined by enclosure on both ends and contacted pitch,
        # at least one poly and n-1 poly pitches
        self.active_width = 2 * self.end_to_poly + self.poly_width + \
                                 (self.mults - 1) * self.poly_pitch

        # Active height is just the transistor width
        self.active_height = self.tx_width

        # Poly height must include poly extension over active
        self.poly_height = self.tx_width + 2 * self.poly_extend_active
        
        # The active offset is due to the well extension
        if "pwell" in layer:
            pwell_enclose_active = drc("pwell_enclose_active")
        else:
            pwell_enclose_active = 0
        if "nwell" in layer:
            nwell_enclose_active = drc("nwell_enclose_active")
        else:
            nwell_enclose_active = 0
        # Use the max of either so that the poly gates will align properly
        well_enclose_active = max(pwell_enclose_active,
                                  nwell_enclose_active)
        self.active_offset = vector([well_enclose_active] * 2)

        # Well enclosure of active, ensure minwidth as well
        well_name = "{}well".format(self.well_type)
        if well_name in layer:
            well_width_rule = drc("minwidth_" + well_name)
            well_enclose_active = drc(well_name + "_enclose_active")
            self.well_width = max(self.active_width + 2 * well_enclose_active,
                                  well_width_rule)
            self.well_height = max(self.active_height + 2 * well_enclose_active,
                                   well_width_rule)
            # We are going to shift the 0,0, so include that in the width and height
            self.height = self.well_height - self.active_offset.y
            self.width = self.well_width - self.active_offset.x
        else:
            # The well is not included in the height and width
            self.height = self.poly_height
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

    def connect_fingered_active(self, drain_positions, source_positions):
        """
        Connect each contact  up/down to a source or drain pin
        """
        
        # This is the distance that we must route up or down from the center
        # of the contacts to avoid DRC violations to the other contacts
        pin_offset = vector(0,
                            0.5 * self.active_contact.second_layer_height + self.m1_space + 0.5 * self.m1_width)
        # This is the width of a m1 extend the ends of the pin
        end_offset = vector(self.m1_width / 2.0, 0)

        # drains always go to the MIDDLE of the cell,
        # so top of NMOS, bottom of PMOS
        # so reverse the directions for NMOS compared to PMOS.
        if self.tx_type == "pmos":
            drain_dir = -1
            source_dir = 1
        else:
            drain_dir = 1
            source_dir = -1
            
        if len(source_positions) > 1:
            source_offset = pin_offset.scale(source_dir, source_dir)
            # remove the individual connections
            self.remove_layout_pin("S")
            # Add each vertical segment
            for a in source_positions:
                self.add_path(("m1"),
                              [a, a + pin_offset.scale(source_dir,
                                                       source_dir)])
            # Add a single horizontal pin
            self.add_layout_pin_segment_center(text="S",
                                               layer="m1",
                                               start=source_positions[0] + source_offset - end_offset,
                                               end=source_positions[-1] + source_offset + end_offset)

        if len(drain_positions)>1:
            drain_offset = pin_offset.scale(drain_dir,drain_dir)
            self.remove_layout_pin("D") # remove the individual connections
            # Add each vertical segment
            for a in drain_positions:
                self.add_path(("m1"), [a,a+drain_offset])
            # Add a single horizontal pin
            self.add_layout_pin_segment_center(text="D",
                                               layer="m1",
                                               start=drain_positions[0] + drain_offset - end_offset,
                                               end=drain_positions[-1] + drain_offset + end_offset)
            
    def add_poly(self):
        """
        Add the poly gates(s) and (optionally) connect them.
        """
        # poly is one contacted spacing from the end and down an extension
        poly_offset = self.active_offset \
                      + vector(self.poly_width, self.poly_height).scale(0.5, 0.5) \
                      + vector(self.end_to_poly, -self.poly_extend_active)

        # poly_positions are the bottom center of the poly gates
        poly_positions = []

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
            self.add_layout_pin_rect_center(text="G",
                                            layer="poly",
                                            offset=poly_offset,
                                            height=self.poly_height,
                                            width=self.poly_width)
            poly_positions.append(poly_offset)
            poly_offset = poly_offset + vector(self.poly_pitch,0)

        if self.connect_poly:
            self.connect_fingered_poly(poly_positions)
            
    def add_active(self):
        """
        Adding the diffusion (active region = diffusion region)
        """
        self.add_rect(layer="active",
                      offset=self.active_offset,
                      width=self.active_width,
                      height=self.active_height)
        # If the implant must enclose the active, shift offset
        # and increase width/height
        enclose_width = self.implant_enclose_active
        enclose_offset = [enclose_width] * 2
        self.add_rect(layer="{}implant".format(self.implant_type),
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

        center_pos = self.active_offset + vector(0.5*self.active_width,
                                                 0.5*self.active_height)
        well_ll = center_pos - vector(0.5*self.well_width,
                                      0.5*self.well_height)
        if well_name in layer:
            self.add_rect(layer=well_name,
                          offset=well_ll,
                          width=self.well_width,
                          height=self.well_height)
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

    def get_contact_positions(self):
        """
        Create a list of the centers of drain and source contact positions.
        """
        # The first one will always be a source
        source_positions = [self.contact_offset]
        drain_positions = []
        # It is important that these are from left to right,
        # so that the pins are in the right
        # order for the accessors.
        for i in range(self.mults):
            if i%2:
                # It's a source... so offset from previous drain.
                source_positions.append(drain_positions[-1] + vector(self.contact_spacing, 0))
            else:
                # It's a drain... so offset from previous source.
                drain_positions.append(source_positions[-1] + vector(self.contact_spacing, 0))

        return [source_positions,drain_positions]
        
    def add_active_contacts(self):
        """
        Add the active contacts to the transistor.
        """

        [source_positions,drain_positions] = self.get_contact_positions()

        for pos in source_positions:
            contact=self.add_via_center(layers=self.active_stack,
                                        offset=pos,
                                        size=(1, self.num_contacts),
                                        directions=("V","V"),
                                        implant_type=self.implant_type,
                                        well_type=self.well_type)
            self.add_layout_pin_rect_center(text="S",
                                            layer="m1",
                                            offset=pos,
                                            width=contact.mod.second_layer_width,
                                            height=contact.mod.second_layer_height)

                
        for pos in drain_positions:
            contact=self.add_via_center(layers=self.active_stack,
                                        offset=pos,
                                        size=(1, self.num_contacts),
                                        directions=("V","V"),
                                        implant_type=self.implant_type,
                                        well_type=self.well_type)
            self.add_layout_pin_rect_center(text="D",
                                            layer="m1",
                                            offset=pos,
                                            width=contact.mod.second_layer_width,
                                            height=contact.mod.second_layer_height)
                
        if self.connect_active:
            self.connect_fingered_active(drain_positions, source_positions)

    def get_cin(self):
        """Returns the relative gate cin of the tx"""
        return self.tx_width / drc("minwidth_tx")

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)
        
