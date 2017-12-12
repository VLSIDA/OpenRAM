import contact
import design
import debug
from tech import drc, parameter, spice, info
from ptx import ptx
from vector import vector
from globals import OPTS

class pgate(design.design):
    """
    This is a module that implements some shared functions for parameterized gates.
    """

    def __init__(self, name):
        """ Creates a generic cell """
        design.design.__init__(self, name)


    def connect_pin_to_rail(self,inst,pin,supply):
        """ Conencts a ptx pin to a supply rail. """
        source_pin = inst.get_pin(pin)
        supply_pin = self.get_pin(supply)
        if supply_pin.overlaps(source_pin):
            return
            
        if supply=="gnd":
            height=supply_pin.by()-source_pin.by()
        elif supply=="vdd":
            height=supply_pin.uy()-source_pin.by()
        else:
            debug.error("Invalid supply name.",-1)    
        
        if abs(height)>0:
            self.add_rect(layer="metal1",
                          offset=source_pin.ll(),
                          height=height,
                          width=source_pin.width())
    
    def route_input_gate(self, pmos_inst, nmos_inst, ypos, name, position="left", rotate=90):
        """ Route the input gate to the left side of the cell for access.
        Position specifies to place the contact the left, center, or right of gate. """

        nmos_gate_pin = nmos_inst.get_pin("G")
        pmos_gate_pin = pmos_inst.get_pin("G")

        # Check if the gates are aligned and give an error if they aren't!
        debug.check(nmos_gate_pin.ll().x==pmos_gate_pin.ll().x, "Connecting unaligned gates not supported.")
        
        # Pick point on the left of NMOS and connect down to PMOS
        nmos_gate_pos = nmos_gate_pin.ll() + vector(0.5*drc["minwidth_poly"],0)
        pmos_gate_pos = vector(nmos_gate_pos.x,pmos_gate_pin.bc().y)
        self.add_path("poly",[nmos_gate_pos,pmos_gate_pos])

        # Add the via to the cell midpoint along the gate
        left_gate_offset = vector(nmos_gate_pin.lx(),ypos)

        # Center is completely symmetric. 
        if rotate==90:
            contact_width = contact.poly.height
            contact_m1_width = contact.poly.second_layer_height
            contact_m1_height = contact.poly.second_layer_width
        else:
            contact_width = contact.poly.width
            contact_m1_width = contact.poly.second_layer_width
            contact_m1_height = contact.poly.second_layer_height
            
        if position=="center":
            contact_offset = left_gate_offset + vector(0.5*self.poly_width, 0)
        elif position=="left":
            contact_offset = left_gate_offset - vector(0.5*contact_width - 0.5*self.poly_width, 0)
        elif position=="right":
            contact_offset = left_gate_offset + vector(0.5*contact.width + 0.5*self.poly_width, 0)
        else:
            debug.error("Invalid contact placement option.", -1)

        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                offset=contact_offset,
                                rotate=rotate)
        # self.add_layout_pin_center_segment(text=name,
        #                                    layer="metal1",
        #                                    start=left_gate_offset.scale(0,1),
        #                                    end=left_gate_offset)
        self.add_layout_pin_center_rect(text=name,
                                        layer="metal1",
                                        offset=contact_offset,
                                        width=contact_m1_width,
                                        height=contact_m1_height)
        

        # This is to ensure that the contact is connected to the gate
        mid_point = contact_offset.scale(0.5,1)+left_gate_offset.scale(0.5,0)
        self.add_rect_center(layer="poly",
                             offset=mid_point,
                             height=contact.poly.first_layer_width,
                             width=left_gate_offset.x-contact_offset.x)

    def extend_wells(self, middle_position):
        """ Extend the n/p wells to cover whole cell """

        nwell_height = self.height - middle_position.y
        if info["has_nwell"]:
            self.add_rect(layer="nwell",
                          offset=middle_position,
                          width=self.well_width,
                          height=nwell_height)
        self.add_rect(layer="vtg",
                      offset=middle_position,
                      width=self.well_width,
                      height=nwell_height)

        if info["has_pwell"]:
            self.add_rect(layer="pwell",
                          offset=vector(0,0),
                          width=self.well_width,
                          height=middle_position.y)
        self.add_rect(layer="vtg",
                      offset=vector(0,0),
                      width=self.well_width,
                      height=middle_position.y)

    def add_nwell_contact(self, nmos, nmos_pos):
        """ Add an nwell contact next to the given nmos device. """
        
        layer_stack = ("active", "contact", "metal1")
        
        # To the right a spacing away from the nmos right active edge
        nwell_contact_xoffset = nmos_pos.x + nmos.active_width + drc["active_to_body_active"]
        nwell_contact_yoffset = nmos_pos.y 
        nwell_offset = vector(nwell_contact_xoffset, nwell_contact_yoffset)
        # Offset by half a contact in x and y
        nwell_offset += vector(0.5*nmos.active_contact.first_layer_width,
                               0.5*nmos.active_contact.first_layer_height)
        self.nwell_contact=self.add_contact_center(layers=layer_stack,
                                                   offset=nwell_offset)
        self.add_rect_center(layer="metal1",
                             offset=nwell_offset.scale(1,0.5),
                             width=self.nwell_contact.second_layer_width,
                             height=nwell_offset.y)
        # Now add the full active and implant for the NMOS
        nwell_offset = nmos_pos + vector(nmos.active_width,0) 
        nwell_contact_width = drc["active_to_body_active"] + nmos.active_contact.width
        self.add_rect(layer="active",
                      offset=nwell_offset,
                      width=nwell_contact_width,
                      height=nmos.active_height)
        
        implant_offset = nwell_offset + vector(drc["implant_to_implant"],0)
        implant_width = nwell_contact_width - drc["implant_to_implant"]
        self.add_rect(layer="pimplant",
                      offset=implant_offset,
                      width=implant_width,
                      height=nmos.active_height)


    def add_pwell_contact(self, pmos, pmos_pos):
        """ Add an pwell contact next to the given pmos device. """

        layer_stack = ("active", "contact", "metal1")

        
        # To the right a spacing away from the pmos right active edge
        pwell_contact_xoffset = pmos_pos.x + pmos.active_width + drc["active_to_body_active"]
        pwell_contact_yoffset = pmos_pos.y + pmos.active_height - pmos.active_contact.height
        pwell_offset = vector(pwell_contact_xoffset, pwell_contact_yoffset)
        # Offset by half a contact
        pwell_offset += vector(0.5*pmos.active_contact.first_layer_width,
                               0.5*pmos.active_contact.first_layer_height)
        self.pwell_contact=self.add_contact_center(layers=layer_stack,
                                                   offset=pwell_offset)
        self.add_rect_center(layer="metal1",
                             offset=pwell_offset + vector(0,0.5*(self.height-pwell_offset.y)),
                             width=self.pwell_contact.second_layer_width,
                             height=self.height - pwell_offset.y)
        # Now add the full active and implant for the PMOS
        pwell_offset = pmos_pos + vector(pmos.active_width,0)        
        pwell_contact_width = drc["active_to_body_active"] + pmos.active_contact.width        
        self.add_rect(layer="active",
                      offset=pwell_offset,
                      width=pwell_contact_width,
                      height=pmos.active_height)


        implant_offset = pwell_offset + vector(drc["implant_to_implant"],0)
        implant_width = pwell_contact_width - drc["implant_to_implant"]
        self.add_rect(layer="nimplant",
                      offset=implant_offset,
                      width=implant_width,
                      height=pmos.active_height)
        
