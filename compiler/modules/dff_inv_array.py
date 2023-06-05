# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram import OPTS


class dff_inv_array(design):
    """
    This is a simple row (or multiple rows) of flops.
    Unlike the data flops, these are never spaced out.
    """
    unique_id = 1

    def __init__(self, rows, columns, inv_size=2, name=""):
        self.rows = rows
        self.columns = columns

        if name=="":
            name = "dff_inv_array_{0}x{1}_{2}".format(rows, columns, dff_inv_array.unique_id)
            dff_inv_array.unique_id += 1
        super().__init__(name)
        debug.info(1, "Creating {}".format(self.name))
        self.add_comment("rows: {0} cols: {1}".format(rows, columns))
        self.add_comment("inv1: {0}".format(inv1_size))

        self.inv_size = inv_size

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_dff_array()

    def create_layout(self):
        self.width = self.columns * self.dff.width
        self.height = self.rows * self.dff.height

        self.place_dff_array()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        self.dff = factory.create(module_type="dff")

    def add_pins(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.add_pin(self.get_din_name(row,col), "INPUT")
        for row in range(self.rows):
            for col in range(self.columns):
                self.add_pin(self.get_dout_name(row,col), "OUTPUT")
                self.add_pin(self.get_dout_bar_name(row,col), "OUTPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_dff_array(self):
        self.dff_insts={}
        for row in range(self.rows):
            for col in range(self.columns):
                name = "Xdff_r{0}_c{1}".format(row,col)
                self.dff_insts[row,col]=self.add_inst(name=name,
                                                      mod=self.dff)
                self.connect_inst([self.get_din_name(row,col),
                                   self.get_dout_name(row,col),
                                   self.get_dout_bar_name(row,col),
                                   "clk",
                                   "vdd",
                                   "gnd"])

    def place_dff_array(self):
        for row in range(self.rows):
            for col in range(self.columns):
                name = "Xdff_r{0}_c{1}".format(row,col)
                if (row % 2 == 0):
                    base = vector(col*self.dff.width,row*self.dff.height)
                    mirror = "R0"
                else:
                    base = vector(col*self.dff.width,(row+1)*self.dff.height)
                    mirror = "MX"
                self.dff_insts[row,col].place(offset=base,
                                              mirror=mirror)

    def get_din_name(self, row, col):
        if self.columns == 1:
            din_name = "din_{0}".format(row)
        elif self.rows == 1:
            din_name = "din_{0}".format(col)
        else:
            din_name = "din_{0}_{1}".format(row,col)

        return din_name

    def get_dout_name(self, row, col):
        if self.columns == 1:
            dout_name = "dout_{0}".format(row)
        elif self.rows == 1:
            dout_name = "dout_{0}".format(col)
        else:
            dout_name = "dout_{0}_{1}".format(row,col)

        return dout_name

    def get_dout_bar_name(self, row, col):
        if self.columns == 1:
            dout_bar_name = "dout_bar_{0}".format(row)
        elif self.rows == 1:
            dout_bar_name = "dout_bar_{0}".format(col)
        else:
            dout_bar_name = "dout_bar_{0}_{1}".format(row,col)

        return dout_bar_name

    def add_layout_pins(self):
        for row in range(self.rows):
            for col in range(self.columns):
                # Adds power pin on left of row
                vdd_pin=self.dff_insts[row,col].get_pin("vdd")
                self.add_power_pin(vdd_pin, loc=vdd_pin.lc(), start_layer=vdd_pin.layer)

                # Adds gnd pin on left of row
                gnd_pin=self.dff_insts[row,col].get_pin("gnd")
                self.add_power_pin(gnd_pin, loc=gnd_pin.lc(), start_layer=gnd_pin.layer)

        for row in range(self.rows):
            for col in range(self.columns):
                din_pin = self.dff_insts[row,col].get_pin("D")
                debug.check(din_pin.layer=="m2","DFF D pin not on metal2")
                self.add_layout_pin(text=self.get_din_name(row,col),
                                    layer=din_pin.layer,
                                    offset=din_pin.ll(),
                                    width=din_pin.width(),
                                    height=din_pin.height())

                dout_pin = self.dff_insts[row,col].get_pin("Q")
                debug.check(dout_pin.layer=="m2","DFF Q pin not on metal2")
                self.add_layout_pin(text=self.get_dout_name(row,col),
                                    layer=dout_pin.layer,
                                    offset=dout_pin.ll(),
                                    width=dout_pin.width(),
                                    height=dout_pin.height())

                dout_bar_pin = self.dff_insts[row,col].get_pin("Qb")
                debug.check(dout_bar_pin.layer=="m2","DFF Qb pin not on metal2")
                self.add_layout_pin(text=self.get_dout_bar_name(row,col),
                                    layer=dout_bar_pin.layer,
                                    offset=dout_bar_pin.ll(),
                                    width=dout_bar_pin.width(),
                                    height=dout_bar_pin.height())


        # Create vertical spines to a single horizontal rail
        clk_pin = self.dff_insts[0,0].get_pin("clk")
        clk_ypos = 2*self.m3_pitch+self.m3_width
        debug.check(clk_pin.layer=="m2","DFF clk pin not on metal2")
        if self.columns==1:
            self.add_layout_pin(text="clk",
                                layer="m2",
                                offset=clk_pin.ll().scale(1,0),
                                width=self.m2_width,
                                height=self.height)
        else:
            self.add_layout_pin_segment_center(text="clk",
                                            layer="m3",
                                            start=vector(0,clk_ypos),
                                            end=vector(self.width,clk_ypos))
            for col in range(self.columns):
                clk_pin = self.dff_insts[0,col].get_pin("clk")
                # Make a vertical strip for each column
                self.add_rect(layer="m2",
                              offset=clk_pin.ll().scale(1,0),
                              width=self.m2_width,
                              height=self.height)
                # Drop a via to the M3 pin
                self.add_via_center(layers=self.m2_stack,
                                    offset=vector(clk_pin.cx(),clk_ypos))
