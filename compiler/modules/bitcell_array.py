# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import drc, spice
from openram.sram_factory import factory
from openram import OPTS
from .bitcell_base_array import bitcell_base_array


class bitcell_array(bitcell_base_array):
    """
    Creates a rows x cols array of memory cells.
    Assumes bit-lines and word lines are connected by abutment.
    """
    def __init__(self, rows, cols, column_offset=0, name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        # This will create a default set of bitline/wordline names
        self.create_all_bitline_names()
        self.create_all_wordline_names()

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        # We don't offset this because we need to align
        # the replica bitcell in the control logic
        # self.offset_all_coordinates()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("bit_r{0}_c{1}")

        self.add_layout_pins()

        self.route_supplies()

        self.add_boundary()

        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.cell = factory.create(module_type=OPTS.bitcell)

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.cell)
                self.connect_inst(self.get_bitcell_pins(row, col))

                # If it is a "core" cell, it could be trimmed for sim time
                if col>0 and col<self.column_size-1 and row>0 and row<self.row_size-1:
                    self.trim_insts.add(name)

    def analytical_power(self, corner, load):
        """Power of Bitcell array and bitline in nW."""

        # Dynamic Power from Bitline
        bl_wire = self.gen_bl_wire()
        cell_load = 2 * bl_wire.return_input_cap()
        bl_swing = OPTS.rbl_delay_percentage
        freq = spice["default_event_frequency"]
        bitline_dynamic = self.calc_dynamic_power(corner, cell_load, freq, swing=bl_swing)

        # Calculate the bitcell power which currently only includes leakage
        cell_power = self.cell.analytical_power(corner, load)

        # Leakage power grows with entire array and bitlines.
        total_power = self.return_power(cell_power.dynamic + bitline_dynamic * self.column_size,
                                        cell_power.leakage * self.column_size * self.row_size)
        return total_power

    def gen_wl_wire(self):
        if OPTS.netlist_only:
            width = 0
        else:
            width = self.width
        wl_wire = self.generate_rc_net(int(self.column_size), width, drc("minwidth_m1"))
        # 2 access tx gate per cell
        wl_wire.wire_c = 2 * spice["min_tx_gate_c"] + wl_wire.wire_c
        return wl_wire

    def gen_bl_wire(self):
        if OPTS.netlist_only:
            height = 0
        else:
            height = self.height
        bl_pos = 0
        bl_wire = self.generate_rc_net(int(self.row_size - bl_pos), height, drc("minwidth_m1"))
        # 1 access tx d/s per cell
        bl_wire.wire_c =spice["min_tx_drain_c"] + bl_wire.wire_c
        return bl_wire

    def graph_exclude_bits(self, targ_row=None, targ_col=None):
        """
        Excludes bits in column from being added to graph except target
        """
        # Function is not robust with column mux configurations
        for row in range(self.row_size):
            for col in range(self.column_size):
                if row == targ_row and col == targ_col:
                    continue
                self.graph_inst_exclude.add(self.cell_inst[row, col])

    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        return inst_name + "{}x".format(OPTS.hier_seperator) + self.cell_inst[row, col].name, self.cell_inst[row, col]
