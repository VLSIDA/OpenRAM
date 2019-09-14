# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from tech import drc
import debug
from wire_path import wire_path
from sram_factory import factory

class wire(wire_path):
    """ 
    Object metal wire; given the layer type
    Add a wire of minimium metal width between a set of points. 
    The points should be rectilinear to control the bend points. If
    not, it will always go down first.
    The points are the center of the wire.
    The layer stack is the vertical, contact/via, and horizontal layers, respectively. 
    """
    def __init__(self, obj, layer_stack, position_list):
        self.obj = obj
        self.layer_stack = layer_stack
        self.position_list = position_list
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
        self.node_to_node = [drc("minwidth_" + str(self.horiz_layer_name)) + via_connect.width,
                             drc("minwidth_" + str(self.horiz_layer_name)) + via_connect.height]

    # create a 1x1 contact
    def create_vias(self):
        """ Add a via and corner square at every corner of the path."""
        self.c=factory.create(module_type="contact",
                              layer_stack=self.layer_stack,
                              dimensions=(1, 1))
        c_width = self.c.width
        c_height = self.c.height
        
        from itertools import tee,islice
        nwise = lambda g,n=2: zip(*(islice(g,i,None) for i,g in enumerate(tee(g,n))))
        threewise=nwise(self.position_list,3)

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
            if pl[index][0] != pl[index + 1][0]:
                line_length = pl[index + 1][0] - pl[index][0]
                temp_offset = [pl[index][0],
                               pl[index][1] - 0.5*self.horiz_layer_width]
                if line_length < 0:
                    temp_offset = [temp_offset[0] + line_length,
                                   temp_offset[1]]
                self.add_line(layer_name=self.horiz_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="horizontal",
                              layer_width=self.horiz_layer_width)
            elif pl[index][1] != pl[index + 1][1]:
                line_length = pl[index + 1][1] - pl[index][1]
                temp_offset = [pl[index][0] - 0.5 * self.vert_layer_width,
                               pl[index][1]]
                if line_length < 0:
                    temp_offset = [temp_offset[0],
                                   temp_offset[1] + line_length]
                self.add_line(layer_name=self.vert_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="vertical",
                              layer_width=self.vert_layer_width)

    def assert_node(self, A, B):
        """ Check if the node movements are not big enough for the
        technology sizes."""
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
