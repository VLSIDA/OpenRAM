import design
from tech import drc
from vector import vector
import debug
from globals import OPTS

class sense_amp_array(design.design):
    """
    Array of sense amplifiers to read the bitlines through the column mux.
    Dynamically generated sense amp array for all bitlines.
    """

    def __init__(self, word_size, words_per_row):
        design.design.__init__(self, "sense_amp_array")
        debug.info(1, "Creating {0}".format(self.name))

        c = reload(__import__(OPTS.sense_amp))
        self.mod_sense_amp = getattr(c, OPTS.sense_amp)
        self.amp = self.mod_sense_amp("sense_amp")
        self.add_mod(self.amp)

        self.word_size = word_size
        self.words_per_row = words_per_row
        self.row_size = self.word_size * self.words_per_row

        self.height = self.amp.height
        self.width = self.amp.width * self.word_size * self.words_per_row

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):

        for i in range(0,self.row_size,self.words_per_row):
            self.add_pin("data[{0}]".format(i/self.words_per_row))
            self.add_pin("bl[{0}]".format(i))
            self.add_pin("br[{0}]".format(i))

        self.add_pin("en")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):

        self.add_sense_amp()
        self.connect_rails()
        

    def add_sense_amp(self):
            
        bl_pin = self.amp.get_pin("bl")            
        br_pin = self.amp.get_pin("br")
        dout_pin = self.amp.get_pin("dout")
        
        for i in range(0,self.row_size,self.words_per_row):

            name = "sa_d{0}".format(i)
            amp_position = vector(self.amp.width * i, 0)
            
            bl_offset = amp_position + bl_pin.ll().scale(1,0)
            br_offset = amp_position + br_pin.ll().scale(1,0)
            dout_offset = amp_position + dout_pin.ll()
            
            inst = self.add_inst(name=name,
                          mod=self.amp,
                          offset=amp_position)
            self.connect_inst(["bl[{0}]".format(i),"br[{0}]".format(i), 
                               "data[{0}]".format(i/self.words_per_row), 
                               "en", "vdd", "gnd"])

            
            gnd_pos = inst.get_pin("gnd").center()
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=gnd_pos)
            self.add_layout_pin_rect_center(text="gnd",
                                            layer="metal3",
                                            offset=gnd_pos)

            vdd_pos = inst.get_pin("vdd").center()
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=vdd_pos)
            self.add_layout_pin_rect_center(text="vdd",
                                            layer="metal3",
                                            offset=vdd_pos)
            

            self.add_layout_pin(text="bl[{0}]".format(i),
                                layer="metal2",
                                offset=bl_offset,
                                width=bl_pin.width(),
                                height=bl_pin.height())
            self.add_layout_pin(text="br[{0}]".format(i),
                                layer="metal2",
                                offset=br_offset,
                                width=br_pin.width(),
                                height=br_pin.height())
                           
            self.add_layout_pin(text="data[{0}]".format(i/self.words_per_row),
                                layer="metal3",
                                offset=dout_offset,
                                width=dout_pin.width(),
                                height=dout_pin.height())
                           

    def connect_rails(self):
        # add sclk rail across entire array
        sclk_offset = self.amp.get_pin("en").ll().scale(0,1)
        self.add_layout_pin(text="en",
                      layer="metal1",
                      offset=sclk_offset,
                      width=self.width,
                      height=drc["minwidth_metal1"])

    def analytical_delay(self, slew, load=0.0):
        return self.amp.analytical_delay(slew=slew, load=load)
        
