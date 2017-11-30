import contact
import design
import debug
from tech import drc, parameter, spice, info
from ptx import ptx
from vector import vector
from math import ceil
from globals import OPTS

class pinv(design.design):
    """
    Pinv generates gds of a parametrically sized inverter. The
    size is specified as the drive size (relative to minimum NMOS) and
    a beta value for choosing the pmos size.  The inverter's cell
    height is usually the same as the 6t library cell and is measured
    from center of rail to rail..  The route_output will route the
    output to the right side of the cell for easier access.
    """
    c = reload(__import__(OPTS.config.bitcell))
    bitcell = getattr(c, OPTS.config.bitcell)

    unique_id = 1
    
    def __init__(self, size=1, beta=parameter["pinv_beta"], height=bitcell.height, route_output=True):
        # We need to keep unique names because outputting to GDSII
        # will use the last record with a given name. I.e., you will
        # over-write a design in GDS if one has and the other doesn't
        # have poly connected, for example.
        name = "pinv{0}".format(pinv.unique_id)
        pinv.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "create pinv structure {0} with size of {1}".format(name, size))

        self.nmos_size = size
        self.pmos_size = beta*size
        self.beta = beta
        self.height = height
        self.route_output = route_output

        self.add_pins()
        self.create_layout()

        # for run-time, we won't check every transitor DRC/LVS independently
        # but this may be uncommented for debug purposes
        #self.DRC_LVS()

    def add_pins(self):
        """Adds pins for spice netlist"""
        self.add_pin_list(["A", "Z", "vdd", "gnd"])

    def create_layout(self):
        """Calls all functions related to the generation of the layout"""

        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact = contact.contact(("poly", "contact", "metal1"))
        self.m1m2_via = contact.contact(("metal1", "via1", "metal2"))

        self.determine_tx_mults()
        self.create_ptx()
        self.setup_layout_constants()
        self.add_supply_rails()
        self.add_ptx()

        # These aren't for instantiating, but we use them to get the dimensions
        # self.nwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
        #                                      dimensions=(1, self.pmos.num_contacts))
        # self.pwell_contact = contact.contact(layer_stack=("active", "contact", "metal1"),
        #                                      dimensions=(1, self.nmos.num_contacts))

        self.extend_wells()
        #self.extend_active()
        self.add_well_contacts()
        self.connect_rails()
        self.route_input_gate()
        self.route_output_drain()
        

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
        pmos = ptx(width=self.beta*drc["minwidth_tx"], tx_type="pmos")
        tx_height = nmos.height + pmos.height
        # rotated m1 pitch
        m1_pitch = self.poly_contact.width + drc["metal1_to_metal1"]
        metal_height = 4 * m1_pitch # This could be computed more accurately
        debug.check(self.height>tx_height + metal_height,"Cell height too small for our simple design rules.")

        # Determine the height left to the transistors to determine the number of fingers
        tx_height_available = self.height - metal_height
        # Divide the height in half. Could divide proportional to beta, but this makes
        # connecting wells of multiple cells easier.
        nmos_height_available = 0.5 * tx_height_available
        pmos_height_available = 0.5 * tx_height_available
        

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
        self.nmos_width = self.nmos_width / self.tx_mults
        debug.check(self.nmos_width>=drc["minwidth_tx"],"Cannot finger NMOS transistors to fit cell height.")
        self.pmos_width = self.pmos_width / self.tx_mults
        debug.check(self.pmos_width>=drc["minwidth_tx"],"Cannot finger PMOS transistors to fit cell height.")        

    def setup_layout_constants(self):
        """
        Pre-compute some handy layout parameters.
        """

        self.m1_width = drc["minwidth_metal1"]
        
        # the well width is determined the multi-finger PMOS device width plus
        # the well contact width and half well enclosure on both sides
        self.well_width = self.pmos.active_width + self.pmos.active_contact.width \
                          + drc["active_to_body_active"] + 2*drc["well_enclosure_active"]
        self.width = self.well_width
        # Height is an input parameter

        # This will help with the wells and the input/output placement
        self.middle_position = vector(0,0.5*self.height)

        
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
        pmos_position = vector(0,self.height-self.pmos.height-0.5*drc["poly_to_poly"])
        self.pmos_inst=self.add_inst(name="pinv_pmos",
                                     mod=self.pmos,
                                     offset=pmos_position)
        self.connect_inst(["Z", "A", "vdd", "vdd"])

        # place NMOS so that it is half a poly spacing up from the bottom
        nmos_position = vector(0,self.nmos.height+0.5*drc["poly_to_poly"])
        self.nmos_inst=self.add_inst(name="pinv_nmos",
                                     mod=self.nmos,
                                     offset=nmos_position,
                                     mirror="MX")
        self.connect_inst(["Z", "A", "gnd", "gnd"])


    def extend_wells(self):
        """ Extend the n/p wells to cover whole cell """

        nwell_height = self.height - self.middle_position.y
        if info["has_nwell"]:
            self.add_rect(layer="nwell",
                          offset=self.middle_position,
                          width=self.well_width,
                          height=nwell_height)
        self.add_rect(layer="vtg",
                      offset=self.middle_position,
                      width=self.well_width,
                      height=nwell_height)

        if info["has_pwell"]:
            self.add_rect(layer="pwell",
                          offset=vector(0,0),
                          width=self.well_width,
                          height=self.middle_position.y)
        self.add_rect(layer="vtg",
                      offset=vector(0,0),
                      width=self.well_width,
                      height=self.middle_position.y)

    # def extend_active(self):
    #     """Extends the active area for n/p mos for the addition of the n/p well taps"""
    #     # calculates the new active width that includes the well_taps
    #     self.active_width = self.pmos.active_width \
    #                       + drc["active_to_body_active"] \
    #                       + self.pmos.active_contact.width

    #     # Calculates the coordinates of the bottom left corner of active area
    #     # of the pmos
    #     offset = self.pmos_position + self.pmos.active_position
    #     self.add_rect(layer="active",
    #                   offset=offset,
    #                   width=self.active_width,
    #                   height=self.pmos.active_height)

    #     # Determines where the active of the well portion starts to add the
    #     # implant
    #     offset = offset + vector(self.pmos.active_width,0)
    #     implant_width = self.active_width - self.pmos.active_width
    #     self.add_rect(layer="nimplant",
    #                   offset=offset,
    #                   width=implant_width,
    #                   height=self.pmos.active_height)

    #     # Calculates the coordinates of the bottom left corner of active area
    #     # of the nmos
    #     offset = self.nmos_position + self.nmos.active_position
    #     self.add_rect(layer="active",
    #                   offset=offset,
    #                   width=self.active_width,
    #                   height=self.nmos.active_height)

    #     # Determines where the active of the well portion starts to add the
    #     # implant
    #     offset = offset + vector(self.pmos.active_width,0)
    #     implant_width = self.active_width - self.nmos.active_width
    #     self.add_rect(layer="pimplant",
    #                   offset=offset,
    #                   width=implant_width,
    #                   height=self.nmos.active_height)


    def route_input_gate(self):
        """Routes the input gate to the left side of the cell for access"""
        nmos_gate_pin = self.nmos_inst.get_pin("G")
        pmos_gate_pin = self.pmos_inst.get_pin("G")

        # Pick point on the left of NMOS and connect down to PMOS
        nmos_gate_pos = nmos_gate_pin.ll() + vector(0.5*drc["minwidth_poly"],0)
        pmos_gate_pos = vector(nmos_gate_pos.x,pmos_gate_pin.bc().y)
        self.add_path("poly",[nmos_gate_pos,pmos_gate_pos])

        # Add the via to the cell midpoint along the gate
        left_gate_offset = vector(nmos_gate_pin.lx(),self.middle_position.y)
        contact_offset = left_gate_offset - vector(0.5*self.poly_contact.height,0)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                offset=contact_offset,
                                rotate=90)
        self.add_layout_pin_center_segment(text="A",
                                           layer="metal1",
                                           start=left_gate_offset.scale(0,1),
                                           end=left_gate_offset)

        # This is to ensure that the contact is connected to the gate
        mid_point = contact_offset.scale(0.5,1)+left_gate_offset.scale(0.5,0)
        self.add_rect_center(layer="poly",
                             offset=mid_point,
                             height=self.poly_contact.first_layer_width,
                             width=left_gate_offset.x-contact_offset.x)
        

    def route_output_drain(self):
        """ Route the output (drains) together. Optionally, routes output to edge. """

        # Get the drain pins
        nmos_drain_pin = self.nmos_inst.get_pin("D")
        pmos_drain_pin = self.pmos_inst.get_pin("D")

        # Pick point in center of NMOS and connect down to PMOS
        nmos_drain_pos = nmos_drain_pin.uc()
        pmos_drain_pos = vector(nmos_drain_pin.uc().x,pmos_drain_pin.bc().y)
        self.add_path("metal1",[nmos_drain_pos,pmos_drain_pos])

        # Remember the mid for the output
        mid_drain_offset = vector(nmos_drain_pos.x,self.middle_position.y)
        output_length = self.width - mid_drain_offset.x
        
        if self.route_output == True:
            # This extends the output to the edge of the cell
            output_offset = mid_drain_offset.scale(0,1) + vector(self.width,0)
            self.add_layout_pin_center_segment(text="Z",
                                               layer="metal1",
                                               start=mid_drain_offset,
                                               end=output_offset)
        else:
            # This leaves the output as an internal pin (min sized)
            self.add_layout_pin(text="Z",
                                layer="metal1",
                                offset=mid_drain_offset)


    def add_well_contacts(self):
        """ Add n/p well taps to the layout and connect to supplies"""
        
        layer_stack = ("active", "contact", "metal1")
        
        # Lower left of the NMOS active
        nmos_pos = self.nmos_inst.ll() + self.nmos.active_offset
        # To the right a spacing away from the nmos right active edge
        nwell_contact_offset = self.nmos.active_width + drc["active_to_body_active"]
        nwell_offset = nmos_pos + vector(nwell_contact_offset, 0)
        # Offset by half a contact in x and y
        nwell_offset += vector(0.5*self.nmos.active_contact.first_layer_width,
                               0.5*self.nmos.active_contact.first_layer_height)
        self.nwell_contact=self.add_contact_center(layers=layer_stack,
                                                   offset=nwell_offset,
                                                   size=(1,self.nmos.num_contacts))
        self.add_path("metal1",[nwell_offset,nwell_offset.scale(1,0)])
        # Now add the full active and implant for the PMOS
        nwell_offset = nmos_pos + vector(self.nmos.active_width,0)
        nwell_contact_width = drc["active_to_body_active"] + self.nmos.active_contact.width
        self.add_rect(layer="active",
                      offset=nwell_offset,
                      width=nwell_contact_width,
                      height=self.nmos.active_height)
        self.add_rect(layer="pimplant",
                      offset=nwell_offset,
                      width=nwell_contact_width,
                      height=self.nmos.active_height)


        
        # Lower left of the PMOS active
        pmos_pos = self.pmos_inst.ll() + self.pmos.active_offset
        pwell_contact_offset = self.pmos.active_width + drc["active_to_body_active"]
        # To the right a spacing away from the pmos right active edge
        pwell_offset = pmos_pos + vector(pwell_contact_offset, 0)
        # Offset by half a contact
        pwell_offset += vector(0.5*self.pmos.active_contact.first_layer_width,
                               0.5*self.pmos.active_contact.first_layer_height)
        self.pwell_contact=self.add_contact_center(layers=layer_stack,
                                                   offset=pwell_offset,
                                                   size=(1,self.pmos.num_contacts))
        self.add_path("metal1",[pwell_offset,vector(pwell_offset.x,self.height)])
        # Now add the full active and implant for the PMOS
        pwell_offset = pmos_pos + vector(self.pmos.active_width,0)        
        pwell_contact_width = drc["active_to_body_active"] + self.pmos.active_contact.width        
        self.add_rect(layer="active",
                      offset=pwell_offset,
                      width=pwell_contact_width,
                      height=self.pmos.active_height)
        self.add_rect(layer="nimplant",
                      offset=pwell_offset,
                      width=pwell_contact_width,
                      height=self.pmos.active_height)



    def connect_rails(self):
        """ Connect the nmos and pmos to its respective power rails """

        nmos_source_pin = self.nmos_inst.get_pin("S")
        gnd_pin = self.get_pin("gnd")
        # Only if they don't overlap already
        if gnd_pin.uy() < nmos_source_pin.by():
            self.add_rect(layer="metal1",
                          offset=nmos_source_pin.ll(),
                          height=-1*nmos_source_pin.by(),
                          width=nmos_source_pin.width())

        pmos_source_pin = self.pmos_inst.get_pin("S")
        vdd_pin = self.get_pin("vdd")
        # Only if they don't overlap already
        if vdd_pin.by() > pmos_source_pin.uy():
            self.add_rect(layer="metal1",
                          offset=pmos_source_pin.ll(),
                          height=vdd_pin.by()-pmos_source_pin.by(),
                          width=pmos_source_pin.width())
    

    def input_load(self):
        return ((self.nmos_size+self.pmos_size)/parameter["min_tx_size"])*spice["min_tx_gate_c"]

    def analytical_delay(self, slew, load=0.0):
        from tech import spice
        r = spice["min_tx_r"]/(self.nmos_size/parameter["min_tx_size"])
        c_para = spice["min_tx_drain_c"]*(self.nmos_size/parameter["min_tx_size"])#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
