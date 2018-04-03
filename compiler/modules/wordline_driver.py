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
        self.add_pins()
        self.design_layout()
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

    def design_layout(self):
        self.add_layout()
        self.offsets_of_gates()
        self.create_layout()

    def add_layout(self):
        self.inv = pinv()
        self.add_mod(self.inv)

        self.inv_no_output = pinv(route_output=False)
        self.add_mod(self.inv_no_output)
        
        self.nand2 = pnand2()
        self.add_mod(self.nand2)




    def offsets_of_gates(self):
        self.x_offset0 = 2*self.m1_width + 5*self.m1_space
        self.x_offset1 = self.x_offset0 + self.inv.width
        self.x_offset2 = self.x_offset1 + self.nand2.width

        self.width = self.x_offset2 + self.inv.width
        self.height = self.inv.height * self.rows

    def create_layout(self):
        # Wordline enable connection
        en_pin=self.add_layout_pin(text="en",
                                   layer="metal2",
                                   offset=[self.m1_width + 2*self.m1_space,0],
                                   width=self.m2_width,
                                   height=self.height)
        
        self.add_layout_pin(text="gnd",
                            layer="metal1",
                            offset=[0, -0.5*self.m1_width],
                            width=self.x_offset0,
                            height=self.m1_width)
        
        for row in range(self.rows):
            name_inv1 = "wl_driver_inv_en{}".format(row)
            name_nand = "wl_driver_nand{}".format(row)
            name_inv2 = "wl_driver_inv{}".format(row)

            inv_nand2B_connection_height = (abs(self.inv.get_pin("Z").ll().y 
                                                - self.nand2.get_pin("B").ll().y)
                                            + self.m1_width)

            if (row % 2):
                y_offset = self.inv.height*(row + 1)
                inst_mirror = "MX"
                cell_dir = vector(0,-1)
                m1tm2_rotate=270
                m1tm2_mirror="R0"
            else:
                y_offset = self.inv.height*row
                inst_mirror = "R0"
                cell_dir = vector(0,1)
                m1tm2_rotate=90
                m1tm2_mirror="MX"

            name_inv1_offset = [self.x_offset0, y_offset]
            nand2_offset=[self.x_offset1, y_offset]
            inv2_offset=[self.x_offset2, y_offset]
            base_offset = vector(self.width, y_offset)

            # Extend vdd and gnd of wordline_driver
            yoffset = (row + 1) * self.inv.height - 0.5 * self.m1_width
            if (row % 2):
                pin_name = "gnd"
            else:
                pin_name = "vdd"
                
            self.add_layout_pin(text=pin_name,
                                layer="metal1",
                                offset=[0, yoffset],
                                width=self.x_offset0,
                                height=self.m1_width)
            
            
            # add inv1 based on the info above
            inv1_inst=self.add_inst(name=name_inv1,
                                    mod=self.inv_no_output,
                                    offset=name_inv1_offset,
                                    mirror=inst_mirror )
            self.connect_inst(["en",
                               "en_bar[{0}]".format(row),
                               "vdd", "gnd"])
            # add nand 2
            nand_inst=self.add_inst(name=name_nand,
                                    mod=self.nand2,
                                    offset=nand2_offset,
                                    mirror=inst_mirror)
            self.connect_inst(["en_bar[{0}]".format(row),
                               "in[{0}]".format(row),
                               "net[{0}]".format(row),
                               "vdd", "gnd"])
            # add inv2
            inv2_inst=self.add_inst(name=name_inv2,
                                mod=self.inv,
                                    offset=inv2_offset,
                                    mirror=inst_mirror)
            self.connect_inst(["net[{0}]".format(row),
                               "wl[{0}]".format(row),
                               "vdd", "gnd"])

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
            self.add_layout_pin_center_segment(text="in[{0}]".format(row),
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
            self.add_layout_pin_center_segment(text="wl[{0}]".format(row),
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
