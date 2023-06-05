#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram.base import geometry
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS
from .sky130_bitcell_base_array import sky130_bitcell_base_array

class sky130_col_cap_array(sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, location, column_offset=0, mirror=0, name=""):
        # Don't call the regular col-cap_array constructor since we don't want its constructor, just
        # some of it's useful member functions
        sky130_bitcell_base_array.__init__(self, rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.mirror = mirror
        self.location = location
        self.rows = rows
        self.cols = cols
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        # This module has no wordlines
        # self.create_all_wordline_names()
        # This module has no bitlines
        # self.create_all_bitline_names()
        self.add_modules()
        self.create_all_wordline_names()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        self.place_array("dummy_r{0}_c{1}", self.mirror)
        self.add_layout_pins()
        self.add_supply_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        """ Add the modules used in this design """
        if self.location == "top":
            self.colend1 = factory.create(module_type="col_cap", version="colend")
            self.colend2 = factory.create(module_type="col_cap", version="colend_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colend_cent")
        elif self.location == "bottom":
            self.colend1 = factory.create(module_type="col_cap", version="colenda")
            self.colend2 = factory.create(module_type="col_cap", version="colenda_p_cent")
            self.colend3 = factory.create(module_type="col_cap", version="colenda_cent")

        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        self.array_layout = []
        bitline = 0
        for col in range((self.column_size * 2) - 1):
            row_layout = []
            name="rca_{0}_{1}".format(self.location, col)
            # Top/bottom cell are always dummy cells.
            # Regular array cells are replica cells (>left_rbl and <rows-right_rbl)
            # Replic bit specifies which other bit (in the full range (0,rows) to make a replica cell.
            pins = []
            if col % 4 == 0:
                row_layout.append(self.colend1)
                self.cell_inst[col]=self.add_inst(name=name, mod=self.colend1)
                pins.append("fake_bl_{}".format(bitline))
                pins.append("vdd")
                pins.append("gnd")
                pins.append("fake_br_{}".format(bitline))
                pins.append("gate")
                pins.append("vdd")
                pins.append("gnd")
                bitline += 1
            elif col % 4 == 1:
                row_layout.append(self.colend2)
                self.cell_inst[col]=self.add_inst(name=name, mod=self.colend3)
                pins.append("vdd")
                pins.append("vdd")
                pins.append("gnd")
            elif col % 4 == 2:
                row_layout.append(self.colend1)
                self.cell_inst[col]=self.add_inst(name=name, mod=self.colend1)
                pins.append("fake_bl_{}".format(bitline))
                pins.append("vdd")
                pins.append("gnd")
                pins.append("fake_br_{}".format(bitline))
                pins.append("gate")
                pins.append("vdd")
                pins.append("gnd")
                bitline += 1
            elif col % 4 ==3:
                row_layout.append(self.colend2)
                self.cell_inst[col]=self.add_inst(name=name, mod=self.colend2)
                pins.append("gnd")
                pins.append("vdd")
                pins.append("vnb")

            self.connect_inst(pins)

            self.array_layout.append(row_layout)

    def place_array(self, name_template, row_offset=0):
        xoffset = 0.0
        yoffset = 0.0

        for col in range(len(self.insts)):
            inst = self.insts[col]
            if col % 4 == 0:
                inst.place(offset=[xoffset + inst.width, yoffset], mirror="MY")
            elif col % 4 == 1:
                inst.place(offset=[xoffset, yoffset])
            elif col % 4 == 2:
                inst.place(offset=[xoffset, yoffset])
            elif col % 4 ==3:
                inst.place(offset=[xoffset, yoffset])

            xoffset += inst.width

        self.width = max([x.rx() for x in self.insts])
        self.height = max([x.uy() for x in self.insts])

    def add_pins(self):

        for fake_bl in range(self.cols):
            self.add_pin("fake_bl_{}".format(fake_bl), "OUTPUT")
            self.add_pin("fake_br_{}".format(fake_bl), "OUTPUT")
        #self.add_pin("fake_wl", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        self.add_pin("gate", "BIAS")


    def add_layout_pins(self):
        """ Add the layout pins """
        # Add vdd/gnd via stacks
        for cols in range((self.column_size * 2) - 1):
            inst = self.cell_inst[cols]
            for pin_name in ["vdd", "gnd"]:
                for pin in inst.get_pins(pin_name):
                    if inst.mod.cell_name == 'sky130_fd_bd_sram__sram_sp_colend' or 'sky130_fd_bd_sram__sram_sp_colenda':
                        if inst.mirror == "MY":
                            if pin_name == "vdd" and pin.layer == 'm1':
                                self.add_layout_pin_rect_center(text="vdd",
                                                                layer=pin.layer,
                                                                offset=inst.lr(),
                                                                width=pin.width(),
                                                                height=pin.height())
                            elif pin_name == "gnd" and pin.layer == 'm1':
                                self.add_layout_pin_rect_center(text="gnd",
                                                                layer=pin.layer,
                                                                offset=inst.ll(),
                                                                width=pin.width(),
                                                                height=pin.height())
                        else:
                            if pin_name == "vdd" and pin.layer == 'm1':
                                self.add_layout_pin_rect_center(text="vdd",
                                                                layer=pin.layer,
                                                                offset=inst.ll(),
                                                                width=pin.width(),
                                                                height=pin.height())
                            elif pin_name == "gnd" and pin.layer == 'm1':
                                self.add_layout_pin_rect_center(text="gnd",
                                                                layer=pin.layer,
                                                                offset=inst.lr(),
                                                                width=pin.width(),
                                                                height=pin.height())
            

            for col in range(len(self.insts)):

                inst = self.insts[col]
                if col % 4 == 0:
                    pin = self.cell_inst[col].get_pin("bl")
                    text = "fake_bl_{}".format(int(col/2))
                    self.add_layout_pin(text=text,
                            layer=pin.layer,
                            offset=pin.ll().scale(1, 0),
                            width=pin.width(),
                            height=pin.height())
                    
                    pin = self.cell_inst[col].get_pin("br")
                    text = "fake_br_{}".format(int(col/2))
                    self.add_layout_pin(text=text,
                            layer=pin.layer,
                            offset=pin.ll().scale(1, 0),
                            width=pin.width(),
                            height=pin.height())

                elif col % 4 == 2:
                    pin = self.cell_inst[col].get_pin("bl")
                    text = "fake_bl_{}".format(int(col/2))
                    self.add_layout_pin(text=text,
                            layer=pin.layer,
                            offset=pin.ll().scale(1, 0),
                            width=pin.width(),
                            height=pin.height())
                    
                    pin = self.cell_inst[col].get_pin("br")
                    text = "fake_br_{}".format(int(col/2))
                    self.add_layout_pin(text=text,
                            layer=pin.layer,
                            offset=pin.ll().scale(1, 0),
                            width=pin.width(),
                            height=pin.height())
        return
    
    def add_supply_pins(self):
        for col in range(len(self.insts)):
            inst = self.cell_inst[col]

            if 'VPB' or 'vnb' in self.cell_inst[col].mod.pins:
                pin = inst.get_pin("vpb")
                self.objs.append(geometry.rectangle(layer["nwell"],
                pin.ll(),
                pin.width(),
                pin.height()))
                self.objs.append(geometry.label("vdd", layer["nwell"], pin.center()))

                
            if 'VNB' or 'vnb' in self.cell_inst[col].mod.pins:
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



    def create_all_wordline_names(self, row_size=None):
        if row_size == None:
            row_size = self.row_size

        for row in range(row_size):
            for port in self.all_ports:
                self.wordline_names[port].append("wl_{0}_{1}".format(port, row))

        self.all_wordline_names = [x for sl in zip(*self.wordline_names) for x in sl]
