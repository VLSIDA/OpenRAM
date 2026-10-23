"""Foundry 4-to-16 row decoder; native CS latch and ECLK gating.

This is not a combinational replacement for OpenRAM's generic decoder.
The boundary is the source geometry envelope, not a placement pitch.
"""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_row_decoder(design):
    def __init__(self, name):
        ports = [f"addr_{i}" for i in reversed(range(4))] + ["cs", "eclk"]
        ports += [f"decode_{i}" for i in reversed(range(16))] + ["vdd", "gnd"]
        types = ["INPUT"] * 6 + ["OUTPUT"] * 16 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_row_decoder", prop=cell(ports, types))
