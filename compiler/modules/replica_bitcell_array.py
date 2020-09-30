# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#

import debug
import bitcell_base_array
from tech import drc, spice, cell_properties
from vector import vector
from globals import OPTS
from sram_factory import factory


class replica_bitcell_array(bitcell_base_array.bitcell_base_array):
    """
    Creates a bitcell arrow of cols x rows and then adds the replica
    and dummy columns and rows.  Replica columns are on the left and
    right, respectively and connected to the given bitcell ports.
    Dummy are the outside columns/rows with WL and BL tied to gnd.
    Requires a regular bitcell array, replica bitcell, and dummy
    bitcell (Bl/BR disconnected).
    """
    def __init__(self, rows, cols, rbl, name, add_rbl=None):
        super().__init__(name, rows, cols, column_offset=0)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows
        # This is how many RBLs are in all the arrays
        self.rbl = rbl
        self.left_rbl = rbl[0]
        self.right_rbl = rbl[1]
        # This is how many RBLs are added to THIS array
        if add_rbl == None:
            self.add_left_rbl = rbl[0]
            self.add_right_rbl = rbl[1]
        else:
            self.add_left_rbl = add_rbl[0]
            self.add_right_rbl = add_rbl[1]
            for a, b in zip(add_rbl, rbl):
                debug.check(a <= b,
                            "Invalid number of RBLs for port configuration.")

        debug.check(sum(rbl) <= len(self.all_ports),
                    "Invalid number of RBLs for port configuration.")

        # Two dummy rows plus replica even if we don't add the column
        self.extra_rows = 2 + sum(rbl)
        # Two dummy cols plus replica if we add the column
        self.extra_cols = 2 + self.add_left_rbl + self.add_right_rbl
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

    def add_modules(self):
        """  Array and dummy/replica columns

        d or D = dummy cell (caps to distinguish grouping)
        r or R = replica cell (caps to distinguish grouping)
        b or B = bitcell
         replica columns 1
         v              v
        bdDDDDDDDDDDDDDDdb <- Dummy row
        bdDDDDDDDDDDDDDDrb <- Dummy row
        br--------------rb
        br|   Array    |rb
        br| row x col  |rb
        br--------------rb
        brDDDDDDDDDDDDDDdb <- Dummy row
        bdDDDDDDDDDDDDDDdb <- Dummy row

          ^^^^^^^^^^^^^^^
          dummy rows cols x 1

        ^ dummy columns  ^
          1 x (rows + 4)
        """
        # Bitcell array
        self.bitcell_array = factory.create(module_type="bitcell_array",
                                            column_offset=1 + self.add_left_rbl,
                                            cols=self.column_size,
                                            rows=self.row_size)
        self.add_mod(self.bitcell_array)

        # Replica bitlines
        self.replica_columns = {}
        for bit in range(self.add_left_rbl + self.add_right_rbl):
            # Creating left_rbl
            if bit < self.add_left_rbl:
                # These go from the top (where the bitcell array starts ) down
                replica_bit = self.left_rbl - bit
            # Creating right_rbl
            else:
                # These go from the bottom up
                replica_bit = self.left_rbl + self.row_size + 1 + bit
            # If we have an odd numer on the bottom
            column_offset = self.left_rbl + 1

            self.replica_columns[bit] = factory.create(module_type="replica_column",
                                                       rows=self.row_size,
                                                       rbl=self.rbl,
                                                       column_offset=column_offset,
                                                       replica_bit=replica_bit)
            self.add_mod(self.replica_columns[bit])
                # If there are bitcell end caps, replace the dummy cells on the edge of the bitcell array with end caps.
        try:
            end_caps_enabled = cell_properties.bitcell.end_caps
        except AttributeError:
            end_caps_enabled = False
            # Dummy row
        self.dummy_row = factory.create(module_type="dummy_array",
                                            cols=self.column_size,
                                            rows=1,
                                            # dummy column + left replica column
                                            column_offset=1 + self.add_left_rbl,
                                            mirror=0)
        self.add_mod(self.dummy_row)
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):

            # Dummy Row or Col Cap, depending on bitcell array properties
            col_cap_module_type = ("col_cap_array" if end_caps_enabled else "dummy_array")
            self.col_cap = factory.create(module_type=col_cap_module_type,
                                        cols=self.column_size,
                                        rows=1,
                                        # dummy column + left replica column(s)
                                        column_offset=1 + self.add_left_rbl,
                                        mirror=0)
            self.add_mod(self.col_cap)

            # Dummy Col or Row Cap, depending on bitcell array properties
            row_cap_module_type = ("row_cap_array" if end_caps_enabled else "dummy_array")

            self.row_cap_left = factory.create(module_type=row_cap_module_type,
                                                cols=1,
                                                column_offset=0,
                                                rows=self.row_size + self.extra_rows,
                                                mirror=(self.left_rbl + 1) % 2)
            self.add_mod(self.row_cap_left)

            self.row_cap_right = factory.create(module_type=row_cap_module_type,
                                                cols=1,
                                                #   dummy column
                                                # + left replica column(s)
                                                # + bitcell columns
                                                # + right replica column(s)
                                                column_offset = 1 + self.add_left_rbl + self.column_size + self.add_right_rbl,
                                                rows=self.row_size + self.extra_rows,
                                                mirror=(self.left_rbl + 1) %2)
            self.add_mod(self.row_cap_right)
        else:
            # Dummy Row or Col Cap, depending on bitcell array properties
            col_cap_module_type = ("s8_col_cap_array" if end_caps_enabled else "dummy_array")
            self.col_cap_top = factory.create(module_type=col_cap_module_type,
                                        cols=self.column_size,
                                        rows=1,
                                        # dummy column + left replica column(s)
                                        column_offset=1 + self.add_left_rbl,
                                        mirror=0,
                                        location="top")
            self.add_mod(self.col_cap_top)

            self.col_cap_bottom = factory.create(module_type=col_cap_module_type,
                                        cols=self.column_size,
                                        rows=1,
                                        # dummy column + left replica column(s)
                                        column_offset=1 + self.add_left_rbl,
                                        mirror=0,
                                        location="bottom")
            self.add_mod(self.col_cap_bottom)
            # Dummy Col or Row Cap, depending on bitcell array properties
            row_cap_module_type = ("s8_row_cap_array" if end_caps_enabled else "dummy_array")

            self.row_cap_left = factory.create(module_type=row_cap_module_type,
                                                cols=1,
                                                column_offset=0,
                                                rows=self.row_size + self.extra_rows,
                                                mirror=0)
            self.add_mod(self.row_cap_left)

            self.row_cap_right = factory.create(module_type=row_cap_module_type,
                                                cols=1,
                                                #   dummy column
                                                # + left replica column(s)
                                                # + bitcell columns
                                                # + right replica column(s)
                                                column_offset = 1 + self.add_left_rbl + self.column_size + self.add_right_rbl,
                                                rows=self.row_size + self.extra_rows,
                                                mirror=0)
            self.add_mod(self.row_cap_right)

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
        # Regular bitline names by port
        self.bitline_names = []
        # Replica bitlines by port
        self.rbl_bitline_names = []
        # Dummy bitlines by left/right
        self.dummy_col_bitline_names = []
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):

            for loc in ["left", "right"]:
                self.dummy_col_bitline_names.append([])
                for port in self.all_ports:
                    bitline_names = ["dummy_{0}_{1}".format(x, loc) for x in self.row_cap_left.get_bitline_names(port)]
                    self.dummy_col_bitline_names[-1].extend(bitline_names)
            self.all_dummy_col_bitline_names = [x for sl in self.dummy_col_bitline_names for x in sl]
        for port in range(self.add_left_rbl + self.add_right_rbl):
            left_names=["rbl_bl_{0}_{1}".format(x, port) for x in self.all_ports]
            right_names=["rbl_br_{0}_{1}".format(x, port) for x in self.all_ports]
            bitline_names = [x for t in zip(left_names, right_names) for x in t]
            self.rbl_bitline_names.append(bitline_names)
        # Make a flat list too
        self.all_rbl_bitline_names = [x for sl in self.rbl_bitline_names for x in sl]

        for port in self.all_ports:
            bitline_names = self.bitcell_array.get_bitline_names(port)
            self.bitline_names.append(bitline_names)
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.add_pin_list(self.dummy_col_bitline_names[0], "INOUT")
            for port in range(self.add_left_rbl):
                self.add_pin_list(self.rbl_bitline_names[port], "INOUT")
            self.add_pin_list(self.all_bitline_names, "INOUT")
            for port in range(self.add_left_rbl, self.add_left_rbl + self.add_right_rbl):
                self.add_pin_list(self.rbl_bitline_names[port], "INOUT")
            self.add_pin_list(self.dummy_col_bitline_names[1], "INOUT")
        
    def add_wordline_pins(self):

        # Regular wordlines by port
        self.wordline_names = []
        # Replica wordlines by port
        self.rbl_wordline_names = []
        # Dummy wordlines by bot/top
        self.dummy_row_wordline_names = []
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            dummy_row_wordline_names = ["dummy_" + x for x in self.col_cap.get_wordline_names()]
            for loc in ["bot", "top"]:
                wordline_names = ["{0}_{1}".format(wl_name, loc) for wl_name in dummy_row_wordline_names]
                self.dummy_row_wordline_names.append(wordline_names)
            self.all_dummy_row_wordline_names = [x for sl in self.dummy_row_wordline_names for x in sl]

        for port in range(self.left_rbl + self.right_rbl):
                if not cell_properties.compare_ports(cell_properties.bitcell.split_wl):
                    wordline_names=["rbl_wl_{0}_{1}".format(x, port) for x in self.all_ports]
                    self.rbl_wordline_names.append(wordline_names)
                else:
                    for x in self.all_ports:
                        wordline_names = []
                        wordline_names.append("rbl_wl0_{0}_{1}".format(x, port))
                        wordline_names.append("rbl_wl1_{0}_{1}".format(x, port))
                        self.rbl_wordline_names.append(wordline_names)
        self.all_rbl_wordline_names = [x for sl in self.rbl_wordline_names for x in sl]

        for port in self.all_ports:
            wordline_names = self.bitcell_array.get_wordline_names(port)
            self.wordline_names.append(wordline_names)
        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]

        # All wordlines including dummy and RBL
        self.replica_array_wordline_names = []
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.replica_array_wordline_names.extend(self.dummy_row_wordline_names[0])
        for p in range(self.left_rbl):
            self.replica_array_wordline_names.extend(self.rbl_wordline_names[p])
        self.replica_array_wordline_names.extend(self.all_wordline_names)
        for p in range(self.left_rbl, self.left_rbl + self.right_rbl):
            self.replica_array_wordline_names.extend(self.rbl_wordline_names[p])
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.replica_array_wordline_names.extend(self.dummy_row_wordline_names[1])
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.add_pin_list(self.dummy_row_wordline_names[0], "INPUT")
        for port in range(self.left_rbl):
            self.add_pin_list(self.rbl_wordline_names[port], "INPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")
        for port in range(self.left_rbl, self.left_rbl + self.right_rbl):
            self.add_pin_list(self.rbl_wordline_names[port], "INPUT")
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.add_pin_list(self.dummy_row_wordline_names[1], "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """
        
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.supplies = ["vdd", "gnd"]
        else:
            self.supplies = ["vpwr", "vgnd"]

        # Used for names/dimensions only
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.cell = factory.create(module_type="bitcell")
        else:
            self.cell = factory.create(module_type="s8_bitcell", version = "opt1")

        # Main array
        self.bitcell_array_inst=self.add_inst(name="bitcell_array",
                                              mod=self.bitcell_array)
        self.connect_inst(self.all_bitline_names + self.all_wordline_names +  self.supplies)

        # Replica columns
        self.replica_col_insts = []
        for port in range(self.add_left_rbl + self.add_right_rbl):
            self.replica_col_insts.append(self.add_inst(name="replica_col_{}".format(port),
                                                       mod=self.replica_columns[port]))
            self.connect_inst(self.rbl_bitline_names[port] + self.replica_array_wordline_names +  self.supplies)
        # Dummy rows under the bitcell array (connected with with the replica cell wl)
        self.dummy_row_replica_insts = []
        # Note, this is the number of left and right even if we aren't adding the columns to this bitcell array!
        for port in range(self.left_rbl + self.right_rbl):
            self.dummy_row_replica_insts.append(self.add_inst(name="dummy_row_{}".format(port),
                                                            mod=self.dummy_row))
            self.connect_inst(self.all_bitline_names + self.rbl_wordline_names[port] +  self.supplies)


        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            # Top/bottom dummy rows or col caps
            self.dummy_row_insts = []
            self.dummy_row_insts.append(self.add_inst(name="dummy_row_bot",
                                                    mod=self.col_cap))
            self.connect_inst(self.all_bitline_names
                            + self.dummy_row_wordline_names[0]
                            +  self.supplies)
            self.dummy_row_insts.append(self.add_inst(name="dummy_row_top",
                                                    mod=self.col_cap))
            self.connect_inst(self.all_bitline_names
                            + self.dummy_row_wordline_names[1]
                            +  self.supplies)
            # Left/right Dummy columns
            self.dummy_col_insts = []
            self.dummy_col_insts.append(self.add_inst(name="dummy_col_left",
                                                    mod=self.row_cap_left))
            self.connect_inst(self.dummy_col_bitline_names[0] + self.replica_array_wordline_names +  self.supplies)
            self.dummy_col_insts.append(self.add_inst(name="dummy_col_right",
                                                    mod=self.row_cap_right))
            self.connect_inst(self.dummy_col_bitline_names[1] + self.replica_array_wordline_names +  self.supplies)
        else:
            # Top/bottom dummy rows or col caps
            self.dummy_row_insts = []
            self.dummy_row_insts.append(self.add_inst(name="col_cap_bottom",
                                                    mod=self.col_cap_bottom))
            self.connect_inst(self.all_bitline_names
                            +  self.supplies)
            self.dummy_row_insts.append(self.add_inst(name="col_cap_top",
                                                    mod=self.col_cap_top))
            self.connect_inst(self.all_bitline_names
                            +  self.supplies)
            # Left/right Dummy columns
            self.dummy_col_insts = []
            self.dummy_col_insts.append(self.add_inst(name="row_cap_left",
                                                    mod=self.row_cap_left))
            self.connect_inst(self.replica_array_wordline_names +  self.supplies)
            self.dummy_col_insts.append(self.add_inst(name="row_cap_right",
                                                    mod=self.row_cap_right))
            self.connect_inst(self.replica_array_wordline_names +  self.supplies)

    def create_layout(self):
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.height = (self.row_size + self.extra_rows) * self.dummy_row.height
            self.width = (self.column_size + self.extra_cols) * self.cell.width
        else:
            self.width = self.row_cap_left.top_corner.width + self.row_cap_right.top_corner.width + (self.col_cap_top.colend1.width + self.col_cap_top.colend2.width) * (self.column_size + self.extra_cols) -  self.col_cap_top.colend2.width
            self.height = self.row_cap_left.height

        # This is a bitcell x bitcell offset to scale
        self.bitcell_offset = vector(self.cell.width, self.cell.height)
        if not cell_properties.compare_ports(cell_properties.bitcell_array.use_custom_cell_arrangement):
            self.strap_offset = vector(0, 0)
            self.col_end_offset = vector(self.cell.width, self.cell.height)
            self.row_end_offset = vector(self.cell.width, self.cell.height)
        else:
            self.strap_offset = vector(self.replica_col_insts[0].mod.strap1.width, self.replica_col_insts[0].mod.strap1.height)
            self.col_end_offset = vector(self.dummy_row_insts[0].mod.colend1.width, self.dummy_row_insts[0].mod.colend1.height)
            self.row_end_offset = vector(self.dummy_col_insts[0].mod.rowend1.width, self.dummy_col_insts[0].mod.rowend1.height)

        # Everything is computed with the main array at (0, 0) to start
        self.bitcell_array_inst.place(offset=[0, 0])

        self.add_replica_columns()
        
        self.add_end_caps()

        # Array was at (0, 0) but move everything so it is at the lower left
        # We move DOWN the number of left RBL even if we didn't add the column to this bitcell array
        self.translate_all(self.bitcell_offset.scale(-1 - self.add_left_rbl, -1 - self.left_rbl))

        self.add_layout_pins()

        self.add_boundary()

        self.DRC_LVS()

    def add_replica_columns(self):
        """ Add replica columns on left and right of array """
        end_caps_enabled = cell_properties.bitcell.end_caps

        # Grow from left to right, toward the array
        for bit in range(self.add_left_rbl):
            if not end_caps_enabled:
                offset = self.bitcell_offset.scale(-self.add_left_rbl + bit, -self.left_rbl - 1) + self.strap_offset.scale(-self.add_left_rbl + bit, 0)
            else:
                offset = self.bitcell_offset.scale(-self.add_left_rbl + bit, -self.left_rbl - (self.col_end_offset.y/self.cell.height)) + self.strap_offset.scale(-self.add_left_rbl + bit, 0)

            self.replica_col_insts[bit].place(offset)
        # Grow to the right of the bitcell array, array outward
        for bit in range(self.add_right_rbl):
            if not end_caps_enabled:
                offset = self.bitcell_array_inst.lr() + self.bitcell_offset.scale(bit, -self.left_rbl - 1) + self.strap_offset.scale(bit, -self.left_rbl - 1)
            else:
                offset = self.bitcell_array_inst.lr() + self.bitcell_offset.scale(bit, -self.left_rbl - (self.col_end_offset.y/self.cell.height)) + self.strap_offset.scale(bit, -self.left_rbl - 1)

            self.replica_col_insts[self.add_left_rbl + bit].place(offset)

        # Replica dummy rows
        # Add the dummy rows even if we aren't adding the replica column to this bitcell array
        # These grow up, toward the array
        for bit in range(self.left_rbl):
            self.dummy_row_replica_insts[bit].place(offset=self.bitcell_offset.scale(0, -self.left_rbl + bit + (-self.left_rbl + bit) % 2),
                                                   mirror="MX" if (-self.left_rbl + bit) % 2 else "R0")
        # These grow up, away from the array
        for bit in range(self.right_rbl):
            self.dummy_row_replica_insts[self.left_rbl + bit].place(offset=self.bitcell_offset.scale(0, bit + bit % 2) + self.bitcell_array_inst.ul(),
                                                                   mirror="MX" if bit % 2 else "R0")
        
    def add_end_caps(self):
        """ Add dummy cells or end caps around the array """
        end_caps_enabled = cell_properties.bitcell.end_caps

        # FIXME: These depend on the array size itself
        # Far top dummy row (first row above array is NOT flipped)
        flip_dummy = self.right_rbl % 2
        if not end_caps_enabled:
            dummy_row_offset = self.bitcell_offset.scale(0, self.right_rbl + flip_dummy) + self.bitcell_array_inst.ul()
        else:
            dummy_row_offset = self.bitcell_offset.scale(0, self.right_rbl + flip_dummy) + self.bitcell_array_inst.ul()

        self.dummy_row_insts[1].place(offset=dummy_row_offset,
                                      mirror="MX" if flip_dummy else "R0")
        # FIXME: These depend on the array size itself
        # Far bottom dummy row (first row below array IS flipped)
        flip_dummy = (self.left_rbl + 1) % 2
        if not end_caps_enabled:
            dummy_row_offset = self.bitcell_offset.scale(0, -self.left_rbl - 1 + flip_dummy)
        else:
             dummy_row_offset = self.bitcell_offset.scale(0, -self.left_rbl - (self.col_end_offset.y/self.cell.height) + flip_dummy)
        self.dummy_row_insts[0].place(offset=dummy_row_offset,
                                          mirror="MX" if flip_dummy else "R0")
        # Far left dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        if not end_caps_enabled:
            dummy_col_offset = self.bitcell_offset.scale(-self.add_left_rbl - 1, -self.left_rbl - 1)
        else:
            dummy_col_offset = self.bitcell_offset.scale(-(self.add_left_rbl*(1+self.strap_offset.x/self.cell.width)) - (self.row_end_offset.x/self.cell.width), -self.left_rbl - (self.col_end_offset.y/self.cell.height))

        self.dummy_col_insts[0].place(offset=dummy_col_offset)
        # Far right dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        if not end_caps_enabled:
            dummy_col_offset = self.bitcell_offset.scale(self.add_right_rbl*(1+self.strap_offset.x/self.cell.width), -self.left_rbl - 1) + self.bitcell_array_inst.lr()
        else:
            dummy_col_offset = self.bitcell_offset.scale(self.add_right_rbl*(1+self.strap_offset.x/self.cell.width), -self.left_rbl - (self.col_end_offset.y/self.cell.height)) + self.bitcell_array_inst.lr()

        self.dummy_col_insts[1].place(offset=dummy_col_offset)

    def add_layout_pins(self):
        """ Add the layout pins """

        # All wordlines
        # Main array wl and bl/br
        for pin_name in self.all_wordline_names:
            pin_list = self.bitcell_array_inst.get_pins(pin_name)
            for pin in pin_list:
                self.add_layout_pin(text=pin_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=pin.height())
        for pin_name in self.all_bitline_names:
            pin_list = self.bitcell_array_inst.get_pins(pin_name)
            for pin in pin_list:
                self.add_layout_pin(text=pin_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(1, 0),
                                    width=pin.width(),
                                    height=self.height)

        # Dummy wordlines
        for (names, inst) in zip(self.dummy_row_wordline_names, self.dummy_row_insts):
            for (wl_name, pin_name) in zip(names, self.dummy_row.get_wordline_names()):
                # It's always a single row
                pin = inst.get_pin(pin_name)
                self.add_layout_pin(text=wl_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=pin.height())

        # Replica wordlines (go by the row instead of replica column because we may have to add a pin
        # even though the column is in another local bitcell array)
        for (names, inst) in zip(self.rbl_wordline_names, self.dummy_row_replica_insts):
            for (wl_name, pin_name) in zip(names, self.dummy_row.get_wordline_names()):
                pin = inst.get_pin(pin_name)
                self.add_layout_pin(text=wl_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=pin.height())

        # Replica bitlines
        for (names, inst) in zip(self.rbl_bitline_names, self.replica_col_insts):
            for (bl_name, pin_name) in zip(names, self.replica_columns[0].all_bitline_names):
                pin = inst.get_pin(pin_name)
                self.add_layout_pin(text=bl_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(1, 0),
                                    width=pin.width(),
                                    height=self.height)

        # vdd/gnd are only connected in the perimeter cells
        # replica column should only have a vdd/gnd in the dummy cell on top/bottom
        supply_insts = self.dummy_col_insts + self.dummy_row_insts
        
        for pin_name in  self.supplies:
            for inst in supply_insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name,
                                       loc=pin.center(),
                                       directions=("V", "V"),
                                       start_layer=pin.layer)

            for inst in self.replica_col_insts:
                self.copy_layout_pin(inst, pin_name)

    def get_rbl_wordline_names(self, port=None):
        """ 
        Return the ACTIVE WL for the given RBL port.
        Inactive will be set to gnd. 
        """
        if port == None:
            return self.all_rbl_wordline_names
        else:
            return self.rbl_wordline_names[port]

    def get_rbl_bitline_names(self, port=None):
        """ Return the BL for the given RBL port """
        if port == None:
            return self.all_rbl_bitline_names
        else:
            return self.rbl_bitline_names[port]

    def get_bitline_names(self, port=None):
        """ Return the regular bitlines for the given port or all"""
        if port == None:
            return self.all_bitline_names
        else:
            return self.bitline_names[port]
        
    def get_all_bitline_names(self):
        """ Return ALL the bitline names (including dummy and rbl) """
        temp = []
        temp.extend(self.get_dummy_bitline_names(0))
        if self.add_left_rbl > 0:
            temp.extend(self.get_rbl_bitline_names(0))
        temp.extend(self.get_bitline_names())
        if self.add_right_rbl > 0:
            temp.extend(self.get_rbl_bitline_names(self.add_left_rbl))
        temp.extend(self.get_dummy_bitline_names(1))
        return temp

    def get_wordline_names(self, port=None):
        """ Return the regular wordline names """
        if port == None:
            return self.all_wordline_names
        else:
            return self.wordline_names[port]
    
    def get_all_wordline_names(self, port=None):
        """ Return all the wordline names """
        temp = []
        temp.extend(self.get_dummy_wordline_names(0))
        temp.extend(self.get_rbl_wordline_names(0))
        if port == None:
            temp.extend(self.all_wordline_names)
        else:
            temp.extend(self.wordline_names[port])
        if len(self.all_ports) > 1:
            temp.extend(self.get_rbl_wordline_names(1))
        temp.extend(self.get_dummy_wordline_names(1))
        return temp
        
    def get_dummy_wordline_names(self, port=None):
        """ 
        Return the ACTIVE WL for the given dummy port.
        """
        if port == None:
            return self.all_dummy_row_wordline_names
        else:
            return self.dummy_row_wordline_names[port]

    def get_dummy_bitline_names(self, port=None):
        """ Return the BL for the given dummy port """
        if port == None:
            return self.all_dummy_col_bitline_names
        else:
            return self.dummy_col_bitline_names[port]
        
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

    def get_wordline_cin(self):
        """Get the relative input capacitance from the wordline connections in all the bitcell"""
        # A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
        bitcell_wl_cin = self.cell.get_wl_cin()
        total_cin = bitcell_wl_cin * self.column_size
        return total_cin

    def graph_exclude_bits(self, targ_row, targ_col):
        """Excludes bits in column from being added to graph except target"""
        self.bitcell_array.graph_exclude_bits(targ_row, targ_col)

    def graph_exclude_replica_col_bits(self):
        """Exclude all replica/dummy cells in the replica columns except the replica bit."""

        for port in range(self.left_rbl + self.right_rbl):
            self.replica_columns[port].exclude_all_but_replica()

    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        return self.bitcell_array.get_cell_name(inst_name + '.x' + self.bitcell_array_inst.name, row, col)
