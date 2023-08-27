#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram.base import geometry
from openram.sram_factory import factory
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array
from openram.modules.row_cap_array import row_cap_array
from openram.modules.pattern import pattern
from math import ceil

class sky130_row_cap_array(row_cap_array, sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, location="", name=""):
        super().__init__(rows, cols, column_offset=column_offset, location=location, name=name)
        self.mirror = mirror
        self.location = location
    def add_modules(self):
        """ Add the modules used in this design """
        if self.column_offset == 0:
            self.top_corner = factory.create(module_type="corner", location="ul")
            self.bottom_corner =factory.create(module_type="corner", location="ll")
            #self.rowend1 = factory.create(module_type="row_cap", version="rowend_replica")
            #self.rowend2 = factory.create(module_type="row_cap", version="rowenda_replica")

        else:
            self.top_corner = factory.create(module_type="corner", location="ur")
            self.bottom_corner = factory.create(module_type="corner", location="lr")

            #self.rowend1 = factory.create(module_type="row_cap", version="rowend")
            #self.rowend2 = factory.create(module_type="row_cap", version="rowenda")
        self.rowend = factory.create(module_type="row_cap", version="rowend")
        self.rowenda = factory.create(module_type="row_cap", version="rowenda")
        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        self.all_inst={}
        self.cell_inst={}
        
        bit_block = []
        top_corner = geometry.instance("row_cap_top_corner", mod=self.top_corner, is_bitcell=False, mirror="XY")
        bottom_corner = geometry.instance("row_cap_bottom_corner", mod=self.bottom_corner, is_bitcell=False)
        rowend = geometry.instance("row_cap_rowend", mod=self.rowend, is_bitcell=True)
        rowenda = geometry.instance("row_cap_rowenda", mod=self.rowenda, is_bitcell=True, mirror="XY")
        
        pattern.append_row_to_block(bit_block, [top_corner])
        for row in range(1,self.row_size-1):
            if row % 2 == 0:
                pattern.append_row_to_block(bit_block, [rowend])
            else:
                pattern.append_row_to_block(bit_block, [rowenda])
        pattern.append_row_to_block(bit_block, [bottom_corner])
        self.pattern = pattern(self, "row_cap_array_" + self.location, bit_block, num_rows=self.row_size, num_cols=self.column_size, num_cores_x=ceil(self.column_size/2), num_cores_y=ceil(self.row_size/2), name_template="row_cap_array" + self.location + "_r{0}_c{1}")
        self.pattern.connect_array_raw()
        
 
    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """

        bitcell_pins = []
        bitcell_pins.append("vdd") # vdd   
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])

        #bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])

        return bitcell_pins
    
    def get_strap_pins(self, row, col):
        
        strap_pins = []
        
        strap_pins.append("vdd") # vdd
        strap_pins.append("vdd") # vpb
        strap_pins.append("gnd") # vnb
        
        return strap_pins
        
    def create_all_wordline_names(self, row_size=None, start_row=0):
        if row_size == None:
            row_size = self.row_size
        row_size = row_size - 2
        for row in range(start_row, row_size):
            for port in self.all_ports:
                self.wordline_names[port].append("wl_{0}_{1}".format(port, row))

        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]
        
    def create_layout(self):

        self.place_array()
        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()
        
