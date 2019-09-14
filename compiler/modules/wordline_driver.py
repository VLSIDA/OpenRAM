# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from tech import drc, parameter
import debug
import design
import contact
from math import log
from math import sqrt
import math
from vector import vector
from sram_factory import factory
from globals import OPTS

class wordline_driver(design.design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """

    def __init__(self, name, rows, cols):
        design.design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))
        
        self.rows = rows
        self.cols = cols
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_drivers()
        
    def create_layout(self):
        self.place_drivers()
        self.route_layout()
        self.route_vdd_gnd()
        self.offset_all_coordinates()
        self.add_boundary()
        self.DRC_LVS()
        
    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.rows):
            self.add_pin("in_{0}".format(i), "INPUT")
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("wl_{0}".format(i), "OUTPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def add_modules(self):
        # This is just used for measurements,
        # so don't add the module

        self.inv = factory.create(module_type="pdriver",
                                  fanout=self.cols,
                                  neg_polarity=True)
        self.add_mod(self.inv)

        self.inv_no_output = factory.create(module_type="pinv",
                                            route_output=False)
        self.add_mod(self.inv_no_output)
        
        self.nand2 = factory.create(module_type="pnand2")
        self.add_mod(self.nand2)
        

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # Find the x offsets for where the vias/pins should be placed
        a_xoffset = self.nand_inst[0].rx()
        b_xoffset = self.inv2_inst[0].lx()
        for num in range(self.rows):
            # this will result in duplicate polygons for rails, but who cares
            
            # use the inverter offset even though it will be the nand's too
            (gate_offset, y_dir) = self.get_gate_offset(0, self.inv.height, num)

            # Route both supplies
            for name in ["vdd", "gnd"]:
                supply_pin = self.inv2_inst[num].get_pin(name)

                # Add pins in two locations
                for xoffset in [a_xoffset, b_xoffset]:
                    pin_pos = vector(xoffset, supply_pin.cy())
                    self.add_power_pin(name, pin_pos)
            


    def create_drivers(self):
        self.nand_inst = []            
        self.inv2_inst = []            
        for row in range(self.rows):
            name_nand = "wl_driver_nand{}".format(row)
            name_inv2 = "wl_driver_inv{}".format(row)

            # add nand 2
            self.nand_inst.append(self.add_inst(name=name_nand,
                                                mod=self.nand2))
            self.connect_inst(["en",
                               "in_{0}".format(row),
                               "wl_bar_{0}".format(row),
                               "vdd", "gnd"])
            # add inv2
            self.inv2_inst.append(self.add_inst(name=name_inv2,
                                                mod=self.inv))
            self.connect_inst(["wl_bar_{0}".format(row),
                               "wl_{0}".format(row),
                               "vdd", "gnd"])


    def place_drivers(self):
        nand2_xoffset = 2*self.m1_width + 5*self.m1_space 
        inv2_xoffset = nand2_xoffset + self.nand2.width
        
        self.width = inv2_xoffset + self.inv.width
        self.height = self.inv.height * self.rows
        
        for row in range(self.rows):
            if (row % 2):
                y_offset = self.inv.height*(row + 1)
                inst_mirror = "MX"
            else:
                y_offset = self.inv.height*row
                inst_mirror = "R0"

            nand2_offset=[nand2_xoffset, y_offset]
            inv2_offset=[inv2_xoffset, y_offset]
            
            # add nand 2
            self.nand_inst[row].place(offset=nand2_offset,
                                      mirror=inst_mirror)
            # add inv2
            self.inv2_inst[row].place(offset=inv2_offset,
                                      mirror=inst_mirror)


    def route_layout(self):
        """ Route all of the signals """

        # Wordline enable connection
        en_pin=self.add_layout_pin(text="en",
                                   layer="metal2",
                                   offset=[self.m1_width + 2*self.m1_space,0],
                                   width=self.m2_width,
                                   height=self.height)
        
        
        for row in range(self.rows):
            nand_inst = self.nand_inst[row]
            inv2_inst = self.inv2_inst[row]
            
            # en connection
            a_pin = nand_inst.get_pin("A")
            a_pos = a_pin.lc()
            clk_offset = vector(en_pin.bc().x,a_pos.y)
            self.add_segment_center(layer="metal1",
                                    start=clk_offset,
                                    end=a_pos)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=clk_offset)

            # Nand2 out to 2nd inv
            zr_pos = nand_inst.get_pin("Z").rc()
            al_pos = inv2_inst.get_pin("A").lc()
            # ensure the bend is in the middle 
            mid1_pos = vector(0.5*(zr_pos.x+al_pos.x), zr_pos.y)
            mid2_pos = vector(0.5*(zr_pos.x+al_pos.x), al_pos.y)
            self.add_path("metal1", [zr_pos, mid1_pos, mid2_pos, al_pos])

            # connect the decoder input pin to nand2 B
            b_pin = nand_inst.get_pin("B")
            b_pos = b_pin.lc()
            # needs to move down since B nand input is nearly aligned with A inv input
            up_or_down = self.m2_space if row%2 else -self.m2_space
            input_offset = vector(0,b_pos.y + up_or_down) 
            mid_via_offset = vector(clk_offset.x,input_offset.y) + vector(0.5*self.m2_width+self.m2_space+0.5*contact.m1m2.width,0) 
            # must under the clk line in M1
            self.add_layout_pin_segment_center(text="in_{0}".format(row),
                                               layer="metal1",
                                               start=input_offset,
                                               end=mid_via_offset)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=mid_via_offset,
                                directions=("V","V"))

            # now connect to the nand2 B
            self.add_path("metal2", [mid_via_offset, b_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=b_pos - vector(0.5*contact.m1m2.height,0),
                                directions=("H","H"))


            # output each WL on the right
            wl_offset = inv2_inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="wl_{0}".format(row),
                                               layer="metal1",
                                               start=wl_offset,
                                               end=wl_offset-vector(self.m1_width,0))

    def determine_wordline_stage_efforts(self, external_cout, inp_is_rise=True):
        """Follows the clk_buf to a wordline signal adding each stages stage effort to a list"""
        stage_effort_list = []
        
        stage1_cout = self.inv.get_cin()
        stage1 = self.nand2.get_stage_effort(stage1_cout, inp_is_rise)
        stage_effort_list.append(stage1)
        last_stage_is_rise = stage1.is_rise
        
        stage2 = self.inv.get_stage_efforts(external_cout, last_stage_is_rise)
        stage_effort_list.extend(stage2)
        
        return stage_effort_list
        
    def get_wl_en_cin(self):
        """Get the relative capacitance of all the enable connections in the bank"""
        #The enable is connected to a nand2 for every row.
        total_cin = self.nand2.get_cin() * self.rows
        return total_cin
