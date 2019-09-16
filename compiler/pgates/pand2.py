# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import drc
from math import log
from vector import vector
from globals import OPTS
import pgate
from sram_factory import factory

class pand2(pgate.pgate):
    """
    This is a simple buffer used for driving loads. 
    """
    def __init__(self, name, size=1, height=None):
        debug.info(1, "Creating pnand2 {}".format(name))
        self.add_comment("size: {}".format(size))
        
        self.size = size
        
        # Creates the netlist and layout        
        pgate.pgate.__init__(self, name, height)

    def create_netlist(self):
        self.add_pins()
        self.create_modules()
        self.create_insts()

    def create_modules(self):
        # Shield the cap, but have at least a stage effort of 4
        self.nand = factory.create(module_type="pnand2",height=self.height) 
        self.add_mod(self.nand)

        self.inv = factory.create(module_type="pdriver", neg_polarity=True, fanout=3*self.size, height=self.height)
        self.add_mod(self.inv)

    def create_layout(self):
        self.width = self.nand.width + self.inv.width
        self.place_insts()
        self.add_wires()
        self.add_layout_pins()
        self.DRC_LVS()
        
    def add_pins(self):
        self.add_pin("A", "INPUT")
        self.add_pin("B", "INPUT")
        self.add_pin("Z", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_insts(self):
        self.nand_inst=self.add_inst(name="pand2_nand",
                                     mod=self.nand)
        self.connect_inst(["A", "B", "zb_int",  "vdd", "gnd"])
        
        self.inv_inst=self.add_inst(name="pand2_inv",
                                    mod=self.inv)
        self.connect_inst(["zb_int", "Z",  "vdd", "gnd"])

    def place_insts(self):
        # Add NAND to the right 
        self.nand_inst.place(offset=vector(0,0))

        # Add INV to the right
        self.inv_inst.place(offset=vector(self.nand_inst.rx(),0))
        
    def add_wires(self):
        # nand Z to inv A
        z1_pin = self.nand_inst.get_pin("Z")
        a2_pin = self.inv_inst.get_pin("A")
        mid1_point = vector(0.5*(z1_pin.cx()+a2_pin.cx()), z1_pin.cy())
        mid2_point = vector(mid1_point, a2_pin.cy())
        self.add_path("metal1", [z1_pin.center(), mid1_point, mid2_point, a2_pin.center()])
        
        
    def add_layout_pins(self):
        # Continous vdd rail along with label.
        vdd_pin=self.inv_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
        
        # Continous gnd rail along with label.
        gnd_pin=self.inv_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=gnd_pin.ll().scale(0,1),
                            width=self.width,
                            height=vdd_pin.height())
            
        pin = self.inv_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Z",
                                        layer=pin.layer,
                                        offset=pin.center(),
                                        width=pin.width(),
                                        height=pin.height())

        for pin_name in ["A","B"]:
            pin = self.nand_inst.get_pin(pin_name)
            self.add_layout_pin_rect_center(text=pin_name,
                                            layer=pin.layer,
                                            offset=pin.center(),
                                            width=pin.width(),
                                            height=pin.height())
        
    def get_stage_efforts(self, external_cout, inp_is_rise=False):
        """Get the stage efforts of the A or B -> Z path"""
        stage_effort_list = []
        stage1_cout = self.inv.get_cin()
        stage1 = self.nand.get_stage_effort(stage1_cout, inp_is_rise)
        stage_effort_list.append(stage1)
        last_stage_is_rise = stage1.is_rise
        
        stage2 = self.inv.get_stage_effort(external_cout, last_stage_is_rise)
        stage_effort_list.append(stage2)
        
        return stage_effort_list

    def get_cin(self):
        """Return the relative input capacitance of a single input"""
        return self.nand.get_cin()
        
