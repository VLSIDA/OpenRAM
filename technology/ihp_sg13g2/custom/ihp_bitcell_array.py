"""Foundry-framed 16-row array; deliberately not a global compiler override.

Use four-column groups to retain the shipped alternating M4 supply feeds.
Other row counts require a separately validated tap/strap topology.
"""

from openram.base import design, vector
from openram.drc.custom_cell_properties import cell
from openram.modules.bitcell_array import bitcell_array


class ihp_bitcell_array(bitcell_array):
    def __init__(self, rows, cols, column_offset=0, row_offset=0, name="",
                 left_rbl=None, right_rbl=None):
        if rows != 16 or cols < 4 or cols > 32 or cols % 4:
            raise ValueError("Foundry frame supports 16 rows and 4..32 columns in groups of four")
        if column_offset or row_offset or left_rbl or right_rbl:
            raise ValueError("Offset/replica frames have not been validated")
        super().__init__(rows, cols, name=name)

    def create_instances(self):
        super().create_instances()
        supplies = ["vdd", "gnd"]
        self.frame_tiles = []
        for kind, ports, types in [
            ("tile", supplies, ["POWER", "GROUND"]),
            ("edge", [f"wl_{r}" for r in range(16)] + supplies,
             ["INPUT"] * 16 + ["POWER", "GROUND"]),
            ("power", supplies, ["POWER", "GROUND"]),
        ]:
            mod = design("ihp_frame_" + kind, prop=cell(ports, types))
            count = {"tile": self.column_size // 2, "edge": 2,
                     "power": self.column_size // 4}[kind]
            for index in range(count):
                inst = self.add_inst(f"frame_{kind}_{index}", mod)
                self.connect_inst(self.get_wordline_names() + supplies if kind == "edge" else supplies)
                self.frame_tiles.append((kind, index, inst))

    def create_layout(self):
        self.place_array()
        for inst in self.cell_inst.values():
            inst.place(inst.offset + vector(1.61, .9), inst.mirror)
        self.width = self.column_size * 2.81 + 3.22
        self.height = 18.92
        for kind, index, inst in self.frame_tiles:
            if kind == "edge":
                inst.place((0 if index == 0 else self.width, 0), "R0" if index == 0 else "MY")
            else:
                inst.place((1.61 + index * (5.62 if kind == "tile" else 11.24), 0))
        self.add_layout_pins()
        self.route_supplies()
        self.add_boundary()
        # Verification is run explicitly with the installed PDK's runner,
        # against the shipped reference. The generic verifier is incomplete.

    def add_bitline_pins(self):
        for col in range(self.column_size):
            for pin, name in zip(self.cell.get_all_bitline_names(),
                                 self.get_bitline_names()[2 * col:2 * col + 2]):
                shape = self.cell_inst[0, col].get_pin(pin)
                self.add_layout_pin(name, shape.layer, (shape.lx(), .025),
                                    shape.width(), 18.87)
