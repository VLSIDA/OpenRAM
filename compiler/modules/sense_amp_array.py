# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import cell_properties
from openram import OPTS


class sense_amp_array(design):
    """
    Array of sense amplifiers to read the bitlines through the column mux.
    Dynamically generated sense amp array for all bitlines.
    """

    def __init__(self, name, word_size, words_per_row, offsets=None, num_spare_cols=None, column_offset=0):

        super().__init__(name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("word_size {0}".format(word_size))
        self.add_comment("words_per_row: {0}".format(words_per_row))

        self.word_size = word_size
        self.words_per_row = words_per_row
        self.num_cols = word_size * words_per_row
        self.offsets = offsets
        if not num_spare_cols:
            self.num_spare_cols = 0
        else:
            self.num_spare_cols = num_spare_cols

        self.column_offset = column_offset
        self.row_size = self.word_size * self.words_per_row

        if OPTS.tech_name == "sky130":
            self.en_layer = "m3"
        else:
            self.en_layer = "m1"
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
        self.create_sense_amp_array()

    def create_layout(self):

        self.place_sense_amp_array()

        self.height = self.amp.height
        self.width = self.local_insts[-1].rx()

        self.add_layout_pins()

        self.route_supplies()
        self.route_rails()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(0, self.word_size + self.num_spare_cols):
            self.add_pin(self.data_name + "_{0}".format(i), "OUTPUT")
            self.add_pin(self.get_bl_name() + "_{0}".format(i), "INPUT")
            self.add_pin(self.get_br_name() + "_{0}".format(i), "INPUT")
        self.add_pin(self.en_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.amp = factory.create(module_type="sense_amp")

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type=OPTS.bitcell)

    def create_sense_amp_array(self):
        self.local_insts = []
        for i in range(0, self.word_size + self.num_spare_cols):
            name = "sa_d{0}".format(i)
            self.local_insts.append(self.add_inst(name=name,
                                                  mod=self.amp))
            self.connect_inst([self.get_bl_name() + "_{0}".format(i),
                               self.get_br_name() + "_{0}".format(i),
                               self.data_name + "_{0}".format(i),
                               self.en_name, "vdd", "gnd"])

    def place_sense_amp_array(self):
        cell = factory.create(module_type=OPTS.bitcell)
        if(cell_properties.use_strap  == True and OPTS.num_ports == 1):
            strap = factory.create(module_type=cell_properties.strap_module, version=cell_properties.strap_version)
            precharge_width = cell.width + strap.width
        else:
            precharge_width = cell.width

        if precharge_width > self.amp.width:
            self.amp_spacing = precharge_width
        else:
            self.amp_spacing = self.amp.width

        if not self.offsets:
            self.offsets = []
            for i in range(self.num_cols + self.num_spare_cols):
                self.offsets.append(i * self.amp_spacing)

        for i, xoffset in enumerate(self.offsets[0:self.num_cols:self.words_per_row]):
            if self.bitcell.mirror.y and (i * self.words_per_row + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.amp_spacing
            else:
                mirror = ""

            amp_position = vector(xoffset, 0)
            self.local_insts[i].place(offset=amp_position, mirror=mirror)
        # place spare sense amps (will share the same enable as regular sense amps)
        for i, xoffset in enumerate(self.offsets[self.num_cols:]):
            index = self.word_size + i
            if self.bitcell.mirror.y and (index + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.amp_spacing
            else:
                mirror = ""

            amp_position = vector(xoffset, 0)
            self.local_insts[index].place(offset=amp_position, mirror=mirror)

    def add_layout_pins(self):
        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]

            bl_pin = inst.get_pin(inst.mod.get_bl_names())
            br_pin = inst.get_pin(inst.mod.get_br_names())
            dout_pin = inst.get_pin(inst.mod.dout_name)

            self.add_layout_pin(text=self.get_bl_name() + "_{0}".format(i),
                                layer=bl_pin.layer,
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())
            self.add_layout_pin(text=self.get_br_name() + "_{0}".format(i),
                                layer=br_pin.layer,
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())

            self.add_layout_pin(text=self.data_name + "_{0}".format(i),
                                layer=dout_pin.layer,
                                offset=dout_pin.ll(),
                                width=dout_pin.width(),
                                height=dout_pin.height())

    def route_supplies(self):
        self.route_horizontal_pins("vdd")
        self.route_horizontal_pins("gnd")

    def route_rails(self):
        # Add enable across the array
        en_pin = self.amp.get_pin(self.amp.en_name)
        start_offset = en_pin.lc().scale(0, 1)
        end_offset = start_offset + vector(self.width, 0)
        self.add_layout_pin_segment_center(text=self.en_name,
                                           layer=self.en_layer,
                                           start=start_offset,
                                           end=end_offset)
        for inst in self.local_insts:
            self.add_via_stack_center(from_layer=en_pin.layer,
                                      to_layer=self.en_layer,
                                      offset=inst.get_pin(self.amp.en_name).center())
