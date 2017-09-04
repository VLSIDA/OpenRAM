from tech import drc
from tech import layer as techlayer
import debug
from vector import vector

class path():
    """
    Object metal path; given the layer type
    Add a path of minimium metal width between a set of points. 
    The points should be rectilinear to control the bend points. If
    not, it will always go down first. The points are the center of the path.
    If width is not given, it uses minimum layer width.
    """
    def __init__(self, obj, layer, position_list, width=None):
        self.obj = obj
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

    def connect_corner(self):
        """ Add a corner square at every corner of the path."""
        from itertools import tee,islice
        nwise = lambda g,n=2: zip(*(islice(g,i,None) for i,g in enumerate(tee(g,n))))
        threewise=nwise(self.position_list,3)

        for (a, offset, c) in list(threewise):
            # add a exceptions to prevent a corner when we retrace back in the same direction
            if a[0] == c[0]:
                continue
            if a[1] == c[1]:
                continue
            corner_offset = [offset[0] - 0.5 * self.layer_width,
                             offset[1] - 0.5 * self.layer_width]
            self.draw_corner_wire(corner_offset)


    def draw_corner_wire(self, offset):
        """ This function adds the corner squares since the center
        line convention only draws to the center of the corner."""
        self.obj.add_rect(layer=self.layer_name,
                          offset=offset,
                          width=self.layer_width,
                          height=self.layer_width)

    def create_rectangles(self):
        """ Create the actual rectangles on teh appropriate layers
        using the position list of the corners. """
        pl = self.position_list  # position list
        for index in range(len(pl) - 1):

            # if we have x motion
            if pl[index][0] != pl[index + 1][0]:
                line_length = pl[index + 1][0] - pl[index][0]
                offset = [pl[index][0],
                          pl[index][1] - 0.5 * self.layer_width]
                if line_length < 0:
                    offset = [offset[0] + line_length,
                              offset[1]]
                self.add_line(layer_name=self.layer_name,
                              length=abs(line_length),
                              offset=offset,
                              orientation="horizontal")
            # if we have y motion
            elif pl[index][1] != pl[index + 1][1]:
                line_length = pl[index + 1][1] - pl[index][1]
                offset = [pl[index][0] - 0.5 * self.layer_width,
                          pl[index][1]]
                if line_length < 0:
                    offset = [offset[0],
                              offset[1] + line_length]
                self.add_line(layer_name=self.layer_name,
                              length=abs(line_length),
                              offset=offset,
                              orientation="vertical")

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
        self.obj.add_rect(layer=layer_name,
                          offset=offset,
                          width=width,
                          height=height)
