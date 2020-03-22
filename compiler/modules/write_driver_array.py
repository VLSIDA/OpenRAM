# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from math import log
import design
from tech import drc
import debug
from sram_factory import factory
from vector import vector
from globals import OPTS

class write_driver_array(design.design):
    """
    Array of tristate drivers to write to the bitlines through the column mux.
    Dynamically generated write driver array of all bitlines.
    """

    def __init__(self, name, columns, word_size,write_size=None):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("columns: {0}".format(columns))
        self.add_comment("word_size {0}".format(word_size))        

        self.columns = columns
        self.word_size = word_size
        self.write_size = write_size
        self.words_per_row = int(columns / word_size)

        if self.write_size:
            self.num_wmasks = int(self.word_size/self.write_size)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def get_bl_name(self):
        bl_name = "bl"
        return bl_name

    def get_br_name(self):
        br_name = "br"
        return br_name

    @property
    def data_name(self):
        return "data"

    @property
    def en_name(self):
        return "en"

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_write_array()
        
    def create_layout(self):
    
        if self.bitcell.width > self.driver.width:
            self.width = self.columns * self.bitcell.width
        else:
            self.width = self.columns * self.driver.width
        self.height = self.driver.height
        
        self.place_write_array()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size):
            self.add_pin(self.data_name + "_{0}".format(i), "INPUT")
        for i in range(self.word_size):
            self.add_pin(self.get_bl_name() + "_{0}".format(i), "OUTPUT")
            self.add_pin(self.get_br_name() + "_{0}".format(i), "OUTPUT")
        if self.write_size:
            for i in range(self.num_wmasks):
                self.add_pin(self.en_name + "_{0}".format(i), "INPUT")
        else:
            self.add_pin(self.en_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.driver = factory.create(module_type="write_driver")
        self.add_mod(self.driver)

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type="bitcell")

    def create_write_array(self):
        self.driver_insts = {}
        w = 0
        windex=0
        for i in range(0,self.columns,self.words_per_row):
            name = "write_driver{}".format(i)
            index = int(i/self.words_per_row)
            self.driver_insts[index]=self.add_inst(name=name,
                                                   mod=self.driver)

            if self.write_size:
                self.connect_inst([self.data_name + "_{0}".format(index),
                                   self.get_bl_name() + "_{0}".format(index),
                                   self.get_br_name() + "_{0}".format(index),
                                   self.en_name + "_{0}".format(windex), "vdd", "gnd"])
                w+=1
                # when w equals write size, the next en pin can be connected since we are now at the next wmask bit
                if w == self.write_size:
                    w = 0
                    windex+=1
            else:
                self.connect_inst([self.data_name + "_{0}".format(index),
                                   self.get_bl_name() + "_{0}".format(index),
                                   self.get_br_name() + "_{0}".format(index),
                                   self.en_name, "vdd", "gnd"])


    def place_write_array(self):
        from tech import cell_properties
        if self.bitcell.width > self.driver.width:
            self.driver_spacing = self.bitcell.width
        else:
            self.driver_spacing = self.driver.width
        for i in range(0,self.columns,self.words_per_row):
            index = int(i/self.words_per_row)
            xoffset = i * self.driver_spacing

            if cell_properties.bitcell.mirror.y and i % 2:
                mirror = "MY"
                xoffset = xoffset + self.driver.width
            else:
                mirror = ""

            base = vector(xoffset, 0)
            self.driver_insts[index].place(offset=base, mirror=mirror)

            
    def add_layout_pins(self):
        for i in range(self.word_size):
            inst = self.driver_insts[i]
            din_pin = inst.get_pin(inst.mod.din_name)
            self.add_layout_pin(text=self.data_name + "_{0}".format(i),
                                layer="m2",
                                offset=din_pin.ll(),
                                width=din_pin.width(),
                                height=din_pin.height())
            bl_pin = inst.get_pin(inst.mod.get_bl_names())
            self.add_layout_pin(text=self.get_bl_name() + "_{0}".format(i),
                                layer="m2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())

            br_pin = inst.get_pin(inst.mod.get_br_names())
            self.add_layout_pin(text=self.get_br_name() + "_{0}".format(i),
                                layer="m2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())

            for n in ["vdd", "gnd"]:
                pin_list = self.driver_insts[i].get_pins(n)
                for pin in pin_list:
                    self.add_power_pin(name = n,
                                       loc = pin.center(),
                                       vertical=True,
                                       start_layer = "m2")
        if self.write_size:
            for bit in range(self.num_wmasks):
                inst = self.driver_insts[bit*self.write_size]
                en_pin = inst.get_pin(inst.mod.en_name)
                # Determine width of wmask modified en_pin with/without col mux
                wmask_en_len = self.words_per_row*(self.write_size * self.driver_spacing)
                if (self.words_per_row == 1):
                    en_gap = self.driver_spacing - en_pin.width()
                else:
                    en_gap = self.driver_spacing

                self.add_layout_pin(text=self.en_name + "_{0}".format(bit),
                                    layer=en_pin.layer,
                                    offset=en_pin.ll(),
                                    width=wmask_en_len-en_gap,
                                    height=en_pin.height())
        else:
            inst = self.driver_insts[0]
            self.add_layout_pin(text=self.en_name,
                                layer="m1",
                                offset=inst.get_pin(inst.mod.en_name).ll().scale(0,1),
                                width=self.width)


                       

    def get_w_en_cin(self):
        """Get the relative capacitance of all the enable connections in the bank"""
        #The enable is connected to a nand2 for every row.
        return self.driver.get_w_en_cin() * len(self.driver_insts)
