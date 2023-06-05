# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram.sram_factory import factory
from openram import OPTS
from .bitcell_base_array import bitcell_base_array


class col_cap_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, mirror=0, location="", name=""):
        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.mirror = mirror
        self.location = location

        self.no_instances = True
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        # This will create a default set of bitline/wordline names
        self.cell = factory.create(module_type=OPTS.bitcell)

        if not self.cell.end_caps:
            self.create_all_wordline_names()
        self.create_all_bitline_names()

        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)
        self.add_layout_pins()

        self.height = self.dummy_cell.height
        self.width = self.column_size * self.cell.width

        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.dummy_cell = factory.create(module_type="col_cap_{}".format(OPTS.bitcell))

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(row, col))

    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """

        if len(self.all_ports) == 1:
            bitcell_pins = ["bl0_{0}".format(col),
                            "br0_{0}".format(col),
                            "vdd"]
        else:
            bitcell_pins = ["bl0_{0}".format(col),
                            "br0_{0}".format(col),
                            "bl1_{0}".format(col),
                            "br1_{0}".format(col),
                            "vdd"]

        return bitcell_pins

    def add_layout_pins(self):
        """ Add the layout pins """

        column_list = self.cell.get_all_bitline_names()

        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[0, col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column + "_{0}".format(col),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)

        # Add vdd/gnd via stacks
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row, col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.copy_layout_pin(inst, pin_name)
