import debug
import design
from tech import drc
from pinv import pinv
from contact import contact
from bitcell_array import bitcell_array
from nor_2 import nor_2
from ptx import ptx
from vector import vector
from globals import OPTS

class replica_bitline(design.design):
    """
    Generate a module that simulate the delay of control logic 
    and bit line charging.
    Used for memory timing control
    """

    def __init__(self, rows, name="replica_bitline"):
        design.design.__init__(self, name)

        g = reload(__import__(OPTS.config.delay_chain))
        self.mod_delay_chain = getattr(g, OPTS.config.delay_chain)

        g = reload(__import__(OPTS.config.replica_bitcell))
        self.mod_replica_bitcell = getattr(g, OPTS.config.replica_bitcell)

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)

        for pin in ["en", "out", "vdd", "gnd"]:
            self.add_pin(pin)
        self.rows = rows

        self.create_modules()
        self.calculate_module_offsets()
        self.add_modules()
        self.route()
        self.add_layout_pins()

        self.DRC_LVS()

    def calculate_module_offsets(self):
        """ Calculate all the module offsets """
        
        # These aren't for instantiating, but we use them to get the dimensions
        self.active_contact = contact(layer_stack=("active", "contact", "poly"))
        self.poly_contact = contact(layer_stack=("poly", "contact", "metal1"))
        self.poly_contact_offset = vector(0.5*self.poly_contact.width,0.5*self.poly_contact.height)
        self.m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        self.m2m3_via = contact(layer_stack=("metal2", "via2", "metal3"))

        # M1/M2 routing pitch is based on contacted pitch
        self.m1_pitch = max(self.m1m2_via.width,self.m1m2_via.height) + max(drc["metal1_to_metal1"],drc["metal2_to_metal2"])
        self.m2_pitch = max(self.m2m3_via.width,self.m2m3_via.height) + max(drc["metal2_to_metal2"],drc["metal3_to_metal3"])
        
        # This corrects the offset pitch difference between M2 and M1
        self.offset_fix = vector(0.5*(drc["minwidth_metal2"]-drc["minwidth_metal1"]),0)

        # delay chain will be rotated 90, so move it over a width
        # we move it up a inv height just for some routing room
        self.rbl_inv_offset = vector(self.delay_chain.height, self.inv.width)
        # access TX goes right on top of inverter, leave space for an inverter which is
        # about the same as a TX. We'll need to add rails though.
        self.access_tx_offset = vector(1.5*self.inv.height,self.rbl_inv_offset.y) + vector(0,2.25*self.inv.width)
        self.delay_chain_offset = self.rbl_inv_offset + vector(0,4*self.inv.width)

        # Replica bitline and such are not rotated, but they must be placed far enough
        # away from the delay chain/inverter with space for three M2 tracks
        self.bitcell_offset = self.rbl_inv_offset + vector(2*self.m2_pitch, 0) + vector(0, self.bitcell.height + self.inv.width)

        self.rbl_offset = self.bitcell_offset

        
        self.height = self.rbl_offset.y + self.rbl.height + self.m2_pitch
        self.width = self.rbl_offset.x + self.bitcell.width


    def create_modules(self):
        """ Create modules for later instantiation """
        self.bitcell = self.replica_bitcell = self.mod_replica_bitcell()
        self.add_mod(self.bitcell)

        # This is the replica bitline load column that is the height of our array
        self.rbl = bitcell_array(name="bitline_load", cols=1, rows=self.rows)
        self.add_mod(self.rbl)
        
        self.delay_chain = self.mod_delay_chain([1, 1, 1])
        self.add_mod(self.delay_chain)

        self.inv = pinv()
        self.add_mod(self.inv)

        self.access_tx = ptx(tx_type="pmos")
        self.add_mod(self.access_tx)

    def add_modules(self):
        """ Add all of the module instances in the logical netlist """
        # This is the threshold detect inverter on the output of the RBL
        self.rbl_inv_inst=self.add_inst(name="rbl_inv",
                                        mod=self.inv,
                                        offset=self.rbl_inv_offset+vector(0,self.inv.width),
                                        rotate=270,
                                        mirror="MX")
        self.connect_inst(["bl[0]", "out", "vdd", "gnd"])

        self.tx_inst=self.add_inst(name="rbl_access_tx",
                                   mod=self.access_tx,
                                   offset=self.access_tx_offset,
                                   rotate=90)
        # D, G, S, B
        self.connect_inst(["vdd", "delayed_en", "bl[0]", "vdd"])
        # add the well and poly contact

        self.dc_inst=self.add_inst(name="delay_chain",
                                   mod=self.delay_chain,
                                   offset=self.delay_chain_offset,
                                   rotate=90)
        self.connect_inst(["en", "delayed_en", "vdd", "gnd"])

        self.rbc_inst=self.add_inst(name="bitcell",
                                    mod=self.replica_bitcell,
                                    offset=self.bitcell_offset,
                                    mirror="MX")
        self.connect_inst(["bl[0]", "br[0]", "delayed_en", "vdd", "gnd"])

        self.rbl_inst=self.add_inst(name="load",
                                    mod=self.rbl,
                                    offset=self.rbl_offset)
        self.connect_inst(["bl[0]", "br[0]"] + ["gnd"]*self.rows + ["vdd", "gnd"])
        



    def route(self):
        """ Connect all the signals together """
        self.route_gnd()
        self.route_vdd()
        self.route_access_tx()


    def route_access_tx(self):
        # GATE ROUTE
        # 1. Add the poly contact and nwell enclosure
        # Determines the y-coordinate of where to place the gate input poly pin
        # (middle in between the pmos and nmos)

        # finds the lower right of the poly gate
        poly_offset = self.access_tx_offset + self.access_tx.poly_positions[0].rotate_scale(-1,1)
        # This centers the contact on the poly
        contact_offset = poly_offset.scale(0,1) + self.dc_inst.get_pin("out").ll().scale(1,0) \
                         + vector(-drc["poly_extend_contact"], -0.5*self.poly_contact.height + 0.5*drc["minwidth_poly"])
        self.add_contact(layers=("poly", "contact", "metal1"),
                         offset=contact_offset)
        self.add_rect(layer="poly",
                      offset=poly_offset,
                      width=contact_offset.x-poly_offset.x,
                      height=drc["minwidth_poly"])
        nwell_offset = self.rbl_inv_offset + vector(-self.inv.height,self.inv.width)
        self.add_rect(layer="nwell",
                      offset=nwell_offset,
                      width=0.5*self.inv.height,
                      height=self.delay_chain_offset.y-nwell_offset.y)

        # 2. Route delay chain output to access tx gate
        delay_en_offset = self.dc_inst.get_pin("out").bc()
        delay_en_end_offset = contact_offset + vector(self.poly_contact.width,self.poly_contact.height).scale(0.5,0.5)
        self.add_path("metal1", [delay_en_offset,delay_en_end_offset])


        # 3. Route the mid-point of previous route to the bitcell WL
        # route bend of previous net to bitcell WL
        wl_offset = self.rbc_inst.get_pin("WL").lc()
        wl_mid = vector(delay_en_end_offset.x,wl_offset.y)
        self.add_path("metal1", [delay_en_end_offset, wl_mid, wl_offset])

        # SOURCE ROUTE
        # Route the source to the vdd rail
        source_offset = self.access_tx_offset + self.access_tx.active_contact_positions[1].rotate_scale(-1,1)\
                        + vector(self.active_contact.width,self.active_contact.height).rotate_scale(-0.5,0.5)

        inv_vdd_offset = self.rbl_inv_inst.get_pin("vdd").uc()
        vdd_offset = inv_vdd_offset.scale(1,0) + source_offset.scale(0,1) 
        self.add_path("metal1", [source_offset, vdd_offset])
        
        # DRAIN ROUTE
        # Route the drain to the RBL inverter input
        drain_offset = self.access_tx_offset + self.access_tx.active_contact_positions[0].rotate_scale(-1,1) \
                       + self.poly_contact_offset.rotate_scale(-1,1)
        mid1 = drain_offset.scale(1,0) + vector(0,self.rbl_inv_offset.y+self.inv.width+self.m2_pitch)
        inv_A_offset = self.rbl_inv_inst.get_pin("A").uc()
        mid2 = vector(inv_A_offset.x, mid1.y)
        self.add_path("metal1",[drain_offset, mid1, mid2, inv_A_offset])
        
        # Route the connection of the drain route (mid2) to the RBL bitline (left)
        drain_offset = mid2
        # Route the M2 to the right of the vdd rail between rbl_inv and bitcell
        gnd_pin = self.rbl_inv_inst.get_pin("gnd").ll()
        mid1 = vector(gnd_pin.x+self.m2_pitch,drain_offset.y)
        # Via will go halfway down from the bitcell
        bl_offset = self.rbc_inst.get_pin("BL").bc()
        via_offset = bl_offset - vector(0,0.5*self.inv.width)
        mid2 = vector(mid1.x,via_offset.y)
        # self.add_contact(layers=("metal1", "via1", "metal2"),
        #                  offset=via_offset - vector(0.5*drc["minwidth_metal2"],0.5*drc["minwidth_metal1"]))
        self.add_wire(("metal1","via1","metal2"),[drain_offset,mid1,mid2,via_offset,bl_offset])
        #self.add_path("metal2",[via_offset,bl_offset])   
        
    def route_vdd(self):
        # Add a rail in M2 that is to the right of the inverter gnd pin 
        # The replica column may not fit in a single standard cell pitch, so add the vdd rail to the
        # right of it. 
        vdd_start = vector(self.bitcell_offset.x + self.bitcell.width + self.m1_pitch,0)
        # It is the height of the entire RBL and bitcell
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_start,
                            width=drc["minwidth_metal1"],
                            height=self.rbl.height+self.bitcell.height+2*self.inv.width+0.5*drc["minwidth_metal1"])

        # Connect the vdd pins of the bitcell load directly to vdd
        vdd_pins = self.rbl_inst.get_pins("vdd")
        for pin in vdd_pins:
            offset = vector(vdd_start.x,pin.by()) 
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=self.rbl_offset.x-vdd_start.x,
                          height=drc["minwidth_metal1"])

        # Also connect the replica bitcell vdd pin to vdd
        pin = self.rbc_inst.get_pin("vdd")
        offset = vector(vdd_start.x,pin.by())
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=self.bitcell_offset.x-vdd_start.x,
                      height=drc["minwidth_metal1"])
        
        # Add a second vdd pin. No need for full length. It is must connect at the next level.
        inv_vdd_offset = self.rbl_inv_inst.get_pin("vdd").ll()
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=inv_vdd_offset.scale(1,0),
                            width=drc["minwidth_metal1"],
                            height=self.delay_chain_offset.y)

        
        
        
    def route_gnd(self):
        """ Route all signals connected to gnd """
        
        # Add a rail in M1 from bottom to two along delay chain
        gnd_start = self.rbl_inv_inst.get_pin("gnd").ll() - self.offset_fix
        
        # It is the height of the entire RBL and bitcell
        self.add_rect(layer="metal2",
                      offset=gnd_start,
                      width=drc["minwidth_metal2"],
                      height=self.rbl.height+self.bitcell.height+self.inv.width+self.m2_pitch)
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_start.scale(1,0),
                            width=drc["minwidth_metal2"],
                            height=2*self.inv.width)
                      
        # Connect the WL pins directly to gnd
        for row in range(self.rows):
            wl = "wl[{}]".format(row)
            pin = self.rbl_inst.get_pin(wl)
            offset = vector(gnd_start.x,pin.by())
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=self.rbl_offset.x-gnd_start.x,
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset)

        # Add via for the delay chain
        offset = self.delay_chain_offset - vector(0.5*drc["minwidth_metal1"],0) - self.offset_fix
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)

        # Add via for the inverter
        offset = self.rbl_inv_offset - vector(0.5*drc["minwidth_metal1"],self.m1m2_via.height) - self.offset_fix
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=offset)

        # Connect the bitcell gnd pin to the rail
        gnd_pins = self.get_pins("gnd")
        gnd_start = gnd_pins[0].uc()
        rbl_gnd_pins = self.rbl_inst.get_pins("gnd")
        # Find the left most rail on M2
        gnd_pin = None
        for pin in rbl_gnd_pins:
            if gnd_pin == None or (pin.layer=="metal2" and pin.lx()<gnd_pin.lx()):
                gnd_pin = pin
        gnd_end = gnd_pin.uc()
        # Add a couple midpoints so that the wire will drop a via and then route horizontal on M1
        gnd_mid1 = gnd_start + vector(0,self.m2_pitch)
        gnd_mid2 = gnd_end + vector(0,self.m2_pitch)
        self.add_wire(("metal1","via1","metal2"), [gnd_start, gnd_mid1, gnd_mid2, gnd_end])
        

        # Add a second gnd pin to the second delay chain rail. No need for full length.
        dc_gnd_offset = self.dc_inst.get_pins("gnd")[1].ll()
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=dc_gnd_offset.scale(1,0),
                            width=drc["minwidth_metal1"],
                            height=self.delay_chain_offset.y)

        

    def add_layout_pins(self):
        """ Route the input and output signal """
        en_offset = self.delay_chain_offset+self.delay_chain.get_pin("in").ur().rotate_scale(-1,1) 
        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=en_offset.scale(1,0),
                            width=drc["minwidth_metal1"],
                            height=en_offset.y)

        out_offset = self.rbl_inv_offset+self.inv.get_pin("Z").ur().rotate_scale(-1,1) - vector(0,self.inv.width)
        self.add_layout_pin(text="out",
                            layer="metal1",
                            offset=out_offset.scale(1,0),
                            width=drc["minwidth_metal1"],
                            height=out_offset.y)
        
