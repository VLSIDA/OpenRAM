import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS

class dff_array(design.design):
    """
    This is a simple row (or multiple rows) of flops.
    Unlike the data flops, these are never spaced out.
    """

    def __init__(self, rows, columns, name=""):
        self.rows = rows
        self.columns = columns

        if name=="":
            name = "dff_array_{0}x{1}".format(rows, columns)
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        c = reload(__import__(OPTS.dff))
        self.mod_dff = getattr(c, OPTS.dff)
        self.ms = self.mod_dff("dff")
        self.add_mod(self.ms)

        self.width = self.columns * self.ms.width
        self.height = self.rows * self.ms.height

        self.create_layout()

    def create_layout(self):
        self.add_pins()
        self.create_dff_array()
        self.add_layout_pins()
        self.DRC_LVS()

    def add_pins(self):
        for row in range(self.rows):  
            for col in range(self.columns):
                self.add_pin("din[{0}][{1}]".format(row,col))
        for row in range(self.rows):  
            for col in range(self.columns):
                self.add_pin("dout[{0}][{1}]".format(row,col))
                #self.add_pin("dout_bar[{0}]".format(i))
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_dff_array(self):
        self.dff_insts={}
        for y in range(self.rows):  
            for x in range(self.columns):
                name = "Xdff_r{0}_c{1}".format(y,x)
                if (y % 2 == 0):
                    base = vector(x*self.ms.width,y*self.ms.height)
                    mirror = "R0"
                else:
                    base = vector(x*self.ms.width,(y+1)*self.ms.height)
                    mirror = "MX"
                self.dff_insts[x,y]=self.add_inst(name=name,
                                                  mod=self.ms,
                                                  offset=base, 
                                                  mirror=mirror)
                self.connect_inst(["din[{0}][{1}]".format(x,y),
                                   "dout[{0}][{1}]".format(x,y),
                                   "clk",
                                   "vdd",
                                   "gnd"])

    def add_layout_pins(self):
        
        for y in range(self.rows):
            # Continous vdd rail along with label.
            vdd_pin=self.dff_insts[0,y].get_pin("vdd")
            self.add_layout_pin(text="vdd",
                                layer="metal1",
                                offset=vdd_pin.ll(),
                                width=self.width,
                                height=drc["minwidth_metal1"])

            # Continous gnd rail along with label.
            gnd_pin=self.dff_insts[0,y].get_pin("gnd")
            self.add_layout_pin(text="gnd",
                                layer="metal1",
                                offset=gnd_pin.ll(),
                                width=self.width,
                                height=drc["minwidth_metal1"])
            

        for y in range(self.rows):            
            for x in range(self.columns):            
                din_pin = self.dff_insts[x,y].get_pin("d")
                self.add_layout_pin(text="din[{0}][{1}]".format(x,y),
                                    layer=din_pin.layer,
                                    offset=din_pin.ll(),
                                    width=din_pin.width(),
                                    height=din_pin.height())

                dout_pin = self.dff_insts[x,y].get_pin("q")
                self.add_layout_pin(text="dout[{0}][{1}]".format(x,y),
                                    layer="metal1",
                                    offset=dout_pin.ll(),
                                    width=dout_pin.width(),
                                    height=dout_pin.height())

            
        # # Continous clk rail along with label.
        # self.add_layout_pin(text="clk",
        #                     layer="metal1",
        #                     offset=self.dff_insts[0].get_pin("clk").ll().scale(0,1),
        #                     width=self.width,
        #                     height=drc["minwidth_metal1"])

        

    def analytical_delay(self, slew, load=0.0):
        return self.ms.analytical_delay(slew=slew, load=load)
