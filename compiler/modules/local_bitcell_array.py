# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from bitcell_base_array import bitcell_base_array
from tech import drc, spice
from globals import OPTS
from sram_factory import factory


class local_bitcell_array(bitcell_base_array):
    """
    A local wordline array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, name, rows, cols):
        super().__init__(name, rows, cols)

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

    def create_layout(self):

        self.place_array("bit_r{0}_c{1}")

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.bit_array = factory.create(module_type="bitcell_array",
                                        rows=self.rows,
                                        cols=self.cols,
                                        column_offset=self.column_offset)
        self.add_mod(self.bit_array)

        self.wl_array = factory.create(module_type="wordline_driver_array",
                                       rows=self.rows,
                                       cols=self.cols)
        self.add_mod(self.wl_array)
        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.bitcell_inst = self.add_inst(mod=self.bitcell_array)
        self.connect_inst(self.get_bitcell_pins(row, col))
        self.wl_inst = self.add_inst(mod=self.wl_array)
        self.connect_inst(self.get_bitcell_pins(row, col))
        
