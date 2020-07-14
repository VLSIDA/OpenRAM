# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from vector import vector
from sram_factory import factory
from globals import OPTS


class dff_array(design.design):
    """
    This is a simple row (or multiple rows) of flops.
    Unlike the data flops, these are never spaced out.
    """

    def __init__(self, rows, columns, name=""):
        self.rows = rows
        self.columns = columns

        if name=="":
            name = "dff_array_{0}x{1}".format(rows, columns)
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} rows={1} cols={2}".format(self.name, self.rows, self.columns))
        self.add_comment("rows: {0} cols: {1}".format(rows, columns))
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
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
        self.add_mod(self.dff)
        
    def add_pins(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.add_pin(self.get_din_name(row, col), "INPUT")
        for row in range(self.rows):
            for col in range(self.columns):
                self.add_pin(self.get_dout_name(row, col), "OUTPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_dff_array(self):
        self.dff_insts={}
        for row in range(self.rows):
            for col in range(self.columns):
                name = "dff_r{0}_c{1}".format(row, col)
                self.dff_insts[row, col]=self.add_inst(name=name,
                                                       mod=self.dff)
                instance_ports = [self.get_din_name(row, col),
                                  self.get_dout_name(row, col)]
                for port in self.dff.pin_names:
                    if port != 'D' and port != 'Q':
                        instance_ports.append(port)
                self.connect_inst(instance_ports)

    def place_dff_array(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if (row % 2 == 0):
                    base = vector(col * self.dff.width, row * self.dff.height)
                    mirror = "R0"
                else:
                    base = vector(col * self.dff.width, (row + 1) * self.dff.height)
                    mirror = "MX"
                self.dff_insts[row, col].place(offset=base,
                                               mirror=mirror)
                
    def get_din_name(self, row, col):
        if self.columns == 1:
            din_name = "din_{0}".format(row)
        elif self.rows == 1:
            din_name = "din_{0}".format(col)
        else:
            din_name = "din_{0}_{1}".format(row, col)

        return din_name
    
    def get_dout_name(self, row, col):
        if self.columns == 1:
            dout_name = "dout_{0}".format(row)
        elif self.rows == 1:
            dout_name = "dout_{0}".format(col)
        else:
            dout_name = "dout_{0}_{1}".format(row, col)

        return dout_name
    
    def add_layout_pins(self):
        for row in range(self.rows):
            for col in range(self.columns):
                # Continous vdd rail along with label.
                vdd_pin=self.dff_insts[row, col].get_pin("vdd")
                self.add_power_pin("vdd", vdd_pin.center(), start_layer=vdd_pin.layer)

                # Continous gnd rail along with label.
                gnd_pin=self.dff_insts[row, col].get_pin("gnd")
                self.add_power_pin("gnd", gnd_pin.center(), start_layer=gnd_pin.layer)
            
        for row in range(self.rows):
            for col in range(self.columns):
                din_pin = self.dff_insts[row, col].get_pin("D")
                debug.check(din_pin.layer == "m2", "DFF D pin not on metal2")
                self.add_layout_pin(text=self.get_din_name(row, col),
                                    layer=din_pin.layer,
                                    offset=din_pin.ll(),
                                    width=din_pin.width(),
                                    height=din_pin.height())

                dout_pin = self.dff_insts[row, col].get_pin("Q")
                debug.check(dout_pin.layer == "m2", "DFF Q pin not on metal2")
                self.add_layout_pin(text=self.get_dout_name(row, col),
                                    layer=dout_pin.layer,
                                    offset=dout_pin.ll(),
                                    width=dout_pin.width(),
                                    height=dout_pin.height())

        # Create vertical spines to a single horizontal rail
        clk_pin = self.dff_insts[0, 0].get_pin(self.dff.clk_pin)
        clk_ypos = 2 * self.m3_pitch + self.m3_width
        debug.check(clk_pin.layer == "m2", "DFF clk pin not on metal2")
        self.add_layout_pin_segment_center(text="clk",
                                           layer="m3",
                                           start=vector(0, clk_ypos),
                                           end=vector(self.width, clk_ypos))
        for col in range(self.columns):
            clk_pin = self.dff_insts[0, col].get_pin(self.dff.clk_pin)
            # Make a vertical strip for each column
            self.add_rect(layer="m2",
                          offset=clk_pin.ll().scale(1, 0),
                          width=self.m2_width,
                          height=self.height)
            # Drop a via to the M3 pin
            self.add_via_stack_center(from_layer=clk_pin.layer,
                                      to_layer="m3",
                                      offset=vector(clk_pin.cx(), clk_ypos))
            
    def get_clk_cin(self):
        """Return the total capacitance (in relative units) that the clock is loaded by in the dff array"""
        dff_clk_cin = self.dff.get_clk_cin()
        total_cin = dff_clk_cin * self.rows * self.columns
        return total_cin
