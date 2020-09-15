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
from sram_factory import factory
from globals import OPTS


class bitcell_base_array(design.design):
    """
    Abstract base class for bitcell-arrays -- bitcell, dummy, replica
    """
    def __init__(self, name, rows, cols, column_offset):
        super().__init__(name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows
        self.column_offset = column_offset

        # Bitcell for port names only
        if OPTS.tech_name != "sky130":
            self.cell = factory.create(module_type="bitcell")
        else:
            self.cell = factory.create(module_type="s8_bitcell", version="opt1")
            self.cell2 = factory.create(module_type="s8_bitcell", version="opt1a")
            self.strap = factory.create(module_type="s8_internal", version="wlstrap")
            self.strap2 = factory.create(module_type="s8_internal", version="wlstrap_p")

        self.create_all_bitline_names()
        self.create_all_wordline_names()

    def get_all_bitline_names(self, prefix=""):
        return [prefix + x for x in self.all_bitline_names]

    def create_all_bitline_names(self):
        self.bitline_names = [[] for port in self.all_ports]
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col),
                                                 "br_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]
                
    def get_all_wordline_names(self, prefix=""):
        return [prefix + x for x in self.all_wordline_names]

    def create_all_wordline_names(self):
        self.wordline_names = [[] for port in self.all_ports]
        for row in range(self.row_size):
            for port in self.all_ports:
                if not cell_properties.bitcell.split_wl:
                    self.wordline_names[port].append("wl_{0}_{1}".format(port, row))
                else:
                    self.wordline_names[port].append("wl0_{0}_{1}".format(port, row))
                    self.wordline_names[port].append("wl1_{0}_{1}".format(port, row))
        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]
        
    def get_bitline_names(self, port=None):
        if port == None:
            return self.all_bitline_names
        else:
            return self.bitline_names[port]
        
    def get_wordline_names(self, port=None):
        if port == None:
            return self.all_wordline_names
        else:
            return self.wordline_names[port]
        
    def add_pins(self):
        if OPTS.tech_name != "sky130":
            for bl_name in self.get_bitline_names():
                self.add_pin(bl_name, "INOUT")
            for wl_name in self.get_wordline_names():
                self.add_pin(wl_name, "INPUT")
            self.add_pin("vdd", "POWER")
            self.add_pin("gnd", "GROUND")
        else:
            for bl_name in self.get_bitline_names():
                self.add_pin(bl_name, "INOUT")
            for wl_name in self.get_wordline_names():
                self.add_pin(wl_name, "INPUT")
            self.add_pin("vpwr", "POWER")
            self.add_pin("vgnd", "GROUND")
    def get_bitcell_pins(self, row, col):
        """ Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")

        return bitcell_pins

    def add_layout_pins(self):
        """ Add the layout pins """
        if OPTS.tech_name != "sky130":
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

            wl_names = self.cell.get_all_wl_names()
            for row in range(self.row_size):
                for port in self.all_ports:
                    wl_pin = self.cell_inst[row, 0].get_pin(wl_names[port])
                    self.add_layout_pin(text="wl_{0}_{1}".format(port, row),
                                        layer=wl_pin.layer,
                                        offset=wl_pin.ll().scale(0, 1),
                                        width=self.width,
                                        height=wl_pin.height())

            # Copy a vdd/gnd layout pin from every cell
            for row in range(self.row_size):
                for col in range(self.column_size):
                    inst = self.cell_inst[row, col]
                    for pin_name in ["vdd", "gnd"]:
                        self.copy_layout_pin(inst, pin_name)
        else:
            bitline_names = self.cell.get_all_bitline_names()
            for col in range(self.column_size):
                for port in self.all_ports:
                    bl_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port])
                    self.add_layout_pin(text="bl0_{0}_{1}".format(port, col),
                                        layer=bl_pin.layer,
                                        offset=bl_pin.ll().scale(1, 0),
                                        width=bl_pin.width(),
                                        height=self.height)
                    br_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port + 1])
                    self.add_layout_pin(text="bl1_{0}_{1}".format(port, col),
                                        layer=br_pin.layer,
                                        offset=br_pin.ll().scale(1, 0),
                                        width=br_pin.width(),
                                        height=self.height)

            wl_names = self.cell.get_all_wl_names()
            for row in range(self.row_size):
                for port in self.all_ports:
                    wl0_pin = self.cell_inst[row, 0].get_pin(wl_names[port])
                    self.add_layout_pin(text="wl0_{0}_{1}".format(port, row),
                                        layer=wl0_pin.layer,
                                        offset=wl0_pin.ll().scale(0, 1),
                                        width=self.width,
                                        height=wl0_pin.height())
                    wl1_pin = self.cell_inst[row, 0].get_pin(wl_names[port])
                    self.add_layout_pin(text="wl1_{0}_{1}".format(port, row),
                                        layer=wl1_pin.layer,
                                        offset=wl1_pin.ll().scale(0, 1),
                                        width=self.width,
                                        height=wl1_pin.height())
            # Copy a vdd/gnd layout pin from every cell
            for row in range(self.row_size):
                for col in range(self.column_size):
                    inst = self.cell_inst[row, col]
                    for pin_name in ["vpwr", "vgnd"]:

                        self.copy_layout_pin(inst, pin_name)
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
        if OPTS.tech_name != "sky130":
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
        else:
            array_layout = []
            for y in range(0,self.row_size):

                row_layout = []
                alternate_bitcell = 1
                alternate_strap = 1
                for x in range(0,self.column_size):
                    if alternate_bitcell == 1:
                        row_layout.append(self.cell)
                        alternate_bitcell = 0
                    else:
                        row_layout.append(self.cell2)
                        alternate_bitcell = 1
                    if x != self.column_size:
                        if alternate_strap:
                            row_layout.append(self.strap2)
                            alternate_strap = 0
                        else:
                            
                            row_layout.append(self.strap)
                            alternate_strap = 1
                array_layout.append(row_layout)

            self.height = self.row_size * self.cell.height + (self.row_size - 1) * self.strap.height
            self.width = self.column_size * self.cell.width + (self.column_size-1) * self.strap.width
            

            yoffset = 0.0

            for row in range(0, len(array_layout)):
                xoffset = 0.0               
                for col in range(0, len(array_layout[row])):
                    inst = self.add_inst(name = "row_{}, col_{}".format(row,col), mod=array_layout[row][col])
                    inst.place(offset=[xoffset, yoffset])
                    xoffset += inst.width
                yoffset += self.cell.height
                