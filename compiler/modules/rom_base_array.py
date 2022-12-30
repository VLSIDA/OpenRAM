# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#


import math
from .bitcell_base_array import bitcell_base_array
from openram.base import vector
from openram import OPTS
from openram.sram_factory import factory 
from openram.tech import drc

class rom_base_array(bitcell_base_array):

    def __init__(self, rows, cols, strap_spacing, bitmap, name="", column_offset=0, route_layer="li", output_layer="m2", pitch_match=False):

        super().__init__(name=name, rows=rows, cols=cols, column_offset=column_offset)

        self.data = bitmap
        self.pitch_match = pitch_match
        self.route_layer = route_layer
        self.output_layer = output_layer
        self.strap_spacing = strap_spacing 
        self.data_col_size = self.column_size
        if strap_spacing != 0:
            self.array_col_size = self.column_size + math.ceil(self.column_size / strap_spacing)      
        else:
            self.array_col_size = self.column_size
        self.create_all_bitline_names()
        self.create_all_wordline_names()
        self.create_netlist()
        self.create_layout()
        

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        
        self.create_cell_instances()
        self.create_precharge_inst()
        

    def create_layout(self):
        self.create_layout_constants()
        self.place_array()
        if self.pitch_match:
            self.route_pitch_offsets()
        self.place_precharge()
        self.place_wordline_contacts()
        self.place_bitline_contacts()

        
        self.place_rails()
        self.route_precharge()
        
        self.add_boundary()
        self.add_label("ARRAY ZERO", self.route_layer)
        self.add_label("array height", self.route_layer, [0, self.height])

        
        
    #def add_pins(self):
    def add_boundary(self):
        ll = self.find_lowest_coords()
        bottom_offset = - self.dummy.nmos.end_to_contact + self.precharge_inst.offset.y
        m1_offset = self.m1_width
        self.translate_all(vector(0, ll.y + 0.5 * m1_offset))
        ur = self.find_highest_coords()
        
        ur = vector(ur.x, ur.y - self.m1_width)
        #super().add_boundary(ll=vector(lowerx, lowery), ur=vector(upperx, uppery))
        super().add_boundary(vector(0, 0), ur)
        self.width = ur.x
        self.height = ur.y 

        
    def add_modules(self):

        # dummy cell, "dummy" cells represent 0
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

        self.zero_tap = factory.create(module_type="rom_poly_tap", strap_length=0)
        

        self.precharge_array = factory.create(module_type="rom_precharge_array", cols=self.column_size, strap_spacing=self.strap_spacing, route_layer=self.route_layer)


    def create_layout_constants(self):
        self.route_width = drc("minwidth_" + self.route_layer)

        self.route_pitch = drc("{0}_to_{0}".format(self.route_layer))


    def add_pins(self):
        for bl_name in self.get_bitline_names():
            self.add_pin(bl_name, "INOUT")
        for wl_name in self.get_wordline_names():
            self.add_pin(wl_name, "INPUT")
        self.add_pin("precharge_gate", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def create_cell_instances(self):
        self.tap_inst = {}
        self.cell_inst = {}
        self.cell_list = []
        self.current_row = 0
        #list of current bitline interconnect nets, starts as the same as the bitline list and is updated when new insts of cells are added
        self.int_bl_list = self.bitline_names[0].copy()
        #When rotated correctly rows are word lines
        for row in range(self.row_size):
            row_list = []

            # for each new strap placed, offset the column index refrenced to get correct bit in the data array
            # cols are bit lines
            strap_row = False
            pre_strap_row = False
            if row % self.strap_spacing == 0 and self.pitch_match:
                strap_row = True
            if (row + 1) % self.strap_spacing == 0 and self.pitch_match:
                pre_strap_row = True
            for col in range(self.column_size):
                
                if col % self.strap_spacing == 0:

                    name = "tap_r{0}_c{1}".format(row, col)
                    #print("tap instance added at c{0}, r{1}".format(col, row))
                    self.tap_inst[row, col]=self.add_inst(name=name, mod=self.poly_tap)
                    self.connect_inst([])
                    
                name = "bit_r{0}_c{1}".format(row, col)

                if self.data[row][col] == 1:
                    # if dummy/0 cell above and below a 1, add a tx with contacts on both drain and source 
                    # if the first row and a 0 above, add both contacts
                    # if the last row and 0 below add both contacts
                    if  (row < self.row_size - 1 and row > 0 and self.data[row + 1][col] == 0 and self.data[row - 1][col] == 0) or \
                        (row == self.row_size - 1 and self.data[row - 1][col] == 0) or \
                        (row == 0 and self.data[row + 1][col] == 0) or \
                        (row < self.row_size - 1 and self.data[row + 1][col] == 0 and strap_row) or \
                        (row > 0 and self.data[row - 1][col] == 0 and pre_strap_row):
                        
                        new_inst = self.add_inst(name=name, mod=self.cell_ac)
                        
                    # if dummy/0 is below and not above, add a source contact
                    # if in the first row, add a source contact
                    elif (row > 0 and self.data[row - 1][col] == 0) or \
                         (row == 0) or \
                         (strap_row):

                        new_inst=self.add_inst(name=name, mod=self.cell_sc)

                    elif (row < self.row_size - 1 and self.data[row + 1][col] == 0) or \
                         (row == self.row_size - 1) or \
                          (pre_strap_row):          
                        new_inst=self.add_inst(name=name, mod=self.cell_dc)

                    else:
                        new_inst=self.add_inst(name=name, mod=self.cell_nc)

                    if row == self.row_size - 1 or self.get_next_cell_in_bl(row, col) == -1:
                        
                        bl_l = self.int_bl_list[col]
                        bl_h = "gnd" 
                    # elif first_in_col:
                    #     bl_l = self.bitline_names[0][col]
                    #     int_bl_list[col] = "bl_int_{0}_{1}".format(row, col)
                    #     bl_h = int_bl_list[col]
                    #     first_in_col = False
                    else:
                        bl_l = self.int_bl_list[col]
                        self.int_bl_list[col] = "bl_int_{0}_{1}".format(row, col)
                        bl_h = self.int_bl_list[col]
                    
                    
                    self.cell_inst[row, col] = new_inst
                    self.connect_inst([bl_h, bl_l, self.wordline_names[0][row], "gnd"])                    
                    

                else: 
                    new_inst = self.add_inst(name=name, mod=self.dummy)
                    self.cell_inst[row, col] = new_inst
                    self.connect_inst([])
                    
                # when col = 0 bl_h is connected to vdd, otherwise connect to previous bl connection
                # when col = col_size - 1 connected column_sizeto gnd otherwise create new bl connection
                # 
                

                row_list.append(new_inst)

                
            name = "tap_r{0}_c{1}".format(row, self.array_col_size)
            #print(*row_list)
            self.tap_inst[row, self.column_size]=self.add_inst(name=name, mod=self.zero_tap)
            self.connect_inst([])

            self.cell_list.append(row_list)


    def create_precharge_inst(self):
        prechrg_pins = self.bitline_names[0].copy()

        for bl in range(self.column_size):
            # if the internal bl was never updated there are no active cells in the bitline, so it should route straight to ground"
            if self.int_bl_list[bl] == prechrg_pins[bl]:
                prechrg_pins[bl] = "gnd"
        
        prechrg_pins.append("precharge_gate")
        prechrg_pins.append("vdd")
        self.precharge_inst = self.add_inst(name="decode_array_precharge", mod=self.precharge_array)
        self.connect_inst(prechrg_pins)



    def create_all_bitline_names(self):
        for col in range(self.column_size):
            for port in self.all_ports:
                self.bitline_names[port].extend(["bl_{0}_{1}".format(port, col)])
        # Make a flat list too
        self.all_bitline_names = [x for sl in zip(*self.bitline_names) for x in sl]

        

    def place_rails(self):

        spacing = self.route_pitch
        
        rail_y = self.cell_list[self.row_size - 1][0].offset.y + self.dummy.base_width + spacing
        # self.dummy.height * (self.row_size) 
        start_x = self.get_pin(self.bitline_names[0][0]).cx()
            # self.cell_list[self.row_size - 1][0].offset.x
        end_x = self.get_pin(self.bitline_names[0][self.column_size - 1]).cx()
            # self.cell_list[self.row_size - 1][self.column_size - 1].offset.x
        #self.dummy.height * self.row_size
        #self.cell_inst[self.row_size - 1,0].uy() 
        rail_start = vector(start_x , rail_y)
        rail_end = vector(end_x, rail_y)

        self.gnd = self.add_layout_pin_rect_ends(name="gnd",
                                        layer="m1",
                                        start=rail_start,
                                        end=rail_end)

        for bl in range(self.column_size):
            drain_pin = self.cell_list[self.row_size - 1][bl].get_pin("D")
            via_pos = vector(drain_pin.cx(), rail_y)
            self.add_segment_center(self.route_layer, drain_pin.center(), via_pos)

            
            self.add_via_stack_center(via_pos, self.route_layer, "m1", ["H", "V"])
        

    def place_array(self):
        self.cell_pos = {}
        self.strap_pos = {}
        # rows are wordlines

        pitch_offset = 0
        for row in range(self.row_size):
            
            if row % self.strap_spacing == 0 and row != 0 and self.pitch_match:
                pitch_offset += self.poly_tap.width
            
            cell_y = row * (self.dummy.height) + pitch_offset
            
            cell_x = 0
            for col in range(self.column_size):                    

                if col % self.strap_spacing == 0:
                    self.strap_pos[row, col] = vector(cell_x, cell_y)
                    self.tap_inst[row, col].place(self.strap_pos[row, col])
                    cell_x += self.poly_tap.width
                    
                self.cell_pos[row, col] = vector(cell_x, cell_y)
                self.cell_inst[row, col].place(self.cell_pos[row, col])
                cell_x += self.dummy.width
                self.add_label("debug", "li", self.cell_pos[row, col])

            
            self.strap_pos[row, self.column_size] = vector(cell_x, cell_y)
            self.tap_inst[row, self.column_size].place(self.strap_pos[row, self.column_size])


            # tap_pin = self.cell_inst[row, self.array_col_size].get_pin("poly_tap").center()
            # self.add_layout_pin_rect_center("wl{}".format(row), "m2", tap_pin)
    

    def route_pitch_offsets(self):

        for row in range(0  , self.row_size, self.strap_spacing):
            if row != 0:
                for col in range(self.column_size):
                    source = self.cell_inst[row, col].get_pin("S")
                    drain = self.cell_inst[row - 1, col].get_pin("D")

                    start = vector(drain.cx(), source.cy())
                    end = drain.center()
                    self.add_segment_center(self.route_layer, start, end)


    def place_precharge(self):

        self.precharge_offset = vector(0,  - self.precharge_inst.height - self.dummy.nmos.end_to_contact - 2 * drc["nwell_enclose_active"])

        self.precharge_inst.place(offset=self.precharge_offset)

        self.copy_layout_pin(self.precharge_inst, "vdd")
        self.copy_layout_pin(self.precharge_inst, "gate", "precharge")

    
                    
    def place_wordline_contacts(self):

        width = self.route_width
        
        height = self.route_width

        offset = vector(self.poly_contact.width * 0.5, self.dummy.poly.offset.y)

        for wl in range(self.row_size):
            
            poly_via = self.tap_inst[wl, 0].get_pin("via")
            self.copy_layout_pin(self.tap_inst[wl, 0], "via", self.wordline_names[0][wl])
            # self.add_via_stack_center(poly_via.center(), "m1", self.output_layer)

        # self.create_horizontal_pin_bus(self.route_layer, offset=corrected_offset, names=self.wordline_names[0], pitch=self.dummy.height, length=None)

    def place_bitline_contacts(self):

        rail_y = self.precharge_inst.get_pin("vdd").cy()

        for bl in range(self.column_size):

            src_pin = self.cell_list[0][bl].get_pin("S")
            prechg_pin_name = "pre_bl{0}_out".format(bl)
            pre_pin = self.precharge_inst.get_pin(prechg_pin_name)

            middle_offset = (src_pin.cy() - pre_pin.cy() ) * 0.5

            corrected = vector(src_pin.cx(), src_pin.cy() - middle_offset)
            self.add_via_stack_center(corrected, self.route_layer, self.output_layer)

            output_pos = vector(corrected.x, rail_y)

            self.add_segment_center(self.output_layer, corrected, output_pos)
            
            self.add_layout_pin_rect_center(self.bitline_names[0][bl], self.output_layer, output_pos )



    def route_precharge(self):
        for bl in range(self.column_size):
            bl_pin = self.cell_list[0][bl].get_pin("S")
            prechg_pin = "pre_bl{0}_out".format(bl)
            pre_out_pin = self.precharge_inst.get_pin(prechg_pin)

            bl_start = bl_pin.center()
            bl_end = vector(bl_start.x, pre_out_pin.cy())

            self.add_segment_center(self.route_layer, bl_start, bl_end)

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
    
    
