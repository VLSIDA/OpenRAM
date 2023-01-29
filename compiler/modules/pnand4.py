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


class pnand4(pgate):
    """
    This module generates gds of a parametrically sized 4-input nand.
    This model use ptx to generate a 4-input nand within a cetrain height.
    """
    def __init__(self, name, size=1, height=None, add_wells=True):
        """ Creates a cell for a simple 3 input nand """

        debug.info(2,
                   "creating pnand4 structure {0} with size of {1}".format(name,
                                                                           size))
        self.add_comment("size: {}".format(size))

        # We have trouble pitch matching a 3x sizes to the bitcell...
        # If we relax this, we could size this better.
        self.size = size
        self.nmos_size = 2 * size
        self.pmos_size = parameter["beta"] * size
        self.nmos_width = self.nmos_size * drc("minwidth_tx")
        self.pmos_width = self.pmos_size * drc("minwidth_tx")

        # FIXME: Allow these to be sized
        debug.check(size == 1,
                    "Size 1 pnand4 is only supported now.")
        self.tx_mults = 1

        if cell_props.ptx.bin_spice_models:
            self.nmos_width = self.nearest_bin("nmos", self.nmos_width)
            self.pmos_width = self.nearest_bin("pmos", self.pmos_width)

        # Creates the netlist and layout
        super().__init__(name, height, add_wells)

    def add_pins(self):
        """ Adds pins for spice netlist """
        pin_list = ["A", "B", "C", "D", "Z", "vdd", "gnd"]
        dir_list = ["INPUT", "INPUT", "INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"]
        self.add_pin_list(pin_list, dir_list)

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

    def add_ptx(self):
        """ Create the PMOS and NMOS transistors. """
        self.nmos_center = factory.create(module_type="ptx",
                                          width=self.nmos_width,
                                          mults=self.tx_mults,
                                          tx_type="nmos",
                                          add_source_contact="active",
                                          add_drain_contact="active")

        self.nmos_right = factory.create(module_type="ptx",
                                         width=self.nmos_width,
                                         mults=self.tx_mults,
                                         tx_type="nmos",
                                         add_source_contact="active",
                                         add_drain_contact=self.route_layer)

        self.nmos_left = factory.create(module_type="ptx",
                                        width=self.nmos_width,
                                        mults=self.tx_mults,
                                        tx_type="nmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact="active")

        self.pmos_left = factory.create(module_type="ptx",
                                        width=self.pmos_width,
                                        mults=self.tx_mults,
                                        tx_type="pmos",
                                        add_source_contact=self.route_layer,
                                        add_drain_contact=self.route_layer)

        self.pmos_center = factory.create(module_type="ptx",
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

        # Compute the overlap of the source and drain pins
        self.ptx_offset = self.pmos_left.get_pin("D").center() - self.pmos_left.get_pin("S").center()

        # This is the extra space needed to ensure DRC rules
        # to the active contacts
        nmos = factory.create(module_type="ptx", tx_type="nmos")

    def create_ptx(self):
        """
        Create the PMOS and NMOS in the netlist.
        """

        self.pmos1_inst = self.add_inst(name="pnand4_pmos1",
                                        mod=self.pmos_left)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos2_inst = self.add_inst(name="pnand4_pmos2",
                                        mod=self.pmos_center)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

        self.pmos3_inst = self.add_inst(name="pnand4_pmos3",
                                        mod=self.pmos_center)
        self.connect_inst(["Z", "C", "vdd", "vdd"])

        self.pmos4_inst = self.add_inst(name="pnand4_pmos4",
                                        mod=self.pmos_right)
        self.connect_inst(["Z", "D", "vdd", "vdd"])

        self.nmos1_inst = self.add_inst(name="pnand4_nmos1",
                                        mod=self.nmos_left)
        self.connect_inst(["Z", "D", "net1", "gnd"])

        self.nmos2_inst = self.add_inst(name="pnand4_nmos2",
                                        mod=self.nmos_center)
        self.connect_inst(["net1", "C", "net2", "gnd"])

        self.nmos3_inst = self.add_inst(name="pnand4_nmos3",
                                        mod=self.nmos_center)
        self.connect_inst(["net2", "B", "net3", "gnd"])

        self.nmos4_inst = self.add_inst(name="pnand4_nmos4",
                                        mod=self.nmos_right)
        self.connect_inst(["net3", "A", "gnd", "gnd"])

    def place_ptx(self):
        """
        Place the PMOS and NMOS in the layout at the upper-most
        and lowest position to provide maximum routing in channel
        """

        pmos1_pos = vector(self.pmos_left.active_offset.x,
                           self.height - self.pmos_left.active_height - self.top_bottom_space)
        self.pmos1_inst.place(pmos1_pos)

        pmos2_pos = pmos1_pos + self.ptx_offset
        self.pmos2_inst.place(pmos2_pos)

        pmos3_pos = pmos2_pos + self.ptx_offset
        self.pmos3_inst.place(pmos3_pos)

        self.pmos4_pos = pmos3_pos + self.ptx_offset
        self.pmos4_inst.place(self.pmos4_pos)

        nmos1_pos = vector(self.pmos_left.active_offset.x,
                           self.top_bottom_space)
        self.nmos1_inst.place(nmos1_pos)

        nmos2_pos = nmos1_pos + self.ptx_offset
        self.nmos2_inst.place(nmos2_pos)

        nmos3_pos = nmos2_pos + self.ptx_offset
        self.nmos3_inst.place(nmos3_pos)

        self.nmos4_pos = nmos3_pos + self.ptx_offset
        self.nmos4_inst.place(self.nmos4_pos)

    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies """

        self.add_nwell_contact(self.pmos_right,
                               self.pmos4_pos + vector(self.m1_pitch, 0))
        self.add_pwell_contact(self.nmos_right,
                               self.nmos4_pos + vector(self.m1_pitch, 0))

    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst, "S", "gnd")

        self.connect_pin_to_rail(self.pmos1_inst, "S", "vdd")

        self.connect_pin_to_rail(self.pmos2_inst, "D", "vdd")

        self.connect_pin_to_rail(self.pmos4_inst, "D", "vdd")

    def route_inputs(self):
        """ Route the A and B and C inputs """

        # We can use this pitch because the contacts and overlap won't be adjacent
        pmos_drain_bottom = self.pmos1_inst.get_pin("D").by()
        self.output_yoffset = pmos_drain_bottom - 0.5 * self.route_layer_width - self.route_layer_space

        bottom_pin = self.nmos1_inst.get_pin("D")
        # active contact metal to poly contact metal spacing
        active_contact_to_poly_contact = bottom_pin.uy() + self.m1_space + 0.5 * self.poly_contact.second_layer_height
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
                                     position="left")

        self.inputB_yoffset = self.inputA_yoffset + self.m1_pitch
        bpin = self.route_input_gate(self.pmos2_inst,
                                     self.nmos2_inst,
                                     self.inputB_yoffset,
                                     "B",
                                     position="center")

        self.inputC_yoffset = self.inputB_yoffset + self.m1_pitch
        cpin = self.route_input_gate(self.pmos3_inst,
                                     self.nmos3_inst,
                                     self.inputC_yoffset,
                                     "C",
                                     position="right")

        self.inputD_yoffset = self.inputC_yoffset + self.m1_pitch
        dpin = self.route_input_gate(self.pmos4_inst,
                                     self.nmos4_inst,
                                     self.inputD_yoffset,
                                     "D",
                                     position="right")

        if cell_props.pgate.add_implants:
            self.add_enclosure([apin, bpin, cpin, dpin], "npc", drc("npc_enclose_poly"))

    def route_output(self):
        """ Route the Z output """

        # PMOS1 drain
        pmos1_pin = self.pmos1_inst.get_pin("D")
        # PMOS3 drain
        pmos3_pin = self.pmos3_inst.get_pin("D")
        # NMOS3 drain
        nmos4_pin = self.nmos4_inst.get_pin("D")

        out_offset = vector(nmos4_pin.cx() + self.route_layer_pitch,
                            self.output_yoffset)

        # Go up to metal2 for ease on all output pins
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=pmos1_pin.center(),
        #                     directions=("V", "V"))
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=pmos3_pin.center(),
        #                     directions=("V", "V"))
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=nmos3_pin.center(),
        #                     directions=("V", "V"))

        # # Route in the A input track (top track)
        # mid_offset = vector(nmos3_pin.center().x, self.inputA_yoffset)
        # self.add_path("m1", [pmos1_pin.center(), mid_offset, nmos3_pin.uc()])

        # This extends the output to the edge of the cell
        # self.add_via_center(layers=self.m1_stack,
        #                     offset=mid_offset)

        top_left_pin_offset = pmos1_pin.center()
        top_right_pin_offset = pmos3_pin.center()
        bottom_pin_offset = nmos4_pin.center()

        # PMOS1 to output
        self.add_path(self.route_layer, [top_left_pin_offset,
                                         vector(top_left_pin_offset.x, out_offset.y),
                                         out_offset])
        # PMOS4 to output
        self.add_path(self.route_layer, [top_right_pin_offset,
                                         vector(top_right_pin_offset.x, out_offset.y),
                                         out_offset])
        # NMOS4 to output
        mid2_offset = vector(out_offset.x, bottom_pin_offset.y)
        self.add_path(self.route_layer,
                      [bottom_pin_offset, mid2_offset],
                      width=nmos4_pin.height())
        mid3_offset = vector(out_offset.x, nmos4_pin.by())
        self.add_path(self.route_layer, [mid3_offset, out_offset])

        self.add_layout_pin_rect_center(text="Z",
                                        layer=self.route_layer,
                                        offset=out_offset)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_frequency"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nand4_leakage"]

        total_power = self.return_power(power_dyn, power_leak)
        return total_power

    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        # In fF
        c_para = spice["min_tx_drain_c"] * (self.nmos_size / parameter["min_tx_size"])
        transition_prob = 0.1094
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
        parasitic_delay = 3
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

    def get_on_resistance(self):
        """On resistance of pnand, defined by stacked NMOS"""
        is_nchannel = True
        stack = 4
        is_cell = False
        return self.tr_r_on(self.nmos_width, is_nchannel, stack, is_cell)

    def get_input_capacitance(self):
        """Input cap of input, passes width of gates to gate cap function"""
        return self.gate_c(self.nmos_width+self.pmos_width)

    def get_intrinsic_capacitance(self):
        """Get the drain capacitances of the TXs in the gate."""
        nmos_stack = 4
        nmos_drain_c =  self.drain_c_(self.nmos_width*self.tx_mults,
                                      nmos_stack,
                                      self.tx_mults)
        pmos_drain_c =  self.drain_c_(self.pmos_width*self.tx_mults,
                                      1,
                                      self.tx_mults)
        return nmos_drain_c + pmos_drain_c
