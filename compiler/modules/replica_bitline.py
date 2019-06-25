# See LICENSE for licensing information.
#
#Copyright (c) 2016-2019 Regents of the University of California and The Board
#of Regents for the Oklahoma Agricultural and Mechanical College
#(acting for and on behalf of Oklahoma State University)
#All rights reserved.
#
import debug
import design
from tech import drc
import contact
from sram_factory import factory
from vector import vector
from globals import OPTS

class replica_bitline(design.design):
    """
    Generate a module that simulates the delay of control logic 
    and bit line charging. Stages is the depth of the delay
    line and rows is the height of the replica bit loads.
    """

    def __init__(self, name, delay_fanout_list, bitcell_loads):
        design.design.__init__(self, name)

        self.bitcell_loads = bitcell_loads
        self.delay_fanout_list = delay_fanout_list
        if len(delay_fanout_list) == 0 or len(delay_fanout_list)%2 == 1:
            debug.error('Delay chain must contain an even amount of stages to maintain polarity.',1)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            
    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.calculate_module_offsets()
        self.place_instances()
        self.route()
        self.add_layout_pins()

        self.offset_all_coordinates()

        #self.add_lvs_correspondence_points()

        # Extra pitch on top and right
        self.width = self.replica_column_inst.rx() - self.delay_chain_inst.lx() + self.m2_pitch
        self.height = max(self.replica_column_inst.uy(), self.delay_chain_inst.uy()) + self.m3_pitch

        self.DRC_LVS()

    def add_pins(self):
        for pin in ["en", "out", "vdd", "gnd"]:
            self.add_pin(pin)

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


    def add_modules(self):
        """ Add the modules for later usage """

        self.replica_bitcell = factory.create(module_type="replica_bitcell")
        self.add_mod(self.replica_bitcell)

        bitcell = factory.create(module_type="bitcell")
        # This is the replica bitline load column that is the height of our array
        self.rbl = factory.create(module_type="bitcell_array",
                                  cols=1,
                                  rows=self.bitcell_loads,
                                  bitcell=bitcell)
        self.add_mod(self.rbl)

        # FIXME: The FO and depth of this should be tuned
        self.delay_chain = factory.create(module_type="delay_chain",
                                          fanout_list=self.delay_fanout_list)
        self.add_mod(self.delay_chain)

        self.inv = factory.create(module_type="pinv")
        self.add_mod(self.inv)

        self.access_tx = factory.create(module_type="ptx",
                                        tx_type="pmos")
        self.add_mod(self.access_tx)

    def create_instances(self):
        """ Create all of the module instances in the logical netlist """
        
        # This is the threshold detect inverter on the output of the RBL
        self.rbl_inv_inst=self.add_inst(name="rbl_inv",
                                        mod=self.inv)
        self.connect_inst(["bl0_0", "out", "vdd", "gnd"])

        self.tx_inst=self.add_inst(name="rbl_access_tx",
                                   mod=self.access_tx)
        # D, G, S, B
        self.connect_inst(["vdd", "delayed_en", "bl0_0", "vdd"])
        # add the well and poly contact

        self.delay_chain_inst=self.add_inst(name="delay_chain",
                                            mod=self.delay_chain)
        self.connect_inst(["en", "delayed_en", "vdd", "gnd"])

        self.replica_cell_inst=self.add_inst(name="bitcell",
                                             mod=self.replica_bitcell)
        temp = []
        for port in self.all_ports:
            temp.append("bl{}_0".format(port))
            temp.append("br{}_0".format(port))
        for port in self.all_ports:
            temp.append("delayed_en")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

        self.replica_column_inst=self.add_inst(name="load",
                                               mod=self.rbl)
        
        temp = []
        for port in self.all_ports:
            temp.append("bl{}_0".format(port))
            temp.append("br{}_0".format(port))
        for wl in range(self.bitcell_loads):
            for port in self.all_ports:
                temp.append("gnd")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)
        
        self.wl_list = self.rbl.cell.list_all_wl_names()
        self.bl_list = self.rbl.cell.list_all_bl_names()
        
    def place_instances(self):
        """ Add all of the module instances in the logical netlist """
        
        # This is the threshold detect inverter on the output of the RBL
        self.rbl_inv_inst.place(offset=self.rbl_inv_offset,
                                rotate=180)

        self.tx_inst.place(self.access_tx_offset)

        self.delay_chain_inst.place(self.delay_chain_offset)

        self.replica_cell_inst.place(offset=self.bitcell_offset,
                            mirror="MX")

        self.replica_column_inst.place(self.rbl_offset)


    def route(self):
        """ Connect all the signals together """
        self.route_supplies()
        self.route_wl()
        self.route_access_tx()

    def route_wl(self):
        """ Connect the RBL word lines to gnd """
        # Connect the WL and gnd pins directly to the center and right gnd rails
        for row in range(self.bitcell_loads):
            wl = self.wl_list[0]+"_{}".format(row)
            pin = self.replica_column_inst.get_pin(wl)

            # Route the connection to the right so that it doesn't interfere with the cells
            # Wordlines may be close to each other when tiled, so gnd connections are routed in opposite directions            
            pin_right = pin.rc()
            pin_extension = pin_right + vector(self.m3_pitch,0)

            if pin.layer != "metal1":
                continue
            pin_width_ydir = pin.uy()-pin.by()
            #Width is set to pin y width to avoid DRC issues with m1 gaps
            self.add_path("metal1", [pin_right, pin_extension], pin_width_ydir)
            self.add_power_pin("gnd", pin_extension)
            
            # for multiport, need to short wordlines to each other so they all connect to gnd.
            wl_last = self.wl_list[-1]+"_{}".format(row)
            pin_last = self.replica_column_inst.get_pin(wl_last)
            self.short_wordlines(pin, pin_last, "right", False, row, vector(self.m3_pitch,0))
                    
    def short_wordlines(self, wl_pin_a, wl_pin_b, pin_side, is_replica_cell, cell_row=0, offset_x_vec=None):
        """Connects the word lines together for a single bitcell. Also requires which side of the bitcell to short the pins."""
        #Assumes input pins are wordlines. Also assumes the word lines are horizontal in metal1. Also assumes pins have same x coord.
        #This is my (Hunter) first time editing layout in openram so this function is likely not optimal.
        if len(self.all_ports) > 1:
            #1. Create vertical metal for all the bitlines to connect to
            #m1 needs to be extended in the y directions, direction needs to be determined as every other cell is flipped
            correct_y = vector(0, 0.5*drc("minwidth_metal1"))
            #x spacing depends on the side being drawn. Unknown to me (Hunter) why the size of the space differs by the side.
            #I assume this is related to how a wire is draw, but I have not investigated the issue.
            if pin_side == "right":
                correct_x = vector(0.5*drc("minwidth_metal1"), 0)
                if offset_x_vec != None:
                    correct_x = offset_x_vec
                else:
                    correct_x = vector(1.5*drc("minwidth_metal1"), 0)
                    
                if wl_pin_a.uy() > wl_pin_b.uy():
                    self.add_path("metal1", [wl_pin_a.rc()+correct_x+correct_y, wl_pin_b.rc()+correct_x-correct_y])
                else:
                    self.add_path("metal1", [wl_pin_a.rc()+correct_x-correct_y, wl_pin_b.rc()+correct_x+correct_y])
            elif pin_side == "left":
                if offset_x_vec != None:
                    correct_x = offset_x_vec
                else:
                    correct_x = vector(1.5*drc("minwidth_metal1"), 0)
                
                if wl_pin_a.uy() > wl_pin_b.uy():
                    self.add_path("metal1", [wl_pin_a.lc()-correct_x+correct_y, wl_pin_b.lc()-correct_x-correct_y])
                else:
                    self.add_path("metal1", [wl_pin_a.lc()-correct_x-correct_y, wl_pin_b.lc()-correct_x+correct_y])
            else:
                debug.error("Could not connect wordlines on specified input side={}".format(pin_side),1)
            
            #2. Connect word lines horizontally. Only replica cell needs. Bitline loads currently already do this.
            for port in self.all_ports:
                if is_replica_cell:
                    wl = self.wl_list[port]
                    pin = self.replica_cell_inst.get_pin(wl)
                else:
                    wl = self.wl_list[port]+"_{}".format(cell_row)
                    pin = self.replica_column_inst.get_pin(wl)
                    
                if pin_side == "left":    
                    self.add_path("metal1", [pin.lc()-correct_x, pin.lc()])
                elif pin_side == "right":
                    self.add_path("metal1", [pin.rc()+correct_x, pin.rc()])
                
            
                
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        # These are the instances that every bank has
        top_instances = [self.replica_column_inst,
                         self.delay_chain_inst]        
        for inst in top_instances:
            self.copy_layout_pin(inst, "vdd")
            self.copy_layout_pin(inst, "gnd")


        # Route the inverter supply pin from M1
        # Only vdd is needed because gnd shares a rail with the delay chain
        pin = self.rbl_inv_inst.get_pin("vdd")
        self.add_power_pin("vdd", pin.lc())
            
        for pin in self.replica_cell_inst.get_pins("vdd"):
            self.add_power_pin(name="vdd", loc=pin.center(), vertical=True, start_layer=pin.layer)
        
        for pin in self.replica_cell_inst.get_pins("gnd"):
            self.add_power_pin("gnd", pin.center(), vertical=True, start_layer=pin.layer)

            

    def route_access_tx(self):
        # GATE ROUTE
        # 1. Add the poly contact and nwell enclosure
        # Determines the y-coordinate of where to place the gate input poly pin
        # (middle in between the pmos and nmos)

        poly_pin = self.tx_inst.get_pin("G")
        poly_offset = poly_pin.uc()
        # This centers the contact above the poly by one pitch
        contact_offset = poly_offset + vector(0,self.m2_pitch)
        self.add_via_center(layers=("poly", "contact", "metal1"),
                            offset=contact_offset)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
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
        delay_en_offset = self.delay_chain_inst.get_pin("out").bc()
        self.add_path("metal2", [delay_en_offset,contact_offset])

        # 3. Route the contact of previous route to the bitcell WL
        # route bend of previous net to bitcell WL
        wl_offset = self.replica_cell_inst.get_pin(self.wl_list[0]).lc()
        wl_mid1 = wl_offset - vector(1.5*drc("minwidth_metal1"), 0)
        wl_mid2 = vector(wl_mid1.x, contact_offset.y)
        #xmid_point= 0.5*(wl_offset.x+contact_offset.x)
        #wl_mid1 = vector(xmid_point,contact_offset.y)
        #wl_mid2 = vector(xmid_point,wl_offset.y)
        self.add_path("metal1", [wl_offset, wl_mid1, wl_mid2, contact_offset])
        
        # 4. Short wodlines if multiport
        wl = self.wl_list[0]
        wl_last = self.wl_list[-1]
        pin = self.replica_cell_inst.get_pin(wl)
        pin_last = self.replica_cell_inst.get_pin(wl_last)
        x_offset = self.short_wordlines(pin, pin_last, "left", True)
        
        #correct = vector(0.5*drc("minwidth_metal1"), 0)
        #self.add_path("metal1", [pin.lc()+correct, pin_last.lc()+correct])

        # DRAIN ROUTE
        # Route the drain to the vdd rail
        drain_offset = self.tx_inst.get_pin("D").center()
        self.add_power_pin("vdd", drain_offset, vertical=True)
        
        # SOURCE ROUTE
        # Route the drain to the RBL inverter input 
        source_offset = self.tx_inst.get_pin("S").center()
        inv_A_offset = self.rbl_inv_inst.get_pin("A").center()
        self.add_path("metal1",[source_offset, inv_A_offset])

        # Route the connection of the source route to the RBL bitline (left)
        # Via will go halfway down from the bitcell
        bl_offset = self.replica_cell_inst.get_pin(self.bl_list[0]).bc()
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

        self.copy_layout_pin(self.delay_chain_inst,"vdd")
        self.copy_layout_pin(self.replica_cell_inst,"vdd")        
        
        # Connect the WL and vdd pins directly to the center and right vdd rails
        # Connect RBL vdd pins to center and right rails
        rbl_vdd_pins = self.replica_column_inst.get_pins("vdd")
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
                                offset=start)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=end)

        # Add via for the inverter
        pin = self.rbl_inv_inst.get_pin("vdd")
        start = vector(self.left_vdd_pin.cx(),pin.cy())
        end = vector(self.center_vdd_pin.cx(),pin.cy())
        self.add_segment_center(layer="metal1",
                                start=start,
                                end=end)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=start)

        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=end)


        # Add via for the RBC
        pin = self.replica_cell_inst.get_pin("vdd")
        start = pin.lc()
        end = vector(self.right_vdd_pin.cx(),pin.cy())
        self.add_segment_center(layer="metal1",
                                start=start,
                                end=end)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=end)

        # Create the RBL rails too
        rbl_pins = self.replica_column_inst.get_pins("vdd")
        for pin in rbl_pins:
            if pin.layer != "metal1":
                continue
            # If above the delay line, route the full width
            left = vector(self.left_vdd_pin.cx(),pin.cy())                
            center = vector(self.center_vdd_pin.cx(),pin.cy())          
            if pin.cy() > self.delay_chain_inst.uy() + self.m1_pitch:
                start = left
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left)
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
        left_gnd_start = self.delay_chain_inst.ll().scale(1,0) - vector(2*self.m2_pitch,0)
        left_gnd_end = vector(left_gnd_start.x, self.replica_column_inst.uy()+self.m2_pitch)
        self.left_gnd_pin=self.add_segment_center(layer="metal2",
                                                  start=left_gnd_start,
                                                  end=left_gnd_end)

        # Gnd line to the left of the replica bitline
        center_gnd_start = self.replica_cell_inst.ll().scale(1,0) - vector(2*self.m2_pitch,0)
        center_gnd_end = vector(center_gnd_start.x, self.replica_column_inst.uy()+self.m2_pitch)
        self.center_gnd_pin=self.add_segment_center(layer="metal2",
                                                    start=center_gnd_start,
                                                    end=center_gnd_end)

        # Gnd line to the right of the replica bitline
        right_gnd_start = self.replica_cell_inst.lr().scale(1,0) + vector(self.m2_pitch,0)
        right_gnd_end = vector(right_gnd_start.x, self.replica_column_inst.uy()+self.m2_pitch)
        self.right_gnd_pin=self.add_segment_center(layer="metal2",
                                                   start=right_gnd_start,
                                                   end=right_gnd_end)
                      

        
        # Connect the WL and gnd pins directly to the center and right gnd rails
        for row in range(self.bitcell_loads):
            wl = self.wl_list[0]+"_{}".format(row)
            pin = self.replica_column_inst.get_pin(wl)
            if pin.layer != "metal1":
                continue
            # If above the delay line, route the full width
            left = vector(self.left_gnd_pin.cx(),pin.cy())                
            center = vector(self.center_gnd_pin.cx(),pin.cy())                
            if pin.cy() > self.delay_chain_inst.uy() + self.m1_pitch:
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
                                    offset=left)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=center)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=end)


        # rbl_gnd_pins = self.replica_column_inst.get_pins("gnd")
        # # Add L shapes to each vertical gnd rail
        # for pin in rbl_gnd_pins:
        #     if pin.layer != "metal1":
        #         continue
        #     # If above the delay line, route the full width
        #     left = vector(self.left_gnd_pin.cx(),pin.cy())                
        #     center = vector(self.center_gnd_pin.cx(),pin.cy())                
        #     if pin.cy() > self.delay_chain_inst.uy() + self.m1_pitch:
        #         start = left
        #     else:
        #         start = center
        #     end = vector(self.right_gnd_pin.cx(),pin.cy())
        #     self.add_segment_center(layer="metal1",
        #                             start=start,
        #                             end=end)
        #     if start == left:
        #         self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                             offset=left)
        #     self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                         offset=center)
        #     self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                         offset=end)



        # Connect the gnd pins of the delay chain to the left rails
        dc_gnd_pins = self.delay_chain_inst.get_pins("gnd")
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
                                offset=start)

            # self.add_via_center(layers=("metal1", "via1", "metal2"),
            #                     offset=end)

        
        # Add via for the inverter
        # pin = self.rbl_inv_inst.get_pin("gnd")
        # start = vector(self.left_gnd_pin.cx(),pin.cy())
        # end = vector(self.center_gnd_pin.cx(),pin.cy())
        # self.add_segment_center(layer="metal1",
        #                         start=start,
        #                         end=end)
        # self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                     offset=start)
        # self.add_via_center(layers=("metal1", "via1", "metal2"),
        #                     offset=end)


        
        # Create RBL rails too
        rbl_pins = self.replica_column_inst.get_pins("gnd")
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
        en_offset = self.delay_chain_inst.get_pin("in").bc()
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

        pin = self.delay_chain_inst.get_pin("out")
        self.add_label_pin(text="delayed_en",
                           layer=pin.layer,
                           offset=pin.ll(),
                           height=pin.height(),
                           width=pin.width())
                           
    def get_en_cin(self):
        """Get the enable input relative capacitance"""
        #The enable is only connected to the delay, get the cin from that module
        en_cin = self.delay_chain.get_cin()
        return en_cin
        
    def determine_sen_stage_efforts(self, ext_cout, inp_is_rise=True):
        """Get the stage efforts from the en to s_en. Does not compute the delay for the bitline load."""
        stage_effort_list = []
        #Stage 1 is the delay chain
        stage1_cout = self.get_delayed_en_cin()
        stage1 = self.delay_chain.determine_delayed_en_stage_efforts(stage1_cout, inp_is_rise)
        stage_effort_list += stage1
        
        #There is a disconnect between the delay chain and inverter. The rise/fall of the input to the inverter
        #Will be the negation of the previous stage.
        last_stage_is_rise = not stage_effort_list[-1].is_rise
        
        #The delay chain triggers the enable on the replica bitline (rbl). This is used to track the bitline delay whereas this
        #model is intended to track every but that. Therefore, the next stage is the inverter after the rbl. 
        stage2 = self.inv.get_stage_effort(ext_cout, last_stage_is_rise)
        stage_effort_list.append(stage2)
        
        return stage_effort_list
        
    def get_delayed_en_cin(self):
        """Get the fanout capacitance (relative) of the delayed enable from the delay chain."""
        access_tx_cin = self.access_tx.get_cin()
        rbc_cin = self.replica_bitcell.get_wl_cin()
        return access_tx_cin + rbc_cin
        
