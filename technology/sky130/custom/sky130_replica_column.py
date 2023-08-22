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

class sky130_replica_column(sky130_bitcell_base_array):
    """
    Generate a replica bitline column for the replica array.
    Rows is the total number of rows i the main array.
    rbl is a tuple with the number of left and right replica bitlines.
    Replica bit specifies which replica column this is (to determine where to put the
    replica cell relative to the bottom (including the dummy bit at 0).
    """

    def __init__(self, name, rows, rbl, replica_bit, column_offset=0):
        # Used for pin names and properties
        self.cell = factory.create(module_type=OPTS.bitcell)
        # Row size is the number of rows with word lines
        self.row_size = sum(rbl) + rows
        # Start of regular word line rows
        self.row_start = rbl[0] + 1
        # End of regular word line rows
        self.row_end = self.row_start + rows
        super().__init__(rows=self.row_size, cols=1, column_offset=column_offset, name=name)

        self.rows = rows
        self.left_rbl = rbl[0]
        self.right_rbl = rbl[1]
        self.replica_bit = replica_bit
        # left, right, regular rows plus top/bottom dummy cells

        self.total_size = self.left_rbl + rows + self.right_rbl
        self.column_offset = column_offset

        # if self.rows % 2 == 0:
        #     debug.error("Invalid number of rows {}. Number of rows must be even to connect to col ends".format(self.rows), -1)
        # if self.column_offset % 2 == 0:
        #     debug.error("Invalid column_offset {}. Column offset must be odd to connect to col ends".format(self.rows), -1)
        # debug.check(replica_bit != 0 and replica_bit != rows,
        #             "Replica bit cannot be the dummy row.")
        # debug.check(replica_bit <= self.left_rbl or replica_bit >= self.total_size - self.right_rbl - 1,
        #             "Replica bit cannot be in the regular array.")
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.place_array()

        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):

        self.create_all_bitline_names()
        #self.create_all_wordline_names(self.row_size+2)
        # +2 to add fake wl pins for colends
        self.create_all_wordline_names(self.row_size)
        self.add_pin_list(self.all_bitline_names, "OUTPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        #self.add_pin("top_gate", "INPUT")
        #self.add_pin("bot_gate", "INPUT")

    def add_modules(self):
        self.replica_cell = factory.create(module_type="replica_bitcell_1port", version="opt1")
        self.cell = self.replica_cell
        self.replica_cell2 = factory.create(module_type="replica_bitcell_1port", version="opt1a")

        self.dummy_cell = factory.create(module_type="dummy_bitcell_1port", version="opt1")
        self.dummy_cell2 = factory.create(module_type="dummy_bitcell_1port", version="opt1")

        self.strap = factory.create(module_type="internal", version="wlstrap_p")
        self.strap2 = factory.create(module_type="internal", version="wlstrapa_p")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.all_inst={}
        self.cell_inst={}
        replica_row_opt1 = [geometry.instance("00_rep_opt1", mod=self.replica_cell, is_bitcell=True, mirror='MX')] \
                     + [geometry.instance("01_strap1", mod=self.strap, is_bitcell=False, mirror='MX')]
  
        replica_row_opt1a = [geometry.instance("10_opt1a", mod=self.replica_cell2, is_bitcell=True)] \
                      + [geometry.instance("11_strapa", mod=self.strap2, is_bitcell=False)]

        replica_dummy_row_opt1 = [geometry.instance("00_rep_opt1", mod=self.dummy_cell, is_bitcell=True, mirror='MX')] \
                     + [geometry.instance("01_rep_strap", mod=self.strap, is_bitcell=False, mirror='MX')]
  
        replica_dummy_row_opt1a = [geometry.instance("10_opt1a", mod=self.dummy_cell2, is_bitcell=True)] \
                      + [geometry.instance("11_strapa", mod=self.strap2, is_bitcell=False)]

        bit_block = []
        current_row = self.row_start
        for row in range(self.total_size):
            # Regular array cells are replica cells
            # Replic bit specifies which other bit (in the full range (0,total_size) to make a replica cell.
            # All other cells are dummies
            if (row == self.replica_bit) or (row >= self.row_start and row < self.row_end):
                if current_row % 2:
                    pattern.append_row_to_block(bit_block, replica_row_opt1)
                else:
                    pattern.append_row_to_block(bit_block, replica_row_opt1a)
            else:
                if current_row %2:
                    pattern.append_row_to_block(bit_block, replica_dummy_row_opt1)
                else:
                    pattern.append_row_to_block(bit_block, replica_dummy_row_opt1a)
            current_row += 1
        self.pattern = pattern(self, "replica_column", bit_block, num_rows=self.total_size, num_cols=len(replica_row_opt1a), name_template="rbc_r{0}_c{1}", )
        self.pattern.connect_array_raw()

    def exclude_all_but_replica(self):
        """
        Excludes all bits except the replica cell (self.replica_bit).
        """
        for row, cell in self.cell_inst.items():
            if row != self.replica_bit:
                self.graph_inst_exclude.add(cell)
