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

        c = reload(__import__(OPTS.config.tri_gate))
        self.mod_tri_gate = getattr(c, OPTS.config.tri_gate)
        self.tri_gate_chars = self.mod_tri_gate.chars

        self.columns = columns
        self.word_size = word_size
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        """generate layout """
        self.add_modules()
        self.setup_layout_constants()
        self.add_pins()
        self.create_write_array()
        self.add_metal_rails()
        self.add_labels()

    def add_pins(self):
        """create the name of pins depend on the word size"""
        for i in range(self.word_size):
            self.add_pin("tri_in[{0}]".format(i))
        for i in range(self.word_size):
            self.add_pin("DATA[{0}]".format(i))
        for pin in ["en", "en_bar", "vdd", "gnd"]:
            self.add_pin(pin)

    def setup_layout_constants(self):
        """caculate the size of tri gate array"""
        self.words_per_row = self.columns / self.word_size
        self.width = (self.columns / self.words_per_row) * self.tri.width
        self.height = self.tri.height
        self.tri_gate_positions = []
        self.vdd_positions = []
        self.gnd_positions = []
        self.tri_in_positions = []
        self.DATA_positions = []

    def add_modules(self):
        """instantiation of a tri gate"""
        self.tri = self.mod_tri_gate("tri_gate")
        self.add_mod(self.tri)

    def create_write_array(self):
        """add tri gate to the array """
        for i in range(self.word_size):
            mirror = "R0"
            if (i % 2 == 0):
                name = "Xtri_gate{0}".format(i)
                x_off = i * self.tri.width * self.words_per_row
            else:
                name = "Xtri_gate{0}".format(i)
                if (self.words_per_row == 1):
                    x_off = (i + 1) * self.tri.width * self.words_per_row
                    mirror = "MY"
                else:
                    x_off = i * self.tri.width * self.words_per_row
            self.add_inst(name=name,
                          mod=self.tri,
                          offset=[x_off, 0],
                          mirror = mirror)
            self.connect_inst(["tri_in[{0}]".format(i),
                               "DATA[{0}]".format(i),
                               "en", "en_bar", "vdd", "gnd"])

    def add_metal_rails(self):
        """Connect en en_bar and vdd together """
        correct = vector(0, 0.5 * drc["minwidth_metal1"])
        width = (self.tri.width * self.columns 
                     - (self.words_per_row - 1) * self.tri.width)
        self.add_rect(layer="metal1",
                      offset=(self.tri_gate_chars["en"] - correct).scale(0, 1),
                      width=width,
                      height=drc['minwidth_metal1'])
        self.add_rect(layer="metal1",
                      offset=(self.tri_gate_chars["en_bar"] - correct).scale(0, 1),
                      width=width,
                      height=drc['minwidth_metal1'])
        self.add_rect(layer="metal1",
                      offset=(self.tri_gate_chars["vdd"] - correct).scale(0, 1),
                      width=width,
                      height=drc['minwidth_metal1'])

    def add_labels(self):
        """add label for pins"""
        for i in range(self.word_size):
            if (i % 2 == 0 or self.words_per_row > 1):
                x_off = i * self.tri.width * self.words_per_row
                dir_vector = vector(1,1)
            else:
                x_off = (i + 1) * self.tri.width * self.words_per_row
                dir_vector = vector(-1,1)

            pin_offset={}
            for pin in ["en", "en_bar", "vdd", "gnd", "in", "out"]:
                pin_offset[pin] = vector(x_off, 0) + dir_vector.scale(self.tri_gate_chars[pin])

            for pin in ["en", "en_bar", "vdd"]:
                self.add_label(text=pin,
                               layer="metal1",
                               offset=pin_offset[pin])
            self.add_label(text="gnd",
                           layer="metal2",
                           offset=pin_offset["gnd"])
            self.add_label(text="tri_in[{0}]".format(i),
                           layer="metal2",
                           offset=pin_offset["in"])
            self.add_label(text="DATA[{0}]".format(i),
                           layer="metal2",
                           offset=pin_offset["out"])

            self.vdd_positions.append(pin_offset["vdd"])
            self.gnd_positions.append(pin_offset["gnd"])
            self.tri_in_positions.append(pin_offset["in"])
            self.DATA_positions.append(pin_offset["out"])

        self.add_label(text="tri gate",
                       layer="text",
                       offset=[self.width / 2.0,
                               self.height / 2.0])

    def delay(self, slope, load=0.0):
        result = self.tri.delay(slope = slope, 
                                    load = load)
        return result
