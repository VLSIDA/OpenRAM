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

    pin_names = ["bl", "br", "wl", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("cell_6t", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "cell_6t", GDS["unit"], layer["boundary"])

    def __init__(self):
        design.design.__init__(self, "cell_6t")
        debug.info(2, "Create bitcell")

        self.width = bitcell.width
        self.height = bitcell.height
        self.pin_map = bitcell.pin_map

    def analytical_delay(self, slew, load=0, swing = 0.5):
        # delay of bit cell is not like a driver(from WL)
        # so the slew used should be 0
        # it should not be slew dependent?
        # because the value is there
        # the delay is only over half transsmission gate
        from tech import spice
        r = spice["min_tx_r"]*3
        c_para = spice["min_tx_drain_c"]
        result = self.cal_delay_with_rc(r = r, c =  c_para+load, slew = slew, swing = swing)
        return result
   
 
    def list_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = ["bl[{0}]".format(col),
                        "br[{0}]".format(col),
                        "wl[{0}]".format(row),
                        "vdd",
                        "gnd"]
        return bitcell_pins
        
    
    def list_row_pins(self):
        """ Creates a list of all row pins (except for gnd and vdd) """
        row_pins = ["wl"]    
        return row_pins
    
    def list_read_row_pins(self):
        """ Creates a list of row pins associated with read ports """
        row_pins = ["wl"]    
        return row_pins
        
    def list_write_row_pins(self):
        """ Creates a list of row pins associated with write ports """
        row_pins = ["wl"]    
        return row_pins
    
    
    def list_column_pins(self):
        """ Creates a list of all column pins (except for gnd and vdd) """
        column_pins = ["bl", "br"]
        return column_pins
        
    def list_read_column_pins(self):
        """ Creates a list of column pins associated with read ports """
        column_pins = ["bl"]
        return column_pins
    
    def list_read_bar_column_pins(self):
        """ Creates a list of column pins associated with read_bar ports """
        column_pins = ["br"]
        return column_pins
        
    def list_write_column_pins(self):
        """ Creates a list of column pins associated with write ports """
        column_pins = ["bl"]
        return column_pins
    
    def list_write_bar_column_pins(self):
        """ Creates a list of column pins asscociated with write_bar ports"""
        column_pins = ["br"]
        return column_pins
    
    def analytical_power(self, proc, vdd, temp, load):
        """Bitcell power in nW. Only characterizes leakage."""
        from tech import spice
        leakage = spice["bitcell_leakage"]
        dynamic = 0 #temporary
        total_power = self.return_power(dynamic, leakage)
        return total_power

