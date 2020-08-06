# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
from globals import OPTS
from sram_factory import factory
import debug


class local_bitcell_array(design.design):
    """
    A local bitcell array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, rows, cols, ports, left_rbl=0, right_rbl=0, name=""):
        design.design.__init__(self, name)
        debug.info(2, "create sram of size {0} with {1} words".format(self.word_size,
                                                                      self.num_words))

        self.rows = rows
        self.cols = cols
        self.left_rbl = left_rbl
        self.right_rbl = right_rbl
        self.all_ports = ports

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

        self.place()

        self.add_layout_pins()

        self.add_boundary()

        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        # This is just used for names
        self.cell = factory.create(module_type="bitcell")

        self.bitcell_array = factory.create(module_type="replica_bitcell_array",
                                            cols=self.cols,
                                            rows=self.rows,
                                            left_rbl=self.left_rbl,
                                            right_rbl=self.right_rbl,
                                            bitcell_ports=self.all_ports)
        self.add_mod(self.bitcell_array)

        self.wl_array = factory.create(module_type="wordline_buffer_array",
                                       rows=self.rows,
                                       cols=self.cols)
        self.add_mod(self.wl_array)

    def create_instances(self):
        """ Create the module instances used in this design """

        self.wl_inst = self.add_inst(mod=self.wl_array)
        self.connect_inst(self.pins)

        self.array_inst = self.add_inst(mod=self.bitcell_array,
                                        offset=self.wl_inst.lr())
        self.connect_inst(self.pins)
