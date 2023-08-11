# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import GDS, layer
from openram.tech import preferred_directions
from openram.tech import cell_properties as props
from openram import OPTS
from . import utils
from .hierarchy_design import hierarchy_design


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
            debug.check(prop.port_names == list(self.pins),
                        "Custom cell pin names do not match spice file:\n{0} vs {1}".format(prop.port_names, list(self.pins)))
            self.add_pin_indices(prop.port_indices)
            self.add_pin_names(prop.port_map)
            self.update_pin_types(prop.port_types)


            (width, height) = utils.get_libcell_size(self.cell_name,
                                                     GDS["unit"],
                                                     layer[prop.boundary_layer])
            self.pin_map = utils.get_libcell_pins(list(self.pins),
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

        try:
            from openram.tech import power_grid
            self.supply_stack = power_grid
        except ImportError:
            # if no power_grid is specified by tech we use sensible defaults
            # Route a M3/M4 grid
            self.supply_stack = self.m3_stack

    def check_pins(self):
        for pin_name in self.pins:
            pins = self.get_pins(pin_name)
            for pin in pins:
                debug.info(0, "{0} {1}".format(pin_name, pin))

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
