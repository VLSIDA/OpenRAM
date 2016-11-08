import debug
import design
import utils
from tech import GDS,layer

class write_driver(design.design):
    """
    Tristate write driver to be active during write operations only.       
    This module implements the write driver cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    """

    pins = ["din", "BL", "BR", "en", "gnd", "vdd"]
    chars = utils.auto_measure_libcell(pins, "write_driver", GDS["unit"], layer["boundary"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create write_driver object")

        self.width = write_driver.chars["width"]
        self.height = write_driver.chars["height"]

