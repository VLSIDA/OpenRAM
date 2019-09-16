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


class write_mask_and_array(design.design):
    """
    Array of AND gates to turn write mask signal on only when w_en is on.
    The write mask AND array goes between the write driver array and the sense amp array.
    """

    def __init__(self, name, columns, word_size, write_size, port=0):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("columns: {0}".format(columns))
        self.add_comment("word_size {0}".format(word_size))
        self.add_comment("write_size {0}".format(write_size))

        self.columns = columns
        self.word_size = word_size
        self.write_size = write_size
        self.port = port
        self.words_per_row = int(columns / word_size)
        self.num_wmasks = int(word_size / write_size)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_and2_array()


    def create_layout(self):
        self.place_and2_array()
        spacing = self.wmask_en_len - self.and2.width
        self.width = (self.num_wmasks*self.and2.width) + ((self.num_wmasks-1)*spacing)
        self.height = self.and2.height
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        for bit in range(self.num_wmasks):
            self.add_pin("wmask_in_{}".format(bit),"INPUT")
        self.add_pin("en", "INPUT")
        for bit in range(self.num_wmasks):
            self.add_pin("wmask_out_{}".format(bit),"OUTPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

    def add_modules(self):
        # Size the AND gate for the number of write drivers it drives, which is equal to the write size.
        # Assume stage effort of 3 to compute the size
        self.and2 = factory.create(module_type="pand2",
                                   size=self.write_size/4.0)
        self.add_mod(self.and2)


    def create_and2_array(self):
        self.and2_insts = {}
        for bit in range(self.num_wmasks):
            name = "and2_{}".format(bit)
            self.and2_insts[bit] = self.add_inst(name=name,
                                                 mod=self.and2)
            self.connect_inst(["wmask_in_{}".format(bit),
                               "en",
                               "wmask_out_{}".format(bit),
                               "vdd", "gnd"])


    def place_and2_array(self):
        # Place the write mask AND array at the start of each write driver enable length.
        # This ensures the write mask AND array will be directly under the corresponding write driver enable wire.

        # This is just used for measurements, so don't add the module
        self.bitcell = factory.create(module_type="bitcell")
        self.driver = factory.create(module_type="write_driver")
        if self.bitcell.width > self.driver.width:
            self.driver_spacing = self.bitcell.width
        else:
            self.driver_spacing = self.driver.width

        self.wmask_en_len = self.words_per_row * (self.write_size * self.driver_spacing)
        debug.check(self.wmask_en_len >= self.and2.width,
                    "Write mask AND is wider than the corresponding write drivers {0} vs {1}.".format(self.and2.width,self.wmask_en_len))

        for i in range(self.num_wmasks):
            base = vector(i * self.wmask_en_len, 0)
            self.and2_insts[i].place(base)


    def add_layout_pins(self):
        self.nand2 = factory.create(module_type="pnand2")
        supply_pin=self.nand2.get_pin("vdd")

        # Create the enable pin that connects all write mask AND array's B pins
        beg_en_pin = self.and2_insts[0].get_pin("B")
        end_en_pin = self.and2_insts[self.num_wmasks-1].get_pin("B")
        if self.port % 2:
            # Extend metal3 to edge of AND array in multiport
            en_to_edge = self.and2.width - beg_en_pin.cx()
            self.add_layout_pin(text="en",
                                layer="metal3",
                                offset=beg_en_pin.bc(),
                                width=end_en_pin.cx() - beg_en_pin.cx() + en_to_edge)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=vector(end_en_pin.cx() + en_to_edge, end_en_pin.cy()))
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=vector(end_en_pin.cx() + en_to_edge, end_en_pin.cy()))
        else:
            self.add_layout_pin(text="en",
                                layer="metal3",
                                offset=beg_en_pin.bc(),
                                width=end_en_pin.cx() - beg_en_pin.cx())

        for i in range(self.num_wmasks):
            # Copy remaining layout pins
            self.copy_layout_pin(self.and2_insts[i],"A","wmask_in_{0}".format(i))
            self.copy_layout_pin(self.and2_insts[i],"Z","wmask_out_{0}".format(i))

            # Add via connections to metal3 for AND array's B pin
            en_pin = self.and2_insts[i].get_pin("B")
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=en_pin.center())
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=en_pin.center())

            self.add_power_pin("gnd", vector(supply_pin.width() + i * self.wmask_en_len, 0))
            self.add_power_pin("vdd", vector(supply_pin.width() + i * self.wmask_en_len, self.height))
            # Route power and ground rails together
            if i < self.num_wmasks-1:
                for n in ["gnd","vdd"]:
                    pin = self.and2_insts[i].get_pin(n)
                    next_pin = self.and2_insts[i+1].get_pin(n)
                    self.add_path("metal1",[pin.center(),next_pin.center()])

    def get_cin(self):
        """Get the relative capacitance of all the input connections in the bank"""
        # The enable is connected to an and2 for every row.
        return self.and2.get_cin() * len(self.and2_insts)


