# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import collections
import geometry
import gdsMill
import debug
from math import sqrt
from tech import drc, GDS
from tech import layer as techlayer
from tech import layer_indices
from tech import layer_stacks
import os
from globals import OPTS
from vector import vector
from pin_layout import pin_layout
from utils import round_to_grid


class layout():
    """
    Class consisting of a set of objs and instances for a module
    This provides a set of useful generic types for hierarchy
    management. If a module is a custom designed cell, it will read from
    the GDS and spice files and perform LVS/DRC. If it is dynamically
    generated, it should implement a constructor to create the
    layout/netlist and perform LVS/DRC.
    """

    def __init__(self, name):
        self.name = name
        self.width = None
        self.height = None
        self.bounding_box = None
        self.insts = []      # Holds module/cell layout instances
        self.objs = []       # Holds all other objects (labels, geometries, etc)
        self.pin_map = {}    # Holds name->pin_layout map for all pins
        self.visited = []    # List of modules we have already visited
        self.is_library_cell = False # Flag for library cells
        self.gds_read()
        
        try:
            from tech import power_grid
            self.pwr_grid_layer = power_grid[0]
        except ImportError:
            self.pwr_grid_layer = "m3"

            

    ############################################################
    # GDS layout
    ############################################################
    def offset_all_coordinates(self):
        """ This function is called after everything is placed to
        shift the origin in the lowest left corner """
        offset = self.find_lowest_coords()
        self.translate_all(offset)
        return offset

    def get_gate_offset(self, x_offset, height, inv_num):
        """Gets the base offset and y orientation of stacked rows of gates
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

        if len(self.objs) > 0:
            lowestx1 = min(obj.lx() for obj in self.objs if obj.name != "label")
            lowesty1 = min(obj.by() for obj in self.objs if obj.name != "label")
        else:
            lowestx1 = lowesty1 = None
        if len(self.insts) > 0:
            lowestx2 = min(inst.lx() for inst in self.insts)
            lowesty2 = min(inst.by() for inst in self.insts)
        else:
            lowestx2 = lowesty2 = None

        if lowestx1 == None and lowestx2 == None:
            return None
        elif lowestx1 == None:
            return vector(lowestx2, lowesty2)
        elif lowestx2 == None:
            return vector(lowestx1, lowesty1)
        else:
            return vector(min(lowestx1, lowestx2), min(lowesty1, lowesty2))

    def find_highest_coords(self):
        """
        Finds the highest set of 2d cartesian coordinates within
        this layout
        """
        if len(self.objs) > 0:
            highestx1 = max(obj.rx() for obj in self.objs if obj.name != "label")
            highesty1 = max(obj.uy() for obj in self.objs if obj.name != "label")
        else:
            highestx1 = highesty1 = None
        if len(self.insts) > 0:
            highestx2 = max(inst.rx() for inst in self.insts)
            highesty2 = max(inst.uy() for inst in self.insts)
        else:
            highestx2 = highesty2 = None
        if highestx1 == None and highestx2 == None:
            return None
        elif highestx1 == None:
            return vector(highestx2, highesty2)
        elif highestx2 == None:
            return vector(highestx1, highesty1)
        else:
            return vector(max(highestx1, highestx2),
                          max(highesty1, highesty2))

    def find_highest_layer_coords(self, layer):
        """
        Finds the highest set of 2d cartesian coordinates within
        this layout on a layer
        """
        # Only consider the layer not the purpose for now
        layerNumber = techlayer[layer][0]
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
        layerNumber = techlayer[layer][0]
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
                inst.compute_boundary(inst.offset)
        for pin_name in self.pin_map.keys():
            # All the pins are absolute coordinates that need to be updated.
            pin_list = self.pin_map[pin_name]
            for pin in pin_list:
                pin.rect = [pin.ll() - offset, pin.ur() - offset]

    def add_inst(self, name, mod, offset=[0, 0], mirror="R0", rotate=0):
        """ Adds an instance of a mod to this module """
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

    def add_rect(self, layer, offset, width=None, height=None):
        """
        Adds a rectangle on a given layer,offset with width and height
        """
        if not width:
            width = drc["minwidth_{}".format(layer)]
        if not height:
            height = drc["minwidth_{}".format(layer)]
        lpp = techlayer[layer]
        if abs(offset[0]-5.16250)<0.01 and abs(offset[1]-8.70750)<0.01:
            import pdb; pdb.set_trace()
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
        lpp = techlayer[layer]
        corrected_offset = offset - vector(0.5 * width, 0.5 * height)
        self.objs.append(geometry.rectangle(lpp,
                                            corrected_offset,
                                            width,
                                            height))
        return self.objs[-1]

    def add_segment_center(self, layer, start, end):
        """
        Add a min-width rectanglular segment using center
        line on the start to end point
        """
        minwidth_layer = drc["minwidth_{}".format(layer)]
        if start.x != end.x and start.y != end.y:
            debug.error("Nonrectilinear center rect!", -1)
        elif start.x != end.x:
            offset = vector(0, 0.5 * minwidth_layer)
            return self.add_rect(layer,
                                 start - offset,
                                 end.x - start.x,
                                 minwidth_layer)
        else:
            offset = vector(0.5 * minwidth_layer, 0)
            return self.add_rect(layer,
                                 start - offset,
                                 minwidth_layer,
                                 end.y - start.y)

    def get_pin(self, text):
        """
        Return the pin or list of pins
        """
        try:
            if len(self.pin_map[text]) > 1:
                debug.error("Should use a pin iterator since more than one pin {}".format(text), -1)
            # If we have one pin, return it and not the list.
            # Otherwise, should use get_pins()
            any_pin = next(iter(self.pin_map[text]))
            return any_pin
        except Exception:
            self.gds_write("missing_pin.gds")
            debug.error("No pin found with name {0} on {1}. Saved as missing_pin.gds.".format(text, self.name), -1)

    def get_pins(self, text):
        """
        Return a pin list (instead of a single pin)
        """
        if text in self.pin_map.keys():
            return self.pin_map[text]
        else:
            return set()

    def get_pin_names(self):
        """
        Return a pin list of all pins
        """
        return self.pin_map.keys()

    def copy_layout_pin(self, instance, pin_name, new_name=""):
        """
        Create a copied version of the layout pin at the current level.
        You can optionally rename the pin to a new name.
        """
        pins = instance.get_pins(pin_name)

        debug.check(len(pins) > 0,
                    "Could not find pin {}".format(pin_name))

        for pin in pins:
            if new_name == "":
                new_name = pin.name
            self.add_layout_pin(new_name,
                                pin.layer,
                                pin.ll(),
                                pin.width(),
                                pin.height())

    def copy_layout_pins(self, instance, prefix=""):
        """
        Create a copied version of the layout pin at the current level.
        You can optionally rename the pin to a new name.
        """
        for pin_name in self.pin_map.keys():
            self.copy_layout_pin(instance, pin_name, prefix + pin_name)

    def add_layout_pin_segment_center(self, text, layer, start, end):
        """
        Creates a path like pin with center-line convention
        """
        if start.x != end.x and start.y != end.y:
            file_name = "non_rectilinear.gds"
            self.gds_write(file_name)
            debug.error("Cannot have a non-manhatten layout pin: {}".format(file_name), -1)

        minwidth_layer = drc["minwidth_{}".format(layer)]

        # one of these will be zero
        width = max(start.x, end.x) - min(start.x, end.x)
        height = max(start.y, end.y) - min(start.y, end.y)
        ll_offset = vector(min(start.x, end.x), min(start.y, end.y))

        # Shift it down 1/2 a width in the 0 dimension
        if height == 0:
            ll_offset -= vector(0, 0.5 * minwidth_layer)
        if width == 0:
            ll_offset -= vector(0.5 * minwidth_layer, 0)
        # This makes sure it is long enough, but also it is not 0 width!
        height = max(minwidth_layer, height)
        width = max(minwidth_layer, width)

        return self.add_layout_pin(text,
                                   layer,
                                   ll_offset,
                                   width,
                                   height)

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

    def add_label(self, text, layer, offset=[0, 0], zoom=-1):
        """Adds a text label on the given layer,offset, and zoom level"""
        debug.info(5, "add label " + str(text) + " " + layer + " " + str(offset))
        lpp = techlayer[layer]
        self.objs.append(geometry.label(text, lpp, offset, zoom))
        return self.objs[-1]

    def add_path(self, layer, coordinates, width=None):
        """Connects a routing path on given layer,coordinates,width."""
        debug.info(4, "add path " + str(layer) + " " + str(coordinates))
        import wire_path
        # NOTE: (UNTESTED) add_path(...) is currently not used
        # lpp = techlayer[layer]
        # self.objs.append(geometry.path(lpp, coordinates, width))

        wire_path.wire_path(obj=self,
                            layer=layer,
                            position_list=coordinates,
                            width=width)

    def add_route(self, layers, coordinates, layer_widths):
        """Connects a routing path on given layer,coordinates,width. The
        layers are the (horizontal, via, vertical). add_wire assumes
        preferred direction routing whereas this includes layers in
        the coordinates.
        """
        import route
        debug.info(4, "add route " + str(layers) + " " + str(coordinates))
        # add an instance of our path that breaks down into rectangles and contacts
        route.route(obj=self,
                    layer_stack=layers,
                    path=coordinates,
                    layer_widths=layer_widths)

    def add_zjog(self, layer, start, end, first_direction="H"):
        """
        Add a simple jog at the halfway point.
        If layer is a single value, it is a path.
        If layer is a tuple, it is a wire with preferred directions.
        """

        # vertical first
        if first_direction == "V":
            mid1 = vector(start.x, 0.5 * start.y + 0.5 * end.y)
            mid2 = vector(end.x, mid1.y)
        # horizontal first
        elif first_direction == "H":
            mid1 = vector(0.5 * start.x + 0.5 * end.x, start.y)
            mid2 = vector(mid1, end.y)
        else:
            debug.error("Invalid direction for jog -- must be H or V.")
            
        if layer in layer_stacks:
            self.add_wire(layer, [start, mid1, mid2, end])
        elif layer in techlayer:
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
        import wire
        # add an instance of our path that breaks down
        # into rectangles and contacts
        wire.wire(obj=self,
                  layer_stack=layers,
                  position_list=coordinates,
                  widen_short_wires=widen_short_wires)

    def get_preferred_direction(self, layer):
        """ Return the preferred routing directions """
        from tech import preferred_directions
        return preferred_directions[layer]

    def add_via(self, layers, offset, size=[1, 1], directions=None, implant_type=None, well_type=None):
        """ Add a three layer via structure. """
        from sram_factory import factory
        via = factory.create(module_type="contact",
                             layer_stack=layers,
                             dimensions=size,
                             directions=directions,
                             implant_type=implant_type,
                             well_type=well_type)
        self.add_mod(via)
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
        from sram_factory import factory
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

        self.add_mod(via)
        inst = self.add_inst(name=via.name,
                             mod=via,
                             offset=corrected_offset)
        # We don't model the logical connectivity of wires/paths
        self.connect_inst([])
        return inst

    def add_via_stack(self, offset, from_layer, to_layer,
                      directions=None,
                      size=[1, 1],
                      implant_type=None,
                      well_type=None):
        """
        Punch a stack of vias from a start layer to a target layer.
        """
        return self.__add_via_stack_internal(offset=offset,
                                             directions=directions,
                                             from_layer=from_layer,
                                             to_layer=to_layer,
                                             via_func=self.add_via,
                                             last_via=None,
                                             size=size,
                                             implant_type=implant_type,
                                             well_type=well_type)

    def add_via_stack_center(self,
                             offset,
                             from_layer,
                             to_layer,
                             directions=None,
                             size=[1, 1],
                             implant_type=None,
                             well_type=None):
        """
        Punch a stack of vias from a start layer to a target layer by the center
        coordinate accounting for mirroring and rotation.
        """
        return self.__add_via_stack_internal(offset=offset,
                                             directions=directions,
                                             from_layer=from_layer,
                                             to_layer=to_layer,
                                             via_func=self.add_via_center,
                                             last_via=None,
                                             size=size,
                                             implant_type=implant_type,
                                             well_type=well_type)

    def __add_via_stack_internal(self, offset, directions, from_layer, to_layer,
                                 via_func, last_via, size, implant_type=None, well_type=None):
        """
        Punch a stack of vias from a start layer to a target layer. Here we
        figure out whether to punch it up or down the stack.
        """

        if from_layer == to_layer:
            return last_via

        from_id = layer_indices[from_layer]
        to_id   = layer_indices[to_layer]

        if from_id < to_id: # grow the stack up
            search_id = 0
            next_id = 2
        else: # grow the stack down
            search_id = 2
            next_id = 0

        curr_stack = next(filter(lambda stack: stack[search_id] == from_layer, layer_stacks), None)
        if curr_stack is None:
            raise ValueError("Cannot create via from '{0}' to '{1}'."
                             "Layer '{0}' not defined".format(from_layer, to_layer))

        via = via_func(layers=curr_stack,
                       size=size,
                       offset=offset,
                       directions=directions,
                       implant_type=implant_type,
                       well_type=well_type)

        via = self.__add_via_stack_internal(offset=offset,
                                            directions=directions,
                                            from_layer=curr_stack[next_id],
                                            to_layer=to_layer,
                                            via_func=via_func,
                                            last_via=via,
                                            size=size)
        return via
    
    def add_ptx(self, offset, mirror="R0", rotate=0, width=1, mults=1, tx_type="nmos"):
        """Adds a ptx module to the design."""
        import ptx
        mos = ptx.ptx(width=width,
                      mults=mults,
                      tx_type=tx_type)
        self.add_mod(mos)
        inst = self.add_inst(name=mos.name,
                             mod=mos,
                             offset=offset,
                             mirror=mirror,
                             rotate=rotate)
        return inst

    def gds_read(self):
        """Reads a GDSII file in the library and checks if it exists
           Otherwise, start a new layout for dynamic generation."""

        # This must be done for netlist only mode too
        if os.path.isfile(self.gds_file):
            self.is_library_cell = True

        if OPTS.netlist_only:
            self.gds = None
            return

        # open the gds file if it exists or else create a blank layout
        if os.path.isfile(self.gds_file):
            debug.info(3, "opening {}".format(self.gds_file))
            self.gds = gdsMill.VlsiLayout(units=GDS["unit"])
            reader = gdsMill.Gds2reader(self.gds)
            reader.loadFromFile(self.gds_file)
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
        reader.loadFromFile(gds_file)

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
            if "stdc" in techlayer.keys():
                boundary_layer = "stdc"
                boundary = [self.find_lowest_coords(),
                            self.find_highest_coords()]
                height = boundary[1][1] - boundary[0][1]
                width = boundary[1][0] - boundary[0][0]
                (layer_number, layer_purpose) = techlayer[boundary_layer]
                gds_layout.addBox(layerNumber=layer_number,
                                  purposeNumber=layer_purpose,
                                  offsetInMicrons=boundary[0],
                                  width=width,
                                  height=height,
                                  center=False)
                debug.info(2, "Adding {0} boundary {1}".format(self.name, boundary))

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
            lpp = techlayer[layer]
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

        line_positions = {}
        if vertical:
            for i in range(len(names)):
                line_offset = offset + vector(i * pitch,
                                              0)
                if make_pins:
                    self.add_layout_pin(text=names[i],
                                        layer=layer,
                                        offset=line_offset,
                                        height=length)
                else:
                    self.add_rect(layer=layer,
                                  offset=line_offset,
                                  height=length)
                line_positions[names[i]] = line_offset + vector(half_minwidth, 0)
        else:
            for i in range(len(names)):
                line_offset = offset + vector(0,
                                              i * pitch + half_minwidth)
                if make_pins:
                    self.add_layout_pin(text=names[i],
                                        layer=layer,
                                        offset=line_offset,
                                        width=length)
                else:
                    self.add_rect(layer=layer,
                                  offset=line_offset,
                                  width=length)
                # Make this the center of the rail
                line_positions[names[i]] = line_offset + vector(0.5 * length,
                                                                half_minwidth)

        return line_positions

    def connect_horizontal_bus(self, mapping, inst, bus_offsets,
                               layer_stack=("m1", "via1", "m2")):
        """ Horizontal version of connect_bus. """
        self.connect_bus(mapping, inst, bus_offsets, layer_stack, True)

    def connect_vertical_bus(self, mapping, inst, bus_offsets,
                             layer_stack=("m1", "via1", "m2")):
        """ Vertical version of connect_bus. """
        self.connect_bus(mapping, inst, bus_offsets, layer_stack, False)

    def connect_bus(self, mapping, inst, bus_offsets, layer_stack, horizontal):
        """
        Connect a mapping of pin -> name for a bus. This could be
        replaced with a channel router in the future.
        NOTE: This has only really been tested with point-to-point
        connections (not multiple pins on a net).
        """
        (horizontal_layer, via_layer, vertical_layer) = layer_stack
        if horizontal:
            route_layer = vertical_layer
        else:
            route_layer = horizontal_layer

        for (pin_name, bus_name) in mapping:
            pin = inst.get_pin(pin_name)
            pin_pos = pin.center()
            bus_pos = bus_offsets[bus_name]

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
                self.add_via_center(layers=layer_stack,
                                    offset=pin_pos)
            # FIXME: output pins tend to not be rotate,
            # but supply pins are. Make consistent?

            # We only need a via if they happened to align perfectly
            # so the add_wire didn't add a via
            if (horizontal and bus_pos.y == pin_pos.y) or (not horizontal and bus_pos.x == pin_pos.x):
                self.add_via_center(layers=layer_stack,
                                    offset=bus_pos,
                                    rotate=90)

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
        
    def get_layer_pitch(self, layer):
        """ Return the track pitch on a given layer """
        try:
            # FIXME: Using non-pref pitch here due to overlap bug in VCG constraints.
            # It should just result in inefficient channel width but will work.
            pitch = getattr(self, "{}_pitch".format(layer))
            nonpref_pitch = getattr(self, "{}_nonpref_pitch".format(layer))
            space = getattr(self, "{}_space".format(layer))
        except AttributeError:
            debug.error("Cannot find layer pitch.", -1)
        return (nonpref_pitch, pitch, pitch - space, space)
    
    def add_horizontal_trunk_route(self,
                                   pins,
                                   trunk_offset,
                                   layer_stack,
                                   pitch):
        """
        Create a trunk route for all pins with
        the trunk located at the given y offset.
        """
        max_x = max([pin.center().x for pin in pins])
        min_x = min([pin.center().x for pin in pins])

        # if we are less than a pitch, just create a non-preferred layer jog
        if max_x - min_x <= pitch:
            half_layer_width = 0.5 * drc["minwidth_{0}".format(self.vertical_layer)]

            # Add the horizontal trunk on the vertical layer!
            self.add_path(self.vertical_layer,
                          [vector(min_x - half_layer_width, trunk_offset.y),
                           vector(max_x + half_layer_width, trunk_offset.y)])

            # Route each pin to the trunk
            for pin in pins:
                # No bend needed here
                mid = vector(pin.center().x, trunk_offset.y)
                self.add_path(self.vertical_layer, [pin.center(), mid])
        else:
            # Add the horizontal trunk
            self.add_path(self.horizontal_layer,
                          [vector(min_x, trunk_offset.y),
                           vector(max_x, trunk_offset.y)])

            # Route each pin to the trunk
            for pin in pins:
                mid = vector(pin.center().x, trunk_offset.y)
                self.add_path(self.vertical_layer, [pin.center(), mid])
                self.add_via_center(layers=layer_stack,
                                    offset=mid)

    def add_vertical_trunk_route(self,
                                 pins,
                                 trunk_offset,
                                 layer_stack,
                                 pitch):
        """
        Create a trunk route for all pins with the
        trunk located at the given x offset.
        """
        max_y = max([pin.center().y for pin in pins])
        min_y = min([pin.center().y for pin in pins])

        # if we are less than a pitch, just create a non-preferred layer jog
        if max_y - min_y <= pitch:

            half_layer_width = 0.5 * drc["minwidth_{0}".format(self.horizontal_layer)]

            # Add the vertical trunk on the horizontal layer!
            self.add_path(self.horizontal_layer,
                          [vector(trunk_offset.x, min_y - half_layer_width),
                           vector(trunk_offset.x, max_y + half_layer_width)])

            # Route each pin to the trunk
            for pin in pins:
                # No bend needed here
                mid = vector(trunk_offset.x, pin.center().y)
                self.add_path(self.horizontal_layer, [pin.center(), mid])
        else:
            # Add the vertical trunk
            self.add_path(self.vertical_layer,
                          [vector(trunk_offset.x, min_y),
                           vector(trunk_offset.x, max_y)])

            # Route each pin to the trunk
            for pin in pins:
                mid = vector(trunk_offset.x, pin.center().y)
                self.add_path(self.horizontal_layer, [pin.center(), mid])
                self.add_via_center(layers=layer_stack,
                                    offset=mid)

    def create_channel_route(self, netlist,
                             offset,
                             layer_stack,
                             directions=None,
                             vertical=False):
        """
        The net list is a list of the nets with each net being a list of pins
        to be connected. The offset is the lower-left of where the
        routing channel will start.  This does NOT try to minimize the
        number of tracks -- instead, it picks an order to avoid the
        vertical conflicts between pins. The track size must be the number of
        nets times the *nonpreferred* routing of the non-track layer pitch.

        """
        def remove_net_from_graph(pin, g):
            """
            Remove the pin from the graph and all conflicts
            """
            g.pop(pin, None)

            # Remove the pin from all conflicts
            # FIXME: This is O(n^2), so maybe optimize it.
            for other_pin, conflicts in g.items():
                if pin in conflicts:
                    conflicts.remove(pin)
                    g[other_pin]=conflicts
            return g

        def vcg_nets_overlap(net1, net2, vertical):
            """
            Check all the pin pairs on two nets and return a pin
            overlap if any pin overlaps.
            """

            if vertical:
                pitch = self.horizontal_nonpref_pitch
            else:
                pitch = self.vertical_nonpref_pitch
            
            for pin1 in net1:
                for pin2 in net2:
                    if vcg_pin_overlap(pin1, pin2, vertical, pitch):
                        return True

            return False

        def vcg_pin_overlap(pin1, pin2, vertical, pitch):
            """ Check for vertical or horizontal overlap of the two pins """
            
            # FIXME: If the pins are not in a row, this may break.
            # However, a top pin shouldn't overlap another top pin,
            # for example, so the extra comparison *shouldn't* matter.

            # Pin 1 must be in the "BOTTOM" set
            x_overlap = pin1.by() < pin2.by() and abs(pin1.center().x - pin2.center().x) < pitch

            # Pin 1 must be in the "LEFT" set
            y_overlap = pin1.lx() < pin2.lx() and abs(pin1.center().y - pin2.center().y) < pitch
            overlaps = (not vertical and x_overlap) or (vertical and y_overlap)
            return overlaps

        if not directions:
            # Use the preferred layer directions
            if self.get_preferred_direction(layer_stack[0]) == "V":
                self.vertical_layer = layer_stack[0]
                self.horizontal_layer = layer_stack[2]
            else:
                self.vertical_layer = layer_stack[2]
                self.horizontal_layer = layer_stack[0]
        else:
            # Use the layer directions specified to the router rather than
            # the preferred directions
            debug.check(directions[0] != directions[1], "Must have unique layer directions.")
            if directions[0] == "V":
                self.vertical_layer = layer_stack[0]
                self.horizontal_layer = layer_stack[2]
            else:
                self.horizontal_layer = layer_stack[0]
                self.vertical_layer = layer_stack[2]

        layer_stuff = self.get_layer_pitch(self.vertical_layer)
        (self.vertical_nonpref_pitch, self.vertical_pitch, self.vertical_width, self.vertical_space) = layer_stuff
        
        layer_stuff = self.get_layer_pitch(self.horizontal_layer)
        (self.horizontal_nonpref_pitch, self.horizontal_pitch, self.horizontal_width, self.horizontal_space) = layer_stuff

        # FIXME: Must extend this to a horizontal conflict graph
        # too if we want to minimize the
        # number of tracks!
        # hcg = {}

        # Initialize the vertical conflict graph (vcg)
        # and make a list of all pins
        vcg = collections.OrderedDict()

        # Create names for the nets for the graphs
        nets = collections.OrderedDict()
        index = 0
        # print(netlist)
        for pin_list in netlist:
            net_name = "n{}".format(index)
            index += 1
            nets[net_name] = pin_list

        # print("Nets:")
        # for net_name in nets:
         #    print(net_name, [x.name for x in nets[net_name]])
            
        # Find the vertical pin conflicts
        # FIXME: O(n^2) but who cares for now
        for net_name1 in nets:
            if net_name1 not in vcg.keys():
                vcg[net_name1] = []
            for net_name2 in nets:
                if net_name2 not in vcg.keys():
                    vcg[net_name2] = []
                # Skip yourself
                if net_name1 == net_name2:
                    continue
                if vcg_nets_overlap(nets[net_name1],
                                    nets[net_name2],
                                    vertical):
                    vcg[net_name2].append(net_name1)

        # list of routes to do
        while vcg:
            # from pprint import pformat
            # print("VCG:\n", pformat(vcg))
            # get a route from conflict graph with empty fanout set
            net_name = None
            for net_name, conflicts in vcg.items():
                if len(conflicts) == 0:
                    vcg = remove_net_from_graph(net_name, vcg)
                    break
            else:
                # FIXME: We don't support cyclic VCGs right now.
                debug.error("Cyclic VCG in channel router.", -1)

            # These are the pins we'll have to connect
            pin_list = nets[net_name]
            # print("Routing:", net_name, [x.name for x in pin_list])

            # Remove the net from other constriants in the VCG
            vcg = remove_net_from_graph(net_name, vcg)

            # Add the trunk routes from the bottom up for
            # horizontal or the left to right for vertical
            if vertical:
                self.add_vertical_trunk_route(pin_list,
                                              offset,
                                              layer_stack,
                                              self.vertical_nonpref_pitch)
                # This accounts for the via-to-via spacings
                offset += vector(self.horizontal_nonpref_pitch, 0)
            else:
                self.add_horizontal_trunk_route(pin_list,
                                                offset,
                                                layer_stack,
                                                self.horizontal_nonpref_pitch)
                # This accounts for the via-to-via spacings
                offset += vector(0, self.vertical_nonpref_pitch)

    def create_vertical_channel_route(self, netlist, offset, layer_stack, directions=None):
        """
        Wrapper to create a vertical channel route
        """
        self.create_channel_route(netlist, offset, layer_stack, directions, vertical=True)

    def create_horizontal_channel_route(self, netlist, offset, layer_stack, directions=None):
        """
        Wrapper to create a horizontal channel route
        """
        self.create_channel_route(netlist, offset, layer_stack, directions, vertical=False)

    def add_boundary(self, ll=vector(0, 0), ur=None):
        """ Add boundary for debugging dimensions """
        if OPTS.netlist_only:
            return

        if "stdc" in techlayer.keys():
            boundary_layer = "stdc"
        else:
            boundary_layer = "boundary"
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

    def add_enclosure(self, insts, layer="nwell"):
        """ Add a layer that surrounds the given instances. Useful
        for creating wells, for example. Doesn't check for minimum widths or
        spacings."""

        xmin = insts[0].lx()
        ymin = insts[0].by()
        xmax = insts[0].rx()
        ymax = insts[0].uy()
        for inst in insts:
            xmin = min(xmin, inst.lx())
            ymin = min(ymin, inst.by())
            xmax = max(xmax, inst.rx())
            ymax = max(ymax, inst.uy())

        self.add_rect(layer=layer,
                      offset=vector(xmin, ymin),
                      width=xmax - xmin,
                      height=ymax - ymin)

    def copy_power_pins(self, inst, name):
        """
        This will copy a power pin if it is on the lowest power_grid layer.
        If it is on M1, it will add a power via too.
        """
        pins = inst.get_pins(name)
        for pin in pins:
            if pin.layer == self.pwr_grid_layer:
                self.add_layout_pin(name,
                                    pin.layer,
                                    pin.ll(),
                                    pin.width(),
                                    pin.height())
            elif pin.layer == "m1":
                self.add_power_pin(name, pin.center())
            else:
                debug.warning("{0} pins of {1} should be on {2} or metal1 for "\
                              "supply router."
                              .format(name, inst.name, self.pwr_grid_layer))

    def add_power_pin(self, name, loc, size=[1, 1], directions=None, start_layer="m1"):
        """
        Add a single power pin from the lowest power_grid layer down to M1 (or li) at
        the given center location. The starting layer is specified to determine
        which vias are needed.
        """

        via = self.add_via_stack_center(from_layer=start_layer,
                                        to_layer=self.pwr_grid_layer,
                                        size=size,
                                        offset=loc,
                                        directions=directions)
        if start_layer == self.pwr_grid_layer:
            self.add_layout_pin_rect_center(text=name,
                                            layer=self.pwr_grid_layer,
                                            offset=loc)
        else:
            # Hack for min area
            if OPTS.tech_name == "s8":
                width = round_to_grid(sqrt(drc["minarea_m3"]))
                height = round_to_grid(drc["minarea_m3"]/width)
            else:
                width = via.width
                height = via.height
            self.add_layout_pin_rect_center(text=name,
                                            layer=self.pwr_grid_layer,
                                            offset=loc,
                                            width=width,
                                            height=height)

    def add_power_ring(self, bbox):
        """
        Create vdd and gnd power rings around an area of the bounding box
        argument. Must have a supply_rail_width and supply_rail_pitch
        defined as a member variable.  Defines local variables of the
        left/right/top/bottom vdd/gnd center offsets for use in other
        modules..
        """

        [ll, ur] = bbox

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
        from sram_factory import factory
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
