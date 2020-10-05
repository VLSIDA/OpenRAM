# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California
# All rights reserved.
#
import design
from sram_factory import factory
from globals import OPTS
from tech import cell_properties


class s8_col_cap_array(design.design):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, location, column_offset=0, mirror=0, name=""):
        super().__init__(name)
        self.rows = rows
        self.cols = cols
        self.location = location
        self.column_offset = column_offset
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

        self.place_array("col_cap_r{0}_c{1}", self.mirror)
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        if self.location == "top":
            self.colend1 = factory.create(module_type="s8_col_end", version = "colend")
            self.add_mod(self.colend1)
            self.colend2 = factory.create(module_type="s8_col_end", version = "colend_p_cent")
            self.add_mod(self.colend2)
        elif self.location == "bottom":
            self.colend1 = factory.create(module_type="s8_col_end", version = "colenda")
            self.add_mod(self.colend1)
            self.colend2 = factory.create(module_type="s8_col_end", version = "colenda_p_cent")
            self.add_mod(self.colend2)

        self.cell = factory.create(module_type="s8_bitcell", version = "opt1")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        self.array_layout = []
        alternate_bitcell = 0
        for col in range((self.cols * 2 )-1):
            row_layout = []
            name="rca_{0}".format(col)
            # Top/bottom cell are always dummy cells.
            # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
            # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.
            if alternate_bitcell == 0:
                row_layout.append(self.colend1)
                self.cell_inst[col]=self.add_inst(name=name, mod=self.colend1)
                #self.connect_inst(self.get_bitcell_pins(row, 0))
                alternate_bitcell = 1

            else:
                row_layout.append(self.colend2)
                self.cell_inst[col]=self.add_inst(name=name,mod=self.colend2)
                #self.connect_inst(self.get_bitcell_pins(row, 0))
                alternate_bitcell = 0

            self.array_layout.append(row_layout)


    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        pin_name = cell_properties.bitcell.cell_6t.pin
        bitcell_pins = ["{0}_{1}".format(pin_name.bl0, col),
                        "{0}_{1}".format(pin_name.br0, col),
                        "vdd"]

        return bitcell_pins

    def place_array(self, name_template, row_offset=0):
        self.height = self.colend1.height
        self.width = (self.colend1.width + self.colend2.width) * self.cols - self.colend2.width

        yoffset = 0.0
        xoffset = 0.0   
        for row in range(0, len(self.array_layout)):
            inst = self.insts[row]
            inst.place(offset=[xoffset, yoffset])
            xoffset += inst.width

    def add_pins(self):
        for row in range(self.cols):
            for port in self.all_ports:
                self.add_pin("bl{}_{}".format(port, row), "OUTPUT")
                self.add_pin("br{}_{}".format(port, row), "OUTPUT")
        self.add_pin("vpwr", "POWER")
        self.add_pin("vgnd", "GROUND")

    def add_layout_pins(self):
        """ Add the layout pins """
        return
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

