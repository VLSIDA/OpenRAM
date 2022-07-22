# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#



from .bitcell_base_array import bitcell_base_array
from base import vector
from globals import OPTS
from sram_factory import factory

class rom_base_array(bitcell_base_array):

    def __init__(self, rows, cols, bitmap, name="", column_offset=0):
        super().__init__(name=name, rows=rows, cols=cols, column_offset=column_offset)
        self.data = bitmap

        self.create_all_bitline_names()
        self.create_all_wordline_names()
        self.create_netlist()

        self.create_layout()
        

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()


    def create_layout(self):
        #self.add_layout_pins()
        self.place_ptx()
        self.route_supplies()

        #self.add_boundary()

        #self.DRC_LVS()
        
    #def add_pins(self):
    def add_boundary(self):
        self.width = self.nmos.width * self.column_size
        self.height = self.nmos.height * self.row_size
        super().add_boundary()

    def add_modules(self):

        self.nmos = factory.create(module_type="ptx", tx_type="nmos")
    


    def create_instances(self):
        self.cell_inst = {}
        self.current_row = 0
        for col in range(self.column_size):
            for row in range(self.row_size):
                name = "bit_r{0}_c{1}".format(row, col)

                if(self.data[col][row] == 1):
                    self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.nmos)
                    
                    self.connect_inst(self.get_bitcell_pins(row, col))

                # If it is a "core" cell, it could be trimmed for sim time
                #if col>0 and col<self.column_size-1 and row>0 and row<self.row_size-1:
                #    self.trim_insts.add(name)

    def place_ptx(self):
        self.cell_pos = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                

                if(self.data[col][row] == 1):

                    cell_x = (self.nmos.width + 2 * self.nmos.active_contact_to_gate + self.nmos.contact_width) * col 
                    cell_y = (self.nmos.height + self.nmos.poly_extend_active)  * row
                    self.cell_pos[row, col] = self.nmos.active_offset.scale(1, 0) \
                        + vector(cell_x, cell_y)
                    
                    self.cell_inst[row, col].place(self.cell_pos[row, col])




    def create_all_bitline_names(self):
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]


    def get_bitcell_pins(self, row, col):
        bitcell_pins = []

        #drain pin
        if self.current_row == 0:
            bitcell_pins.append(self.bitline_names[0][col])
        else:
            bitcell_pins.append(self.get_current_bl_interconnect(col))
            

        #gate pin
        bitcell_pins.append(self.get_wordline_names()[row])

        #source pin
        

        if 1 not in self.data[col][row + 1:]:
            bitcell_pins.append("gnd")
        else:
            bitcell_pins.append(self.create_next_bl_interconnect(row, col))
        #body pin
        bitcell_pins.append("gnd")

        return bitcell_pins

    def create_next_bl_interconnect(self, row, col):
        self.current_row = row
        return "bli_{0}_{1}".format(row, col)

    def get_current_bl_interconnect(self, col):
        return "bli_{0}_{1}".format(self.current_row, col)


