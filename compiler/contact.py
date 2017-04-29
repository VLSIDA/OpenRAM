import design
import debug
from tech import drc
from vector import vector

class contact(design.design):
    """
    Object for a contact shape with its conductor enclosures.
    Creates a contact array minimum active or poly enclosure and metal1 enclosure.
    This class has enclosure on multiple sides of the contact whereas a via may
    have extension on two or four sides.
    """
    def __init__(self, layer_stack, dimensions=[1,1]):
        name = "{0}_{1}_{2}_{3}x{4}".format(layer_stack[0],
                                            layer_stack[1],
                                            layer_stack[2],
                                            dimensions[0],
                                            dimensions[1])
        design.design.__init__(self, name)
        debug.info(3, "create contact object {0}".format(name))

        self.layer_stack = layer_stack
        self.dimensions = dimensions
        self.offset = vector(0,0)
        self.pins = [] # used for matching parm lengths
        self.create_layout()

    def create_layout(self):
        self.setup_layers()
        self.setup_layout_constants()
        self.create_contact_array()
        self.create_first_layer_enclosure()
        self.create_second_layer_enclosure()
        self.offset_all_coordinates()

    def offset_all_coordinates(self):
        coordinate = self.find_lowest_coords()
        self.offset_attributes(coordinate)
        self.translate(coordinate)

        self.height = max(obj.offset.y + obj.height for obj in self.objs)
        self.width = max(obj.offset.x + obj.width for obj in self.objs)

    def setup_layers(self):
        (first_layer, via_layer, second_layer) = self.layer_stack
        self.first_layer_name = first_layer
        self.via_layer_name = via_layer
        self.second_layer_name = second_layer

    def setup_layout_constants(self):
        self.contact_width = drc["minwidth_{0}". format(self.via_layer_name)]
        self.contact_to_contact = drc["{0}_to_{0}".format(self.via_layer_name)]
        self.contact_pitch = self.contact_width + self.contact_to_contact
        self.contact_array_width = self.contact_width \
            + (self.dimensions[0] - 1) * self.contact_pitch
        self.contact_array_height = self.contact_width \
            + (self.dimensions[1] - 1) * self.contact_pitch

        # FIME break this up
        self.first_layer_horizontal_enclosure = max((drc["minwidth_{0}".format(self.first_layer_name)] - self.contact_array_width) / 2,
                                                    drc["{0}_enclosure_{1}".format(self.first_layer_name, self.via_layer_name)])
        self.first_layer_vertical_enclosure = max((drc["minarea_{0}".format(self.first_layer_name)]
                                                   / (self.contact_array_width + 2 * self.first_layer_horizontal_enclosure) - self.contact_array_height) / 2,
                                                  (drc["minheight_{0}".format(
                                                      self.first_layer_name)] - self.contact_array_height) / 2,
                                                  drc["{0}_extend_{1}".format(self.first_layer_name, self.via_layer_name)])

        self.second_layer_horizontal_enclosure = max((drc["minwidth_{0}".format(self.second_layer_name)] - self.contact_array_width) / 2,
                                                    drc["{0}_enclosure_{1}".format(self.second_layer_name, self.via_layer_name)])
        self.second_layer_vertical_enclosure = max((drc["minarea_{0}".format(self.second_layer_name)]
                                                   / (self.contact_array_width + 2 * self.second_layer_horizontal_enclosure) - self.contact_array_height) / 2,
                                                  (drc["minheight_{0}".format(
                                                      self.second_layer_name)] - self.contact_array_height) / 2,
                                                  drc["{0}_extend_{1}".format(self.second_layer_name, self.via_layer_name)])

    def create_contact_array(self):
        """ Create the contact array at the origin"""
        self.via_layer_position = vector(0, 0)
        for i in range(self.dimensions[1]):
            offset = [0, 0 + self.contact_pitch * i]
            for j in range(self.dimensions[0]):
                self.add_rect(layer=self.via_layer_name,
                              offset=offset,
                              width=self.contact_width,
                              height=self.contact_width)
                offset = [offset[0] + self.contact_pitch, offset[1]]

    def create_first_layer_enclosure(self):
        width = self.first_layer_width = self.contact_array_width \
            + 2 * self.first_layer_horizontal_enclosure
        height = self.first_layer_height = self.contact_array_height \
            + 2 * self.first_layer_vertical_enclosure
        offset = self.first_layer_position = vector(-self.first_layer_horizontal_enclosure,
                                                     -self.first_layer_vertical_enclosure)
        self.add_rect(layer=self.first_layer_name,
                      offset=offset,
                      width=width,
                      height=height)

    def create_second_layer_enclosure(self):
        width = self.second_layer_width = self.contact_array_width \
            + 2 * self.second_layer_horizontal_enclosure
        height = self.second_layer_height = self.contact_array_height \
            + 2 * self.second_layer_vertical_enclosure
        offset = self.second_layer_position = vector(-self.second_layer_horizontal_enclosure, 
                                                     -self.second_layer_vertical_enclosure)
        self.add_rect(layer=self.second_layer_name,
                      offset=offset,
                      width=width,
                      height=height)
