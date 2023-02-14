#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.modules import bitcell_array
from openram.sram_factory import factory
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array


class sky130_bitcell_array(bitcell_array, sky130_bitcell_base_array):
    """
    Creates a rows x cols array of memory cells.
    Assumes bit-lines and word lines are connected by abutment.
    """
    def __init__(self, rows, cols, column_offset=0, name=""):
        # Don't call the regular bitcell_array constructor since we don't want its constructor, just
        # some of it's useful member functions
        sky130_bitcell_base_array.__init__(self, rows=rows, cols=cols, column_offset=column_offset, name=name)
        if self.row_size % 2 == 0:
            debug.error("Invalid number of rows {}. number of rows (excluding dummy rows) must be odd to connect to col ends".format(self.row_size), -1)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, self.row_size, self.column_size))
        self.add_comment("rows: {0} cols: {1}".format(self.row_size, self.column_size))

        # This will create a default set of bitline/wordline names
        self.create_all_bitline_names()
        self.create_all_wordline_names()
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            self.add_supply_pins()

    def add_modules(self):
        """ Add the modules used in this design """
        # Bitcell for port names only
        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")
        self.cell2 = factory.create(module_type=OPTS.bitcell, version="opt1a")
        self.strap = factory.create(module_type="internal", version="wlstrap")
        self.strap2 = factory.create(module_type="internal", version="wlstrap_p")
        self.strap3 = factory.create(module_type="internal", version="wlstrapa")
        self.strap4 = factory.create(module_type="internal", version="wlstrapa_p")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        self.array_layout = []
        alternate_bitcell = (self.row_size) % 2
        for row in range(0, self.row_size):

            row_layout = []

            alternate_strap = (self.row_size+1) % 2
            for col in range(0, self.column_size):
                if alternate_bitcell == 1:
                    row_layout.append(self.cell)
                    self.cell_inst[row, col]=self.add_inst(name="row_{}_col_{}_bitcell".format(row, col),
                                                           mod=self.cell)
                else:
                    row_layout.append(self.cell2)
                    self.cell_inst[row, col]=self.add_inst(name="row_{}_col_{}_bitcell".format(row, col),
                                                           mod=self.cell2)
                self.connect_inst(self.get_bitcell_pins(row, col))
                if col != self.column_size - 1:
                    if alternate_strap:
                        if row % 2:
                            name="row_{}_col_{}_wlstrapa_p".format(row, col)
                            row_layout.append(self.strap4)
                            self.add_inst(name=name, mod=self.strap4)
                        else:
                            name="row_{}_col_{}_wlstrap_p".format(row, col)
                            row_layout.append(self.strap2)
                            self.add_inst(name=name, mod=self.strap2)
                        alternate_strap = 0
                    else:
                        if row % 2:
                            name="row_{}_col_{}_wlstrapa".format(row, col)
                            row_layout.append(self.strap3)
                            self.add_inst(name=name.format(row, col), mod=self.strap3)
                        else:
                            name="row_{}_col_{}_wlstrap".format(row, col)
                            row_layout.append(self.strap)
                            self.add_inst(name=name.format(row, col), mod=self.strap)
                        alternate_strap = 1
                    self.connect_inst(self.get_strap_pins(row, col, name))
            if alternate_bitcell == 0:
                alternate_bitcell = 1
            else:
                alternate_bitcell = 0
            self.array_layout.append(row_layout)
