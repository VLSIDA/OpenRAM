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
from tech import cell_properties as props
import bitcell_base


class col_cap_bitcell_1rw_1r(bitcell_base.bitcell_base):
    """
    todo"""

    pin_names = [props.bitcell.cell_1rw1r.pin.bl0,
                 props.bitcell.cell_1rw1r.pin.br0,
                 props.bitcell.cell_1rw1r.pin.bl1,
                 props.bitcell.cell_1rw1r.pin.br1,
                 props.bitcell.cell_1rw1r.pin.vdd]

    type_list = ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT",
                 "POWER", "GROUND"]

    (width, height) = utils.get_libcell_size("col_cap_cell_1rw_1r",
                                             GDS["unit"],
                                             layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names,
                                     "col_cap_cell_1rw_1r",
                                     GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        bitcell_base.bitcell_base.__init__(self, "col_cap_cell_1rw_1r")
        debug.info(2, "Create col_cap bitcell 1rw+1r object")

        self.width = col_cap_bitcell_1rw_1r.width
        self.height = col_cap_bitcell_1rw_1r.height
        self.pin_map = col_cap_bitcell_1rw_1r.pin_map
        self.add_pin_types(self.type_list)
