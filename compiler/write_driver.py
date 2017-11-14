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

    pin_names = ["din", "BL", "BR", "en", "gnd", "vdd"]
    (width,height) = utils.get_libcell_size("write_driver", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "write_driver", GDS["unit"], layer["boundary"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create write_driver")

        self.width = write_driver.width
        self.height = write_driver.height
        self.pin_map = write_driver.pin_map

