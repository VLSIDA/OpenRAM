import design
import debug
import utils
from tech import drc
from vector import vector


class contact(design.design):
    """
    Object for a contact shape with its conductor enclosures.
    Creates a contact array minimum active or poly enclosure and metal1 enclosure.
    This class has enclosure on multiple sides of the contact whereas a via may
    have extension on two or four sides.
    The well/implant_type is an option to add a select/implant layer enclosing the contact. This is
    necessary to import layouts into Magic which requires the select to be in the same GDS
    hierarchy as the contact.
    """
    def __init__(self, layer_stack, dimensions=[1,1], implant_type=None, well_type=None):
        if implant_type or well_type:
            name = "{0}_{1}_{2}_{3}x{4}_{5}{6}".format(layer_stack[0],
                                                       layer_stack[1],
                                                       layer_stack[2],
                                                       dimensions[0],
                                                       dimensions[1],
                                                       implant_type,
                                                       well_type)
        else:
            name = "{0}_{1}_{2}_{3}x{4}".format(layer_stack[0],
                                                       layer_stack[1],
                                                       layer_stack[2],
                                                       dimensions[0],
                                                       dimensions[1])
                                       
        design.design.__init__(self, name)
        debug.info(4, "create contact object {0}".format(name))

        self.layer_stack = layer_stack
        self.dimensions = dimensions
        self.offset = vector(0,0)
        self.implant_type = implant_type
        self.well_type = well_type        
        self.pins = [] # used for matching parm lengths
        self.create_layout()

    def create_layout(self):
        self.setup_layers()
        self.setup_layout_constants()
        self.create_contact_array()
        self.create_first_layer_enclosure()
        self.create_second_layer_enclosure()
        
        self.height = max(obj.offset.y + obj.height for obj in self.objs)
        self.width = max(obj.offset.x + obj.width for obj in self.objs)

        # Do not include the select layer in the height/width
        if self.implant_type and self.well_type:
            self.create_implant_well_enclosures()
        elif self.implant_type or self.well_type:
            debug.error(-1,"Must define both implant and well type or none at all.")

    def setup_layers(self):
        (first_layer, via_layer, second_layer) = self.layer_stack
        self.first_layer_name = first_layer
        self.via_layer_name = via_layer
        # Some technologies have a separate active contact from the poly contact
        # We will use contact for DRC, but active_contact for output
        if first_layer=="active" or second_layer=="active":
            self.via_layer_name_expanded = "active_"+via_layer
        else:
            self.via_layer_name_expanded = via_layer
        self.second_layer_name = second_layer

    def setup_layout_constants(self):
        self.contact_width = drc["minwidth_{0}". format(self.via_layer_name)]
        contact_to_contact = drc["{0}_to_{0}".format(self.via_layer_name)]
        self.contact_pitch = self.contact_width + contact_to_contact
        self.contact_array_width = self.contact_width + (self.dimensions[0] - 1) * self.contact_pitch
        self.contact_array_height = self.contact_width + (self.dimensions[1] - 1) * self.contact_pitch

        # DRC rules
        first_layer_minwidth = drc["minwidth_{0}".format(self.first_layer_name)]
        first_layer_minarea = drc["minarea_{0}".format(self.first_layer_name)]
        first_layer_enclosure = drc["{0}_enclosure_{1}".format(self.first_layer_name, self.via_layer_name)]
        first_layer_extend = drc["{0}_extend_{1}".format(self.first_layer_name, self.via_layer_name)]
        second_layer_minwidth = drc["minwidth_{0}".format(self.second_layer_name)]
        second_layer_minarea = drc["minarea_{0}".format(self.second_layer_name)]
        second_layer_enclosure = drc["{0}_enclosure_{1}".format(self.second_layer_name, self.via_layer_name)]
        second_layer_extend = drc["{0}_extend_{1}".format(self.second_layer_name, self.via_layer_name)]

        self.first_layer_horizontal_enclosure = max((first_layer_minwidth - self.contact_array_width) / 2,
                                                    first_layer_enclosure)
        self.first_layer_vertical_enclosure = max(utils.ceil((first_layer_minarea
                                                              / (self.contact_array_width + 2*self.first_layer_horizontal_enclosure)
                                                              - self.contact_array_height)/2),
                                                  (first_layer_minwidth - self.contact_array_height)/2,
                                                  first_layer_extend)

        self.second_layer_horizontal_enclosure = max((second_layer_minwidth - self.contact_array_width)/2,
                                                     second_layer_enclosure)
        self.second_layer_vertical_enclosure = max(utils.ceil((second_layer_minarea
                                                               / (self.contact_array_width + 2*self.second_layer_horizontal_enclosure) 
                                                               - self.contact_array_height)/2),
                                                   (second_layer_minwidth - self.contact_array_height)/2,
                                                   second_layer_extend)
        
    def create_contact_array(self):
        """ Create the contact array at the origin"""
        # offset for the via array
        self.via_layer_position =vector(max(self.first_layer_horizontal_enclosure,self.second_layer_horizontal_enclosure),
                                        max(self.first_layer_vertical_enclosure,self.second_layer_vertical_enclosure))

        for i in range(self.dimensions[1]):
            offset = self.via_layer_position + vector(0, self.contact_pitch * i)
            for j in range(self.dimensions[0]):
                self.add_rect(layer=self.via_layer_name_expanded,
                              offset=offset,
                              width=self.contact_width,
                              height=self.contact_width)
                offset = offset + vector(self.contact_pitch,0)

    def create_first_layer_enclosure(self):
        # this is if the first and second layers are different
        self.first_layer_position = vector(max(self.second_layer_horizontal_enclosure - self.first_layer_horizontal_enclosure,0),
                                           max(self.second_layer_vertical_enclosure - self.first_layer_vertical_enclosure,0))

        self.first_layer_width = self.contact_array_width + 2*self.first_layer_horizontal_enclosure
        self.first_layer_height = self.contact_array_height + 2*self.first_layer_vertical_enclosure
        self.add_rect(layer=self.first_layer_name,
                      offset=self.first_layer_position,
                      width=self.first_layer_width,
                      height=self.first_layer_height)

    def create_second_layer_enclosure(self):
        # this is if the first and second layers are different
        self.second_layer_position = vector(max(self.first_layer_horizontal_enclosure - self.second_layer_horizontal_enclosure,0),
                                            max(self.first_layer_vertical_enclosure - self.second_layer_vertical_enclosure,0))

        self.second_layer_width = self.contact_array_width  + 2*self.second_layer_horizontal_enclosure
        self.second_layer_height = self.contact_array_height + 2*self.second_layer_vertical_enclosure
        self.add_rect(layer=self.second_layer_name,
                      offset=self.second_layer_position,
                      width=self.second_layer_width,
                      height=self.second_layer_height)

    def create_implant_well_enclosures(self):
        implant_position = self.first_layer_position - [drc["implant_enclosure_active"]]*2
        implant_width =  self.first_layer_width  + 2*drc["implant_enclosure_active"]
        implant_height = self.first_layer_height + 2*drc["implant_enclosure_active"]
        self.add_rect(layer="{}implant".format(self.implant_type),
                      offset=implant_position,
                      width=implant_width,
                      height=implant_height)
        well_position = self.first_layer_position - [drc["well_enclosure_active"]]*2
        well_width =  self.first_layer_width  + 2*drc["well_enclosure_active"]
        well_height = self.first_layer_height + 2*drc["well_enclosure_active"]
        self.add_rect(layer="{}well".format(self.well_type),
                      offset=well_position,
                      width=well_width,
                      height=well_height)
        


# This is not instantiated and used for calculations only.
# These are static 1x1 contacts to reuse in all the design modules.
well = contact(layer_stack=("active", "contact", "metal1"))
active = contact(layer_stack=("active", "contact", "poly"))
poly = contact(layer_stack=("poly", "contact", "metal1"))
m1m2 = contact(layer_stack=("metal1", "via1", "metal2"))
m2m3 = contact(layer_stack=("metal2", "via2", "metal3"))

