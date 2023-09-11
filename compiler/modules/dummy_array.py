# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.sram_factory import factory
from openram import OPTS
from .bitcell_base_array import bitcell_base_array
from openram.base import geometry
from .pattern import pattern

class dummy_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """

    def __init__(self, rows, cols, column_offset=0, row_offset=0 ,mirror=0, location="", name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.location = location
        self.row_offset = row_offset
        self.mirror = mirror
 
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        # This will create a default set of bitline/wordline names
        self.create_all_bitline_names()
        self.create_all_wordline_names()

        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array()

        self.add_layout_pins()

        self.route_supplies()

        self.add_boundary()

        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """

        self.dummy_cell = factory.create(module_type=OPTS.dummy_bitcell)
        self.cell = factory.create(module_type=OPTS.bitcell)

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst={}
        if self.cell.mirror.y:
            core_block = [[0 for x in range(2)] for y in range(2)]
            core_block[(0+self.mirror) %2][0] = geometry.instance("core_0_0", mod=self.dummy_cell, is_bitcell=True)
            core_block[(1+self.mirror) %2][0] = geometry.instance("core_1_0", mod=self.dummy_cell, is_bitcell=True, mirror='MX')
            core_block[(0+self.mirror) %2][1] = geometry.instance("core_0_1", mod=self.dummy_cell, is_bitcell=True, mirror='MY')
            core_block[(1+self.mirror) %2][1] = geometry.instance("core_1_1", mod=self.dummy_cell, is_bitcell=True, mirror='XY')
        else: 
            core_block = [[0 for x in range(1)] for y in range(2)]
            core_block[(0+self.mirror) %2][0] = geometry.instance("core_0_0", mod=self.dummy_cell, is_bitcell=True)
            core_block[(1+self.mirror) %2][0] = geometry.instance("core_1_0", mod=self.dummy_cell, is_bitcell=True, mirror='MX')


        self.pattern = pattern(self, "dummy_array", core_block, num_rows=self.row_size, num_cols=self.column_size, name_template="bit_r{0}_c{1}")
        self.pattern.connect_array()

    def add_pins(self):
        # bitline pins are not added because they are floating
        for bl_name in self.get_bitline_names():
            self.add_pin(bl_name, "INOUT")
        # bitline pins are not added because they are floating
        for wl_name in self.get_wordline_names():
            self.add_pin(wl_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def input_load(self):
        # FIXME: This appears to be old code from previous characterization. Needs to be updated.
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()
