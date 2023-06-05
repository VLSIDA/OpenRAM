# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.sram_factory import factory
from openram import OPTS


class bitcell_base_array(design):
    """
    Abstract base class for bitcell-arrays -- bitcell, dummy, replica
    """
    def __init__(self, name, rows, cols, column_offset):
        super().__init__(name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))

        self.column_size = cols
        self.row_size = rows
        self.column_offset = column_offset

        # Bitcell for port names only
        self.cell = factory.create(module_type=OPTS.bitcell)

        self.wordline_names = [[] for port in self.all_ports]
        self.all_wordline_names = []
        self.bitline_names = [[] for port in self.all_ports]
        self.all_bitline_names = []
        self.rbl_bitline_names = [[] for port in self.all_ports]
        self.all_rbl_bitline_names = []
        self.rbl_wordline_names = [[] for port in self.all_ports]
        self.all_rbl_wordline_names = []

    def create_all_bitline_names(self):
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col),
                                                 "br_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]

    def create_all_wordline_names(self, row_size=None, start_row=0):
        if row_size == None:
            row_size = self.row_size

        for row in range(start_row, row_size):
            for port in self.all_ports:
                self.wordline_names[port].append("wl_{0}_{1}".format(port, row))

        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]

    def add_pins(self):
        for bl_name in self.get_bitline_names():
            self.add_pin(bl_name, "INOUT")
        for wl_name in self.get_wordline_names():
            self.add_pin(wl_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def get_bitcell_pins(self, row, col):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def get_rbl_wordline_names(self, port=None):
        """
        Return the WL for the given RBL port.
        """
        if port == None:
            return self.all_rbl_wordline_names
        else:
            return self.rbl_wordline_names[port]

    def get_rbl_bitline_names(self, port=None):
        """ Return all the BL for the given RBL port """
        if port == None:
            return self.all_rbl_bitline_names
        else:
            return self.rbl_bitline_names[port]

    def get_bitline_names(self, port=None):
        """ Return the regular bitlines for the given port or all"""
        if port == None:
            return self.all_bitline_names
        else:
            return self.bitline_names[port]

    def get_all_bitline_names(self, port=None):
        """ Return ALL the bitline names (including rbl) """
        temp = []
        temp.extend(self.get_rbl_bitline_names(0))
        if port == None:
            temp.extend(self.all_bitline_names)
        else:
            temp.extend(self.bitline_names[port])
        if len(self.all_ports) > 1:
            temp.extend(self.get_rbl_bitline_names(1))
        return temp

    def get_wordline_names(self, port=None):
        """ Return the regular wordline names """
        if port == None:
            return self.all_wordline_names
        else:
            return self.wordline_names[port]

    def get_all_wordline_names(self, port=None):
        """ Return all the wordline names """
        temp = []
        temp.extend(self.get_rbl_wordline_names(0))
        if port == None:
            temp.extend(self.all_wordline_names)
        else:
            temp.extend(self.wordline_names[port])
        if len(self.all_ports) > 1:
            temp.extend(self.get_rbl_wordline_names(1))
        return temp

    def add_bitline_pins(self):
        bitline_names = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for port in self.all_ports:
                bl_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port])
                self.add_layout_pin(text="bl_{0}_{1}".format(port, col),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)
                br_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port + 1])
                self.add_layout_pin(text="br_{0}_{1}".format(port, col),
                                    layer=br_pin.layer,
                                    offset=br_pin.ll().scale(1, 0),
                                    width=br_pin.width(),
                                    height=self.height)
    def add_wl_pins(self):
        wl_names = self.cell.get_all_wl_names()
        for row in range(self.row_size):
            for port in self.all_ports:
                wl_pin = self.cell_inst[row, 0].get_pin(wl_names[port])
                self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0, 1),
                                    width=self.width,
                                    height=wl_pin.height())

    def route_supplies(self):
        for inst in self.cell_inst.values():
            for pin_name in ["vdd", "gnd"]:
                self.copy_layout_pin(inst, pin_name)

    def add_layout_pins(self):
        """ Add the layout pins """
        self.add_bitline_pins()
        self.add_wl_pins()

    def _adjust_x_offset(self, xoffset, col, col_offset):
        tempx = xoffset
        dir_y = False
        # If we mirror the current cell on the y axis adjust the x position
        if self.cell.mirror.y and (col + col_offset) % 2:
            tempx = xoffset + self.cell.width
            dir_y = True
        return (tempx, dir_y)

    def _adjust_y_offset(self, yoffset, row, row_offset):
        tempy = yoffset
        dir_x = False
        # If we mirror the current cell on the x axis adjust the y position
        if self.cell.mirror.x and (row + row_offset) % 2:
            tempy = yoffset + self.cell.height
            dir_x = True
        return (tempy, dir_x)

    def place_array(self, name_template, row_offset=0):
        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size * self.cell.height
        self.width = self.column_size * self.cell.width

        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = 0.0
            tempx, dir_y = self._adjust_x_offset(xoffset, col, self.column_offset)

            for row in range(self.row_size):
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

    def get_column_offsets(self):
        """
        Return an array of the x offsets of all the regular bits
        """
        offsets = [self.cell_inst[0, col].lx() for col in range(self.column_size)]
        return offsets
