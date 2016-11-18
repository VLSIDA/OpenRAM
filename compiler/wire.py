from tech import drc
import debug
import design
from contact import contact
from path import path


class wire(path):
    """ 
    Object metal wire; given the layer type
    Add a wire of minimium metal width between a set of points. 
    The points should be rectilinear to control the bend points. If
    not, it will always go down first.
    The points are the center of the wire.
    The layer stack is the vertical, contact/via, and horizontal layers, respectively. 
    """
    unique_wire_id = 1

    def __init__(self, layer_stack, position_list):
        name = "wire_{0}".format(wire.unique_wire_id)
        wire.unique_wire_id += 1
        design.design.__init__(self, name)
        debug.info(3, "create wire obj {0}".format(name))

        self.layer_stack = layer_stack
        self.position_list = position_list
        self.pins = [] # used for matching parm lengths
        self.switch_pos_list = []

        self.create_layout()

    def create_layout(self):
        self.setup_layers()
        self.create_rectilinear_route()
        self.create_vias()
        self.create_rectangles()
        # wires and paths should not be offset to (0,0)

    def setup_layers(self):
        (horiz_layer, via_layer, vert_layer) = self.layer_stack
        if (via_layer != None):
            self.via_layer_name = via_layer
        else:
            self.via_layer_name = None

        self.vert_layer_name = vert_layer
        self.vert_layer_width = drc["minwidth_{0}".format(vert_layer)]

        self.horiz_layer_name = horiz_layer
        self.horiz_layer_width = drc["minwidth_{0}".format(horiz_layer)]
        via_connect = contact(self.layer_stack,
                              (1, 1))
        self.node_to_node = [drc["minwidth_" + str(self.horiz_layer_name)] \
                                         + via_connect.width,
                                     drc["minwidth_" + str(self.horiz_layer_name)] \
                                         + via_connect.height]

    # create a 1x1 contact
    def create_vias(self):
        """ Add a via and corner square at every corner of the path."""
        pl = self.pairwise(self.position_list)
        from itertools import izip
        if self.via_layer_name == None:
            c_height = 0
            c_width = 0
            c = None
        else:
            c = self.c = contact(self.layer_stack, (1, 1))
            c_width = c.width
            c_height = c.height
        orient = None  # orientation toggler
        offset = [0, 0]

        for (v, w), index in izip(pl, range(len(pl))):
            if index != 0:
                if pl[index][1] == pl[index - 1][0]:
                    if v[0] != w[0]:
                        offset = [(offset[0] + (w[0] - v[0])),
                                  offset[1]]
                    else:
                        offset = [offset[0], 
                                  (offset[1] + w[1] - v[1])]
                    orient = not orient
                    continue
            if v[0] != w[0]:
                if (orient == None):
                    orient = True
                if not orient:
                    orient = not orient
                    if w[0] - v[0] < 0:
                        temp_offset = [
                            offset[0] + 0.5*c_height,
                            offset[1] - 0.5*self.horiz_layer_width]
                    else:
                        temp_offset = [offset[0] + 0.5*c_height,
                                       offset[1] - 0.5*self.horiz_layer_width]
                    self.switch_pos_list.append(temp_offset)
                    via_offset = self.switch_pos_list[-1]
                    if c:
                        self.add_inst(name="via_{0}_{1}".format(v, w),
                                      mod=c,
                                      offset=via_offset,
                                      rotate=90)
                    corner_offset = [via_offset[0] \
                                         - 0.5*(c_height + self.vert_layer_width),
                                     via_offset[1] \
                                         + 0.5*(c_width - self.horiz_layer_width)]
                    self.draw_corner_wire(corner_offset)
                offset = [(offset[0] + (w[0] - v[0])),
                          offset[1]]
            elif v[1] != w[1]:
                if (orient == None):
                    orient = False
                if orient:
                    orient = not orient
                    if -w[1] - v[1] > 0:
                        temp_offset = [offset[0] + 0.5*c_height,
                                       offset[1] - 0.5*c_width]
                    else:
                        temp_offset = [offset[0] + 0.5*c_height,
                                       offset[1] - 0.5*c_width]
                    self.switch_pos_list.append(temp_offset)
                    via_offset = self.switch_pos_list[-1]
                    if c:
                        self.add_inst(name="via{0}_{1}".format(v, w),
                                      mod=c,
                                      offset=self.switch_pos_list[-1],
                                      rotate=90)
                    corner_offset = [via_offset[0] \
                                         - 0.5*(c_height + self.vert_layer_width),
                                     via_offset[1] \
                                         + 0.5*(c_width - self.horiz_layer_width)]
                    self.draw_corner_wire(corner_offset)
                offset = [offset[0],
                          (offset[1] + w[1] - v[1])]

    def draw_corner_wire(self, offset):
        """ This function adds the corner squares since the center
        line convention only draws to the center of the corner.
        It must add squares on both layers."""
        self.add_rect(layer=self.vert_layer_name,
                      offset=offset,
                      width=self.vert_layer_width,
                      height=self.horiz_layer_width)
        self.add_rect(layer=self.horiz_layer_name,
                      offset=offset,
                      width=self.vert_layer_width,
                      height=self.horiz_layer_width)

    def create_rectangles(self):
        """ Create the actual rectangles on teh appropriate layers
        using the position list of the corners. """
        offset = [0, 0]
        # FIXME: This is not a good max/min value
        xval = [1000000, -1000000]
        yval = [1000000, -1000000]
        pl = self.position_list  # position list
        for index in range(len(pl) - 1):
            temp_offset = offset
            if temp_offset[0] < xval[0]:
                xval[0] = temp_offset[0]
            if temp_offset[0] > xval[1]:
                xval[1] = temp_offset[0]
            if temp_offset[1] < yval[0]:
                yval[0] = temp_offset[1]
            if temp_offset[1] > yval[1]:
                yval[1] = temp_offset[1]
            if pl[index][0] != pl[index + 1][0]:
                line_length = pl[index + 1][0] - pl[index][0]
                temp_offset = [temp_offset[0],
                               temp_offset[1] - 0.5*self.horiz_layer_width]
                if line_length < 0:
                    temp_offset = [temp_offset[0] + line_length,
                                   temp_offset[1]]
                self.add_line(layer_name=self.horiz_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="horizontal")
                offset = [offset[0] + line_length, offset[1]]
            elif pl[index][1] != pl[index + 1][1]:
                line_length = pl[index + 1][1] - pl[index][1]
                temp_offset = [temp_offset[0] - 0.5 * self.vert_layer_width,
                               temp_offset[1]]
                if line_length < 0:
                    temp_offset = [temp_offset[0],
                                   temp_offset[1] + line_length]
                self.add_line(layer_name=self.vert_layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="vertical")
                offset = [offset[0],
                          offset[1] + line_length]
        self.width = abs(xval[0] - xval[1])
        self.height = abs(yval[0] - yval[1])
        if self.via_layer_name != None:
            self.height += self.c.width
        else:
            self.height += self.vert_layer_width

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
