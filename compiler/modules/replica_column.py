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
    rbl is a tuple with the number of left and right replica bitlines.
    Replica bit specifies which replica column this is (to determine where to put the
    replica cell relative to the bottom (including the dummy bit at 0).
    """

    def __init__(self, name, rows, rbl, replica_bit, column_offset=0):
        super().__init__(name)

        self.rows = rows
        self.left_rbl = rbl[0]
        self.right_rbl = rbl[1]
        self.replica_bit = replica_bit
        # left, right, regular rows plus top/bottom dummy cells
        self.total_size = self.left_rbl + rows + self.right_rbl + 2
        self.column_offset = column_offset

        debug.check(replica_bit != 0 and replica_bit != rows,
                    "Replica bit cannot be the dummy row.")
        debug.check(replica_bit <= self.left_rbl or replica_bit >= self.total_size - self.right_rbl - 1,
                    "Replica bit cannot be in the regular array.")
        if OPTS.tech_name == "sky130":
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
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):

        self.bitline_names = [[] for port in self.all_ports]
        col = 0
        for port in self.all_ports:
            self.bitline_names[port].append("bl_{0}_{1}".format(port, col))
            self.bitline_names[port].append("br_{0}_{1}".format(port, col))
        self.all_bitline_names = [x for sl in self.bitline_names for x in sl]
        self.add_pin_list(self.all_bitline_names, "OUTPUT")

        self.wordline_names = [[] for port in self.all_ports]
        for row in range(self.total_size):
            for port in self.all_ports:
                if not cell_properties.compare_ports(cell_properties.bitcell.split_wl):
                    self.wordline_names[port].append("wl_{0}_{1}".format(port, row))
                else:
                    self.wordline_names[port].append("wl0_{0}_{1}".format(port, row))
                    self.wordline_names[port].append("wl1_{0}_{1}".format(port, row))
        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]
        self.add_pin_list(self.all_wordline_names, "INPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
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
        else:
            self.replica_cell = factory.create(module_type="s8_bitcell", version = "opt1")
            self.add_mod(self.replica_cell)
            self.cell = self.replica_cell
            self.replica_cell2 = factory.create(module_type="s8_bitcell", version = "opt1a")
            self.add_mod(self.replica_cell2)

            self.dummy_cell = factory.create(module_type="s8_bitcell", version = "opt1")
            self.dummy_cell2 = factory.create(module_type="s8_bitcell", version = "opt1")

            self.strap1 = factory.create(module_type="s8_internal", version = "wlstrap")
            self.add_mod(self.strap1)
            self.strap2 = factory.create(module_type="s8_internal", version = "wlstrap_p")
            self.add_mod(self.strap2)

            self.colend = factory.create(module_type="s8_col_end", version = "colenda")
            self.edge_cell = self.colend
            self.add_mod(self.colend)
            self.colenda = factory.create(module_type="s8_col_end", version = "colenda")
            self.add_mod(self.colenda)
            self.colend_p_cent = factory.create(module_type="s8_col_end", version = "colend_p_cent")
            self.add_mod(self.colend_p_cent)
            self.colenda_p_cent = factory.create(module_type="s8_col_end", version = "colenda_p_cent")
            self.add_mod(self.colenda_p_cent)

            self.corner_ul = factory.create(module_type="s8_corner", location = "ul")
            self.add_mod(self.corner_ul)
            self.corner_ur =factory.create(module_type="s8_corner", location = "ur")
            self.add_mod(self.corner_ur)
            self.corner_ll = factory.create(module_type="s8_corner", location = "ll")
            self.add_mod(self.corner_ll)
            self.corner_lr = factory.create(module_type="s8_corner", location = "lr")
            self.add_mod(self.corner_lr)


    def create_instances(self):
        self.cell_inst = {}
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            try:
                end_caps_enabled = cell_properties.bitcell.end_caps
            except AttributeError:
                end_caps_enabled = False
            
            for row in range(self.total_size):
                name="rbc_{0}".format(row)
                # Top/bottom cell are always dummy cells.
                # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
                # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.
                if (row > self.left_rbl and row < self.total_size - self.right_rbl - 1):
                    self.cell_inst[row]=self.add_inst(name=name,
                                                    mod=self.replica_cell)
                    self.connect_inst(self.get_bitcell_pins(row, 0))
                elif row==self.replica_bit:
                    self.cell_inst[row]=self.add_inst(name=name,
                                                    mod=self.replica_cell)
                    self.connect_inst(self.get_bitcell_pins(row, 0))
                elif (row == 0 or row == self.total_size - 1):
                    self.cell_inst[row]=self.add_inst(name=name,
                                                    mod=self.edge_cell)
                    if end_caps_enabled:
                        self.connect_inst(self.get_bitcell_pins_col_cap(row, 0))
                    else:
                        self.connect_inst(self.get_bitcell_pins(row, 0))
                else:
                    self.cell_inst[row]=self.add_inst(name=name,
                                                    mod=self.dummy_cell)
                    self.connect_inst(self.get_bitcell_pins(row, 0))
        else:
            from tech import custom_replica_column_arrangement
            custom_replica_column_arrangement(self)

    def place_instances(self):
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):

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
        else:
            from tech import custom_replica_cell_placement
            custom_replica_cell_placement(self)

    def add_layout_pins(self):
        """ Add the layout pins """
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
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

            for port in self.all_ports:
                for row in range(row_range_min, row_range_max):
                    wl_pin = self.cell_inst[row].get_pin(self.cell.get_wl_name(port))
                    self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
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
        else:
            for port in self.all_ports:
                bl_pin = self.cell_inst[2].get_pin(self.cell.get_bl_name(port))
                self.add_layout_pin(text="bl_{0}_{1}".format(port, 0),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)
                bl_pin = self.cell_inst[2].get_pin(self.cell.get_br_name(port))
                self.add_layout_pin(text="br_{0}_{1}".format(port, 0),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)


            row_range_max = self.total_size - 1
            row_range_min = 1

            for port in self.all_ports:
                for row in range(row_range_min, row_range_max):
                    wl_pin = self.cell_inst[row].get_pin(self.cell.get_wl_name(port))
                    self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
                                        layer=wl_pin.layer,
                                        offset=wl_pin.ll().scale(0, 1),
                                        width=self.width,
                                        height=wl_pin.height())

            # # Supplies are only connected in the ends
            # for (index, inst) in self.cell_inst.items():
            #     for pin_name in ["vdd", "gnd"]:
            #         if inst in [self.cell_inst[0], self.cell_inst[self.total_size - 1]]:
            #             self.copy_power_pins(inst, pin_name)
            #         else:
            #             self.copy_layout_pin(inst, pin_name)

    def get_bitline_names(self, port=None):
        if port == None:
            return self.all_bitline_names
        else:
            return self.bitline_names[port]

    def get_bitcell_pins(self, row, col):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def get_bitcell_pins_col_cap(self, row, col):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def exclude_all_but_replica(self):
        """Excludes all bits except the replica cell (self.replica_bit)."""

        for row, cell in self.cell_inst.items():
            if row != self.replica_bit:
                self.graph_inst_exclude.add(cell)
