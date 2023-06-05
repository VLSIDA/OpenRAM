#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram.sram_factory import factory
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_row_cap_array(sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, name=""):
        # Don't call the regular col-cap_array constructor since we don't want its constructor, just
        # some of it's useful member functions
        sky130_bitcell_base_array.__init__(self, rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.rows = rows
        self.cols = cols
        self.column_offset = column_offset
        self.mirror = mirror
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.create_all_wordline_names()
        # This module has no bitlines
        # self.create_all_bitline_names()

        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)
        self.add_layout_pins()

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        if self.column_offset == 0:
            self.top_corner = factory.create(module_type="corner", location="ul")
            self.bottom_corner =factory.create(module_type="corner", location="ll")
            self.rowend1 = factory.create(module_type="row_cap", version="rowend_replica")
            self.rowend2 = factory.create(module_type="row_cap", version="rowenda_replica")

        else:
            self.top_corner = factory.create(module_type="corner", location="ur")
            self.bottom_corner = factory.create(module_type="corner", location="lr")

            self.rowend1 = factory.create(module_type="row_cap", version="rowend")
            self.rowend2 = factory.create(module_type="row_cap", version="rowenda")

        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        self.array_layout = []
        alternate_bitcell = (self.rows + 1) % 2
        for row in range(self.rows + 2):
            row_layout = []
            name="rca_{0}".format(row)
            # Top/bottom cell are always dummy cells.
            # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
            # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.

            if (row < self.rows + 1 and row > 0):

                if alternate_bitcell == 0:
                    row_layout.append(self.rowend1)
                    self.cell_inst[row]=self.add_inst(name=name, mod=self.rowend1)
                    self.connect_inst(["wl_0_{}".format(row - 1), "vdd"])
                    alternate_bitcell = 1

                else:
                    row_layout.append(self.rowend2)
                    self.cell_inst[row] = self.add_inst(name=name, mod=self.rowend2)
                    self.connect_inst(["wl_0_{}".format(row - 1), "vdd"])
                    alternate_bitcell = 0

            elif (row == 0):
                row_layout.append(self.bottom_corner)
                self.cell_inst[row]=self.add_inst(name=name, mod=self.bottom_corner)
                self.connect_inst(self.get_corner_pins())

            elif (row == self.rows + 1):
                row_layout.append(self.top_corner)
                self.cell_inst[row]=self.add_inst(name=name, mod=self.top_corner)
                self.connect_inst(self.get_corner_pins())

            self.array_layout.append(row_layout)

    def place_array(self, name_template, row_offset=0):
        xoffset = 0.0
        yoffset = 0.0
        for row in range(len(self.insts)):
            inst = self.insts[row]
            if row == 0:
                inst.place(offset=[xoffset, yoffset + inst.height], mirror="MX")
            elif row == len(self.insts)-1:
                inst.place(offset=[xoffset, yoffset])
            else:
                if row % 2 ==0:
                    inst.place(offset=[xoffset, yoffset + inst.height], mirror="MX")
                else:
                    inst.place(offset=[xoffset, yoffset])
            yoffset += inst.height

    def add_pins(self):
        for row in range(self.rows + 2):
            for port in self.all_ports:
                self.add_pin("wl_{}_{}".format(port, row), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_layout_pins(self):
        """ Add the layout pins """
        for row in range(0, self.rows + 1):
            if row > 0 and row < self.rows + 1:
                wl_pin = self.cell_inst[row].get_pin("wl")
                self.add_layout_pin(text="wl_0_{0}".format(row -1),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        # Add vdd/gnd via stacks
        for row in range(1, self.rows):
            inst = self.cell_inst[row]
            for pin_name in ["vdd", "gnd"]:
                for pin in inst.get_pins(pin_name):
                    self.copy_layout_pin(inst, pin_name)
