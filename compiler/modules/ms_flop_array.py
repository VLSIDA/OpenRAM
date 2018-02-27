import debug
import design
from tech import drc
from math import log
from vector import vector
from globals import OPTS

class ms_flop_array(design.design):
    """
    An Array of D-Flipflops used for to store Data_in & Data_out of
    Write_driver & Sense_amp, address inputs of column_mux &
    hierdecoder
    """

    def __init__(self, columns, word_size, name=""):
        self.columns = columns
        self.word_size = word_size
        if name=="":
            name = "flop_array_c{0}_w{1}".format(columns,word_size)
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(self.name))

        c = reload(__import__(OPTS.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.ms_flop)
        self.ms = self.mod_ms_flop("ms_flop")
        self.add_mod(self.ms)

        self.width = self.columns * self.ms.width
        self.height = self.ms.height
        self.words_per_row = self.columns / self.word_size

        self.create_layout()

    def create_layout(self):
        self.add_pins()
        self.create_ms_flop_array()
        self.add_layout_pins()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size):
            self.add_pin("din[{0}]".format(i))
        for i in range(self.word_size):
            self.add_pin("dout[{0}]".format(i))
            self.add_pin("dout_bar[{0}]".format(i))
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_ms_flop_array(self):
        self.ms_inst={}
        for i in range(0,self.columns,self.words_per_row):
            name = "Xdff{0}".format(i)
            if (i % 2 == 0 or self.words_per_row>1):
                base = vector(i*self.ms.width,0)
                mirror = "R0"
            else:
                base = vector((i+1)*self.ms.width,0)
                mirror = "MY"
            self.ms_inst[i/self.words_per_row]=self.add_inst(name=name,
                                                             mod=self.ms,
                                                             offset=base, 
                                                             mirror=mirror)
            self.connect_inst(["din[{0}]".format(i/self.words_per_row),
                               "dout[{0}]".format(i/self.words_per_row),
                               "dout_bar[{0}]".format(i/self.words_per_row),
                               "clk",
                               "vdd", "gnd"])

    def add_layout_pins(self):
        
        for i in range(self.word_size):

            for gnd_pin in self.ms_inst[i].get_pins("gnd"):
                if gnd_pin.layer!="metal2":
                    continue
                self.add_layout_pin(text="gnd",
                                    layer="metal2",
                                    offset=gnd_pin.ll(),
                                    width=gnd_pin.width(),
                                    height=gnd_pin.height())

            din_pins = self.ms_inst[i].get_pins("din")
            for din_pin in din_pins:
                self.add_layout_pin(text="din[{}]".format(i),
                                    layer=din_pin.layer,
                                    offset=din_pin.ll(),
                                    width=din_pin.width(),
                                    height=din_pin.height())

            dout_pin = self.ms_inst[i].get_pin("dout")
            self.add_layout_pin(text="dout[{}]".format(i),
                                layer="metal2",
                                offset=dout_pin.ll(),
                                width=dout_pin.width(),
                                height=dout_pin.height())

            doutbar_pin = self.ms_inst[i].get_pin("dout_bar")
            self.add_layout_pin(text="dout_bar[{}]".format(i),
                                layer="metal2",
                                offset=doutbar_pin.ll(),
                                width=doutbar_pin.width(),
                                height=doutbar_pin.height())
            
            
        # Continous clk rail along with label.
        self.add_layout_pin(text="clk",
                            layer="metal1",
                            offset=self.ms_inst[0].get_pin("clk").ll().scale(0,1),
                            width=self.width,
                            height=drc["minwidth_metal1"])

        
        # Continous vdd rail along with label.
        for vdd_pin in self.ms_inst[i].get_pins("vdd"):
            if vdd_pin.layer!="metal1":
                continue
            self.add_layout_pin(text="vdd",
                                layer="metal1",
                                offset=vdd_pin.ll().scale(0,1),
                                width=self.width,
                                height=drc["minwidth_metal1"])

        # Continous gnd rail along with label.
        for gnd_pin in self.ms_inst[i].get_pins("gnd"):
            if gnd_pin.layer!="metal1":
                continue
            self.add_layout_pin(text="gnd",
                                layer="metal1",
                                offset=gnd_pin.ll().scale(0,1),
                                width=self.width,
                                height=drc["minwidth_metal1"])
            

    def analytical_delay(self, slew, load=0.0):
        return self.ms.analytical_delay(slew=slew, load=load)
        
