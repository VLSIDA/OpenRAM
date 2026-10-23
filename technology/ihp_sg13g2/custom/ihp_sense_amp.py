"""Foundry clocked differential sense/latch, not a generic combinational SA.

CP high evaluates: DP > DN produces QP high / QN low. CP low precharges
the internal sense nodes while retaining the output. Power-up output is
undefined until a valid evaluation. Boundary is the geometry envelope.
"""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_sense_amp(design):
    def __init__(self, name):
        ports = ["cp", "dn", "dp", "qn", "qp", "vdd", "gnd"]
        types = ["INPUT"] * 3 + ["OUTPUT"] * 2 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_sense_amp", prop=cell(ports, types))
