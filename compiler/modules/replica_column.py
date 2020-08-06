# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
import debug
import design
from tech import cell_properties
from sram_factory import factory
from vector import vector
from globals import OPTS


class replica_column(design.design):
    """
    Generate a replica bitline column for the replica array.
    Rows is the total number of rows i the main array.
    Left_rbl and right_rbl are the number of left and right replica bitlines.
    Replica bit specifies which replica column this is (to determine where to put the
    replica cell.
    """

    def __init__(self, name, rows, left_rbl, right_rbl, replica_bit,
                 column_offset=0):
        super().__init__(name)

        self.rows = rows
        self.left_rbl = left_rbl
        self.right_rbl = right_rbl
        self.replica_bit = replica_bit
        # left, right, regular rows plus top/bottom dummy cells
        self.total_size = self.left_rbl + rows + self.right_rbl + 2
        self.column_offset = column_offset

        debug.check(replica_bit != 0 and replica_bit != rows,
                    "Replica bit cannot be the dummy row.")
        debug.check(replica_bit <= left_rbl or replica_bit >= self.total_size - right_rbl - 1,
                    "Replica bit cannot be in the regular array.")
        if OPTS.tech_name == "sky130":
            debug.check(rows % 2 == 0 and (left_rbl + 1) % 2 == 0,
                        "sky130 currently requires rows to be even and to start with X mirroring"
                        + " (left_rbl must be odd) for LVS.")

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.height = self.total_size * self.cell.height
        self.width = self.cell.width

        self.place_instances()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):

        for bl_name in self.cell.get_all_bitline_names():
            # In the replica column, these are only outputs!
            self.add_pin("{0}_{1}".format(bl_name, 0), "OUTPUT")

        for row in range(self.total_size):
            for wl_name in self.cell.get_all_wl_names():
                self.add_pin("{0}_{1}".format(wl_name, row), "INPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        self.replica_cell = factory.create(module_type="replica_{}".format(OPTS.bitcell))
        self.add_mod(self.replica_cell)
        self.dummy_cell = factory.create(module_type="dummy_{}".format(OPTS.bitcell))
        self.add_mod(self.dummy_cell)
        try:
            edge_module_type = ("col_cap" if cell_properties.bitcell.end_caps else "dummy")
        except AttributeError:
            edge_module_type = "dummy"
        self.edge_cell = factory.create(module_type=edge_module_type + "_" + OPTS.bitcell)
        self.add_mod(self.edge_cell)
        # Used for pin names only
        self.cell = factory.create(module_type="bitcell")

    def create_instances(self):

        try:
            end_caps_enabled = cell_properties.bitcell.end_caps
        except AttributeError:
            end_caps_enabled = False

        self.cell_inst = {}
        for row in range(self.total_size):
            name="rbc_{0}".format(row)
            # Top/bottom cell are always dummy cells.
            # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
            # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.
            if (row > self.left_rbl and row < self.total_size - self.right_rbl - 1):
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.replica_cell)
                self.connect_inst(self.get_bitcell_pins(0, row))
            elif row==self.replica_bit:
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.replica_cell)
                self.connect_inst(self.get_bitcell_pins(0, row))
            elif (row == 0 or row == self.total_size - 1):
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.edge_cell)
                if end_caps_enabled:
                    self.connect_inst(self.get_bitcell_pins_col_cap(0, row))
                else:
                    self.connect_inst(self.get_bitcell_pins(0, row))
            else:
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(0, row))

    def place_instances(self):
        from tech import cell_properties
        # Flip the mirrors if we have an odd number of replica+dummy rows at the bottom
        # so that we will start with mirroring rather than not mirroring
        rbl_offset = (self.left_rbl + 1) %2

        # if our bitcells are mirrored on the y axis, check if we are in global
        # column that needs to be flipped.
        dir_y = False
        xoffset = 0
        if cell_properties.bitcell.mirror.y and self.column_offset % 2:
            dir_y = True
            xoffset = self.replica_cell.width

        for row in range(self.total_size):
            # name = "bit_r{0}_{1}".format(row, "rbl")
            dir_x = cell_properties.bitcell.mirror.x and (row + rbl_offset) % 2

            offset = vector(xoffset, self.cell.height * (row + (row + rbl_offset) % 2))

            if dir_x and dir_y:
                dir_key = "XY"
            elif dir_x:
                dir_key = "MX"
            elif dir_y:
                dir_key = "MY"
            else:
                dir_key = ""

            self.cell_inst[row].place(offset=offset,
                                      mirror=dir_key)

    def add_layout_pins(self):
        """ Add the layout pins """

        for bl_name in self.cell.get_all_bitline_names():
            bl_pin = self.cell_inst[0].get_pin(bl_name)
            self.add_layout_pin(text=bl_name,
                                layer=bl_pin.layer,
                                offset=bl_pin.ll().scale(1, 0),
                                width=bl_pin.width(),
                                height=self.height)

        try:
            end_caps_enabled = cell_properties.bitcell.end_caps
        except AttributeError:
            end_caps_enabled = False

        if end_caps_enabled:
            row_range_max = self.total_size - 1
            row_range_min = 1
        else:
            row_range_max = self.total_size
            row_range_min = 0

        for row in range(row_range_min, row_range_max):
            for wl_name in self.cell.get_all_wl_names():
                wl_pin = self.cell_inst[row].get_pin(wl_name)
                self.add_layout_pin(text="{0}_{1}".format(wl_name, row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        # Supplies are only connected in the ends
        for (index, inst) in self.cell_inst.items():
            for pin_name in ["vdd", "gnd"]:
                if inst in [self.cell_inst[0], self.cell_inst[self.total_size - 1]]:
                    self.copy_power_pins(inst, pin_name)
                else:
                    self.copy_layout_pin(inst, pin_name)

    def get_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """

        bitcell_pins = []

        pin_names = self.cell.get_all_bitline_names()
        for pin in pin_names:
            bitcell_pins.append(pin + "_{0}".format(col))
        pin_names = self.cell.get_all_wl_names()
        for pin in pin_names:
            bitcell_pins.append(pin + "_{0}".format(row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def get_bitcell_pins_col_cap(self, col, row):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """

        bitcell_pins = []

        pin_names = self.cell.get_all_bitline_names()
        for pin in pin_names:
            bitcell_pins.append(pin + "_{0}".format(col))
        bitcell_pins.append("vdd")

        return bitcell_pins

    def exclude_all_but_replica(self):
        """Excludes all bits except the replica cell (self.replica_bit)."""

        for row, cell in self.cell_inst.items():
            if row != self.replica_bit:
                self.graph_inst_exclude.add(cell)
