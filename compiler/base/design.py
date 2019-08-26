# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from hierarchy_design import hierarchy_design
import contact
import globals
import verify
import debug
import os
from globals import OPTS

class design(hierarchy_design):
    """
    This is the same as the hierarchy_design class except it contains
    some DRC constants and analytical models for other modules to reuse.

    """

    def __init__(self, name):
        hierarchy_design.__init__(self,name)
        
        self.setup_drc_constants()
        self.setup_multiport_constants()

        from tech import layer
        self.m1_pitch = max(contact.m1m2.width,contact.m1m2.height) + max(self.m1_space, self.m2_space)
        self.m2_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(self.m2_space, self.m3_space)
        if "metal4" in layer:
            self.m3_pitch = max(contact.m3m4.width,contact.m3m4.height) + max(self.m3_space, self.m4_space)
        else:
            self.m3_pitch = self.m2_pitch

    def setup_drc_constants(self):
        """ These are some DRC constants used in many places in the compiler."""
        from tech import drc,layer
        self.well_width = drc("minwidth_well")
        self.poly_width = drc("minwidth_poly")
        self.poly_space = drc("poly_to_poly")        
        self.m1_width = drc("minwidth_metal1")
        self.m1_space = drc("metal1_to_metal1")
        self.m2_width = drc("minwidth_metal2")
        self.m2_space = drc("metal2_to_metal2")        
        self.m3_width = drc("minwidth_metal3")
        self.m3_space = drc("metal3_to_metal3")
        if "metal4" in layer:
            self.m4_width = drc("minwidth_metal4")
            self.m4_space = drc("metal4_to_metal4")
        self.active_width = drc("minwidth_active")
        self.active_space = drc("active_to_body_active")
        self.contact_width = drc("minwidth_contact")

        self.poly_to_active = drc("poly_to_active")
        self.poly_extend_active = drc("poly_extend_active")
        self.poly_to_polycontact = drc("poly_to_polycontact")
        self.contact_to_gate = drc("contact_to_gate")
        self.well_enclose_active = drc("well_enclosure_active")
        self.implant_enclose_active = drc("implant_enclosure_active")
        self.implant_space = drc("implant_to_implant")
        
    def setup_multiport_constants(self):
        """ 
        These are contants and lists that aid multiport design.
        Ports are always in the order RW, W, R.
        Port indices start from 0 and increment.
        A first RW port will have clk0, csb0, web0, addr0, data0
        A first W port (with no RW ports) will be: clk0, csb0, addr0, data0

        """
        total_ports = OPTS.num_rw_ports + OPTS.num_w_ports + OPTS.num_r_ports

        # These are the read/write port indices.
        self.readwrite_ports = []
        # These are the read/write and write-only port indices
        self.write_ports = []
        # These are the write-only port indices.
        self.writeonly_ports = []
        # These are teh read/write and read-only port indice
        self.read_ports = []
        # These are the read-only port indices.
        self.readonly_ports = []
        # These are all the ports
        self.all_ports = list(range(total_ports))
        
        port_number = 0
        for port in range(OPTS.num_rw_ports):
            self.readwrite_ports.append(port_number)
            self.write_ports.append(port_number)
            self.read_ports.append(port_number)
            port_number += 1
        for port in range(OPTS.num_w_ports):
            self.write_ports.append(port_number)
            self.writeonly_ports.append(port_number)            
            port_number += 1
        for port in range(OPTS.num_r_ports):
            self.read_ports.append(port_number)
            self.readonly_ports.append(port_number)
            port_number += 1                    
        
    def analytical_power(self, corner, load):
        """ Get total power of a module  """
        total_module_power = self.return_power()
        for inst in self.insts:
            total_module_power += inst.mod.analytical_power(corner, load)
        return total_module_power
    
