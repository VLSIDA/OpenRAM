"""Row-addressed foundry slice; column selection and cycle timing are external.

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
        inputs = [f"addr_{i}" for i in reversed(range(4))] + ["cs", "eclk"]
        for pin in inputs:
            self.add_pin(pin, "INPUT")
        for pin in list(self.memory.pins)[16:]:
            self.add_pin(pin, self.memory.get_pin_type(pin))
        self.decoder_inst = self.add_inst("decoder", self.decoder)
        decode = [f"decode_{i}" for i in reversed(range(16))]
        wordlines = [f"wl_{i}" for i in reversed(range(16))]
        self.connect_inst(inputs + decode + ["vdd", "gnd"])
        self.driver_inst = self.add_inst("driver", self.driver)
        self.connect_inst(decode + wordlines + ["vdd", "gnd"])
        self.memory_inst = self.add_inst("memory", self.memory)
        self.connect_inst(list(self.memory.pins))
        if not OPTS.netlist_only:
            self.create_layout()

    def create_layout(self):
        # A 1.2 um left channel keeps new power via stacks outside the
        # foundry decoder's tightly packed M2/M3 routing.
        self.decoder_inst.place((1.2, 33.6))
        self.driver_inst.place((29.76, 33.6))
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
        for pin in list(self.memory.pins)[16:]:
            self.copy_layout_pin(self.memory_inst, pin)
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
        self.add_boundary()
