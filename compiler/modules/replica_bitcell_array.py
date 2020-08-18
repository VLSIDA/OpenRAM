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

        # Dummy row
        self.dummy_row = factory.create(module_type="dummy_array",
                                        cols=self.column_size,
                                        rows=1,
                                        # dummy column + left replica column
                                        column_offset=1 + self.add_left_rbl,
                                        mirror=0)
        self.add_mod(self.dummy_row)

        # If there are bitcell end caps, replace the dummy cells on the edge of the bitcell array with end caps.
        try:
            end_caps_enabled = cell_properties.bitcell.end_caps
        except AttributeError:
            end_caps_enabled = False

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

    def add_pins(self):

        # Arrays are always:
        # word lines (bottom to top)
        # bit lines (left to right)
        # vdd
        # gnd
        
        self.add_wordline_pins()
        self.add_bitline_pins()
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_bitline_pins(self):
        
        # Regular bitline names for all ports
        self.bitline_names = []
        # Bitline names for each port
        self.bitline_names_by_port = [[] for x in self.all_ports]
        # Replica wordlines by port
        self.replica_bitline_names = [[] for x in self.all_ports]
        # Dummy wordlines by port
        self.dummy_bitline_names = []

        # Regular array bitline names
        self.bitcell_array_bitline_names = self.bitcell_array.get_all_bitline_names()

        # These are the non-indexed names
        dummy_bitline_names = ["dummy_" + x for x in self.cell.get_all_bitline_names()]
        self.dummy_bitline_names.append([x + "_left" for x in dummy_bitline_names])
        self.dummy_bitline_names.append([x + "_right" for x in dummy_bitline_names])

        # Array of all port bitline names
        for port in range(self.add_left_rbl):
            left_names=["rbl_{0}_{1}".format(self.cell.get_bl_name(x), port) for x in range(len(self.all_ports))]
            right_names=["rbl_{0}_{1}".format(self.cell.get_br_name(x), port) for x in range(len(self.all_ports))]
            # Interleave the left and right lists
            bitline_names = [x for t in zip(left_names, right_names) for x in t]
            self.replica_bitline_names[port] = bitline_names
            self.add_pin_list(bitline_names, "INOUT")

        # Dummy bitlines are not connected to anything
        self.bitline_names.extend(self.bitcell_array_bitline_names)

        # Array of all port bitline names
        for port in range(self.add_left_rbl, self.add_left_rbl + self.add_right_rbl):
            left_names=["rbl_{0}_{1}".format(self.cell.get_bl_name(x), port) for x in range(len(self.all_ports))]
            right_names=["rbl_{0}_{1}".format(self.cell.get_br_name(x), port) for x in range(len(self.all_ports))]
            # Interleave the left and right lists
            bitline_names = [x for t in zip(left_names, right_names) for x in t]
            self.replica_bitline_names[port] = bitline_names
            self.add_pin_list(bitline_names, "INOUT")

        self.add_pin_list(self.bitline_names, "INOUT")
            
    def add_wordline_pins(self):
        
        # All wordline names for all ports
        self.wordline_names = []
        # Wordline names for each port
        self.wordline_names_by_port = [[] for x in self.all_ports]
        # Replica wordlines by port
        self.replica_wordline_names = [[] for x in self.all_ports]
        # Dummy wordlines
        self.dummy_wordline_names = {}

        # Regular array wordline names
        self.bitcell_array_wordline_names = self.bitcell_array.get_all_wordline_names()
        
        # These are the non-indexed names
        dummy_cell_wl_names = ["dummy_" + x for x in self.cell.get_all_wl_names()]
        
        # Create the full WL names include dummy, replica, and regular bit cells
        self.wordline_names = []
        
        self.dummy_wordline_names["bot"] = ["{0}_bot".format(x) for x in dummy_cell_wl_names]
        self.wordline_names.extend(self.dummy_wordline_names["bot"])
        
        # Left port WLs 
        for port in range(self.left_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            # Keep track of the pin that is the RBL
            self.replica_wordline_names[port] = wl_names
            self.wordline_names.extend(wl_names)
            
        # Regular WLs
        self.wordline_names.extend(self.bitcell_array_wordline_names)
        
        # Right port WLs
        for port in range(self.left_rbl, self.left_rbl + self.right_rbl):
            # Make names for all RBLs
            wl_names=["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            # Keep track of the pin that is the RBL
            self.replica_wordline_names[port] = wl_names
            self.wordline_names.extend(wl_names)
            
        self.dummy_wordline_names["top"] = ["{0}_top".format(x) for x in dummy_cell_wl_names]
        self.wordline_names.extend(self.dummy_wordline_names["top"])

        # Array of all port wl names
        for port in range(self.left_rbl + self.right_rbl):
            wl_names = ["rbl_{0}_{1}".format(x, port) for x in self.cell.get_all_wl_names()]
            self.replica_wordline_names[port] = wl_names

        self.add_pin_list(self.wordline_names, "INPUT")
         
    def create_instances(self):
        """ Create the module instances used in this design """

        supplies = ["vdd", "gnd"]

        # Used for names/dimensions only
        self.cell = factory.create(module_type="bitcell")

        # Main array
        self.bitcell_array_inst=self.add_inst(name="bitcell_array",
                                              mod=self.bitcell_array)
        self.connect_inst(self.bitcell_array_bitline_names + self.bitcell_array_wordline_names + supplies)

        # Replica columns
        self.replica_col_inst = {}
        for port in range(self.add_left_rbl + self.add_right_rbl):
            self.replica_col_inst[port]=self.add_inst(name="replica_col_{}".format(port),
                                                      mod=self.replica_columns[port])
            self.connect_inst(self.replica_bitline_names[port] + self.wordline_names + supplies)
                
        # Dummy rows under the bitcell array (connected with with the replica cell wl)
        self.dummy_row_replica_inst = {}
        # Note, this is the number of left and right even if we aren't adding the columns to this bitcell array!
        for port in range(self.left_rbl + self.right_rbl):
            self.dummy_row_replica_inst[port]=self.add_inst(name="dummy_row_{}".format(port),
                                                            mod=self.dummy_row)
            self.connect_inst(self.bitcell_array_bitline_names + self.replica_wordline_names[port] + supplies)

        # Top/bottom dummy rows or col caps
        self.dummy_row_bot_inst=self.add_inst(name="dummy_row_bot",
                                                 mod=self.col_cap)
        self.connect_inst(self.bitcell_array_bitline_names
                          + self.dummy_wordline_names["bot"]
                          + supplies)
        self.dummy_row_top_inst=self.add_inst(name="dummy_row_top",
                                                 mod=self.col_cap)
        self.connect_inst(self.bitcell_array_bitline_names
                          + self.dummy_wordline_names["top"]
                          + supplies)

        # Left/right Dummy columns
        self.dummy_col_left_inst=self.add_inst(name="dummy_col_left",
                                               mod=self.row_cap_left)
        self.connect_inst(self.dummy_bitline_names[0] + self.wordline_names + supplies)
        self.dummy_col_right_inst=self.add_inst(name="dummy_col_right",
                                                mod=self.row_cap_right)
        self.connect_inst(self.dummy_bitline_names[-1] + self.wordline_names + supplies)

    def create_layout(self):

        self.height = (self.row_size + self.extra_rows) * self.dummy_row.height
        self.width = (self.column_size + self.extra_cols) * self.cell.width

        # This is a bitcell x bitcell offset to scale
        self.bitcell_offset = vector(self.cell.width, self.cell.height)

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

        # Grow from left to right, toward the array
        for bit in range(self.add_left_rbl):
            offset = self.bitcell_offset.scale(-self.add_left_rbl + bit, -self.left_rbl - 1)
            self.replica_col_inst[bit].place(offset)
        # Grow to the right of the bitcell array, array outward
        for bit in range(self.add_right_rbl):
            offset = self.bitcell_array_inst.lr() + self.bitcell_offset.scale(bit, -self.left_rbl - 1)
            self.replica_col_inst[self.add_left_rbl + bit].place(offset)

        # Replica dummy rows
        # Add the dummy rows even if we aren't adding the replica column to this bitcell array
        # These grow up, toward the array
        for bit in range(self.left_rbl):
            self.dummy_row_replica_inst[bit].place(offset=self.bitcell_offset.scale(0, -self.left_rbl + bit + (-self.left_rbl + bit) % 2),
                                                   mirror="MX" if (-self.left_rbl + bit) % 2 else "R0")
        # These grow up, away from the array
        for bit in range(self.right_rbl):
            self.dummy_row_replica_inst[self.left_rbl + bit].place(offset=self.bitcell_offset.scale(0, bit + bit % 2) + self.bitcell_array_inst.ul(),
                                                                   mirror="MX" if bit % 2 else "R0")
        
    def add_end_caps(self):
        """ Add dummy cells or end caps around the array """

        # FIXME: These depend on the array size itself
        # Far top dummy row (first row above array is NOT flipped)
        flip_dummy = self.right_rbl % 2
        dummy_row_offset = self.bitcell_offset.scale(0, self.right_rbl + flip_dummy) + self.bitcell_array_inst.ul()
        self.dummy_row_top_inst.place(offset=dummy_row_offset,
                                      mirror="MX" if flip_dummy else "R0")
        # FIXME: These depend on the array size itself
        # Far bottom dummy row (first row below array IS flipped)
        flip_dummy = (self.left_rbl + 1) % 2
        dummy_row_offset = self.bitcell_offset.scale(0, -self.left_rbl - 1 + flip_dummy)
        self.dummy_row_bot_inst.place(offset=dummy_row_offset,
                                      mirror="MX" if flip_dummy else "R0")
        # Far left dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(-self.add_left_rbl - 1, -self.left_rbl - 1)
        self.dummy_col_left_inst.place(offset=dummy_col_offset)
        # Far right dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(self.add_right_rbl, -self.left_rbl - 1) + self.bitcell_array_inst.lr()
        self.dummy_col_right_inst.place(offset=dummy_col_offset)

    def add_layout_pins(self):
        """ Add the layout pins """

        # All wordlines
        # Main array wl and bl/br
        pin_names = self.bitcell_array.get_pin_names()
        for pin_name in pin_names:
            for wl in self.bitcell_array_wordline_names:
                if wl in pin_name:
                    pin_list = self.bitcell_array_inst.get_pins(pin_name)
                    for pin in pin_list:
                        self.add_layout_pin(text=pin_name,
                                            layer=pin.layer, 
                                            offset=pin.ll().scale(0, 1),
                                            width=self.width,
                                            height=pin.height())
            for bitline in self.bitcell_array_bitline_names:
                if bitline in pin_name:
                    pin_list = self.bitcell_array_inst.get_pins(pin_name)
                    for pin in pin_list:
                        self.add_layout_pin(text=pin_name,
                                            layer=pin.layer,
                                            offset=pin.ll().scale(1, 0),
                                            width=pin.width(),
                                            height=self.height)

        # Dummy wordlines
        for (name, inst) in [("bot", self.dummy_row_bot_inst), ("top", self.dummy_row_top_inst)]:
            for (pin_name, wl_name) in zip(self.cell.get_all_wl_names(), self.dummy_wordline_names[name]):
                # It's always a single row
                pin = inst.get_pin(pin_name + "_0")
                self.add_layout_pin(text=wl_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=pin.height())

        # Replica wordlines (go by the row instead of replica column because we may have to add a pin
        # even though the column is in another local bitcell array)
        for (port, inst) in list(self.dummy_row_replica_inst.items()):
            for (pin_name, wl_name) in zip(self.cell.get_all_wl_names(), self.replica_wordline_names[port]):
                pin = inst.get_pin(pin_name + "_0")
                self.add_layout_pin(text=wl_name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=pin.height())

        # Replica bitlines
        for port in range(self.add_left_rbl + self.add_right_rbl):
            inst = self.replica_col_inst[port]
            for (pin_name, bl_name) in zip(self.cell.get_all_bitline_names(), self.replica_bitline_names[port]):
                pin = inst.get_pin(pin_name)
                name = "rbl_{0}_{1}".format(pin_name, port)
                self.add_layout_pin(text=name,
                                    layer=pin.layer,
                                    offset=pin.ll().scale(1, 0),
                                    width=pin.width(),
                                    height=self.height)

        # vdd/gnd are only connected in the perimeter cells
        # replica column should only have a vdd/gnd in the dummy cell on top/bottom
        supply_insts = [self.dummy_col_left_inst, self.dummy_col_right_inst,
                        self.dummy_row_top_inst, self.dummy_row_bot_inst]
        for pin_name in ["vdd", "gnd"]:
            for inst in supply_insts:
                pin_list = inst.get_pins(pin_name)
                for pin in pin_list:
                    self.add_power_pin(name=pin_name,
                                       loc=pin.center(),
                                       directions=("V", "V"),
                                       start_layer=pin.layer)

            for inst in list(self.replica_col_inst.values()):
                self.copy_layout_pin(inst, pin_name)

    def get_rbl_wordline_names(self, port=None):
        """ 
        Return the ACTIVE WL for the given RBL port.
        Inactive will be set to gnd. 
        """
        if port == None:
            temp = []
            for port in self.all_ports:
                temp.extend(self.replica_wordline_names[port])
            return temp
        else:
            wl_names = self.replica_wordline_names[port]
            return wl_names[port]

    def get_rbl_bitline_names(self, port=None):
        """ Return the BL for the given RBL port """
        if port == None:
            temp = []
            for port in self.all_ports:
                temp.extend(self.replica_bitline_names[port])
            return temp
        else:
            bl_names = self.replica_bitline_names[port]
            return bl_names[2 * port:2 * port + 2]

    def get_wordline_names(self):
        """ Return the wordline names """
        return self.wordline_names

    def get_bitline_names(self):
        """ Return the bitline names """
        return self.bitline_names

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
