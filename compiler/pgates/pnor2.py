# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import contact
import pgate
import debug
from tech import drc, parameter, spice
from vector import vector
from globals import OPTS
import logical_effort
from sram_factory import factory

class pnor2(pgate.pgate):
    """
    This module generates gds of a parametrically sized 2-input nor.
    This model use ptx to generate a 2-input nor within a cetrain height.
    """
    def __init__(self, name, size=1, height=None):
        """ Creates a cell for a simple 2 input nor """

        debug.info(2, "creating pnor2 structure {0} with size of {1}".format(name, size))
        self.add_comment("size: {}".format(size))

        self.nmos_size = size
        # We will just make this 1.5 times for now. NORs are not ideal anyhow.
        self.pmos_size = 1.5*parameter["beta"]*size
        self.nmos_width = self.nmos_size*drc("minwidth_tx")
        self.pmos_width = self.pmos_size*drc("minwidth_tx")

        # FIXME: Allow these to be sized
        debug.check(size==1,"Size 1 pnor2 is only supported now.")
        self.tx_mults = 1

        # Creates the netlist and layout
        pgate.pgate.__init__(self, name, height)

        
    def create_netlist(self):
        self.add_pins()
        self.add_ptx()
        self.create_ptx()
        
    def create_layout(self):
        """ Calls all functions related to the generation of the layout """
        
        self.setup_layout_constants()
        self.route_supply_rails()
        self.place_ptx()
        self.connect_rails()
        self.add_well_contacts()
        self.extend_wells(self.well_pos)
        self.route_inputs()
        self.route_output()

    def add_pins(self):
        """ Adds pins for spice netlist """
        pin_list = ["A", "B", "Z", "vdd", "gnd"]
        dir_list = ["INPUT", "INPUT", "OUTPUT", "INOUT", "INOUT"]
        self.add_pin_list(pin_list, dir_list)

    def add_ptx(self):
        """ Create the PMOS and NMOS transistors. """
        self.nmos = factory.create(module_type="ptx",
                                   width=self.nmos_width,
                                   mults=self.tx_mults,
                                   tx_type="nmos",
                                   connect_poly=True,
                                   connect_active=True)
        self.add_mod(self.nmos)

        self.pmos = factory.create(module_type="ptx",
                                   width=self.pmos_width,
                                   mults=self.tx_mults,
                                   tx_type="pmos",
                                   connect_poly=True,
                                   connect_active=True)
        self.add_mod(self.pmos)

    def setup_layout_constants(self):
        """ Pre-compute some handy layout parameters. """

        # metal spacing to allow contacts on any layer
        self.input_spacing = max(self.poly_space + contact.poly.first_layer_width,
                                 self.m1_space + contact.m1m2.first_layer_width,
                                 self.m2_space + contact.m2m3.first_layer_width, 
                                 self.m3_space + contact.m2m3.second_layer_width)
        
        # Compute the other pmos2 location, but determining offset to overlap the
        # source and drain pins
        self.overlap_offset = self.pmos.get_pin("D").ll() - self.pmos.get_pin("S").ll()

        # Two PMOS devices and a well contact. Separation between each.
        # Enclosure space on the sides.
        self.well_width = 2*self.pmos.active_width + self.pmos.active_contact.width \
                          + 2*drc("active_to_body_active") + 2*drc("well_enclosure_active")

        self.width = self.well_width
        # Height is an input parameter, so it is not recomputed.

        # This is the extra space needed to ensure DRC rules to the active contacts
        extra_contact_space = max(-self.nmos.get_pin("D").by(),0)
        # This is a poly-to-poly of a flipped cell
        self.top_bottom_space = max(0.5*self.m1_width + self.m1_space + extra_contact_space, 
                                    drc("poly_extend_active"), self.poly_space)
        
    def route_supply_rails(self):
        """ Add vdd/gnd rails to the top and bottom. """
        self.add_layout_pin_rect_center(text="gnd",
                                        layer="metal1",
                                        offset=vector(0.5*self.width,0),
                                        width=self.width)

        self.add_layout_pin_rect_center(text="vdd",
                                        layer="metal1",
                                        offset=vector(0.5*self.width,self.height),
                                        width=self.width)

    def create_ptx(self):
        """ 
        Add PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        self.pmos1_inst=self.add_inst(name="pnor2_pmos1",
                                      mod=self.pmos)
        self.connect_inst(["vdd", "A", "net1", "vdd"])

        self.pmos2_inst = self.add_inst(name="pnor2_pmos2",
                                        mod=self.pmos)
        self.connect_inst(["net1", "B", "Z", "vdd"])

        
        self.nmos1_inst=self.add_inst(name="pnor2_nmos1",
                                      mod=self.nmos)
        self.connect_inst(["Z", "A", "gnd", "gnd"])

        self.nmos2_inst=self.add_inst(name="pnor2_nmos2",
                                      mod=self.nmos)
        self.connect_inst(["Z", "B", "gnd", "gnd"])
        

    def place_ptx(self):
        """ 
        Add PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        pmos1_pos = vector(self.pmos.active_offset.x,
                           self.height - self.pmos.active_height - self.top_bottom_space)
        self.pmos1_inst.place(pmos1_pos)

        self.pmos2_pos = pmos1_pos + self.overlap_offset
        self.pmos2_inst.place(self.pmos2_pos)
        
        nmos1_pos = vector(self.pmos.active_offset.x, self.top_bottom_space)
        self.nmos1_inst.place(nmos1_pos)
        
        self.nmos2_pos = nmos1_pos + self.overlap_offset
        self.nmos2_inst.place(self.nmos2_pos)
        
        # Output position will be in between the PMOS and NMOS        
        self.output_pos = vector(0,0.5*(pmos1_pos.y+nmos1_pos.y+self.nmos.active_height))

        # This will help with the wells 
        self.well_pos = vector(0,self.nmos1_inst.uy())
        
    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies """

        self.add_nwell_contact(self.pmos, self.pmos2_pos)
        self.add_pwell_contact(self.nmos, self.nmos2_pos)

        
    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst,"S","gnd")

        self.connect_pin_to_rail(self.nmos2_inst,"D","gnd")

        self.connect_pin_to_rail(self.pmos1_inst,"S","vdd")


    def route_inputs(self):
        """ Route the A and B inputs """
        # Use M2 spaces so we can drop vias on the pins later!
        inputB_yoffset = self.nmos2_pos.y + self.nmos.active_height + self.m2_space + self.m2_width
        self.route_input_gate(self.pmos2_inst, self.nmos2_inst, inputB_yoffset, "B", position="center")
        
        # This will help with the wells and the input/output placement
        self.inputA_yoffset = inputB_yoffset + self.input_spacing
        self.route_input_gate(self.pmos1_inst, self.nmos1_inst, self.inputA_yoffset, "A")

    def route_output(self):
        """ Route the Z output """
        # PMOS2 drain 
        pmos_pin = self.pmos2_inst.get_pin("D")
        # NMOS1 drain
        nmos_pin = self.nmos1_inst.get_pin("D")
        # NMOS2 drain (for output via placement)
        nmos2_pin = self.nmos2_inst.get_pin("D")

        # Go up to metal2 for ease on all output pins
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=pmos_pin.center())
        m1m2_contact=self.add_via_center(layers=("metal1", "via1", "metal2"),
                                         offset=nmos_pin.center())

        
        mid1_offset = vector(pmos_pin.center().x,nmos2_pin.center().y)
        mid2_offset = vector(pmos_pin.center().x,self.inputA_yoffset)
        mid3_offset = mid2_offset + vector(self.m2_width,0)
        
        # PMOS1 to mid-drain to NMOS2 drain
        self.add_path("metal2",[pmos_pin.bc(), mid2_offset, mid3_offset])
        self.add_path("metal2",[nmos_pin.rc(), mid1_offset, mid2_offset])
        # This extends the output to the edge of the cell
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=mid3_offset)
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal1",
                                        offset=mid3_offset,
                                        width=contact.m1m2.first_layer_height,
                                        height=contact.m1m2.first_layer_width)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_rate"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nor2_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        transition_prob = spice["nor2_transition_prob"]
        return transition_prob*(c_load + c_para) 
        
    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets) 
