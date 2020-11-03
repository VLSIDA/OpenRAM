# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
from tech import cell_properties as props
import bitcell_base


class row_cap_bitcell_1rw_1r(bitcell_base.bitcell_base):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = [props.bitcell.cell_1rw1r.pin.wl0,
                 props.bitcell.cell_1rw1r.pin.wl1,
                 props.bitcell.cell_1rw1r.pin.gnd]
    type_list = ["INPUT", "INPUT", "GROUND"]

    def __init__(self, name="row_cap_cell_1rw_1r", cell_name=None):
        if not cell_name:
            cell_name = name
        bitcell_base.bitcell_base.__init__(self, name, cell_name)
        debug.info(2, "Create row_cap bitcell 1rw+1r object")

        self.no_instances = True
