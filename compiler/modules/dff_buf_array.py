import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS
import dff_buf

class dff_buf_array(design.design):
    """
    This is a simple row (or multiple rows) of flops.
    Unlike the data flops, these are never spaced out.
    """

    def __init__(self, rows, columns, inv1_size=2, inv2_size=4, name=""):
        self.rows = rows
        self.columns = columns

        if name=="":
            name = "dff_array_{0}x{1}".format(rows, columns)
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        self.dff = dff_buf.dff_buf(inv1_size, inv2_size)
        self.add_mod(self.dff)

        self.width = self.columns * self.dff.width
        self.height = self.rows * self.dff.height

        self.create_layout()

    def create_layout(self):
        self.add_pins()
        self.create_dff_array()
        self.add_layout_pins()
        self.DRC_LVS()

    def add_pins(self):
        for y in range(self.rows):  
            for x in range(self.columns):
                self.add_pin(self.get_din_name(y,x))
        for y in range(self.rows):  
            for x in range(self.columns):
                self.add_pin(self.get_dout_name(y,x))
                self.add_pin(self.get_dout_bar_name(y,x))
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_dff_array(self):
        self.dff_insts={}
        for y in range(self.rows):  
            for x in range(self.columns):
                name = "Xdff_r{0}_c{1}".format(y,x)
                if (y % 2 == 0):
                    base = vector(x*self.dff.width,y*self.dff.height)
                    mirror = "R0"
                else:
                    base = vector(x*self.dff.width,(y+1)*self.dff.height)
                    mirror = "MX"
                self.dff_insts[x,y]=self.add_inst(name=name,
                                                  mod=self.dff,
                                                  offset=base, 
                                                  mirror=mirror)
                self.connect_inst([self.get_din_name(y,x),
                                   self.get_dout_name(y,x),
                                   self.get_dout_bar_name(y,x),  
                                   "clk",
                                   "vdd",
                                   "gnd"])

    def get_din_name(self, row, col):
        if self.columns == 1:
            din_name = "din[{0}]".format(row)
        elif self.rows == 1:
            din_name = "din[{0}]".format(col)
        else:
            din_name = "din[{0}][{1}]".format(row,col)

        return din_name
    
    def get_dout_name(self, row, col):
        if self.columns == 1:
            dout_name = "dout[{0}]".format(row)
        elif self.rows == 1:
            dout_name = "dout[{0}]".format(col)
        else:
            dout_name = "dout[{0}][{1}]".format(row,col)

        return dout_name
    
    def get_dout_bar_name(self, row, col):
        if self.columns == 1:
            dout_bar_name = "dout_bar[{0}]".format(row)
        elif self.rows == 1:
            dout_bar_name = "dout_bar[{0}]".format(col)
        else:
            dout_bar_name = "dout_bar[{0}][{1}]".format(row,col)

        return dout_bar_name
    
    def add_layout_pins(self):
        
        for y in range(self.rows):
            # Continous vdd rail along with label.
            vdd_pin=self.dff_insts[0,y].get_pin("vdd")
            self.add_layout_pin(text="vdd",
                                layer="metal1",
                                offset=vdd_pin.ll(),
                                width=self.width,
                                height=self.m1_width)

            # Continous gnd rail along with label.
            gnd_pin=self.dff_insts[0,y].get_pin("gnd")
            self.add_layout_pin(text="gnd",
                                layer="metal1",
                                offset=gnd_pin.ll(),
                                width=self.width,
                                height=self.m1_width)
            

        for y in range(self.rows):            
            for x in range(self.columns):            
                din_pin = self.dff_insts[x,y].get_pin("D")
                debug.check(din_pin.layer=="metal2","DFF D pin not on metal2")
                self.add_layout_pin(text=self.get_din_name(y,x),
                                    layer=din_pin.layer,
                                    offset=din_pin.ll(),
                                    width=din_pin.width(),
                                    height=din_pin.height())

                dout_pin = self.dff_insts[x,y].get_pin("Q")
                debug.check(dout_pin.layer=="metal2","DFF Q pin not on metal2")
                self.add_layout_pin(text=self.get_dout_name(y,x),
                                    layer=dout_pin.layer,
                                    offset=dout_pin.ll(),
                                    width=dout_pin.width(),
                                    height=dout_pin.height())


                dout_bar_pin = self.dff_insts[x,y].get_pin("Qb")
                debug.check(dout_bar_pin.layer=="metal2","DFF Qb pin not on metal2")
                self.add_layout_pin(text=self.get_dout_bar_name(y,x),
                                    layer=dout_bar_pin.layer,
                                    offset=dout_bar_pin.ll(),
                                    width=dout_bar_pin.width(),
                                    height=dout_bar_pin.height())

                
        # Create vertical spines to a single horizontal rail
        clk_pin = self.dff_insts[0,0].get_pin("clk")
        debug.check(clk_pin.layer=="metal2","DFF clk pin not on metal2")
        if self.columns==1:
            self.add_layout_pin(text="clk",
                                layer="metal2",
                                offset=clk_pin.ll().scale(1,0),
                                width=self.m2_width,
                                height=self.height)
        else:
            self.add_layout_pin(text="clk",
                                layer="metal3",
                                offset=vector(0,0),
                                width=self.width,
                                height=self.m3_width)
            for x in range(self.columns):
                clk_pin = self.dff_insts[x,0].get_pin("clk")
                # Make a vertical strip for each column
                self.add_layout_pin(text="clk",
                                    layer="metal2",
                                    offset=clk_pin.ll().scale(1,0),
                                    width=self.m2_width,
                                    height=self.height)
                # Drop a via to the M3 pin
                self.add_via_center(layers=("metal2","via2","metal3"),
                                    offset=clk_pin.center().scale(1,0))
                
        

    def analytical_delay(self, slew, load=0.0):
        return self.dff.analytical_delay(slew=slew, load=load)
