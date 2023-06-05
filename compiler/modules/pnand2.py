# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.base import logical_effort
from openram.sram_factory import factory
from openram.tech import drc, parameter, spice
from openram.tech import cell_properties as cell_props
from .pgate import *


class pnand2(pgate):
    """
    This module generates gds of a parametrically sized 2-input nand.
    This model use ptx to generate a 2-input nand within a cetrain height.
    """
    def __init__(self, name, size=1, height=None, add_wells=True):
        """ Creates a cell for a simple 2 input nand """

        debug.info(2,
                   "creating pnand2 structure {0} with size of {1}".format(name,
                                                                           size))
        self.add_comment("size: {}".format(size))

        self.size = size
        self.nmos_size = 2 * size
        self.pmos_size = parameter["beta"] * size
        self.nmos_width = self.nmos_size * drc("minwidth_tx")
        self.pmos_width = self.pmos_size * drc("minwidth_tx")

        # FIXME: Allow these to be sized
        debug.check(size == 1, "Size 1 pnand2 is only supported now.")
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
        self.route_output()
        self.determine_width()
        self.route_supply_rails()
        self.connect_rails()
        self.extend_wells()
        self.route_inputs()
        self.add_boundary()

    def add_pins(self):
        """ Adds pins for spice netlist """
        pin_list = ["A", "B", "Z", "vdd", "gnd"]
        dir_list = ["INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"]
        self.add_pin_list(pin_list, dir_list)

    def add_ptx(self):
        """ Create the PMOS and NMOS transistors. """
        self.nmos_left = factory.create(module_type="ptx",
                                        width=self.nmos_width,
                                        mults=self.tx_mults,
                                        tx_type="nmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact="active")

        self.nmos_right = factory.create(module_type="ptx",
                                         width=self.nmos_width,
                                         mults=self.tx_mults,
                                         tx_type="nmos",
                                         add_source_contact="active",
                                         add_drain_contact=self.route_layer)

        self.pmos_left = factory.create(module_type="ptx",
                                        width=self.pmos_width,
                                        mults=self.tx_mults,
                                        tx_type="pmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact=self.route_layer)

        self.pmos_right = factory.create(module_type="ptx",
                                         width=self.pmos_width,
                                         mults=self.tx_mults,
                                         tx_type="pmos",
                                         add_source_contact=self.route_layer,
                                         add_drain_contact=self.route_layer)

    def setup_layout_constants(self):
        """ Pre-compute some handy layout parameters. """

        # Compute the other pmos2 location,
        # but determining offset to overlap the
        # source and drain pins
        self.overlap_offset = self.pmos_left.get_pin("D").center() - self.pmos_left.get_pin("S").center()

    def create_ptx(self):
        """
        Add PMOS and NMOS to the netlist.
        """

        self.pmos1_inst = self.add_inst(name="pnand2_pmos1",
                                        mod=self.pmos_left)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos2_inst = self.add_inst(name="pnand2_pmos2",
                                        mod=self.pmos_right)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

        self.nmos1_inst = self.add_inst(name="pnand2_nmos1",
                                        mod=self.nmos_left)
        self.connect_inst(["Z", "B", "net1", "gnd"])

        self.nmos2_inst = self.add_inst(name="pnand2_nmos2",
                                        mod=self.nmos_right)
        self.connect_inst(["net1", "A", "gnd", "gnd"])

    def place_ptx(self):
        """
        Place PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        pmos1_pos = vector(self.pmos_left.active_offset.x,
                           self.height - self.pmos_left.active_height \
                           - self.top_bottom_space)
        self.pmos1_inst.place(pmos1_pos)

        self.pmos2_pos = pmos1_pos + self.overlap_offset
        self.pmos2_inst.place(self.pmos2_pos)

        nmos1_pos = vector(self.pmos_left.active_offset.x,
                           self.top_bottom_space)
        self.nmos1_inst.place(nmos1_pos)

        self.nmos2_pos = nmos1_pos + self.overlap_offset
        self.nmos2_inst.place(self.nmos2_pos)

    def add_well_contacts(self):
        """
        Add n/p well taps to the layout and connect to supplies
        AFTER the wells are created
        """

        self.add_nwell_contact(self.pmos_right, self.pmos2_pos)
        self.add_pwell_contact(self.nmos_left, self.nmos2_pos)

    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst, "S", "gnd")

        self.connect_pin_to_rail(self.pmos1_inst, "S", "vdd")

        self.connect_pin_to_rail(self.pmos2_inst, "D", "vdd")

    def route_inputs(self):
        """ Route the A and B inputs """

        # Top of NMOS drain
        bottom_pin = self.nmos1_inst.get_pin("D")
        # active contact metal to poly contact metal spacing
        active_contact_to_poly_contact = bottom_pin.uy() + self.route_layer_space + 0.5 * self.poly_contact.second_layer_height
        # active diffusion to poly contact spacing
        # doesn't use nmos uy because that is calculated using offset + poly height
        active_top = self.nmos1_inst.by() + self.nmos1_inst.mod.active_height
        active_to_poly_contact = active_top + self.poly_to_active + 0.5 * self.poly_contact.first_layer_height
        active_to_poly_contact2 = active_top + self.poly_contact_to_gate + 0.5 * self.route_layer_width
        self.inputA_yoffset = max(active_contact_to_poly_contact,
                                  active_to_poly_contact,
                                  active_to_poly_contact2)

        apin = self.route_input_gate(self.pmos1_inst,
                                     self.nmos1_inst,
                                     self.inputA_yoffset,
                                     "A",
                                     position="center")

        self.inputB_yoffset = self.inputA_yoffset + 2 * self.m3_pitch
        # # active contact metal to poly contact metal spacing
        # active_contact_to_poly_contact = self.output_yoffset - self.route_layer_space - 0.5 * self.poly_contact.second_layer_height
        # active_bottom = self.pmos1_inst.by()
        # active_to_poly_contact = active_bottom - self.poly_to_active - 0.5 * self.poly_contact.first_layer_height
        # active_to_poly_contact2 = active_bottom - self.poly_contact_to_gate - 0.5 * self.route_layer_width
        # self.inputB_yoffset = min(active_contact_to_poly_contact,
        #                           active_to_poly_contact,
        #                           active_to_poly_contact2)

        # This will help with the wells and the input/output placement
        bpin = self.route_input_gate(self.pmos2_inst,
                                     self.nmos2_inst,
                                     self.inputB_yoffset,
                                     "B",
                                     position="center")

        if cell_props.pgate.add_implants:
            self.add_enclosure([apin, bpin], "npc", drc("npc_enclose_poly"))

    def route_output(self):
        """ Route the Z output """

        # One routing track layer below the PMOS contacts
        route_layer_offset = 0.5 * self.poly_contact.second_layer_height + self.route_layer_space
        self.output_yoffset = self.pmos1_inst.get_pin("D").by() - route_layer_offset


        # PMOS1 drain
        pmos_pin = self.pmos1_inst.get_pin("D")
        top_pin_offset = pmos_pin.bc()
        # NMOS2 drain
        nmos_pin = self.nmos2_inst.get_pin("D")
        bottom_pin_offset = nmos_pin.uc()

        # Output pin
        out_offset = vector(nmos_pin.cx() + self.route_layer_pitch,
                            self.output_yoffset)

        # This routes on M2
        # # Midpoints of the L routes go horizontal first then vertical
        # mid1_offset = vector(out_offset.x, top_pin_offset.y)
        # mid2_offset = vector(out_offset.x, bottom_pin_offset.y)

        # # Non-preferred active contacts
        # self.add_via_center(layers=self.m1_stack,
        #                     directions=("V", "H"),
        #                     offset=pmos_pin.center())
        # # Non-preferred active contacts
        # self.add_via_center(layers=self.m1_stack,
        #                     directions=("V", "H"),
        #                     offset=nmos_pin.center())
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=out_offset)

        # # PMOS1 to mid-drain to NMOS2 drain
        # self.add_path("m2",
        #               [top_pin_offset, mid1_offset, out_offset,
        #                mid2_offset, bottom_pin_offset])

        # This routes on route_layer
        # Midpoints of the L routes goes vertical first then horizontal
        top_mid_offset = vector(top_pin_offset.x, out_offset.y)
        # Top transistors
        self.add_path(self.route_layer,
                      [top_pin_offset, top_mid_offset, out_offset])

        bottom_mid_offset = bottom_pin_offset + vector(0, self.route_layer_pitch)
        # Bottom transistors
        self.add_path(self.route_layer,
                      [out_offset, bottom_mid_offset, bottom_pin_offset])

        # This extends the output to the edge of the cell
        self.add_layout_pin_rect_center(text="Z",
                                        layer=self.route_layer,
                                        offset=out_offset)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nand2_leakage"]

        total_power = self.return_power(power_dyn, power_leak)
        return total_power

    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        # In fF
        c_para = spice["min_tx_drain_c"] * (self.nmos_size / parameter["min_tx_size"])
        transition_prob = 0.1875
        return transition_prob * (c_load + c_para)

    def input_load(self):
        """Return the relative input capacitance of a single input"""
        return self.nmos_size + self.pmos_size

    def get_stage_effort(self, cout, inp_is_rise=True):
        """
        Returns an object representing the parameters for delay in tau units.
        Optional is_rise refers to the input direction rise/fall.
        Input inverted by this stage.
        """
        parasitic_delay = 2
        return logical_effort(self.name,
                              self.size,
                              self.input_load(),
                              cout,
                              parasitic_delay,
                              not inp_is_rise)

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)

    def is_non_inverting(self):
        """Return input to output polarity for module"""
        return False

    def get_on_resistance(self):
        """On resistance of pnand, defined by stacked NMOS"""
        is_nchannel = True
        stack = 2
        is_cell = False
        return self.tr_r_on(self.nmos_width, is_nchannel, stack, is_cell)

    def get_input_capacitance(self):
        """Input cap of input, passes width of gates to gate cap function"""
        return self.gate_c(self.nmos_width+self.pmos_width)

    def get_intrinsic_capacitance(self):
        """Get the drain capacitances of the TXs in the gate."""
        nmos_stack = 2
        nmos_drain_c =  self.drain_c_(self.nmos_width*self.tx_mults,
                                      nmos_stack,
                                      self.tx_mults)
        pmos_drain_c =  self.drain_c_(self.pmos_width*self.tx_mults,
                                      1,
                                      self.tx_mults)
        return nmos_drain_c + pmos_drain_c
