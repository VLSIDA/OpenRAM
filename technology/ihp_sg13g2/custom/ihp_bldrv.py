"""Unchanged foundry combined precharge/select/write hard cell.

Not a replacement for the generic write_driver slot: a future IHP port_data
must instantiate this instead of all three separate column functions.
PRE_N is active low; SEL_P and the mutually exclusive WR_ONE/WR_ZERO are
active high. All VDD/GND pin shapes are must-connect at the parent level.
The boundary is the geometry envelope, not the foundry placement pitch.
"""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_bldrv(design):
    def __init__(self, name):
        ports = ["br", "br_sel", "bl", "bl_sel", "pre_n", "sel_p",
                 "wr_one", "wr_zero", "vdd", "gnd"]
        types = ["INOUT"] * 4 + ["INPUT"] * 4 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_bldrv", prop=cell(ports, types))
