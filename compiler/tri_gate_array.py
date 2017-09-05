import debug
from tech import drc
import design
from vector import vector
from globals import OPTS

class tri_gate_array(design.design):
    """
    Dynamically generated tri gate array of all bitlines.  words_per_row
    """

    def __init__(self, columns, word_size, row_locations=None):
        """Intial function of tri gate array """
        design.design.__init__(self, "tri_gate_array")
        debug.info(1, "Creating {0}".format(self.name))

        c = reload(__import__(OPTS.config.tri_gate))
        self.mod_tri_gate = getattr(c, OPTS.config.tri_gate)
        self.tri_gate_chars = self.mod_tri_gate.chars

        self.columns = columns
        self.word_size = word_size
        self.create_layout(row_locations)
        self.DRC_LVS()

    def create_layout(self, row_locations):
        """generate layout """
        self.add_modules()
        self.setup_layout_constants()
        self.add_pins()
        self.create_write_array(row_locations)
        self.add_metal_rails()
        self.add_labels(row_locations)

    def add_pins(self):
        """create the name of pins depend on the word size"""
        for i in range(self.word_size):
            self.add_pin("IN[{0}]".format(i))
        for i in range(self.word_size):
            self.add_pin("OUT[{0}]".format(i))
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
        self.in_positions = []
        self.out_positions = []

    def add_modules(self):
        """instantiation of a tri gate"""
        self.tri = self.mod_tri_gate("tri_gate")
        self.add_mod(self.tri)

    def create_write_array(self, row_locations):
        """add tri gate to the array """
        for i in range(self.word_size):
            mirror = "R0"
            if (i % 2 == 0):
                name = "Xtri_gate{0}".format(i)
                if row_locations == None:
                    x_off = i * self.tri.width * self.words_per_row
                else:
                    x_off = row_locations[ i * self.words_per_row][0]
            else:
                name = "Xtri_gate{0}".format(i)
                if (self.words_per_row == 1):
                    if row_locations == None:
                        x_off = (i + 1) * self.tri.width * self.words_per_row
                    else:
                        x_off = row_locations[(i + 1)* self.words_per_row][0]
                    mirror = "MY"
                else:
                    if row_locations == None:
                        x_off = i * self.tri.width * self.words_per_row
                    else:
                        x_off = row_locations[i * self.words_per_row][0]
            self.add_inst(name=name,
                          mod=self.tri,
                          offset=[x_off, 0],
                          mirror = mirror)
            self.connect_inst(["in[{0}]".format(i),
                               "out[{0}]".format(i),
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

    def add_labels(self, row_locations):
        """add label for pins"""
        for i in range(self.word_size):
            if (i % 2 == 0 or self.words_per_row > 1):
                if row_locations == None:
                    x_off = i * self.tri.width * self.words_per_row
                else:
                    x_off = row_locations[i * self.words_per_row][0]
                dir_vector = vector(1,1)
            else:
                if row_locations == None:
                    x_off = (i + 1) * self.tri.width * self.words_per_row
                else:
                    x_off = row_locations[(i+1) * self.words_per_row][0]
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
            self.add_label(text="in[{0}]".format(i),
                           layer="metal2",
                           offset=pin_offset["in"])
            self.add_label(text="out[{0}]".format(i),
                           layer="metal2",
                           offset=pin_offset["out"])

            self.vdd_positions.append(pin_offset["vdd"])
            self.gnd_positions.append(pin_offset["gnd"])
            self.in_positions.append(pin_offset["in"])
            self.out_positions.append(pin_offset["out"])

    def delay(self, slew, load=0.0):
        result = self.tri.delay(slew = slew, load = load)
        return result
