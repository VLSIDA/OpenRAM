"""Four-column foundry data path, currently circuit-only.

Four BLDRVs share selected bitlines and one clocked sense/latch, as in
COLCTRL2. The caller supplies one-hot selection and nonoverlapping write,
precharge and sense controls. No generic precharge/mux/write blocks belong
alongside this module. Placement and parent supply routing are not yet
implemented; this is deliberately not registered as generic port_data.
"""

from openram import OPTS
from openram.base import design
from openram.sram_factory import factory


class ihp_column_data(design):
    def __init__(self, name):
        if not OPTS.netlist_only:
            raise NotImplementedError("IHP column-data layout is not yet verified; use netlist_only")
        super().__init__(name)
        for col in range(4):
            self.add_pin(f"bl_{col}", "INOUT")
            self.add_pin(f"br_{col}", "INOUT")
        for col in range(4):
            self.add_pin(f"sel_{col}", "INPUT")
        for pin in ("pre_n", "wr_one", "wr_zero", "sae"):
            self.add_pin(pin, "INPUT")
        self.add_pin("qp", "OUTPUT")
        self.add_pin("qn", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        driver = factory.create(module_type="ihp_bldrv")
        sense = factory.create(module_type="ihp_sense_amp")
        for col in range(4):
            self.add_inst(f"driver_{col}", driver)
            self.connect_inst([f"br_{col}", "br_sel", f"bl_{col}", "bl_sel",
                               "pre_n", f"sel_{col}", "wr_one", "wr_zero", "vdd", "gnd"])
        self.add_inst("sense", sense)
        self.connect_inst(["sae", "br_sel", "bl_sel", "qn", "qp", "vdd", "gnd"])
