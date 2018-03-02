import debug
from tech import drc
import design
from vector import vector
from globals import OPTS

class tri_gate_array(design.design):
    """
    Dynamically generated tri gate array of all bitlines.  words_per_row
    """

    def __init__(self, columns, word_size):
        """Intial function of tri gate array """
        design.design.__init__(self, "tri_gate_array")
        debug.info(1, "Creating {0}".format(self.name))

        c = reload(__import__(OPTS.tri_gate))
        self.mod_tri_gate = getattr(c, OPTS.tri_gate)
        self.tri = self.mod_tri_gate("tri_gate")
        self.add_mod(self.tri)

        self.columns = columns
        self.word_size = word_size

        self.words_per_row = self.columns / self.word_size
        self.width = (self.columns / self.words_per_row) * self.tri.width
        self.height = self.tri.height
        
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        """generate layout """
        self.add_pins()
        self.create_array()
        self.add_layout_pins()

    def add_pins(self):
        """create the name of pins depend on the word size"""
        for i in range(self.word_size):
            self.add_pin("in[{0}]".format(i))
        for i in range(self.word_size):
            self.add_pin("out[{0}]".format(i))
        for pin in ["en", "en_bar", "vdd", "gnd"]:
            self.add_pin(pin)

    def create_array(self):
        """add tri gate to the array """
        self.tri_inst = {}
        for i in range(0,self.columns,self.words_per_row):
            name = "Xtri_gate{0}".format(i)
            base = vector(i*self.tri.width, 0)
            self.tri_inst[i]=self.add_inst(name=name,
                                           mod=self.tri,
                                           offset=base)
            self.connect_inst(["in[{0}]".format(i/self.words_per_row),
                               "out[{0}]".format(i/self.words_per_row),
                               "en", "en_bar", "vdd", "gnd"])


    def add_layout_pins(self):
        
        for i in range(0,self.columns,self.words_per_row):

            in_pin = self.tri_inst[i].get_pin("in")
            self.add_layout_pin(text="in[{0}]".format(i/self.words_per_row),
                                layer="metal2",
                                offset=in_pin.ll(),
                                width=in_pin.width(),
                                height=in_pin.height())

            out_pin = self.tri_inst[i].get_pin("out")
            self.add_layout_pin(text="out[{0}]".format(i/self.words_per_row),
                                layer="metal2",
                                offset=out_pin.ll(),
                                width=out_pin.width(),
                                height=out_pin.height())



        width = self.tri.width * self.columns - (self.words_per_row - 1) * self.tri.width
        en_pin = self.tri_inst[0].get_pin("en")
        self.add_layout_pin(text="en",
                            layer="metal1",
                            offset=en_pin.ll().scale(0, 1),
                            width=width,
                            height=drc["minwidth_metal1"])
        
        enbar_pin = self.tri_inst[0].get_pin("en_bar")
        self.add_layout_pin(text="en_bar",
                            layer="metal1",
                            offset=enbar_pin.ll().scale(0, 1),
                            width=width,
                            height=drc["minwidth_metal1"])
        
        vdd_pin = self.tri_inst[0].get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="metal1",
                            offset=vdd_pin.ll().scale(0, 1),
                            width=width,
                            height=drc["minwidth_metal1"])
            
        for gnd_pin in self.tri_inst[0].get_pins("gnd"):
            if gnd_pin.layer=="metal1":
                self.add_layout_pin(text="gnd",
                                    layer="metal1",
                                    offset=gnd_pin.ll().scale(0, 1),
                                    width=width,
                                    height=drc["minwidth_metal1"])


    def analytical_delay(self, slew, load=0.0):
        return self.tri.analytical_delay(slew = slew, load = load)
        
