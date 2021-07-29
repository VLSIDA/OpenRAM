# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# All rights reserved.
#
import debug
from bitcell_base_array import bitcell_base_array
from sram_factory import factory
from vector import vector
from globals import OPTS
from tech import layer_properties as layer_props


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
        self.row_start = rbl[0] + 1
        # End of regular word line rows
        self.row_end = self.row_start + rows
        if not self.cell.end_caps:
            self.row_size += 2
        super().__init__(rows=self.row_size, cols=1, column_offset=column_offset, name=name)

        self.rows = rows
        self.left_rbl = rbl[0]
        self.right_rbl = rbl[1]
        self.replica_bit = replica_bit
        
        # Total size includes the replica rows and column cap rows
        self.total_size = self.left_rbl + rows + self.right_rbl + 2

        self.column_offset = column_offset

        debug.check(replica_bit != 0 and replica_bit != self.total_size - 1,
                    "Replica bit cannot be the dummy/cap row.")
        debug.check(replica_bit < self.row_start or replica_bit >= self.row_end,
                    "Replica bit cannot be in the regular array.")
        if layer_props.replica_column.even_rows:
            debug.check(rows % 2 == 0 and (self.left_rbl + 1) % 2 == 0,
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
        self.place_instances()
        
        self.height = self.cell_inst[-1].uy()
        self.width = self.cell_inst[0].rx()

        self.add_layout_pins()

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
        self.add_mod(self.replica_cell)
        self.dummy_cell = factory.create(module_type=OPTS.dummy_bitcell)
        self.add_mod(self.dummy_cell)
        try:
            edge_module_type = ("col_cap" if self.cell.end_caps else "dummy")
        except AttributeError:
            edge_module_type = "dummy"
        self.edge_cell = factory.create(module_type=edge_module_type + "_" + OPTS.bitcell)
        self.add_mod(self.edge_cell)

    def create_instances(self):
        self.cell_inst = []

        for row in range(self.total_size):
            name="rbc_{0}".format(row)
            real_row = row
            if self.cell.end_caps:
                real_row -= 1
                
            # Regular array cells are replica cells
            # Replic bit specifies which other bit (in the full range (0,total_size) to make a replica cell.
            if (row == 0 or row == self.total_size - 1):
                self.cell_inst.append(self.add_inst(name=name,
                                                    mod=self.edge_cell))
                if self.cell.end_caps:
                    self.connect_inst(self.get_bitcell_pins_col_cap(real_row, 0))
                else:
                    self.connect_inst(self.get_bitcell_pins(real_row, 0))
            elif (row==self.replica_bit) or (row >= self.row_start and row < self.row_end):
                self.cell_inst.append(self.add_inst(name=name,
                                                    mod=self.replica_cell))
                self.connect_inst(self.get_bitcell_pins(real_row, 0))
            else:
                # Top/bottom cell are always dummy/cap cells.
                self.cell_inst.append(self.add_inst(name=name,
                                                    mod=self.dummy_cell))
                self.connect_inst(self.get_bitcell_pins(real_row, 0))

    def place_instances(self):
        # Flip the mirrors if we have an odd number of replica+dummy rows at the bottom
        # so that we will start with mirroring rather than not mirroring
        rbl_offset = (self.left_rbl + 1) %2

        # if our bitcells are mirrored on the y axis, check if we are in global
        # column that needs to be flipped.
        dir_y = False
        xoffset = 0
        if self.cell.mirror.y and self.column_offset % 2:
            dir_y = True
            xoffset = self.replica_cell.width

        for row in range(self.total_size):
            # name = "bit_r{0}_{1}".format(row, "rbl")
            dir_x = self.cell.mirror.x and (row + rbl_offset) % 2

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
        for port in self.all_ports:
            bl_pin = self.cell_inst[0].get_pin(self.cell.get_bl_name(port))
            self.add_layout_pin(text="bl_{0}_{1}".format(port, 0),
                                layer=bl_pin.layer,
                                offset=bl_pin.ll().scale(1, 0),
                                width=bl_pin.width(),
                                height=self.height)
            bl_pin = self.cell_inst[0].get_pin(self.cell.get_br_name(port))
            self.add_layout_pin(text="br_{0}_{1}".format(port, 0),
                                layer=bl_pin.layer,
                                offset=bl_pin.ll().scale(1, 0),
                                width=bl_pin.width(),
                                height=self.height)

        if self.cell.end_caps:
            row_range_max = self.total_size - 1
            row_range_min = 1
        else:
            row_range_max = self.total_size
            row_range_min = 0

        for port in self.all_ports:
            for row in range(row_range_min, row_range_max):
                wl_pin = self.cell_inst[row].get_pin(self.cell.get_wl_name(port))
                self.add_layout_pin(text="wl_{0}_{1}".format(port, row - row_range_min),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        # Supplies are only connected in the ends
        for (index, inst) in enumerate(self.cell_inst):
            for pin_name in ["vdd", "gnd"]:
                if inst in [self.cell_inst[0], self.cell_inst[self.total_size - 1]]:
                    for pin in inst.get_pins(pin_name):
                        self.copy_power_pin(pin)
                else:
                    self.copy_layout_pin(inst, pin_name)

    def get_bitline_names(self, port=None):
        if port == None:
            return self.all_bitline_names
        else:
            return self.bitline_names[port]

    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

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
                self.graph_inst_exclude.add(cell)
        
