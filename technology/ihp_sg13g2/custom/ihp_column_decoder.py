"""Foundry combinational 2-to-4 column decode, without BIST or registers.

Exactly one select is high after settling. Address must remain stable
through a read/write cycle; this block does not latch or gate selection.
"""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_column_decoder(design):
    def __init__(self, name):
        ports = ["addr_1", "addr_0"] + [f"sel_{i}" for i in range(4)] + ["vdd", "gnd"]
        types = ["INPUT"] * 2 + ["OUTPUT"] * 4 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_column_decoder", prop=cell(ports, types))
