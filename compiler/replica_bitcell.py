import design
import debug
import utils
from tech import GDS,layer

class replica_bitcell(design.design):
    """
    A single bit cell (6T, 8T, etc.)
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = ["BL", "BR", "WL", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("replica_cell_6t", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "replica_cell_6t", GDS["unit"], layer["boundary"])

    def __init__(self):
        design.design.__init__(self, "replica_cell_6t")
        debug.info(2, "Create replica bitcell object")

        self.width = replica_bitcell.width
        self.height = replica_bitcell.height
        self.pin_map = replica_bitcell.pin_map
