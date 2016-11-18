from tech import drc
from tech import layer as techlayer
import debug
import design
from vector import vector

class path(design.design):
    """
    Object metal path; given the layer type
    Add a path of minimium metal width between a set of points. 
    The points should be rectilinear to control the bend points. If
    not, it will always go down first. The points are the center of the path.
    If width is not given, it uses minimum layer width.
    """

    unique_path_id = 1

    def __init__(self, layer, position_list, width=None):
        name = "path_{0}".format(path.unique_path_id)
        path.unique_path_id += 1
        design.design.__init__(self, name)
        debug.info(3, "create path obj {0}".format(name))

        self.name = name
        self.layer_name = layer
        self.layer_id = techlayer[layer]
        if width==None:
            self.layer_width = drc["minwidth_{0}".format(layer)]
        else:
            self.layer_width = width
        self.position_list = position_list
        self.pins = [] # used for matching parm lengths
        self.switch_pos_list = []
        self.create_layout()


    def create_layout(self):
        self.create_rectilinear_route()
        self.connect_corner()
        self.create_rectangles()
        # wires and paths should not be offset to (0,0)

    def create_rectilinear_route(self):
        """ Add intermediate nodes if it isn't rectilinear. Also skip
        repeated nodes. Also, convert to vector if the aren't."""
        pl = self.position_list

        self.position_list = []
        for index in range(len(pl) - 1):
            if pl[index] != pl[index + 1]:
                self.position_list.append(vector(pl[index]))
            if (pl[index][0] != pl[index + 1][0]) and (pl[index][1] != pl[index + 1][1]):
                self.position_list.append(vector(pl[index][0], pl[index + 1][1]))
        self.position_list.append(vector(pl[-1]))



    def pairwise(self, iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        from itertools import tee, izip
        a, b = tee(iterable)
        next(b, None)
        temp = []
        for v in izip(a, b):
            temp.append(list(v))
        return temp

    def connect_corner(self):
        """ Add a corner square at every corner of the path."""
        pl = self.pairwise(self.position_list)
        from itertools import izip
        orient = None  # orientation toggler
        offset = [0, 0]

        for (v, w), index in izip(pl, range(len(pl))):
            if index != 0:
                if pl[index][1] == pl[index - 1][0]:
                    if v[0] != w[0]:
                        offset = [(offset[0] + (w[0] - v[0])), offset[1]]
                    else:
                        offset = [offset[0], (offset[1] + w[1] - v[1])]
                    orient = not orient
                    continue
            if v[0] != w[0]:
                if (orient == None):
                    orient = True
                if not orient:
                    orient = not orient
                    temp_offset = offset
                    self.switch_pos_list.append(temp_offset)
                    via_offset = self.switch_pos_list[-1]
                    corner_offset = [via_offset[0] - 0.5 * self.layer_width,
                                     via_offset[1] - 0.5 * self.layer_width]
                    self.draw_corner_wire(corner_offset)
                offset = [(offset[0] + (w[0] - v[0])), offset[1]]
            elif v[1] != w[1]:
                if (orient == None):
                    orient = False
                if orient:
                    orient = not orient
                    temp_offset = offset
                    self.switch_pos_list.append(temp_offset)
                    via_offset = self.switch_pos_list[-1]
                    corner_offset = [via_offset[0] - 0.5 * self.layer_width,
                                     via_offset[1] - 0.5 * self.layer_width]
                    self.draw_corner_wire(corner_offset)
                offset = [offset[0], (offset[1] + w[1] - v[1])]

    def draw_corner_wire(self, offset):
        """ This function adds the corner squares since the center
        line convention only draws to the center of the corner."""
        self.add_rect(layer=self.layer_name,
                      offset=offset,
                      width=self.layer_width,
                      height=self.layer_width)

    def create_rectangles(self):
        """ Create the actual rectangles on teh appropriate layers
        using the position list of the corners. """
        offset = [0, 0]
        # FIXME: These should not be hard coded limits.
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
                               temp_offset[1] - 0.5 * self.layer_width]
                if line_length < 0:
                    temp_offset = [temp_offset[0] + line_length,
                                   temp_offset[1]]
                self.add_line(layer_name=self.layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="horizontal")
                offset = [offset[0] + line_length,
                          offset[1]]
            elif pl[index][1] != pl[index + 1][1]:
                line_length = pl[index + 1][1] - pl[index][1]
                temp_offset = [temp_offset[0] - 0.5 * self.layer_width,
                               temp_offset[1]]
                if line_length < 0:
                    temp_offset = [temp_offset[0],
                                   temp_offset[1] + line_length]
                self.add_line(layer_name=self.layer_name,
                              length=abs(line_length),
                              offset=temp_offset,
                              orientation="vertical")

                offset = [offset[0],
                          offset[1] + line_length]
        self.width = abs(xval[0] - xval[1])
        self.height = abs(yval[0] - yval[1])


    def add_line(self, layer_name, length, offset, orientation):
        """
        straight line object with layer_minwidth 
        (orientation: "vertical" or "horizontal") default is vertical
        """

        layer_width = drc["minwidth_{0}".format(layer_name)]
        width = layer_width
        height = length 

        if orientation == "horizontal":
            width = length
            height = layer_width
        self.add_rect(layer=layer_name,
                      offset=offset,
                      width=width,
                      height=height)
