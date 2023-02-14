# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from itertools import tee
from openram import debug
from openram.sram_factory import factory
from openram.tech import drc
from .design import design
from .vector import vector
from .vector3d import vector3d


class route(design):
    """
    Object route (used by the router module)
    Add a route of minimium metal width between a set of points.
    The widths are the layer widths of the layer stack.
    (Vias are in numer of vias.)
    The wire must be completely rectilinear and the
    z-dimension of the points refers to the layers.
    The points are the center of the wire.
    This can have non-preferred direction routing.
    """

    unique_route_id = 0

    def __init__(self, obj, layer_stack, path, layer_widths=[None,1,None]):
        name = "route_{0}".format(route.unique_route_id)
        route.unique_route_id += 1
        super().__init__(name)
        debug.info(3, "create route obj {0}".format(name))

        self.obj = obj
        self.layer_stack = layer_stack
        self.layer_widths = layer_widths
        self.path = path

        self.setup_layers()
        self.create_wires()


    def setup_layers(self):
        (self.horiz_layer_name, self.via_layer, self.vert_layer_name) = self.layer_stack
        (self.horiz_layer_width, self.num_vias, self.vert_layer_width) = self.layer_widths

        if not self.vert_layer_width:
            self.vert_layer_width = drc("minwidth_{0}".format(self.vert_layer_name))
        if not self.horiz_layer_width:
            self.horiz_layer_width = drc("minwidth_{0}".format(self.horiz_layer_name))

        # offset this by 1/2 the via size
        self.c=factory.create(module_type="contact",
                              layer_stack=self.layer_stack,
                              dimensions=(self.num_vias, self.num_vias))


    def create_wires(self):
        """
        Add the wire segments of the route.
        """

        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)

        plist = list(pairwise(self.path))
        for p0,p1 in plist:
            if p0.z != p1.z: # via
                via_size = [self.num_vias]*2
                self.obj.add_via_center(self.layer_stack,vector(p0.x,p0.y),size=via_size)
            elif p0.x != p1.x and p0.y != p1.y: # diagonal!
                debug.error("Diagonal route! {}".format(self.path),-3)
            else:
                # this will draw an extra corner at the end but that is ok
                self.draw_corner_wire(p1)
                # draw the point to point wire
                self.draw_wire(p0,p1)


        # Draw the layers on the ends of the wires to ensure full width
        # connections
        self.draw_corner_wire(plist[0][0])
        self.draw_corner_wire(plist[-1][1])


    def get_layer_width(self, layer_zindex):
        """
        Return the layer width
        """
        if layer_zindex==0:
            return self.horiz_layer_width
        elif layer_zindex==1:
            return self.vert_layer_width
        else:
            debug.error("Incorrect layer zindex.",-1)

    def get_layer_name(self, layer_zindex):
        """
        Return the layer name
        """
        if layer_zindex==0:
            return self.horiz_layer_name
        elif layer_zindex==1:
            return self.vert_layer_name
        else:
            debug.error("Incorrect layer zindex.",-1)


    def draw_wire(self, p0, p1):
        """
        This draws a straight wire with layer_minwidth
        """

        layer_width = self.get_layer_width(p0.z)
        layer_name = self.get_layer_name(p0.z)

        # always route left to right or bottom to top
        if p0.z != p1.z:
            self.error("Adding a via as a wire!")
        elif p0.x < p1.x or p0.y < p1.y:
            start = p0
            end = p1
        elif p0.x > p1.x or p0.y > p1.y:
            start = p1
            end = p0
        else:
            debug.error("Neither horizontal or vertical wire.")

        # now determine the route geometry and offset
        if start.x != end.x: # horizontal
            offset = start + vector3d(0,-0.5*layer_width,0)
            height = layer_width
            width = end.x - start.x
        elif start.y != end.y: # vertical
            offset = start + vector3d(-0.5*layer_width,0,0)
            height = end.y - start.y
            width = layer_width

        self.obj.add_rect(layer=layer_name,
                          offset=vector(offset.x,offset.y),
                          width=width,
                          height=height)


    def draw_corner_wire(self, p0):
        """ This function adds the corner squares since the center
        line convention only draws to the center of the corner."""

        layer_width = self.get_layer_width(p0.z)
        layer_name = self.get_layer_name(p0.z)
        offset = vector(p0.x-0.5*layer_width,p0.y-0.5*layer_width)
        self.obj.add_rect(layer=layer_name,
                          offset=offset,
                          width=layer_width,
                          height=layer_width)


