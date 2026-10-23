"""Four-column foundry data path with source placement and parent routing.

Four BLDRVs share selected bitlines and one clocked sense/latch, as in
COLCTRL2. The caller supplies one-hot selection and nonoverlapping write,
precharge and sense controls. No generic precharge/mux/write blocks belong
alongside this module. The boundary is a geometry envelope, not a repeat
pitch. This is deliberately not registered as generic port_data.
"""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_column_data(design):
    def __init__(self, name):
        ports = [p for col in range(4) for p in (f"bl_{col}", f"br_{col}")]
        ports += [f"sel_{col}" for col in range(4)]
        ports += ["pre_n", "wr_one", "wr_zero", "sae", "qp", "qn", "vdd", "gnd"]
        types = ["INOUT"] * 8 + ["INPUT"] * 8 + ["OUTPUT"] * 2 + ["POWER", "GROUND"]
        super().__init__(name, cell_name="ihp_column_data", prop=cell(ports, types))
