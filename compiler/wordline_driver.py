from tech import drc, parameter
import debug
import design
from math import log
from math import sqrt
import math
from pinv import pinv
from nand_2 import nand_2
from vector import vector
from globals import OPTS
from contact import contact


class wordline_driver_unit(design.design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """
    def __init__(self, name, load_size = 8, create_layout = True):
        design.design.__init__(self, name)
        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        self.wl_driver_mults = 1
        self.add_pins()
        self.driver_size, self.nand_size = self.logic_effort_sizing(load_size)
        self.create_mods()
        self.offsets_of_gates()
        if create_layout == True:
            self.create_layout()
            self.DRC_LVS()

    def add_pins(self):
        # inputs to wordline_driver.
        self.add_pin("decode_out")
        # Outputs from wordline_driver.
        self.add_pin("wl")
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def splite_drivers(self, size_share_lst):
        self.driver = []
        for size_share in size_share_lst:
            driver_to_add = pinv(nmos_width=self.driver_size * size_share,
                                 beta=parameter["pinv_beta"])
            self.driver.append(driver_to_add)
        self.width = self.x_offset2 + self.driver[0].width
        self.create_inv_and_nand2()

    def arrange_drivers(self, gap_list):
        self.create_layout()
        if len(gap_list)+1 < len(self.driver):
            debug.error(" {0} gaps and {1} drivers".format(len(gap_list),
                                                           len(self.driver)))
        base_offset = vector(self.x_offset2, 0)
        for index in range(1,len(self.driver)):
            driver = self.driver[index]
            self.add_mod(driver)
            base_offset = base_offset + vector(gap_list[index-1],0) + vector(driver.width, 0)
            self.add_inst(name="Wordline_driver_inv[%d]" %index,
                          mod=driver,
                          offset=base_offset)
            self.connect_inst(["net",
                               "wl",
                               "vdd", "gnd"])
            # vdd
            start = base_offset
            end = start - vector(gap_list[index-1],0)
            self.add_path(layer="metal1",
                          coordinates = [start, end])
            # gnd
            start = start + vector(0, driver.height)
            end = start - vector(gap_list[index-1],0)
            self.add_path(layer="metal1",
                          coordinates = [start, end])
            self.rout_net_0(vector(self.x_offset2, 0), base_offset, driver)
            self.route_to_prev_WL(base_offset, driver, gap_list[index-1])


    def rout_net_0(self,first_driver_offset, extra_driver_offset, driver):
        m1m2_via = contact(layer_stack=("metal2", "via2", "metal3"))
        start = first_driver_offset + driver.A_position
        end = extra_driver_offset + driver.A_position
        
        self.add_path(layer=("metal3"),
                      coordinates=[start,end+ vector(m1m2_via.width,0)])
        for offset in [start, end]:
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset)
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=offset)

    def route_to_prev_WL(self,driver_offset, driver, array_to_driver):
        start = driver_offset + driver.Z_position \
                + vector(0,0.5*drc["minwidth_metal1"])
        end = driver_offset - vector(array_to_driver,0) \
              + vector(0, self.bitcell_chars["WL"][1])
        mid0 = start + vector(drc["metal1_to_metal1"],0)
        mid1 = vector(start.x,end.y) + vector(drc["minwidth_metal1"],
                                              0.5*drc["minwidth_metal1"])
        mid2 = vector(mid1.x, end.y) + vector(drc["minwidth_metal2"],0) 
        mid3 = driver_offset.scale(1,0) \
               - vector(drc["metal1_to_metal1"]+drc["minwidth_metal2"], 0) \
               + end.scale(0,1)

        self.add_path(layer=("metal1"),
                      coordinates=[start,mid0,mid1])

        m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        via_offset = mid1 - vector(0.5 * m1m2_via.width, 
                                   m1m2_via.height*0.5) \
                     + vector(0, m1m2_via.height * 0.5) \
                     - vector(0, 0.5*drc["minwidth_metal2"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=via_offset)
        self.add_path(layer=("metal2"),
                      coordinates=[mid1,mid3])

        via_offset = mid3 - vector(m1m2_via.width * 0.5, m1m2_via.height * 0.5) \
                     + vector(0, m1m2_via.height*0.5) \
                     - vector(0, 0.5*drc["minwidth_metal2"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=via_offset )   
        self.add_path(layer=("metal1"),
                      coordinates=[mid3,end]) 
            
    def create_mods(self):
        self.driver = pinv(nmos_width= self.driver_size,
                           beta=parameter["pinv_beta"])
        self.add_mod(self.driver)

        self.create_inv_and_nand2()

    def create_inv_and_nand2(self):
        self.inv = pinv(nmos_width=drc["minwidth_tx"],
                        beta=parameter["pinv_beta"])
        self.add_mod(self.inv)
        
        self.NAND2 = nand_2(nmos_width=self.nand_size)
        self.add_mod(self.NAND2)

    def get_sub_driver_width(self):
        sub_driver_width = []
        for driver in self.driver:
            sub_driver_width.append(driver.width)
        return sub_driver_width



    def logic_effort_sizing(self, load_size):
        nand_effort = (4.0/3.0)
        G = 1.0*nand_effort*1.0
        H = load_size *(2.0/3.0)
        F = G*H
        f = F**(1.0/3.0)
        y = load_size*1.0/f
        x = y *nand_effort/f
        driver_strength = int(x+1)*drc["minwidth_tx"] 
        NAND2_strength = int(y+1)*drc["minwidth_tx"]

        return driver_strength, NAND2_strength


    def offsets_of_gates(self):
        self.x_offset0 = 2 * drc["minwidth_metal1"] + 5 * drc["metal1_to_metal1"]
        self.x_offset1 = self.x_offset0 + self.inv.width
        self.x_offset2 = self.x_offset1 + self.NAND2.width

        self.width = self.x_offset2 + self.driver.width
        self.height = self.inv.height

        # Defining offset postions
        self.decode_out_positions = []
        self.clk_positions = []
        self.WL_positions = []
        self.vdd_positions = []
        self.gnd_positions = []

    def create_clk_connection(self):
        # Clk connection
        self.add_rect(layer="metal1",
                      offset=[drc["minwidth_metal1"] + 2 * drc["metal1_to_metal1"],
                              2 * drc["minwidth_metal1"]],
                      width=drc["minwidth_metal1"],
                      height=self.height + 4*drc["minwidth_metal1"])
        self.clk_positions.append([drc["minwidth_metal1"] + 2*drc["metal1_to_metal1"],
                                           self.height])
        self.add_label(text="clk",
                       layer="metal1",
                       offset=self.clk_positions[0])

    def extend_wordline_driver_vdd_gnd(self): 
        yoffset = self.inv.height - 0.5 * drc["minwidth_metal2"]
        self.add_rect(layer="metal2",
                      offset=[0, yoffset],
                      width=self.x_offset0,
                      height=drc["minwidth_metal2"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[drc["minwidth_metal1"], yoffset],
                      mirror="R90")
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[self.x_offset0 + drc["minwidth_metal1"],
                              yoffset],
                      mirror="R90")

        self.add_rect(layer="metal2",
                      offset=[0, - 0.5 * drc["minwidth_metal2"]],
                      width=self.x_offset0,
                      height=drc["minwidth_metal2"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[drc["minwidth_metal1"], - 0.5 * drc["minwidth_metal2"]],
                      mirror="R90")
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[self.x_offset0 + drc["minwidth_metal1"],
                              - 0.5 * drc["minwidth_metal2"]],
                      mirror="R90")

    def create_layout(self):
        self.create_clk_connection()
        self.extend_wordline_driver_vdd_gnd()
        inv_nand2B_connection_height = (abs(self.inv.Z_position.y 
                                                - self.NAND2.B_position.y)
                                            + drc["minwidth_metal1"])
        name_inv1_offset = [self.x_offset0, 0]
        nand2_offset=[self.x_offset1, 0]
        inv2_offset=[self.x_offset2, 0]

        # add inv1 based on the info above
        self.add_inst(name="Wordline_driver_inv_clk" ,
                      mod=self.inv,
                      offset=name_inv1_offset)
        self.connect_inst(["clk", "clk_bar",
                           "vdd", "gnd"])
        # add nand 2
        self.add_inst(name="Wordline_driver_nand" ,
                      mod=self.NAND2,
                      offset=nand2_offset)
        self.connect_inst(["decode_out",
                           "clk_bar",
                           "net",
                           "vdd", "gnd"])
        # add inv2
        if isinstance(self.driver, list):
            inv2 = self.driver[0]
        else:
            inv2 = self.driver
        self.add_mod(inv2)

        self.add_inst(name="Wordline_driver_inv" ,
                      mod=inv2,
                      offset=inv2_offset)
        self.connect_inst(["net",
                           "wl",
                           "vdd", "gnd"])
        # if driver is list we do diff

        # clk connection
        clk_offset= [drc["minwidth_metal1"] + 2 * drc["metal1_to_metal1"],
                     self.inv.A_position.y]
        self.add_rect(layer="metal1",
                      offset=clk_offset,
                      width=self.x_offset0 - 2*drc["metal1_to_metal1"],
                      height= drc["minwidth_metal1"])
        # first inv to nand2 B
        inv_to_nand2B_offset = [self.x_offset1 - drc["minwidth_metal1"],
                                self.NAND2.B_position.y]
        self.add_rect(layer="metal1",
                      offset=inv_to_nand2B_offset,
                      width=drc["minwidth_metal1"],
                      height=inv_nand2B_connection_height)
        # Nand2 out to 2nd inv
        nand2_to_2ndinv_offset =[self.x_offset2,
                                 self.NAND2.Z_position.y]
        self.add_rect(layer="metal1",
                      offset=nand2_to_2ndinv_offset,
                      width=drc["minwidth_metal1"],
                      height=drc["minwidth_metal1"])
        # nand2 A connection
        self.add_rect(layer="metal2",
                      offset=[0, self.NAND2.A_position.y],
                      width=self.x_offset1,
                      height= drc["minwidth_metal2"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[self.x_offset1,
                              self.NAND2.A_position.y],
                      rotate=90,
                      mirror="MX")
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=[0, 
                              self.NAND2.A_position.y])


        base_offset = vector(self.width, 0)

        self.decode_out_position = base_offset.scale(0,1)+self.NAND2.A_position.scale(0,1)
        self.WL_position = base_offset + inv2.Z_position.scale(0,1)
        self.vdd_position = base_offset + inv2.vdd_position.scale(0,1)
        self.gnd_position = base_offset + inv2.gnd_position.scale(0,1)
        self.add_label(text="decode_out",
                       layer="metal2",
                       offset=self.decode_out_position)
        self.add_rect(layer="metal1",
                      offset=self.WL_position,
                      width=drc["minwidth_metal1"],
                      height=drc["minwidth_metal1"])
        self.add_label(text="wl",
                       layer="metal1",
                       offset=self.WL_position)
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=self.gnd_position)
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.vdd_position)

    def add_extra_driver(self, driver_mults, start, array_gap, array_to_driver):
        self.wl_driver_mults = driver_mults
        for seg in range(1,driver_mults):
            seg_driver_width = self.driver.width
            extra_driver_offset= start + array_gap.scale(seg,0)
            self.add_extra_row_driver(extra_driver_offset, array_to_driver, seg)

    def get_1st_driver_width(self):
        if isinstance(self.driver, list):
            inv2 = self.driver[0]
        else:
            inv2 = self.driver
        return inv2.width

    def delay(self, slew, load=0):
        # decode_out -> net
        if self.wl_driver_mults == 1:
            decode_t_net = self.NAND2.delay(slew = slew, load = self.driver.input_load())
        else:
            net_wire = self.generate_rc_net(self.wl_driver_mults, self.net_wire_length, drc["minwidth_metal1"])
            net_wire.wire_c = self.driver.input_load() + net_wire.wire_c
            decode_t_net = self.NAND2.delay(slew = slew, load = net_wire.return_input_cap())
            wire_delay = net_wire.return_delay_over_wire(decode_t_net.slope)
            decode_t_net = decode_t_net + wire_delay
        # net -> wl
        net_t_wl = self.driver.delay(slew = decode_t_net.slew, load = load)

        result = decode_t_net + net_t_wl
        return result
    
    def input_load(self):
        return self.NAND2.input_load()


class wordline_driver(design.design):
    """
    Creates a single column of Wordline Driver Unit
    """
    def __init__(self, name, rows, load_size = 8, create_layout = True):
        design.design.__init__(self, name)
        self.rows = rows
        self.wl_driver_mults= 1

        self.add_pins()
        self.create_unit(load_size, create_layout)
        if create_layout:
            self.create_layout()
            self.DRC_LVS()

    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.rows):
            self.add_pin("decode_out[{0}]".format(i))
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("wl[{0}]".format(i))
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

        self.clk_positions = []
        self.WL_positions = []
        self.decode_out_positions = []
        self.vdd_positions = []
        self.gnd_positions = []
    
    def create_unit(self, load_size, create_layout):
        self.unit = wordline_driver_unit(name="wordline_driver_unit", 
                                         load_size=load_size,
                                         create_layout = create_layout)
        self.add_mod(self.unit)
        self.width = self.unit.width
        self.height = self.unit.inv.height * self.rows

    def create_layout(self):
        # Clk connection
        self.add_rect(layer="metal1",
                      offset=[drc["minwidth_metal1"] + 2 * drc["metal1_to_metal1"],
                              2 * drc["minwidth_metal1"]],
                      width=drc["minwidth_metal1"],
                      height=self.height + 4*drc["minwidth_metal1"])
        self.clk_positions.append([drc["minwidth_metal1"] + 2*drc["metal1_to_metal1"],
                                           self.height])
        self.add_label(text="clk",
                       layer="metal1",
                       offset=self.clk_positions[0])

        for row in range(self.rows):
            if (row % 2):
                yoffset = self.unit.height*(row + 1)
                inst_mirror = "MX"
                cell_dir = vector(1,-1)
            else:
                yoffset = self.unit.height*row
                inst_mirror = "R0"
                cell_dir = vector(1,1)
            name = "Wordline_driver_%d" % (row)
            self.add_inst(name=name,
                          mod=self.unit,
                          offset=vector(0,yoffset),
                          mirror=inst_mirror )
            self.connect_inst(["decode_out[%d]" % (row),
                               "wl[%d]" % (row),                               
                               "clk", "vdd", "gnd"])

            decode_pos = vector(0,yoffset) + self.unit.decode_out_position.scale(cell_dir)
            self.decode_out_positions.append(decode_pos)
            self.add_label(text="decode_out[%d]" % (row),
                           layer="metal2",
                           offset=decode_pos)

            wl_pos = vector(0,yoffset) + self.unit.WL_position.scale(cell_dir)
            self.WL_positions.append(wl_pos)
            self.add_label(text="wl[%d]" % (row),
                           layer="metal1",
                           offset=wl_pos)

            vdd_pos = vector(0,yoffset) + self.unit.vdd_position.scale(cell_dir)
            self.vdd_positions.append(vdd_pos)
            self.add_label(text="vdd",
                           layer="metal1",
                           offset=vdd_pos)

            gnd_pos = vector(0,yoffset) + self.unit.gnd_position.scale(cell_dir)
            self.gnd_positions.append(gnd_pos)
            self.add_label(text="gnd",
                           layer="metal1",
                           offset=gnd_pos)

    def get_1st_driver_width(self):
        result = self.unit.get_1st_driver_width()
        return result

    def splite_drivers(self, share_lst):
        self.width = self.unit.width
        self.unit.splite_drivers(share_lst)

    def arrange_drivers(self, gap_lst):
        self.unit.arrange_drivers(gap_lst)
        self.create_layout()

    def get_gaps_width(self):
        return self.unit.get_sub_driver_width()
