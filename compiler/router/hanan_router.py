# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.gdsMill import gdsMill
from openram.tech import GDS
from openram.tech import layer as tech_layer
from openram import OPTS
from .router_tech import router_tech
from .hanan_graph import hanan_graph
from .hanan_shape import hanan_shape


class hanan_router(router_tech):
    """
    This is the router class that implements Hanan graph routing algorithm.
    """

    def __init__(self, layers, design, bbox=None, pin_type=None):

        router_tech.__init__(self, layers, route_track_width=1)

        self.layers = layers
        self.design = design
        self.pin_type = pin_type
        self.gds_filename = OPTS.openram_temp + "temp.gds"
        self.pins = {}
        self.all_pins = set()
        self.blockages = []
        self.new_pins = {}
        self.fake_pins = []

        # Set the offset here
        self.offset = self.layer_widths[0] / 2


    def route(self, vdd_name="vdd", gnd_name="gnd"):
        """ Route the given pins in the given order. """
        #debug.info(1, "Running router for {}...".format(pins))
        self.write_debug_gds(gds_name="before.gds")

        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

        # Prepare gdsMill to find pins and blockages
        self.prepare_gds_reader()

        # Find pins to be routed
        self.find_pins(vdd_name)
        self.find_pins(gnd_name)

        # Find blockages
        self.find_blockages()

        # Add side pins
        if self.pin_type in ["top", "bottom", "right", "left"]:
            self.add_side_pin(vdd_name)
            self.add_side_pin(gnd_name)
        elif self.pin_type == "ring":
            self.add_ring_pin(vdd_name)
            self.add_ring_pin(gnd_name)
        else:
            debug.warning("Side supply pins aren't created.")

        self.write_debug_gds(gds_name="after.gds")

        # Add vdd and gnd pins as blockages as well
        # NOTE: This is done to make vdd and gnd pins DRC-safe
        for pin in self.all_pins:
            self.blockages.append(pin.inflated_pin(multiple=1, extra_spacing=self.offset, keep_link=True))

        # Route vdd and gnd
        for pin_name in [vdd_name, gnd_name]:
            pins = self.pins[pin_name]
            # Create minimum spanning tree connecting all pins
            for source, target in self.get_mst_pairs(list(pins)):
                # Create the Hanan graph
                hg = hanan_graph(self)
                hg.create_graph(source, target)
                # Find the shortest path from source to target
                path = hg.find_shortest_path()
                debug.check(path is not None, "Couldn't route from {} to {}".format(source, target))
                # Create the path shapes on layout
                self.add_path(path)
                # Find the recently added shapes
                self.prepare_gds_reader()
                self.find_blockages(pin_name)

        self.write_debug_gds(gds_name="after.gds")


    def prepare_gds_reader(self):
        """  """

        self.design.gds_write(self.gds_filename)
        self.layout = gdsMill.VlsiLayout(units=GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(self.gds_filename)


    def find_pins(self, pin_name):
        """  """
        debug.info(1, "Finding all pins for {}".format(pin_name))

        shape_list = self.layout.getAllPinShapes(str(pin_name))
        pin_set = set()
        for shape in shape_list:
            layer, boundary = shape
            # gdsMill boundaries are in (left, bottom, right, top) order
            # so repack and snap to the grid
            ll = vector(boundary[0], boundary[1])
            ur = vector(boundary[2], boundary[3])
            rect = [ll, ur]
            new_pin = hanan_shape(pin_name, rect, layer)
            # Skip this pin if it's contained by another pin of the same type
            if new_pin.contained_by_any(pin_set):
                continue
            # Remove any previous pin of the same type contained by this new pin
            for pin in list(pin_set):
                if new_pin.contains(pin):
                    pin_set.remove(pin)
                elif new_pin.aligns(pin):
                    new_pin.bbox([pin])
                    pin_set.remove(pin)
            pin_set.add(new_pin)
        # Add these pins to the 'pins' dict
        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)


    def find_blockages(self, shape_name=None):
        """  """
        debug.info(1, "Finding blockages...")

        prev_blockages = self.blockages[:]

        blockages = []
        for lpp in [self.vert_lpp, self.horiz_lpp]:
            shapes = self.layout.getAllShapes(lpp)
            for boundary in shapes:
                # gdsMill boundaries are in (left, bottom, right, top) order
                # so repack and snap to the grid
                ll = vector(boundary[0], boundary[1])
                ur = vector(boundary[2], boundary[3])
                rect = [ll, ur]
                if shape_name is None:
                    name = "blockage{}".format(len(blockages))
                else:
                    name = shape_name
                new_shape = hanan_shape(name, rect, lpp)
                # If there is a rectangle that is the same in the pins,
                # it isn't a blockage
                # Also ignore the new pins
                if new_shape.contained_by_any(self.all_pins) or \
                   new_shape.contained_by_any(prev_blockages) or \
                   new_shape.contained_by_any(blockages):
                    continue
                # Remove blockages contained by this new blockage
                for i in range(len(blockages) - 1, -1, -1):
                    blockage = blockages[i]
                    # Remove the previous blockage contained by this new
                    # blockage
                    if new_shape.contains(blockage):
                        blockages.remove(blockage)
                    # Merge the previous blockage into this new blockage if
                    # they are aligning
                    elif new_shape.aligns(blockage):
                        new_shape.bbox([blockage])
                        blockages.remove(blockage)
                blockages.append(new_shape)

        # Inflate the shapes to prevent DRC errors
        for blockage in blockages:
            self.blockages.append(blockage.inflated_pin(multiple=1,
                                                        extra_spacing=self.offset,
                                                        keep_link=shape_name is not None))
            # Remove blockages contained by this new blockage
            for i in range(len(prev_blockages) - 1, -1, -1):
                prev_blockage = prev_blockages[i]
                # Remove the previous blockage contained by this new
                # blockage
                if blockage.contains(prev_blockage):
                    prev_blockages.remove(prev_blockage)
                    self.blockages.remove(prev_blockage)
                # Merge the previous blockage into this new blockage if
                # they are aligning
                elif blockage.aligns(prev_blockage):
                    blockage.bbox([prev_blockage])
                    prev_blockages.remove(prev_blockage)
                    self.blockages.remove(prev_blockage)


    def add_side_pin(self, pin_name, side, width=3, num_connects=4, bbox=None):
        """ Add supply pin to one side of the layout. """

        vertical = side in ["left", "right"]
        inner = pin_name == self.gnd_name

        if bbox is None:
            bbox = self.design.get_bbox()
        ll, ur = bbox

        # Calculate wires' wideness
        wideness = self.track_wire * width + self.track_space * (width - 1)

        # Calculate the offset for the inner ring
        if inner:
            margin = wideness * 2
        else:
            margin = 0

        if side == "top":
            offset = vector(ll.x + margin, ur.y - wideness - margin)
        elif side == "bottom":
            offset = vector(ll.x + margin, ll.y + margin)
        elif side == "left":
            offset = vector(ll.x + margin, ll.y + margin)
        elif side == "right":
            offset = vector(ur.x - wideness - margin, ll.y + margin)

        shape = ur - ll

        if vertical:
            shape_width = wideness
            shape_height = shape.y
        else:
            shape_width = shape.x
            shape_height = wideness

        if inner:
            if vertical:
                shape_height -= margin * 2
            else:
                shape_width -= margin * 2

        # Add this new pin
        layer = self.get_layer(int(vertical))
        pin = self.design.add_layout_pin(text=pin_name,
                                         layer=layer,
                                         offset=offset,
                                         width=shape_width,
                                         height=shape_height)
        # Add fake pins on this new pin evenly
        fake_pins = []
        if vertical:
            space = (shape_height - (2 * wideness) - num_connects * self.track_wire) / (num_connects + 1)
            start_offset = vector(offset.x, offset.y + wideness)
        else:
            space = (shape_width - (2 * wideness) - num_connects * self.track_wire) / (num_connects + 1)
            start_offset = vector(offset.x + wideness, offset.y)
        for i in range(1, num_connects + 1):
            if vertical:
                offset = vector(start_offset.x, start_offset.y + i * (space + self.track_wire))
                ll = vector(offset.x, offset.y - self.track_wire)
                ur = vector(offset.x + wideness, offset.y)
            else:
                offset = vector(start_offset.x + i * (space + self.track_wire), start_offset.y)
                ll = vector(offset.x - self.track_wire, offset.y)
                ur = vector(offset.x, offset.y + wideness)
            rect = [ll, ur]
            fake_pin = hanan_shape(name=pin_name,
                                   rect=rect,
                                   layer_name_pp=layer)
            fake_pins.append(fake_pin)
        return pin, fake_pins


    def add_ring_pin(self, pin_name, width=3, num_connects=4):
        """ Add suply ring to the layout. """

        bbox = self.design.get_bbox()

        # Add side pins
        new_pins = []
        for side in ["top", "bottom", "right", "left"]:
            new_shape, fake_pins = self.add_side_pin(pin_name, side, width, num_connects, bbox)
            ll, ur = new_shape.rect
            rect = [ll, ur]
            layer = self.get_layer(side in ["left", "right"])
            new_pin = hanan_shape(name=pin_name,
                                  rect=rect,
                                  layer_name_pp=layer)
            new_pins.append(new_pin)
            self.pins[pin_name].update(fake_pins)
            self.fake_pins.extend(fake_pins)

        # Add vias to the corners
        shift = self.track_wire + self.track_space
        half_wide = self.track_wire / 2
        for i in range(4):
            ll, ur = new_pins[i].rect
            if i % 2:
                top_left = vector(ur.x - (width - 1) * shift - half_wide, ll.y + (width - 1) * shift + half_wide)
            else:
                top_left = vector(ll.x + half_wide, ur.y - half_wide)
            for j in range(width):
                for k in range(width):
                    offset = vector(top_left.x + j * shift, top_left.y - k * shift)
                    self.design.add_via_center(layers=self.layers,
                                               offset=offset)

        # Save side pins for routing
        self.new_pins[pin_name] = new_pins
        for pin in new_pins:
            self.blockages.append(pin.inflated_pin(multiple=1,
                                                   extra_spacing=self.offset,
                                                   keep_link=True))


    def get_mst_pairs(self, pins):
        """
        Return the pin pairs from the minimum spanning tree in a graph that
        connects all pins together.
        """

        pin_count = len(pins)

        # Create an adjacency matrix that connects all pins
        edges = [[0] * pin_count for i in range(pin_count)]
        for i in range(pin_count):
            for j in range(pin_count):
                # Skip if they're the same pin
                if i == j:
                    continue
                # Skip if both pins are fake
                if pins[i] in self.fake_pins and pins[j] in self.fake_pins:
                    continue
                edges[i][j] = pins[i].distance(pins[j])

        pin_connected = [False] * pin_count
        pin_connected[0] = True

        # Add the minimum cost edge in each iteration (Prim's)
        mst_pairs = []
        for i in range(pin_count - 1):
            min_cost = float("inf")
            s = 0
            t = 0
            # Iterate over already connected pins
            for m in range(pin_count):
                # Skip if not connected
                if not pin_connected[m]:
                    continue
                # Iterate over this pin's neighbors
                for n in range(pin_count):
                    # Skip if already connected or isn't a neighbor
                    if pin_connected[n] or edges[m][n] == 0:
                        continue
                    # Choose this edge if it's better the the current one
                    if edges[m][n] < min_cost:
                        min_cost = edges[m][n]
                        s = m
                        t = n
            pin_connected[t] = True
            mst_pairs.append((pins[s], pins[t]))

        return mst_pairs


    def add_path(self, path):
        """ Add the route path to the layout. """

        coordinates = self.prepare_path(path)
        self.design.add_route(layers=self.layers,
                              coordinates=coordinates,
                              layer_widths=self.layer_widths)


    def prepare_path(self, path):
        """
        Remove unnecessary nodes on the path to reduce the number of shapes in
        the layout.
        """

        last_added = path[0]
        coordinates = [path[0].center]
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
                last_added = candidate
                coordinates.append(candidate.center)
                direction = current_direction
                candidate = node
        if candidate.center not in coordinates:
            coordinates.append(candidate.center)
        return coordinates


    def get_new_pins(self, name):
        """  """

        return self.new_pins[name]


    def write_debug_gds(self, gds_name="debug_route.gds", hg=None, source=None, target=None):
        """  """

        self.add_router_info(hg, source, target)
        self.design.gds_write(gds_name)
        self.del_router_info()


    def add_router_info(self, hg=None, source=None, target=None):
        """  """

        # Display the inflated blockage
        if hg:
            for blockage in self.blockages:
                if blockage in hg.graph_blockages:
                    self.add_object_info(blockage, "blockage{}++[{}]".format(self.get_zindex(blockage.lpp), blockage.name))
                else:
                    self.add_object_info(blockage, "blockage{}[{}]".format(self.get_zindex(blockage.lpp), blockage.name))
            for node in hg.nodes:
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
        """  """

        lpp = tech_layer["text"]
        self.design.objs = [x for x in self.design.objs if x.lpp != lpp]


    def add_object_info(self, obj, label):
        """  """

        ll, ur = obj.rect
        self.design.add_rect(layer="text",
                             offset=ll,
                             width=ur.x - ll.x,
                             height=ur.y - ll.y)
        self.design.add_label(text=label,
                              layer="text",
                              offset=ll)
