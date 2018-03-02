import contact
import pgate
import debug
from tech import drc, parameter, spice
from ptx import ptx
from vector import vector
from globals import OPTS

class pnand2(pgate.pgate):
    """
    This module generates gds of a parametrically sized 2-input nand.
    This model use ptx to generate a 2-input nand within a cetrain height.
    """

    c = reload(__import__(OPTS.bitcell))
    bitcell = getattr(c, OPTS.bitcell)

    unique_id = 1
    
    def __init__(self, size=1, height=bitcell.height):
        """ Creates a cell for a simple 2 input nand """
        name = "pnand2_{0}".format(pnand2.unique_id)
        pnand2.unique_id += 1
        pgate.pgate.__init__(self, name)
        debug.info(2, "create pnand2 structure {0} with size of {1}".format(name, size))

        self.nmos_size = 2*size
        self.pmos_size = parameter["beta"]*size
        self.nmos_width = self.nmos_size*drc["minwidth_tx"]
        self.pmos_width = self.pmos_size*drc["minwidth_tx"]
        self.height = height

        # FIXME: Allow these to be sized
        debug.check(size==1,"Size 1 pnand2 is only supported now.")
        self.tx_mults = 1

        self.add_pins()
        self.create_layout()
        #self.DRC_LVS()

        
    def add_pins(self):
        """ Adds pins for spice netlist """
        self.add_pin_list(["A", "B", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ Calls all functions related to the generation of the layout """

        self.create_ptx()
        self.setup_layout_constants()
        self.add_supply_rails()
        self.add_ptx()
        self.connect_rails()
        self.add_well_contacts()
        self.extend_wells(self.well_pos)
        self.route_inputs()
        self.route_output()

    def create_ptx(self):
        """ Create the PMOS and NMOS transistors. """
        self.nmos = ptx(width=self.nmos_width,
                        mults=self.tx_mults,
                        tx_type="nmos",
                        connect_poly=True,
                        connect_active=True)
        self.add_mod(self.nmos)

        self.pmos = ptx(width=self.pmos_width,
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
        self.well_width = 2*self.pmos.active_width + contact.active.width \
                          + 2*drc["active_to_body_active"] + 2*drc["well_enclosure_active"]

        self.width = self.well_width
        # Height is an input parameter, so it is not recomputed.

        # This is the extra space needed to ensure DRC rules to the active contacts
        extra_contact_space = max(-self.nmos.get_pin("D").by(),0)
        # This is a poly-to-poly of a flipped cell
        self.top_bottom_space = max(0.5*self.m1_width + self.m1_space + extra_contact_space, 
                                    drc["poly_extend_active"], self.poly_space)
        
    def add_supply_rails(self):
        """ Add vdd/gnd rails to the top and bottom. """
        self.add_layout_pin_center_rect(text="gnd",
                                        layer="metal1",
                                        offset=vector(0.5*self.width,0),
                                        width=self.width)

        self.add_layout_pin_center_rect(text="vdd",
                                        layer="metal1",
                                        offset=vector(0.5*self.width,self.height),
                                        width=self.width)

    def add_ptx(self):
        """ 
        Add PMOS and NMOS to the layout at the upper-most and lowest position
        to provide maximum routing in channel
        """

        pmos1_pos = vector(self.pmos.active_offset.x,
                           self.height - self.pmos.active_height - self.top_bottom_space)
        self.pmos1_inst=self.add_inst(name="pnand2_pmos1",
                                      mod=self.pmos,
                                      offset=pmos1_pos)
        self.connect_inst(["vdd", "A", "Z", "vdd"])

        self.pmos2_pos = pmos1_pos + self.overlap_offset
        self.pmos2_inst = self.add_inst(name="pnand2_pmos2",
                                        mod=self.pmos,
                                        offset=self.pmos2_pos)
        self.connect_inst(["Z", "B", "vdd", "vdd"])

        
        nmos1_pos = vector(self.pmos.active_offset.x, self.top_bottom_space)
        self.nmos1_inst=self.add_inst(name="pnand2_nmos1",
                                      mod=self.nmos,
                                      offset=nmos1_pos)
        self.connect_inst(["Z", "B", "net1", "gnd"])

        self.nmos2_pos = nmos1_pos + self.overlap_offset
        self.nmos2_inst=self.add_inst(name="pnand2_nmos2",
                                      mod=self.nmos,
                                      offset=self.nmos2_pos)
        self.connect_inst(["net1", "A", "gnd", "gnd"])

        # Output position will be in between the PMOS and NMOS        
        self.output_pos = vector(0,0.5*(pmos1_pos.y+nmos1_pos.y+self.nmos.active_height))

        # This will help with the wells 
        self.well_pos = vector(0,self.nmos1_inst.uy())
        
    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies AFTER the wells are created """

        self.add_nwell_contact(self.pmos, self.pmos2_pos)
        self.add_pwell_contact(self.nmos, self.nmos2_pos)

        
    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos1_inst,"S","gnd")

        self.connect_pin_to_rail(self.pmos1_inst,"S","vdd")        

        self.connect_pin_to_rail(self.pmos2_inst,"D","vdd")

    def route_inputs(self):
        """ Route the A and B inputs """
        inputB_yoffset = self.nmos2_pos.y + self.nmos.active_height + self.m2_space + 0.5*self.m2_width
        self.route_input_gate(self.pmos2_inst, self.nmos2_inst, inputB_yoffset, "B", position="center")
        
        # This will help with the wells and the input/output placement
        self.inputA_yoffset = inputB_yoffset + self.input_spacing
        self.route_input_gate(self.pmos1_inst, self.nmos1_inst, self.inputA_yoffset, "A")

        
    def route_output(self):
        """ Route the Z output """
        # PMOS1 drain 
        pmos_pin = self.pmos1_inst.get_pin("D")
        # NMOS2 drain
        nmos_pin = self.nmos2_inst.get_pin("D")        
        # Output pin
        mid_offset = vector(nmos_pin.center().x,self.inputA_yoffset)
        
        self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                offset=pmos_pin.center())
        self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                offset=nmos_pin.center())
        self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                offset=mid_offset,
                                rotate=90)

        # PMOS1 to mid-drain to NMOS2 drain
        self.add_path("metal2",[pmos_pin.bc(), mid_offset, nmos_pin.uc()])

        # This extends the output to the edge of the cell
        self.add_layout_pin_center_rect(text="Z",
                                        layer="metal1",
                                        offset=mid_offset,
                                        width=contact.m1m2.first_layer_height,
                                        height=contact.m1m2.first_layer_width)




    def input_load(self):
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def analytical_delay(self, slew, load=0.0):
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
        
    def analytical_power(self, proc, vdd, temp, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_rate"]
        power_dyn = c_eff*vdd*vdd*freq
        power_leak = spice["nand2_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        transistion_prob = spice["nand2_transisition_prob"]
        return transistion_prob*(c_load + c_para) 
