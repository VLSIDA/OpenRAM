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

    def __init__(self, name, columns, word_size):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))

        self.columns = columns
        self.word_size = word_size
        self.words_per_row = int(columns / word_size)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


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
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size):
            self.add_pin("data_{0}".format(i))
        for i in range(self.word_size):            
            self.add_pin("bl_{0}".format(i))
            self.add_pin("br_{0}".format(i))
        self.add_pin("en")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        self.driver = factory.create(module_type="write_driver")
        self.add_mod(self.driver)

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type="bitcell")

    def create_write_array(self):
        self.driver_insts = {}
        for i in range(0,self.columns,self.words_per_row):
            name = "write_driver{}".format(i)
            index = int(i/self.words_per_row)
            self.driver_insts[index]=self.add_inst(name=name,
                                                   mod=self.driver)

            self.connect_inst(["data_{0}".format(index),
                               "bl_{0}".format(index),
                               "br_{0}".format(index),
                               "en", "vdd", "gnd"])


    def place_write_array(self):
        if self.bitcell.width > self.driver.width:
            driver_spacing = self.bitcell.width
        else:
            driver_spacing = self.driver.width
    
        for i in range(0,self.columns,self.words_per_row):
            index = int(i/self.words_per_row)            
            base = vector(i * driver_spacing,0)
            self.driver_insts[index].place(base)

            
    def add_layout_pins(self):
        for i in range(self.word_size):
            din_pin = self.driver_insts[i].get_pin("din")
            self.add_layout_pin(text="data_{0}".format(i),
                                layer="metal2",
                                offset=din_pin.ll(),
                                width=din_pin.width(),
                                height=din_pin.height())
            bl_pin = self.driver_insts[i].get_pin("bl")            
            self.add_layout_pin(text="bl_{0}".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())
                           
            br_pin = self.driver_insts[i].get_pin("br")
            self.add_layout_pin(text="br_{0}".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())

            for n in ["vdd", "gnd"]:
                pin_list = self.driver_insts[i].get_pins(n)
                for pin in pin_list:
                    pin_pos = pin.center()
                    # Add the M2->M3 stack 
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_pos)
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="metal3",
                                                    offset=pin_pos)



        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=self.driver_insts[0].get_pin("en").ll().scale(0,1),
                            width=self.width,
                            height=drc('minwidth_metal1'))
                       
                       

    def get_w_en_cin(self):
        """Get the relative capacitance of all the enable connections in the bank"""
        #The enable is connected to a nand2 for every row.
        return self.driver.get_w_en_cin() * len(self.driver_insts)
