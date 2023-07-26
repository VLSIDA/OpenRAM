# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
import os
import re
from math import sqrt
from openram import debug
from openram.gdsMill import gdsMill
from openram import tech
from openram.tech import drc, GDS
from openram.tech import layer as tech_layer
from openram.tech import layer_indices as tech_layer_indices
from openram.tech import preferred_directions
from openram.tech import layer_stacks as tech_layer_stacks
from openram.tech import active_stack as tech_active_stack
from openram.sram_factory import factory
from openram import OPTS
from .vector import vector
from .pin_layout import pin_layout
from .utils import round_to_grid
from . import geometry

try:
    from openram.tech import special_purposes
except ImportError:
    special_purposes = {}


class layout():
    """
    Class consisting of a set of objs and instances for a module
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    """

    def __init__(self, name, cell_name):
        # This gets set in both spice and layout so either can be called first.
        self.name = name
        self.cell_name = cell_name

        self.gds_file = OPTS.openram_tech + "gds_lib/" + cell_name + ".gds"
        self.is_library_cell = os.path.isfile(self.gds_file)

        self.width = None
        self.height = None
        self.bounding_box = None # The rectangle shape
        self.bbox = None # The ll, ur coords
        # Holds module/cell layout instances
        self.insts = []
        # Set of names to check for duplicates
        self.inst_names = set()
        # Holds all other objects (labels, geometries, etc)
        self.objs = []
        # This is a mapping of internal pin names to cell pin names
        # If the key is not found, the internal pin names is assumed
        self.pin_names = {}
        # Holds name->pin_layout map for all pins
        self.pin_map = {}
        # List of modules we have already visited
        self.visited = []

        self.gds_read()

        if "contact" not in self.name:
            if not hasattr(layout, "_drc_constants"):
                layout._drc_constants = True
                layout.setup_drc_constants()
                layout.setup_contacts()
                layout.setup_layer_constants()


    @classmethod
    def setup_drc_constants(layout):
        """
        These are some DRC constants used in many places
        in the compiler.
        """

        # Make some local rules for convenience
        for rule in drc.keys():
            # Single layer width rules
            match = re.search(r"minwidth_(.*)", rule)
            if match:
                if match.group(1) == "active_contact":
                    setattr(layout, "contact_width", drc(match.group(0)))
                else:
                    setattr(layout, match.group(1) + "_width", drc(match.group(0)))

            # Single layer area rules
            match = re.search(r"minarea_(.*)", rule)
            if match:
                setattr(layout, match.group(0), drc(match.group(0)))

            # Single layer spacing rules
            match = re.search(r"(.*)_to_(.*)", rule)
            if match and match.group(1) == match.group(2):
                setattr(layout, match.group(1) + "_space", drc(match.group(0)))
            elif match and match.group(1) != match.group(2):
                if match.group(2) == "poly_active":
                    setattr(layout, match.group(1) + "_to_contact",
                            drc(match.group(0)))
                else:
                    setattr(layout, match.group(0), drc(match.group(0)))

            match = re.search(r"(.*)_enclose_(.*)", rule)
            if match:
                setattr(layout, match.group(0), drc(match.group(0)))

            match = re.search(r"(.*)_extend_(.*)", rule)
            if match:
                setattr(layout, match.group(0), drc(match.group(0)))

        # Create the maximum well extend active that gets used
        # by cells to extend the wells for interaction with other cells
        layout.well_extend_active = 0
        if "nwell" in tech_layer:
            layout.well_extend_active = max(layout.well_extend_active, layout.nwell_extend_active)
        if "pwell" in tech_layer:
            layout.well_extend_active = max(layout.well_extend_active, layout.pwell_extend_active)

        # The active offset is due to the well extension
        if "pwell" in tech_layer:
            layout.pwell_enclose_active = drc("pwell_enclose_active")
        else:
            layout.pwell_enclose_active = 0
        if "nwell" in tech_layer:
            layout.nwell_enclose_active = drc("nwell_enclose_active")
        else:
            layout.nwell_enclose_active = 0
        # Use the max of either so that the poly gates will align properly
        layout.well_enclose_active = max(layout.pwell_enclose_active,
                                       layout.nwell_enclose_active,
                                       layout.active_space)

        # These are for debugging previous manual rules
        level=99
        debug.info(level, "poly_width".format(layout.poly_width))
        debug.info(level, "poly_space".format(layout.poly_space))
        debug.info(level, "m1_width".format(layout.m1_width))
        debug.info(level, "m1_space".format(layout.m1_space))
        debug.info(level, "m2_width".format(layout.m2_width))
        debug.info(level, "m2_space".format(layout.m2_space))
        debug.info(level, "m3_width".format(layout.m3_width))
        debug.info(level, "m3_space".format(layout.m3_space))
        debug.info(level, "m4_width".format(layout.m4_width))
        debug.info(level, "m4_space".format(layout.m4_space))
        debug.info(level, "active_width".format(layout.active_width))
        debug.info(level, "active_space".format(layout.active_space))
        debug.info(level, "contact_width".format(layout.contact_width))
        debug.info(level, "poly_to_active".format(layout.poly_to_active))
        debug.info(level, "poly_extend_active".format(layout.poly_extend_active))
        debug.info(level, "poly_to_contact".format(layout.poly_to_contact))
        debug.info(level, "active_contact_to_gate".format(layout.active_contact_to_gate))
        debug.info(level, "poly_contact_to_gate".format(layout.poly_contact_to_gate))
        debug.info(level, "well_enclose_active".format(layout.well_enclose_active))
        debug.info(level, "implant_enclose_active".format(layout.implant_enclose_active))
        debug.info(level, "implant_space".format(layout.implant_space))

    @classmethod
    def setup_layer_constants(layout):
        """
        These are some layer constants used
        in many places in the compiler.
        """
        try:
            from openram.tech import power_grid
            layout.pwr_grid_layers = [power_grid[0], power_grid[2]]
        except ImportError:
            layout.pwr_grid_layers = ["m3", "m4"]

        for layer_id in tech_layer_indices:
            key = "{}_stack".format(layer_id)

            # Set the stack as a local helper
            try:
                layer_stack = getattr(tech, key)
                setattr(layout, key, layer_stack)
            except AttributeError:
                pass

            # Skip computing the pitch for non-routing layers
            if layer_id in ["active", "nwell"]:
                continue

            # Add the pitch
            setattr(layout,
                    "{}_pitch".format(layer_id),
                    layout.compute_pitch(layer_id, True))

            # Add the non-preferrd pitch (which has vias in the "wrong" way)
            setattr(layout,
                    "{}_nonpref_pitch".format(layer_id),
                    layout.compute_pitch(layer_id, False))

        level=99
        for name in tech_layer_indices:
            if name == "active":
                continue
            try:
                debug.info(level, "{0} width {1} space {2}".format(name,
                                                       getattr(layout, "{}_width".format(name)),
                                                       getattr(layout, "{}_space".format(name))))

                debug.info(level, "pitch {0} nonpref {1}".format(getattr(layout, "{}_pitch".format(name)),
                                                     getattr(layout, "{}_nonpref_pitch".format(name))))
            except AttributeError:
                pass

    @staticmethod
    def compute_pitch(layer, preferred=True):
        """
        This is the preferred direction pitch
        i.e. we take the minimum or maximum contact dimension
        """
        # Find the layer stacks this is used in
        pitches = []
        for stack in tech_layer_stacks:
            # Compute the pitch with both vias above and below (if they exist)
            if stack[0] == layer:
                pitches.append(layout.compute_layer_pitch(stack, preferred))
            if stack[2] == layer:
                pitches.append(layout.compute_layer_pitch(stack[::-1], True))

        return max(pitches)

    @staticmethod
    def get_preferred_direction(layer):
        return preferred_directions[layer]

    @staticmethod
    def compute_layer_pitch(layer_stack, preferred):

        (layer1, via, layer2) = layer_stack
        try:
            if layer1 == "poly" or layer1 == "active":
                contact1 = getattr(layout, layer1 + "_contact")
            else:
                contact1 = getattr(layout, layer1 + "_via")
        except AttributeError:
            contact1 = getattr(layout, layer2 + "_via")

        if preferred:
            if preferred_directions[layer1] == "V":
                contact_width = contact1.first_layer_width
            else:
                contact_width = contact1.first_layer_height
        else:
            if preferred_directions[layer1] == "V":
                contact_width = contact1.first_layer_height
            else:
                contact_width = contact1.first_layer_width
        layer_space = getattr(layout, layer1 + "_space")

        #print(layer_stack)
        #print(contact1)
        pitch = contact_width + layer_space

        return round_to_grid(pitch)


    @classmethod
    def setup_contacts(layout):
        # Set up a static for each layer to be used for measurements
        # unless we are a contact class!

        for layer_stack in tech_layer_stacks:
            (layer1, via, layer2) = layer_stack
            cont = factory.create(module_type="contact",
                                  layer_stack=layer_stack)
            module = sys.modules[__name__]
            # Also create a contact that is just the first layer
            if layer1 == "poly" or layer1 == "active":
                setattr(layout, layer1 + "_contact", cont)
            else:
                setattr(layout, layer1 + "_via", cont)

        # Set up a static for each well contact for measurements
        if "nwell" in tech_layer:
            cont = factory.create(module_type="contact",
                                  layer_stack=tech_active_stack,
                                  implant_type="n",
                                  well_type="n")
            module = sys.modules[__name__]
            setattr(layout, "nwell_contact", cont)

        if "pwell" in tech_layer:
            cont = factory.create(module_type="contact",
                                  layer_stack=tech_active_stack,
                                  implant_type="p",
                                  well_type="p")
            module = sys.modules[__name__]
            setattr(layout, "pwell_contact", cont)



    ############################################################
    # GDS layout
    ############################################################
    def offset_all_coordinates(self, offset=None):
        """
        This function is called after everything is placed to
        shift the origin in the lowest left corner
        """
        if not offset:
            offset = vector(0, 0)
        ll = self.find_lowest_coords()
        real_offset = ll + offset
        self.translate_all(real_offset)
        return real_offset

    def offset_x_coordinates(self, offset=None):
        """
        This function is called after everything is placed to
        shift the origin to the furthest left point.
        Y offset is unchanged.
        """
        if not offset:
            offset = vector(0, 0)
        ll = self.find_lowest_coords()
        real_offset = ll.scale(1, 0) + offset
        self.translate_all(real_offset)
        return real_offset

    def get_gate_offset(self, x_offset, height, inv_num):
        """
        Gets the base offset and y orientation of stacked rows of gates
        assuming a minwidth metal1 vdd/gnd rail. Input is which gate
        in the stack from 0..n
        """

        if (inv_num % 2 == 0):
            base_offset = vector(x_offset, inv_num * height)
            y_dir = 1
        else:
            # we lose a rail after every 2 gates
            base_offset = vector(x_offset,
                                 (inv_num + 1) * height - \
                                 (inv_num % 2) * drc["minwidth_m1"])
            y_dir = -1

        return (base_offset, y_dir)

    def find_lowest_coords(self):
        """
        Finds the lowest set of 2d cartesian coordinates within
        this layout
        """
        lowestx = lowesty = sys.maxsize

        if len(self.objs) > 0:
            lowestx = min(min(obj.lx() for obj in self.objs if obj.name != "label"), lowestx)
            lowesty = min(min(obj.by() for obj in self.objs if obj.name != "label"), lowesty)

        if len(self.insts) > 0:
            lowestx = min(min(inst.lx() for inst in self.insts), lowestx)
            lowesty = min(min(inst.by() for inst in self.insts), lowesty)

        if len(self.pin_map) > 0:
            for pin_set in self.pin_map.values():
                if len(pin_set) == 0:
                    continue
                lowestx = min(min(pin.lx() for pin in pin_set), lowestx)
                lowesty = min(min(pin.by() for pin in pin_set), lowesty)

        return vector(lowestx, lowesty)

    def find_highest_coords(self):
        """
        Finds the highest set of 2d cartesian coordinates within
        this layout
        """
        highestx = highesty = -sys.maxsize - 1

        if len(self.objs) > 0:
            highestx = max(max(obj.rx() for obj in self.objs if obj.name != "label"), highestx)
            highesty = max(max(obj.uy() for obj in self.objs if obj.name != "label"), highesty)

        if len(self.insts) > 0:
            highestx = max(max(inst.rx() for inst in self.insts), highestx)
            highesty = max(max(inst.uy() for inst in self.insts), highesty)

        if len(self.pin_map) > 0:
            for pin_set in self.pin_map.values():
                if len(pin_set) == 0:
                    continue
                highestx = max(max(pin.rx() for pin in pin_set), highestx)
                highesty = max(max(pin.uy() for pin in pin_set), highesty)

        return vector(highestx, highesty)

    def find_highest_layer_coords(self, layer):
        """
        Finds the highest set of 2d cartesian coordinates within
        this layout on a layer
        """
        # Only consider the layer not the purpose for now
        layerNumber = tech_layer[layer][0]
        try:
            highestx = max(obj.rx() for obj in self.objs if obj.layerNumber == layerNumber)
        except ValueError:
            highestx =0
        try:
            highesty = max(obj.uy() for obj in self.objs if obj.layerNumber == layerNumber)
        except ValueError:
            highesty = 0

        for inst in self.insts:
            # This really should be rotated/mirrored etc...
            subcoord = inst.mod.find_highest_layer_coords(layer) + inst.offset
            highestx = max(highestx, subcoord.x)
            highesty = max(highesty, subcoord.y)

        return vector(highestx, highesty)

    def find_lowest_layer_coords(self, layer):
        """
        Finds the highest set of 2d cartesian coordinates within
        this layout on a layer
        """
        # Only consider the layer not the purpose for now
        layerNumber = tech_layer[layer][0]
        try:
            lowestx = min(obj.lx() for obj in self.objs if obj.layerNumber == layerNumber)
        except ValueError:
            lowestx = 0
        try:
            lowesty = min(obj.by() for obj in self.objs if obj.layerNumber == layerNumber)
        except ValueError:
            lowesty = 0

        for inst in self.insts:
            # This really should be rotated/mirrored etc...
            subcoord = inst.mod.find_lowest_layer_coords(layer) + inst.offset
            lowestx = min(lowestx, subcoord.x)
            lowesty = min(lowesty, subcoord.y)

        return vector(lowestx, lowesty)

    def translate_all(self, offset):
        """
        Translates all objects, instances, and pins by the given (x,y) offset
        """
        for obj in self.objs:
            obj.offset = vector(obj.offset - offset)
        for inst in self.insts:
            inst.offset = vector(inst.offset - offset)
            # The instances have a precomputed boundary that we need to update.
            if inst.__class__.__name__ == "instance":
                inst.compute_boundary(inst.offset, inst.mirror, inst.rotate)
        for pin_name in self.pin_map.keys():
            # All the pins are absolute coordinates that need to be updated.
            pin_list = self.pin_map[pin_name]
            for pin in pin_list:
                pin.rect = [pin.ll() - offset, pin.ur() - offset]

    def add_inst(self, name, mod, offset=[0, 0], mirror="R0", rotate=0):
        """ Adds an instance of a mod to this module """
        # Contacts are not really instances, so skip them
        if "contact" not in mod.name:
            # Check that the instance name is unique
            debug.check(name not in self.inst_names, "Duplicate named instance in {0}: {1}".format(self.cell_name, name))

        self.mods.add(mod)
        self.inst_names.add(name)
        self.insts.append(geometry.instance(name, mod, offset, mirror, rotate))
        debug.info(3, "adding instance {}".format(self.insts[-1]))
        # This is commented out for runtime reasons
        # debug.info(4, "instance list: " + ",".join(x.name for x in self.insts))
        return self.insts[-1]

    def get_inst(self, name):
        """ Retrieve an instance by name """
        for inst in self.insts:
            if inst.name == name:
                return inst
        return None

    def add_flat_inst(self, name, mod, offset=[0, 0]):
        """ Copies all of the items in instance into this module """
        for item in mod.objs:
            item.offset += offset
            self.objs.append(item)
        for item in mod.insts:
            item.offset += offset
            self.insts.append(item)
            debug.check(len(item.mod.pins) == 0, "Cannot add flat instance with subinstances.")
            self.connect_inst([])
        debug.info(3, "adding flat instance {}".format(name))
        return None

    def add_rect(self, layer, offset, width=None, height=None):
        """
        Adds a rectangle on a given layer,offset with width and height
        """
        if not width:
            width = drc["minwidth_{}".format(layer)]
        if not height:
            height = drc["minwidth_{}".format(layer)]
        lpp = tech_layer[layer]
        self.objs.append(geometry.rectangle(lpp,
                                            offset,
                                            width,
                                            height))
        return self.objs[-1]

    def add_rect_center(self, layer, offset, width=None, height=None):
        """
        Adds a rectangle on a given layer at the center
        point with width and height
        """
        if not width:
            width = drc["minwidth_{}".format(layer)]
        if not height:
            height = drc["minwidth_{}".format(layer)]
        lpp = tech_layer[layer]
        corrected_offset = offset - vector(0.5 * width, 0.5 * height)
        self.objs.append(geometry.rectangle(lpp,
                                            corrected_offset,
                                            width,
                                            height))
        return self.objs[-1]

    def add_segment_center(self, layer, start, end, width=None):
        """
        Add a min-width rectanglular segment using center
        line on the start to end point
        """
        if not width:
            width = drc["minwidth_{}".format(layer)]

        if start.x != end.x and start.y != end.y:
            debug.error("Nonrectilinear center rect!", -1)
        elif start.x != end.x:
            offset = vector(0, 0.5 * width)
            return self.add_rect(layer,
                                 start - offset,
                                 end.x - start.x,
                                 width)
        else:
            offset = vector(0.5 * width, 0)
            return self.add_rect(layer,
                                 start - offset,
                                 width,
                                 end.y - start.y)

    def get_tx_insts(self, tx_type=None):
        """
        Return a list of the instances of given tx type.
        """
        tx_list = []
        for i in self.insts:
            try:
                if tx_type and i.mod.tx_type == tx_type:
                    tx_list.append(i)
                elif not tx_type:
                    if i.mod.tx_type == "nmos" or i.mod.tx_type == "pmos":
                        tx_list.append(i)
            except AttributeError:
                pass

        return tx_list

    def get_pin(self, text):
        """
        Return the pin or list of pins
        """
        name = self.get_pin_name(text)

        try:
            if len(self.pin_map[name]) > 1:
                debug.error("Should use a pin iterator since more than one pin {}".format(text), -1)
            # If we have one pin, return it and not the list.
            # Otherwise, should use get_pins()
            any_pin = next(iter(self.pin_map[name]))
            return any_pin
        except Exception:
            self.gds_write("missing_pin.gds")
            debug.error("No pin found with name {0} on {1}. Saved as missing_pin.gds.".format(name, self.cell_name), -1)

    def get_pins(self, text):
        """
        Return a pin list (instead of a single pin)
        """
        name = self.get_pin_name(text)

        if name in self.pin_map.keys():
            return self.pin_map[name]
        else:
            return set()

    def add_pin_names(self, pin_dict):
        """
        Create a mapping from internal pin names to external pin names.
        """
        self.pin_names = pin_dict

        self.original_pin_names = {y: x for (x, y) in self.pin_names.items()}

    def get_pin_name(self, text):
        """ Return the custom cell pin name """

        if text in self.pin_names:
            return self.pin_names[text]
        else:
            return text

    def get_original_pin_names(self):
        """ Return the internal cell pin name """

        # This uses the hierarchy_spice pins (in order)
        return [self.get_original_pin_name(x) for x in self.pins]

    def get_original_pin_name(self, text):
        """ Return the internal cell pin names in custom port order """
        if text in self.original_pin_names:
            return self.original_pin_names[text]
        else:
            return text

    def get_pin_names(self):
        """
        Return a pin list of all pins
        """
        return list(self.pins)

    def copy_layout_pin(self, instance, pin_name, new_name="", relative_offset=vector(0, 0)):
        """
        Create a copied version of the layout pin at the current level.
        You can optionally rename the pin to a new name.
        You can optionally add an offset vector by which to move the pin.
        """
        pins = instance.get_pins(pin_name)

        if len(pins) == 0:
            debug.warning("Could not find pin {0} on {1}".format(pin_name, instance.mod.name))

        for pin in pins:
            if new_name == "":
                new_name = pin_name
            self.add_layout_pin(new_name,
                                pin.layer,
                                pin.ll() + relative_offset,
                                pin.width(),
                                pin.height())


    def connect_row_locs(self, from_layer, to_layer, locs, name=None, full=False):
        """
        Connects left/right rows that are aligned on the given layer.
        """
        bins = {}
        for loc in locs:
                y = pin.y
                try:
                    bins[y].append(loc)
                except KeyError:
                    bins[y] = [loc]

        for y, v in bins.items():
            # Not enough to route a pin, so just copy them
            if len(v) < 2:
                continue

            if full:
                left_x = 0
                right_x = self.width
            else:
                left_x = min([loc.x for loc in v])
                right_x = max([loc.x for loc in v])

            left_pos = vector(left_x, y)
            right_pos = vector(right_x, y)

            # Make sure to add vias to the new route
            for loc in v:
                self.add_via_stack_center(from_layer=from_layer,
                                          to_layer=to_layer,
                                          offset=loc,
                                          min_area=True)

            if name:
                self.add_layout_pin_segment_center(text=name,
                                                   layer=to_layer,
                                                   start=left_pos,
                                                   end=right_pos)
            else:
                self.add_segment_center(layer=to_layer,
                                        start=left_pos,
                                        end=right_pos)

    def connect_row_pins(self, layer, pins, name=None, full=False, round=False):
        """
        Connects left/right rows that are aligned.
        """
        bins = {}
        for pin in pins:
                y = pin.cy()
                if round:
                    y = round_to_grid(y)
                try:
                    bins[y].append(pin)
                except KeyError:
                    bins[y] = [pin]

        for y, v in bins.items():
            # Not enough to route a pin, so just copy them
            if len(v) < 2:
                continue

            if full:
                left_x = 0
                right_x = self.width
            else:
                left_x = min([pin.lx() for pin in v])
                right_x = max([pin.rx() for pin in v])

            left_pos = vector(left_x, y)
            right_pos = vector(right_x, y)

            # Make sure to add vias to the new route
            for pin in v:
                self.add_via_stack_center(from_layer=pin.layer,
                                          to_layer=layer,
                                          offset=pin.center(),
                                          min_area=True)

            if name:
                self.add_layout_pin_segment_center(text=name,
                                                   layer=layer,
                                                   start=left_pos,
                                                   end=right_pos)
            else:
                self.add_segment_center(layer=layer,
                                        start=left_pos,
                                        end=right_pos)

    def connect_col_locs(self, from_layer, to_layer, locs, name=None, full=False):
        """
        Connects top/bot columns that are aligned.
        """
        bins = {}
        for loc in locs:
                x = loc.x
                try:
                    bins[x].append(loc)
                except KeyError:
                    bins[x] = [loc]

        for x, v in bins.items():
            # Not enough to route a pin, so just copy them
            if len(v) < 2:
                continue

            if full:
                bot_y = 0
                top_y = self.height
            else:
                bot_y = min([loc.y for loc in v])
                top_y = max([loc.y for loc in v])

            top_pos = vector(x, top_y)
            bot_pos = vector(x, bot_y)

            # Make sure to add vias to the new route
            for loc in v:
                self.add_via_stack_center(from_layer=from_layer,
                                          to_layer=to_layer,
                                          offset=loc,
                                          min_area=True)

            if name:
                self.add_layout_pin_segment_center(text=name,
                                                   layer=to_layer,
                                                   start=top_pos,
                                                   end=bot_pos)
            else:
                self.add_segment_center(layer=to_layer,
                                        start=top_pos,
                                        end=bot_pos)


    def connect_col_pins(self, layer, pins, name=None, full=False, round=False, directions="pref"):
        """
        Connects top/bot columns that are aligned.
        """
        bins = {}
        for pin in pins:
                x = pin.cx()
                if round:
                    x = round_to_grid(x)
                try:
                    bins[x].append(pin)
                except KeyError:
                    bins[x] = [pin]

        for x, v in bins.items():
            # Not enough to route a pin, so just copy them
            if len(v) < 2:
                continue

            if full:
                bot_y = 0
                top_y = self.height
            else:
                bot_y = min([pin.by() for pin in v])
                top_y = max([pin.uy() for pin in v])

            top_pos = vector(x, top_y)
            bot_pos = vector(x, bot_y)

            # Make sure to add vias to the new route
            for pin in v:
                self.add_via_stack_center(from_layer=pin.layer,
                                          to_layer=layer,
                                          offset=pin.center(),
                                          min_area=True,
                                          directions=directions)

            if name:
                self.add_layout_pin_segment_center(text=name,
                                                   layer=layer,
                                                   start=top_pos,
                                                   end=bot_pos)
            else:
                self.add_segment_center(layer=layer,
                                        start=top_pos,
                                        end=bot_pos)

    def get_metal_layers(self, from_layer, to_layer):

        from_id = tech_layer_indices[from_layer]
        to_id   = tech_layer_indices[to_layer]

        layer_list = [x for x in tech_layer_indices.keys() if tech_layer_indices[x] >= from_id and tech_layer_indices[x] < to_id]

        return layer_list


    def route_vertical_pins(self, name, insts=None, layer=None, xside="cx", yside="cy", full_width=True):
        """
        Route together all of the pins of a given name that vertically align.
        Uses local_insts if insts not specified.
        Uses center of pin by default, or right or left if specified.
        TODO: Add equally spaced option for IR drop min, right now just 2
        """


        bins = {}
        if not insts:
            insts = self.local_insts

        for inst in insts:
            for pin in inst.get_pins(name):

                x = getattr(pin, xside)()
                try:
                    bins[x].append((inst,pin))
                except KeyError:
                    bins[x] = [(inst,pin)]

        for x, v in bins.items():
            # Not enough to route a pin, so just copy them
            if len(v) < 2:
                debug.warning("Pins don't align well so copying pins instead of connecting with pin.")
                for inst,pin in v:
                    self.add_layout_pin(pin.name,
                                        pin.layer,
                                        pin.ll(),
                                        pin.width(),
                                        pin.height())
                continue

            last_via = None
            pin_layer = None
            for inst,pin in v:
                if layer:
                    pin_layer = layer
                else:
                    pin_layer = self.supply_stack[2]

                y = getattr(pin, yside)()

                last_via = self.add_via_stack_center(from_layer=pin.layer,
                                                     to_layer=pin_layer,
                                                     offset=vector(x, y))

            if last_via:
                via_width=last_via.mod.second_layer_width
                via_height=last_via.mod.second_layer_height
            else:
                via_width=None
                via_height=0

            bot_y = min([pin.by() for (inst,pin) in v])
            top_y = max([pin.uy() for (inst,pin) in v])

            if full_width:
                bot_y = min(0, bot_y)
                top_y = max(self.height, top_y)

            top_pos = vector(x, top_y + 0.5 * via_height)
            bot_pos = vector(x, bot_y - 0.5 * via_height)

#            self.add_layout_pin_rect_ends(name=name,
#                                          layer=pin_layer,
#                                          start=top_pos,
#                                          end=bot_pos,
#                                          width=via_width)
            self.add_layout_pin_segment_center(text=name,
                                               layer=pin_layer,
                                               start=top_pos,
                                               end=bot_pos,
                                               width=via_width)


    def add_layout_pin_rect_ends(self, name, layer, start, end, width=None):

        # This adds pins on the end connected by a segment
        top_rect = self.add_layout_pin_rect_center(text=name,
                                                   layer=layer,
                                                   offset=start)
        bot_rect = self.add_layout_pin_rect_center(text=name,
                                                   layer=layer,
                                                   offset=end)
        # This is made to not overlap with the pin above
        # so that the power router will only select a small pin.
        # Otherwise it adds big blockages over the rails.
        if start.y != end.y:
            self.add_segment_center(layer=layer,
                                    start=bot_rect.uc(),
                                    end=top_rect.bc())
        else:
            self.add_segment_center(layer=layer,
                                    start=bot_rect.rc(),
                                    end=top_rect.lc())

        return (bot_rect, top_rect)

    def route_horizontal_pins(self, name, insts=None, layer=None, xside="cx", yside="cy", full_width=True):
        """
        Route together all of the pins of a given name that horizontally align.
        Uses local_insts if insts not specified.
        Uses center of pin by default, or top or botom if specified.
        TODO: Add equally spaced option for IR drop min, right now just 2
        """


        bins = {}
        if not insts:
            insts = self.local_insts

        for inst in insts:
            for pin in inst.get_pins(name):

                y = getattr(pin, yside)()
                try:
                    bins[y].append((inst,pin))
                except KeyError:
                    bins[y] = [(inst,pin)]

        # Filter the small bins

        for y, v in bins.items():
            if len(v) < 2:
                debug.warning("Pins don't align well so copying pins instead of connecting with pin.")
                for inst,pin in v:
                    self.add_layout_pin(pin.name,
                                        pin.layer,
                                        pin.ll(),
                                        pin.width(),
                                        pin.height())
                continue

            last_via = None
            pin_layer = None
            for inst,pin in v:
                if layer:
                    pin_layer = layer
                else:
                    pin_layer = self.supply_stack[0]

                x = getattr(pin, xside)()

                last_via = self.add_via_stack_center(from_layer=pin.layer,
                                                     to_layer=pin_layer,
                                                     offset=vector(x, y),
                                                     min_area=True)

            if last_via:
                via_height=last_via.mod.second_layer_height
                via_width=last_via.mod.second_layer_width
            else:
                via_height=None
                via_width=0

            left_x = min([pin.lx() for (inst,pin) in v])
            right_x = max([pin.rx() for (inst,pin) in v])

            if full_width:
                left_x = min(0, left_x)
                right_x = max(self.width, right_x)

            left_pos = vector(left_x + 0.5 * via_width, y)
            right_pos = vector(right_x + 0.5 * via_width, y)

#            self.add_layout_pin_rect_ends(name=name,
#                                          layer=pin_layer,
#                                          start=left_pos,
#                                          end=right_pos,
#                                          width=via_height)
            self.add_layout_pin_segment_center(text=name,
                                               layer=pin_layer,
                                               start=left_pos,
                                               end=right_pos,
                                               width=via_height)

    def add_layout_end_pin_segment_center(self, text, layer, start, end):
        """
        Creates a path with two pins on the end that don't overlap.
        """

        start_pin = self.add_layout_pin_rect_center(text=text,
                                                    layer=layer,
                                                    offset=start)
        end_pin = self.add_layout_pin_rect_center(text=text,
                                                  layer=layer,
                                                  offset=end)

        if start.x != end.x and start.y != end.y:
            file_name = "non_rectilinear.gds"
            self.gds_write(file_name)
            debug.error("Cannot have a non-manhatten layout pin: {}".format(file_name), -1)
        elif start.x != end.x:
            self.add_segment_center(layer=layer,
                                    start=start_pin.rc(),
                                    end=end_pin.lc())
        elif start.y != end.y:
            self.add_segment_center(layer=layer,
                                    start=start_pin.uc(),
                                    end=end_pin.bc())
        else:
            debug.error("Cannot have a point pin.", -1)

    def add_layout_pin_segment_center(self, text, layer, start, end, width=None):
        """
        Creates a path like pin with center-line convention
        """
        if start.x != end.x and start.y != end.y:
            file_name = "non_rectilinear.gds"
            self.gds_write(file_name)
            debug.error("Cannot have a non-manhatten layout pin: {}".format(file_name), -1)

        if not width:
            layer_width = drc["minwidth_{}".format(layer)]
        else:
            layer_width = width

        # one of these will be zero
        bbox_width = max(start.x, end.x) - min(start.x, end.x)
        bbox_height = max(start.y, end.y) - min(start.y, end.y)
        ll_offset = vector(min(start.x, end.x), min(start.y, end.y))

        # Shift it down 1/2 a width in the 0 dimension
        if bbox_height == 0:
            ll_offset -= vector(0, 0.5 * layer_width)
        if bbox_width == 0:
            ll_offset -= vector(0.5 * layer_width, 0)

        return self.add_layout_pin(text=text,
                                   layer=layer,
                                   offset=ll_offset,
                                   width=max(bbox_width, layer_width),
                                   height=max(bbox_height, layer_width))

    def add_layout_pin_rect_center(self, text, layer, offset, width=None, height=None):
        """ Creates a path like pin with center-line convention """
        if not width:
            width = drc["minwidth_{0}".format(layer)]
        if not height:
            height = drc["minwidth_{0}".format(layer)]

        ll_offset = offset - vector(0.5 * width, 0.5 * height)

        return self.add_layout_pin(text, layer, ll_offset, width, height)

    def remove_layout_pin(self, text):
        """
        Delete a labeled pin (or all pins of the same name)
        """
        self.pin_map[text] = set()

    def remove_layout_pins(self):
        """
        Delete all the layout pins
        """
        self.pin_map = {}

    def copy_layout_pin_shapes(self, text):
        """
        Copy the shapes of the layout pins as objects.
        """
        for s in self.pin_map[text]:
            self.add_rect(layer=s.layer,
                          offset=s.ll(),
                          width=s.width(),
                          height=s.height())

    def replace_layout_pin(self, text, pin):
        """
        Remove the old pin and replace with a new one
        """
        # Keep the shapes as they were used to connect to the router pins
        self.copy_layout_pin_shapes(text)
        # Remove the shapes as actual pins
        self.remove_layout_pin(text)
        # Add the new pin
        self.add_layout_pin(text=text,
                            layer=pin.layer,
                            offset=pin.ll(),
                            width=pin.width(),
                            height=pin.height())

    def add_layout_pin(self, text, layer, offset, width=None, height=None):
        """
        Create a labeled pin
        """
        if not width:
            width = drc["minwidth_{0}".format(layer)]
        if not height:
            height = drc["minwidth_{0}".format(layer)]

        new_pin = pin_layout(text,
                             [offset, offset + vector(width, height)],
                             layer)

        try:
            # Check if there's a duplicate!
            # and if so, silently ignore it.
            # Rounding errors may result in some duplicates.
            if new_pin not in self.pin_map[text]:
                self.pin_map[text].add(new_pin)
        except KeyError:
            self.pin_map[text] = set()
            self.pin_map[text].add(new_pin)

        return new_pin

    def add_label_pin(self, text, layer, offset, width=None, height=None):
        """
        Create a labeled pin WITHOUT the pin data structure. This is not an
        actual pin but a named net so that we can add a correspondence point
        in LVS.
        """
        if not width:
            width = drc["minwidth_{0}".format(layer)]
        if not height:
            height = drc["minwidth_{0}".format(layer)]
        self.add_rect(layer=layer,
                      offset=offset,
                      width=width,
                      height=height)
        self.add_label(text=text,
                       layer=layer,
                       offset=offset + vector(0.5 * width,
                                              0.5 * height))

    def add_label(self, text, layer, offset=[0, 0], zoom=None):
        """Adds a text label on the given layer,offset, and zoom level"""
        debug.info(5, "add label " + str(text) + " " + layer + " " + str(offset))
        lpp = tech_layer[layer]
        self.objs.append(geometry.label(text, lpp, offset, zoom))
        return self.objs[-1]

    def add_path(self, layer, coordinates, width=None):
        """Connects a routing path on given layer,coordinates,width."""
        debug.info(4, "add path " + str(layer) + " " + str(coordinates))
        from . import wire_path
        # NOTE: (UNTESTED) add_path(...) is currently not used
        # lpp = tech_layer[layer]
        # self.objs.append(geometry.path(lpp, coordinates, width))

        wire_path(obj=self,
                  layer=layer,
                  position_list=coordinates,
                  width=width)

    def add_route(self, layers, coordinates, layer_widths):
        """Connects a routing path on given layer,coordinates,width. The
        layers are the (horizontal, via, vertical). add_wire assumes
        preferred direction routing whereas this includes layers in
        the coordinates.
        """
        from . import route
        debug.info(4, "add route " + str(layers) + " " + str(coordinates))
        # add an instance of our path that breaks down into rectangles and contacts
        route(obj=self,
              layer_stack=layers,
              path=coordinates,
              layer_widths=layer_widths)

    def add_zjog(self, layer, start, end, first_direction="H", var_offset=0.5, fixed_offset=None):
        """
        Add a simple jog at the halfway point.
        If layer is a single value, it is a path.
        If layer is a tuple, it is a wire with preferred directions.
        """

        neg_offset = 1.0 - var_offset
        # vertical first
        if first_direction == "V":
            if fixed_offset:
                mid1 = vector(start.x, fixed_offset)
            else:
                mid1 = vector(start.x, neg_offset * start.y + var_offset * end.y)
            mid2 = vector(end.x, mid1.y)
        # horizontal first
        elif first_direction == "H":
            if fixed_offset:
                mid1 = vector(fixed_offset, start.y)
            else:
                mid1 = vector(neg_offset * start.x + var_offset * end.x, start.y)
            mid2 = vector(mid1, end.y)
        else:
            debug.error("Invalid direction for jog -- must be H or V.")

        if layer in tech_layer_stacks:
            self.add_wire(layer, [start, mid1, mid2, end])
        elif layer in tech_layer:
            self.add_path(layer, [start, mid1, mid2, end])
        else:
            debug.error("Could not find layer {}".format(layer))

    def add_horizontal_zjog_path(self, layer, start, end):
        """ Add a simple jog at the halfway point """

        # horizontal first
        mid1 = vector(0.5 * start.x + 0.5 * end.x, start.y)
        mid2 = vector(mid1, end.y)
        self.add_path(layer, [start, mid1, mid2, end])

    def add_wire(self, layers, coordinates, widen_short_wires=True):
        """Connects a routing path on given layer,coordinates,width.
        The layers are the (horizontal, via, vertical). """
        from . import wire
        # add an instance of our path that breaks down
        # into rectangles and contacts
        wire(obj=self,
             layer_stack=layers,
             position_list=coordinates,
             widen_short_wires=widen_short_wires)

    def add_via(self, layers, offset, size=[1, 1], directions=None, implant_type=None, well_type=None):
        """ Add a three layer via structure. """
        via = factory.create(module_type="contact",
                             layer_stack=layers,
                             dimensions=size,
                             directions=directions,
                             implant_type=implant_type,
                             well_type=well_type)
        inst = self.add_inst(name=via.name,
                             mod=via,
                             offset=offset)
        # We don't model the logical connectivity of wires/paths
        self.connect_inst([])
        return inst

    def add_via_center(self, layers, offset, directions=None, size=[1, 1], implant_type=None, well_type=None):
        """
        Add a three layer via structure by the center coordinate
        accounting for mirroring and rotation.
        """
        via = factory.create(module_type="contact",
                             layer_stack=layers,
                             dimensions=size,
                             directions=directions,
                             implant_type=implant_type,
                             well_type=well_type)
        height = via.height
        width = via.width

        corrected_offset = offset + vector(-0.5 * width,
                                           -0.5 * height)

        inst = self.add_inst(name=via.name,
                             mod=via,
                             offset=corrected_offset)
        # We don't model the logical connectivity of wires/paths
        self.connect_inst([])
        return inst

    def add_via_stack_center(self,
                             offset,
                             from_layer,
                             to_layer,
                             directions=None,
                             size=[1, 1],
                             implant_type=None,
                             well_type=None,
                             min_area=False):
        """
        Punch a stack of vias from a start layer to a target layer by the center.
        """

        if from_layer == to_layer:
            # In the case where we have no vias added, make sure that there is at least
            # a metal enclosure. This helps with center-line path routing.
            self.add_rect_center(layer=from_layer,
                                 offset=offset)
            return None

        intermediate_layers = self.get_metal_layers(from_layer, to_layer)

        via = None
        cur_layer = from_layer
        while cur_layer != to_layer:
            from_id = tech_layer_indices[cur_layer]
            to_id   = tech_layer_indices[to_layer]

            if from_id < to_id: # grow the stack up
                search_id = 0
                next_id = 2
            else: # grow the stack down
                search_id = 2
                next_id = 0

            curr_stack = next(filter(lambda stack: stack[search_id] == cur_layer, tech_layer_stacks), None)

            via = self.add_via_center(layers=curr_stack,
                                      size=size,
                                      offset=offset,
                                      directions=directions,
                                      implant_type=implant_type,
                                      well_type=well_type)

            # Only add the enclosure if we are in an intermediate layer
            # or we are forced to
            if min_area or cur_layer in intermediate_layers:
                self.add_min_area_rect_center(cur_layer,
                                              offset,
                                              via.mod.first_layer_width,
                                              via.mod.first_layer_height)

            cur_layer = curr_stack[next_id]

        return via

    def add_min_area_rect_center(self,
                                 layer,
                                 offset,
                                 width=None,
                                 height=None):
        """
        Add a minimum area retcangle at the given point.
        Either width or height should be fixed.
        """
        min_area = drc("minarea_{}".format(layer))
        if min_area == 0:
            return

        min_width = drc("minwidth_{}".format(layer))

        if preferred_directions[layer] == "V":
            new_height = max(min_area / width, min_width)
            new_width = width
        else:
            new_width = max(min_area / height, min_width)
            new_height = height

        debug.check(min_area <= round_to_grid(new_height*new_width), "Min area violated.")

        self.add_rect_center(layer=layer,
                             offset=offset,
                             width=new_width,
                             height=new_height)

    def add_ptx(self, offset, mirror="R0", rotate=0, width=1, mults=1, tx_type="nmos"):
        """Adds a ptx module to the design."""
        from openram.modules import ptx
        mos = ptx(width=width,
                  mults=mults,
                  tx_type=tx_type)
        inst = self.add_inst(name=mos.name,
                             mod=mos,
                             offset=offset,
                             mirror=mirror,
                             rotate=rotate)
        return inst

    def gds_read(self):
        """Reads a GDSII file in the library and checks if it exists
           Otherwise, start a new layout for dynamic generation."""

        if OPTS.netlist_only:
            self.gds = None
            return

        # open the gds file if it exists or else create a blank layout
        if os.path.isfile(self.gds_file):
            debug.info(3, "opening {}".format(self.gds_file))
            self.gds = gdsMill.VlsiLayout(units=GDS["unit"])
            reader = gdsMill.Gds2reader(self.gds)
            reader.loadFromFile(self.gds_file, special_purposes)
        else:
            debug.info(3, "Creating layout structure {}".format(self.name))
            self.gds = gdsMill.VlsiLayout(name=self.name, units=GDS["unit"])

    def print_gds(self, gds_file=None):
        """Print the gds file (not the vlsi class) to the terminal """
        if not gds_file:
            gds_file = self.gds_file
        debug.info(4, "Printing {}".format(gds_file))
        arrayCellLayout = gdsMill.VlsiLayout(units=GDS["unit"])
        reader = gdsMill.Gds2reader(arrayCellLayout, debugToTerminal=1)
        reader.loadFromFile(gds_file, special_purposes)

    def clear_visited(self):
        """ Recursively clear the visited flag """
        self.visited = []

    def gds_write_file(self, gds_layout):
        """Recursive GDS write function"""
        # Visited means that we already prepared self.gds for this subtree
        if self.name in self.visited:
            return
        for i in self.insts:
            i.gds_write_file(gds_layout)
        for i in self.objs:
            i.gds_write_file(gds_layout)
        for pin_name in self.pin_map.keys():
            for pin in self.pin_map[pin_name]:
                pin.gds_write_file(gds_layout)

        # If it's not a premade cell
        # and we didn't add our own boundary,
        # we should add a boundary just for DRC in some technologies
        if not self.is_library_cell and not self.bounding_box:
            # If there is a boundary layer, and we didn't create one, add one.
            boundary_layers = []
            if "boundary" in tech_layer.keys():
                boundary_layers.append("boundary")
            if "stdc" in tech_layer.keys():
                boundary_layers.append("stdc")
            boundary = [self.find_lowest_coords(),
                        self.find_highest_coords()]
            debug.check(boundary[0] and boundary[1], "No shapes to make a boundary.")

            height = boundary[1][1] - boundary[0][1]
            width = boundary[1][0] - boundary[0][0]

            for boundary_layer in boundary_layers:
                (layer_number, layer_purpose) = tech_layer[boundary_layer]
                gds_layout.addBox(layerNumber=layer_number,
                                  purposeNumber=layer_purpose,
                                  offsetInMicrons=boundary[0],
                                  width=width,
                                  height=height,
                                  center=False)
                debug.info(4, "Adding {0} boundary {1}".format(self.name, boundary))

        self.visited.append(self.name)

    def gds_write(self, gds_name):
        """Write the entire gds of the object to the file."""
        debug.info(3, "Writing to {}".format(gds_name))

        # If we already wrote a GDS, we need to reset and traverse it again in
        # case we made changes.
        if not self.is_library_cell and self.visited:
            debug.info(3, "Creating layout structure {}".format(self.name))
            self.gds = gdsMill.VlsiLayout(name=self.name, units=GDS["unit"])

        writer = gdsMill.Gds2writer(self.gds)
        # MRG: 3/2/18 We don't want to clear the visited flag since
        # this would result in duplicates of all instances being placed in self.gds
        # which may have been previously processed!
        # MRG: 10/4/18 We need to clear if we make changes and write a second GDS!
        self.clear_visited()

        # recursively create all the remaining objects
        self.gds_write_file(self.gds)

        # populates the xyTree data structure for gds
        # self.gds.prepareForWrite()
        writer.writeToFile(gds_name)
        debug.info(3, "Done writing to {}".format(gds_name))

    def get_boundary(self):
        """ Return the lower-left and upper-right coordinates of boundary """
        # This assumes nothing spans outside of the width and height!
        return [vector(0, 0), vector(self.width, self.height)]
        #return [self.find_lowest_coords(), self.find_highest_coords()]

    def get_blockages(self, layer, top_level=False):
        """
        Write all of the obstacles in the current (and children)
        modules to the lef file.
        Do not write the pins since they aren't obstructions.
        """
        if type(layer) == str:
            lpp = tech_layer[layer]
        else:
            lpp = layer

        blockages = []
        for i in self.objs:
            blockages += i.get_blockages(lpp)
        for i in self.insts:
            blockages += i.get_blockages(lpp)
        # Must add pin blockages to non-top cells
        if not top_level:
            blockages += self.get_pin_blockages(lpp)
        return blockages

    def get_pin_blockages(self, lpp):
        """ Return the pin shapes as blockages for non-top-level blocks. """
        # FIXME: We don't have a body contact in ptx, so just ignore it for now
        import copy
        # FIXME: this may not work now that self.pins is a dict as defined in hierarchy_spice
        pin_names = copy.deepcopy(self.pins)
        if self.name.startswith("pmos") or self.name.startswith("nmos"):
            pin_names.remove("B")

        blockages = []
        for pin_name in pin_names:
            pin_list = self.get_pins(pin_name)
            for pin in pin_list:
                if pin.same_lpp(pin.lpp, lpp):
                    blockages += [pin.rect]

        return blockages

    def create_horizontal_pin_bus(self, layer, offset, names, length, pitch=None):
        """ Create a horizontal bus of pins. """
        return self.create_bus(layer,
                               offset,
                               names,
                               length,
                               vertical=False,
                               make_pins=True,
                               pitch=pitch)

    def create_vertical_pin_bus(self, layer, offset, names, length, pitch=None):
        """ Create a horizontal bus of pins. """
        return self.create_bus(layer,
                               offset,
                               names,
                               length,
                               vertical=True,
                               make_pins=True,
                               pitch=pitch)

    def create_vertical_bus(self, layer, offset, names, length, pitch=None):
        """ Create a horizontal bus. """
        return self.create_bus(layer,
                               offset,
                               names,
                               length,
                               vertical=True,
                               make_pins=False,
                               pitch=pitch)

    def create_horizontal_bus(self, layer, offset, names, length, pitch=None):
        """ Create a horizontal bus. """
        return self.create_bus(layer,
                               offset,
                               names,
                               length,
                               vertical=False,
                               make_pins=False,
                               pitch=pitch)

    def create_bus(self, layer, offset, names, length, vertical, make_pins, pitch=None):
        """
        Create a horizontal or vertical bus. It can be either just rectangles, or actual
        layout pins. It returns an map of line center line positions indexed by name.
        The other coordinate is a 0 since the bus provides a range.
        TODO: combine with channel router.
        """

        # half minwidth so we can return the center line offsets
        half_minwidth = 0.5 * drc["minwidth_{}".format(layer)]
        if not pitch:
            pitch = getattr(self, "{}_pitch".format(layer))

        pins = {}
        if vertical:
            for i in range(len(names)):
                line_offset = offset + vector(i * pitch,
                                              0)
                if make_pins:
                    new_pin = self.add_layout_pin(text=names[i],
                                                  layer=layer,
                                                  offset=line_offset,
                                                  height=length)
                else:
                    rect = self.add_rect(layer=layer,
                                         offset=line_offset,
                                         height=length)
                    new_pin = pin_layout(names[i],
                                         [rect.ll(), rect.ur()],
                                         layer)

                pins[names[i]] = new_pin
        else:
            for i in range(len(names)):
                line_offset = offset + vector(0,
                                              i * pitch + half_minwidth)
                if make_pins:
                    new_pin = self.add_layout_pin(text=names[i],
                                                  layer=layer,
                                                  offset=line_offset,
                                                  width=length)
                else:
                    rect = self.add_rect(layer=layer,
                                         offset=line_offset,
                                         width=length)
                    new_pin = pin_layout(names[i],
                                         [rect.ll(), rect.ur()],
                                         layer)

                pins[names[i]] = new_pin

        return pins

    def connect_horizontal_bus(self, mapping, inst, bus_pins,
                               layer_stack=("m1", "via1", "m2")):
        """ Horizontal version of connect_bus. """
        self.connect_bus(mapping, inst, bus_pins, layer_stack, True)

    def connect_vertical_bus(self, mapping, inst, bus_pins,
                             layer_stack=("m1", "via1", "m2")):
        """ Vertical version of connect_bus. """
        self.connect_bus(mapping, inst, bus_pins, layer_stack, False)

    def connect_bus(self, mapping, inst, bus_pins, layer_stack, horizontal):
        """
        Connect a mapping of pin -> name for a bus. This could be
        replaced with a channel router in the future.
        NOTE: This has only really been tested with point-to-point
        connections (not multiple pins on a net).
        """
        (horizontal_layer, via_layer, vertical_layer) = layer_stack
        if horizontal:
            route_layer = vertical_layer
            bus_layer = horizontal_layer
        else:
            route_layer = horizontal_layer
            bus_layer = vertical_layer

        for (pin_name, bus_name) in mapping:
            pin = inst.get_pin(pin_name)
            pin_pos = pin.center()
            bus_pos = bus_pins[bus_name].center()

            if horizontal:
                # up/down then left/right
                mid_pos = vector(pin_pos.x, bus_pos.y)
            else:
                # left/right then up/down
                mid_pos = vector(bus_pos.x, pin_pos.y)

            # Don't widen short wires because pin_pos and mid_pos could be really close
            self.add_wire(layer_stack,
                          [bus_pos, mid_pos, pin_pos],
                          widen_short_wires=False)

            # Connect to the pin on the instances with a via if it is
            # not on the right layer
            if pin.layer != route_layer:
                self.add_via_stack_center(from_layer=pin.layer,
                                          to_layer=route_layer,
                                          offset=pin_pos)
            # FIXME: output pins tend to not be rotate,
            # but supply pins are. Make consistent?

            # We only need a via if they happened to align perfectly
            # so the add_wire didn't add a via
            if (horizontal and bus_pos.y == pin_pos.y) or (not horizontal and bus_pos.x == pin_pos.x):
                self.add_via_stack_center(from_layer=route_layer,
                                          to_layer=bus_layer,
                                          offset=bus_pos)

    def connect_vbus(self, src_pin, dest_pin, hlayer="m3", vlayer="m2"):
        """
        Helper routine to connect an instance to a vertical bus.
        Routes horizontal then vertical L shape.
        """

        if src_pin.cx()<dest_pin.cx():
            in_pos = src_pin.rc()
        else:
            in_pos = src_pin.lc()
        if src_pin.cy() < dest_pin.cy():
            out_pos = dest_pin.bc()
        else:
            out_pos = dest_pin.uc()

        # move horizontal first on layer stack
        mid_pos = vector(out_pos.x, in_pos.y)
        self.add_via_stack_center(from_layer=src_pin.layer,
                                  to_layer=hlayer,
                                  offset=in_pos)
        self.add_path(hlayer, [in_pos, mid_pos])
        self.add_via_stack_center(from_layer=hlayer,
                                  to_layer=vlayer,
                                  offset=mid_pos)
        self.add_path(vlayer, [mid_pos, out_pos])
        self.add_via_stack_center(from_layer=vlayer,
                                  to_layer=dest_pin.layer,
                                  offset=out_pos)

    def connect_hbus(self, src_pin, dest_pin, hlayer="m3", vlayer="m2"):
        """
        Helper routine to connect an instance to a horizontal bus.
        Routes horizontal then vertical L shape.
        """

        if src_pin.cx()<dest_pin.cx():
            in_pos = src_pin.rc()
        else:
            in_pos = src_pin.lc()
        if src_pin.cy() < dest_pin.cy():
            out_pos = dest_pin.lc()
        else:
            out_pos = dest_pin.rc()

        # move horizontal first
        mid_pos = vector(out_pos.x, in_pos.y)
        self.add_via_stack_center(from_layer=src_pin.layer,
                                  to_layer=hlayer,
                                  offset=in_pos)
        self.add_path(hlayer, [in_pos, mid_pos])
        self.add_via_stack_center(from_layer=hlayer,
                                  to_layer=vlayer,
                                  offset=mid_pos)
        self.add_path(vlayer, [mid_pos, out_pos])
        self.add_via_stack_center(from_layer=vlayer,
                                  to_layer=dest_pin.layer,
                                  offset=out_pos)

    def create_vertical_channel_route(self, netlist, offset, layer_stack, directions=None):
        """
        Wrapper to create a vertical channel route
        """
        from .channel_route import channel_route
        cr = channel_route(netlist, offset, layer_stack, directions, vertical=True, parent=self)
        # This causes problem in magic since it sometimes cannot extract connectivity of isntances
        # with no active devices.
        # self.add_inst(cr.name, cr)
        # self.connect_inst([])
        self.add_flat_inst(cr.name, cr)

    def create_horizontal_channel_route(self, netlist, offset, layer_stack, directions=None):
        """
        Wrapper to create a horizontal channel route
        """
        from .channel_route import channel_route
        cr = channel_route(netlist, offset, layer_stack, directions, vertical=False, parent=self)
        # This causes problem in magic since it sometimes cannot extract connectivity of isntances
        # with no active devices.
        # self.add_inst(cr.name, cr)
        # self.connect_inst([])
        self.add_flat_inst(cr.name, cr)

    def add_boundary(self, ll=vector(0, 0), ur=None):
        """ Add boundary for debugging dimensions """
        if OPTS.netlist_only:
            return

        boundary_layers = []
        if "stdc" in tech_layer.keys():
            boundary_layers.append("stdc")
        if "boundary" in tech_layer.keys():
            boundary_layers.append("boundary")
        # Save the last one as self.bounding_box
        for boundary_layer in boundary_layers:
            if not ur:
                self.bounding_box = self.add_rect(layer=boundary_layer,
                                                  offset=ll,
                                                  height=self.height,
                                                  width=self.width)
            else:
                self.bounding_box = self.add_rect(layer=boundary_layer,
                                                  offset=ll,
                                                  height=ur.y - ll.y,
                                                  width=ur.x - ll.x)

        self.bbox = [self.bounding_box.ll(), self.bounding_box.ur()]

    def get_bbox(self, side="all", margin=0):
        """
        Get the bounding box from the GDS
        """
        gds_filename = OPTS.openram_temp + "temp.gds"
        # If didn't specify a gds blockage file, write it out to read the gds
        # This isn't efficient, but easy for now
        # Load the gds file and read in all the shapes
        self.gds_write(gds_filename)
        layout = gdsMill.VlsiLayout(units=GDS["unit"])
        reader = gdsMill.Gds2reader(layout)
        reader.loadFromFile(gds_filename)
        top_name = layout.rootStructureName

        if not self.bbox:
            # The boundary will determine the limits to the size
            # of the routing grid
            boundary = layout.measureBoundary(top_name)
            # These must be un-indexed to get rid of the matrix type
            ll = vector(boundary[0][0], boundary[0][1])
            ur = vector(boundary[1][0], boundary[1][1])
        else:
            ll, ur = self.bbox

        ll_offset = vector(0, 0)
        ur_offset = vector(0, 0)
        if side in ["ring", "top", "all"]:
            ur_offset += vector(0, margin)
        if side in ["ring", "bottom", "all"]:
            ll_offset += vector(0, margin)
        if side in ["ring", "left", "all"]:
            ll_offset += vector(margin, 0)
        if side in ["ring", "right", "all"]:
            ur_offset += vector(margin, 0)
        bbox = (ll - ll_offset, ur + ur_offset)
        size = ur - ll
        debug.info(1, "Size: {0} x {1} with perimeter margin {2}".format(size.x,
                                                                                               size.y,
                                                                                               margin))

        return bbox

    def add_enclosure(self, insts, layer="nwell", extend=0, leftx=None, rightx=None, topy=None, boty=None):
        """
        Add a layer that surrounds the given instances. Useful
        for creating wells, for example. Doesn't check for minimum widths or
        spacings. Extra arg can force a dimension to one side left/right top/bot.
        """

        if leftx != None:
            xmin = leftx
        else:
            xmin = insts[0].lx()
            for inst in insts:
                xmin = min(xmin, inst.lx())
            xmin = xmin - extend
        if boty != None:
            ymin = boty
        else:
            ymin = insts[0].by()
            for inst in insts:
                ymin = min(ymin, inst.by())
            ymin = ymin - extend
        if rightx != None:
            xmax = rightx
        else:
            xmax = insts[0].rx()
            for inst in insts:
                xmax = max(xmax, inst.rx())
            xmax = xmax + extend
        if topy != None:
            ymax = topy
        else:
            ymax = insts[0].uy()
            for inst in insts:
                ymax = max(ymax, inst.uy())
            ymax = ymax + extend

        rect = self.add_rect(layer=layer,
                             offset=vector(xmin, ymin),
                             width=xmax - xmin,
                             height=ymax - ymin)
        return rect

    def copy_power_pins(self, inst, name, add_vias=True, new_name=""):
        """
        This will copy a power pin if it is on the lowest power_grid layer.
        If it is on M1, it will add a power via too.
        """
        pins = inst.get_pins(name)
        for pin in pins:
            if new_name == "":
                new_name = pin.name
            if pin.layer in self.pwr_grid_layers:
                self.add_layout_pin(new_name,
                                    pin.layer,
                                    pin.ll(),
                                    pin.width(),
                                    pin.height())

            elif add_vias:
                self.copy_power_pin(pin, new_name=new_name)

    def add_io_pin(self, instance, pin_name, new_name, start_layer=None, directions=None):
        """
        Add a signle input or output pin up to metal 3.
        """
        pin = instance.get_pin(pin_name)

        if not start_layer:
            start_layer = pin.layer

        # Just use the power pin function for now to save code
        self.add_power_pin(new_name, pin.center(), start_layer=start_layer, directions=directions)

    def add_power_pin(self, name, loc, directions=None, start_layer="m1"):
        # Hack for min area
        if OPTS.tech_name == "sky130":
            min_area = drc["minarea_{}".format(self.pwr_grid_layers[1])]
            width = round_to_grid(sqrt(min_area))
            height = round_to_grid(min_area / width)
        else:
            width = None
            height = None

        pin = None
        if start_layer in self.pwr_grid_layers:
            pin = self.add_layout_pin_rect_center(text=name,
                                                   layer=start_layer,
                                                   offset=loc,
                                                   width=width,
                                                   height=height)
        else:
            via = self.add_via_stack_center(from_layer=start_layer,
                                            to_layer=self.pwr_grid_layers[0],
                                            offset=loc,
                                            directions=directions)

            if not width:
                width = via.width
            if not height:
                height = via.height
            pin = self.add_layout_pin_rect_center(text=name,
                                                  layer=self.pwr_grid_layers[0],
                                                  offset=loc,
                                                  width=width,
                                                  height=height)

        return pin

    def copy_power_pin(self, pin, loc=None, directions=None, new_name=""):
        """
        Add a single power pin from the lowest power_grid layer down to M1 (or li) at
        the given center location. The starting layer is specified to determine
        which vias are needed.
        """

        if new_name == "":
                new_name = pin.name
        if not loc:
            loc = pin.center()

        # Hack for min area
        if OPTS.tech_name == "sky130":
            min_area = drc["minarea_{}".format(self.pwr_grid_layers[1])]
            width = round_to_grid(sqrt(min_area))
            height = round_to_grid(min_area / width)
        else:
            width = None
            height = None

        if pin.layer in self.pwr_grid_layers:
            self.add_layout_pin_rect_center(text=new_name,
                                            layer=pin.layer,
                                            offset=loc,
                                            width=width,
                                            height=height)
        else:
            via = self.add_via_stack_center(from_layer=pin.layer,
                                            to_layer=self.pwr_grid_layers[0],
                                            offset=loc,
                                            directions=directions)

            if not width:
                width = via.width
            if not height:
                height = via.height
            self.add_layout_pin_rect_center(text=new_name,
                                            layer=self.pwr_grid_layers[0],
                                            offset=loc,
                                            width=width,
                                            height=height)

    def add_perimeter_pin(self, name, pin, side, bbox):
        """
        Add a pin along the perimeter side specified by the bbox with
        the given name and layer from the pin starting location.
        """
        (ll, ur) = bbox
        left = ll.x
        bottom = ll.y
        right = ur.x
        top = ur.y

        pin_loc = pin.center()
        if side == "left":
            peri_pin_loc = vector(left, pin_loc.y)
            layer = "m3"
        elif side == "right":
            layer = "m3"
            peri_pin_loc = vector(right, pin_loc.y)
        elif side == "top":
            layer = "m4"
            peri_pin_loc = vector(pin_loc.x, top)
        elif side == "bottom":
            layer = "m4"
            peri_pin_loc = vector(pin_loc.x, bottom)

        self.add_via_stack_center(from_layer=pin.layer,
                                  to_layer=layer,
                                  offset=pin_loc)

        self.add_path(layer,
                      [pin_loc, peri_pin_loc])

        return self.add_layout_pin_rect_center(text=name,
                                               layer=layer,
                                               offset=peri_pin_loc)

    def add_dnwell(self, bbox=None, inflate=1):
        """ Create a dnwell, along with nwell moat at border. """

        if "dnwell" not in tech_layer:
            return

        if not bbox:
            bbox =  [self.find_lowest_coords(),
                     self.find_highest_coords()]

        # Find the corners
        [ll, ur] = bbox

        # Possibly inflate the bbox
        nwell_offset = vector(2 * self.nwell_width, 2 * self.nwell_width)
        ll -= nwell_offset.scale(inflate, inflate)
        ur += nwell_offset.scale(inflate, inflate)

        # Other corners
        ul = vector(ll.x, ur.y)
        lr = vector(ur.x, ll.y)

        # Add the dnwell
        self.add_rect("dnwell",
                      offset=ll,
                      height=ur.y - ll.y,
                      width=ur.x - ll.x)

        # Add the moat
        self.add_path("nwell", [ll, lr, ur, ul, ll - vector(0, 0.5 * self.nwell_width)])

        # Add the taps
        layer_stack = self.active_stack
        tap_spacing = 2
        nwell_offset = vector(self.nwell_width, self.nwell_width)

        # Every nth tap is connected to gnd
        period = 5

        # BOTTOM
        count = 0
        loc = ll + nwell_offset.scale(tap_spacing, 0)
        end_loc = lr - nwell_offset.scale(tap_spacing, 0)
        while loc.x < end_loc.x:
            self.add_via_center(layers=layer_stack,
                                offset=loc,
                                implant_type="n",
                                well_type="n")
            if count % period:
                self.add_via_stack_center(from_layer="li",
                                          to_layer="m1",
                                          offset=loc)
            else:
                self.add_power_pin(name="vdd",
                                   loc=loc,
                                   start_layer="li")
            count += 1
            loc += nwell_offset.scale(tap_spacing, 0)

        # TOP
        count = 0
        loc = ul + nwell_offset.scale(tap_spacing, 0)
        end_loc = ur - nwell_offset.scale(tap_spacing, 0)
        while loc.x < end_loc.x:
            self.add_via_center(layers=layer_stack,
                                offset=loc,
                                implant_type="n",
                                well_type="n")
            if count % period:
                self.add_via_stack_center(from_layer="li",
                                          to_layer="m1",
                                          offset=loc)
            else:
                self.add_power_pin(name="vdd",
                                   loc=loc,
                                   start_layer="li")
            count += 1
            loc += nwell_offset.scale(tap_spacing, 0)

        # LEFT
        count = 0
        loc = ll + nwell_offset.scale(0, tap_spacing)
        end_loc = ul - nwell_offset.scale(0, tap_spacing)
        while loc.y < end_loc.y:
            self.add_via_center(layers=layer_stack,
                                offset=loc,
                                implant_type="n",
                                well_type="n")
            if count % period:
                self.add_via_stack_center(from_layer="li",
                                          to_layer="m2",
                                          offset=loc)
            else:
                self.add_power_pin(name="vdd",
                                   loc=loc,
                                   start_layer="li")
            count += 1
            loc += nwell_offset.scale(0, tap_spacing)

        # RIGHT
        count = 0
        loc = lr + nwell_offset.scale(0, tap_spacing)
        end_loc = ur - nwell_offset.scale(0, tap_spacing)
        while loc.y < end_loc.y:
            self.add_via_center(layers=layer_stack,
                                offset=loc,
                                implant_type="n",
                                well_type="n")
            if count % period:
                self.add_via_stack_center(from_layer="li",
                                          to_layer="m2",
                                          offset=loc)
            else:
                self.add_power_pin(name="vdd",
                                   loc=loc,
                                   start_layer="li")
            count += 1
            loc += nwell_offset.scale(0, tap_spacing)

        # Add the gnd ring
        self.add_ring([ll, ur])

    def add_ring(self, bbox=None, width_mult=8, offset=0):
        """
        Add a ring around the bbox
        """
        # Ring size/space/pitch
        wire_width = self.m2_width * width_mult
        half_width = 0.5 * wire_width
        wire_space = self.m2_space
        wire_pitch = wire_width + wire_space

        # Find the corners
        if not bbox:
            bbox =  [self.find_lowest_coords(),
                     self.find_highest_coords()]

        [ll, ur] = bbox
        ul = vector(ll.x, ur.y)
        lr = vector(ur.x, ll.y)
        ll += vector(-offset * wire_pitch,
                     -offset * wire_pitch)
        lr += vector(offset * wire_pitch,
                     -offset * wire_pitch)
        ur += vector(offset * wire_pitch,
                     offset * wire_pitch)
        ul += vector(-offset * wire_pitch,
                     offset * wire_pitch)

        half_offset = vector(half_width, half_width)
        self.add_path("m1", [ll - half_offset.scale(1, 0), lr + half_offset.scale(1, 0)], width=wire_width)
        self.add_path("m1", [ul - half_offset.scale(1, 0), ur + half_offset.scale(1, 0)], width=wire_width)
        self.add_path("m2", [ll - half_offset.scale(0, 1), ul + half_offset.scale(0, 1)], width=wire_width)
        self.add_path("m2", [lr - half_offset.scale(0, 1), ur + half_offset.scale(0, 1)], width=wire_width)

        # Find the number of vias for this pitch
        supply_vias = 1
        while True:
            c = factory.create(module_type="contact",
                               layer_stack=self.m1_stack,
                               dimensions=(supply_vias, supply_vias))
            if c.second_layer_width < wire_width and c.second_layer_height < wire_width:
                supply_vias += 1
            else:
                supply_vias -= 1
                break

        via_points = [ll, lr, ur, ul]
        for pt in via_points:
            self.add_via_center(layers=self.m1_stack,
                                offset=pt,
                                size=(supply_vias,
                                      supply_vias))

    def add_power_ring(self):
        """
        Create vdd and gnd power rings around an area of the bounding box
        argument. Must have a supply_rail_width and supply_rail_pitch
        defined as a member variable.  Defines local variables of the
        left/right/top/bottom vdd/gnd center offsets for use in other
        modules..
        """

        [ll, ur] = self.bbox

        supply_rail_spacing = self.supply_rail_pitch - self.supply_rail_width
        height = (ur.y - ll.y) + 3 * self.supply_rail_pitch - supply_rail_spacing
        width = (ur.x - ll.x) + 3 * self.supply_rail_pitch - supply_rail_spacing

        # LEFT vertical rails
        offset = ll + vector(-2 * self.supply_rail_pitch,
                             -2 * self.supply_rail_pitch)
        left_gnd_pin = self.add_layout_pin(text="gnd",
                                           layer="m2",
                                           offset=offset,
                                           width=self.supply_rail_width,
                                           height=height)

        offset = ll + vector(-1 * self.supply_rail_pitch,
                             -1 * self.supply_rail_pitch)
        left_vdd_pin = self.add_layout_pin(text="vdd",
                                           layer="m2",
                                           offset=offset,
                                           width=self.supply_rail_width,
                                           height=height)

        # RIGHT vertical rails
        offset = vector(ur.x, ll.y) + vector(0, -2 * self.supply_rail_pitch)
        right_gnd_pin = self.add_layout_pin(text="gnd",
                                            layer="m2",
                                            offset=offset,
                                            width=self.supply_rail_width,
                                            height=height)

        offset = vector(ur.x, ll.y) + vector(self.supply_rail_pitch,
                                            -1 * self.supply_rail_pitch)
        right_vdd_pin = self.add_layout_pin(text="vdd",
                                            layer="m2",
                                            offset=offset,
                                            width=self.supply_rail_width,
                                            height=height)

        # BOTTOM horizontal rails
        offset = ll + vector(-2 * self.supply_rail_pitch,
                             -2 * self.supply_rail_pitch)
        bottom_gnd_pin = self.add_layout_pin(text="gnd",
                                             layer="m1",
                                             offset=offset,
                                             width=width,
                                             height=self.supply_rail_width)

        offset = ll + vector(-1 * self.supply_rail_pitch,
                             -1 * self.supply_rail_pitch)
        bottom_vdd_pin = self.add_layout_pin(text="vdd",
                                             layer="m1",
                                             offset=offset,
                                             width=width,
                                             height=self.supply_rail_width)

        # TOP horizontal rails
        offset = vector(ll.x, ur.y) + vector(-2 * self.supply_rail_pitch,
                                             0)
        top_gnd_pin = self.add_layout_pin(text="gnd",
                                          layer="m1",
                                          offset=offset,
                                          width=width,
                                          height=self.supply_rail_width)

        offset = vector(ll.x, ur.y) + vector(-1 * self.supply_rail_pitch,
                                             self.supply_rail_pitch)
        top_vdd_pin = self.add_layout_pin(text="vdd",
                                          layer="m1",
                                          offset=offset,
                                          width=width,
                                          height=self.supply_rail_width)

        # Remember these for connecting things in the design
        self.left_gnd_x_center = left_gnd_pin.cx()
        self.left_vdd_x_center = left_vdd_pin.cx()
        self.right_gnd_x_center = right_gnd_pin.cx()
        self.right_vdd_x_center = right_vdd_pin.cx()

        self.bottom_gnd_y_center = bottom_gnd_pin.cy()
        self.bottom_vdd_y_center = bottom_vdd_pin.cy()
        self.top_gnd_y_center = top_gnd_pin.cy()
        self.top_vdd_y_center = top_vdd_pin.cy()

        # Find the number of vias for this pitch
        self.supply_vias = 1
        while True:
            c = factory.create(module_type="contact",
                               layer_stack=self.m1_stack,
                               dimensions=(self.supply_vias, self.supply_vias))
            if c.second_layer_width < self.supply_rail_width and c.second_layer_height < self.supply_rail_width:
                self.supply_vias += 1
            else:
                self.supply_vias -= 1
                break

        via_points = [vector(self.left_gnd_x_center, self.bottom_gnd_y_center),
                      vector(self.left_gnd_x_center, self.top_gnd_y_center),
                      vector(self.right_gnd_x_center, self.bottom_gnd_y_center),
                      vector(self.right_gnd_x_center, self.top_gnd_y_center),
                      vector(self.left_vdd_x_center, self.bottom_vdd_y_center),
                      vector(self.left_vdd_x_center, self.top_vdd_y_center),
                      vector(self.right_vdd_x_center, self.bottom_vdd_y_center),
                      vector(self.right_vdd_x_center, self.top_vdd_y_center)]

        for pt in via_points:
            self.add_via_center(layers=self.m1_stack,
                                offset=pt,
                                size=(self.supply_vias,
                                      self.supply_vias))

    def pdf_write(self, pdf_name):
        """
        Display the layout to a PDF file.
        """
        debug.error("NOTE: Currently does not work (Needs further research)")
        # self.pdf_name = self.name + ".pdf"
        debug.info(0, "Writing to {}".format(pdf_name))
        pdf = gdsMill.pdfLayout(self.gds)

        return
        pdf.layerColors[self.gds.layerNumbersInUse[0]] = "#219E1C"
        pdf.layerColors[self.gds.layerNumbersInUse[1]] = "#271C9E"
        pdf.layerColors[self.gds.layerNumbersInUse[2]] = "#CC54C8"
        pdf.layerColors[self.gds.layerNumbersInUse[3]] = "#E9C514"
        pdf.layerColors[self.gds.layerNumbersInUse[4]] = "#856F00"
        pdf.layerColors[self.gds.layerNumbersInUse[5]] = "#BD1444"
        pdf.layerColors[self.gds.layerNumbersInUse[6]] = "#FD1444"
        pdf.layerColors[self.gds.layerNumbersInUse[7]] = "#FD1414"

        pdf.setScale(500)
        pdf.drawLayout()
        pdf.writeToFile(pdf_name)



    def print_attr(self):
        """Prints a list of attributes for the current layout object"""
        debug.info(0,
                   "|==============================================================================|")
        debug.info(0,
                   "|=========      LIST OF OBJECTS (Rects) FOR: " + self.name)
        debug.info(0,
                   "|==============================================================================|")
        for obj in self.objs:
            debug.info(0, "layer={0} : offset={1} : size={2}".format(obj.layerNumber,
                                                                     obj.offset,
                                                                     obj.size))

        debug.info(0,
                   "|==============================================================================|")
        debug.info(0,
                   "|=========      LIST OF INSTANCES FOR: " + self.name)
        debug.info(0,
                   "|==============================================================================|")
        for inst in self.insts:
            debug.info(0, "name={0} : mod={1} : offset={2}".format(inst.name,
                                                                   inst.mod.name,
                                                                   inst.offset))
