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

        self.word_size = word_size
        self.words_per_row = words_per_row
        self.row_size = self.word_size * self.words_per_row

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_sense_amp_array()

    def create_layout(self):
        self.height = self.amp.height
        
        if self.bitcell.width > self.amp.width:
            self.width = self.bitcell.width * self.word_size * self.words_per_row
        else:
            self.width = self.amp.width * self.word_size * self.words_per_row

        self.place_sense_amp_array()
        self.add_layout_pins()
        self.route_rails()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(0,self.word_size):
            self.add_pin("data_{0}".format(i))
            self.add_pin("bl_{0}".format(i))
            self.add_pin("br_{0}".format(i))
        self.add_pin("en")
        self.add_pin("vdd")
        self.add_pin("gnd")
        
    def add_modules(self):
        from importlib import reload
        c = reload(__import__(OPTS.sense_amp))
        self.mod_sense_amp = getattr(c, OPTS.sense_amp)
        self.amp = self.mod_sense_amp("sense_amp")
        self.add_mod(self.amp)

        # This is just used for measurements,
        # so don't add the module
        c = reload(__import__(OPTS.bitcell))
        self.mod_bitcell = getattr(c, OPTS.bitcell)
        self.bitcell = self.mod_bitcell()
        
    def create_sense_amp_array(self):
        self.local_insts = []
        for i in range(0,self.word_size):

            name = "sa_d{0}".format(i)
            self.local_insts.append(self.add_inst(name=name,
                                                  mod=self.amp))
            self.connect_inst(["bl_{0}".format(i),
                               "br_{0}".format(i), 
                               "data_{0}".format(i), 
                               "en", "vdd", "gnd"])

    def place_sense_amp_array(self):
            
        if self.bitcell.width > self.amp.width:
            amp_spacing = self.bitcell.width * self.words_per_row
        else:
            amp_spacing = self.amp.width * self.words_per_row
        for i in range(0,self.word_size):
            amp_position = vector(amp_spacing * i, 0)
            self.local_insts[i].place(amp_position)

        
    def add_layout_pins(self):
        for i in range(len(self.local_insts)):
            inst = self.local_insts[i]
            
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

            bl_pin = inst.get_pin("bl")            
            br_pin = inst.get_pin("br")
            dout_pin = inst.get_pin("dout")
            
            self.add_layout_pin(text="bl_{0}".format(i),
                                layer="metal2",
                                offset=bl_pin.ll(),
                                width=bl_pin.width(),
                                height=bl_pin.height())
            self.add_layout_pin(text="br_{0}".format(i),
                                layer="metal2",
                                offset=br_pin.ll(),
                                width=br_pin.width(),
                                height=br_pin.height())
                           
            self.add_layout_pin(text="data_{0}".format(i),
                                layer="metal2",
                                offset=dout_pin.ll(),
                                width=dout_pin.width(),
                                height=dout_pin.height())
                           
            
    def route_rails(self):
        # add sclk rail across entire array
        sclk_offset = self.amp.get_pin("en").ll().scale(0,1)
        self.add_layout_pin(text="en",
                      layer="metal1",
                      offset=sclk_offset,
                      width=self.width,
                      height=drc("minwidth_metal1"))

    def analytical_delay(self, slew, load=0.0):
        return self.amp.analytical_delay(slew=slew, load=load)
        
