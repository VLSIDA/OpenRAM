"""Binary-addressed foundry slice; cycle timing and write encoding are external.

Placement follows the shipped macro's right bank. This intermediate assembly
is not a generic bank replacement or a synchronous SRAM interface.
"""

from openram import OPTS
from openram.base import design
from openram.sram_factory import factory


class ihp_row_memory(design):
    def __init__(self, name, cols=4):
        super().__init__(name)
        self.memory = factory.create(module_type="ihp_memory_slice", cols=cols)
        self.decoder = factory.create(module_type="ihp_row_decoder")
        self.driver = factory.create(module_type="ihp_wordline_driver")
        self.column_decoder = factory.create(module_type="ihp_column_decoder")
        inputs = [f"addr_{i}" for i in reversed(range(4))] + ["cs", "eclk"]
        for pin in inputs:
            self.add_pin(pin, "INPUT")
        for pin in ("col_1", "col_0"):
            self.add_pin(pin, "INPUT")
        for pin in list(self.memory.pins)[20:]:
            self.add_pin(pin, self.memory.get_pin_type(pin))
        self.decoder_inst = self.add_inst("decoder", self.decoder)
        decode = [f"decode_{i}" for i in reversed(range(16))]
        wordlines = [f"wl_{i}" for i in reversed(range(16))]
        self.connect_inst(inputs + decode + ["vdd", "gnd"])
        self.driver_inst = self.add_inst("driver", self.driver)
        self.connect_inst(decode + wordlines + ["vdd", "gnd"])
        self.column_decoder_inst = self.add_inst("column_decoder", self.column_decoder)
        self.connect_inst(["col_1", "col_0"] + [f"sel_{i}" for i in range(4)] + ["vdd", "gnd"])
        self.memory_inst = self.add_inst("memory", self.memory)
        self.connect_inst(list(self.memory.pins))
        if not OPTS.netlist_only:
            self.create_layout()

    def create_layout(self):
        # A 1.2 um left channel keeps new power via stacks outside the
        # foundry decoder's tightly packed M2/M3 routing.
        self.decoder_inst.place((1.2, 33.6))
        self.driver_inst.place((29.76, 33.6))
        self.column_decoder_inst.place((4, 18))
        self.memory_inst.place((41.25, 0))
        self.width = 41.25 + self.memory.width
        self.height = self.memory.height
        for row in range(16):
            for source, source_pin, target, target_pin in (
                (self.decoder_inst, f"decode_{row}", self.driver_inst, f"decode_{row}"),
                (self.driver_inst, f"wl_{row}", self.memory_inst, f"wl_{row}"),
            ):
                left = min(source.get_pins(source_pin), key=lambda p: p.lx())
                right = min(target.get_pins(target_pin), key=lambda p: p.lx())
                self.add_path("m3", [left.center(), right.center()], width=.2)
        for pin in list(self.pins)[:6]:
            self.copy_layout_pin(self.decoder_inst, pin)
        for bit in (1, 0):
            self.copy_layout_pin(self.column_decoder_inst, f"addr_{bit}", f"col_{bit}")
        for pin in list(self.memory.pins)[20:]:
            self.copy_layout_pin(self.memory_inst, pin)
        # Existing M3 select rails abut across all column-data groups.
        # Escape the closely pitched decoder outputs before placing vias;
        # four M4 drops in the reserved channel then reach those M3 rails.
        for col, x, y in ((0, 24, 27), (1, 23, 25.5), (2, 21, 22.5), (3, 22, 24.3)):
            pin = self.column_decoder_inst.get_pin(f"sel_{col}")
            self.add_path("m3", [pin.rc(), (x, pin.cy()), (x, y)], width=.2)
            self.add_via_stack_center((x, y), "m3", "m4", min_area=True)
            target_y = 12.15 + .51 * col
            self.add_path("m4", [(x, y), (x, target_y)], width=.3)
            self.add_via_stack_center((x, target_y), "m3", "m4", min_area=True)
            self.add_path("m3", [(x, target_y), (43.2, target_y)], width=.26)
        # Join the source's split M1 supply rails and take power over the
        # signal routing on M5, landing only on the matching M4 array feed.
        for pin, y in (("gnd", 33.9), ("vdd", 38.1)):
            self.add_rect("m1", (.3, y - .3), width=38.64, height=.6)
            start = (.3, y)
            feed = min((p for p in self.memory_inst.get_pins(pin) if p.layer == "m4"),
                       key=lambda p: p.lx())
            end = (feed.cx(), y)
            self.add_via_stack_center(start, "m1", "m5", min_area=True)
            self.add_via_stack_center(end, "m4", "m5", min_area=True)
            self.add_path("m5", [start, end], width=.6)
        for pin, x, y, rail_y in (("vdd", 3.5, 18.525, 38.1), ("gnd", 1.3, 22.725, 33.9)):
            self.add_path("m1", [(x, y), (4.8, y)], width=.6)
            self.add_via_stack_center((x, y), "m1", "m4", min_area=True)
            if pin == "gnd":
                # The decoder has a VDD M4 shape just to the right of the
                # existing ground via. Approach that via from below/left.
                self.add_path("m4", [(x, y), (x, 32.7), (.3, 32.7), (.3, rail_y)], width=.6)
            else:
                self.add_path("m4", [(x, y), (x, rail_y)], width=.6)
                self.add_via_stack_center((x, rail_y), "m4", "m5", min_area=True)
        self.add_boundary()
