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

