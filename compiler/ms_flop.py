import globals
import design
from math import log
import design
from tech import GDS,layer
import utils

class ms_flop(design.design):
    """
    Memory address flip-flop
    """

    pins = ["din", "dout", "dout_bar", "clk", "vdd", "gnd"]
    chars = utils.auto_measure_libcell(pins, "ms_flop", GDS["unit"], layer["boundary"])

    def __init__(self, name):
        design.design.__init__(self, name)

        self.width = ms_flop.chars["width"]
        self.height = ms_flop.chars["height"]

        self.clk_offset = ms_flop.chars["clk"]
        self.din_offset = ms_flop.chars["din"]
        self.dout_offset = ms_flop.chars["dout"]
        self.dout_bar_offset = ms_flop.chars["dout_bar"]
