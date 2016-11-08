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

        c = reload(__import__(OPTS.config.sense_amp))
        self.mod_sense_amp = getattr(c, OPTS.config.sense_amp)
        self.sense_amp_chars = self.mod_sense_amp.chars

        self.word_size = word_size
        self.words_per_row = words_per_row

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):

        if (self.words_per_row == 1):
            for i in range(self.word_size):
                self.add_pin("bl[{0}]".format(i))
                self.add_pin("br[{0}]".format(i))
        else:
            for i in range(self.word_size):
                index = i * self.words_per_row
                self.add_pin("bl_out[{0}]".format(index))
                self.add_pin("br_out[{0}]".format(index))

        for i in range(self.word_size):
            self.add_pin("data_out[{0}]".format(i))

        self.add_pin("sclk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        self.create_sense_amp()
        self.setup_layout_constants()
        self.add_sense_amp()
        self.connect_rails()
        self.offset_all_coordinates()

    def setup_layout_constants(self):
        self.vdd_positions = []
        self.gnd_positions = []
        self.SCLK_positions = []
        self.amp_positions = []
        self.Data_out_positions = []
        self.height = self.amp.height
        self.width = self.amp.width * self.word_size * self.words_per_row

    def create_sense_amp(self):
        self.amp = self.mod_sense_amp("sense_amp")
        self.add_mod(self.amp)

    def add_sense_amp(self):
        for i in range(self.word_size):
            name = "sa_d{0}".format(i)
            index = i * self.words_per_row
            amp_position = vector(self.amp.width * index, 0)
            BL_offset = amp_position + vector(self.sense_amp_chars["BL"][0], 0) 
            BR_offset = amp_position + vector(self.sense_amp_chars["BR"][0], 0)

            self.add_inst(name=name,
                          mod=self.amp,
                          offset=amp_position)
            self.amp_positions.append(amp_position)
            if (self.words_per_row == 1):
                self.add_label(text="bl[{0}]".format(i),
                               layer="metal2",
                               offset=BL_offset)
                self.add_label(text="br[{0}]".format(i),
                               layer="metal2",
                               offset=BR_offset)
                self.connect_inst(["bl[{0}]".format(i),"br[{0}]".format(i), 
                                   "data_out[{0}]".format(i), 
                                   "sclk", "vdd", "gnd"])
            else:
                self.add_label(text="bl_out[{0}]".format(index),
                               layer="metal2",
                               offset=BL_offset)
                self.add_label(text="br_out[{0}]".format(index),
                               layer="metal2",
                               offset=BR_offset)
                self.connect_inst(["bl_out[{0}]".format(index), "br_out[{0}]".format(index), 
                                   "data_out[{0}]".format(i), 
                                   "sclk", "vdd", "gnd"])

            self.add_label(text="data_out[{0}]".format(i),
                           layer="metal2",
                           offset=amp_position + self.sense_amp_chars["Dout"])
            self.Data_out_positions.append(amp_position + self.sense_amp_chars["Dout"])

    def connect_rails(self):
        base_offset = vector(0, - 0.5 * drc["minwidth_metal1"])
        # add vdd rail across entire array
        vdd_offset = base_offset + vector(self.sense_amp_chars["vdd"]).scale(0,1)
        self.add_layout_pin(text="vdd",
                      layer="metal1",
                      offset=vdd_offset,
                      width=self.width,
                      height=drc["minwidth_metal1"])
        self.vdd_positions.append(vdd_offset)

        # NOTE:the gnd rails are vertical so it is not connected horizontally
        # add gnd rail across entire array
        gnd_offset = base_offset + vector(self.sense_amp_chars["gnd"]).scale(0,1)
        self.add_layout_pin(text="gnd",
                      layer="metal1",
                      offset=gnd_offset,
                      width=self.width,
                      height=drc["minwidth_metal1"])
        self.gnd_positions.append(gnd_offset)

        # add sclk rail across entire array
        sclk_offset = base_offset + vector(self.sense_amp_chars["SCLK"]).scale(0,1)
        self.add_layout_pin(text="sclk",
                      layer="metal1",
                      offset=sclk_offset,
                      width=self.width,
                      height=drc["minwidth_metal1"])
        self.SCLK_positions.append(sclk_offset)
