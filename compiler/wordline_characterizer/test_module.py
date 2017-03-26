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
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """

    def __init__(self, name, word_size, measured_WL_pos, extra=1 ,strength=None):
        design.design.__init__(self, name)

        self.word_size = word_size
        self.add_pin("sel")
        self.add_pin("clk")
        self.add_pin("wl")
        self.add_pin("vdd")
        self.add_pin("gnd")

        if strength == None:
            self.nand_size, self.inv_size = self.logic_effort_sizing(word_size)
        else:
            self.nand_size = 2
            self.inv_size = strength
        seg_size = self.word_size/extra
        self.inv_size = self.inv_size/extra
        driver = p_wordline_driver.wordline_driver(name="Wordline_driver", 
                                                 rows=1)
        array = bitcell_array.bitcell_array(name="bitcell_array", cols=seg_size, rows=1)
        array_offset = vector(driver.width+6*drc["minwidth_metal1"],0)

        driver_to_array = 6*drc["minwidth_metal1"]

        # adding metal to just test the wire RC
        start = array_offset+array.WL_positions[0]
        end = start + vector(array.width,0)
        #print "array.width",array.width
        self.add_path(("metal1"),
                      [start, end])

        #"""
        if extra >1:
            for seg in range(1,extra):
                seg_driver_width = driver.driver.width
                #print seg," array and dirver"
                arary_i_offset = array_offset+vector((array.width+2*driver_to_array+seg_driver_width)*(seg-1),0)
                #print "arary_i_offset",arary_i_offset
                self.add_inst(name="array{0}".format(seg),
                              mod=array,
                              offset=arary_i_offset)
                temp = []
                for i in range(seg_size):
                    temp.append("bl{0}".format(i+(seg-1)*seg_size))
                    temp.append("br{0}".format(i+(seg-1)*seg_size))
                temp = temp + ["wl", "vdd", "gnd"]
                self.connect_inst(temp)

                extra_driver_offset= arary_i_offset + vector(driver_to_array+array.width,0)
                driver.add_extra_driver(extra_driver_offset)
                #print "extra_driver_offset",extra_driver_offset
                WL_offset = arary_i_offset + array.WL_positions[-1]
                driver.route_extra_WL(WL_offset)

                arary_i_offset = array_offset+vector((array.width+2*driver_to_array+seg_driver_width)*seg,0)
                WL_offset = arary_i_offset + array.WL_positions[0]
                vdd_offset = arary_i_offset + array.vdd_positions[-1]
                gnd_offset = arary_i_offset + array.gnd_positions[-1]

                if seg != extra-1:
                    driver.extend_extra_WL(WL_offset)
                    driver.extend_extra_vdd(vdd_offset)            
                    driver.extend_extra_gnd(gnd_offset)    
        else:
            self.add_inst(name="array",
                          mod=array,
                          offset=array_offset)
            temp = []
            for i in range(seg_size):
                temp.append("bl{0}".format(i))
                temp.append("br{0}".format(i))
            temp = temp + ["wl", "vdd", "gnd"]
            self.connect_inst(temp)
        #"""



        self.add_mod(array)
        self.add_mod(driver)

        self.add_inst(name="wordline_driver",
                      mod=driver,
                      offset=[0,0])
        temp = ['sel', 'wl', 'clk', 'vdd', 'gnd']
        self.connect_inst(temp)
        self.add_label(text="clk",
                       layer="metal1",
                       offset=driver.clk_positions[0])

        self.add_label(text="sel",
                       layer="metal2",
                       offset=driver.decode_out_positions[0])
        #self.add_label(text="wl",
        #               layer="metal1",
        #               offset=driver.WL_positions[0])
        offset = array_offset + vector(measured_WL_pos*array.width, array.WL_positions[0].y )
        self.add_label(text="wl",
                       layer="metal1",
                       offset=offset)

        self.add_label(text="vdd",
                       layer="metal1",
                       offset=driver.vdd_positions[0])
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=driver.gnd_positions[0])






        
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

    def logic_effort_sizing(self,load_size):
        nand_effort = (4.0/3.0)
        G = 1.0*nand_effort*1.0
        H = load_size *(2.0/3.0)
        F = G*H
        f = F**(1.0/3.0)
        y = load_size*1.0/f
        x = y *nand_effort/f
        #print G,H,F,f
        #print "nand size",x,"inv size",y
        nand_size = int(x)+1
        inv_size = int(y)+1
        return nand_size, inv_size



