# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#

from openram import debug
from openram.base import vector
from openram.base import contact
from openram.sram_factory import factory
from openram.tech import drc, spice
from openram.tech import cell_properties as props
from openram import OPTS
from openram.modules.capped_replica_bitcell_array import capped_replica_bitcell_array
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_capped_replica_bitcell_array(capped_replica_bitcell_array, sky130_bitcell_base_array):
    """
    Creates a replica bitcell array then adds the row and column caps to all
    sides of a bitcell array.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(rows, cols, rbl, left_rbl, right_rbl, name)

    def add_layout_pins(self):
        for used_name, base_name in zip(self.used_wordline_names, self.dummy_col_insts[0].mod.all_wordline_names):
            pin = self.dummy_col_insts[0].get_pin(base_name)

            pin_offset = pin.ll().scale(0, 1)
            pin_width  = self.width
            pin_height = pin.height()

            self.add_layout_pin(text=used_name,
                                layer=pin.layer,
                                offset=pin_offset,
                                width=pin_width,
                                height=pin_height)

        for used_name, pin_name in zip(self.bitline_pin_list, self.dummy_row_insts[0].mod.all_bitline_names):
            pin = self.dummy_row_insts[0].get_pin(pin_name)
            pin_offset = pin.ll().scale(1, 0)
            pin_width  = pin.width()
            pin_height = self.height
            self.add_layout_pin(text=used_name,
                                layer=pin.layer,
                                offset=pin_offset,
                                width=pin_width,
                                height=pin_height)


