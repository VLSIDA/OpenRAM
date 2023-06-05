#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import geometry
from openram.modules import bitcell_base_array
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS


class sky130_bitcell_base_array(bitcell_base_array):
    """
    Abstract base class for bitcell-arrays -- bitcell, dummy, replica
    """
    def __init__(self, name, rows, cols, column_offset):
        super().__init__(name, rows, cols, column_offset)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))

        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def place_array(self, name_template, row_offset=0, col_offset=0):
        yoffset = 0.0

        for row in range(0, len(self.array_layout)):
            xoffset = 0.0
            for col in range(0, len(self.array_layout[row])):
                self.place_inst = self.insts[(col) + (row) * len(self.array_layout[row])]

                if row % 2 == 0:
                    if col == 0:
                        self.place_inst.place(offset=[xoffset, yoffset + self.cell.height], mirror="MX")
                    elif col % 4 == 0:
                        self.place_inst.place(offset=[xoffset, yoffset + self.cell.height], mirror="MX")
                    elif col % 4 == 3 :
                        self.place_inst.place(offset=[xoffset, yoffset + self.cell.height], mirror="MX")
                    elif col % 4 == 2:
                        self.place_inst.place(offset=[xoffset + self.cell.width, yoffset + self.cell.height], mirror="XY")
                    else:
                        self.place_inst.place(offset=[xoffset, yoffset + self.cell.height], mirror="MX")
                else:
                    if col == 0:
                        self.place_inst.place(offset=[xoffset, yoffset])
                    elif col % 4 == 0:
                        self.place_inst.place(offset=[xoffset, yoffset])
                    elif col % 4 == 3 :
                        self.place_inst.place(offset=[xoffset, yoffset])
                    elif col % 4 == 2:
                        self.place_inst.place(offset=[xoffset + self.cell.width, yoffset], mirror="MY")
                        # self.place_inst.place(offset=[xoffset, yoffset])
                    else:
                        self.place_inst.place(offset=[xoffset, yoffset])

                xoffset += self.place_inst.width
            yoffset += self.place_inst.height

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

    def get_bitcell_pins(self, row, col, swap = False):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        bitcell_pins = []
        for port in self.all_ports:
            bitcell_pins.extend([x for x in self.get_bitline_names(port) if x.endswith("_{0}".format(col))])
        bitcell_pins.append("gnd") # gnd
        bitcell_pins.append("vdd") # vdd
        bitcell_pins.append("vdd") # vpb
        bitcell_pins.append("gnd") # vnb
        bitcell_pins.extend([x for x in self.all_wordline_names if x.endswith("_{0}".format(row))])

        return bitcell_pins

    def get_strap_pins(self, row, col, name=""):
        """
        Creates a list of connections in the strap cell,
        indexed by column and row, for instance use in bitcell_array
        """
        if name and "_p" in name:
            strap_pins = ["gnd"]
        else:
            strap_pins = ["vdd"]
        return strap_pins

    def get_col_cap_p_pins(self, row, col):
        """
        """
        strap_pins = ["gnd", "vdd", "gnd"]
        return strap_pins

    def get_col_cap_pins(self, row, col):
        """
        """
        strap_pins = []
        for port in self.all_ports:
            strap_pins.extend([x for x in self.get_bitline_names(port) if "bl" in x and x.endswith("_{0}".format(col))])
        strap_pins.extend(["vdd", "gnd"])
        for port in self.all_ports:
            strap_pins.extend([x for x in self.get_bitline_names(port) if "br" in x and x.endswith("_{0}".format(col))])
        if row == 0:
            strap_pins.extend(["top_gate"])
        else:
            strap_pins.extend(["bot_gate"])
        strap_pins.extend(["vdd", "gnd"])
        return strap_pins

    def get_row_cap_pins(self, row, col):
        """
        """
        strap_pins = ["gnd", "vdd", "gnd"]
        return strap_pins

    def get_corner_pins(self):
        """
        """
        strap_pins = ["vdd", "gnd", "vdd"]
        return strap_pins

    def add_supply_pins(self):
        """ Add the layout pins """
        # Copy a vdd/gnd layout pin from every cell

        for inst in self.insts:
            if "wlstrap" in inst.name:
                if "VPWR" in inst.mod.pins:
                    self.copy_layout_pin(inst, "VPWR", "vdd")
                if "VGND" in inst.mod.pins:
                    self.copy_layout_pin(inst, "VGND", "gnd")

        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row, col]
                for pin_name in ["vdd", "gnd"]:
                    self.copy_layout_pin(inst, pin_name)

                if row == 2: #add only 1 label per col

                    if 'VPB' or 'vpb' in self.cell_inst[row, col].mod.pins:
                        pin = inst.get_pin("vpb")
                        self.objs.append(geometry.rectangle(layer["nwell"],
                                                            pin.ll(),
                                                            pin.width(),
                                                            pin.height()))
                        self.objs.append(geometry.label("vdd", layer["nwell"], pin.center()))

                    if 'VNB' or 'vnb'in self.cell_inst[row, col].mod.pins:
                        try:
                            from openram.tech import layer_override
                            if layer_override['VNB']:
                                pin = inst.get_pin("vnb")
                                self.objs.append(geometry.label("gnd", layer["pwellp"], pin.center()))
                                self.objs.append(geometry.rectangle(layer["pwellp"],
                                                                    pin.ll(),
                                                                    pin.width(),
                                                                    pin.height()))
                        except:
                            pin = inst.get_pin("vnb")
                            self.add_label("vdd", pin.layer, pin.center())

    def add_bitline_pins(self):
        bitline_names = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for port in self.all_ports:
                bl_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port])
                text = "bl_{0}_{1}".format(port, col)
                #if "Y" in self.cell_inst[0, col].mirror:
                #    text = text.replace("bl", "br")
                self.add_layout_pin(text=text,
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)
                br_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port + 1])
                text = "br_{0}_{1}".format(port, col)
                #if "Y" in self.cell_inst[0, col].mirror:
                #    text = text.replace("br", "bl")
                self.add_layout_pin(text=text,
                                    layer=br_pin.layer,
                                    offset=br_pin.ll().scale(1, 0),
                                    width=br_pin.width(),
                                    height=self.height)
