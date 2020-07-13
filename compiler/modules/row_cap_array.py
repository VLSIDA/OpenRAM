# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
from bitcell_base_array import bitcell_base_array
from sram_factory import factory
from globals import OPTS
from tech import cell_properties


class row_cap_array(bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, cols, rows, column_offset=0, mirror=0, name=""):
        super().__init__(cols, rows, name, column_offset)
        self.mirror = mirror
        self.no_instances = True
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
        self.dummy_cell = factory.create(module_type="row_cap_{}".format(OPTS.bitcell))
        self.add_mod(self.dummy_cell)

        self.cell = factory.create(module_type="bitcell")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(1, self.row_size - 1):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(col, row))

    def get_bitcell_pins(self, col, row):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """

        pin_name = cell_properties.bitcell.cell_1rw1r.pin
        bitcell_pins = ["{0}_{1}".format(pin_name.wl0, row),
                        "{0}_{1}".format(pin_name.wl1, row),
                        "gnd"]

        return bitcell_pins

    def place_array(self, name_template, row_offset=0):
        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size * self.cell.height
        self.width = self.column_size * self.cell.width

        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = self.cell.height
            tempx, dir_y = self._adjust_x_offset(xoffset, col, self.column_offset)

            for row in range(1, self.row_size - 1):
                tempy, dir_x = self._adjust_y_offset(yoffset, row, row_offset)

                if dir_x and dir_y:
                    dir_key = "XY"
                elif dir_x:
                    dir_key = "MX"
                elif dir_y:
                    dir_key = "MY"
                else:
                    dir_key = ""

                self.cell_inst[row, col].place(offset=[tempx, tempy],
                                               mirror=dir_key)
                yoffset += self.cell.height
            xoffset += self.cell.width

    def add_layout_pins(self):
        """ Add the layout pins """

        row_list = self.cell.get_all_wl_names()

        for row in range(1, self.row_size - 1):
            for cell_row in row_list:
                wl_pin = self.cell_inst[row, 0].get_pin(cell_row)
                self.add_layout_pin(text=cell_row + "_{0}".format(row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

        # Add vdd/gnd via stacks
        for row in range(1, self.row_size - 1):
            for col in range(self.column_size):
                inst = self.cell_inst[row, col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_power_pin(name=pin.name,
                                           loc=pin.center(),
                                           start_layer=pin.layer)

