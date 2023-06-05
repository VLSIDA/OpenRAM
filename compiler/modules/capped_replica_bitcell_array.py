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
from .bitcell_base_array import bitcell_base_array


class capped_replica_bitcell_array(bitcell_base_array):
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

        self.column_size = cols
        self.row_size = rows
        # This is how many RBLs are in all the arrays
        if rbl is not None:
            self.rbl = rbl
        else:
            self.rbl = [0] * len(self.all_ports)
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
            self.right_rbl=[]
        self.rbls = self.left_rbl + self.right_rbl

        # Two dummy rows plus replica even if we don't add the column
        self.extra_rows = sum(self.rbl)
        # If we aren't using row/col caps, then we need to use the bitcell
        if not self.cell.end_caps:
            self.extra_rows += 2

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def add_modules(self):
        """  Array and cap rows/columns """

        self.replica_bitcell_array = factory.create(module_type="replica_bitcell_array",
                                                    cols=self.column_size,
                                                    rows=self.row_size,
                                                    rbl=self.rbl,
                                                    left_rbl=self.left_rbl,
                                                    right_rbl=self.right_rbl)

        # Dummy Row or Col Cap, depending on bitcell array properties
        col_cap_module_type = ("col_cap_array" if self.cell.end_caps else "dummy_array")

        # TODO: remove redundancy from arguments in pairs below (top/bottom, left/right)
        # for example, cols takes the same value for top/bottom
        self.col_cap_top = factory.create(module_type=col_cap_module_type,
                                          cols=self.column_size + len(self.rbls),
                                          rows=1,
                                          # dummy column + left replica column(s)
                                          column_offset=1,
                                          mirror=0,
                                          location="top")

        self.col_cap_bottom = factory.create(module_type=col_cap_module_type,
                                             cols=self.column_size + len(self.rbls),
                                             rows=1,
                                             # dummy column + left replica column(s)
                                             column_offset=1,
                                             mirror=0,
                                             location="bottom")

        # Dummy Col or Row Cap, depending on bitcell array properties
        row_cap_module_type = ("row_cap_array" if self.cell.end_caps else "dummy_array")

        self.row_cap_left = factory.create(module_type=row_cap_module_type,
                                            cols=1,
                                            column_offset=0,
                                            rows=self.row_size + self.extra_rows,
                                            mirror=(self.rbl[0] + 1) % 2)

        self.row_cap_right = factory.create(module_type=row_cap_module_type,
                                            cols=1,
                                            #   dummy column
                                            # + left replica column(s)
                                            # + bitcell columns
                                            # + right replica column(s)
                                            column_offset=1 + len(self.left_rbl) + self.column_size + self.rbl[0],
                                            rows=self.row_size + self.extra_rows,
                                            mirror=(self.rbl[0] + 1) % 2)

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
        # these four are only included for compatibility with other modules
        self.bitline_names = self.replica_bitcell_array.bitline_names
        self.all_bitline_names = self.replica_bitcell_array.all_bitline_names
        self.rbl_bitline_names = self.replica_bitcell_array.rbl_bitline_names
        self.all_rbl_bitline_names = self.replica_bitcell_array.all_rbl_bitline_names

        # this one is actually used (obviously)
        self.bitline_pin_list = self.replica_bitcell_array.bitline_pin_list
        self.add_pin_list(self.bitline_pin_list, "INOUT")

    def add_wordline_pins(self):
        # some of these are just included for compatibility with modules instantiating this module
        self.rbl_wordline_names = self.replica_bitcell_array.rbl_wordline_names
        self.all_rbl_wordline_names = self.replica_bitcell_array.all_rbl_wordline_names
        self.wordline_names = self.replica_bitcell_array.wordline_names
        self.all_wordline_names = self.replica_bitcell_array.all_wordline_names

        self.used_wordline_names = self.replica_bitcell_array.used_wordline_names
        self.unused_wordline_names = self.replica_bitcell_array.unused_wordline_names
        self.replica_array_wordline_names_with_grounded_wls = ["gnd" if x in self.unused_wordline_names else x for x in self.replica_bitcell_array.wordline_pin_list]

        self.wordline_pin_list = []
        self.wordline_pin_list.extend(["gnd"] * len(self.col_cap_top.get_wordline_names()))
        self.wordline_pin_list.extend(self.replica_array_wordline_names_with_grounded_wls)
        self.wordline_pin_list.extend(["gnd"] * len(self.col_cap_bottom.get_wordline_names()))

        self.add_pin_list(self.used_wordline_names, "INPUT")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.supplies = ["vdd", "gnd"]

        # Main array
        self.replica_bitcell_array_inst=self.add_inst(name="replica_bitcell_array",
                                                      mod=self.replica_bitcell_array)
        self.connect_inst(self.bitline_pin_list + self.replica_array_wordline_names_with_grounded_wls + self.supplies)

        # Top/bottom dummy rows or col caps
        self.dummy_row_insts = []
        self.dummy_row_insts.append(self.add_inst(name="dummy_row_bot",
                                                  mod=self.col_cap_bottom))
        self.connect_inst(self.bitline_pin_list + ["gnd"] * len(self.col_cap_bottom.get_wordline_names()) + self.supplies)
        self.dummy_row_insts.append(self.add_inst(name="dummy_row_top",
                                                  mod=self.col_cap_top))
        self.connect_inst(self.bitline_pin_list + ["gnd"] * len(self.col_cap_top.get_wordline_names()) + self.supplies)

        # Left/right Dummy columns
        self.dummy_col_insts = []
        self.dummy_col_insts.append(self.add_inst(name="dummy_col_left",
                                                    mod=self.row_cap_left))
        self.connect_inst(["dummy_left_" + bl for bl in self.row_cap_left.all_bitline_names] + self.wordline_pin_list + self.supplies)
        self.dummy_col_insts.append(self.add_inst(name="dummy_col_right",
                                                    mod=self.row_cap_right))
        self.connect_inst(["dummy_right_" + bl for bl in self.row_cap_right.all_bitline_names] + self.wordline_pin_list + self.supplies)

        # bitcell array needed for some offset calculations
        self.bitcell_array_inst = self.replica_bitcell_array.bitcell_array_inst

    def create_layout(self):

        # This creates space for the unused wordline connections as well as the
        # row-based or column based power and ground lines.
        self.vertical_pitch = 1.1 * getattr(self, "{}_pitch".format(self.supply_stack[0]))
        self.horizontal_pitch = 1.1 * getattr(self, "{}_pitch".format(self.supply_stack[2]))
        # FIXME: custom sky130 replica module has a better version of this offset
        self.unused_offset = vector(0.25, 0.25)

        # This is a bitcell x bitcell offset to scale
        self.bitcell_offset = vector(self.cell.width, self.cell.height)
        self.col_end_offset = vector(self.cell.width, self.cell.height)
        self.row_end_offset = vector(self.cell.width, self.cell.height)

        # Everything is computed with the replica array
        self.replica_bitcell_array_inst.place(offset=self.unused_offset)

        self.add_end_caps()

        # shift everything up and right to account for cap cells
        self.translate_all(self.bitcell_offset.scale(-1, -1))

        self.width = self.dummy_col_insts[1].rx() + self.unused_offset.x
        self.height = self.dummy_row_insts[1].uy()

        self.add_layout_pins()

        self.route_supplies()

        self.route_unused_wordlines()

        lower_left = self.find_lowest_coords()
        upper_right = self.find_highest_coords()
        self.width = upper_right.x - lower_left.x
        self.height = upper_right.y - lower_left.y
        self.translate_all(lower_left)

        self.add_boundary()

        self.DRC_LVS()

    def get_main_array_top(self):
        return self.replica_bitcell_array_inst.by() + self.replica_bitcell_array.get_main_array_top()

    def get_main_array_bottom(self):
        return self.replica_bitcell_array_inst.by() + self.replica_bitcell_array.get_main_array_bottom()

    def get_main_array_left(self):
        return self.replica_bitcell_array_inst.lx() + self.replica_bitcell_array.get_main_array_left()

    def get_main_array_right(self):
        return self.replica_bitcell_array_inst.lx() + self.replica_bitcell_array.get_main_array_right()

    # FIXME: these names need to be changed to reflect what they're actually returning
    def get_replica_top(self):
        return self.dummy_row_insts[1].by()

    def get_replica_bottom(self):
        return self.dummy_row_insts[0].uy()

    def get_replica_left(self):
        return self.dummy_col_insts[0].lx()

    def get_replica_right(self):
        return self.dummy_col_insts[1].rx()


    def get_column_offsets(self):
        """
        Return an array of the x offsets of all the regular bits
        """
        # must add the offset of the instance
        offsets = [self.replica_bitcell_array_inst.lx() + x for x in self.replica_bitcell_array.get_column_offsets()]
        return offsets

    def add_end_caps(self):
        """ Add dummy cells or end caps around the array """

        # Far top dummy row (first row above array is NOT flipped if even number of rows)
        flip_dummy = (self.row_size + self.rbl[1]) % 2
        dummy_row_offset = self.bitcell_offset.scale(0, flip_dummy) + self.replica_bitcell_array_inst.ul()
        self.dummy_row_insts[1].place(offset=dummy_row_offset,
                                      mirror="MX" if flip_dummy else "R0")

        # Far bottom dummy row (first row below array IS flipped)
        flip_dummy = (self.rbl[0] + 1) % 2
        dummy_row_offset = self.bitcell_offset.scale(0, flip_dummy - 1) + self.unused_offset
        self.dummy_row_insts[0].place(offset=dummy_row_offset,
                                      mirror="MX" if flip_dummy else "R0")
        # Far left dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(-1, -1) + self.unused_offset
        self.dummy_col_insts[0].place(offset=dummy_col_offset)

        # Far right dummy col
        # Shifted down by the number of left RBLs even if we aren't adding replica column to this bitcell array
        dummy_col_offset = self.bitcell_offset.scale(0, -1) + self.replica_bitcell_array_inst.lr()
        self.dummy_col_insts[1].place(offset=dummy_col_offset)

    def add_layout_pins(self):
        for pin_name in self.used_wordline_names + self.bitline_pin_list:
            pin = self.replica_bitcell_array_inst.get_pin(pin_name)

            if "wl" in pin_name:
                # wordlines
                pin_offset = pin.ll().scale(0, 1)
                pin_width  = self.width
                pin_height = pin.height()
            else:
                # bitlines
                pin_offset = pin.ll().scale(1, 0)
                pin_width  = pin.width()
                pin_height = self.height

            self.add_layout_pin(text=pin_name,
                                layer=pin.layer,
                                offset=pin_offset,
                                width=pin_width,
                                height=pin_height)

    def route_supplies(self):

        if OPTS.bitcell == "pbitcell":
            bitcell = factory.create(module_type="pbitcell")
        else:
            bitcell = getattr(props, "bitcell_{}port".format(OPTS.num_ports))

        vdd_dir = bitcell.vdd_dir
        gnd_dir = bitcell.gnd_dir

        # vdd/gnd are only connected in the perimeter cells
        supply_insts = self.dummy_col_insts + self.dummy_row_insts

        # For the wordlines
        top_bot_mult = 1
        left_right_mult = 1

        # There are always vertical pins for the WLs on the left/right if we have unused wordlines
        self.left_gnd_locs = self.route_side_pin("gnd", "left", left_right_mult)
        self.right_gnd_locs = self.route_side_pin("gnd", "right", left_right_mult)
        # This needs to be big enough so that they aren't in the same supply routing grid
        left_right_mult = 4

        if gnd_dir == "V":
            self.top_gnd_locs = self.route_side_pin("gnd", "top", top_bot_mult)
            self.bot_gnd_locs = self.route_side_pin("gnd", "bot", top_bot_mult)
            # This needs to be big enough so that they aren't in the same supply routing grid
            top_bot_mult = 4

        if vdd_dir == "V":
            self.top_vdd_locs = self.route_side_pin("vdd", "top", top_bot_mult)
            self.bot_vdd_locs = self.route_side_pin("vdd", "bot", top_bot_mult)
        elif vdd_dir == "H":
            self.left_vdd_locs = self.route_side_pin("vdd", "left", left_right_mult)
            self.right_vdd_locs = self.route_side_pin("vdd", "right", left_right_mult)
        else:
            debug.error("Invalid vdd direction {}".format(vdd_dir), -1)

        for inst in supply_insts:
            for pin in inst.get_pins("vdd"):
                if vdd_dir == "V":
                    self.connect_side_pin(pin, "top", self.top_vdd_locs[0].y)
                    self.connect_side_pin(pin, "bot", self.bot_vdd_locs[0].y)
                elif vdd_dir == "H":
                    self.connect_side_pin(pin, "left", self.left_vdd_locs[0].x)
                    self.connect_side_pin(pin, "right", self.right_vdd_locs[0].x)

        for inst in supply_insts:
            for pin in inst.get_pins("gnd"):
                if gnd_dir == "V":
                    self.connect_side_pin(pin, "top", self.top_gnd_locs[0].y)
                    self.connect_side_pin(pin, "bot", self.bot_gnd_locs[0].y)
                elif gnd_dir == "H":
                    self.connect_side_pin(pin, "left", self.left_gnd_locs[0].x)
                    self.connect_side_pin(pin, "right", self.right_gnd_locs[0].x)

    def route_unused_wordlines(self):
        """
        Connect the unused RBL and dummy wordlines to gnd
        """
        # This grounds all the dummy row word lines
        for inst in self.dummy_row_insts:
            for wl_name in self.col_cap_top.get_wordline_names():
                pin = inst.get_pin(wl_name)
                self.connect_side_pin(pin, "left", self.left_gnd_locs[0].x)
                self.connect_side_pin(pin, "right", self.right_gnd_locs[0].x)

        # Ground the unused replica wordlines
        for wl_name in self.unused_wordline_names:
            pin = self.replica_bitcell_array_inst.get_pin(wl_name)
            self.connect_side_pin(pin, "left", self.left_gnd_locs[0].x)
            self.connect_side_pin(pin, "right", self.right_gnd_locs[0].x)

    def route_side_pin(self, name, side, offset_multiple=1):
        """
        Routes a vertical or horizontal pin on the side of the bbox.
        The multiple specifies how many track offsets to be away from the side assuming
        (0,0) (self.width, self.height)
        """
        if side in ["left", "right"]:
            return self.route_vertical_side_pin(name, side, offset_multiple)
        elif side in ["top", "bottom", "bot"]:
            return self.route_horizontal_side_pin(name, side, offset_multiple)
        else:
            debug.error("Invalid side {}".format(side), -1)

    def route_vertical_side_pin(self, name, side, offset_multiple=1):
        """
        Routes a vertical pin on the side of the bbox.
        """
        if side == "left":
            bot_loc = vector(-offset_multiple * self.vertical_pitch, 0)
            top_loc = vector(-offset_multiple * self.vertical_pitch, self.height)
        elif side == "right":
            bot_loc = vector(self.width + offset_multiple * self.vertical_pitch, 0)
            top_loc = vector(self.width + offset_multiple * self.vertical_pitch, self.height)

        layer = self.supply_stack[2]
        top_via = contact(layer_stack=self.supply_stack,
                          directions=("H", "H"))

        self.add_layout_pin_segment_center(text=name,
                                           layer=layer,
                                           start=bot_loc,
                                           end=top_loc,
                                           width=top_via.second_layer_width)

        return (bot_loc, top_loc)

    def route_horizontal_side_pin(self, name, side, offset_multiple=1):
        """
        Routes a horizontal pin on the side of the bbox.
        """
        if side in ["bottom", "bot"]:
            left_loc = vector(0, -offset_multiple * self.horizontal_pitch)
            right_loc = vector(self.width, -offset_multiple * self.horizontal_pitch)
        elif side == "top":
            left_loc = vector(0, self.height + offset_multiple * self.horizontal_pitch)
            right_loc = vector(self.width, self.height + offset_multiple * self.horizontal_pitch)

        layer = self.supply_stack[0]
        side_via = contact(layer_stack=self.supply_stack,
                           directions=("V", "V"))

        self.add_layout_pin_segment_center(text=name,
                                           layer=layer,
                                           start=left_loc,
                                           end=right_loc,
                                           width=side_via.first_layer_height)

        return (left_loc, right_loc)

    def connect_side_pin(self, pin, side, offset):
        """
        Used to connect a pin to the a horizontal or vertical strap
        offset gives the location of the strap
        """
        if side in ["left", "right"]:
            self.connect_vertical_side_pin(pin, offset)
        elif side in ["top", "bottom", "bot"]:
            self.connect_horizontal_side_pin(pin, offset)
        else:
            debug.error("Invalid side {}".format(side), -1)

    def connect_horizontal_side_pin(self, pin, yoffset):
        """
        Used to connect a pin to the top/bottom horizontal straps
        """
        cell_loc = pin.center()
        pin_loc = vector(cell_loc.x, yoffset)

        # Place the pins a track outside of the array
        self.add_via_stack_center(offset=pin_loc,
                                  from_layer=pin.layer,
                                  to_layer=self.supply_stack[0],
                                  directions=("V", "V"))

        # Add a path to connect to the array
        self.add_path(pin.layer, [cell_loc, pin_loc])

    def connect_vertical_side_pin(self, pin, xoffset):
        """
        Used to connect a pin to the left/right vertical straps
        """
        cell_loc = pin.center()
        pin_loc = vector(xoffset, cell_loc.y)

        # Place the pins a track outside of the array
        self.add_via_stack_center(offset=pin_loc,
                                  from_layer=pin.layer,
                                  to_layer=self.supply_stack[2],
                                  directions=("H", "H"))

        # Add a path to connect to the array
        self.add_path(pin.layer, [cell_loc, pin_loc])

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
