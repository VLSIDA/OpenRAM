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
import debug

class global_bitcell_array(bitcell_base_array):
    """
    Creates a global bitcell array with a number
    of local arrays of a sizes given by a tuple in the list.
    """
    def __init__(self, sizes, name=""):
        # Each bank will have the same number of rows
        self.rows = sizes[0][0]
        for (r, c) in sizes:
            debug.check(r[0] == self.rows, "Cannot have non-uniform number of rows in global array.")
        # The total of all columns will be the number of columns
        self.cols = sum(x[1] for x in sizes)
        self.sizes = sizes
        super().__init__(rows=self.rows, cols=self.cols, name=name)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place()

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.local_mods = []
        for (row, col) in self.sizes:
            la = factory.create(module_type="local_bitcell_array", rows=row, cols=col)
            self.add_mod(la)
            self.local_mods.append(la)

    def create_instances(self):
        """ Create the module instances used in this design """
        self.local_inst = {}
        for i in range(self.sizes):
            name = "local_array_{0}".format(i)
                self.local_inst.append(self.add_inst(name=name,
                                                     mod=self.local_mods[i])
                self.connect_inst(self.get_bitcell_pins(row, col))
        
 
