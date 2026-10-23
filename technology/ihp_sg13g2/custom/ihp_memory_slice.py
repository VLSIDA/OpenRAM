"""Framed 16-row array plus four-way column-data groups.

Wordline, one-hot column select, write encoding and sense timing are
external. This is not yet an addressed/clocked OpenRAM bank. Placement
follows the right-hand bank of the shipped 64x16 macro, including the
25 nm overlap at the bitline interface. Boundaries are not tiling pitches.
"""

from openram import OPTS
from openram.base import design
from openram.sram_factory import factory


class ihp_memory_slice(design):
    def __init__(self, name, cols=4):
        if cols < 4 or cols > 32 or cols % 4:
            raise ValueError("Memory slice supports 16 rows and 4..32 columns in groups of four")
        super().__init__(name)
        self.cols = cols
        self.array = factory.create(module_type="ihp_bitcell_array", rows=16, cols=cols)
        self.column = factory.create(module_type="ihp_column_data")
        for row in range(16):
            self.add_pin(f"wl_{row}", "INPUT")
        for col in range(4):
            self.add_pin(f"sel_{col}", "INPUT")
        for group in range(cols // 4):
            for pin in ("pre_n", "sae", "wr_one", "wr_zero"):
                self.add_pin(f"{pin}_{group}", "INPUT")
            for pin in ("qp", "qn"):
                self.add_pin(f"{pin}_{group}", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

        self.array_inst = self.add_inst("array", self.array)
        self.connect_inst(self.array.get_bitline_names() + [f"wl_{r}" for r in range(16)] + ["vdd", "gnd"])
        self.column_insts = []
        for group in range(cols // 4):
            self.column_insts.append(self.add_inst(f"column_{group}", self.column))
            self.connect_inst([p for c in range(4 * group, 4 * group + 4)
                               for p in (f"bl_0_{c}", f"br_0_{c}")] +
                              [f"sel_{c}" for c in range(4)] +
                              [f"pre_n_{group}", f"wr_one_{group}", f"wr_zero_{group}", f"sae_{group}",
                               f"qp_{group}", f"qn_{group}", "vdd", "gnd"])
        if not OPTS.netlist_only:
            self.create_layout()

    def create_layout(self):
        self.array_inst.place((0, 32.84))
        self.width = self.array.width
        self.height = 51.76
        for row in range(16):
            self.copy_layout_pin(self.array_inst, f"wl_0_{row}", f"wl_{row}")
        for group, inst in enumerate(self.column_insts):
            inst.place((1.26 + 11.24 * group, 0))
            # The column's M4 VDD feed stops below the array. Unlike GND,
            # it does not join by abutment: bridge the gap on the same M4
            # track, with overlap into both existing 2.81 um-wide stripes.
            self.add_rect("m4", (7.39 + 11.24 * group, 26), width=2.81, height=7)
            if group < len(self.column_insts) - 1:
                # COLCTRL2's parent-level 20 nm active bridges complete the
                # shared tap stripes across its 11.24 um placement pitch.
                # They are not part of the isolated column hard cell.
                for y in (12.75, 16.95, 21.15, 29.55):
                    self.add_rect("active", (12.99 + 11.24 * group, y), width=.02, height=.3)
            for pin in ("vdd", "gnd"):
                self.copy_layout_pin(inst, pin)
            for col in range(4):
                self.copy_layout_pin(inst, f"sel_{col}")
            for pin in ("pre_n", "sae", "wr_one", "wr_zero", "qp", "qn"):
                self.copy_layout_pin(inst, pin, f"{pin}_{group}")
        for pin in ("vdd", "gnd"):
            self.copy_layout_pin(self.array_inst, pin)
        self.add_boundary()
