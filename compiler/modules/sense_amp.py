import design
import debug
import utils
from tech import GDS,layer, parameter,drc

class sense_amp(design.design):
    """
    This module implements the single sense amp cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    Sense amplifier to read a pair of bit-lines.
    """

    pin_names = ["bl", "br", "dout", "en", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("sense_amp", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "sense_amp", GDS["unit"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create sense_amp")

        self.width = sense_amp.width
        self.height = sense_amp.height
        self.pin_map = sense_amp.pin_map

    def input_load(self):
        #Input load for the bitlines which are connected to the source/drain of a TX. Not the selects.
        from tech import spice, parameter
        # Default is 8x. Per Samira and Hodges-Jackson book:
        # "Column-mux transistors driven by the decoder must be sized for optimal speed"
        bitline_pmos_size = 8 #FIXME: This should be set somewhere and referenced. Probably in tech file.
        return spice["min_tx_drain_c"]*(bitline_pmos_size/parameter["min_tx_size"])#ff   
        
    def analytical_delay(self, slew, load=0.0):
        from tech import spice
        r = spice["min_tx_r"]/(10)
        c_para = spice["min_tx_drain_c"]
        result = self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew)
        return self.return_delay(result.delay, result.slew)

    def analytical_power(self, proc, vdd, temp, load):
        """Returns dynamic and leakage power. Results in nW"""
        #Power in this module currently not defined. Returns 0 nW (leakage and dynamic).
        total_power = self.return_power()
        return total_power

    def get_en_cin(self):
        """Get the relative capacitance of sense amp enable gate cin"""
        pmos_cin = parameter["sa_en_pmos_size"]/drc("minwidth_tx")
        nmos_cin = parameter["sa_en_nmos_size"]/drc("minwidth_tx")
        #sen is connected to 2 pmos isolation TX and 1 nmos per sense amp.
        return 2*pmos_cin + nmos_cin