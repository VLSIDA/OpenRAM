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


class dummy_bitcell_2port(bitcell_base.bitcell_base):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = [props.bitcell.cell_2port.pin.bl0,
                 props.bitcell.cell_2port.pin.br0,
                 props.bitcell.cell_2port.pin.bl1,
                 props.bitcell.cell_2port.pin.br1,
                 props.bitcell.cell_2port.pin.wl0,
                 props.bitcell.cell_2port.pin.wl1,
                 props.bitcell.cell_2port.pin.vdd,
                 props.bitcell.cell_2port.pin.gnd]
    type_list = ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT",
                 "INPUT", "INPUT", "POWER", "GROUND"]

    def __init__(self, name):
        super().__init__(name)
        debug.info(2, "Create dummy bitcell 2 port object")


