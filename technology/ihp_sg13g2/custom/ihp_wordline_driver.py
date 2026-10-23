"""Foundry sixteen-wordline buffer bank with unchanged source placement."""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_wordline_driver(design):
    def __init__(self, name):
        ports = [f"decode_{i}" for i in reversed(range(16))]
        ports += [f"wl_{i}" for i in reversed(range(16))] + ["vdd", "gnd"]
        types = ["INPUT"] * 16 + ["OUTPUT"] * 16 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_wordline_driver", prop=cell(ports, types))
