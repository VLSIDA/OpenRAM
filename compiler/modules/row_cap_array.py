# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.sram_factory import factory
from openram import OPTS
from .bitcell_base_array import bitcell_base_array
from .pattern import pattern
from openram.base import geometry
from math import ceil

class row_cap_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, row_offset=0, mirror=0, location="", name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, row_offset=row_offset, name=name)
        self.mirror = mirror
        self.location = location
        self.row_offset = row_offset
        #self.no_instances = True
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        # This will create a default set of bitline/wordline names
        self.create_all_wordline_names()
        self.create_all_bitline_names()

        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array()
        self.add_layout_pins()

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.row_cap = factory.create(module_type="row_cap_{}".format(OPTS.bitcell))

        self.cell = factory.create(module_type=OPTS.bitcell)

    def create_instances(self):
        """ Create the module instances used in this design """
        self.all_inst={}
        self.cell_inst={}
        
        bit_block = []
        
        if self.location == "left":
            #top_corner = geometry.instance("row_cap_top_corner", mod=self.top_corner, is_bitcell=False, mirror="MY")
            #bottom_corner = geometry.instance("row_cap_bottom_corner", mod=self.bottom_corner, is_bitcell=False, mirror="XY")
            rowend = geometry.instance("row_cap_rowend", mod=self.row_cap, is_bitcell=True, mirror="")
            rowend_m = geometry.instance("row_cap_rowend_m", mod=self.row_cap, is_bitcell=True, mirror="MX")
        elif self.location == "right":
            #top_corner = geometry.instance("row_cap_top_corner", mod=self.top_corner, is_bitcell=False)
            #bottom_corner = geometry.instance("row_cap_bottom_corner", mod=self.bottom_corner, is_bitcell=False, mirror="MX")
            rowend = geometry.instance("row_cap_rowend", mod=self.row_cap, is_bitcell=True, mirror="MY")
            rowend_m = geometry.instance("row_cap_rowend_m", mod=self.row_cap, is_bitcell=True, mirror="XY")
        #pattern.append_row_to_block(bit_block, [top_corner])
        for row in range(0, self.row_size):
                if row % 2 == 1:
                    pattern.append_row_to_block(bit_block, [rowend])
                else:
                    pattern.append_row_to_block(bit_block, [rowend_m])

        #pattern.append_row_to_block(bit_block, [bottom_corner])
        if self.cell.has_corners is False:
            num_rows = self.row_size - 2
        else:
            num_rows = self.row_size
        self.pattern = pattern(self, "row_cap_array_" + self.location, bit_block, num_rows=num_rows, num_cols=self.column_size, num_cores_x=ceil(self.column_size/2), num_cores_y=ceil(self.row_size/2), name_template="row_cap_array" + self.location + "_r{0}_c{1}")
        self.pattern.connect_array_raw()

    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """

        bitcell_pins = ["wl0_{0}".format(row),
                        "wl1_{0}".format(row),
                        "gnd"]

        return bitcell_pins

    def add_layout_pins(self):
        """ Add the layout pins """

        wl_names = self.cell.get_all_wl_names()
        max_row = self.row_size - 2
        for row in range(0, max_row):
            for port in self.all_ports:
                wl_pin = self.cell_inst[max_row - 1 - row, 0].get_pin(wl_names[port])
                self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        for row in range(0, max_row):
            for col in range(self.column_size):
                inst = self.cell_inst[row, col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_layout_pin(text=pin_name,
                                            layer=pin.layer,
                                            offset=pin.ll(),
                                            width=pin.width(),
                                            height=pin.height())
