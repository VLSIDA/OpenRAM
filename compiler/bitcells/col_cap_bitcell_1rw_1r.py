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
    
    def __init__(self, name="col_cap_cell_1rw_1r"):
        # Ignore the name argument
        bitcell_base.bitcell_base.__init__(self, name)
        debug.info(2, "Create col_cap bitcell 1rw+1r object")

        self.no_instances = True
