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
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_capped_replica_bitcell_array(sky130_bitcell_base_array):
    """
    Creates a replica bitcell array then adds the row and column caps to all
    sides of a bitcell array.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(name, rows, cols, column_offset=0)
        debug.info(1, "Creating {0} {1} x {2} rbls: {3} left_rbl: {4} right_rbl: {5}".format(self.name,
                                                                                             rows,
                                                                                             cols,
                                                                                             rbl,
                                                                                             left_rbl,
                                                                                             right_rbl))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))
        self.add_comment("rbl: {0} left_rbl: {1} right_rbl: {2}".format(rbl, left_rbl, right_rbl))

        # This is how many RBLs are in all the arrays
        self.rbl = rbl
        # This specifies which RBL to put on the left or right by port number
        # This could be an empty list
        if left_rbl is not None:
            self.left_rbl = left_rbl
        else:
            self.left_rbl = []
        # This could be an empty list
        if right_rbl is not None:
            self.right_rbl = right_rbl
        else:
            self.right_rbl = []

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def add_modules(self):
        self.replica_bitcell_array = factory.create(module_type="replica_bitcell_array",
                                                    cols=self.column_size,
                                                    rows=self.row_size,
                                                    rbl=self.rbl,
                                                    left_rbl=self.left_rbl,
                                                    right_rbl=self.right_rbl)

    def add_pins(self):

        # Arrays are always:
        # bitlines (column first then port order)
        # word lines (row first then port order)
        # dummy wordlines
        # replica wordlines
        # regular wordlines (bottom to top)
        # # dummy bitlines
        # replica bitlines (port order)
        # regular bitlines (left to right port order)
        #
        # vdd
        # gnd

        self.add_bitline_pins()
        self.add_wordline_pins()
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_bitline_pins(self):
        self.bitline_names = self.replica_bitcell_array.bitline_names
        self.all_bitline_names = self.replica_bitcell_array.all_bitline_names
        self.rbl_bitline_names = self.replica_bitcell_array.rbl_bitline_names
        self.all_rbl_bitline_names = self.replica_bitcell_array.all_rbl_bitline_names

        self.bitline_pins = []

        for port in self.left_rbl:
            self.bitline_pins.extend(self.rbl_bitline_names[port])
        self.bitline_pins.extend(self.all_bitline_names)
        for port in self.right_rbl:
            self.bitline_pins.extend(self.rbl_bitline_names[port])

        self.add_pin_list(self.bitline_pins, "INOUT")

    def add_wordline_pins(self):
        # some of these are just included for compatibility with modules instantiating this module
        self.rbl_wordline_names = self.replica_bitcell_array.rbl_wordline_names
        self.all_rbl_wordline_names = self.replica_bitcell_array.all_rbl_wordline_names
        self.wordline_names = self.replica_bitcell_array.wordline_names
        self.all_wordline_names = self.replica_bitcell_array.all_wordline_names

        self.wordline_pins = []

        for port in range(self.rbl[0]):
            self.wordline_pins.append(self.rbl_wordline_names[port][port])
        self.wordline_pins.extend(self.all_wordline_names)
        for port in range(self.rbl[0], self.rbl[0] + self.rbl[1]):
            self.wordline_pins.append(self.rbl_wordline_names[port][port])

        self.add_pin_list(self.wordline_pins, "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.supplies = ["vdd", "gnd"]

        # Main array
        self.replica_bitcell_array_inst=self.add_inst(name="replica_bitcell_array",
                                                      mod=self.replica_bitcell_array)
        self.connect_inst(self.bitline_pins + self.wordline_pins + self.supplies)

    def create_layout(self):

        self.replica_bitcell_array_inst.place(offset=0)

        self.width = self.replica_bitcell_array.width
        self.height = self.replica_bitcell_array.height

        for pin_name in self.bitline_pins + self.wordline_pins + self.supplies:
            self.copy_layout_pin(self.replica_bitcell_array_inst, pin_name)

        self.add_boundary()

        self.DRC_LVS()

    def get_main_array_top(self):
        return self.replica_bitcell_array.get_main_array_top()

    def get_main_array_bottom(self):
        return self.replica_bitcell_array.get_main_array_bottom()

    def get_main_array_left(self):
        return self.replica_bitcell_array.get_main_array_left()

    def get_main_array_right(self):
        return self.replica_bitcell_array.get_main_array_right()

    def get_replica_top(self):
        return self.replica_bitcell_array.get_replica_top()

    def get_replica_bottom(self):
        return self.replica_bitcell_array.get_replica_bottom()

    def get_replica_left(self):
        return self.replica_bitcell_array.get_replica_left()

    def get_replica_right(self):
        return self.replica_bitcell_array.get_replica_right()


    def get_column_offsets(self):
        return self.replica_bitcell_array.get_column_offsets()

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


    def gen_bl_wire(self):
        if OPTS.netlist_only:
            height = 0
        else:
            height = self.height
        bl_pos = 0
        bl_wire = self.generate_rc_net(int(self.row_size - bl_pos), height, drc("minwidth_m1"))
        bl_wire.wire_c =spice["min_tx_drain_c"] + bl_wire.wire_c # 1 access tx d/s per cell
        return bl_wire

    def graph_exclude_bits(self, targ_row=None, targ_col=None):
        """
        Excludes bits in column from being added to graph except target
        """
        self.replica_bitcell_array.graph_exclude_bits(targ_row, targ_col)

    def graph_exclude_replica_col_bits(self):
        """
        Exclude all replica/dummy cells in the replica columns except the replica bit.
        """
        self.replica_bitcell_array.graph_exclude_replica_col_bits()

    def get_cell_name(self, inst_name, row, col):
        """
        Gets the spice name of the target bitcell.
        """
        return self.replica_bitcell_array.get_cell_name(inst_name + "{}x".format(OPTS.hier_seperator) + self.replica_bitcell_array_inst.name, row, col)

    def clear_exclude_bits(self):
        """
        Clears the bit exclusions
        """
        self.replica_bitcell_array.clear_exclude_bits()
