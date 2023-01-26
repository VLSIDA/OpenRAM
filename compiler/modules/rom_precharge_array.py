# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from math import ceil
from openram.base import geometry
from openram.base import design
from openram.sram_factory import factory
from openram.base import vector
from openram.tech import layer, drc



class rom_precharge_array(design):
    """
    An array of inverters to create the inverted address lines for the rom decoder
    """
    def __init__(self, cols, name="", route_layer="li", strap_spacing=None, strap_layer="m2", tap_direction="row"):
        self.cols = cols
        self.route_layer = route_layer
        self.strap_layer = strap_layer
        self.tap_direction = tap_direction

        if self.route_layer == "m1" :
            self.supply_layer = "li"
        else:
            self.supply_layer = "m1"

        if name=="":
            name = "rom_inv_array_{0}".format(cols)

        if strap_spacing != None:
            self.strap_spacing = strap_spacing 
        else:
            self.strap_spacing = 0

        
        if strap_spacing != 0:
            self.num_straps = ceil(self.cols / self.strap_spacing)
            self.array_col_size = self.cols + self.num_straps  
        else:
            self.num_straps = 0
            self.array_col_size = self.cols

        super().__init__(name)
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.create_modules()
        self.add_pins()
        self.create_instances()
        


    def create_layout(self):
        self.width = self.cols * self.pmos.width 
        self.height = self.pmos.width
        self.place_instances()
        self.create_layout_pins()
        self.route_supply()
        self.connect_taps()
        
        self.add_boundary()
        self.extend_well()


    def add_boundary(self):
        # self.translate_all(self.well_ll)
        ur = self.find_highest_coords()
        self.add_label(layer="nwell", text="upper right",offset=ur)
        # ur = vector(ur.x, ur.y - self.well_ll.y)
        super().add_boundary(vector(0, 0), ur)
        self.height = ur.y 
        self.width = ur.x

    def create_modules(self):

        self.pmos = factory.create(module_type="rom_precharge_cell", module_name="precharge_cell", route_layer=self.route_layer, supply_layer=self.supply_layer)

        # For layout constants
        self.dummy = factory.create(module_type="rom_base_cell")

        self.poly_tap = factory.create(module_type="rom_poly_tap", tx_type="pmos", add_tap=(self.tap_direction == "col"))

    def add_pins(self):
        for col in range(self.cols):
            self.add_pin("pre_bl{0}_out".format(col), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gate", "INPUT")

    def create_instances(self):
        self.array_insts = []
        self.pmos_insts = []
        self.tap_insts = []

        self.create_poly_tap(-1)
        for col in range(self.cols):
            
            if col % self.strap_spacing  == 0:
                self.create_poly_tap(col)
            self.create_precharge_tx(col)

            

    def create_precharge_tx(self, col):
        name = "Xpmos_c{0}".format(col)
        pmos = self.add_inst(name=name, mod=self.pmos)
        self.array_insts.append(pmos)
        self.pmos_insts.append(pmos)
        bl = "pre_bl{0}_out".format(col)
        self.connect_inst(["vdd", "gate", bl])

    def create_poly_tap(self, col):
        name = "tap_c{}".format( col)
        new_tap = self.add_inst(name=name, mod=self.poly_tap)
        self.tap_insts.append(new_tap)
        self.connect_inst([])

    def place_instances(self):
        self.add_label("ZERO", self.route_layer)

        self.array_pos = []
        strap_num = 1     
        cell_y = 0  
        # columns are bit lines4
        cell_x = 0

        self.tap_insts[0].place(vector(cell_x, cell_y))

        for col in range(self.cols):
            
            if col % self.strap_spacing == 0:
                self.tap_insts[strap_num].place(vector(cell_x, cell_y))
                strap_num += 1

                if self.tap_direction == "col":
                        cell_x += self.poly_tap.pitch_offset


            # if col % self.strap_spacing == 0 :
            #     self.tap_insts[strap_num].place(vector(cell_x, cell_y))
            #     self.add_label("debug", "li", vector(cell_x, cell_y))
            #     cell_x += self.poly_tap.width
                
            self.pmos_insts[col].place(vector(cell_x, cell_y))
            self.add_label("debug", "li", vector(cell_x, cell_y))
            cell_x += self.pmos.width
            

    def create_layout_pins(self):
        self.copy_layout_pin(self.tap_insts[0], "poly_tap", "gate")
        for col in range(self.cols):
            source_pin = self.pmos_insts[col].get_pin("D")
            bl = "pre_bl{0}_out".format(col)
            self.add_layout_pin_rect_center(bl, self.route_layer, source_pin.center())
        

    def route_supply(self):

        # self.vdd = self.add_layout_pin_segment_center("vdd", self.supply_layer, start, end)
        # vdd = [self.pmos_insts[i].get_pin("vdd") for i in range(self.cols)]routeroute_horizon_horizon
        self.route_horizontal_pins("vdd", insts=self.pmos_insts)




    def connect_taps(self):
        array_pins = [self.tap_insts[i].get_pin("poly_tap") for i in range(len(self.tap_insts))]

        self.connect_row_pins(layer=self.strap_layer, pins=array_pins, name=None, round=False)

    def extend_well(self):
        self.well_offset = self.pmos.tap_offset
        well_y = self.pmos_insts[0].get_pin("vdd").cy() - 0.5 * self.nwell_width

        well_y = self.get_pin("vdd").cy() - 0.5 * self.nwell_width
        well_ll = vector(0, well_y)

        self.add_rect("nwell", well_ll, self.width , self.height - well_y)
