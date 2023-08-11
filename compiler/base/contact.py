# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import drc, layer, preferred_directions
from openram.tech import layer as tech_layers
from .hierarchy_design import hierarchy_design
from .vector import vector


class contact(hierarchy_design):
    """
    Object for a contact shape with its conductor enclosures.  Creates
    a contact array minimum active or poly enclosure and metal1
    enclosure.  This class has enclosure on two or four sides of the
    contact.  The direction specifies whether the first and second
    layer have asymmetric extension in the H or V direction.

    The well/implant_type is an option to add a select/implant layer
    enclosing the contact. This is necessary to import layouts into
    Magic which requires the select to be in the same GDS hierarchy as
    the contact.

    """

    def __init__(self, layer_stack, dimensions=(1, 1), directions=None,
                 implant_type=None, well_type=None, name=""):
        # This will ignore the name parameter since
        # we can guarantee a unique name here

        super().__init__(name, name)
        debug.info(4, "create contact object {0}".format(name))

        self.add_comment("layers: {0}".format(layer_stack))
        self.add_comment("dimensions: {0}".format(dimensions))
        if implant_type or well_type:
            self.add_comment("implant type: {}\n".format(implant_type))
            self.add_comment("well_type: {}\n".format(well_type))

        self.is_well_contact = implant_type == well_type

        # If we have a special tap layer, use it
        self.layer_stack = layer_stack
        self.dimensions = dimensions

        # Non-preferred directions
        if directions == "nonpref":
            first_dir = "H" if preferred_directions[layer_stack[0]]=="V" else "V"
            second_dir = "H" if preferred_directions[layer_stack[2]]=="V" else "V"
            self.directions = (first_dir, second_dir)
        # Preferred directions
        elif directions == "pref":
            self.directions = (preferred_directions[layer_stack[0]],
                               preferred_directions[layer_stack[2]])
        # User directions
        elif directions:
            self.directions = directions
        # Preferred directions
        else:
            self.directions = (preferred_directions[layer_stack[0]],
                               preferred_directions[layer_stack[2]])
        self.offset = vector(0, 0)
        self.implant_type = implant_type
        self.well_type = well_type
        self.create_layout()

    def create_layout(self):

        self.setup_layers()
        self.setup_layout_constants()
        self.create_contact_array()
        self.create_first_layer_enclosure()
        self.create_second_layer_enclosure()
        self.create_nitride_cut_enclosure()

        self.height = max(self.first_layer_position.y + self.first_layer_height,
                          self.second_layer_position.y + self.second_layer_height)
        self.width = max(self.first_layer_position.x + self.first_layer_width,
                         self.second_layer_position.x + self.second_layer_width)

        # Do not include the select layer in the height/width
        if self.implant_type and self.well_type:
            self.create_implant_well_enclosures()
        elif self.implant_type or self.well_type:
            debug.error(-1,
                        "Must define both implant and well type or none.")

    def setup_layers(self):
        """ Locally assign the layer names. """

        (first_layer, via_layer, second_layer) = self.layer_stack
        self.first_layer_name = first_layer
        self.second_layer_name = second_layer

        # Contacts will have unique per first layer
        if via_layer in tech_layers:
            self.via_layer_name = via_layer
        elif via_layer == "contact":
            if first_layer in ("active", "poly"):
                self.via_layer_name = first_layer + "_" + via_layer
            elif second_layer in ("active", "poly"):
                self.via_layer_name = second_layer + "_" + via_layer
            else:
                debug.error("Invalid via layer {}".format(via_layer), -1)
        else:
            debug.error("Invalid via layer {}".format(via_layer), -1)

    def setup_layout_constants(self):
        """ Determine the design rules for the enclosure layers """

        self.contact_width = drc("minwidth_{0}". format(self.via_layer_name))
        contact_to_contact = drc("{0}_to_{0}".format(self.via_layer_name))
        self.contact_pitch = self.contact_width + contact_to_contact

        self.contact_array_width = self.contact_width + (self.dimensions[0] - 1) * self.contact_pitch
        self.contact_array_height = self.contact_width + (self.dimensions[1] - 1) * self.contact_pitch

        # DRC rules
        # The extend rule applies to asymmetric enclosures in one direction.
        # The enclosure rule applies to symmetric enclosure component.

        self.first_layer_minwidth = drc("minwidth_{0}".format(self.first_layer_name))
        self.first_layer_enclosure = drc("{0}_enclose_{1}".format(self.first_layer_name, self.via_layer_name))
        # If there's a different rule for active
        # FIXME: Make this more elegant
        if self.is_well_contact and self.first_layer_name == "active" and "tap_extend_contact" in drc.keys():
            self.first_layer_extend = drc("tap_extend_contact")
        else:
            self.first_layer_extend = drc("{0}_extend_{1}".format(self.first_layer_name, self.via_layer_name))

        self.second_layer_minwidth = drc("minwidth_{0}".format(self.second_layer_name))
        self.second_layer_enclosure = drc("{0}_enclose_{1}".format(self.second_layer_name, self.via_layer_name))
        self.second_layer_extend = drc("{0}_extend_{1}".format(self.second_layer_name, self.via_layer_name))

        # In some technologies, the minimum width may be larger
        # than the overlap requirement around the via, so
        # check this for each dimension.
        if self.directions[0] == "V":
            self.first_layer_horizontal_enclosure = max(self.first_layer_enclosure,
                                                        (self.first_layer_minwidth - self.contact_array_width) / 2)
            self.first_layer_vertical_enclosure = max(self.first_layer_extend,
                                                      (self.first_layer_minwidth - self.contact_array_height) / 2)
        elif self.directions[0] == "H":
            self.first_layer_horizontal_enclosure = max(self.first_layer_extend,
                                                        (self.first_layer_minwidth - self.contact_array_width) / 2)
            self.first_layer_vertical_enclosure = max(self.first_layer_enclosure,
                                                      (self.first_layer_minwidth - self.contact_array_height) / 2)
        else:
            debug.error("Invalid first layer direction: ".format(self.directions[0]), -1)

        # In some technologies, the minimum width may be larger
        # than the overlap requirement around the via, so
        # check this for each dimension.
        if self.directions[1] == "V":
            self.second_layer_horizontal_enclosure = max(self.second_layer_enclosure,
                                                         (self.second_layer_minwidth - self.contact_array_width) / 2)
            self.second_layer_vertical_enclosure = max(self.second_layer_extend,
                                                       (self.second_layer_minwidth - self.contact_array_height) / 2)
        elif self.directions[1] == "H":
            self.second_layer_horizontal_enclosure = max(self.second_layer_extend,
                                                         (self.second_layer_minwidth - self.contact_array_height) / 2)
            self.second_layer_vertical_enclosure = max(self.second_layer_enclosure,
                                                       (self.second_layer_minwidth - self.contact_array_width) / 2)
        else:
            debug.error("Invalid secon layer direction: ".format(self.directions[1]), -1)

    def create_contact_array(self):
        """ Create the contact array at the origin"""
        # offset for the via array
        self.via_layer_position = vector(
            max(self.first_layer_horizontal_enclosure,
                self.second_layer_horizontal_enclosure),
            max(self.first_layer_vertical_enclosure,
                self.second_layer_vertical_enclosure))

        for i in range(self.dimensions[1]):
            offset = self.via_layer_position + vector(0,
                                                      self.contact_pitch * i)
            for j in range(self.dimensions[0]):
                self.add_rect(layer=self.via_layer_name,
                              offset=offset,
                              width=self.contact_width,
                              height=self.contact_width)
                offset = offset + vector(self.contact_pitch, 0)

    def create_nitride_cut_enclosure(self):
        """ Special layer that encloses poly contacts in some processes """
        # Check if there is a special poly nitride cut layer
        if "npc" not in tech_layers:
            return

        npc_enclose_poly = drc("npc_enclose_poly")
        npc_enclose_offset = vector(npc_enclose_poly, npc_enclose_poly)
        # Only add for poly layers
        if self.first_layer_name == "poly":
            self.add_rect(layer="npc",
                          offset=self.first_layer_position - npc_enclose_offset,
                          width=self.first_layer_width + 2 * npc_enclose_poly,
                          height=self.first_layer_height + 2 * npc_enclose_poly)
        elif self.second_layer_name == "poly":
            self.add_rect(layer="npc",
                          offset=self.second_layer_position - npc_enclose_offset,
                          width=self.second_layer_width + 2 * npc_enclose_poly,
                          height=self.second_layer_height + 2 * npc_enclose_poly)

    def create_first_layer_enclosure(self):
        # this is if the first and second layers are different
        self.first_layer_position = vector(
            max(self.second_layer_horizontal_enclosure - self.first_layer_horizontal_enclosure, 0),
            max(self.second_layer_vertical_enclosure - self.first_layer_vertical_enclosure, 0))

        self.first_layer_width = max(self.contact_array_width + 2 * self.first_layer_horizontal_enclosure,
                                     self.first_layer_minwidth)
        self.first_layer_height = max(self.contact_array_height + 2 * self.first_layer_vertical_enclosure,
                                      self.first_layer_minwidth)
        if self.is_well_contact and self.first_layer_name == "active" and "tap" in layer:
            first_layer_name = "tap"
        else:
            first_layer_name = self.first_layer_name
        self.add_rect(layer=first_layer_name,
                      offset=self.first_layer_position,
                      width=self.first_layer_width,
                      height=self.first_layer_height)

    def create_second_layer_enclosure(self):
        # this is if the first and second layers are different
        self.second_layer_position = vector(
            max(self.first_layer_horizontal_enclosure - self.second_layer_horizontal_enclosure, 0),
            max(self.first_layer_vertical_enclosure - self.second_layer_vertical_enclosure, 0))

        self.second_layer_width = max(self.contact_array_width + 2 * self.second_layer_horizontal_enclosure,
                                      self.second_layer_minwidth)
        self.second_layer_height = max(self.contact_array_height + 2 * self.second_layer_vertical_enclosure,
                                       self.second_layer_minwidth)
        self.add_rect(layer=self.second_layer_name,
                      offset=self.second_layer_position,
                      width=self.second_layer_width,
                      height=self.second_layer_height)

    def create_implant_well_enclosures(self):
        implant_position = self.first_layer_position - [drc("implant_enclose_active")] * 2
        implant_width = self.first_layer_width + 2 * drc("implant_enclose_active")
        implant_height = self.first_layer_height + 2 * drc("implant_enclose_active")
        self.add_rect(layer="{}implant".format(self.implant_type),
                      offset=implant_position,
                      width=implant_width,
                      height=implant_height)

        # Optionally implant well if layer exists
        well_layer = "{}well".format(self.well_type)
        if well_layer in tech_layers:
            well_width_rule = drc("minwidth_" + well_layer)
            self.well_enclose_active = drc(well_layer + "_enclose_active")
            self.well_width = max(self.first_layer_width + 2 * self.well_enclose_active,
                                  well_width_rule)
            self.well_height = max(self.first_layer_height + 2 * self.well_enclose_active,
                                   well_width_rule)
            center_pos = vector(0.5*self.width, 0.5*self.height)
            well_position = center_pos - vector(0.5*self.well_width, 0.5*self.well_height)
            self.add_rect(layer=well_layer,
                          offset=well_position,
                          width=self.well_width,
                          height=self.well_height)

    def analytical_power(self, corner, load):
        """ Get total power of a module  """
        return self.return_power()


