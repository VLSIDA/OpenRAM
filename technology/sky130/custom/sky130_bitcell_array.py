#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.modules.bitcell_array import bitcell_array
from openram.modules import pattern
from openram.sram_factory import factory
from openram.base import geometry
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array
from math import ceil

class sky130_bitcell_array(bitcell_array, sky130_bitcell_base_array):
    """
    Creates a rows x cols array of memory cells.
    Assumes bit-lines and word lines are connected by abutment.
    """
    def __init__(self, rows, cols, column_offset=0, name=""):
        if rows % 2 == 0:
            debug.error("Invalid number of rows {}. number of rows (excluding dummy rows) must be odd to connect to col ends".format(rows), -1)
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)

    def add_modules(self):
        """ Add the modules used in this design """
        # Bitcell for port names only
        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")
        self.cella = factory.create(module_type=OPTS.bitcell, version="opt1a")
        self.strap = factory.create(module_type="internal", version="wlstrap")
        self.strap_p = factory.create(module_type="internal", version="wlstrap_p")
        self.strapa = factory.create(module_type="internal", version="wlstrapa")
        self.strapa_p = factory.create(module_type="internal", version="wlstrapa_p")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.all_inst={}
        self.cell_inst={}
 
        bit_row_opt1 = [geometry.instance("00_opt1", mod=self.cell, is_bitcell=True, mirror='XY')] \
                     + [geometry.instance("01_strap_p", mod=self.strap_p, is_bitcell=False, mirror='MX')]\
                     + [geometry.instance("02_opt1", mod=self.cell, is_bitcell=True, mirror='MX')] \
                     + [geometry.instance("03_strap", mod=self.strap, is_bitcell=False, mirror='MX')]
  
        bit_row_opt1a = [geometry.instance("10_opt1a", mod=self.cella, is_bitcell=True, mirror='MY')] \
                      + [geometry.instance("11_strap_p", mod=self.strap_p, is_bitcell=False)] \
                      + [geometry.instance("12_opt1a", mod=self.cella, is_bitcell=True)] \
                      + [geometry.instance("13_strapa", mod=self.strapa, is_bitcell=False)]

        bit_block = []
        pattern.append_row_to_block(bit_block, bit_row_opt1)
        pattern.append_row_to_block(bit_block, bit_row_opt1a)
        for row in bit_block:
            row = pattern.rotate_list(row, self.column_offset * 2) 
        self.pattern = pattern(self, "bitcell_array", bit_block, num_rows=self.row_size, num_cols=self.column_size, num_cores_x=ceil(self.column_size/2), num_cores_y=ceil(self.row_size/2), name_template="bit_r{0}_c{1}")
        self.pattern.connect_array()

