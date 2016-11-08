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

    def __init__(self, name, array_type, columns, word_size):
        self.array_type = array_type
        self.columns = columns
        self.word_size = word_size
        design.design.__init__(self, name)
        debug.info(1, "Creating %s" % self.name)

        c = reload(__import__(OPTS.config.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.config.ms_flop)
        self.ms_flop_chars = self.mod_ms_flop.chars

        self.create_layout()

    def create_layout(self):
        self.add_modules()
        self.setup_layout_constants()
        self.add_pins()
        self.create_ms_flop_array()
        self.add_labels()
        self.DRC_LVS()

    def add_modules(self):
        self.ms_flop = self.mod_ms_flop("ms_flop")
        self.add_mod(self.ms_flop)

    def setup_layout_constants(self):
        self.width = self.columns * self.ms_flop.width
        self.height = self.ms_flop.height
        self.words_per_row = self.columns / self.word_size

        self.flop_positions = []
        self.vdd_positions = []
        self.gnd_positions = []
        self.clk_positions = []
        self.dout_positions = []
        self.dout_bar_positions = []
        self.din_positions = []

    def add_pins(self):
        if (self.array_type == "data_in"):
            pins = {"data_in": 1, "din": "DATA", "dout": "data_in", "dout_bar": "data_in_bar", "clk": "clk"}
        elif (self.array_type == "data_out"):
            pins = {"data_out": 1, "din": "data_out", "dout": "tri_in", "dout_bar": "tri_in_bar", "clk": "sclk"}
        elif (self.array_type == "address"):
            pins = {"address": 1, "din": "ADDR", "dout": "A", "dout_bar": "A_bar", "clk": "addr_clk"}
        self.input_output_pins = pins 
        assert(self.array_type in pins), "Invalid input for array_type"

        for i in range(self.word_size):
            self.add_pin(self.input_output_pins["din"] + "[{0}]".format(i))
        for i in range(self.word_size):
            self.add_pin(self.input_output_pins["dout"] + "[{0}]".format(i))
            self.add_pin(self.input_output_pins["dout_bar"] + "[{0}]".format(i))
        self.add_pin(self.input_output_pins["clk"])
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_ms_flop_array(self):
        for i in range(self.word_size):
            name = "Xdff%d" % i
            if (i % 2 == 0):
                x_off = i * self.ms_flop.width * self.words_per_row
                mirror = "None"
            else:
                if (self.words_per_row == 1):
                    x_off = (i + 1) * self.ms_flop.width
                    mirror="MY"
                else:
                    x_off = i * self.ms_flop.width * self.words_per_row
            self.add_inst(name=name,
                          mod=self.ms_flop,
                          offset=[x_off, 0], 
                          mirror=mirror)
            self.connect_inst([self.input_output_pins["din"] + "[{0}]".format(i),
                               self.input_output_pins["dout"] + "[{0}]".format(i),
                               self.input_output_pins["dout_bar"] + "[{0}]".format(i),
                               self.input_output_pins["clk"],
                               "vdd", "gnd"])
            self.flop_positions.append(vector(x_off, 0))

    def add_labels(self):
        for i in range(self.word_size):
            i_str = "[{0}]".format(i)
            if (i % 2 == 0 or self.words_per_row > 1):
                base = vector(i * self.ms_flop.width * self.words_per_row, 0)
                self.add_label(text="gnd",
                               layer="metal2",
                               offset=base + self.ms_flop_chars["gnd"])
                self.add_label(text=self.input_output_pins["din"] + i_str,
                               layer="metal2",
                               offset=base + self.ms_flop_chars["din"])
                self.add_label(text=self.input_output_pins["dout"] + i_str,
                               layer="metal2",
                               offset=base + self.ms_flop_chars["dout"])
                self.add_label(text=self.input_output_pins["dout_bar"] + i_str,
                               layer="metal2",
                               offset=base + self.ms_flop_chars["dout_bar"])

                self.din_positions.append(base + self.ms_flop_chars["din"])
                self.dout_positions.append(base + self.ms_flop_chars["dout"])
                self.dout_bar_positions.append(base + self.ms_flop_chars["dout_bar"])
                self.gnd_positions.append(base + self.ms_flop_chars["gnd"])
            else:
                base = vector((i + 1) * self.ms_flop.width, 0)
                gnd_offset = base + vector(self.ms_flop_chars["gnd"]).scale(-1,1)
                din_offset = base + vector(self.ms_flop_chars["din"]).scale(-1,1)
                dout_offset = base + vector(self.ms_flop_chars["dout"]).scale(-1,1)
                dout_bar_offset = base + vector(self.ms_flop_chars["dout_bar"]).scale(-1,1)

                self.add_label(text="gnd",
                               layer="metal2",
                               offset=gnd_offset)
                self.add_label(text=self.input_output_pins["din"] + i_str,
                               layer="metal2",
                               offset=din_offset)
                self.add_label(text=self.input_output_pins["dout"] + i_str,
                               layer="metal2",
                               offset=dout_offset)
                self.add_label(text=self.input_output_pins["dout_bar"] + i_str,
                               layer="metal2",
                               offset=dout_bar_offset)

                self.gnd_positions.append(gnd_offset)
                self.din_positions.append(din_offset)
                self.dout_positions.append(dout_offset)
                self.dout_bar_positions.append(dout_bar_offset)

        # Continous "clk" rail along with label.
        self.add_rect(layer="metal1",
                      offset=[0, self.ms_flop_chars["clk"][1]],
                      width=self.width,
                      height=-drc["minwidth_metal1"])
        self.add_label(text=self.input_output_pins["clk"],
                       layer="metal1",
                       offset=self.ms_flop_chars["clk"])
        self.clk_positions.append(vector(self.ms_flop_chars["clk"]))

        # Continous "Vdd" rail along with label.
        self.add_rect(layer="metal1",
                      offset=[0, self.ms_flop_chars["vdd"][1] - 0.5 * drc["minwidth_metal1"]],
                      width=self.width,
                      height=drc["minwidth_metal1"])
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=vector(self.ms_flop_chars["vdd"]).scale(0, 1))
        self.vdd_positions.append(vector(self.ms_flop_chars["vdd"]).scale(0, 1))

        self.add_label(text=self.array_type + "ms_flop",
                       layer="text",
                       offset=[self.width / 2.0,
                               self.height / 2.0])
