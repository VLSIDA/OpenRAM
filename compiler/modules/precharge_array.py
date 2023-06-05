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
from openram import OPTS


class precharge_array(design):
    """
    Dynamically generated precharge array of all bitlines.  Cols is number
    of bit line columns, height is the height of the bit-cell array.
    """

    def __init__(self, name, columns, offsets=None, size=1, bitcell_bl="bl", bitcell_br="br", column_offset=0):
        super().__init__(name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("cols: {0} size: {1} bl: {2} br: {3}".format(columns, size, bitcell_bl, bitcell_br))

        self.columns = columns
        self.offsets = offsets
        self.size = size
        self.bitcell_bl = bitcell_bl
        self.bitcell_br = bitcell_br
        self.column_offset = column_offset

        if OPTS.tech_name == "sky130":
            self.en_bar_layer = "m3"
        else:
            self.en_bar_layer = "m1"

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def get_bl_name(self):
        bl_name = self.pc_cell.get_bl_names()
        return bl_name

    def get_br_name(self):
        br_name = self.pc_cell.get_br_names()
        return br_name

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
        self.place_insts()

        self.width = self.offsets[-1] + self.pc_cell.width
        self.height = self.pc_cell.height

        self.add_layout_pins()
        self.route_supplies()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        self.pc_cell = factory.create(module_type=OPTS.precharge,
                                      size=self.size,
                                      bitcell_bl=self.bitcell_bl,
                                      bitcell_br=self.bitcell_br)

        self.cell = factory.create(module_type=OPTS.bitcell)

    def add_layout_pins(self):

        en_pin = self.pc_cell.get_pin("en_bar")
        self.route_horizontal_pins("en_bar", layer=self.en_bar_layer)
        for inst in self.local_insts:
            self.add_via_stack_center(from_layer=en_pin.layer,
                                      to_layer=self.en_bar_layer,
                                      offset=inst.get_pin("en_bar").center())

        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]
            self.copy_layout_pin(inst, "bl", "bl_{0}".format(i))
            self.copy_layout_pin(inst, "br", "br_{0}".format(i))

    def route_supplies(self):
        self.route_horizontal_pins("vdd")

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

        # Default to single spaced columns
        if not self.offsets:
            self.offsets = [n * self.pc_cell.width for n in range(self.columns)]

        for i, xoffset in enumerate(self.offsets):
            if self.cell.mirror.y and (i + self.column_offset) % 2:
                mirror = "MY"
                tempx = xoffset + self.pc_cell.width
            else:
                mirror = ""
                tempx = xoffset

            offset = vector(tempx, 0)
            self.local_insts[i].place(offset=offset, mirror=mirror)
