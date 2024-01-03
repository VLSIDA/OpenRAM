# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram.gdsMill import gdsMill
from openram.tech import GDS
from openram.tech import drc
from openram.tech import layer as tech_layer
from openram import OPTS
from .graph_shape import graph_shape
from .graph_utils import snap
from .router_tech import router_tech


class router(router_tech):
    """
    This is the base class for routers that use the Hanan grid graph method.
    """

    def __init__(self, layers, design, bbox=None):

        # `router_tech` contains tech constants for the router
        router_tech.__init__(self, layers, route_track_width=1)

        # Layers that can be used for routing
        self.layers = layers
        # This is the `hierarchy_layout` object
        self.design = design
        # Temporary GDSII file name to find pins and blockages
        self.gds_filename = OPTS.openram_temp + "temp.gds"
        # Calculate the bounding box for routing around the perimeter
        # FIXME: We wouldn't do this if `rom_bank` wasn't behaving weird
        if bbox is None:
            self.bbox = self.design.get_bbox(margin=11 * self.track_width)
        else:
            ll, ur = bbox
            margin = vector([11 * self.track_width] * 2)
            self.bbox = [ll - margin, ur + margin]
        # Dictionary for vdd and gnd pins
        self.pins = {}
        # Set of all the pins
        self.all_pins = set()
        # This is all the blockages including the pins. The graph class handles
        # pins as blockages while considering their routability
        self.blockages = []
        # This is all the vias between routing layers
        self.vias = []
        # Fake pins are imaginary pins on the side supply pins to route other
        # pins to them
        self.fake_pins = []

        # Set the offset here
        self.half_wire = snap(self.track_wire / 2)


    def prepare_gds_reader(self):
        """ Write the current layout to a temporary file to read the layout. """

        # NOTE: Avoid using this function if possible since it is too slow to
        # write/read these files
        self.design.gds_write(self.gds_filename)
        self.layout = gdsMill.VlsiLayout(units=GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(self.gds_filename)


    def merge_shapes(self, merger, shape_list):
        """
        Merge shapes in the list into the merger if they are contained or
        aligned by the merger.
        """

        merger_core = merger.get_core()
        for shape in list(shape_list):
            shape_core = shape.get_core()
            # If merger contains the shape, remove it from the list
            if merger_core.contains(shape_core):
                shape_list.remove(shape)
            # If the merger aligns with the shape, expand the merger and remove
            # the shape from the list
            elif merger_core.aligns(shape_core):
                merger.bbox([shape])
                merger_core.bbox([shape_core])
                shape_list.remove(shape)


    def find_pins(self, pin_name):
        """ Find the pins with the given name. """
        debug.info(4, "Finding all pins for {}".format(pin_name))

        shape_list = self.layout.getAllPinShapes(str(pin_name))
        pin_set = set()
        for shape in shape_list:
            layer, boundary = shape
            # gdsMill boundaries are in (left, bottom, right, top) order
            ll = vector(boundary[0], boundary[1])
            ur = vector(boundary[2], boundary[3])
            rect = [ll, ur]
            new_pin = graph_shape(pin_name, rect, layer)
            # Skip this pin if it's contained by another pin of the same type
            if new_pin.core_contained_by_any(pin_set):
                continue
            # Merge previous pins into this one if possible
            self.merge_shapes(new_pin, pin_set)
            pin_set.add(new_pin)
        # Add these pins to the 'pins' dict
        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)


    def find_blockages(self, name="blockage", shape_list=None):
        """ Find all blockages in the routing layers. """
        debug.info(4, "Finding blockages...")

        for lpp in [self.vert_lpp, self.horiz_lpp]:
            # If the list of shapes is given, don't get them from gdsMill
            if shape_list is None:
                shapes = self.layout.getAllShapes(lpp)
            else:
                shapes = shape_list
            for boundary in shapes:
                if shape_list is not None:
                    if boundary.lpp != lpp:
                        continue
                    ll = boundary.ll()
                    ur = boundary.ur()
                else:
                    # gdsMill boundaries are in (left, bottom, right, top) order
                    ll = vector(boundary[0], boundary[1])
                    ur = vector(boundary[2], boundary[3])
                rect = [ll, ur]
                new_shape = graph_shape(name, rect, lpp)
                new_shape = self.inflate_shape(new_shape)
                # Skip this blockage if it's contained by a pin or an existing
                # blockage
                if new_shape.core_contained_by_any(self.all_pins) or \
                   new_shape.core_contained_by_any(self.blockages):
                    continue
                # Merge previous blockages into this one if possible
                self.merge_shapes(new_shape, self.blockages)
                self.blockages.append(new_shape)


    def find_vias(self, shape_list=None):
        """ Find all vias in the routing layers. """
        debug.info(4, "Finding vias...")

        # Prepare lpp values here
        from openram.tech import layer
        via_lpp = layer[self.via_layer_name]
        valid_lpp = self.horiz_lpp # Just a temporary lpp to prevent errors

        # If the list of shapes is given, don't get them from gdsMill
        if shape_list is None:
            shapes = self.layout.getAllShapes(via_lpp)
        else:
            shapes = shape_list
        for boundary in shapes:
            if shape_list is not None:
                ll = boundary.ll()
                ur = boundary.ur()
            else:
                # gdsMill boundaries are in (left, bottom, right, top) order
                ll = vector(boundary[0], boundary[1])
                ur = vector(boundary[2], boundary[3])
            rect = [ll, ur]
            new_shape = graph_shape("via", rect, valid_lpp)
            # Skip this via if it's contained by an existing via blockage
            if new_shape.contained_by_any(self.vias):
                continue
            self.vias.append(self.inflate_shape(new_shape))


    def convert_vias(self):
        """ Convert vias that overlap a pin. """

        for via in self.vias:
            via_core = via.get_core()
            for pin in self.all_pins:
                pin_core = pin.get_core()
                via_core.lpp = pin_core.lpp
                # If the via overlaps a pin, change its name
                if via_core.overlaps(pin_core):
                    via.rename(pin.name)
                    break


    def convert_blockages(self):
        """ Convert blockages that overlap a pin. """

        # NOTE: You need to run `convert_vias()` before since a blockage may
        # be connected to a pin through a via.
        for blockage in self.blockages:
            blockage_core = blockage.get_core()
            for pin in self.all_pins:
                pin_core = pin.get_core()
                # If the blockage overlaps a pin, change its name
                if blockage_core.overlaps(pin_core):
                    blockage.rename(pin.name)
                    break
            else:
                for via in self.vias:
                    # Skip if this via isn't connected to a pin
                    if via.name == "via":
                        continue
                    via_core = via.get_core()
                    via_core.lpp = blockage_core.lpp
                    # If the blockage overlaps a pin via, change its name
                    if blockage_core.overlaps(via_core):
                        blockage.rename(via.name)
                        break


    def inflate_shape(self, shape):
        """ Inflate a given shape with spacing rules. """

        # Get the layer-specific spacing rule
        if self.get_zindex(shape.lpp) == 1:
            spacing = self.vert_layer_spacing
        else:
            spacing = self.horiz_layer_spacing
        # If the shape is wider than the supply wire width, its spacing can be
        # different
        wide = min(shape.width(), shape.height())
        if wide > self.layer_widths[0]:
            spacing = self.get_layer_space(self.get_zindex(shape.lpp), wide)

        # Shapes must keep their center lines away from any blockage to prevent
        # the nodes from being unconnected
        xdiff = self.track_wire - shape.width()
        ydiff = self.track_wire - shape.height()
        diff = snap(max(xdiff, ydiff) / 2)
        if diff > 0:
            spacing += diff

        # Add minimum unit to the spacing to keep nodes out of inflated regions
        spacing += drc["grid"]

        return shape.inflated_pin(spacing=spacing,
                                  extra_spacing=self.half_wire)


    def add_path(self, path):
        """ Add the route path to the layout. """

        nodes = self.prepare_path(path)
        shapes = self.add_route(nodes)
        return shapes


    def prepare_path(self, path):
        """
        Remove unnecessary nodes on the path to reduce the number of shapes in
        the layout.
        """

        nodes = [path[0]]
        direction = path[0].get_direction(path[1])
        candidate = path[1]
        for i in range(2, len(path)):
            node = path[i]
            current_direction = node.get_direction(candidate)
            # Skip the previous candidate since the current node follows the
            # same direction
            if direction == current_direction:
                candidate = node
            else:
                nodes.append(candidate)
                direction = current_direction
                candidate = node
        if candidate not in nodes:
            nodes.append(candidate)
        return nodes


    def add_route(self, nodes):
        """
        Custom `add_route` function since `hierarchy_layout.add_route` isn't
        working for this router.
        """

        new_wires = []
        new_vias = []
        for i in range(0, len(nodes) - 1):
            start = nodes[i].center
            end = nodes[i + 1].center
            direction = nodes[i].get_direction(nodes[i + 1])
            diff = start - end
            offset = start.min(end)
            offset = vector(offset.x - self.half_wire,
                            offset.y - self.half_wire)
            if direction == (1, 1): # Via
                offset = vector(start.x, start.y)
                via = self.design.add_via_center(layers=self.layers,
                                                 offset=offset)
                new_vias.append(via)
            else: # Wire
                wire = self.design.add_rect(layer=self.get_layer(start.z),
                                            offset=offset,
                                            width=abs(diff.x) + self.track_wire,
                                            height=abs(diff.y) + self.track_wire)
                new_wires.append(wire)
        return new_wires, new_vias


    def write_debug_gds(self, gds_name, g=None, source=None, target=None):
        """ Write the debug GDSII file for the router. """

        self.add_router_info(g, source, target)
        self.design.gds_write(gds_name)
        self.del_router_info()


    def add_router_info(self, g=None, source=None, target=None):
        """
        Add debug information to the text layer about the graph and router.
        """

        # Display the inflated blockage
        if g:
            for blockage in self.blockages:
                if blockage in g.graph_blockages:
                    self.add_object_info(blockage, "blockage{}++[{}]".format(self.get_zindex(blockage.lpp), blockage.name))
                else:
                    self.add_object_info(blockage, "blockage{}[{}]".format(self.get_zindex(blockage.lpp), blockage.name))
            for node in g.nodes:
                offset = (node.center.x, node.center.y)
                self.design.add_label(text="n{}".format(node.center.z),
                                      layer="text",
                                      offset=offset)
        else:
            for blockage in self.blockages:
                self.add_object_info(blockage, "blockage{}".format(self.get_zindex(blockage.lpp)))
        for pin in self.fake_pins:
            self.add_object_info(pin, "fake")
        if source:
            self.add_object_info(source, "source")
        if target:
            self.add_object_info(target, "target")


    def del_router_info(self):
        """ Delete router information from the text layer. """

        lpp = tech_layer["text"]
        self.design.objs = [x for x in self.design.objs if x.lpp != lpp]


    def add_object_info(self, obj, label):
        """ Add debug information to the text layer about an object. """

        ll, ur = obj.rect
        self.design.add_rect(layer="text",
                             offset=ll,
                             width=ur.x - ll.x,
                             height=ur.y - ll.y)
        self.design.add_label(text=label,
                              layer="text",
                              offset=ll)
