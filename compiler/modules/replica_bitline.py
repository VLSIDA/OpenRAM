# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
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
        self.width = self.delay_chain_inst.rx() + self.m2_pitch
        self.height = self.delay_chain_inst.uy() + self.m3_pitch

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        pin_list = ["en", "bl", "wl", "out", "vdd", "gnd"]
        pin_dir = ["INPUT", "INPUT", "OUTPUT", "OUTPUT", "POWER", "GROUND"]
        self.add_pin_list(pin_list, pin_dir)
        
    def calculate_module_offsets(self):
        """ Calculate all the module offsets """
        
        # Quadrant 4: with some space below it and tracks on the right for vdd/gnd
        self.delay_chain_offset = vector(0, self.inv.height)
        
        # Will be flipped vertically below the delay chain
        # Align it with the inverters in the delay chain to simplify supply connections
        self.rbl_inv_offset = self.delay_chain_offset + vector(2*self.inv.width, 0)

        # Placed next to the replica bitcell
        self.access_tx_offset = vector(self.rbl_inv_offset.x + self.inv.width, 0.5*self.inv.height)


    def add_modules(self):
        """ Add the modules for later usage """

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

    def place_instances(self):
        """ Add all of the module instances in the logical netlist """
        
        # This is the threshold detect inverter on the output of the RBL
        self.rbl_inv_inst.place(offset=self.rbl_inv_offset,
                                rotate=180)

        self.tx_inst.place(self.access_tx_offset)

        self.delay_chain_inst.place(self.delay_chain_offset)


    def route(self):
        """ Connect all the signals together """
        self.route_supplies()
        self.route_access_tx()

    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        self.copy_layout_pin(self.delay_chain_inst, "vdd")
        self.copy_layout_pin(self.delay_chain_inst, "gnd")

        # Route the inverter supply pin from M1
        # Only vdd is needed because gnd shares a rail with the delay chain
        pin = self.rbl_inv_inst.get_pin("vdd")
        self.add_power_pin("vdd", pin.lc())
            

            

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
        self.add_layout_pin_rect_center(text="wl",
                                        layer="metal1",
                                        offset=contact_offset)
        
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
        source_down_offset = source_offset - vector(0,3*self.m2_pitch)
        self.add_path("metal1",[source_offset, source_down_offset])
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=source_offset)
        self.add_layout_pin_rect_center(text="bl",
                                        layer="metal1",
                                        offset=source_down_offset)

        # BODY ROUTE
        # Connect it to the inverter well
        nwell_offset = self.rbl_inv_inst.lr()
        ur_offset = self.tx_inst.ur()
        self.add_rect(layer="nwell",
                      offset=nwell_offset,
                      width=ur_offset.x-nwell_offset.x,
                      height=ur_offset.y-nwell_offset.y)
        
        

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
        
