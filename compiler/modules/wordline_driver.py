from tech import drc, parameter
import debug
import design
import contact
from math import log
from math import sqrt
import math
from pinv import pinv
from pnand2 import pnand2
from vector import vector
from globals import OPTS

class wordline_driver(design.design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """

    def __init__(self, rows):
        design.design.__init__(self, "wordline_driver")

        self.rows = rows
        
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
        self.DRC_LVS()
        
    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.rows):
            self.add_pin("in[{0}]".format(i))
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("wl[{0}]".format(i))
        self.add_pin("en")
        self.add_pin("vdd")
        self.add_pin("gnd")


    def add_modules(self):
        self.inv = pinv()
        self.add_mod(self.inv)

        self.inv_no_output = pinv(route_output=False)
        self.add_mod(self.inv_no_output)
        
        self.nand2 = pnand2()
        self.add_mod(self.nand2)
        
        from importlib import reload
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()
        self.add_mod(self.bitcell)

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # Find the x offsets for where the vias/pins should be placed
        a_xoffset = self.inv1_inst[0].rx()
        b_xoffset = self.inv2_inst[0].lx()
        for num in range(self.rows):
            # this will result in duplicate polygons for rails, but who cares
            
            # use the inverter offset even though it will be the nand's too
            (gate_offset, y_dir) = self.get_gate_offset(0, self.inv.height, num)

            # Route both supplies
            for n in ["vdd", "gnd"]:
                supply_pin = self.inv2_inst[num].get_pin(n)

                # Add pins in two locations
                for xoffset in [a_xoffset, b_xoffset]:
                    pin_pos = vector(xoffset, supply_pin.cy())
                    self.add_via_center(layers=("metal1", "via1", "metal2"),
                                        offset=pin_pos,
                                        rotate=90)
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_pos,
                                        rotate=90)
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="metal3",
                                                    offset=pin_pos)
            


    def create_drivers(self):
        self.inv1_inst = []
        self.nand_inst = []            
        self.inv2_inst = []            
        for row in range(self.rows):
            name_inv1 = "wl_driver_inv_en{}".format(row)
            name_nand = "wl_driver_nand{}".format(row)
            name_inv2 = "wl_driver_inv{}".format(row)

            # add inv1 based on the info above
            self.inv1_inst.append(self.add_inst(name=name_inv1,
                                               mod=self.inv_no_output))
            self.connect_inst(["en",
                               "en_bar[{0}]".format(row),
                               "vdd", "gnd"])
            # add nand 2
            self.nand_inst.append(self.add_inst(name=name_nand,
                                                mod=self.nand2))
            self.connect_inst(["en_bar[{0}]".format(row),
                               "in[{0}]".format(row),
                               "wl_bar[{0}]".format(row),
                               "vdd", "gnd"])
            # add inv2
            self.inv2_inst.append(self.add_inst(name=name_inv2,
                                                mod=self.inv))
            self.connect_inst(["wl_bar[{0}]".format(row),
                               "wl[{0}]".format(row),
                               "vdd", "gnd"])


    def place_drivers(self):
        inv1_xoffset = 2*self.m1_width + 5*self.m1_space
        nand2_xoffset = inv1_xoffset + self.inv.width
        inv2_xoffset = nand2_xoffset + self.nand2.width
        
        self.width = inv2_xoffset + self.inv.height
        if self.bitcell.height > self.inv.height:
            self.height = self.bitcell.height * self.rows
            driver_height = self.bitcell.height
        else:
            self.height = self.inv.height * self.rows
            driver_height = self.inv.height
        
        for row in range(self.rows):
            if (row % 2):
                y_offset = driver_height*(row + 1)
                inst_mirror = "MX"
            else:
                y_offset = driver_height*row
                inst_mirror = "R0"

            inv1_offset = [inv1_xoffset, y_offset]
            nand2_offset=[nand2_xoffset, y_offset]
            inv2_offset=[inv2_xoffset, y_offset]
            
            # add inv1 based on the info above
            self.inv1_inst[row].place(offset=inv1_offset,
                                      mirror=inst_mirror)
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
            inv1_inst = self.inv1_inst[row]
            nand_inst = self.nand_inst[row]
            inv2_inst = self.inv2_inst[row]
            
            # en connection
            a_pin = inv1_inst.get_pin("A")
            a_pos = a_pin.lc()
            clk_offset = vector(en_pin.bc().x,a_pos.y)
            self.add_segment_center(layer="metal1",
                                    start=clk_offset,
                                    end=a_pos)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=clk_offset)

            # first inv to nand2 A
            zb_pos = inv1_inst.get_pin("Z").bc()
            zu_pos = inv1_inst.get_pin("Z").uc()
            bl_pos = nand_inst.get_pin("A").lc()
            br_pos = nand_inst.get_pin("A").rc()
            self.add_path("metal1", [zb_pos, zu_pos, bl_pos, br_pos])

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
            self.add_layout_pin_segment_center(text="in[{0}]".format(row),
                                               layer="metal1",
                                               start=input_offset,
                                               end=mid_via_offset)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=mid_via_offset)

            # now connect to the nand2 B
            self.add_path("metal2", [mid_via_offset, b_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=b_pos - vector(0.5*contact.m1m2.height,0),
                                rotate=90)


            # output each WL on the right
            wl_offset = inv2_inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="wl[{0}]".format(row),
                                               layer="metal1",
                                               start=wl_offset,
                                               end=wl_offset-vector(self.m1_width,0))


    def analytical_delay(self, slew, load=0):
        # decode -> net
        decode_t_net = self.nand2.analytical_delay(slew, self.inv.input_load())

        # net -> wl
        net_t_wl = self.inv.analytical_delay(decode_t_net.slew, load)

        return decode_t_net + net_t_wl

        
    def input_load(self):
        return self.nand2.input_load()
