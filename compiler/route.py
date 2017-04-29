from tech import drc
import debug
import design
from contact import contact
from itertools import tee
from vector import vector
from vector3d import vector3d

class route(design.design):
    """ 
    Object route
    Add a route of minimium metal width between a set of points.
    The wire must be completely rectilinear and the 
    z-dimension of the points refers to the layers (plus via)
    The points are the center of the wire.
    This can have non-preferred direction routing.
    """
    unique_route_id = 1

    def __init__(self, layer_stack, path):
        name = "route_{0}".format(route.unique_route_id)
        route.unique_route_id += 1
        design.design.__init__(self, name)
        debug.info(3, "create route obj {0}".format(name))

        self.layer_stack = layer_stack
        self.path = path

        self.setup_layers()
        self.create_wires()


    def setup_layers(self):
        (horiz_layer, via_layer, vert_layer) = self.layer_stack
        self.via_layer_name = via_layer

        self.vert_layer_name = vert_layer
        self.vert_layer_width = drc["minwidth_{0}".format(vert_layer)]

        self.horiz_layer_name = horiz_layer
        self.horiz_layer_width = drc["minwidth_{0}".format(horiz_layer)]
        # offset this by 1/2 the via size
        self.c=contact(self.layer_stack, (1, 1))


    def create_wires(self):
        """ 
        Add the wire segments of the route.
        """

        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)
        
        plist = pairwise(self.path)
        for p0,p1 in plist:
            if p0.z != p1.z: # via
                # offset if not rotated
                #via_offset = vector(p0.x+0.5*self.c.width,p0.y+0.5*self.c.height)
                # offset if rotated
                via_offset = vector(p0.x+0.5*self.c.height,p0.y-0.5*self.c.width)
                self.add_via(self.layer_stack,via_offset,rotate=90)
            elif p0.x != p1.x and p0.y != p1.y: # diagonal!
                debug.error("Non-changing direction!")
            else:
                # this will draw an extra corner at the end but that is ok
                self.draw_corner_wire(p1)
                # draw the point to point wire
                self.draw_wire(p0,p1)
                
        

    def draw_wire(self, p0, p1):
        """
        This draws a straight wire with layer_minwidth 
        """
        layer_name = self.layer_stack[2*p0.z]
        layer_width = drc["minwidth_{0}".format(layer_name)]

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

        self.add_rect(layer=layer_name,
                      offset=offset,
                      width=width,
                      height=height)
        
    
    def draw_corner_wire(self, p0):
        """ This function adds the corner squares since the center
        line convention only draws to the center of the corner."""

        layer_name = self.layer_stack[2*p0.z]
        layer_width = drc["minwidth_{0}".format(layer_name)]
        offset = vector(p0.x-0.5*layer_width,p0.y-0.5*layer_width)
        self.add_rect(layer=layer_name,
                      offset=offset,
                      width=layer_width,
                      height=layer_width)


