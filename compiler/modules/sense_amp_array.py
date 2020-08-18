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

    def __init__(self, name, word_size, words_per_row, num_spare_cols=None, column_offset=0):

        super().__init__(name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("word_size {0}".format(word_size))
        self.add_comment("words_per_row: {0}".format(words_per_row))

        self.word_size = word_size
        self.words_per_row = words_per_row
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
        self.height = self.amp.height

        if self.bitcell.width > self.amp.width:
            self.width = self.bitcell.width * (self.word_size * self.words_per_row + self.num_spare_cols)
        else:
            self.width = self.amp.width * (self.word_size * self.words_per_row + self.num_spare_cols)

        self.place_sense_amp_array()
        self.add_layout_pins()
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

        self.add_mod(self.amp)

        # This is just used for measurements,
        # so don't add the module
        self.bitcell = factory.create(module_type="bitcell")

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
        from tech import cell_properties

        for i in range(0, self.row_size, self.words_per_row):
            index = int(i / self.words_per_row)
            xoffset = i * self.bitcell.width
            
            if cell_properties.bitcell.mirror.y and (i + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.amp.width
            else:
                mirror = ""

            amp_position = vector(xoffset, 0)
            self.local_insts[index].place(offset=amp_position, mirror=mirror)
            
        # place spare sense amps (will share the same enable as regular sense amps)
        for i in range(0, self.num_spare_cols):
            index = self.word_size + i
            xoffset = ((self.word_size * self.words_per_row) + i) * self.bitcell.width

            if cell_properties.bitcell.mirror.y and (i + self.column_offset) % 2:
                mirror = "MY"
                xoffset = xoffset + self.amp.width
            else:
                mirror = ""

            amp_position = vector(xoffset, 0)
            self.local_insts[index].place(offset=amp_position, mirror=mirror)

    def add_layout_pins(self):
        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]

            for gnd_pin in inst.get_pins("gnd"):
                self.add_power_pin(name="gnd",
                                   loc=gnd_pin.center(),
                                   start_layer=gnd_pin.layer,
                                   directions=("V", "V"))

            for vdd_pin in inst.get_pins("vdd"):
                self.add_power_pin(name="vdd",
                                   loc=vdd_pin.center(),
                                   start_layer=vdd_pin.layer,
                                   directions=("V", "V"))

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

    def input_load(self):
        return self.amp.input_load()

    def get_en_cin(self):
        """Get the relative capacitance of all the sense amp enable connections in the array"""
        sense_amp_en_cin = self.amp.get_en_cin()
        return sense_amp_en_cin * self.word_size

    def get_drain_cin(self):
        """Get the relative capacitance of the drain of the PMOS isolation TX"""
        from tech import parameter
        # Bitcell drain load being used to estimate PMOS drain load
        drain_load = logical_effort.convert_farad_to_relative_c(parameter['bitcell_drain_cap'])
        return drain_load
