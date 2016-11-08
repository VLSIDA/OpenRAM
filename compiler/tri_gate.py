import debug
import design
import utils
from tech import GDS,layer

class tri_gate(design.design):
    """
    This module implements the tri gate cell used in the design for
    bit-line isolation. It is a hand-made cell, so the layout and
    netlist should be available in the technology library.  
    """

    pins = ["in", "en", "en_bar", "out", "gnd", "vdd"]
    chars = utils.auto_measure_libcell(pins, "tri_gate", GDS["unit"], layer["boundary"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create tri_gate object")


        self.width = tri_gate.chars["width"]
        self.height = tri_gate.chars["height"]
