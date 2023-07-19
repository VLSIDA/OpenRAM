# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
import math
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import drc
from openram.tech import cell_properties
from openram.tech import layer_properties as layer_props
from openram import OPTS


class column_decoder(design):
    """
    Create the column mux decoder.
    """

    def __init__(self, name, col_addr_size):
        super().__init__(name)

        self.col_addr_size = col_addr_size
        self.num_inputs = col_addr_size
        self.num_outputs = pow(2, col_addr_size)
        debug.info(2,
                   "create column decoder of {0} inputs and {1} outputs".format(self.num_inputs,
                                                                                self.num_outputs))

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            self.DRC_LVS()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_instances()

    def create_instances(self):
        self.column_decoder_inst = self.add_inst(name="column_decoder",
                                                 mod=self.column_decoder)
        self.connect_inst(list(self.pins))

    def create_layout(self):
        self.column_decoder_inst.place(vector(0,0))

        self.width = self.column_decoder_inst.width
        self.height = self.column_decoder_inst.height

        self.route_layout()


    def add_pins(self):
        """ Add the module pins """

        for i in range(self.num_inputs):
            self.add_pin("in_{0}".format(i), "INPUT")

        for j in range(self.num_outputs):
            self.add_pin("out_{0}".format(j), "OUTPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def route_layout_pins(self):
        """ Add the pins. """

        if self.col_addr_size == 1:
            self.copy_layout_pin(self.column_decoder_inst, "A", "in_0")
            self.copy_layout_pin(self.column_decoder_inst, "Zb", "out_0")
            self.copy_layout_pin(self.column_decoder_inst, "Z", "out_1")
        elif self.col_addr_size > 1:
            for i in range(self.num_inputs):
                self.copy_layout_pin(self.column_decoder_inst, "in_{0}".format(i))

            for i in range(self.num_outputs):
                self.copy_layout_pin(self.column_decoder_inst, "out_{0}".format(i))

    def route_layout(self):
        """ Create routing among the modules """
        self.route_layout_pins()
        self.route_supplies()

    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        if self.col_addr_size == 1:
            self.copy_layout_pin(self.column_decoder_inst, "vdd")
            self.copy_layout_pin(self.column_decoder_inst, "gnd")
        else:
            self.route_vertical_pins("vdd", self.insts, xside="rx",)
            self.route_vertical_pins("gnd", self.insts, xside="lx",)

    def add_modules(self):

        self.dff =factory.create(module_type="dff")

        if self.col_addr_size == 1:
            self.column_decoder = factory.create(module_type="pinvbuf",
                                                 height=self.dff.height)
        elif self.col_addr_size == 2:
            self.column_decoder = factory.create(module_type="hierarchical_predecode2x4",
                                                 column_decoder=True,
                                                 height=self.dff.height)

        elif self.col_addr_size == 3:
            self.column_decoder = factory.create(module_type="hierarchical_predecode3x8",
                                                 column_decoder=True,
                                                 height=self.dff.height)
        elif self.col_addr_size == 4:
            self.column_decoder = factory.create(module_type="hierarchical_predecode4x16",
                                                 column_decoder=True,
                                                 height=self.dff.height)
        else:
            # No error checking before?
            debug.error("Invalid column decoder?", -1)

