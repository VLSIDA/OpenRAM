    #!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram.base import geometry
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS
from openram.modules.col_cap_array import col_cap_array  
from .sky130_bitcell_base_array import sky130_bitcell_base_array
from openram.modules import pattern
from math import ceil

class sky130_col_cap_array(col_cap_array, sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, location="", name=""):
        super().__init__(rows, cols, column_offset=column_offset, mirror=mirror, location=location, name=name)

    def add_modules(self):
        """ Add the modules used in this design """
        if self.location == "top":
            self.colend1 = factory.create(module_type="col_cap", version="colend")
            self.colend2 = factory.create(module_type="col_cap", version="colend_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colend_cent")
        elif self.location == "bottom":
            self.colend1 = factory.create(module_type="col_cap", version="colenda")
            self.colend2 = factory.create(module_type="col_cap", version="colenda_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colenda_cent")

        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        self.all_inst={}
        self.cell_inst={}
        
        if self.location == "top":
            bit_row = [geometry.instance("00_colend", mod=self.colend1, is_bitcell=True)] \
                    + [geometry.instance("01_strap_p_cent", mod=self.colend2, is_bitcell=False)]\
                    + [geometry.instance("02_colend", mod=self.colend1, is_bitcell=True, mirror="MY")] \
                    + [geometry.instance("03_strap_p", mod=self.colend3, is_bitcell=False)]
        elif self.location == "bottom":
            bit_row = [geometry.instance("00_colend", mod=self.colend1, is_bitcell=True, mirror="MX")] \
                    + [geometry.instance("01_strap_p_cent", mod=self.colend2, is_bitcell=False, mirror="MX")]\
                    + [geometry.instance("02_colend", mod=self.colend1, is_bitcell=True, mirror="XY")] \
                    + [geometry.instance("03_strap_p", mod=self.colend3, is_bitcell=False, mirror="MX")]

        bit_row = pattern.rotate_list(bit_row, self.column_offset * 2)
        bit_block = []
        pattern.append_row_to_block(bit_block, bit_row)
        self.pattern = pattern(self, "col_cap_array_" + self.location , bit_block, num_rows=self.row_size, num_cols=self.column_size, num_cores_x=ceil(self.column_size/2), num_cores_y=ceil(self.row_size/2), name_template="col_cap_array" + self.location + "_r{0}_c{1}")
        self.pattern.connect_array()
        
 
    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.append("vdd") # vdd
        bitcell_pins.append("gnd") # gnd
        bitcell_pins.append("vdd") # vpb
        bitcell_pins.append("gnd") # vnb
        #bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])

        return bitcell_pins
    
    def get_strap_pins(self, row, col):
        
        strap_pins = []
        if col % 2 == 0 and col % 4 != 0:
            strap_pins.append("vdd") # vdd
        else:
            strap_pins.append("gnd") # gnd
        strap_pins.append("vdd") # vpb
        strap_pins.append("gnd") # vnb
        
        return strap_pins
    
    def create_layout(self):

        self.place_array()
        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()
