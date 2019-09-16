# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import contact
import design
import debug
from tech import drc, parameter, spice
from vector import vector
from globals import OPTS
from sram_factory import factory

class pgate(design.design):
    """
    This is a module that implements some shared functions for parameterized gates.
    """

    def __init__(self, name, height=None):
        """ Creates a generic cell """
        design.design.__init__(self, name)

        if height:
            self.height = height
        elif not height:
            b = factory.create(module_type="bitcell")
            self.height = b.height

        self.create_netlist()
        if not OPTS.netlist_only:        
            self.create_layout()
            self.add_boundary()
            self.DRC_LVS()
        

    def create_netlist(self):
        """ Pure virtual function """
        debug.error("Must over-ride create_netlist.",-1)
        
    def create_layout(self):
        """ Pure virtual function """
        debug.error("Must over-ride create_layout.",-1)

    def connect_pin_to_rail(self,inst,pin,supply):
        """ Connects a ptx pin to a supply rail. """
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
    
    def route_input_gate(self, pmos_inst, nmos_inst, ypos, name, position="left", rotate=False):
        """ Route the input gate to the left side of the cell for access.
        Position specifies to place the contact the left, center, or right of gate. """

        nmos_gate_pin = nmos_inst.get_pin("G")
        pmos_gate_pin = pmos_inst.get_pin("G")

        # Check if the gates are aligned and give an error if they aren't!
        debug.check(nmos_gate_pin.ll().x==pmos_gate_pin.ll().x, "Connecting unaligned gates not supported.")
        
        # Pick point on the left of NMOS and connect down to PMOS
        nmos_gate_pos = nmos_gate_pin.ll() + vector(0.5*self.poly_width,0)
        pmos_gate_pos = vector(nmos_gate_pos.x,pmos_gate_pin.bc().y)
        self.add_path("poly",[nmos_gate_pos,pmos_gate_pos])

        # Add the via to the cell midpoint along the gate
        left_gate_offset = vector(nmos_gate_pin.lx(),ypos)

        # Center is completely symmetric. 
        if rotate:
            contact_width = contact.poly.height
            contact_m1_width = contact.poly.second_layer_height
            contact_m1_height = contact.poly.second_layer_width
            directions = ("H","V")
        else:
            contact_width = contact.poly.width
            contact_m1_width = contact.poly.second_layer_width
            contact_m1_height = contact.poly.second_layer_height
            directions = ("V","H")
            
        if position=="center":
            contact_offset = left_gate_offset + vector(0.5*self.poly_width, 0)
        elif position=="farleft":
            contact_offset = left_gate_offset - vector(0.5*contact.poly.width, 0)
        elif position=="left":
            contact_offset = left_gate_offset - vector(0.5*contact_width - 0.5*self.poly_width, 0)
        elif position=="right":
            contact_offset = left_gate_offset + vector(0.5*contact.width + 0.5*self.poly_width, 0)
        else:
            debug.error("Invalid contact placement option.", -1)

        # Non-preferred direction via

        self.add_via_center(layers=("poly", "contact", "metal1"),
                            offset=contact_offset,
                            directions=directions)

        # self.add_layout_pin_segment_center(text=name,
        #                                    layer="metal1",
        #                                    start=left_gate_offset.scale(0,1),
        #                                    end=left_gate_offset)
        self.add_layout_pin_rect_center(text=name,
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

        # Add a rail width to extend the well to the top of the rail
        max_y_offset = self.height + 0.5*self.m1_width
        self.nwell_position = middle_position
        nwell_height = max_y_offset - middle_position.y
        if drc("has_nwell"):
            self.add_rect(layer="nwell",
                          offset=middle_position,
                          width=self.well_width,
                          height=nwell_height)
        self.add_rect(layer="vtg",
                      offset=self.nwell_position,
                      width=self.well_width,
                      height=nwell_height)

        pwell_position = vector(0,-0.5*self.m1_width)
        pwell_height = middle_position.y-pwell_position.y
        if drc("has_pwell"):
            self.add_rect(layer="pwell",
                          offset=pwell_position,
                          width=self.well_width,
                          height=pwell_height)
        self.add_rect(layer="vtg",
                      offset=pwell_position,
                      width=self.well_width,
                      height=pwell_height)

    def add_nwell_contact(self, pmos, pmos_pos):
        """ Add an nwell contact next to the given pmos device. """
        
        layer_stack = ("active", "contact", "metal1")
        
        # To the right a spacing away from the pmos right active edge
        contact_xoffset = pmos_pos.x + pmos.active_width + drc("active_to_body_active")
        # Must be at least an well enclosure of active down from the top of the well
        # OR align the active with the top of PMOS active.
        max_y_offset = self.height + 0.5*self.m1_width
        contact_yoffset = min(pmos_pos.y + pmos.active_height - pmos.active_contact.first_layer_height,
                              max_y_offset - pmos.active_contact.first_layer_height/2 - self.well_enclose_active)
        contact_offset = vector(contact_xoffset, contact_yoffset)
        # Offset by half a contact in x and y
        contact_offset += vector(0.5*pmos.active_contact.first_layer_width,
                               0.5*pmos.active_contact.first_layer_height)
        self.nwell_contact=self.add_via_center(layers=layer_stack,
                                               offset=contact_offset,
                                               directions=("H","V"),
                                               implant_type="n",
                                               well_type="n")
        self.add_rect_center(layer="metal1",
                             offset=contact_offset + vector(0,0.5*(self.height-contact_offset.y)),
                             width=self.nwell_contact.mod.second_layer_width,
                             height=self.height - contact_offset.y)
        
        # Now add the full active and implant for the PMOS
        #active_offset = pmos_pos + vector(pmos.active_width,0)
        # This might be needed if the spacing between the actives is not satisifed
        # self.add_rect(layer="active",
        #               offset=active_offset,
        #               width=pmos.active_contact.width,
        #               height=pmos.active_height)

        # we need to ensure implants don't overlap and are spaced far enough apart
        # implant_spacing = self.implant_space+self.implant_enclose_active
        # implant_offset = active_offset + vector(implant_spacing,0) - vector(0,self.implant_enclose_active)
        # implant_width = pmos.active_contact.width + 2*self.implant_enclose_active
        # implant_height = pmos.active_height + 2*self.implant_enclose_active
        # self.add_rect(layer="nimplant",
        #               offset=implant_offset,
        #               width=implant_width,
        #               height=implant_height)

        # Return the top of the well

    def add_pwell_contact(self, nmos, nmos_pos):
        """ Add an pwell contact next to the given nmos device. """

        layer_stack = ("active", "contact", "metal1")

        pwell_position = vector(0,-0.5*self.m1_width)
        
        # To the right a spacing away from the nmos right active edge
        contact_xoffset = nmos_pos.x + nmos.active_width + drc("active_to_body_active")
        # Must be at least an well enclosure of active up from the bottom of the well
        contact_yoffset = max(nmos_pos.y,
                              self.well_enclose_active - nmos.active_contact.first_layer_height/2)
        contact_offset = vector(contact_xoffset, contact_yoffset)

        # Offset by half a contact
        contact_offset += vector(0.5*nmos.active_contact.first_layer_width,
                               0.5*nmos.active_contact.first_layer_height)
        self.pwell_contact=self.add_via_center(layers=layer_stack,
                                               offset=contact_offset,
                                               directions=("H","V"),
                                               implant_type="p",
                                               well_type="p")
        self.add_rect_center(layer="metal1",
                             offset=contact_offset.scale(1,0.5),
                             width=self.pwell_contact.mod.second_layer_width,
                             height=contact_offset.y)
        
        # Now add the full active and implant for the NMOS
        # active_offset = nmos_pos + vector(nmos.active_width,0)        
        # This might be needed if the spacing between the actives is not satisifed
        # self.add_rect(layer="active",
        #               offset=active_offset,
        #               width=nmos.active_contact.width,
        #               height=nmos.active_height)

        # implant_spacing = self.implant_space+self.implant_enclose_active
        # implant_offset = active_offset + vector(implant_spacing,0) - vector(0,self.implant_enclose_active)
        # implant_width = nmos.active_contact.width + 2*self.implant_enclose_active
        # implant_height = nmos.active_height + 2*self.implant_enclose_active
        # self.add_rect(layer="pimplant",
        #               offset=implant_offset,
        #               width=implant_width,
        #               height=implant_height)
