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

class pnand3(pgate.pgate):
    """
    This module generates gds of a parametrically sized 2-input nand.
    This model use ptx to generate a 2-input nand within a cetrain height.
    """
    def __init__(self, name, size=1, height=None):
        """ Creates a cell for a simple 3 input nand """

        debug.info(2, "creating pnand3 structure {0} with size of {1}".format(name, size))
        self.add_comment("size: {}".format(size))

        # We have trouble pitch matching a 3x sizes to the bitcell...
        # If we relax this, we could size this better.
        self.size = size
        self.nmos_size = 2*size
        self.pmos_size = parameter["beta"]*size
        self.nmos_width = self.nmos_size*drc("minwidth_tx")
        self.pmos_width = self.pmos_size*drc("minwidth_tx")

        # FIXME: Allow these to be sized
        debug.check(size==1,"Size 1 pnand3 is only supported now.")
        self.tx_mults = 1

        # Creates the netlist and layout
        pgate.pgate.__init__(self, name, height)

        
    def add_pins(self):
        """ Adds pins for spice netlist """
        pin_list = ["A", "B", "C", "Z", "vdd", "gnd"]
        dir_list = ["INPUT", "INPUT", "INPUT", "OUTPUT", "POWER", "GROUND"]
        self.add_pin_list(pin_list, dir_list)

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
        
        # Compute the overlap of the source and drain pins
        self.overlap_offset = self.pmos.get_pin("D").ll() - self.pmos.get_pin("S").ll()

        # Two PMOS devices and a well contact. Separation between each.
        # Enclosure space on the sides.
        self.well_width = 3*self.pmos.active_width + self.pmos.active_contact.width \
                          + 2*drc("active_to_body_active") + 2*drc("well_enclosure_active") \
                          - self.overlap_offset.x
        self.width = self.well_width
        # Height is an input parameter, so it is not recomputed.

        # This will help with the wells and the input/output placement
        self.output_pos = vector(0,0.5*self.height)

        # This is the extra space needed to ensure DRC rules to the active contacts
        nmos = factory.create(module_type="ptx", tx_type="nmos")
        extra_contact_space = max(-nmos.get_pin("D").by(),0)
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
        Create the PMOS and NMOS in the netlist.
        """

        self.pmos1_inst=self.add_inst(name="pnand3_pmos1",
                                      mod=self.pmos)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos2_inst = self.add_inst(name="pnand3_pmos2",
                                        mod=self.pmos)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

        self.pmos3_inst = self.add_inst(name="pnand3_pmos3",
                                        mod=self.pmos)
        self.connect_inst(["Z", "C", "vdd", "vdd"])
        
        self.nmos1_inst=self.add_inst(name="pnand3_nmos1",
                                      mod=self.nmos)
        self.connect_inst(["Z", "C", "net1", "gnd"])

        self.nmos2_inst=self.add_inst(name="pnand3_nmos2",
                                      mod=self.nmos)
        self.connect_inst(["net1", "B", "net2", "gnd"])
        
        self.nmos3_inst=self.add_inst(name="pnand3_nmos3",
                                      mod=self.nmos)
        self.connect_inst(["net2", "A", "gnd", "gnd"])
        

    def place_ptx(self):
        """ 
        Place the PMOS and NMOS in the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        pmos1_pos = vector(self.pmos.active_offset.x,
                           self.height - self.pmos.active_height - self.top_bottom_space)
        self.pmos1_inst.place(pmos1_pos)

        pmos2_pos = pmos1_pos + self.overlap_offset
        self.pmos2_inst.place(pmos2_pos)

        self.pmos3_pos = pmos2_pos + self.overlap_offset
        self.pmos3_inst.place(self.pmos3_pos)
        
        
        nmos1_pos = vector(self.pmos.active_offset.x, self.top_bottom_space)
        self.nmos1_inst.place(nmos1_pos)

        nmos2_pos = nmos1_pos + self.overlap_offset
        self.nmos2_inst.place(nmos2_pos)
        
        self.nmos3_pos = nmos2_pos + self.overlap_offset
        self.nmos3_inst.place(self.nmos3_pos)
        
        # This should be placed at the top of the NMOS well
        self.well_pos = vector(0,self.nmos1_inst.uy())
        
    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies """

        self.add_nwell_contact(self.pmos, self.pmos3_pos)
        self.add_pwell_contact(self.nmos, self.nmos3_pos)

        
    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst,"S","gnd")

        self.connect_pin_to_rail(self.pmos1_inst,"S","vdd")        

        self.connect_pin_to_rail(self.pmos2_inst,"D","vdd")

    def route_inputs(self):
        """ Route the A and B inputs """
        # wire space or wire and one contact space
        metal_spacing = max(self.m1_space + self.m1_width, self.m2_space + self.m2_width,
                            self.m1_space + 0.5*contact.poly.width + 0.5*self.m1_width)

        active_spacing = max(self.m1_space, 0.5*contact.poly.first_layer_width + drc("poly_to_active"))
        inputC_yoffset = self.nmos3_pos.y + self.nmos.active_height + active_spacing
        self.route_input_gate(self.pmos3_inst, self.nmos3_inst, inputC_yoffset, "C", position="center")

        inputB_yoffset = inputC_yoffset + metal_spacing
        self.route_input_gate(self.pmos2_inst, self.nmos2_inst, inputB_yoffset, "B", position="center")

        self.inputA_yoffset = inputB_yoffset + metal_spacing
        self.route_input_gate(self.pmos1_inst, self.nmos1_inst, self.inputA_yoffset, "A", position="center")

        

    def route_output(self):
        """ Route the Z output """
        # PMOS1 drain 
        pmos1_pin = self.pmos1_inst.get_pin("D")
        # PMOS3 drain 
        pmos3_pin = self.pmos3_inst.get_pin("D")
        # NMOS3 drain
        nmos3_pin = self.nmos3_inst.get_pin("D")        

        # Go up to metal2 for ease on all output pins
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=pmos1_pin.center())
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=pmos3_pin.center())
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=nmos3_pin.center())
        
        # PMOS3 and NMOS3 are drain aligned
        self.add_path("metal2",[pmos3_pin.bc(), nmos3_pin.uc()])
        # Route in the A input track (top track)
        mid_offset = vector(nmos3_pin.center().x,self.inputA_yoffset)
        self.add_path("metal2",[pmos1_pin.bc(), mid_offset, nmos3_pin.uc()])        

        # This extends the output to the edge of the cell
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=mid_offset)
        self.add_layout_pin_rect_center(text="Z",
                                        layer="metal1",
                                        offset=mid_offset,
                                        width=contact.m1m2.first_layer_width,
                                        height=contact.m1m2.first_layer_height)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_rate"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["nand3_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        transition_prob = spice["nand3_transition_prob"]
        return transition_prob*(c_load + c_para) 

    def input_load(self):
        """Return the relative input capacitance of a single input"""
        return self.nmos_size+self.pmos_size
        
    def get_stage_effort(self, cout, inp_is_rise=True):
        """Returns an object representing the parameters for delay in tau units.
           Optional is_rise refers to the input direction rise/fall. Input inverted by this stage.
        """
        parasitic_delay = 3 
        return logical_effort.logical_effort(self.name, self.size, self.input_load(), cout, parasitic_delay, not inp_is_rise)

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets) 
