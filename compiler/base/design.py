# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from hierarchy_design import hierarchy_design
import contact
from globals import OPTS
import re


class design(hierarchy_design):
    """
    This is the same as the hierarchy_design class except it contains
    some DRC/layer constants and analytical models for other modules to reuse.

    """

    def __init__(self, name):
        hierarchy_design.__init__(self, name)
        
        self.setup_drc_constants()
        self.setup_layer_constants()
        self.setup_multiport_constants()

    def setup_layer_constants(self):
        """
        These are some layer constants used
        in many places in the compiler.
        """
        
        import tech
        for key in dir(tech):
            # Single layer width rules
            match = re.match(r".*_stack$", key)
            if match:
                layer_stack = getattr(tech, key)

                # Set the stack as a local helper
                setattr(self, key, layer_stack)

                # Add the pitch
                setattr(self,
                        "{}_pitch".format(layer_stack[0]),
                        self.compute_pitch(layer_stack))

        if False:
            print("m1_pitch", self.m1_pitch)
            print("m2_pitch", self.m2_pitch)
            print("m3_pitch", self.m3_pitch)
            import sys
            sys.exit(1)

    def compute_pitch(self, layer_stack):
        
        """
        This is contact direction independent pitch,
        i.e. we take the maximum contact dimension
        """
        (layer1, via, layer2) = layer_stack

        if layer1 == "poly" or layer1 == "active":
            contact1 = getattr(contact, layer1 + "_contact")
        else:
            contact1 = getattr(contact, layer1 + "_via")
        max_contact = max(contact1.width, contact1.height)
        
        layer1_space = getattr(self, layer1 + "_space")
        layer2_space = getattr(self, layer2 + "_space")
        pitch = max_contact + max(layer1_space, layer2_space)

        return pitch
        
    def setup_drc_constants(self):
        """ 
        These are some DRC constants used in many places
        in the compiler.
        """
        # Make some local rules for convenience
        from tech import drc
        for rule in drc.keys():
            # Single layer width rules
            match = re.search(r"minwidth_(.*)", rule)
            if match:
                if match.group(1) == "active_contact":
                    setattr(self, "contact_width", drc(match.group(0)))
                else:
                    setattr(self, match.group(1) + "_width", drc(match.group(0)))

            # Single layer area rules
            match = re.search(r"minarea_(.*)", rule)
            if match:
                setattr(self, match.group(0), drc(match.group(0)))
                    
            # Single layer spacing rules
            match = re.search(r"(.*)_to_(.*)", rule)
            if match and match.group(1) == match.group(2):
                setattr(self, match.group(1) + "_space", drc(match.group(0)))
            elif match and match.group(1) != match.group(2):
                if match.group(2) == "poly_active":
                    setattr(self, match.group(1) + "_to_contact",
                            drc(match.group(0)))
                else:
                    setattr(self, match.group(0), drc(match.group(0)))
                
            match = re.search(r"(.*)_enclose_(.*)", rule)
            if match:
                setattr(self, match.group(0), drc(match.group(0)))

            match = re.search(r"(.*)_extend_(.*)", rule)
            if match:
                setattr(self, match.group(0), drc(match.group(0)))

        # Create the maximum well extend active that gets used
        # by cells to extend the wells for interaction with other cells
        from tech import layer
        self.well_extend_active = 0
        if "nwell" in layer:
            self.well_extend_active = max(self.well_extend_active, self.nwell_extend_active)
        if "pwell" in layer:
            self.well_extend_active = max(self.well_extend_active, self.pwell_extend_active)
            
        # These are for debugging previous manual rules
        if False:
            print("poly_width", self.poly_width)
            print("poly_space", self.poly_space)
            print("m1_width", self.m1_width)
            print("m1_space", self.m1_space)
            print("m2_width", self.m2_width)
            print("m2_space", self.m2_space)
            print("m3_width", self.m3_width)
            print("m3_space", self.m3_space)
            print("m4_width", self.m4_width)
            print("m4_space", self.m4_space)
            print("active_width", self.active_width)
            print("active_space", self.active_space)
            print("contact_width", self.contact_width)
            print("poly_to_active", self.poly_to_active)
            print("poly_extend_active", self.poly_extend_active)
            print("poly_to_contact", self.poly_to_contact)
            print("contact_to_gate", self.contact_to_gate)
            print("well_enclose_active", self.well_enclose_active)
            print("implant_enclose_active", self.implant_enclose_active)
            print("implant_space", self.implant_space)
            import sys
            sys.exit(1)
        
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
    
