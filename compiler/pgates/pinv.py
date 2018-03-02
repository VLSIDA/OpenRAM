import contact
import pgate
import debug
from tech import drc, parameter, spice, info
from ptx import ptx
from vector import vector
from math import ceil
from globals import OPTS
from utils import round_to_grid

class pinv(pgate.pgate):
    """
    Pinv generates gds of a parametrically sized inverter. The
    size is specified as the drive size (relative to minimum NMOS) and
    a beta value for choosing the pmos size.  The inverter's cell
    height is usually the same as the 6t library cell and is measured
    from center of rail to rail..  The route_output will route the
    output to the right side of the cell for easier access.
    """
    c = reload(__import__(OPTS.bitcell))
    bitcell = getattr(c, OPTS.bitcell)

    unique_id = 1
    
    def __init__(self, size=1, beta=parameter["beta"], height=bitcell.height, route_output=True):
        # We need to keep unique names because outputting to GDSII
        # will use the last record with a given name. I.e., you will
        # over-write a design in GDS if one has and the other doesn't
        # have poly connected, for example.
        name = "pinv_{}".format(pinv.unique_id)
        pinv.unique_id += 1
        pgate.pgate.__init__(self, name)
        debug.info(2, "create pinv structure {0} with size of {1}".format(name, size))

        self.nmos_size = size
        self.pmos_size = beta*size
        self.beta = beta
        self.height = height # Maybe minimize height if not defined in future?
        self.route_output = False

        self.add_pins()
        self.create_layout()

        # for run-time, we won't check every transitor DRC/LVS independently
        # but this may be uncommented for debug purposes
        #self.DRC_LVS()

    def add_pins(self):
        """ Adds pins for spice netlist """
        self.add_pin_list(["A", "Z", "vdd", "gnd"])

    def create_layout(self):
        """ Calls all functions related to the generation of the layout """

        self.determine_tx_mults()
        self.create_ptx()
        self.setup_layout_constants()
        self.add_supply_rails()
        self.add_ptx()
        self.add_well_contacts()
        self.extend_wells(self.well_pos)
        self.connect_rails()
        self.route_input_gate(self.pmos_inst, self.nmos_inst, self.output_pos.y, "A", rotate=0)
        self.route_outputs()
        

    def determine_tx_mults(self):
        """
        Determines the number of fingers needed to achieve the size within
        the height constraint. This may fail if the user has a tight height.
        """
        # Do a quick sanity check and bail if unlikely feasible height
        # Sanity check. can we make an inverter in the height with minimum tx sizes?
        # Assume we need 3 metal 1 pitches (2 power rails, one between the tx for the drain)
        # plus the tx height
        nmos = ptx(tx_type="nmos")
        pmos = ptx(width=drc["minwidth_tx"], tx_type="pmos")
        tx_height = nmos.poly_height + pmos.poly_height
        # rotated m1 pitch or poly to active spacing
        min_channel = max(contact.poly.width + self.m1_space,
                          contact.poly.width + 2*drc["poly_to_active"])
        # This is the extra space needed to ensure DRC rules to the active contacts
        extra_contact_space = max(-nmos.get_pin("D").by(),0)
        # This is a poly-to-poly of a flipped cell
        self.top_bottom_space = max(0.5*self.m1_width + self.m1_space + extra_contact_space, 
                                    drc["poly_extend_active"], self.poly_space)
        total_height = tx_height + min_channel + 2*self.top_bottom_space
        debug.check(self.height> total_height,"Cell height {0} too small for simple min height {1}.".format(self.height,total_height))

        # Determine the height left to the transistors to determine the number of fingers
        tx_height_available = self.height - min_channel - 2*self.top_bottom_space
        # Divide the height in half. Could divide proportional to beta, but this makes
        # connecting wells of multiple cells easier.
        # Subtract the poly space under the rail of the tx
        nmos_height_available = 0.5 * tx_height_available - 0.5*drc["poly_to_poly"]
        pmos_height_available = 0.5 * tx_height_available - 0.5*drc["poly_to_poly"]

        debug.info(2,"Height avail {0} PMOS height {1} NMOS height {2}".format(tx_height_available, nmos_height_available, pmos_height_available))

        # Determine the number of mults for each to fit width into available space
        self.nmos_width = self.nmos_size*drc["minwidth_tx"]
        self.pmos_width = self.pmos_size*drc["minwidth_tx"]
        nmos_required_mults = max(int(ceil(self.nmos_width/nmos_height_available)),1)
        pmos_required_mults = max(int(ceil(self.pmos_width/pmos_height_available)),1)
        # The mults must be the same for easy connection of poly
        self.tx_mults = max(nmos_required_mults, pmos_required_mults)

        # Recompute each mult width and check it isn't too small
        # This could happen if the height is narrow and the size is small
        # User should pick a bigger size to fix it...
        # We also need to round the width to the grid or we will end up with LVS property
        # mismatch errors when fingers are not a grid length and get rounded in the offset geometry.
        self.nmos_width = round_to_grid(self.nmos_width / self.tx_mults)
        debug.check(self.nmos_width>=drc["minwidth_tx"],"Cannot finger NMOS transistors to fit cell height.")
        self.pmos_width = round_to_grid(self.pmos_width / self.tx_mults)
        debug.check(self.pmos_width>=drc["minwidth_tx"],"Cannot finger PMOS transistors to fit cell height.")
        

    def setup_layout_constants(self):
        """
        Pre-compute some handy layout parameters.
        """

        # the well width is determined the multi-finger PMOS device width plus
        # the well contact width and half well enclosure on both sides
        self.well_width = self.pmos.active_width + self.pmos.active_contact.width \
                          + drc["active_to_body_active"] + 2*drc["well_enclosure_active"]
        self.width = self.well_width
        # Height is an input parameter, so it is not recomputed. 
        

        
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
        
        # place PMOS so it is half a poly spacing down from the top
        self.pmos_pos = self.pmos.active_offset.scale(1,0) \
                        + vector(0, self.height-self.pmos.active_height-self.top_bottom_space)
        self.pmos_inst=self.add_inst(name="pinv_pmos",
                                     mod=self.pmos,
                                     offset=self.pmos_pos)
        self.connect_inst(["Z", "A", "vdd", "vdd"])

        # place NMOS so that it is half a poly spacing up from the bottom
        self.nmos_pos = self.nmos.active_offset.scale(1,0) + vector(0,self.top_bottom_space)
        self.nmos_inst=self.add_inst(name="pinv_nmos",
                                     mod=self.nmos,
                                     offset=self.nmos_pos)
        self.connect_inst(["Z", "A", "gnd", "gnd"])


        # Output position will be in between the PMOS and NMOS drains
        pmos_drain_pos = self.pmos_inst.get_pin("D").ll()
        nmos_drain_pos = self.nmos_inst.get_pin("D").ul()
        self.output_pos = vector(0,0.5*(pmos_drain_pos.y+nmos_drain_pos.y))

        # This will help with the wells 
        self.well_pos = vector(0,self.nmos_inst.uy())
        


    def route_outputs(self):
        """ Route the output (drains) together. Optionally, routes output to edge. """

        # Get the drain pins
        nmos_drain_pin = self.nmos_inst.get_pin("D")
        pmos_drain_pin = self.pmos_inst.get_pin("D")

        # Pick point at right most of NMOS and connect down to PMOS
        nmos_drain_pos = nmos_drain_pin.lr() - vector(0.5*self.m1_width,0)
        pmos_drain_pos = vector(nmos_drain_pos.x, pmos_drain_pin.bc().y)
        self.add_path("metal1",[nmos_drain_pos,pmos_drain_pos])

        # Remember the mid for the output
        mid_drain_offset = vector(nmos_drain_pos.x,self.output_pos.y)

        if self.route_output == True:
            # This extends the output to the edge of the cell
            output_offset = mid_drain_offset.scale(0,1) + vector(self.width,0)
            self.add_layout_pin_center_segment(text="Z",
                                               layer="metal1",
                                               start=mid_drain_offset,
                                               end=output_offset)
        else:
            # This leaves the output as an internal pin (min sized)
            self.add_layout_pin_center_rect(text="Z",
                                            layer="metal1",
                                            offset=mid_drain_offset + vector(0.5*self.m1_width,0))


    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies """

        self.add_nwell_contact(self.pmos, self.pmos_pos)

        self.add_pwell_contact(self.nmos, self.nmos_pos)

    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        self.connect_pin_to_rail(self.nmos_inst,"S","gnd")

        self.connect_pin_to_rail(self.pmos_inst,"S","vdd")
        

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
        power_leak = spice["inv_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        c_load = load
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        transistion_prob = spice["inv_transisition_prob"]
        return transistion_prob*(c_load + c_para) 