#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import geometry
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_replica_column(sky130_bitcell_base_array):
    """
    Generate a replica bitline column for the replica array.
    Rows is the total number of rows i the main array.
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
        # left, right, regular rows plus top/bottom dummy cells

        self.total_size = self.left_rbl + rows + self.right_rbl + 2
        self.column_offset = column_offset

        if self.rows % 2 == 0:
            debug.error("Invalid number of rows {}. Number of rows must be even to connect to col ends".format(self.rows), -1)
        if self.column_offset % 2 == 0:
            debug.error("Invalid column_offset {}. Column offset must be odd to connect to col ends".format(self.rows), -1)
        debug.check(replica_bit != 0 and replica_bit != rows,
                    "Replica bit cannot be the dummy row.")
        debug.check(replica_bit <= self.left_rbl or replica_bit >= self.total_size - self.right_rbl - 1,
                    "Replica bit cannot be in the regular array.")
        # if OPTS.tech_name == "sky130":
        #     debug.check(rows % 2 == 0 and (self.left_rbl + 1) % 2 == 0,
        #                 "sky130 currently requires rows to be even and to start with X mirroring"
        #                 + " (left_rbl must be even) for LVS.")
        # commented out to support odd row counts while testing opc

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.place_instances()

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):

        self.create_all_bitline_names()
        #self.create_all_wordline_names(self.row_size+2)
        # +2 to add fake wl pins for colends
        self.create_all_wordline_names(self.row_size+1, 1)
        self.add_pin_list(self.all_bitline_names, "OUTPUT")
        self.add_pin_list(self.all_wordline_names, "INPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        self.add_pin("top_gate", "INPUT")
        self.add_pin("bot_gate", "INPUT")

    def add_modules(self):
        self.replica_cell = factory.create(module_type="replica_bitcell_1port", version="opt1")
        self.cell = self.replica_cell
        self.replica_cell2 = factory.create(module_type="replica_bitcell_1port", version="opt1a")

        self.dummy_cell = factory.create(module_type="dummy_bitcell_1port", version="opt1")
        self.dummy_cell2 = factory.create(module_type="dummy_bitcell_1port", version="opt1")

        self.strap1 = factory.create(module_type="internal", version="wlstrap")
        self.strap2 = factory.create(module_type="internal", version="wlstrap_p")
        self.strap3 = factory.create(module_type="internal", version="wlstrapa_p")

        self.colend = factory.create(module_type="col_cap", version="colend")
        self.edge_cell = self.colend
        self.colenda = factory.create(module_type="col_cap", version="colenda")
        self.colend_p_cent = factory.create(module_type="col_cap", version="colend_p_cent")
        self.colenda_p_cent = factory.create(module_type="col_cap", version="colenda_p_cent")

    def create_instances(self):
        self.cell_inst = {}
        self.array_layout = []
        alternate_bitcell = (self.rows + 1) % 2
        for row in range(self.total_size):
            row_layout = []
            name="rbc_{0}".format(row)
            # Top/bottom cell are always dummy cells.
            # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
            # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.
            if (row > self.left_rbl and row < self.total_size - 1 or row == self.replica_bit):

                if alternate_bitcell == 0:
                    row_layout.append(self.replica_cell)
                    self.cell_inst[row]=self.add_inst(name=name, mod=self.replica_cell)
                    self.connect_inst(self.get_bitcell_pins(row, 0))
                    row_layout.append(self.strap2)
                    self.add_inst(name=name + "_strap_p", mod=self.strap2)
                    self.connect_inst(self.get_strap_pins(row, 0, name + "_strap_p"))
                    alternate_bitcell = 1

                else:
                    row_layout.append(self.replica_cell2)
                    self.cell_inst[row]=self.add_inst(name=name, mod=self.replica_cell2)
                    self.connect_inst(self.get_bitcell_pins(row, 0))
                    row_layout.append(self.strap3)
                    self.add_inst(name=name + "_strap", mod=self.strap3)
                    self.connect_inst(self.get_strap_pins(row, 0))
                    alternate_bitcell = 0

            elif (row == 0):
                row_layout.append(self.colend)
                self.cell_inst[row]=self.add_inst(name=name, mod=self.colend)
                self.connect_inst(self.get_col_cap_pins(row, 0))
                row_layout.append(self.colend_p_cent)
                self.add_inst(name=name + "_cap", mod=self.colend_p_cent)
                self.connect_inst(self.get_col_cap_p_pins(row, 0))
            elif (row == self.total_size - 1):
                row_layout.append(self.colenda)
                self.cell_inst[row]=self.add_inst(name=name, mod=self.colenda)
                self.connect_inst(self.get_col_cap_pins(row, 0))
                row_layout.append(self.colenda_p_cent)
                self.add_inst(name=name + "_cap", mod=self.colenda_p_cent)
                self.connect_inst(self.get_col_cap_p_pins(row, 0))

            self.array_layout.append(row_layout)

    def place_instances(self, name_template="", row_offset=0):
        col_offset = self.column_offset
        yoffset = 0.0

        for row in range(row_offset, len(self.array_layout) + row_offset):
            xoffset = 0.0
            for col in range(col_offset, len(self.array_layout[row]) + col_offset):
                self.place_inst = self.insts[(col - col_offset) + (row - row_offset) * len(self.array_layout[row - row_offset])]
                if row == row_offset or row == (len(self.array_layout) + row_offset -1):
                    if row == row_offset:
                        self.place_inst.place(offset=[xoffset, yoffset + self.colend.height], mirror="MX")
                    else:
                        self.place_inst.place(offset=[xoffset, yoffset])

                elif col % 2 == 0:
                    if row % 2 == 0:
                        self.place_inst.place(offset=[xoffset, yoffset + self.place_inst.height], mirror="MX")
                    else:
                        self.place_inst.place(offset=[xoffset, yoffset])
                else:
                    if row % 2 == 0:
                        self.place_inst.place(offset=[xoffset + self.place_inst.width, yoffset + self.place_inst.height], mirror="XY")
                    else:
                        self.place_inst.place(offset=[xoffset + self.place_inst.width, yoffset], mirror="MY")

                xoffset += self.place_inst.width
            if row == row_offset:
                yoffset += self.colend.height
            else:
                yoffset += self.place_inst.height

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

    def add_layout_pins(self):
        """ Add the layout pins """
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
                self.add_layout_pin(text="wl_{0}_{1}".format(port, row_range_max-row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        # for colend in [self.cell_inst[0], self.cell_inst[self.row_size]]:
        #     inst = self.cell_inst[row]
        #     for pin_name in ["top_gate", "bot_gate"]:
        #         pin = inst.get_pin("gate")
        #         self.add_layout_pin(text=pin_name,
        #                             layer=pin.layer,
        #                             offset=pin.ll(),
        #                             width=pin.width(),
        #                             height=pin.height())

        for row in range(self.row_size + 2):
            inst = self.cell_inst[row]
            # add only 1 label per col
            for pin_name in ["vdd", "gnd"]:
                self.copy_layout_pin(inst, pin_name)
                #if row == 2:
                if 'VPB' or 'vpb' in self.cell_inst[row].mod.pins:
                    pin = inst.get_pin("vpb")
                    self.objs.append(geometry.rectangle(layer["nwell"],
                                                        pin.ll(),
                                                        pin.width(),
                                                        pin.height()))
                    self.objs.append(geometry.label("vdd", layer["nwell"], pin.center()))

                if 'VNB' or 'vnb' in self.cell_inst[row].mod.pins:
                    try:
                        from openram.tech import layer_override
                        if layer_override['VNB']:
                            pin = inst.get_pin("vnb")
                            self.add_label("gnd", pin.layer, pin.center())
                            self.objs.append(geometry.rectangle(layer["pwellp"],
                                pin.ll(),
                                pin.width(),
                                pin.height()))
                            self.objs.append(geometry.label("gnd", layer["pwellp"], pin.center()))
                            

                    except:
                        pin = inst.get_pin("vnb")
                        self.add_label("gnd", pin.layer, pin.center())

    def exclude_all_but_replica(self):
        """
        Excludes all bits except the replica cell (self.replica_bit).
        """
        for row, cell in self.cell_inst.items():
            if row != self.replica_bit:
                self.graph_inst_exclude.add(cell)
