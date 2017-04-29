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

    def delay(self, bl_delay, load=0.0):
        #init_point = {"delay":- 0.5 * bl_delay["slope"], "slope":0}
        init_point = - 0.5 * bl_delay["slope"]
        slope =  0
        r = 9250.0/(10)
        c_para = 0.7#ff
        if isinstance(load, float):
            result = self.cal_delay_with_rc(r = r, c =  c_para+load, slope =slope)
        else:
            delay_to_out_node = 0.7*r*(c_para+load["lump_num"]*0.5*load["wire_c"])
            delay_to_out_node = delay_to_out_node*0.001#make the unit to ps
            slope_at_out_node = delay_to_out_node*0.6*2 + 0.005* slope # the constant before slope should be explained as r change
            result = {"delay":delay_to_out_node+init_point, "slope":slope_at_out_node}
        return result
