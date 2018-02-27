import debug
import design
from tech import drc
from pinv import pinv
import contact
from bitcell_array import bitcell_array
from ptx import ptx
from vector import vector
from globals import OPTS

class replica_bitline(design.design):
    """
    Generate a module that simulates the delay of control logic 
    and bit line charging. Stages is the depth of the delay
    line and rows is the height of the replica bit loads.
    """

    def __init__(self, delay_stages, delay_fanout, bitcell_loads, name="replica_bitline"):
        design.design.__init__(self, name)

        g = reload(__import__(OPTS.delay_chain))
        self.mod_delay_chain = getattr(g, OPTS.delay_chain)

        g = reload(__import__(OPTS.replica_bitcell))
        self.mod_replica_bitcell = getattr(g, OPTS.replica_bitcell)

        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)

        for pin in ["en", "out", "vdd", "gnd"]:
            self.add_pin(pin)
        self.bitcell_loads = bitcell_loads
        self.delay_stages = delay_stages
        self.delay_fanout = delay_fanout

        self.create_modules()
        self.calculate_module_offsets()
        self.add_modules()
        self.route()
        self.add_layout_pins()
        self.add_lvs_correspondence_points()

        self.DRC_LVS()

    def calculate_module_offsets(self):
        """ Calculate all the module offsets """
        
        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact_offset = vector(0.5*contact.poly.width,0.5*contact.poly.height)

        # M1/M2 routing pitch is based on contacted pitch
        self.m1_pitch = max(contact.m1m2.width,contact.m1m2.height) + max(self.m1_space,self.m2_space)
        self.m2_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(self.m2_space,self.m3_space)
        
        # This corrects the offset pitch difference between M2 and M1
        self.offset_fix = vector(0.5*(self.m2_width-self.m1_width),0)

        # delay chain will be rotated 90, so move it over a width
        # we move it up a inv height just for some routing room
        self.rbl_inv_offset = vector(self.delay_chain.height, self.inv.width)
        # access TX goes right on top of inverter, leave space for an inverter which is
        # about the same as a TX. We'll need to add rails though.
        self.access_tx_offset = vector(1.25*self.inv.height,self.rbl_inv_offset.y) + vector(0,2.5*self.inv.width)
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
        self.rbl = bitcell_array(name="bitline_load", cols=1, rows=self.bitcell_loads)
        self.add_mod(self.rbl)

        # FIXME: The FO and depth of this should be tuned
        self.delay_chain = self.mod_delay_chain([self.delay_fanout]*self.delay_stages)
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
        self.connect_inst(["bl[0]", "br[0]"] + ["gnd"]*self.bitcell_loads + ["vdd", "gnd"])
        



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

        poly_pin = self.tx_inst.get_pin("G")
        poly_offset = poly_pin.rc()
        # This centers the contact on the poly
        contact_offset = poly_offset.scale(0,1) + self.dc_inst.get_pin("out").bc().scale(1,0)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                offset=contact_offset)
        self.add_rect(layer="poly",
                      offset=poly_pin.lr(),
                      width=contact_offset.x-poly_offset.x,
                      height=self.poly_width)
        nwell_offset = self.rbl_inv_offset + vector(-self.inv.height,self.inv.width)
        self.add_rect(layer="nwell",
                      offset=nwell_offset,
                      width=0.5*self.inv.height,
                      height=self.delay_chain_offset.y-nwell_offset.y)

        # 2. Route delay chain output to access tx gate
        delay_en_offset = self.dc_inst.get_pin("out").bc()
        self.add_path("metal1", [delay_en_offset,contact_offset])

        # 3. Route the mid-point of previous route to the bitcell WL
        # route bend of previous net to bitcell WL
        wl_offset = self.rbc_inst.get_pin("WL").lc()
        wl_mid = vector(contact_offset.x,wl_offset.y)
        self.add_path("metal1", [contact_offset, wl_mid, wl_offset])

        # DRAIN ROUTE
        # Route the drain to the vdd rail
        drain_offset = self.tx_inst.get_pin("D").lc()
        inv_vdd_offset = self.rbl_inv_inst.get_pin("vdd").uc()
        vdd_offset = inv_vdd_offset.scale(1,0) + drain_offset.scale(0,1) 
        self.add_path("metal1", [drain_offset, vdd_offset])
        
        # SOURCE ROUTE
        # Route the source to the RBL inverter input
        source_offset = self.tx_inst.get_pin("S").bc()
        mid1 = source_offset.scale(1,0) + vector(0,self.rbl_inv_offset.y+self.inv.width+self.m2_pitch)
        inv_A_offset = self.rbl_inv_inst.get_pin("A").uc()
        mid2 = vector(inv_A_offset.x, mid1.y)
        self.add_path("metal1",[source_offset, mid1, mid2, inv_A_offset])
        
        # Route the connection of the source route (mid2) to the RBL bitline (left)
        source_offset = mid2
        # Route the M2 to the right of the vdd rail between rbl_inv and bitcell
        gnd_pin = self.rbl_inv_inst.get_pin("gnd").ll()
        mid1 = vector(gnd_pin.x+self.m2_pitch,source_offset.y)
        # Via will go halfway down from the bitcell
        bl_offset = self.rbc_inst.get_pin("BL").bc()
        via_offset = bl_offset - vector(0,0.5*self.inv.width)
        mid2 = vector(mid1.x,via_offset.y)
        # self.add_contact(layers=("metal1", "via1", "metal2"),
        #                  offset=via_offset - vector(0.5*self.m2_width,0.5*self.m1_width))
        self.add_wire(("metal1","via1","metal2"),[source_offset,mid1,mid2,via_offset,bl_offset])
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
                            width=self.m1_width,
                            height=self.rbl.height+self.bitcell.height+2*self.inv.width+0.5*self.m1_width)

        # Connect the vdd pins of the bitcell load directly to vdd
        vdd_pins = self.rbl_inst.get_pins("vdd")
        for pin in vdd_pins:
            offset = vector(vdd_start.x,pin.by()) 
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=self.rbl_offset.x-vdd_start.x,
                          height=self.m1_width)

        # Also connect the replica bitcell vdd pin to vdd
        pin = self.rbc_inst.get_pin("vdd")
        offset = vector(vdd_start.x,pin.by())
        self.add_rect(layer="metal1",
                      offset=offset,
                      width=self.bitcell_offset.x-vdd_start.x,
                      height=self.m1_width)
        
        # Add a second vdd pin. No need for full length. It is must connect at the next level.
        inv_vdd_offset = self.rbl_inv_inst.get_pin("vdd").ll()
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=inv_vdd_offset.scale(1,0),
                            width=self.m1_width,
                            height=self.delay_chain_offset.y)

        
        
        
    def route_gnd(self):
        """ Route all signals connected to gnd """
        
        gnd_start = self.rbl_inv_inst.get_pin("gnd").bc()
        gnd_end = vector(gnd_start.x, self.rbl_inst.uy()+2*self.m2_pitch)
        
        # Add a rail in M1 from bottom of delay chain to two above the RBL
        # This prevents DRC errors with vias for the WL
        dc_top = self.dc_inst.ur()
        self.add_segment_center(layer="metal1",
                                start=vector(gnd_start.x, dc_top.y),
                                end=gnd_end)

        # Add a rail in M2 from RBL inverter to two above the RBL
        self.add_segment_center(layer="metal2",
                                start=gnd_start,
                                end=gnd_end)
        
        # Add pin from bottom to RBL inverter
        self.add_layout_pin_center_segment(text="gnd",
                                           layer="metal1",
                                           start=gnd_start.scale(1,0),
                                           end=gnd_start)
                      
        # Connect the WL pins directly to gnd
        gnd_pin = self.get_pin("gnd").rc()
        for row in range(self.bitcell_loads):
            wl = "wl[{}]".format(row)
            pin = self.rbl_inst.get_pin(wl)
            start = vector(gnd_pin.x,pin.cy())
            self.add_segment_center(layer="metal1",
                                    start=start,
                                    end=pin.lc())
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=start)

        # Add via for the delay chain
        offset = self.dc_inst.get_pins("gnd")[0].bc() + vector(0.5*contact.m1m2.width,0.5*contact.m1m2.height)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=offset)

        # Add via for the inverter
        offset = self.rbl_inv_inst.get_pin("gnd").bc() - vector(0,0.5*contact.m1m2.height)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=offset)

        # Connect the bitcell gnd pins to the rail
        gnd_pins = self.get_pins("gnd")
        gnd_start = gnd_pins[0].ul()
        rbl_gnd_pins = self.rbl_inst.get_pins("gnd")
        # Add L shapes to each vertical gnd rail
        for pin in rbl_gnd_pins:
            if pin.layer != "metal2":
                continue
            gnd_end = pin.uc()
            gnd_mid = vector(gnd_end.x, gnd_start.y)
            self.add_wire(("metal1","via1","metal2"), [gnd_start, gnd_mid, gnd_end])
            gnd_start = gnd_mid
        

        # Add a second gnd pin to the second delay chain rail. No need for full length.
        dc_gnd_offset = self.dc_inst.get_pins("gnd")[1].ll()
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=dc_gnd_offset.scale(1,0),
                            width=self.m1_width,
                            height=self.delay_chain_offset.y)

        

    def add_layout_pins(self):
        """ Route the input and output signal """
        en_offset = self.dc_inst.get_pin("in").ll()
        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=en_offset.scale(1,0),
                            width=self.m1_width,
                            height=en_offset.y)

        out_offset = self.rbl_inv_inst.get_pin("Z").ll()
        self.add_layout_pin(text="out",
                            layer="metal1",
                            offset=out_offset.scale(1,0),
                            width=self.m1_width,
                            height=out_offset.y)
        
    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """

        pin = self.rbl_inv_inst.get_pin("A")
        self.add_label_pin(text="bl[0]",
                           layer=pin.layer,
                           offset=pin.ll(),
                           height=pin.height(),
                           width=pin.width())

        pin = self.dc_inst.get_pin("out")
        self.add_label_pin(text="delayed_en",
                           layer=pin.layer,
                           offset=pin.ll(),
                           height=pin.height(),
                           width=pin.width())

