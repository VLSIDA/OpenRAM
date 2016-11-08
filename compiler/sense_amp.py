import design
import debug
import utils
from tech import GDS,layer

class sense_amp(design.design):
    """
    This module implements the single sense amp cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    Sense amplifier to read a pair of bit-lines.
    """

    pins = ["BL", "BR", "Dout", "SCLK", "vdd", "gnd"]
    chars = utils.auto_measure_libcell(pins, "sense_amp", GDS["unit"], layer["boundary"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create Sense Amp object")

        self.width = sense_amp.chars["width"]
        self.height = sense_amp.chars["height"]

