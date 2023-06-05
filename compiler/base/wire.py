# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram.tech import drc
from openram.sram_factory import factory
from .wire_path import wire_path


class wire(wire_path):
    """
    Object metal wire; given the layer type
    Add a wire of minimium metal width between a set of points.
    The points should be rectilinear to control the bend points. If
    not, it will always go down first.
    The points are the center of the wire.
    The layer stack is the vertical, contact/via, and horizontal layers, respectively.
    The widen option will avoid via-to-via spacing problems for really short segments
    (added as an option so we can disable it in bus connections)
    """
    def __init__(self, obj, layer_stack, position_list, widen_short_wires=True):
        self.obj = obj
        self.layer_stack = layer_stack
        self.position_list = position_list
        self.widen_short_wires = widen_short_wires
        self.pins = [] # used for matching parm lengths
        self.switch_pos_list = []

        self.create_layout()

    def create_layout(self):
        self.setup_layers()
        self.create_rectilinear()
        self.create_vias()
        self.create_rectangles()
        # wires and wire_paths should not be offset to (0,0)

    def setup_layers(self):

        (horiz_layer, via_layer, vert_layer) = self.layer_stack
        self.via_layer_name = via_layer

        self.vert_layer_name = vert_layer
        self.vert_layer_width = drc("minwidth_{0}".format(vert_layer))

        self.horiz_layer_name = horiz_layer
        self.horiz_layer_width = drc("minwidth_{0}".format(horiz_layer))
        via_connect = factory.create(module_type="contact",
                                     layer_stack=self.layer_stack,
                                     dimensions=(1, 1))

        # This is used for short connections to avoid via-to-via spacing errors
        self.vert_layer_contact_width = max(via_connect.second_layer_width,
                                            via_connect.first_layer_width)
        self.horiz_layer_contact_width = max(via_connect.second_layer_height,
                                             via_connect.first_layer_height)

        self.node_to_node = [drc("minwidth_" + str(self.horiz_layer_name)) + via_connect.width,
                             drc("minwidth_" + str(self.horiz_layer_name)) + via_connect.height]
        self.pitch = self.compute_pitch(self.layer_stack)

    def compute_pitch(self, layer_stack):

        """
        This is contact direction independent pitch,
        i.e. we take the maximum contact dimension
        """

        # This is here for the unit tests which may not have
        # initialized the static parts of the layout class yet.
        from openram.base import layout
        layout("fake", "fake")

        (layer1, via, layer2) = layer_stack

        if layer1 == "poly" or layer1 == "active":
            try:
                contact1 = getattr(layout, layer1 + "_contact")
            except AttributeError:
                breakpoint()
        else:
            try:
                contact1 = getattr(layout, layer1 + "_via")
            except AttributeError:
                contact1 = getattr(layout, layer2 + "_via")
        max_contact = max(contact1.width, contact1.height)

        layer1_space = drc("{0}_to_{0}".format(layer1))
        layer2_space = drc("{0}_to_{0}".format(layer2))
        pitch = max_contact + max(layer1_space, layer2_space)

        return pitch

    # create a 1x1 contact
    def create_vias(self):
        """ Add a via and corner square at every corner of the path."""
        self.c=factory.create(module_type="contact",
                              layer_stack=self.layer_stack,
                              dimensions=(1, 1))
        from itertools import tee, islice
        nwise = lambda g, n=2: zip(*(islice(g, i, None) for i, g in enumerate(tee(g, n))))
        threewise = nwise(self.position_list, 3)

        for (a, offset, c) in list(threewise):
            # add a exceptions to prevent a via when we don't change directions
            if a[0] == c[0]:
                continue
            if a[1] == c[1]:
                continue
            self.obj.add_via_center(layers=self.layer_stack,
                                    offset=offset)

    def create_rectangles(self):
        """
        Create the actual rectangles on the appropriate layers
        using the position list of the corners.
        """
        pl = self.position_list  # position list
        for index in range(len(pl) - 1):
            # Horizontal wire segment
            if pl[index][0] != pl[index + 1][0]:
                line_length = pl[index + 1][0] - pl[index][0]
                # Make the wire wider to avoid via-to-via spacing problems
                # But don't make it wider if it is shorter than one via
                if self.widen_short_wires and abs(line_length) < self.pitch and abs(line_length) > self.horiz_layer_contact_width:
                    width = self.horiz_layer_contact_width
                else:
                    width = self.horiz_layer_width
                temp_offset = [pl[index][0],
                               pl[index][1] - 0.5 * width]
                # If we go in the negative direction, move the offset
                if line_length < 0:
                    temp_offset = [temp_offset[0] + line_length,
                                   temp_offset[1]]
                self.add_line(layer_name=self.horiz_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="horizontal",
                              layer_width=width)
            # Vertical wire segment
            elif pl[index][1] != pl[index + 1][1]:
                line_length = pl[index + 1][1] - pl[index][1]
                # Make the wire wider to avoid via-to-via spacing problems
                # But don't make it wider if it is shorter than one via
                if self.widen_short_wires and abs(line_length) < self.pitch and abs(line_length) > self.vert_layer_contact_width:
                    width = self.vert_layer_contact_width
                else:
                    width = self.vert_layer_width
                temp_offset = [pl[index][0] - 0.5 * width,
                               pl[index][1]]
                if line_length < 0:
                    temp_offset = [temp_offset[0],
                                   temp_offset[1] + line_length]
                self.add_line(layer_name=self.vert_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="vertical",
                              layer_width=width)

    def assert_node(self, A, B):
        """
        Check if the node movements are not big enough for the
        technology sizes.
        """
        X_diff = abs(A[0] - B[0])
        Y_diff = abs(A[1] - B[1])
        [minX, minY] = self.node_to_node
        if X_diff == 0 and Y_diff == 0:
            pass
        else:
            if X_diff == 0:
                assert Y_diff >= minY, "node" + \
                    str(A) + " and node" + str(B) + \
                    " are too close in Y. Minmum is " + str(minX)
            if Y_diff == 0:
                assert X_diff >= minX, "node" + \
                    str(A) + " and node" + str(B) + \
                    " are too close in X. Minmum is " + str(minY)
