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

    def __init__(self, rows, cols, strap_spacing, bitmap, name="", column_offset=0):
        super().__init__(name=name, rows=rows, cols=cols, column_offset=column_offset)
        
        #TODO: data is input in col-major order for ease of parsing, create a function to convert a row-major input to col-major 
        self.data = bitmap
        self.route_layer = 'm1'
        self.strap_spacing = strap_spacing
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
        self.place_taps()
        self.place_rails()
        #self.route_horizo  ntal_pins(insts=self.cell_inst.values(), layer=self.route_layer, name="S")
        #self.route_bitlines()
        #self.route_wordlines()

        self.add_boundary()

        
        
    #def add_pins(self):
    def add_boundary(self):
        self.width = self.dummy.width * self.column_size
        self.height = self.dummy.height * self.row_size
        super().add_boundary()

    def add_modules(self):

        # dummy cell, # "dummy" cells represent 0
        self.dummy = factory.create(module_type="rom_dummy_cell", route_layer=self.route_layer)

        

        #base cell with no contacts
        self.cell_nc = factory.create(module_name="base_mod_0_contact", module_type="rom_base_cell")
        #base cell with drain contact
        self.cell_dc = factory.create(module_name="base_mod_d_contact", module_type="rom_base_cell", add_drain_contact=self.route_layer)
        #base cell with source contact
        self.cell_sc = factory.create(module_name="base_mod_s_contact", module_type="rom_base_cell", add_source_contact=self.route_layer)
        #base cell with all contacts
        self.cell_ac = factory.create(module_name="base_mod_sd_contact", module_type="rom_base_cell", add_source_contact=self.route_layer, add_drain_contact=self.route_layer)

        self.poly_tap = factory.create(module_type="rom_poly_tap", strap_length=self.strap_spacing)
        
        self.gnd_rail = factory.create(module_type="rom_array_gnd_tap", length=self.row_size)

    def create_instances(self):
        self.tap_inst = {}
        self.cell_inst = {}
        self.cell_list = []
        self.current_row = 0

        #list of current bitline interconnect nets, starts as the same as the bitline list and is updated when new insts of cells are added
        int_bl_list = self.bitline_names[0]
        #When rotated correctly rows are word lines
        for row in range(self.row_size):
            row_list = []

            #when rotated correctly cols are bit lines
            for col in range(self.column_size):
                
                name = "bit_r{0}_c{1}".format(row, col)

                if self.data[row][col] == 1:
                    # if dummy/0 cell above and below a 1, add a tx with contacts on both drain and source 
                    # if the first row and a 0 above, add both contacts
                    # if the last row and 0 below add both contacts
                    #(row == 0 and self.data[row + 1][col] == 0): 
                    if  (row < self.row_size - 1 and row > 0 and self.data[row + 1][col] == 0 and self.data[row - 1][col] == 0) or \
                        (row == self.row_size - 1 and self.data[row - 1][col] == 0):
                        
                        self.cell_inst[row, col]=self.add_inst(name=name, mod=self.cell_ac)
                
                    # if dummy/0 is below and not above, add a source contact
                    # if in the first row, add a source contact
                    elif (row > 0 and self.data[row - 1][col] == 0):
                        self.cell_inst[row, col]=self.add_inst(name=name, mod=self.cell_sc)

                    elif (row < self.row_size - 1 and self.data[row + 1][col] == 0) or \
                         (row == self.row_size - 1):          
                        self.cell_inst[row, col]=self.add_inst(name=name, mod=self.cell_dc)

                    else:
                        self.cell_inst[row, col]=self.add_inst(name=name, mod=self.cell_nc)


                    if row == self.row_size - 1 or self.get_next_cell_in_bl(row, col) == -1:
                        print(self.cell_inst[row, col])
                        bl_l = int_bl_list[col]
                        bl_h = "gnd" 
                    else:
                        bl_l = int_bl_list[col]
                        int_bl_list[col] = "bl_int_{0}_{1}".format(row, col)
                        bl_h = int_bl_list[col]
                    
                    

                    self.connect_inst([bl_h, bl_l, self.wordline_names[0][row], "gnd"])                    
                    

                else: 

                    self.cell_inst[row, col]=self.add_inst(name=name,
                                                           mod=self.dummy)
                    self.connect_inst([])
                    
                # when col = 0 bl_h is connected to vdd, otherwise connect to previous bl connection
                # when col = col_size - 1 connected to gnd otherwise create new bl connection
                # 
                

                row_list.append(self.cell_inst[row, col])

                if col % self.strap_spacing == 0:

                    name = "tap_r{0}_c{1}".format(row, col)

                    self.tap_inst[row, col]=self.add_inst(name=name, mod=self.poly_tap)
                    self.connect_inst([])
                
            name = "tap_r{0}_c{1}".format(row, self.column_size)
            #print(*row_list)
            self.tap_inst[row, self.column_size]=self.add_inst(name=name, mod=self.poly_tap)
            self.connect_inst([])

            self.cell_list.append(row_list)



    def create_all_bitline_names(self):
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]

    def place_taps(self):
        
        self.tap_pos = {}
        for row in range(self.row_size):
            for s_col in range(0, self.column_size, self.strap_spacing):
                col = s_col * self.strap_spacing

                tap_x = self.dummy.width * col
                tap_y = self.dummy.height * row

                self.tap_pos[row, col] = vector(tap_x, tap_y)
                self.tap_inst[row, col].place(self.tap_pos[row, col])
            tap_x = self.dummy.width * self.column_size + self.poly_tap.width
            tap_y = self.dummy.height * row

            self.tap_pos[row, self.column_size] = vector(tap_x, tap_y)
            self.tap_inst[row, self.column_size].place(self.tap_pos[row, self.column_size])
        offset=vector(0, 0),
        

    def place_rails(self):
        
        #self.gnd_rail_inst = self.add_inst(name="gnd", mod=self.gnd_rail)
        #self.connect_inst([])
        print (self.mcon_width)
        rail_start = vector(-self.dummy.width / 2 , self.cell_inst[self.row_size - 1,0].uy() )
        rail_end = vector(self.dummy.height * (self.row_size ), self.cell_inst[self.row_size - 1,0].uy())

        self.add_layout_pin_rect_ends(  name="gnd",
                                        layer="m1",
                                        start=rail_start,
                                        end=rail_end)

    def place_ptx(self):
        self.cell_pos = {}

        # rows are bitlines
        for row in range(self.row_size):
            # columns are word lines
            for col in range(self.column_size):
                
                cell_x = (self.dummy.width)  * col 
                cell_y = row * (self.dummy.height)

                self.cell_pos[row, col] = vector(cell_x, cell_y)
                self.cell_inst[row, col].place(self.cell_pos[row, col], rotate=90)
                #cell_x = self.cell.width  * col
                #cell_y = self.cell.height * row
                #print(self.nmos.height + self.nmos.poly_extend_active)
                if(self.data[row][col] == 1):

                    pass
                    
                    
                    
                    
                    #self.add_label("S_{}_{}".format(row,col), self.route_layer, self.cell_inst[row, col].center())
                    #self.add_label("D", self.route_layer, self.cell_inst[row, col].center())

                #else:
                    
                    #poly_offset = (self.nmos.contact_offset + vector(0.5 * self.nmos.active_contact.width + 0.5 * self.nmos.poly_width + self.nmos.active_contact_to_gate, 0)) + (0, cell_y)
                    #poly_offset = (cell_x, cell_y)
                    #print(cell_x,cell_y)
                    #self.add_rect(layer="poly",
                    #             offset=poly_offset,
                    #             width=self.nmos.height + self.nmos.poly_extend_active,
                    #             height=self.nmos.poly_width
                    #             )
                    


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
