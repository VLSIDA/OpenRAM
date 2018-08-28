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

        from importlib import reload
        g = reload(__import__(OPTS.delay_chain))
        self.mod_delay_chain = getattr(g, OPTS.delay_chain)

        g = reload(__import__(OPTS.replica_bitcell))
        self.mod_replica_bitcell = getattr(g, OPTS.replica_bitcell)

        for pin in ["en", "out", "vdd", "gnd"]:
            self.add_pin(pin)
        self.bitcell_loads = bitcell_loads
        self.delay_stages = delay_stages
        self.delay_fanout = delay_fanout

        self.create_modules()
        self.calculate_module_offsets()
        self.add_modules()
        self.route()

        self.offset_all_coordinates()
        
        self.add_layout_pins()

        #self.add_lvs_correspondence_points()

        # Extra pitch on top and right
        self.width = self.rbl_inst.rx() - self.dc_inst.lx() + self.m2_pitch
        self.height = max(self.rbl_inst.uy(), self.dc_inst.uy()) + self.m3_pitch

        self.DRC_LVS()

    def calculate_module_offsets(self):
        """ Calculate all the module offsets """
        
        # These aren't for instantiating, but we use them to get the dimensions
        self.poly_contact_offset = vector(0.5*contact.poly.width,0.5*contact.poly.height)

        # Quadrant 1: Replica bitline and such are not rotated, but they must be placed far enough
        # away from the delay chain/inverter with space for three M2 tracks
        self.bitcell_offset = vector(0,self.replica_bitcell.height)
        self.rbl_offset = self.bitcell_offset 

        # Gap between the delay chain and RBL
        gap_width = 2*self.m2_pitch
        
        # Quadrant 4: with some space below it and tracks on the right for vdd/gnd
        self.delay_chain_offset = vector(-self.delay_chain.width-gap_width,self.replica_bitcell.height)
        
        # Will be flipped vertically below the delay chain
        # Align it with the inverters in the delay chain to simplify supply connections
        self.rbl_inv_offset = self.delay_chain_offset + vector(2*self.inv.width, 0)

        # Placed next to the replica bitcell
        self.access_tx_offset = vector(-gap_width-self.access_tx.width-self.inv.width, 0.5*self.inv.height)



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
                                        offset=self.rbl_inv_offset,
                                        rotate=180)
        self.connect_inst(["bl[0]", "out", "vdd", "gnd"])

        self.tx_inst=self.add_inst(name="rbl_access_tx",
                                   mod=self.access_tx,
                                   offset=self.access_tx_offset)
        # D, G, S, B
        self.connect_inst(["vdd", "delayed_en", "bl[0]", "vdd"])
        # add the well and poly contact

        self.dc_inst=self.add_inst(name="delay_chain",
                                   mod=self.delay_chain,
                                   offset=self.delay_chain_offset)
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
        self.route_supplies()
        self.route_wl()
        self.route_access_tx()

    def route_wl(self):
        """ Connect the RBL word lines to gnd """
        # Connect the WL and gnd pins directly to the center and right gnd rails
        for row in range(self.bitcell_loads):
            wl = "wl[{}]".format(row)
            pin = self.rbl_inst.get_pin(wl)

            # Route the connection to the right so that it doesn't interfere
            # with the cells
            pin_right = pin.rc()
            pin_extension = pin_right + vector(self.m1_pitch,0)
            if pin.layer != "metal1":
                continue
            self.add_path("metal1", [pin_right, pin_extension])
            self.add_power_pin("gnd", pin_extension)
                               
        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        # These are the instances that every bank has
        top_instances = [self.rbl_inst,
                         self.dc_inst]        
        for inst in top_instances:
            self.copy_layout_pin(inst, "vdd")
            self.copy_layout_pin(inst, "gnd")


        # Route the inverter supply pin from M1
        # Only vdd is needed because gnd shares a rail with the delay chain
        pin = self.rbl_inv_inst.get_pin("vdd")
        self.add_power_pin("vdd", pin.lc())
            
        # Replica bitcell needs to be routed up to M3
        pin=self.rbc_inst.get_pin("vdd")
        # Don't rotate this via to vit in FreePDK45
        self.add_power_pin("vdd", pin.center(), rotate=0)
        
        for pin in self.rbc_inst.get_pins("gnd"):
            self.add_power_pin("gnd", pin.center())

            

    def route_access_tx(self):
        # GATE ROUTE
        # 1. Add the poly contact and nwell enclosure
        # Determines the y-coordinate of where to place the gate input poly pin
        # (middle in between the pmos and nmos)

        poly_pin = self.tx_inst.get_pin("G")
        poly_offset = poly_pin.uc()
        # This centers the contact above the poly by one pitch
        contact_offset = poly_offset + vector(0,self.m2_pitch)
        self.add_contact_center(layers=("poly", "contact", "metal1"),
                                offset=contact_offset)
        self.add_contact_center(layers=("metal1", "via1", "metal2"),
                                offset=contact_offset)
        self.add_segment_center(layer="poly",
                                start=poly_offset,
                                end=contact_offset)
        nwell_offset = self.rbl_inv_offset + vector(-self.inv.height,self.inv.width)
        # self.add_rect(layer="nwell",
        #               offset=nwell_offset,
        #               width=0.5*self.inv.height,
        #               height=self.delay_chain_offset.y-nwell_offset.y)

        # 2. Route delay chain output to access tx gate
        delay_en_offset = self.dc_inst.get_pin("out").bc()
        self.add_path("metal2", [delay_en_offset,contact_offset])

        # 3. Route the contact of previous route to the bitcell WL
        # route bend of previous net to bitcell WL
        wl_offset = self.rbc_inst.get_pin("WL").lc()
        xmid_point= 0.5*(wl_offset.x+contact_offset.x)
        wl_mid1 = vector(xmid_point,contact_offset.y)
        wl_mid2 = vector(xmid_point,wl_offset.y)
        self.add_path("metal1", [contact_offset, wl_mid1, wl_mid2, wl_offset])

        # DRAIN ROUTE
        # Route the drain to the vdd rail
        drain_offset = self.tx_inst.get_pin("D").center()
        self.add_power_pin("vdd", drain_offset)
        
        # SOURCE ROUTE
        # Route the drain to the RBL inverter input 
        source_offset = self.tx_inst.get_pin("S").center()
        inv_A_offset = self.rbl_inv_inst.get_pin("A").center()
        self.add_path("metal1",[source_offset, inv_A_offset])

        # Route the connection of the source route to the RBL bitline (left)
        # Via will go halfway down from the bitcell
        bl_offset = self.rbc_inst.get_pin("BL").bc()
        # Route down a pitch so we can use M2 routing
        bl_down_offset = bl_offset - vector(0, self.m2_pitch)
        self.add_path("metal2",[source_offset, bl_down_offset, bl_offset])   
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=source_offset)

        # BODY ROUTE
        # Connect it to the inverter well
        nwell_offset = self.rbl_inv_inst.lr()
        ur_offset = self.tx_inst.ur()
        self.add_rect(layer="nwell",
                      offset=nwell_offset,
                      width=ur_offset.x-nwell_offset.x,
                      height=ur_offset.y-nwell_offset.y)
        
    def route_vdd(self):
        """ Route all signals connected to vdd """

        self.copy_layout_pin(self.dc_inst,"vdd")
        self.copy_layout_pin(self.rbc_inst,"vdd")        
        

        
        # Connect the WL and vdd pins directly to the center and right vdd rails
        # Connect RBL vdd pins to center and right rails
        rbl_vdd_pins = self.rbl_inst.get_pins("vdd")
        for pin in rbl_vdd_pins:
            if pin.layer != "metal1":
                continue
            start = vector(self.center_vdd_pin.cx(),pin.cy())
            end = vector(self.right_vdd_pin.cx(),pin.cy())
            self.add_layout_pin_segment_center(text="vdd",
                                               layer="metal1",
                                               start=start,
                                               end=end)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=start,
                                rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=end,
                                rotate=90)



        
        # Add via for the inverter
        pin = self.rbl_inv_inst.get_pin("vdd")
        start = vector(self.left_vdd_pin.cx(),pin.cy())
        end = vector(self.center_vdd_pin.cx(),pin.cy())
        self.add_segment_center(layer="metal1",
                                start=start,
                                end=end)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=start,
                            rotate=90)

        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=end,
                            rotate=90)


        # Add via for the RBC
        pin = self.rbc_inst.get_pin("vdd")
        start = pin.lc()
        end = vector(self.right_vdd_pin.cx(),pin.cy())
        self.add_segment_center(layer="metal1",
                                start=start,
                                end=end)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=end,
                            rotate=90)

        # Create the RBL rails too
        rbl_pins = self.rbl_inst.get_pins("vdd")
        for pin in rbl_pins:
            if pin.layer != "metal1":
                continue
            # If above the delay line, route the full width
            left = vector(self.left_vdd_pin.cx(),pin.cy())                
            center = vector(self.center_vdd_pin.cx(),pin.cy())          
            if pin.cy() > self.dc_inst.uy() + self.m1_pitch:
                start = left
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left,
                                    rotate=90)
            else:
                start = center
            end = vector(self.right_vdd_pin.cx()+0.5*self.m1_width,pin.cy())
            self.add_layout_pin_segment_center(text="vdd",
                                               layer="metal1",
                                               start=start,
                                               end=end)

        

        
        
        
    def route_gnd(self):
        """ Route all signals connected to gnd """

        # Route the gnd lines from left to right

        # Add via for the delay chain
        left_gnd_start = self.dc_inst.ll().scale(1,0) - vector(2*self.m2_pitch,0)
        left_gnd_end = vector(left_gnd_start.x, self.rbl_inst.uy()+self.m2_pitch)
        self.left_gnd_pin=self.add_segment_center(layer="metal2",
                                                  start=left_gnd_start,
                                                  end=left_gnd_end)

        # Gnd line to the left of the replica bitline
        center_gnd_start = self.rbc_inst.ll().scale(1,0) - vector(2*self.m2_pitch,0)
        center_gnd_end = vector(center_gnd_start.x, self.rbl_inst.uy()+self.m2_pitch)
        self.center_gnd_pin=self.add_segment_center(layer="metal2",
                                                    start=center_gnd_start,
                                                    end=center_gnd_end)

        # Gnd line to the right of the replica bitline
        right_gnd_start = self.rbc_inst.lr().scale(1,0) + vector(self.m2_pitch,0)
        right_gnd_end = vector(right_gnd_start.x, self.rbl_inst.uy()+self.m2_pitch)
        self.right_gnd_pin=self.add_segment_center(layer="metal2",
                                                   start=right_gnd_start,
                                                   end=right_gnd_end)
                      

        
        # Connect the WL and gnd pins directly to the center and right gnd rails
        for row in range(self.bitcell_loads):
            wl = "wl[{}]".format(row)
            pin = self.rbl_inst.get_pin(wl)
            if pin.layer != "metal1":
                continue
            # If above the delay line, route the full width
            left = vector(self.left_gnd_pin.cx(),pin.cy())                
            center = vector(self.center_gnd_pin.cx(),pin.cy())                
            if pin.cy() > self.dc_inst.uy() + self.m1_pitch:
                start = left
            else:
                start = center
            end = vector(self.right_gnd_pin.cx(),pin.cy())                
            self.add_layout_pin_segment_center(text="gnd",
                                               layer="metal1",
                                               start=start,
                                               end=end)
            if start == left:
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left,
                                    rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=center,
                                rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=end,
                                rotate=90)


        rbl_gnd_pins = self.rbl_inst.get_pins("gnd")
        # Add L shapes to each vertical gnd rail
        for pin in rbl_gnd_pins:
            if pin.layer != "metal1":
                continue
            # If above the delay line, route the full width
            left = vector(self.left_gnd_pin.cx(),pin.cy())                
            center = vector(self.center_gnd_pin.cx(),pin.cy())                
            if pin.cy() > self.dc_inst.uy() + self.m1_pitch:
                start = left
            else:
                start = center
            end = vector(self.right_gnd_pin.cx(),pin.cy())
            self.add_segment_center(layer="metal1",
                                    start=start,
                                    end=end)
            if start == left:
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left,
                                    rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=center,
                                rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=end,
                                rotate=90)



        # Connect the gnd pins of the delay chain to the left rails
        dc_gnd_pins = self.dc_inst.get_pins("gnd")
        for pin in dc_gnd_pins:
            if pin.layer != "metal1":
                continue
            start = vector(self.left_gnd_pin.cx(),pin.cy())
            # Note, we don't connect to the center rails because of
            # via conflicts with the RBL
            #end = vector(self.center_gnd_pin.cx(),pin.cy())
            end = pin.rc()
            self.add_segment_center(layer="metal1",
                                    start=start,
                                    end=end)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=start,
                                rotate=90)

            # self.add_via_center(layers=("metal1", "via1", "metal2"),
            #                     offset=end,
            #rotate=90)

        
        # Add via for the inverter
        # pin = self.rbl_inv_inst.get_pin("gnd")
        # start = vector(self.left_gnd_pin.cx(),pin.cy())
        # end = vector(self.center_gnd_pin.cx(),pin.cy())
        # self.add_segment_center(layer="metal1",
        #                         start=start,
        #                         end=end)
        # self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                     offset=start,
        #rotate=90)
        # self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                     offset=end,
        #rotate=90)


        
        # Create RBL rails too
        rbl_pins = self.rbl_inst.get_pins("gnd")
        for pin in rbl_pins:
            if pin.layer != "metal2":
                continue
            start = vector(pin.cx(),self.right_gnd_pin.by())
            end = vector(pin.cx(),self.right_gnd_pin.uy())
            self.add_layout_pin_segment_center(text="gnd",
                                               layer="metal2",
                                               start=start,
                                               end=end)
            
        

    def add_layout_pins(self):
        """ Route the input and output signal """
        en_offset = self.dc_inst.get_pin("in").bc()
        self.add_layout_pin_segment_center(text="en",
                                           layer="metal2",
                                           start=en_offset,
                                           end=en_offset.scale(1,0))

        out_offset = self.rbl_inv_inst.get_pin("Z").center()
        self.add_layout_pin_segment_center(text="out",
                                           layer="metal2",
                                           start=out_offset,
                                           end=out_offset.scale(1,0))
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=out_offset)
        
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

