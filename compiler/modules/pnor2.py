# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import drc, parameter, spice
from openram.tech import cell_properties as cell_props
from .pgate import *


class pnor2(pgate):
    """
    This module generates gds of a parametrically sized 2-input nor.
    This model use ptx to generate a 2-input nor within a cetrain height.
    """
    def __init__(self, name, size=1, height=None, add_wells=True):
        """ Creates a cell for a simple 2 input nor """

        debug.info(2,
                   "creating pnor2 structure {0} with size of {1}".format(name,
                                                                          size))
        self.add_comment("size: {}".format(size))

        self.nmos_size = size
        # We will just make this 1.5 times for now. NORs are not ideal anyhow.
        self.pmos_size = 1.5 * parameter["beta"] * size
        self.nmos_width = self.nmos_size * drc("minwidth_tx")
        self.pmos_width = self.pmos_size * drc("minwidth_tx")

        # FIXME: Allow these to be sized
        debug.check(size==1, "Size 1 pnor2 is only supported now.")
        self.tx_mults = 1

        if cell_props.ptx.bin_spice_models:
            self.nmos_width = self.nearest_bin("nmos", self.nmos_width)
            self.pmos_width = self.nearest_bin("pmos", self.pmos_width)

        # Creates the netlist and layout
        super().__init__(name, height, add_wells)

    def create_netlist(self):
        self.add_pins()
        self.add_ptx()
        self.create_ptx()

    def create_layout(self):
        """ Calls all functions related to the generation of the layout """

        self.setup_layout_constants()
        self.place_ptx()
        if self.add_wells:
            self.add_well_contacts()
        self.route_inputs()
        self.route_output()
        self.determine_width()
        self.route_supply_rails()
        self.connect_rails()
        self.extend_wells()
        self.add_boundary()

    def add_pins(self):
        """ Adds pins for spice netlist """
        pin_list = ["A", "B", "Z", "vdd", "gnd"]
        dir_list = ["INPUT", "INPUT", "OUTPUT", "INOUT", "INOUT"]
        self.add_pin_list(pin_list, dir_list)

    def add_ptx(self):
        """ Create the PMOS and NMOS transistors. """
        self.nmos_left = factory.create(module_type="ptx",
                                        width=self.nmos_width,
                                        mults=self.tx_mults,
                                        tx_type="nmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact=self.route_layer)

        self.nmos_right = factory.create(module_type="ptx",
                                         width=self.nmos_width,
                                         mults=self.tx_mults,
                                         tx_type="nmos",
                                         add_source_contact=self.route_layer,
                                         add_drain_contact=self.route_layer)

        self.pmos_left = factory.create(module_type="ptx",
                                        width=self.pmos_width,
                                        mults=self.tx_mults,
                                        tx_type="pmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact="active")

        self.pmos_right = factory.create(module_type="ptx",
                                         width=self.pmos_width,
                                         mults=self.tx_mults,
                                         tx_type="pmos",
                                         add_source_contact="active",
                                         add_drain_contact=self.route_layer)

    def setup_layout_constants(self):
        """ Pre-compute some handy layout parameters. """

        # Compute the other pmos2 location, but determining
        # offset to overlap the source and drain pins
        self.overlap_offset = self.pmos_right.get_pin("D").center() - self.pmos_left.get_pin("S").center()

        # Two PMOS devices and a well contact. Separation between each.
        # Enclosure space on the sides.
        self.width = 2 * self.pmos_right.active_width \
                     + self.pmos_right.active_contact.width \
                     + 2 * self.active_space \
                     + 0.5 * self.nwell_enclose_active
        self.well_width = self.width + 2 * self.nwell_enclose_active
        # Height is an input parameter, so it is not recomputed.

    def create_ptx(self):
        """
        Add PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        self.pmos1_inst = self.add_inst(name="pnor2_pmos1",
                                        mod=self.pmos_left)
        self.connect_inst(["vdd", "A", "net1", "vdd"])

        self.pmos2_inst = self.add_inst(name="pnor2_pmos2",
                                        mod=self.pmos_right)
        self.connect_inst(["net1", "B", "Z", "vdd"])

        self.nmos1_inst = self.add_inst(name="pnor2_nmos1",
                                        mod=self.nmos_left)
        self.connect_inst(["Z", "A", "gnd", "gnd"])

        self.nmos2_inst = self.add_inst(name="pnor2_nmos2",
                                        mod=self.nmos_right)
        self.connect_inst(["Z", "B", "gnd", "gnd"])

    def place_ptx(self):
        """
        Add PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """
        # Some of the S/D contacts may extend beyond the active,
        # but this needs to be done in the gate itself
        contact_extend_active_space = max(-self.nmos_right.get_pin("D").by(), 0)
        # Assume the contact starts at the active edge
        contact_to_vdd_rail_space = 0.5 * self.m1_width + self.m1_space + contact_extend_active_space
        # This is a poly-to-poly of a flipped cell
        poly_to_poly_gate_space = self.poly_extend_active + self.poly_space
        # Recompute this since it has a small txwith the added contact extend active spacing
        self.top_bottom_space = max(contact_to_vdd_rail_space,
                                    poly_to_poly_gate_space)

        pmos1_pos = vector(self.pmos_right.active_offset.x,
                           self.height - self.pmos_right.active_height - self.top_bottom_space)
        self.pmos1_inst.place(pmos1_pos)

        self.pmos2_pos = pmos1_pos + self.overlap_offset
        self.pmos2_inst.place(self.pmos2_pos)

        nmos1_pos = vector(self.pmos_right.active_offset.x, self.top_bottom_space)
        self.nmos1_inst.place(nmos1_pos)

        self.nmos2_pos = nmos1_pos + self.overlap_offset
        self.nmos2_inst.place(self.nmos2_pos)

    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies """

        self.add_nwell_contact(self.pmos_right, self.pmos2_pos)
        self.add_pwell_contact(self.nmos_right, self.nmos2_pos)

    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst, "S", "gnd")

        self.connect_pin_to_rail(self.nmos2_inst, "D", "gnd")

        self.connect_pin_to_rail(self.pmos1_inst, "S", "vdd")

    def route_inputs(self):
        """ Route the A and B inputs """

        # Top of NMOS drain
        nmos_pin = self.nmos2_inst.get_pin("D")
        bottom_pin_offset = nmos_pin.uy()
        self.inputB_yoffset = bottom_pin_offset + self.m1_nonpref_pitch
        self.inputA_yoffset = self.inputB_yoffset + self.m1_nonpref_pitch

        bpin = self.route_input_gate(self.pmos2_inst,
                                     self.nmos2_inst,
                                     self.inputB_yoffset,
                                     "B",
                                     position="right",
                                     directions=("V", "V"))

        # This will help with the wells and the input/output placement
        apin = self.route_input_gate(self.pmos1_inst,
                                     self.nmos1_inst,
                                     self.inputA_yoffset,
                                     "A",
                                     directions=("V", "V"))

        self.output_yoffset = self.inputA_yoffset + self.m1_nonpref_pitch

        if cell_props.pgate.add_implants:
            self.add_enclosure([apin, bpin], "npc", drc("npc_enclose_poly"))

    def route_output(self):
        """ Route the Z output """
        # PMOS2 (right) drain
        pmos_pin = self.pmos2_inst.get_pin("D")
        # NMOS1 (left) drain
        nmos_pin = self.nmos1_inst.get_pin("D")
        # NMOS2 (right) drain (for output via placement)
        nmos2_pin = self.nmos2_inst.get_pin("D")

        # Go up to metal2 for ease on all output pins
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=pmos_pin.center())
        # m1m2_contact = self.add_via_center(layers=self.m1_stack,
        #                                    offset=nmos_pin.center())

        mid1_offset = vector(nmos_pin.center().x, self.output_yoffset)
        mid2_offset = vector(pmos_pin.center().x, self.output_yoffset)

        # PMOS1 to mid-drain to NMOS2 drain
        self.add_path(self.route_layer,
                      [nmos_pin.center(), mid1_offset, mid2_offset, pmos_pin.center()])
        self.add_layout_pin_rect_center(text="Z",
                                        layer=self.route_layer,
                                        offset=mid2_offset)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nor2_leakage"]

        total_power = self.return_power(power_dyn, power_leak)
        return total_power

    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        # In fF
        c_para = spice["min_tx_drain_c"] * (self.nmos_size / parameter["min_tx_size"])
        transition_prob = 0.1875
        return transition_prob * (c_load + c_para)

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)
