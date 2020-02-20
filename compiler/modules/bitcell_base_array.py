# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from tech import cell_properties

class bitcell_base_array(design.design):
    """
    Abstract base class for bitcell-arrays -- bitcell, dummy
    """
    def __init__(self, cols, rows, name, column_offset):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows
        self.column_offset = column_offset

    def get_all_bitline_names(self):

        res = list()
        bitline_names = self.cell.get_all_bitline_names()

        # We have to keep the order of self.pins, otherwise we connect
        # it wrong in the spice netlist
        for pin in self.pins:
            for bl_name in bitline_names:
                if bl_name in pin:
                    res.append(pin)
        return res

    def get_all_wordline_names(self):

        res = list()
        wordline_names = self.cell.get_all_wl_names()

        # We have to keep the order of self.pins, otherwise we connect
        # it wrong in the spice netlist
        for pin in self.pins:
            for wl_name in wordline_names:
                if wl_name in pin:
                    res.append(pin)
        return res

    def add_pins(self):
        row_list = self.cell.get_all_wl_names()
        column_list = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for cell_column in column_list:
                self.add_pin(cell_column+"_{0}".format(col), "INOUT")
        for row in range(self.row_size):
            for cell_row in row_list:
                    self.add_pin(cell_row+"_{0}".format(row), "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def get_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """

        bitcell_pins = []

        pin_names = self.cell.get_all_bitline_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(col))
        pin_names = self.cell.get_all_wl_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def add_layout_pins(self):
        """ Add the layout pins """

        row_list = self.cell.get_all_wl_names()
        column_list = self.cell.get_all_bitline_names()

        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[0,col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1,0),
                                    width=bl_pin.width(),
                                    height=self.height)

        for row in range(self.row_size):
            for cell_row in row_list:
                wl_pin = self.cell_inst[row,0].get_pin(cell_row)
                self.add_layout_pin(text=cell_row+"_{0}".format(row),
                                    layer=wl_pin.layer,
                                    offset=wl_pin.ll().scale(0,1),
                                    width=self.width,
                                    height=wl_pin.height())

        # For every second row and column, add a via for gnd and vdd
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_power_pin(name=pin_name, loc=pin.center(), vertical=True, start_layer=pin.layer)

    def _adjust_x_offset(self, xoffset, col, col_offset):
        tempx = xoffset
        dir_y = False
        # If we mirror the current cell on the y axis adjust the x position
        if cell_properties.bitcell.mirror.y and (col + col_offset) % 2:
            tempx = xoffset + self.cell.width
            dir_y = True
        return (tempx, dir_y)

    def _adjust_y_offset(self, yoffset, row, row_offset):
        tempy = yoffset
        dir_x = False
        # If we mirror the current cell on the x axis adjust the y position
        if cell_properties.bitcell.mirror.x and (row + row_offset) % 2:
            tempy = yoffset + self.cell.height
            dir_x = True
        return (tempy, dir_x)


    def place_array(self, name_template, row_offset=0):
        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size*self.cell.height
        self.width = self.column_size*self.cell.width

        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = 0.0
            tempx, dir_y = self._adjust_x_offset(xoffset, col, self.column_offset)

            for row in range(self.row_size):
                name = name_template.format(row, col)
                tempy, dir_x = self._adjust_y_offset(yoffset, row, row_offset)

                if dir_x and dir_y:
                    dir_key = "XY"
                elif dir_x:
                    dir_key = "MX"
                elif dir_y:
                    dir_key = "MY"
                else:
                    dir_key = ""

                self.cell_inst[row,col].place(offset=[tempx, tempy],
                                              mirror=dir_key)
                yoffset += self.cell.height
            xoffset += self.cell.width
