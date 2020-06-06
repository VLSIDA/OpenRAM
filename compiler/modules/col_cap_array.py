# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
from bitcell_base_array import bitcell_base_array
from sram_factory import factory
from globals import OPTS
from tech import cell_properties


class col_cap_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, cols, rows, column_offset=0, mirror=0, name=""):
        super().__init__(cols, rows, name, column_offset)
        self.mirror = mirror

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        self.dummy_cell = factory.create(module_type="col_cap_{}".format(OPTS.bitcell))
        self.add_mod(self.dummy_cell)

        self.cell = factory.create(module_type="bitcell")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row,col]=self.add_inst(name=name,
                                                      mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(col, row))

    def get_bitcell_pins(self, col, row):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """

        pin_name = cell_properties.bitcell.cell_1rw1r.pin
        bitcell_pins = ["{0}_{1}".format(pin_name.bl0, col),
                        "{0}_{1}".format(pin_name.br0, col),
                        "{0}_{1}".format(pin_name.bl1, col),
                        "{0}_{1}".format(pin_name.br1, col),
                        "vdd"]

        return bitcell_pins

    def add_layout_pins(self):
        """ Add the layout pins """

        column_list = self.cell.get_all_bitline_names()

        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[0,col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1,0),
                                    width=bl_pin.width(),
                                    height=self.height)

        # Add vdd/gnd via stacks
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_power_pin(name=pin.name,
                                           loc=pin.center(),
                                           start_layer=pin.layer)


    # def input_load(self):
    #     wl_wire = self.gen_wl_wire()
    #     return wl_wire.return_input_cap()
    #
    # def get_wordline_cin(self):
    #     """Get the relative input capacitance from the wordline connections in all the bitcell"""
    #     #A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
    #     bitcell_wl_cin = self.cell.get_wl_cin()
    #     total_cin = bitcell_wl_cin * self.column_size
    #     return total_cin
