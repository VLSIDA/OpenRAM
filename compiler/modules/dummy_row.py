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

class dummy_row(design.design):
    """
    Generate a replica wordline row for the replica array.
    """

    def __init__(self, name, cols):
        design.design.__init__(self, name)

        self.column_size = cols 

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
            
    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.place_instances()
        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        column_list = self.cell.list_all_bitline_names()
        for col in range(self.column_size):
            for cell_column in column_list:
                self.add_pin("{0}_{1}".format(cell_column,col))
        row_list = self.cell.list_all_wl_names()
        for cell_row in row_list:
            self.add_pin("{0}_{1}".format(cell_row,0))
                    
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        self.dummy_cell = factory.create(module_type="dummy_bitcell")
        self.add_mod(self.dummy_cell)
        # Used for pin names only
        self.cell = factory.create(module_type="bitcell")
        
    def create_instances(self):
        self.cell_inst = {}
        for col in range(self.column_size):
            name="dummy_{0}".format(col)
            self.cell_inst[col]=self.add_inst(name=name,
                                              mod=self.dummy_cell)
            self.connect_inst(self.list_bitcell_pins(col, 0))
            
    def create_layout(self):

        # We increase it by a well enclosure so the precharges don't overlap our wells
        self.height = self.cell.height
        self.width = self.column_size*self.cell.width 
        
        xoffset = 0.0
        tempy = self.cell.height
        dir_key = "MX"
        for col in range(self.column_size):
            name = "bit_{0}_c{1}".format("dummy",col)
            self.cell_inst[col].place(offset=[xoffset, tempy],
                                      mirror=dir_key)
            xoffset += self.cell.width

        self.add_layout_pins()

        self.add_boundary()
        
        self.DRC_LVS()


    def add_layout_pins(self):
        """ Add the layout pins """
        
        row_list = self.cell.list_all_wl_names()
        column_list = self.cell.list_all_bitline_names()

        for col in range(self.column_size):
            for cell_column in column_list:
                bl_pin = self.cell_inst[col].get_pin(cell_column)
                self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                    layer="metal2",
                                    offset=bl_pin.ll(),
                                    width=bl_pin.width(),
                                    height=self.height)

        for cell_row in row_list:
            wl_pin = self.cell_inst[0].get_pin(cell_row)
            self.add_layout_pin(text=cell_row+"_{0}".format(0),
                                layer="metal1",
                                offset=wl_pin.ll(),
                                width=self.width,
                                height=wl_pin.height())

        # For every second row and column, add a via for gnd and vdd
        for col in range(self.column_size):
            inst = self.cell_inst[col]
            for pin_name in ["vdd", "gnd"]:
                self.copy_layout_pin(inst, pin_name)

    def list_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, 
        indexed by column and row, for instance use in bitcell_array """

        bitcell_pins = []
        
        pin_names = self.cell.list_all_bitline_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(col))
        pin_names = self.cell.list_all_wl_names()
        for pin in pin_names:
            bitcell_pins.append(pin+"_{0}".format(row))
        bitcell_pins.append("vdd")
        bitcell_pins.append("gnd")
        
        return bitcell_pins
                
