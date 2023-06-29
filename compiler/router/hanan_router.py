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

        # Create the hanan graph
        # TODO: Remove this part later and route all pins
        vdds = list(self.pins["vdd"])
        for pin in vdds:
            ll, ur = pin.rect
            if ll.x == -11 and ll.y == -8.055:
                vdd_0 = pin
            if ll.x == 10.557500000000001 and ll.y == 11.22:
                vdd_1 = pin
        #vdds.sort()
        #pin_iter = iter(vdds)
        #vdd_0 = next(pin_iter)
        #next(pin_iter)
        #next(pin_iter)
        #next(pin_iter)
        #next(pin_iter)
        #next(pin_iter)
        #next(pin_iter)
        #vdd_1 = next(pin_iter)
        self.hg = hanan_graph(self)
        self.hg.create_graph(vdd_0, vdd_1)

        # Find the shortest path from source to target
        path = self.hg.find_shortest_path()

        # Create the path shapes on layout
        if path:
            self.add_path(path)
            debug.info(0, "Successfully routed")
        else:
            debug.info(0, "No path was found!")

        self.write_debug_gds(gds_name="after.gds", source=vdd_0, target=vdd_1)


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
