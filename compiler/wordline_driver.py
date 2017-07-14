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

class wordline_driver(design.design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """


    def __init__(self, name, rows, load_size = 8):
        design.design.__init__(self, name)
        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_chars = self.mod_bitcell.chars

        self.rows = rows
        self.wl_driver_mults= 1
        self.add_pins()
        self.design_layout(load_size)
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

    def design_layout(self, load_size):
        driver_size, nand_size = self.logic_effort_sizing(load_size)
        self.add_layout(driver_size, nand_size)
        self.offsets_of_gates()
        self.create_layout()

    def add_layout(self, driver_size, nand_size):
        self.inv = pinv(nmos_width=drc["minwidth_tx"],
                        beta=parameter["pinv_beta"])
        self.add_mod(self.inv)

        self.driver = pinv(nmos_width=driver_size,
                           beta=parameter["pinv_beta"])
        self.add_mod(self.driver)

        self.NAND2 = nand_2(nmos_width=nand_size)
        self.add_mod(self.NAND2)

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
        self.height = self.inv.height * self.rows

        # Defining offset postions
        self.decode_out_positions = []
        self.clk_positions = []
        self.WL_positions = []
        self.vdd_positions = []
        self.gnd_positions = []

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
            name_inv1 = "Wordline_driver_inv_clk%d" % (row)
            name_nand = "Wordline_driver_nand%d" % (row)
            name_inv2 = "Wordline_driver_inv%d" % (row)

            # Extend vdd and gnd of Wordline_driver
            yoffset = (row + 1) * self.inv.height - 0.5 * drc["minwidth_metal2"]
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
            inv_nand2B_connection_height = (abs(self.inv.Z_position.y 
                                                    - self.NAND2.B_position.y)
                                                + drc["minwidth_metal1"])

            if (row % 2):
                y_offset = self.inv.height*(row + 1)
                name_inv1_offset = [self.x_offset0, y_offset]
                nand2_offset=[self.x_offset1, y_offset]
                inv2_offset=[self.x_offset2, y_offset]
                inst_mirror = "MX"
                cell_dir = vector(0,-1)
                m1tm2_rotate=270
                m1tm2_mirror="R0"
            else:
                y_offset = self.inv.height*row
                name_inv1_offset = [self.x_offset0, y_offset]
                nand2_offset=[self.x_offset1, y_offset]
                inv2_offset=[self.x_offset2, y_offset]
                inst_mirror = "R0"
                cell_dir = vector(0,1)
                m1tm2_rotate=90
                m1tm2_mirror="MX"

            # add inv1 based on the info above
            self.add_inst(name=name_inv1,
                          mod=self.inv,
                          offset=name_inv1_offset,
                          mirror=inst_mirror )
            self.connect_inst(["clk", "clk_bar[{0}]".format(row),
                               "vdd", "gnd"])
            # add nand 2
            self.add_inst(name=name_nand,
                          mod=self.NAND2,
                          offset=nand2_offset,
                          mirror=inst_mirror)
            self.connect_inst(["decode_out[{0}]".format(row),
                               "clk_bar[{0}]".format(row),
                               "net[{0}]".format(row),
                               "vdd", "gnd"])
            # add inv2
            self.add_inst(name=name_inv2,
                          mod=self.driver,
                          offset=inv2_offset,
                          mirror=inst_mirror)
            self.connect_inst(["net[{0}]".format(row),
                               "wl[{0}]".format(row),
                               "vdd", "gnd"])

            # clk connection
            clk_offset= [drc["minwidth_metal1"] + 2 * drc["metal1_to_metal1"],
                         y_offset + cell_dir.y * self.inv.A_position.y]
            self.add_rect(layer="metal1",
                          offset=clk_offset,
                          width=self.x_offset0 - 2*drc["metal1_to_metal1"],
                          height=cell_dir.y *drc["minwidth_metal1"])
            # first inv to nand2 B
            inv_to_nand2B_offset = [self.x_offset1 - drc["minwidth_metal1"],
                                  y_offset + cell_dir.y * self.NAND2.B_position.y]
            self.add_rect(layer="metal1",
                          offset=inv_to_nand2B_offset,
                          width=drc["minwidth_metal1"],
                          height=cell_dir.y*inv_nand2B_connection_height)
            # Nand2 out to 2nd inv
            nand2_to_2ndinv_offset =[self.x_offset2,
                                  y_offset + cell_dir.y * self.NAND2.Z_position.y]
            self.add_rect(layer="metal1",
                          offset=nand2_to_2ndinv_offset,
                          width=drc["minwidth_metal1"],
                          height=cell_dir.y * drc["minwidth_metal1"])
            # nand2 A connection
            self.add_rect(layer="metal2",
                          offset=[0, y_offset + cell_dir.y * self.NAND2.A_position.y],
                          width=self.x_offset1,
                          height=cell_dir.y*drc["minwidth_metal2"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=[self.x_offset1,
                                  y_offset + cell_dir.y * self.NAND2.A_position.y],
                          rotate=m1tm2_rotate,
                          mirror=m1tm2_mirror)
            self.add_via(layers=("metal1", "via1", "metal2"),
                          offset=[0, 
                                  y_offset +cell_dir.y*self.NAND2.A_position.y],
                          mirror=inst_mirror)


            base_offset = vector(self.width, y_offset)

            decode_out_offset = base_offset.scale(0,1)+self.NAND2.A_position.scale(cell_dir)
            wl_offset = base_offset + self.driver.Z_position.scale(cell_dir)
            vdd_offset = base_offset + self.driver.vdd_position.scale(cell_dir)
            gnd_offset = base_offset + self.driver.gnd_position.scale(cell_dir)
            self.add_label(text="decode_out[{0}]".format(row),
                           layer="metal2",
                           offset=decode_out_offset)
            self.add_rect(layer="metal1",
                          offset=wl_offset,
                          width=drc["minwidth_metal1"]*cell_dir.y,
                          height=drc["minwidth_metal1"]*cell_dir.y)
            self.add_label(text="wl[{0}]".format(row),
                           layer="metal1",
                           offset=wl_offset)
            self.add_label(text="gnd",
                           layer="metal1",
                           offset=gnd_offset)
            self.add_label(text="vdd",
                           layer="metal1",
                           offset=vdd_offset)

            self.decode_out_positions.append(decode_out_offset)
            self.WL_positions.append(wl_offset)
            self.vdd_positions.append(vdd_offset)
            self.gnd_positions.append(gnd_offset)

<<<<<<< HEAD
    def add_extra_driver(self, driver_mults, start, array_gap, array_to_driver):
        self.wl_driver_mults = driver_mults
        for seg in range(1,driver_mults):
            seg_driver_width = self.driver.width
            extra_driver_offset= start + array_gap.scale(seg,0)
            self.add_extra_row_driver(extra_driver_offset, array_to_driver, seg)

    def add_extra_row_driver(self, offset, array_to_driver, seg):
        for row in range(self.rows):
            if (row % 2):
                y_offset = self.inv.height*(row + 1)
                first_driver_offset=[self.x_offset2, y_offset]
                inst_mirror = "MX"
                cell_dir = vector(1,-1)
            else:
                y_offset = self.inv.height*row
                first_driver_offset=[self.x_offset2, y_offset]
                inst_mirror = "R0"
                cell_dir = vector(1,1)
            extra_driver_offset = offset + vector(0,y_offset)
            self.rout_net_0(first_driver_offset, extra_driver_offset, cell_dir)
            self.add_extra_a_driver(extra_driver_offset, inst_mirror, row, seg)
            self.route_to_prev_WL(extra_driver_offset, array_to_driver, cell_dir)
            self.route_to_next_WL(extra_driver_offset, array_to_driver, cell_dir)
            self.extend_extra_vdd(first_driver_offset,extra_driver_offset,cell_dir)
            self.extend_extra_gnd(first_driver_offset,extra_driver_offset,cell_dir)

    def rout_net_0(self,first_driver_offset, extra_driver_offset, cell_dir):
        m1m2_via = contact(layer_stack=("metal2", "via2", "metal3"))
        start = first_driver_offset + self.driver.A_position.scale(cell_dir)
        end = extra_driver_offset + self.driver.A_position.scale(cell_dir)
        
        self.add_path(layer=("metal3"),
                      coordinates=[start,end+ vector(m1m2_via.width,0)],
                      offset=start)
        for offset in [start, end]:
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset)
            self.add_via(layers=("metal2", "via2", "metal3"),
                         offset=offset)
        

    def add_extra_a_driver(self, offset, mirror, row ,seg):
        #sec_offset =[95.045, 0]
        self.add_inst(name="add_on_row_{0}_seg_{1}".format(row, seg),
                      mod=self.driver,
                      offset=offset,
                      mirror=mirror)
        self.connect_inst(["net[{0}]".format(row),
                           "wl[{0}]".format(row),
                           "vdd", "gnd"])

    def route_to_next_WL(self, driver_offset, end, cell_dir):
        start = driver_offset + self.driver.Z_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)
        mid = start + vector(drc["metal1_to_metal1"],0)
        end = vector(start.x + end, driver_offset.y + self.bitcell_chars["WL"][1]*cell_dir.y)
        self.add_path(layer=("metal1"),
                      coordinates=[start,mid,end],
                      offset=start)

    def route_to_prev_WL(self,driver_offset, array_to_driver, cell_dir):
        #start = driver_offset + self.driver.Z_position.scale(-1,1) + vector(-0.5*drc["minwidth_metal1"], drc["minwidth_metal1"])
        #end = vector(offset)
        start =driver_offset + self.driver.Z_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)   
        end = driver_offset - vector(array_to_driver,0) \
              + vector(0, self.bitcell_chars["WL"][1]*cell_dir.y)
        mid0 = start + vector(drc["metal1_to_metal1"],0)
        mid1 = vector(start.x,end.y) + vector(drc["minwidth_metal1"],0.5*drc["minwidth_metal1"]).scale(cell_dir)   
        mid2 = vector(mid1.x, end.y) + vector(drc["minwidth_metal2"],0).scale(cell_dir)   
        mid3 = driver_offset.scale(1,0) - vector(drc["metal1_to_metal1"]+drc["minwidth_metal2"],0)\
                + end.scale(0,1)

        self.add_path(layer=("metal1"),
                      coordinates=[start,mid0,mid1],
                      offset=start)

        m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))
        via_offset = mid1 - vector( 0.5 *m1m2_via.width, m1m2_via.height*0.5) + vector(0, m1m2_via.height*0.5).scale(cell_dir)\
                     - vector(0, 0.5*drc["minwidth_metal2"]).scale(cell_dir)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=via_offset)
        self.add_path(layer=("metal2"),
                      coordinates=[mid1,mid3],
                      offset=mid1)

        via_offset = mid3 - vector(m1m2_via.width * 0.5, m1m2_via.height*0.5) + vector(0, m1m2_via.height*0.5).scale(cell_dir)\
                     - vector(0, 0.5*drc["minwidth_metal2"]).scale(cell_dir)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=via_offset )   
        self.add_path(layer=("metal1"),
                      coordinates=[mid3,end],
                      offset=mid3) 

    def extend_extra_vdd(self,first_driver_offset,extra_driver_offset, cell_dir):
        start =first_driver_offset + self.driver.vdd_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)   
        end = extra_driver_offset + self.driver.vdd_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)       
        self.add_path(layer=("metal1"),
                      coordinates=[start,end],
                      offset=start)

    def extend_extra_gnd(self,first_driver_offset,extra_driver_offset, cell_dir):
        start =first_driver_offset + self.driver.gnd_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)       
        end = extra_driver_offset + self.driver.gnd_position.scale(cell_dir) + vector(0,0.5*drc["minwidth_metal1"]).scale(cell_dir)      
        self.add_path(layer=("metal1"),
                      coordinates=[start,end],
                      offset=start)

    def delay(self, slope, load=0):
        # decode_out -> net
        if self.wl_driver_mults == 1:
            decode_t_net = self.NAND2.delay(slope = slope, load = self.driver.input_load())
        else:
            net_wire = self.generate_rc_net(self.wl_driver_mults, self.net_wire_length, drc["minwidth_metal1"])
            net_wire.wire_c = self.driver.input_load() + net_wire.wire_c
            decode_t_net = self.NAND2.delay(slope = slope, load = net_wire.return_input_cap())
            wire_delay = net_wire.return_delay_over_wire(decode_t_net.slope)
            decode_t_net = decode_t_net + wire_delay
        # net -> wl
        net_t_wl = self.driver.delay(slope = decode_t_net.slope, load = load)

        result = decode_t_net + net_t_wl
        return result
    
    def input_load(self):
        return self.NAND2.input_load()
