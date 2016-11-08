from math import log
import design
from tech import drc
import debug
from vector import vector
from globals import OPTS

class write_driver_array(design.design):
    """
    Array of tristate drivers to write to the bitlines through the column mux.
    Dynamically generated write driver array of all bitlines.
    """

    def __init__(self, columns, word_size):
        design.design.__init__(self, "write_driver_array")
        debug.info(1, "Creating {0}".format(self.name))

        c = reload(__import__(OPTS.config.write_driver))
        self.mod_write_driver = getattr(c, OPTS.config.write_driver)
        self.write_driver_chars = self.mod_write_driver.chars

        self.columns = columns
        self.word_size = word_size
        self.words_per_row = columns / word_size

        self.add_pins()
        self.create_layout()
        self.DRC_LVS()

    def add_pins(self):
        for i in range(self.word_size):
            self.add_pin("data_in[{0}]".format(i))
        if (self.words_per_row == 1):
            for i in range(self.word_size):
                self.add_pin("bl[{0}]".format(i))
                self.add_pin("br[{0}]".format(i))
        else:
            for i in range(self.word_size):
                self.add_pin("bl_out[{0}]".format(i * self.words_per_row))
                self.add_pin("br_out[{0}]".format(i * self.words_per_row))
        self.add_pin("wen")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        self.add_write_driver_module()
        self.setup_layout_constants()
        self.create_write_array()
        self.add_metal_rails()
        self.add_labels()
        self.offset_all_coordinates()

    def add_write_driver_module(self):
        self.driver = self.mod_write_driver("write_driver")
        self.add_mod(self.driver)

    def setup_layout_constants(self):
        self.width = self.columns * self.driver.width
        self.height = self.height = self.driver.height
        self.gnd_positions = []
        self.vdd_positions = []
        self.wen_positions = []
        self.BL_out_positions = []
        self.BR_out_positions = []
        self.driver_positions = []
        self.Data_in_positions = []

    def create_write_array(self):
        for i in range(self.word_size):
            name = "Xwrite_driver%d" % i
            x_off = (i* self.driver.width * self.words_per_row)
            self.driver_positions.append(vector(x_off, 0))
            self.add_inst(name=name,
                          mod=self.driver,
                          offset=[x_off, 0])
            if (self.words_per_row == 1):
                self.connect_inst(["data_in[{0}]".format(i),
                                   "bl[{0}]".format(i),
                                   "br[{0}]".format(i),
                                   "wen", "vdd", "gnd"])
            else:
                self.connect_inst(["data_in[{0}]".format(i),
                                   "bl_out[{0}]".format(i * self.words_per_row),
                                   "br_out[{0}]".format(i * self.words_per_row),
                                   "wen", "vdd", "gnd"])

    def add_metal_rails(self):
        base = vector(0, - 0.5*drc["minwidth_metal1"])
        self.add_rect(layer="metal1",
                      offset=base + vector(self.write_driver_chars["en"]).scale(0, 1),
                      width=self.width - (self.words_per_row - 1) * self.driver.width,
                      height=drc['minwidth_metal1'])
        self.add_rect(layer="metal1",
                      offset=base + vector(self.write_driver_chars["vdd"]).scale(0, 1),
                      width=self.width,
                      height=drc['minwidth_metal1'])
        self.add_rect(layer="metal1",
                      offset=base + vector(self.write_driver_chars["gnd"]).scale(0, 1),
                      width=self.width, 
                      height=drc['minwidth_metal1'])

    def add_labels(self):
        for i in range(self.word_size):
            base = vector(i * self.driver.width * self.words_per_row, 0)
            BL_offset = base + self.write_driver_chars["BL"]
            BR_offset = base + self.write_driver_chars["BR"]

            self.add_label(text="data_in[{0}]".format(i),
                           layer="metal2",
                           offset=base + self.write_driver_chars["din"])
            if (self.words_per_row == 1):
                self.add_label(text="bl[{0}]".format(i),
                               layer="metal2",
                               offset=BL_offset)
                self.add_label(text="br[{0}]".format(i),
                               layer="metal2",
                               offset=BR_offset)
            else:
                self.add_label(text="bl_out[{0}]".format(i*self.words_per_row),
                               layer="metal2",
                               offset=BL_offset)
                self.add_label(text="br_out[{0}]".format(i*self.words_per_row),
                               layer="metal2",
                               offset=BR_offset)
            self.BL_out_positions.append(BL_offset)
            self.BR_out_positions.append(BR_offset)
            self.Data_in_positions.append(base + self.write_driver_chars["din"])

        base = vector(0, - 0.5 * drc["minwidth_metal1"])
        self.add_label(text="wen",
                       layer="metal1",
                       offset=base + vector(self.write_driver_chars["en"]).scale(0,1))
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=base + vector(self.write_driver_chars["vdd"]).scale(0,1))
        self.add_label(text="gnd",
                       layer="metal1",
                       offset=base + vector(self.write_driver_chars["gnd"]).scale(0,1))
        self.wen_positions.append(base + vector(self.write_driver_chars["en"]).scale(0,1))
        self.vdd_positions.append(base + vector(self.write_driver_chars["vdd"]).scale(0,1))
        self.gnd_positions.append(base + vector(self.write_driver_chars["gnd"]).scale(0,1))

        self.add_label(text="WRITE DRIVER",
                       layer="text",
                       offset=[self.width / 2.0,
                               self.height / 2.0])
