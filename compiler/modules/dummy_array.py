# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California 
# All rights reserved.
#
import debug
import design
from tech import drc
import contact
from sram_factory import factory
from vector import vector
from globals import OPTS

class dummy_array(design.design):
    """
    Generate a dummy row/column for the replica array.
    """
    def __init__(self, cols, rows, mirror=0, name=""):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0} {1} x {2}".format(self.name, rows, cols))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.column_size = cols
        self.row_size = rows
        self.mirror = mirror

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

        
    def create_netlist(self):
        """ Create and connect the netlist """
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):

        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.row_size*self.dummy_cell.height
        self.width = self.column_size*self.dummy_cell.width
        
        xoffset = 0.0
        for col in range(self.column_size):
            yoffset = 0.0
            for row in range(self.row_size):
                name = "dummy_r{0}_c{1}".format(row, col)

                if (row+self.mirror) % 2:
                    tempy = yoffset + self.dummy_cell.height
                    dir_key = "MX"
                else:
                    tempy = yoffset
                    dir_key = ""

                self.cell_inst[row,col].place(offset=[xoffset, tempy],
                                              mirror=dir_key)
                yoffset += self.dummy_cell.height
            xoffset += self.dummy_cell.width

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()

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

    def add_modules(self):
        """ Add the modules used in this design """
        self.dummy_cell = factory.create(module_type="dummy_bitcell")
        self.add_mod(self.dummy_cell)

        self.cell = factory.create(module_type="bitcell")
        
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
    
        
    def create_instances(self):
        """ Create the module instances used in this design """
        self.cell_inst = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)
                self.cell_inst[row,col]=self.add_inst(name=name,
                                                      mod=self.dummy_cell)
                self.connect_inst(self.get_bitcell_pins(col, row))
        
    def add_layout_pins(self):
        """ Add the layout pins """
        
        row_list = self.cell.get_all_wl_names()
        column_list = self.cell.get_all_bitline_names()
        
        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[0,col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                    layer="metal2",
                                    offset=bl_pin.ll(),
                                    width=bl_pin.width(),
                                    height=self.height)

        for row in range(self.row_size):
            for cell_row in row_list:
                wl_pin = self.cell_inst[row,0].get_pin(cell_row)
                self.add_layout_pin(text=cell_row+"_{0}".format(row),
                                    layer="metal1",
                                    offset=wl_pin.ll(),
                                    width=self.width,
                                    height=wl_pin.height())

        # For every second row and column, add a via for gnd and vdd
        for row in range(self.row_size):
            for col in range(self.column_size):
                inst = self.cell_inst[row,col]
                for pin_name in ["vdd", "gnd"]:
                    for pin in inst.get_pins(pin_name):
                        self.add_power_pin(name=pin_name, loc=pin.center(), vertical=True, start_layer=pin.layer)
    

    def input_load(self):
        wl_wire = self.gen_wl_wire()
        return wl_wire.return_input_cap()

    def get_wordline_cin(self):
        """Get the relative input capacitance from the wordline connections in all the bitcell"""
        #A single wordline is connected to all the bitcells in a single row meaning the capacitance depends on the # of columns
        bitcell_wl_cin = self.cell.get_wl_cin()
        total_cin = bitcell_wl_cin * self.column_size
        return total_cin
