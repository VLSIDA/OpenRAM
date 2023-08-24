#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import geometry
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array
from openram.modules import pattern
from openram.modules import replica_column
class sky130_replica_column(replica_column, sky130_bitcell_base_array):
    """
    Generate a replica bitline column for the replica array.
    Rows is the total number of rows i the main array.
    rbl is a tuple with the number of left and right replica bitlines.
    Replica bit specifies which replica column this is (to determine where to put the
    replica cell relative to the bottom (including the dummy bit at 0).
    """

    def __init__(self, name, rows, rbl, replica_bit, column_offset=0):
        super().__init__(name=name, rows=rows, rbl=rbl, replica_bit=replica_bit, column_offset=column_offset)

    def add_modules(self):
        self.replica_cell = factory.create(module_type="replica_bitcell_1port", version="opt1")
        self.cell = self.replica_cell
        self.replica_cell2 = factory.create(module_type="replica_bitcell_1port", version="opt1a")

        self.dummy_cell = factory.create(module_type="dummy_bitcell_1port", version="opt1")
        self.dummy_cell2 = factory.create(module_type="dummy_bitcell_1port", version="opt1a")

        self.strap = factory.create(module_type="internal", version="wlstrap")
        self.strap_p = factory.create(module_type="internal", version="wlstrap_p")
        self.strapa = factory.create(module_type="internal", version="wlstrapa")
        self.strapa_p = factory.create(module_type="internal", version="wlstrapa_p")
    def create_instances(self):
        """ Create the module instances used in this design """
        self.all_inst={}
        self.cell_inst={}

        replica_row_opt1 = [geometry.instance("rep_00_opt1", mod=self.replica_cell, is_bitcell=True, mirror='XY')] \
                     + [geometry.instance("rep_01_strap", mod=self.strap_p, is_bitcell=False, mirror='MX')]\
                     + [geometry.instance("rep_02_opt1", mod=self.replica_cell, is_bitcell=True, mirror='MX')] \
                     + [geometry.instance("rep_03_strap_p", mod=self.strap, is_bitcell=False, mirror='MX')]
  
        replica_row_opt1a = [geometry.instance("rep_10_opt1a", mod=self.replica_cell2, is_bitcell=True, mirror='MY')] \
                      + [geometry.instance("rep_11_strapa", mod=self.strap_p, is_bitcell=False)] \
                      + [geometry.instance("rep_12_opt1a", mod=self.replica_cell2, is_bitcell=True)] \
                      + [geometry.instance("rep_13_strapa_p", mod=self.strapa, is_bitcell=False)]

        dummy_row_opt1 = [geometry.instance("dummy_00_opt1", mod=self.dummy_cell, is_bitcell=True, mirror='XY')] \
                     + [geometry.instance("dummy_01_strap", mod=self.strap_p, is_bitcell=False, mirror='MX')]\
                     + [geometry.instance("dummy_02_opt1", mod=self.dummy_cell, is_bitcell=True, mirror='MX')] \
                     + [geometry.instance("dummy_03_strap_p", mod=self.strap, is_bitcell=False, mirror='MX')]
  
        dummy_row_opt1a = [geometry.instance("dummy_10_opt1a", mod=self.dummy_cell2, is_bitcell=True, mirror='MY')] \
                      + [geometry.instance("dummy_11_strapa", mod=self.strap_p, is_bitcell=False)] \
                      + [geometry.instance("dummy_12_opt1a", mod=self.dummy_cell2, is_bitcell=True)] \
                      + [geometry.instance("dummy_13_strapa_p", mod=self.strapa, is_bitcell=False)]

        bit_block = []
        if self.column_offset % 2:
            replica_row_opt1 = replica_row_opt1[0:2]
            replica_row_opt1a = replica_row_opt1a[0:2]
            dummy_row_opt1 = dummy_row_opt1[0:2]
            dummy_row_opt1a = dummy_row_opt1a[0:2]
        else:
            replica_row_opt1 = replica_row_opt1[2:4]
            replica_row_opt1a = replica_row_opt1a[2:4]
            dummy_row_opt1 = dummy_row_opt1[2:4]
            dummy_row_opt1a = dummy_row_opt1a[2:4]

        current_row = self.row_start
        for row in range(self.total_size):
            # Regular array cells are replica cells
            # Replic bit specifies which other bit (in the full range (0,total_size) to make a replica cell.
            # All other cells are dummies
            if (row == self.replica_bit) or (row >= self.row_start and row < self.row_end):
                if current_row % 2 == 0:
                    pattern.append_row_to_block(bit_block, replica_row_opt1)
                else:
                    pattern.append_row_to_block(bit_block, replica_row_opt1a)
            else:
                if current_row % 2 == 0:
                    pattern.append_row_to_block(bit_block, dummy_row_opt1)
                else:
                    pattern.append_row_to_block(bit_block, dummy_row_opt1a)
            current_row += 1
        self.pattern = pattern(self, "replica_column", bit_block, num_rows=self.total_size, num_cols=len(replica_row_opt1), name_template="rbc_r{0}_c{1}")
        self.pattern.connect_array_raw()

