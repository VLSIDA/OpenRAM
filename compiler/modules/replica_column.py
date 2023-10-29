# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer_properties as layer_props
from openram import OPTS
from .bitcell_base_array import bitcell_base_array
from openram.base import geometry
from openram.modules import pattern

class replica_column(bitcell_base_array):
    """
    Generate a replica bitline column for the replica array.
    Rows is the total number of rows in the main array.
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
        self.row_start = rbl[0]
        # End of regular word line rows
        self.row_end = self.row_start + rows
        super().__init__(rows=self.row_size, cols=1, column_offset=column_offset, name=name)

        self.rows = rows
        self.left_rbl = rbl[0]
        self.right_rbl = rbl[1]
        self.replica_bit = replica_bit

        # Total size includes the replica rows
        self.total_size = self.left_rbl + rows + self.right_rbl

        self.column_offset = column_offset

        debug.check(replica_bit < self.row_start or replica_bit >= self.row_end,
                    "Replica bit cannot be in the regular array.")

        #if layer_props.replica_column.even_rows:
        #    debug.check(rows % 2 == 0 and (self.left_rbl + 1) % 2 == 0,
        #                "sky130 currently requires rows to be even and to start with X mirroring"
        #                + " (left_rbl must be odd) for LVS.")

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

        self.route_supplies()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):

        self.create_all_bitline_names()
        self.create_all_wordline_names(self.row_size)

        self.add_pin_list(self.all_bitline_names, "OUTPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.replica_cell = factory.create(module_type=OPTS.replica_bitcell)

        self.dummy_cell = factory.create(module_type=OPTS.dummy_bitcell)

    def create_instances(self):
        self.cell_inst = {}
        core_block = [[0 for x in range(1)] for y in range(self.total_size)]

        current_row = self.row_start
        for row in range(self.total_size):
            # Regular array cells are replica cells
            # Replic bit specifies which other bit (in the full range (0,total_size) to make a replica cell.
            # All other cells are dummies
            if (row == self.replica_bit) or (row >= self.row_start and row < self.row_end):
                if current_row % 2 == 0:
                    core_block[row][0] = geometry.instance("rbc_{}".format(row), mod=self.replica_cell, is_bitcell=True)
                else:
                    core_block[row][0] = geometry.instance("rbc_{}".format(row), mod=self.replica_cell, is_bitcell=True, mirror='MX')
            else:
                if current_row % 2 == 0:
                    core_block[row][0] = geometry.instance("rbc_{}".format(row), mod=self.dummy_cell, is_bitcell=True)
                else:
                    core_block[row][0] = geometry.instance("rbc_{}".format(row), mod=self.dummy_cell, is_bitcell=True, mirror='MX')

            current_row += 1
        if self.cell.mirror.y:
            for row in range(self.total_size):
                if self.column_offset % 2 == 0:
                    if core_block[row][0].mirror=='MX':
                        core_block[row][0].mirror='XY'
                    else:
                        core_block[row][0].mirror='MY'
        self.pattern = pattern(self, "bitcell_array", core_block, num_rows=self.total_size, num_cols=self.column_size, name_template="rbc_r{0}_c{1}")
        self.pattern.connect_array()

    def get_bitcell_pins_col_cap(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        if len(self.edge_cell.get_pins("vdd")) > 0:
            bitcell_pins.append("vdd")
        if len(self.edge_cell.get_pins("gnd")) > 0:
            bitcell_pins.append("gnd")

        return bitcell_pins

    def exclude_all_but_replica(self):
        """
        Excludes all bits except the replica cell (self.replica_bit).
        """

        for row, cell in enumerate(self.cell_inst):
            if row != self.replica_bit:
                self.graph_inst_exclude.add(self.cell_inst[cell])
