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

class replica_column(design.design):
    """
    Generate a replica bitline column for the replica array.
    """

    def __init__(self, name, rows, num_ports):
        design.design.__init__(self, name)

        self.row_size = rows
        self.num_ports = num_ports

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

        self.height = self.row_size*self.cell.height
        self.width = self.cell.width 

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        column_list = self.cell.list_all_bitline_names()
        for cell_column in column_list:
            self.add_pin("{0}_{1}".format(cell_column,0))
        row_list = self.cell.list_all_wl_names()
        for row in range(self.row_size):
            for cell_row in row_list:
                self.add_pin("{0}_{1}".format(cell_row,row))
                    
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        self.replica_cell = factory.create(module_type="replica_bitcell")
        self.add_mod(self.replica_cell)
        self.dummy_cell = factory.create(module_type="dummy_bitcell")
        self.add_mod(self.dummy_cell)
        # Used for pin names only
        self.cell = factory.create(module_type="bitcell")
        
    def create_instances(self):
        self.cell_inst = {}
        for row in range(self.row_size):
            name="rbc_{0}".format(row)
            if row>0 and row<self.row_size - self.num_ports:
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.replica_cell)
            else:
                self.cell_inst[row]=self.add_inst(name=name,
                                                  mod=self.dummy_cell)
            self.connect_inst(self.list_bitcell_pins(0, row))
            
    def place_instances(self):

        yoffset = 0
        for row in range(self.row_size):
            name = "bit_r{0}_{1}".format(row,"rbl")

            # This is opposite of a bitcell array since we will be 1 row off
            if not row % 2:
                tempy = yoffset
                dir_key = ""
            else:
                tempy = yoffset + self.cell.height
                dir_key = "MX"

            self.cell_inst[row].place(offset=[0.0, tempy],
                                          mirror=dir_key)
            yoffset += self.cell.height



    def add_layout_pins(self):
        """ Add the layout pins """
        
        row_list = self.cell.list_all_wl_names()
        column_list = self.cell.list_all_bitline_names()

        col = "0"
        for cell_column in column_list:
            bl_pin = self.cell_inst[0].get_pin(cell_column)
            self.add_layout_pin(text=cell_column+"_{0}".format(col),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=self.height)

        for row in range(self.row_size):
            for cell_row in row_list:
                wl_pin = self.cell_inst[row].get_pin(cell_row)
                self.add_layout_pin(text=cell_row+"_{0}".format(row),
                                    layer="metal1",
                                    offset=wl_pin.ll(),
                                    width=self.width,
                                    height=wl_pin.height())

        # For every second row and column, add a via for gnd and vdd
        for row in range(self.row_size):
            inst = self.cell_inst[row]
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
                
