# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import bitcell_base_array
from globals import OPTS
from sram_factory import factory
from vector import vector
import debug

class local_bitcell_array(bitcell_base_array.bitcell_base_array):
    """
    A local bitcell array is a bitcell array with a wordline driver.
    This can either be a single aray on its own if there is no hierarchical WL
    or it can be combined into a larger array with hierarchical WL.
    """
    def __init__(self, rows, cols, ports, left_rbl=0, right_rbl=0, add_replica=True, name=""):
        super().__init__(name, rows, cols, 0)
        debug.info(2, "create local array of size {} rows x {} cols words".format(rows,
                                                                                  cols + left_rbl + right_rbl))

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
                                       rows=self.rows + len(self.all_ports),
                                       cols=self.cols)
        self.add_mod(self.wl_array)

    def add_pins(self):

        self.bitline_names = self.bitcell_array.get_all_bitline_names()
        self.add_pin_list(self.bitline_names, "INOUT")
        self.wordline_names = self.bitcell_array.get_all_wordline_names()
        self.add_pin_list(self.wordline_names, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_instances(self):
        """ Create the module instances used in this design """

        internal_wl_names = [x + "i" for x in self.wordline_names]
        self.wl_inst = self.add_inst(name="wl_driver",
                                     mod=self.wl_array)
        self.connect_inst(self.wordline_names + internal_wl_names + ["vdd", "gnd"])

        self.array_inst = self.add_inst(name="array",
                                        mod=self.bitcell_array,
                                        offset=self.wl_inst.lr())
        self.connect_inst(self.bitline_names + internal_wl_names + ["vdd", "gnd"])

    def place(self):
        """ Place the bitcelll array to the right of the wl driver. """

        self.wl_inst.place(vector(0, 0))
        self.array_inst.place(self.wl_inst.lr())

        self.height = self.bitcell_array.height
        self.width = self.array_inst.rx()

    def add_layout_pins(self):

        for (x, y) in zip(self.bitline_names, self.bitcell_array.get_inouts()):
            self.copy_layout_pin(self.array_inst, y, x)

        for (x, y) in zip(self.wordline_names, self.wl_array.get_inputs()):
            self.copy_layout_pin(self.wl_inst, y, x)

            
