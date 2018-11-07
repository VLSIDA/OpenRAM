import design
import debug
import utils
from tech import GDS,layer

class replica_bitcell_1rw_1r(design.design):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = ["bl0", "br0", "bl1", "br1", "wl0", "wl1", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("replica_cell_1rw_1r", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "replica_cell_1rw_1r", GDS["unit"])

    def __init__(self):
        design.design.__init__(self, "replica_cell_1rw_1r")
        debug.info(2, "Create replica bitcell 1rw+1r object")

        self.width = replica_bitcell_1rw_1r.width
        self.height = replica_bitcell_1rw_1r.height
        self.pin_map = replica_bitcell_1rw_1r.pin_map
