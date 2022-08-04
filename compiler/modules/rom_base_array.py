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
        
        #TODO: data is input in col-major order for ease of parsing, create a function to convert a row-major input to col-major 
        self.data = bitmap
        self.route_layer = 'm1'
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
        
        #self.route_horizontal_pins(insts=self.cell_inst.values(), layer=self.route_layer, name="S")
        self.route_bitlines()
        #self.route_wordlines()

        self.route_supplies()

        self.add_boundary()

        #self.DRC_LVS()
        
    #def add_pins(self):
    def add_boundary(self):
        self.width = self.nmos.width * self.column_size
        self.height = self.nmos.height * self.row_size
        super().add_boundary()

    def add_modules(self):

        self.nmos = factory.create(module_type="ptx", tx_type="nmos", add_source_contact=self.route_layer,
                                   add_drain_contact=self.route_layer)
        temp = self.nmos.width
        self.nmos.width = self.nmos.height + self.nmos.poly_extend_active
        self.nmos.height = temp 
    def create_instances(self):
        self.cell_inst = {}
        self.cell_list = []
        self.current_row = 0
        for row in range(self.row_size):
            row_list = []

            for col in range(self.column_size):
                
                name = "bit_r{0}_c{1}".format(row, col)

                if(self.data[row][col] == 1):
                    self.cell_inst[row, col]=self.add_inst(name=name,
                                                       mod=self.nmos, rotate=90)

                    row_list.append(self.cell_inst[row, col])
                    self.connect_inst(self.get_bitcell_pins(row, col))
                else: row_list.append(None)
            self.cell_list.append(row_list)



    def create_all_bitline_names(self):
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]


    def place_ptx(self):
        self.cell_pos = {}
        for col in range(self.column_size):
            for row in range(self.row_size):
                
                #cell_x = (self.nmos.height + self.nmos.poly_extend_active) * col 
                #cell_y = (self.nmos.width + 2 * self.nmos.active_contact_to_gate + self.nmos.contact_width)  * row
                cell_x = self.nmos.width * col
                cell_y = self.nmos.height * row
                print(self.nmos.height + self.nmos.poly_extend_active)
                if(self.data[row][col] == 1):

                    
                    self.cell_pos[row, col] = self.nmos.active_offset.scale(1, 0) \
                        + vector(cell_x, cell_y)
                    
                    self.cell_inst[row, col].place(self.cell_pos[row, col], rotate=90)
                    self.add_label("S_{}_{}".format(row,col), self.route_layer, self.cell_inst[row, col].get_pin("S").center())
                    self.add_label("D", self.route_layer, self.cell_inst[row, col].get_pin("D").center())

                else:
                    
                    #poly_offset = (self.nmos.contact_offset + vector(0.5 * self.nmos.active_contact.width + 0.5 * self.nmos.poly_width + self.nmos.active_contact_to_gate, 0)) + (0, cell_y)
                    poly_offset = (cell_x, cell_y)
                    #print(cell_x,cell_y)
                    self.add_rect(layer="poly",
                                 offset=poly_offset,
                                 width=self.nmos.height + self.nmos.poly_extend_active,
                                 height=self.nmos.poly_width
                                 )
                    


    def route_bitlines(self):

        #get first nmos in col

        #connect to main bitline wire

        #get next nmos in col

        #route source to drain

        #loop


        for col in range(self.column_size):
            for row in range(self.row_size ):

                #nmos at this position and another nmos further down 
                if self.data[row][col] == 1 :
                    
                    next_row = self.get_next_cell_in_bl(row, col)
                    if next_row != -1:

                        drain_pin = self.cell_inst[row, col].get_pin("D")
                        source_pin = self.cell_inst[next_row, col].get_pin("S")

                        source_pos = source_pin.bc()
                        drain_pos = drain_pin.bc()
                        self.add_path(self.route_layer, [drain_pos, source_pos])

                



    def get_next_cell_in_bl(self, row_start, col):
        for row in range(row_start + 1, self.row_size):
            if self.data[row][col] == 1:
                return row
        return -1



    def get_current_bl_interconnect(self, col):
        """Get interconnect net for bitline(col) currently being connected """
        return "bli_{0}_{1}".format(self.current_row, col)

    def create_next_bl_interconnect(self, row, col):
        """create a new net name for a bitline interconnect"""
        self.current_row = row
        return "bli_{0}_{1}".format(row, col)
    
    
    def get_bitcell_pins(self, row, col):
        """ 
        return the correct nets to attack nmos/cell drain, gate, source, body pins to
        """

        bitcell_pins = []

        #drain pin
        if self.current_row == 0:
            bitcell_pins.append(self.bitline_names[0][col])
        else:
            bitcell_pins.append(self.get_current_bl_interconnect(col))
            

        #gate pin
        bitcell_pins.append(self.get_wordline_names()[row])

        #source pin
        
        """If there is another bitcell to be placed below the current cell, """
        
        if self.get_next_cell_in_bl(row, col) == -1:
            bitcell_pins.append("gnd")
        else:
            """create another interconnect net"""
            bitcell_pins.append(self.create_next_bl_interconnect(row, col))

        #body pin
        bitcell_pins.append("gnd")

        return bitcell_pins




