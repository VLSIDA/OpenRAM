# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.pin_layout import pin_layout
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram.gdsMill import gdsMill
from openram.tech import GDS
from openram.tech import layer as tech_layer
from openram import OPTS
from .router_tech import router_tech
from .hanan_graph import hanan_graph


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
        vdds.sort()
        pin_iter = iter(vdds)
        vdd_0 = next(pin_iter)
        next(pin_iter)
        next(pin_iter)
        next(pin_iter)
        next(pin_iter)
        next(pin_iter)
        next(pin_iter)
        vdd_1 = next(pin_iter)
        self.hg = hanan_graph(self)
        self.hg.create_graph(vdd_0, vdd_1)

        # Find the shortest path from source to target
        path = self.hg.find_shortest_path(vdd_0, vdd_1)

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
            pin = pin_layout(pin_name, rect, layer)
            pin_set.add(pin)
        # Add these pins to the 'pins' dict
        self.pins[pin_name] = pin_set
        self.all_pins.update(pin_set)


    def find_blockages(self):
        """  """
        debug.info(1, "Finding all blockages...")

        for lpp in [self.vert_lpp, self.horiz_lpp]:
            shapes = self.layout.getAllShapes(lpp)
            for boundary in shapes:
                # gdsMill boundaries are in (left, bottom, right, top) order
                # so repack and snap to the grid
                ll = vector(boundary[0], boundary[1])
                ur = vector(boundary[2], boundary[3])
                rect = [ll, ur]
                new_shape = pin_layout("blockage{}".format(len(self.blockages)),
                                       rect,
                                       lpp)
                # If there is a rectangle that is the same in the pins,
                # it isn't a blockage
                if new_shape not in self.all_pins and not self.pin_contains(new_shape):
                    new_shape = new_shape.inflated_pin(multiple=1)
                    self.blockages.append(new_shape)


    def pin_contains(self, shape):
        """
        Return if this pin contains another pin or is contained by another pin.
        """

        for pin in self.all_pins:
            if pin.contains(shape) or shape.contains(pin):
                return True
        return False


    def add_path(self, path):
        """ Add the route path to the layout. """

        coordinates = [x.center for x in path]
        self.design.add_route(layers=self.layers,
                              coordinates=coordinates,
                              layer_widths=self.layer_widths)


    def write_debug_gds(self, gds_name="debug_route.gds", source=None, target=None):
        """  """

        self.add_router_info(source, target)
        self.design.gds_write(gds_name)
        self.del_router_info()


    def add_router_info(self, source=None, target=None):
        """  """

        # Display the inflated blockage
        if "nav" in self.__dict__:
            for blockage in self.hg.graph_blockages:
                self.add_object_info(blockage, "blockage")
            for node in self.hg.nodes:
                offset = (node.center.x, node.center.y)
                self.design.add_label(text="O",
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
