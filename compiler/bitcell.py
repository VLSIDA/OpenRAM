import design
import debug
import utils
from tech import GDS,layer

class bitcell(design.design):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    pins = ["BL", "BR", "WL", "vdd", "gnd"]
    chars = utils.auto_measure_libcell(pins, "cell_6t", GDS["unit"], layer["boundary"])

    def __init__(self, name="cell_6t"):
        design.design.__init__(self, name)
        debug.info(2, "Create bitcell object")

        self.width = bitcell.chars["width"]
        self.height = bitcell.chars["height"]

    def delay(self, slope, load=0):
        # delay of bit cell is not like a driver(from WL)
        # so the slope used should be 0
        # it should not be slope dependent?
        # because the value is there
        # the delay is only over half transsmission gate
        r = 9250.0*3
        c_para = 0.7#ff
        result = self.cal_delay_with_rc(r = r, c =  c_para+load, slope =slope)
        return result
