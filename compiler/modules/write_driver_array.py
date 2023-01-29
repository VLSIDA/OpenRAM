# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import math
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import drc
from openram import OPTS


class write_driver_array(design):
    """
    Array of tristate drivers to write to the bitlines through the column mux.
    Dynamically generated write driver array of all bitlines.
    """

    def __init__(self, name, columns, word_size, offsets=None, num_spare_cols=None, write_size=None, column_offset=0):

        super().__init__(name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("columns: {0}".format(columns))
        self.add_comment("word_size {0}".format(word_size))

        self.columns = columns
        self.word_size = word_size
        if write_size is None:
            self.write_size = word_size
        else:
            self.write_size = write_size
        self.offsets = offsets
        self.column_offset = column_offset
        self.words_per_row = int(columns / word_size)
        if not num_spare_cols:
            self.num_spare_cols = 0
        else:
            self.num_spare_cols = num_spare_cols

        if self.write_size != self.word_size:
            self.num_wmasks = int(math.ceil(self.word_size / self.write_size))
        else:
            self.num_wmasks = 0

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

        self.place_write_array()
        self.width = self.local_insts[-1].rx()
        self.height = self.driver.height
        self.add_layout_pins()
        self.route_supplies()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size + self.num_spare_cols):
            self.add_pin(self.data_name + "_{0}".format(i), "INPUT")
        for i in range(self.word_size + self.num_spare_cols):
            self.add_pin(self.get_bl_name() + "_{0}".format(i), "OUTPUT")
            self.add_pin(self.get_br_name() + "_{0}".format(i), "OUTPUT")
        if self.write_size != self.word_size:
            for i in range(self.num_wmasks + self.num_spare_cols):
                self.add_pin(self.en_name + "_{0}".format(i), "INPUT")
        elif self.num_spare_cols and self.write_size == self.word_size:
            for i in range(self.num_spare_cols + 1):
                self.add_pin(self.en_name + "_{0}".format(i), "INPUT")
        else:
            self.add_pin(self.en_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.driver = factory.create(module_type="write_driver")

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type=OPTS.bitcell)

    def create_write_array(self):
        self.local_insts = []
        w = 0
        windex=0
        for i in range(0, self.columns, self.words_per_row):
            name = "write_driver{}".format(i)
            index = int(i / self.words_per_row)
            self.local_insts.append(self.add_inst(name=name,
                                                   mod=self.driver))

            if self.write_size != self.word_size:
                self.connect_inst([self.data_name + "_{0}".format(index),
                                   self.get_bl_name() + "_{0}".format(index),
                                   self.get_br_name() + "_{0}".format(index),
                                   self.en_name + "_{0}".format(windex), "vdd", "gnd"])
                w+=1
                # when w equals write size, the next en pin can be connected since we are now at the next wmask bit
                if w == self.write_size:
                    w = 0
                    windex+=1

            elif self.num_spare_cols and self.write_size == self.word_size:
                self.connect_inst([self.data_name + "_{0}".format(index),
                                   self.get_bl_name() + "_{0}".format(index),
                                   self.get_br_name() + "_{0}".format(index),
                                   self.en_name + "_{0}".format(0), "vdd", "gnd"])

            else:
                self.connect_inst([self.data_name + "_{0}".format(index),
                                   self.get_bl_name() + "_{0}".format(index),
                                   self.get_br_name() + "_{0}".format(index),
                                   self.en_name, "vdd", "gnd"])

        for i in range(self.num_spare_cols):
            index = self.word_size + i
            if self.write_size != self.word_size:
                offset = self.num_wmasks
            else:
                offset = 1
            name = "write_driver{}".format(self.columns + i)
            self.local_insts.append(self.add_inst(name=name,
                                                   mod=self.driver))

            self.connect_inst([self.data_name + "_{0}".format(index),
                               self.get_bl_name() + "_{0}".format(index),
                               self.get_br_name() + "_{0}".format(index),
                               self.en_name + "_{0}".format(i + offset), "vdd", "gnd"])

    def place_write_array(self):
        if self.bitcell.width > self.driver.width:
            self.driver_spacing = self.bitcell.width
        else:
            self.driver_spacing = self.driver.width

        if not self.offsets:
            self.offsets = []
            for i in range(self.columns + self.num_spare_cols):
                self.offsets.append(i * self.driver_spacing)

        for i, xoffset in enumerate(self.offsets[0:self.columns:self.words_per_row]):
            if self.bitcell.mirror.y and (i * self.words_per_row + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.driver.width
            else:
                mirror = ""

            base = vector(xoffset, 0)
            self.local_insts[i].place(offset=base, mirror=mirror)

        # place spare write drivers (if spare columns are specified)
        for i, xoffset in enumerate(self.offsets[self.columns:]):
            index = self.word_size + i

            if self.bitcell.mirror.y and (index + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.driver.width
            else:
                mirror = ""

            base = vector(xoffset, 0)
            self.local_insts[index].place(offset=base, mirror=mirror)

    def add_layout_pins(self):
        for i in range(self.word_size + self.num_spare_cols):
            inst = self.local_insts[i]
            din_pin = inst.get_pin(inst.mod.din_name)
            self.add_layout_pin(text=self.data_name + "_{0}".format(i),
                                layer=din_pin.layer,
                                offset=din_pin.ll(),
                                width=din_pin.width(),
                                height=din_pin.height())
            bl_pin = inst.get_pin(inst.mod.get_bl_names())
            self.add_layout_pin(text=self.get_bl_name() + "_{0}".format(i),
                                layer=bl_pin.layer,
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())

            br_pin = inst.get_pin(inst.mod.get_br_names())
            self.add_layout_pin(text=self.get_br_name() + "_{0}".format(i),
                                layer=br_pin.layer,
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())

        if self.write_size != self.word_size:
            for bit in range(self.num_wmasks):
                inst = self.local_insts[bit * self.write_size]
                en_pin = inst.get_pin(inst.mod.en_name)
                # Determine width of wmask modified en_pin with/without col mux
                wmask_en_len = self.words_per_row * (self.write_size * self.driver_spacing)
                if (self.words_per_row == 1):
                    en_gap = self.driver_spacing - en_pin.width()
                else:
                    en_gap = self.driver_spacing

                self.add_layout_pin(text=self.en_name + "_{0}".format(bit),
                                    layer=en_pin.layer,
                                    offset=en_pin.ll(),
                                    width=wmask_en_len - en_gap,
                                    height=en_pin.height())

            for i in range(self.num_spare_cols):
                inst = self.local_insts[self.word_size + i]
                en_pin = inst.get_pin(inst.mod.en_name)
                self.add_layout_pin(text=self.en_name + "_{0}".format(i + self.num_wmasks),
                                    layer="m1",
                                    offset=en_pin.lr() + vector(-drc("minwidth_m1"),0))

        elif self.num_spare_cols and self.write_size == self.word_size:
            # shorten enable rail to accomodate those for spare write drivers
            left_inst = self.local_insts[0]
            left_en_pin = left_inst.get_pin(inst.mod.en_name)
            right_inst = self.local_insts[-self.num_spare_cols - 1]
            right_en_pin = right_inst.get_pin(inst.mod.en_name)
            self.add_layout_pin(text=self.en_name + "_{0}".format(0),
                                layer="m1",
                                offset=left_en_pin.ll(),
                                width=right_en_pin.rx() - left_en_pin.lx())

            # individual enables for every spare write driver
            for i in range(self.num_spare_cols):
                inst = self.local_insts[self.word_size + i]
                en_pin = inst.get_pin(inst.mod.en_name)
                self.add_layout_pin(text=self.en_name + "_{0}".format(i + 1),
                                    layer="m1",
                                    offset=en_pin.lr() + vector(-drc("minwidth_m1"), 0))

        else:
            inst = self.local_insts[0]
            self.add_layout_pin(text=self.en_name,
                                layer="m1",
                                offset=inst.get_pin(inst.mod.en_name).ll().scale(0, 1),
                                width=self.width)

    def route_supplies(self):
        self.route_horizontal_pins("vdd")
        self.route_horizontal_pins("gnd")


