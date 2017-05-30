# test module for wl driver


from tech import drc, parameter
import debug
import design
from math import log
from math import sqrt
import math
import p_wordline_driver
import bitcell_array
from pinv import pinv
from vector import vector
from globals import OPTS


class test_module(design.design):
    """
    Build the minmum set of module together to Measure Delay,
    def __init__(word_size, driver_size, mults, nand_size=None)
        set seg_array_size
    def measure_delay_to_driver() 
        1. a clk inv, a nand, drivers(at differet driver position)
        measure delay to wl     
    def measure_delay_to_wl()
    """

    def __init__(self, name, word_size, driver_size, mults ,auto_size=False):
        design.design.__init__(self, name)

        self.word_size = word_size
        self.add_pin("sel")
        self.add_pin("clk")
        self.add_pin("wl")
        self.add_pin("vdd")
        self.add_pin("gnd")

        if auto_size == True: # auto sizing nand and driver for loads
            self.nand_size, self.inv_size = self.logic_effort_sizing(word_size)
        else: # other wise we fix nand size to 2
            self.nand_size = 2
            self.inv_size = driver_size
        # mults 1 and 2 have the same seg size
        # only break array when more than 2 drivers
        self.seg_size = self.word_size/max((mults-1),1) 
        self.inv_size = self.inv_size/mults
        self.driver = p_wordline_driver.wordline_driver(name="Wordline_driver",
                                                        driver_strength = self.inv_size*drc["minwidth_tx"],
                                                        rows=1)
        self.add_mod(self.driver)

        self.array = bitcell_array.bitcell_array(name="bitcell_array", cols=max(self.seg_size,1), rows=1)
        self.add_mod(self.array)

        self.mults = mults
        self.wl_bit_index =0

    def set_wl_label(self, bit_index):
        self.wl_bit_index = bit_index

    def create_layout(self, cell_load=True):
        self.add_driver()
        self.connect_drivers_to_array(self.driver, self.array)
        self.extend_drivers(self.mults, self.driver, self.array)

        if cell_load == True:
            if self.word_size >0:
                self.add_array(self.mults)
            else: # no array to add even           
                self.replace_array_with_metal(self.mults, self.array)
        else:
            self.replace_array_with_metal(self.mults, self.array)

        self.add_label(text="clk",
                       layer="metal1",
                       offset=self.driver.clk_positions[0])

        self.add_label(text="sel",
                       layer="metal2",
                       offset=self.driver.decode_out_positions[0])

        self.update_wl_label(self.wl_bit_index)

        self.add_label(text="wl",
                       layer="metal1",
                       offset=self.label_position)

        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.driver.vdd_positions[0])
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=self.driver.gnd_positions[0])

    def update_wl_label(self,bit_index):
        array_offset =  vector(self.driver.width+6*drc["minwidth_metal1"],0)
        array_gap = vector(2*6*drc["minwidth_metal1"] + self.array.width+ self.driver.driver.width, 0)

        if bit_index == 0:
            self.label_position = self.driver.WL_positions[0] # default label at driver 0 output
        else:
            # set on the nth bit cell
            if self.mults ==1:
                index = int(bit_index)-1
                x = (self.array.BL_positions[index].x+self.array.BR_positions[index].x)*0.5
                self.label_position = (array_offset
                                        + vector(x,
                                                 self.array.WL_positions[0].y))
            else:
                seg_index = bit_index/self.seg_size
                bit_index = bit_index%self.seg_size
                self.label_position = (array_offset + seg_index * array_gap  
                                        + vector(self.array.cell.width*(bit_index+0.5),
                                                 self.array.WL_positions[0].y))    

    
    def add_driver(self):
        self.add_inst(name="wordline_driver",
                      mod=self.driver,
                      offset=[0,0])
        temp = ['sel', 'wl', 'clk', 'vdd', 'gnd']
        self.connect_inst(temp)


    def connect_drivers_to_array(self, driver, array):
        start = [driver.WL_positions[0].x+drc["minwidth_metal1"],driver.WL_positions[0].y+drc["minwidth_metal1"]]
        end =[driver.width+6*drc["minwidth_metal1"],array.WL_positions[0].y]
        self.add_path(layer=("metal1"),
                      coordinates=[start,end],
                      offset=start)

        start = driver.vdd_positions[0]
        start =[start[0],start[1]+0.5*drc["minwidth_metal1"]]
        end =[end[0],start[1]]
        self.add_path(layer=("metal1"),
                      coordinates=[start,end],
                      offset=start)

        start = driver.gnd_positions[0]
        start =[start[0],start[1]+0.5*drc["minwidth_metal1"]]
        end =[end[0],start[1]]
        self.add_path(layer=("metal1"),
                      coordinates=[start,end],
                      offset=start)

    def extend_drivers(self, mults, driver, array):
        array_offset = vector(self.driver.width - self.driver.driver.width,0)
        array_gap = vector(2*6*drc["minwidth_metal1"] + self.array.width+ self.driver.driver.width, 0)
        for seg in range(1,mults):
            seg_driver_width = driver.driver.width
            extra_driver_offset= array_offset+array_gap.scale(seg,0)
            driver.add_extra_driver(extra_driver_offset)
            
            WL_offset = extra_driver_offset - vector(6*drc["minwidth_metal1"],0) + array.WL_positions[-1].scale(0,1)
            driver.route_extra_WL(WL_offset)

            WL_offset = extra_driver_offset + vector(self.driver.driver.width + 6*drc["minwidth_metal1"],0)+array.WL_positions[-1].scale(0,1)
            vdd_offset = extra_driver_offset + vector(self.driver.driver.width + 6*drc["minwidth_metal1"],0)+array.vdd_positions[-1].scale(0,1)
            gnd_offset = extra_driver_offset + vector(self.driver.driver.width + 6*drc["minwidth_metal1"],0) + array.gnd_positions[-1].scale(0,1)
            if seg != mults-1:
                driver.extend_extra_WL(WL_offset)
                driver.extend_extra_vdd(vdd_offset)            
                driver.extend_extra_gnd(gnd_offset) 

    def add_array(self,mults):
        array_offset = vector(self.driver.width+6*drc["minwidth_metal1"],0)
        start_index = 0
        array_gap = vector(2*6*drc["minwidth_metal1"] + self.array.width+ self.driver.driver.width, 0)
        for seg in range(max(1,mults-1)):
            self.add_inst(name="array"+str(seg),
                          mod=self.array,
                          offset=array_offset)
            temp = []
            for i in range(self.array.column_size):
                temp.append("bl{0}".format(i+start_index))
                temp.append("br{0}".format(i+start_index))
            temp = temp + ["wl", "vdd", "gnd"]
            self.connect_inst(temp)
            array_offset = array_offset + array_gap
            start_index = start_index+self.array.column_size
        
    def replace_array_with_metal(self, mults, array):
        array_offset = vector(self.driver.width+6*drc["minwidth_metal1"],0)
        array_gap = vector(2*6*drc["minwidth_metal1"] + self.array.width+ self.driver.driver.width, 0)
        for seg in range(mults-1):
            WL_postions = array_offset+array.WL_positions[0].scale(0,1)
            vdd_postions = array_offset+array.vdd_positions[0].scale(0,1)
            gnd_postions = array_offset+array.gnd_positions[0].scale(0,1)
            for pos in [WL_postions,vdd_postions,gnd_postions]:
                end = pos + vector(self.array.width,0)
                self.add_path(layer="metal1",
                              coordinates=[pos,end],
                              offset=pos)
            array_offset = array_offset + array_gap 



