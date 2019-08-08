# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from tech import drc
from vector import vector
from sram_factory import factory
import debug
from globals import OPTS
import logical_effort

class sense_amp_array(design.design):
    """
    Array of sense amplifiers to read the bitlines through the column mux.
    Dynamically generated sense amp array for all bitlines.
    """

    def __init__(self, name, word_size, words_per_row):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("word_size {0}".format(word_size))        
        self.add_comment("words_per_row: {0}".format(words_per_row))

        self.word_size = word_size
        self.words_per_row = words_per_row
        self.row_size = self.word_size * self.words_per_row

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_sense_amp_array()

    def create_layout(self):
        self.height = self.amp.height
        
        if self.bitcell.width > self.amp.width:
            self.width = self.bitcell.width * self.word_size * self.words_per_row
        else:
            self.width = self.amp.width * self.word_size * self.words_per_row

        self.place_sense_amp_array()
        self.add_layout_pins()
        self.route_rails()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(0,self.word_size):
            self.add_pin("data_{0}".format(i), "OUTPUT")
            self.add_pin("bl_{0}".format(i), "INPUT")
            self.add_pin("br_{0}".format(i), "INPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        
    def add_modules(self):
        self.amp = factory.create(module_type="sense_amp")
                   
        self.add_mod(self.amp)

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type="bitcell")
        
    def create_sense_amp_array(self):
        self.local_insts = []
        for i in range(0,self.word_size):

            name = "sa_d{0}".format(i)
            self.local_insts.append(self.add_inst(name=name,
                                                  mod=self.amp))
            self.connect_inst(["bl_{0}".format(i),
                               "br_{0}".format(i), 
                               "data_{0}".format(i), 
                               "en", "vdd", "gnd"])

    def place_sense_amp_array(self):
            
        if self.bitcell.width > self.amp.width:
            amp_spacing = self.bitcell.width * self.words_per_row
        else:
            amp_spacing = self.amp.width * self.words_per_row
        for i in range(0,self.word_size):
            amp_position = vector(amp_spacing * i, 0)
            self.local_insts[i].place(amp_position)

        
    def add_layout_pins(self):
        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]
            
            gnd_pos = inst.get_pin("gnd").center()
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=gnd_pos)
            self.add_layout_pin_rect_center(text="gnd",
                                            layer="metal3",
                                            offset=gnd_pos)
            vdd_pos = inst.get_pin("vdd").center()
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=vdd_pos)
            self.add_layout_pin_rect_center(text="vdd",
                                            layer="metal3",
                                            offset=vdd_pos)

            bl_pin = inst.get_pin("bl")            
            br_pin = inst.get_pin("br")
            dout_pin = inst.get_pin("dout")
            
            self.add_layout_pin(text="bl_{0}".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())
            self.add_layout_pin(text="br_{0}".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())
                           
            self.add_layout_pin(text="data_{0}".format(i),
                                layer="metal2",
                                offset=dout_pin.ll(),
                                width=dout_pin.width(),
                                height=dout_pin.height())
                           
            
    def route_rails(self):
        # add sclk rail across entire array
        sclk_offset = self.amp.get_pin("en").ll().scale(0,1)
        self.add_layout_pin(text="en",
                      layer="metal1",
                      offset=sclk_offset,
                      width=self.width,
                      height=drc("minwidth_metal1"))

    def input_load(self):
        return self.amp.input_load()
      
    def get_en_cin(self):
        """Get the relative capacitance of all the sense amp enable connections in the array"""
        sense_amp_en_cin = self.amp.get_en_cin()
        return sense_amp_en_cin * self.word_size
        
    def get_drain_cin(self):
        """Get the relative capacitance of the drain of the PMOS isolation TX"""
        from tech import parameter
        #Bitcell drain load being used to estimate PMOS drain load
        drain_load = logical_effort.convert_farad_to_relative_c(parameter['bitcell_drain_cap'])
        return drain_load
