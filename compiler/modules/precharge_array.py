# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
import debug
from tech import drc
from vector import vector
from sram_factory import factory
from globals import OPTS

class precharge_array(design.design):
    """
    Dynamically generated precharge array of all bitlines.  Cols is number
    of bit line columns, height is the height of the bit-cell array.
    """

    def __init__(self, name, columns, size=1, bitcell_bl="bl", bitcell_br="br"):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("cols: {0} size: {1} bl: {2} br: {3}".format(columns, size, bitcell_bl, bitcell_br))
        
        self.columns = columns
        self.size = size
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def add_pins(self):
        """Adds pins for spice file"""
        for i in range(self.columns):
            # These are outputs from the precharge only
            self.add_pin("bl_{0}".format(i), "OUTPUT")
            self.add_pin("br_{0}".format(i), "OUTPUT")
        self.add_pin("en_bar", "INPUT")
        self.add_pin("vdd", "POWER")

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_insts()
        
    def create_layout(self):
        self.width = self.columns * self.pc_cell.width
        self.height = self.pc_cell.height

        self.place_insts()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        self.pc_cell = factory.create(module_type="precharge",
                                      size=self.size,
                                      bitcell_bl=self.bitcell_bl,
                                      bitcell_br=self.bitcell_br)
                       
        
        self.add_mod(self.pc_cell)

        
    def add_layout_pins(self):

        self.add_layout_pin(text="en_bar",
                            layer="metal1",
                            offset=self.pc_cell.get_pin("en_bar").ll(),
                            width=self.width,
                            height=drc("minwidth_metal1"))

        for inst in self.local_insts:
            self.copy_layout_pin(inst, "vdd")
            
        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]
            bl_pin = inst.get_pin("bl")
            self.add_layout_pin(text="bl_{0}".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=drc("minwidth_metal2"),
                                height=bl_pin.height())
            br_pin = inst.get_pin("br") 
            self.add_layout_pin(text="br_{0}".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=drc("minwidth_metal2"),
                                height=bl_pin.height())
        

    def create_insts(self):
        """Creates a precharge array by horizontally tiling the precharge cell"""
        self.local_insts = []
        for i in range(self.columns):
            name = "pre_column_{0}".format(i)
            offset = vector(self.pc_cell.width * i, 0)
            inst = self.add_inst(name=name,
                                 mod=self.pc_cell,
                                 offset=offset)
            self.local_insts.append(inst)
            self.connect_inst(["bl_{0}".format(i), "br_{0}".format(i), "en_bar", "vdd"])


    def place_insts(self):
        """ Places precharge array by horizontally tiling the precharge cell"""
        for i in range(self.columns):
            offset = vector(self.pc_cell.width * i, 0)
            self.local_insts[i].place(offset)                                   

    def get_en_cin(self):
        """Get the relative capacitance of all the clk connections in the precharge array"""        
        #Assume single port
        precharge_en_cin = self.pc_cell.get_en_cin()
        return precharge_en_cin*self.columns  
        
