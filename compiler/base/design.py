# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from hierarchy_design import hierarchy_design
import utils
import contact
from tech import GDS, layer
from tech import preferred_directions
from tech import cell_properties as props
from globals import OPTS
import re
import debug


class design(hierarchy_design):
    """
    This is the same as the hierarchy_design class except it contains
    some DRC/layer constants and analytical models for other modules to reuse.
    """

    def __init__(self, name, cell_name=None, prop=None):
        # This allows us to use different GDS/spice circuits for hard cells instead of the default ones
        # Except bitcell names are generated automatically by the globals.py setup_bitcells routines
        # depending on the number of ports.

        if name in props.names:
            if type(props.names[name]) is list:
                num_ports = OPTS.num_rw_ports + OPTS.num_r_ports + OPTS.num_w_ports - 1
                cell_name = props.names[name][num_ports]
            else:
                cell_name = props.names[name]

        elif not cell_name:
            cell_name = name
        super().__init__(name, cell_name)

        # This means it is a custom cell.
        # It could have properties and not be a hard cell too (e.g. dff_buf)
        if prop and prop.hard_cell:
            # The pins get added from the spice file, so just check
            # that they matched here
            debug.check(prop.port_names == self.pins,
                        "Custom cell pin names do not match spice file:\n{0} vs {1}".format(prop.port_names, self.pins))
            self.add_pin_indices(prop.port_indices)
            self.add_pin_names(prop.port_map)
            self.add_pin_types(prop.port_types)


            (width, height) = utils.get_libcell_size(self.cell_name,
                                                     GDS["unit"],
                                                     layer[prop.boundary_layer])
            self.pin_map = utils.get_libcell_pins(self.pins,
                                                  self.cell_name,
                                                  GDS["unit"])

            # Convert names back to the original names
            # so that copying will use the new names
            for pin_name in self.pin_map:
                for index1, pin in enumerate(self.pin_map[pin_name]):
                    self.pin_map[pin_name][index1].name = self.get_original_pin_name(pin.name)

            self.width = width
            self.height = height

        self.setup_multiport_constants()

    def check_pins(self):
        for pin_name in self.pins:
            pins = self.get_pins(pin_name)
            for pin in pins:
                print(pin_name, pin)

    @classmethod
    def setup_drc_constants(design):
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
                    setattr(design, "contact_width", drc(match.group(0)))
                else:
                    setattr(design, match.group(1) + "_width", drc(match.group(0)))

            # Single layer area rules
            match = re.search(r"minarea_(.*)", rule)
            if match:
                setattr(design, match.group(0), drc(match.group(0)))

            # Single layer spacing rules
            match = re.search(r"(.*)_to_(.*)", rule)
            if match and match.group(1) == match.group(2):
                setattr(design, match.group(1) + "_space", drc(match.group(0)))
            elif match and match.group(1) != match.group(2):
                if match.group(2) == "poly_active":
                    setattr(design, match.group(1) + "_to_contact",
                            drc(match.group(0)))
                else:
                    setattr(design, match.group(0), drc(match.group(0)))

            match = re.search(r"(.*)_enclose_(.*)", rule)
            if match:
                setattr(design, match.group(0), drc(match.group(0)))

            match = re.search(r"(.*)_extend_(.*)", rule)
            if match:
                setattr(design, match.group(0), drc(match.group(0)))

        # Create the maximum well extend active that gets used
        # by cells to extend the wells for interaction with other cells
        from tech import layer
        design.well_extend_active = 0
        if "nwell" in layer:
            design.well_extend_active = max(design.well_extend_active, design.nwell_extend_active)
        if "pwell" in layer:
            design.well_extend_active = max(design.well_extend_active, design.pwell_extend_active)

        # The active offset is due to the well extension
        if "pwell" in layer:
            design.pwell_enclose_active = drc("pwell_enclose_active")
        else:
            design.pwell_enclose_active = 0
        if "nwell" in layer:
            design.nwell_enclose_active = drc("nwell_enclose_active")
        else:
            design.nwell_enclose_active = 0
        # Use the max of either so that the poly gates will align properly
        design.well_enclose_active = max(design.pwell_enclose_active,
                                       design.nwell_enclose_active,
                                       design.active_space)

        # These are for debugging previous manual rules
        if False:
            print("poly_width", design.poly_width)
            print("poly_space", design.poly_space)
            print("m1_width", design.m1_width)
            print("m1_space", design.m1_space)
            print("m2_width", design.m2_width)
            print("m2_space", design.m2_space)
            print("m3_width", design.m3_width)
            print("m3_space", design.m3_space)
            print("m4_width", design.m4_width)
            print("m4_space", design.m4_space)
            print("active_width", design.active_width)
            print("active_space", design.active_space)
            print("contact_width", design.contact_width)
            print("poly_to_active", design.poly_to_active)
            print("poly_extend_active", design.poly_extend_active)
            print("poly_to_contact", design.poly_to_contact)
            print("active_contact_to_gate", design.active_contact_to_gate)
            print("poly_contact_to_gate", design.poly_contact_to_gate)
            print("well_enclose_active", design.well_enclose_active)
            print("implant_enclose_active", design.implant_enclose_active)
            print("implant_space", design.implant_space)
            import sys
            sys.exit(1)

    @classmethod
    def setup_layer_constants(design):
        """
        These are some layer constants used
        in many places in the compiler.
        """

        from tech import layer_indices
        import tech
        for layer_id in layer_indices:
            key = "{}_stack".format(layer_id)

            # Set the stack as a local helper
            try:
                layer_stack = getattr(tech, key)
                setattr(design, key, layer_stack)
            except AttributeError:
                pass

            # Skip computing the pitch for non-routing layers
            if layer_id in ["active", "nwell"]:
                continue

            # Add the pitch
            setattr(design,
                    "{}_pitch".format(layer_id),
                    design.compute_pitch(layer_id, True))

            # Add the non-preferrd pitch (which has vias in the "wrong" way)
            setattr(design,
                    "{}_nonpref_pitch".format(layer_id),
                    design.compute_pitch(layer_id, False))

        if False:
            from tech import preferred_directions
            print(preferred_directions)
            from tech import layer_indices
            for name in layer_indices:
                if name == "active":
                    continue
                try:
                    print("{0} width {1} space {2}".format(name,
                                                           getattr(design, "{}_width".format(name)),
                                                           getattr(design, "{}_space".format(name))))

                    print("pitch {0} nonpref {1}".format(getattr(design, "{}_pitch".format(name)),
                                                         getattr(design, "{}_nonpref_pitch".format(name))))
                except AttributeError:
                    pass
            import sys
            sys.exit(1)

    @staticmethod
    def compute_pitch(layer, preferred=True):

        """
        This is the preferred direction pitch
        i.e. we take the minimum or maximum contact dimension
        """
        # Find the layer stacks this is used in
        from tech import layer_stacks
        pitches = []
        for stack in layer_stacks:
            # Compute the pitch with both vias above and below (if they exist)
            if stack[0] == layer:
                pitches.append(design.compute_layer_pitch(stack, preferred))
            if stack[2] == layer:
                pitches.append(design.compute_layer_pitch(stack[::-1], True))

        return max(pitches)

    @staticmethod
    def get_preferred_direction(layer):
        return preferred_directions[layer]

    @staticmethod
    def compute_layer_pitch(layer_stack, preferred):

        (layer1, via, layer2) = layer_stack
        try:
            if layer1 == "poly" or layer1 == "active":
                contact1 = getattr(contact, layer1 + "_contact")
            else:
                contact1 = getattr(contact, layer1 + "_via")
        except AttributeError:
            contact1 = getattr(contact, layer2 + "_via")

        if preferred:
            if preferred_directions[layer1] == "V":
                contact_width = contact1.first_layer_width
            else:
                contact_width = contact1.first_layer_height
        else:
            if preferred_directions[layer1] == "V":
                contact_width = contact1.first_layer_height
            else:
                contact_width = contact1.first_layer_width
        layer_space = getattr(design, layer1 + "_space")

        #print(layer_stack)
        #print(contact1)
        pitch = contact_width + layer_space

        return utils.round_to_grid(pitch)

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
        # These are the read/write and read-only port indices
        self.read_ports = []
        # These are the read-only port indices.
        self.readonly_ports = []
        # These are all the ports
        self.all_ports = list(range(total_ports))

        # The order is always fixed as RW, W, R
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

design.setup_drc_constants()
design.setup_layer_constants()

