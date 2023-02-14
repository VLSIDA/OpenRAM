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

class sky130_dummy_array(sky130_bitcell_base_array):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, rows, cols, column_offset=0, row_offset=0 ,mirror=0, location="", name=""):

        super().__init__(rows=rows, cols=cols, column_offset=column_offset, name=name)
        self.mirror = mirror

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        """ Create and connect the netlist """
        # This will create a default set of bitline/wordline names
        self.create_all_bitline_names()
        self.create_all_wordline_names()

        self.add_modules()
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
        self.dummy_cell = factory.create(module_type=OPTS.dummy_bitcell, version="opt1")
        self.dummy_cell2 = factory.create(module_type=OPTS.dummy_bitcell, version="opt1a")
        self.strap = factory.create(module_type="internal", version="wlstrap")
        self.strap2 = factory.create(module_type="internal", version="wlstrap_p")
        self.strap3 = factory.create(module_type="internal", version="wlstrapa")
        self.strap4 = factory.create(module_type="internal", version="wlstrapa_p")
        self.cell = factory.create(module_type=OPTS.bitcell, version="opt1")

    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        self.array_layout = []
        alternate_bitcell = (self.row_size + 1) % 2
        for row in range(0, self.row_size):

            row_layout = []

            alternate_strap = (self.row_size + 1) % 2
            for col in range(0, self.column_size):
                if alternate_bitcell == 1:
                    row_layout.append(self.dummy_cell)
                    self.cell_inst[row, col]=self.add_inst(name="row_{}_col_{}_bitcell".format(row, col),
                                                           mod=self.dummy_cell)
                else:
                    row_layout.append(self.dummy_cell2)
                    self.cell_inst[row, col]=self.add_inst(name="row_{}_col_{}_bitcell".format(row, col),
                                                           mod=self.dummy_cell2)
                self.connect_inst(self.get_bitcell_pins(row, col))
                if col != self.column_size - 1:
                    if alternate_strap:
                        if col % 2:
                            name="row_{}_col_{}_wlstrap_p".format(row, col)
                            row_layout.append(self.strap4)
                            self.add_inst(name=name,
                                        mod=self.strap4) 
                        else:
                            name="row_{}_col_{}_wlstrapa_p".format(row, col)
                            row_layout.append(self.strap2)
                            self.add_inst(name=name,
                                        mod=self.strap2)
                        alternate_strap = 0
                    else:
                        if col % 2:
                            name="row_{}_col_{}_wlstrap".format(row, col)
                            row_layout.append(self.strap)
                            self.add_inst(name=name,
                                            mod=self.strap)
                        else:
                            name="row_{}_col_{}_wlstrapa".format(row, col)
                            row_layout.append(self.strap3)
                            self.add_inst(name=name,
                                            mod=self.strap3)
                        alternate_strap = 1

                    self.connect_inst(self.get_strap_pins(row, col, name))
            if alternate_bitcell == 0:
                alternate_bitcell = 1
            else:
                alternate_bitcell = 0
            self.array_layout.append(row_layout)

    def add_pins(self):
        # bitline pins are not added because they are floating
        for bl in range(self.column_size):
            self.add_pin("bl_0_{}".format(bl))
            self.add_pin("br_0_{}".format(bl))
        for wl_name in self.get_wordline_names():
            self.add_pin(wl_name, "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        #self.add_pin("vpb", "BIAS")
        #Sself.add_pin("vnb", "BIAS")

    def add_layout_pins(self):
        """ Add the layout pins """
        bitline_names = self.cell.get_all_bitline_names()
        for col in range(self.column_size):
            for port in self.all_ports:
                bl_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port])
                text = "bl_{0}_{1}".format(port, col)
                self.add_layout_pin(text=text,
                                    layer=bl_pin.layer,
                                    offset=bl_pin.ll().scale(1, 0),
                                    width=bl_pin.width(),
                                    height=self.height)
                br_pin = self.cell_inst[0, col].get_pin(bitline_names[2 * port + 1])
                text = "br_{0}_{1}".format(port, col)
                self.add_layout_pin(text=text,
                                    layer=br_pin.layer,
                                    offset=br_pin.ll().scale(1, 0),
                                    width=br_pin.width(),
                                    height=self.height)
                # self.add_rect(layer=bl_pin.layer,
                #               offset=bl_pin.ll().scale(1, 0),
                #               width=bl_pin.width(),
                #               height=self.height)
                # self.add_rect(layer=br_pin.layer,
                #               offset=br_pin.ll().scale(1, 0),
                #               width=br_pin.width(),
                #               height=self.height)

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

    def add_supply_pins(self):
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row, col]
                if 'VPB' or 'vpb' in self.cell_inst[row, col].mod.pins:
                    pin = inst.get_pin("vpb")
                    self.objs.append(geometry.rectangle(layer["nwell"],
                                                        pin.ll(),
                                                        pin.width(),
                                                        pin.height()))
                    self.objs.append(geometry.label("vdd", layer["nwell"], pin.center()))

                if 'VNB' or 'vnb' in self.cell_inst[row, col].mod.pins:
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

    def input_load(self):
        # FIXME: This appears to be old code from previous characterization. Needs to be updated.
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()
