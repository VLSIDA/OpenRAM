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
        self.gds_filename = OPTS.openram_temp + "temp.gds"
        self.pins = {}
        self.all_pins = set()
        self.blockages = []


    def route(self, vdd_name="vdd", gnd_name="gnd"):
        """ Route the given pins in the given order. """
        #debug.info(1, "Running router for {}...".format(pins))
        self.write_debug_gds(gds_name="before.gds")

        # Prepare gdsMill to find pins and blockages
        self.design.gds_write(self.gds_filename)
        self.layout = gdsMill.VlsiLayout(units=GDS["unit"])
        self.reader = gdsMill.Gds2reader(self.layout)
        self.reader.loadFromFile(self.gds_filename)

        # Find pins to be routed
        self.find_pins(vdd_name)
        self.find_pins(gnd_name)

        # Find blockages
        self.find_blockages()

        # Route vdd and gnd
        for pin_name in [vdd_name, gnd_name]:
            pins = self.pins[pin_name]
            # Create minimum spanning tree connecting all pins
            for source, target in self.get_mst_pairs(list(pins)):
                # Create the hanan graph
                hg = hanan_graph(self)
                hg.create_graph(source, target)
                # Find the shortest path from source to target
                path = hg.find_shortest_path()
                debug.check(path is not None, "Couldn't route {} to {}".format(source, target))
                # Create the path shapes on layout
                self.add_path(path)

        self.write_debug_gds(gds_name="after.gds")


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
            pin = hanan_shape(pin_name, rect, layer)
            pin_set.add(pin)
        # Add these pins to the 'pins' dict
        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)


    def find_blockages(self):
        """  """
        debug.info(1, "Finding all blockages...")

        blockages = []
        for lpp in [self.vert_lpp, self.horiz_lpp]:
            shapes = self.layout.getAllShapes(lpp)
            for boundary in shapes:
                # gdsMill boundaries are in (left, bottom, right, top) order
                # so repack and snap to the grid
                ll = vector(boundary[0], boundary[1])
                ur = vector(boundary[2], boundary[3])
                rect = [ll, ur]
                new_shape = hanan_shape("blockage{}".format(len(blockages)),
                                       rect,
                                       lpp)
                # If there is a rectangle that is the same in the pins,
                # it isn't a blockage
                if new_shape.contained_by_any(self.all_pins) or new_shape.contained_by_any(blockages):
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
        offset = self.layer_widths[0] / 2
        for blockage in blockages:
            self.blockages.append(blockage.inflated_pin(multiple=1, extra_spacing=offset))

        # Add vdd and gnd pins as blockages as well
        # NOTE: This is done to make vdd and gnd pins DRC-safe
        for pin in self.all_pins:
            self.blockages.append(pin.inflated_pin(multiple=1, extra_spacing=offset, keep_link=True))


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
                if i == j:
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


    def write_debug_gds(self, gds_name="debug_route.gds", source=None, target=None):
        """  """

        self.add_router_info(source, target)
        self.design.gds_write(gds_name)
        self.del_router_info()


    def add_router_info(self, source=None, target=None):
        """  """

        # Display the inflated blockage
        if "hg" in self.__dict__:
            for blockage in self.hg.graph_blockages:
                self.add_object_info(blockage, "blockage{}".format(self.get_zindex(blockage.lpp)))
            for node in self.hg.nodes:
                offset = (node.center.x, node.center.y)
                self.design.add_label(text="n{}".format(node.center.z),
                                      layer="text",
                                      offset=offset)
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
