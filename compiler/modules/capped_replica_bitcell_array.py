# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#

from openram import debug
from openram.base import vector
from openram.base import contact
from openram.sram_factory import factory
from openram.tech import drc, spice
from openram.tech import cell_properties as props
from openram.tech import connect_ring_bottom, connect_ring_left, connect_ring_right, connect_ring_top
from openram.tech import power_ring_top, power_ring_bottom, power_ring_left, power_ring_right

from openram import OPTS
from .bitcell_base_array import bitcell_base_array


class capped_replica_bitcell_array(bitcell_base_array):
    """
    Creates a replica bitcell array then adds the row and column caps to all
    sides of a bitcell array.
    """
    def __init__(self, rows, cols, rbl=None, left_rbl=None, right_rbl=None, name=""):
        super().__init__(name, rows, cols, column_offset=0, row_offset=0)
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
        self.extra_rows = sum(self.rbl) + 2
        # If we aren't using row/col caps, then we need to use the bitcell
        #if not self.cell.end_caps:
        #    self.extra_rows += 2

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
                                                    column_offset=1,
                                                    row_offset=1,
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
                                          row_offset=self.row_size+ self.extra_rows + 1, #add 1 to account for bottom col_cap
                                          mirror=0,
                                          location="top",
                                          left_rbl=self.left_rbl,
                                          right_rbl=self.right_rbl)

        self.col_cap_bottom = factory.create(module_type=col_cap_module_type,
                                             cols=self.column_size + len(self.rbls),
                                             rows=1,
                                             # dummy column + left replica column(s)
                                             column_offset=1,
                                             row_offset=0,
                                             mirror=(1+self.row_size+self.extra_rows) % 2,
                                             location="bottom",
                                             left_rbl=self.left_rbl,
                                             right_rbl=self.right_rbl)

        # Dummy Col or Row Cap, depending on bitcell array properties
        row_cap_module_type = ("row_cap_array" if self.cell.end_caps else "dummy_array")

        self.row_cap_left = factory.create(module_type=row_cap_module_type,
                                            cols=1,
                                            rows=self.row_size + self.extra_rows,
                                            column_offset=0,
                                            row_offset=0,
                                            location="left")

        self.row_cap_right = factory.create(module_type=row_cap_module_type,
                                            cols=1,
                                            rows=self.row_size + self.extra_rows,
                                            column_offset=1 + len(self.left_rbl) + self.column_size + len(self.right_rbl),
                                            row_offset=0,
                                            location="right")

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

        # Left/right row caps cover the full array height. Pad with gnd so the
        # netlist list length matches the row cap (replica in the center); do
        # not use col cap wordline heuristics.

        n_rowcap_wl = len(self.row_cap_left.get_wordline_names())
        n_rba_wl = len(self.replica_array_wordline_names_with_grounded_wls)


        self.wordline_pin_list = []

        if self.rbls:
            self.wordline_pin_list.extend(["gnd"] * len(self.rbls))
        self.wordline_pin_list.extend(self.replica_array_wordline_names_with_grounded_wls)
        if self.rbls:
            self.wordline_pin_list.extend(["gnd"] * len(self.rbls))

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
                                                  mod=self.col_cap_bottom,))
        self.connect_inst(self.bitline_pin_list + ["gnd"] * len(self.col_cap_bottom.get_wordline_names()) + self.supplies)
        self.dummy_row_insts.append(self.add_inst(name="dummy_row_top",
                                                  mod=self.col_cap_top))
        self.connect_inst(self.bitline_pin_list + ["gnd"] * len(self.col_cap_top.get_wordline_names()) + self.supplies)

        # Left/right Dummy columns
        self.dummy_col_insts = []
        self.dummy_col_insts.append(self.add_inst(name="dummy_col_left",
                                                    mod=self.row_cap_left))
        self.connect_inst(["dummy_left_" + bl for bl in self.row_cap_left.all_bitline_names] + self.wordline_pin_list + self.supplies)

        #print(self.dummy_col_insts[0].mod.pins)
        #print(["dummy_left_" + bl for bl in self.row_cap_left.all_bitline_names] + self.wordline_pin_list + self.supplies)

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

        # Everything is computed with the replica array
        self.replica_bitcell_array_inst.place(offset=0)

        self.add_end_caps()

        ll = vector(-1 * self.dummy_col_insts[0].width, -1 * self.dummy_row_insts[0].height)
        self.translate_all(ll)

        self.capped_rba_width = (self.dummy_col_insts[0].width
                                 + self.replica_bitcell_array_inst.width
                                 + self.dummy_col_insts[1].width)
        self.capped_rba_height = (self.dummy_row_insts[0].height
                                  + self.replica_bitcell_array_inst.height
                                  + self.dummy_row_insts[1].height)


        self.route_power_ring(self.supply_stack[2], self.supply_stack[0])
        self._strap_routing_endpoints = []
        self.route_supplies()

        self.route_unused_wordlines()
        self.debug_print_strap_routing_endpoints("right")
        self._bridge_close_strap_taps()

        self.reset_coordinates()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()
    

    def route_power_ring(self, v_layer, h_layer):
        self.bbox = (vector(0,0), vector(self.capped_rba_width, self.capped_rba_height))
        # add_power_ring uses one shared ring width/pitch for both horizontal and
        # vertical rails, so satisfy DRC requirements of both layers.
        v_layer_width = drc("minwidth_{}".format(v_layer))
        h_layer_width = drc("minwidth_{}".format(h_layer))
        self.supply_rail_width = max(v_layer_width, h_layer_width)
        v_layer_space = drc("{}_to_{}".format(v_layer, v_layer))
        h_layer_space = drc("{}_to_{}".format(h_layer, h_layer))
        # Pitch is centerline-to-centerline rail offset in add_power_ring.
        # Prefer technology routing pitch so ring placement aligns with the
        # routing/via grid, but never violate same-layer spacing.
        drc_pitch = self.supply_rail_width + max(v_layer_space, h_layer_space)
        tech_pitch = max(getattr(self, "{}_pitch".format(v_layer)),
                         getattr(self, "{}_pitch".format(h_layer)))
        self.supply_rail_pitch = max(drc_pitch, tech_pitch)
        self.add_power_ring(v_layer=v_layer, h_layer=h_layer, top=power_ring_top, bottom=power_ring_bottom, left=power_ring_left, right=power_ring_right)
        # Match metal widths used by route_vertical_side_pin / route_horizontal_side_pin for strap bridges.
        _vring = contact(layer_stack=self.supply_stack, directions=("H", "H"))
        self._strap_width_vertical_rail = _vring.second_layer_width
        _hring = contact(layer_stack=self.supply_stack, directions=("V", "V"))
        self._strap_width_horizontal_rail = _hring.first_layer_height

    def get_main_array_top(self):
        return self.replica_bitcell_array_inst.by() + self.replica_bitcell_array.get_main_array_top()

    def get_main_array_bottom(self):
        return self.replica_bitcell_array_inst.by() + self.replica_bitcell_array.get_main_array_bottom()

    def get_main_array_left(self):
        return self.replica_bitcell_array_inst.lx() + self.replica_bitcell_array.get_main_array_left()

    def get_main_array_right(self):
        return self.replica_bitcell_array_inst.lx() + self.replica_bitcell_array.get_main_array_right()

    #FIXME: these names need to be changed to reflect what they're actually returning
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

        # Far top dummy row
        offset = self.replica_bitcell_array_inst.ul()
        self.dummy_row_insts[1].place(offset=offset)

        # Far bottom dummy row
        dummy_row_height = vector(0, self.dummy_row_insts[0].height)
        offset = self.replica_bitcell_array_inst.ll() - dummy_row_height
        self.dummy_row_insts[0].place(offset=offset)
        
        # Far left dummy col
        dummy_col_width =  vector(self.dummy_col_insts[0].width, 0)
        offset = self.dummy_row_insts[0].ll() - dummy_col_width
        if self.dummy_col_insts[0].mod.cell.has_corners is False:
            offset += vector(0, dummy_row_height.y)
        self.dummy_col_insts[0].place(offset=offset)

        # Far right dummy col
        offset = self.dummy_row_insts[0].lr()
        if self.dummy_col_insts[0].mod.cell.has_corners is False:
            offset += vector(0, dummy_row_height.y)
        self.dummy_col_insts[1].place(offset=offset)

    def add_layout_pins(self):
        self.pin_width = self.capped_rba_width + 4 * self.supply_rail_pitch
        self.pin_height = self.capped_rba_height + 4 * self.supply_rail_pitch

        for pin_name in self.used_wordline_names + self.bitline_pin_list:
            pin = self.replica_bitcell_array_inst.get_pin(pin_name)

            if "wl" in pin_name:
                # wordlines
                pin_offset = pin.ll().scale(0, 1)
                pin_width  = self.pin_width
                pin_height = pin.height()
            else:
                # bitlines
                pin_offset = pin.ll().scale(1, 0)
                pin_width  = pin.width()
                pin_height = self.pin_height

            self.add_layout_pin(text=pin_name,
                                layer=pin.layer,
                                offset=pin_offset,
                                width=pin_width,
                                height=pin_height)
            

    def route_supplies(self):

        top = connect_ring_top
        bottom = connect_ring_bottom
        left = connect_ring_left
        right = connect_ring_right

        if 'vdd' in top:
            inst = self.dummy_row_insts[1]
            if 'vdd' in inst.mod.pins:
                for array_pin in inst.get_pins('vdd'):
                    self.connect_side_pin(array_pin, "top", self.top_vdd_pin.cy(),
                                          strap_pin=self.top_vdd_pin)
        if 'gnd' in top:
            inst = self.dummy_row_insts[1]
            if 'gnd' in inst.mod.pins:
                for array_pin in inst.get_pins('gnd'):
                    self.connect_side_pin(array_pin, "top", self.top_gnd_pin.cy(),
                                          strap_pin=self.top_gnd_pin)
        if 'vdd' in bottom:
            inst = self.dummy_row_insts[0]
            if 'vdd' in inst.mod.pins:
                for array_pin in inst.get_pins('vdd'):
                    self.connect_side_pin(array_pin, "bottom", self.bottom_vdd_pin.cy(),
                                          strap_pin=self.bottom_vdd_pin)
        if 'gnd' in bottom:
            inst = self.dummy_row_insts[0]
            if 'gnd' in inst.mod.pins:
                for array_pin in inst.get_pins('gnd'):
                    self.connect_side_pin(array_pin, "bottom", self.bottom_gnd_pin.cy(),
                                          strap_pin=self.bottom_gnd_pin)
        if 'vdd' in left:
            inst = self.dummy_col_insts[0]
            if 'vdd' in inst.mod.pins:
                for array_pin in inst.get_pins('vdd'):
                    self.connect_side_pin(array_pin, "left", self.left_vdd_pin.cx(),
                                          strap_pin=self.left_vdd_pin)
        if 'gnd' in left:
            inst = self.dummy_col_insts[0]
            if 'gnd' in inst.mod.pins:
                for array_pin in inst.get_pins('gnd'):
                    self.connect_side_pin(array_pin, "left", self.left_gnd_pin.cx(),
                                          strap_pin=self.left_gnd_pin)
        if 'vdd' in right:
            inst = self.dummy_col_insts[1]
            if 'vdd' in inst.mod.pins:
                for array_pin in inst.get_pins('vdd'):
                    self.connect_side_pin(array_pin, "right", self.right_vdd_pin.cx(),
                                          strap_pin=self.right_vdd_pin)
        if 'gnd' in right:
            inst = self.dummy_col_insts[1]
            if 'gnd' in inst.mod.pins:
                for array_pin in inst.get_pins('gnd'):
                    self.connect_side_pin(array_pin, "right", self.right_gnd_pin.cx(),
                                          strap_pin=self.right_gnd_pin)
                          
    def route_unused_wordlines(self):
        """
        Connect the unused RBL and dummy wordlines to gnd
        """
        # This grounds all the dummy row word lines
        for inst in self.dummy_row_insts:
            for wl_name in inst.mod.get_wordline_names():
                pin = inst.get_pin(wl_name)
                self.connect_side_pin(pin, "left", self.left_gnd_pin.cx(),
                                      strap_pin=self.left_gnd_pin)
                self.connect_side_pin(pin, "right", self.right_gnd_pin.cx(),
                                      strap_pin=self.right_gnd_pin)

        # Ground the unused replica wordlines
        for wl_name in self.unused_wordline_names:
            pin = self.replica_bitcell_array_inst.get_pin(wl_name)
            self.connect_side_pin(pin, "left", self.left_gnd_pin.cx(),
                                  strap_pin=self.left_gnd_pin)
            self.connect_side_pin(pin, "right", self.right_gnd_pin.cx(),
                                  strap_pin=self.right_gnd_pin)

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

    def connect_side_pin(self, pin, side, offset, strap_pin=None):
        """
        Connect a pin to the horizontal or vertical supply strap.
        offset is the strap coordinate (y for top/bottom, x for left/right).
        strap_pin is the ring segment pin; its layer is used as the via top target
        (same as legacy route_supplies to_layer=supply_pin.layer).

        Each tap is recorded in ``_strap_routing_endpoints``; after all supplies and
        wordline grounds are routed, ``_bridge_close_strap_taps`` widens strap metal
        along each rail group (min–max tap extent) to merge same-net strap shapes.
        """
        if side in ["left", "right"]:
            self.connect_vertical_side_pin(pin, offset, strap_pin=strap_pin, side=side)
        elif side in ["top", "bottom", "bot"]:
            self.connect_horizontal_side_pin(pin, offset, strap_pin=strap_pin, side=side)
        else:
            debug.error("Invalid side {}".format(side), -1)

    def connect_horizontal_side_pin(self, pin, yoffset, strap_pin=None, side=None):
        """
        Used to connect a pin to the top/bottom horizontal straps.
        """
        cell_loc = pin.center()
        pin_loc = vector(cell_loc.x, yoffset)
        to_layer = strap_pin.layer if strap_pin is not None else self.supply_stack[0]

        self.add_via_stack_center(offset=pin_loc,
                                  from_layer=pin.layer,
                                  to_layer=to_layer,
                                  directions=("V", "V"))
        self.add_path(pin.layer, [cell_loc, pin_loc])
        if strap_pin is not None and side is not None:
            self._strap_routing_endpoints.append({"kind": "horizontal",
                                                  "side": side,
                                                  "strap": strap_pin,
                                                  "from_layer": pin.layer,
                                                  "pin_name": getattr(pin, "name", ""),
                                                  "center": pin_loc})

    def connect_vertical_side_pin(self, pin, xoffset, strap_pin=None, side=None):
        """
        Used to connect a pin to the left/right vertical straps.
        """
        cell_loc = pin.center()
        pin_loc = vector(xoffset, cell_loc.y)
        to_layer = strap_pin.layer if strap_pin is not None else self.supply_stack[2]

        self.add_via_stack_center(offset=pin_loc,
                                  from_layer=pin.layer,
                                  to_layer=to_layer,
                                  directions=("H", "H"))
        self.add_path(pin.layer, [cell_loc, pin_loc])
        if strap_pin is not None and side is not None:
            self._strap_routing_endpoints.append({"kind": "vertical",
                                                  "side": side,
                                                  "strap": strap_pin,
                                                  "from_layer": pin.layer,
                                                  "pin_name": getattr(pin, "name", ""),
                                                  "center": pin_loc})

    def _strap_side_key(self, side):
        return "bottom" if side == "bot" else side

    def debug_print_strap_routing_endpoints(self, direction):
        """
        Debug: print all entries in ``_strap_routing_endpoints`` for one strap
        direction, sorted along the rail (y for left/right, x for top/bottom).

        direction: ``'left'``, ``'right'``, ``'top'``, ``'bottom'``, or ``'bot'``.

        Call after ``route_supplies`` / ``route_unused_wordlines`` and before
        ``_bridge_close_strap_taps`` (the bridge step clears the list).
        """
        want = self._strap_side_key(direction)
        if want not in ("left", "right", "top", "bottom"):
            print("debug_print_strap_routing_endpoints: invalid direction {!r} (use left, right, top, bottom, bot)".format(direction))
            return

        recs = getattr(self, "_strap_routing_endpoints", None) or []
        filtered = []
        for r in recs:
            sk = self._strap_side_key(r["side"])
            if sk != want:
                continue
            if want in ("left", "right") and r["kind"] != "vertical":
                continue
            if want in ("top", "bottom") and r["kind"] != "horizontal":
                continue
            filtered.append(r)

        if want in ("left", "right"):
            filtered.sort(key=lambda r: (r["center"].y, r["center"].x, r.get("pin_name", "")))
            sort_axis = "y"
        else:
            filtered.sort(key=lambda r: (r["center"].x, r["center"].y, r.get("pin_name", "")))
            sort_axis = "x"

        sep = "-" * 88
        print(sep)
        print("{}  strap_routing_endpoints  side={!r}  ({} taps, sort by {})".format(
            self.name, want, len(filtered), sort_axis))
        print(sep)
        hdr = "{:>4}  {:>12}  {:>12}  {:>6}  {:>6}  {:<20}  {}".format(
            "idx", "cx", "cy", "strap", "from", "pin", "strap_c")
        print(hdr)
        print(sep)
        for i, r in enumerate(filtered):
            c = r["center"]
            sp = r["strap"]
            print("{:>4}  {:12.4f}  {:12.4f}  {:>6}  {:>6}  {:<20}  ({:.4f},{:.4f})".format(
                i, c.x, c.y, sp.layer, r["from_layer"],
                (r.get("pin_name") or "-")[:20],
                sp.cx(), sp.cy()))
        print(sep)

    def _pwr_stack(self):
        st = self.supply_stack
        return st if isinstance(st, (list, tuple)) and len(st) >= 3 else None

    def _strap_m3_merge_width(self, vert, from_layers, strap_layer):
        pw = self._pwr_stack()
        if not pw:
            return self.supply_rail_width
        d = ("H", "H") if vert else ("V", "V")
        mx = max(self.via_stack_metal_layer_extent(fl, strap_layer, d, pw[0], not vert) for fl in from_layers)
        if mx > 0:
            return mx
        c = contact(layer_stack=pw, directions=d)
        return c.first_layer_width if vert else c.first_layer_height

    def _strap_merge_minsep_seg(self, rail_layer, w_fb):
        """Merge spacing: max over ``supply_stack`` of ``minwidth_L+L_to_L`` and adjacent ``L0_to_L1`` if in DRC; else rail-only."""
        pw = self._pwr_stack()
        if pw:
            ms = 0.0
            for lyr in pw:
                wkey = "minwidth_{}".format(lyr)
                if wkey not in drc:
                    continue
                skey = "{}_to_{}".format(lyr, lyr)
                sp = drc(skey) if skey in drc else 0.0
                ms = max(ms, drc(wkey) + sp)
            for i in range(len(pw) - 1):
                a, b = pw[i], pw[i + 1]
                for pair in ("{}_to_{}".format(a, b), "{}_to_{}".format(b, a)):
                    if pair in drc:
                        ms = max(ms, drc(pair))
                        break
            if ms <= 0:
                wkey = "minwidth_{}".format(pw[0])
                if wkey in drc:
                    sk = "{}_to_{}".format(pw[0], pw[0])
                    ms = drc(wkey) + (drc(sk) if sk in drc else 0.0)
            return pw[0], ms
        wkey = "minwidth_{}".format(rail_layer)
        mw = drc(wkey) if wkey in drc else w_fb
        skey = "{}_to_{}".format(rail_layer, rail_layer)
        sp = drc(skey) if skey in drc else 0.0
        return rail_layer, mw + sp

    def _bridge_close_strap_taps(self):
        """Close strap taps: m3 bars (min-area width) on too-close centers; m4 too when rail is stack top; ends at outer m3 along rail."""
        ep = getattr(self, "_strap_routing_endpoints", None)
        if not ep:
            return
        eps, pw = 1e-9, self._pwr_stack()
        m3, m4 = (pw[0], pw[2]) if pw else (None, None)
        wv = getattr(self, "_strap_width_vertical_rail", self.supply_rail_width)
        wh = getattr(self, "_strap_width_horizontal_rail", self.supply_rail_width)

        def cluster(fixed, rail, recs, vert):
            if len(recs) < 2:
                return
            recs.sort(key=(lambda r: (r["center"].y, r["center"].x)) if vert else (lambda r: (r["center"].x, r["center"].y)))
            fl = {r["from_layer"] for r in recs}
            seg, ms = self._strap_merge_minsep_seg(rail, wv if vert else wh)
            dw = self._strap_m3_merge_width(vert, fl, rail)
            d = ("H", "H") if vert else ("V", "V")
            w_top = 0.0
            if m4 is not None and rail == m4:
                c = contact(layer_stack=pw, directions=d)
                w_top = c.second_layer_width if vert else c.second_layer_height
            for i in range(len(recs) - 1):
                r0, r1 = recs[i], recs[i + 1]
                g0, g1 = ((r0["center"].y, r1["center"].y) if vert else (r0["center"].x, r1["center"].x))
                if g1 - g0 <= eps or g1 - g0 >= ms:
                    continue
                if m3:
                    e0 = self.via_stack_metal_layer_extent(r0["from_layer"], rail, d, m3, vert)
                    e1 = self.via_stack_metal_layer_extent(r1["from_layer"], rail, d, m3, vert)
                else:
                    e0 = e1 = 0.0
                a, b = g0 - 0.5 * e0, g1 + 0.5 * e1
                if b <= a + eps:
                    a, b = g0, g1
                if vert:
                    s, e = vector(fixed, a), vector(fixed, b)
                else:
                    s, e = vector(a, fixed), vector(b, fixed)
                self.add_segment_center(layer=seg, start=s, end=e, width=dw)
                if w_top > 0:
                    self.add_segment_center(layer=m4, start=s, end=e, width=w_top)

        vg, hg = {}, {}
        for rec in ep:
            sk = self._strap_side_key(rec["side"])
            sp = rec["strap"]
            if rec["kind"] == "vertical":
                vg.setdefault((sk, round(sp.cx(), 9), sp.layer), []).append(rec)
            elif rec["kind"] == "horizontal":
                hg.setdefault((sk, round(sp.cy(), 9), sp.layer), []).append(rec)

        for key, recs in vg.items():
            if len(recs) >= 2:
                cluster(recs[0]["center"].x, key[2], recs, True)
        for key, recs in hg.items():
            if len(recs) >= 2:
                cluster(recs[0]["center"].y, key[2], recs, False)

        self._strap_routing_endpoints = []

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
