# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import utils
from tech import GDS, layer
import bitcell_base


class dummy_bitcell(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    pin_names = ["bl", "br", "wl", "vdd", "gnd"]
    (width, height) = utils.get_libcell_size("dummy_cell_6t",
                                             GDS["unit"],
                                             layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dummy_cell_6t", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        bitcell_base.bitcell_base.__init__(self, "dummy_cell_6t")
        debug.info(2, "Create dummy bitcell")

        self.width = dummy_bitcell.width
        self.height = dummy_bitcell.height
        self.pin_map = dummy_bitcell.pin_map


