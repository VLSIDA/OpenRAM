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

    def delay(self, slope, load=0.0):
        from tech import spice
        r = spice["min_tx_r"]
        c_para = spice["min_tx_c_para"]#ff
        return self.cal_delay_with_rc(r = r, c =  c_para+load, slope =slope)


    def input_load(self):
        return 9*spice["min_tx_gate_c"]

