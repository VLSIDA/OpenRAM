"""Raw foundry cycle controller, not an external synchronous SRAM interface.

The caller captures requests and supplies the inverted external clock.  The
source delay loads and all transistor geometries stay in the hard cells; this
assembly makes no full-array timing or PVT guarantee.
"""

from openram import OPTS
from openram.base import design, vector
from openram.sram_factory import factory


class ihp_control_logic(design):
    def __init__(self, name):
        super().__init__(name)
        for pin in ("clk", "cs", "re", "we"):
            self.add_pin(pin, "INPUT")
        for pin in ("row_cs", "eclk", "pre_n", "sae", "wclk"):
            self.add_pin(pin, "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        self.controller = self.add_inst(
            "controller", factory.create(module_type="ihp_control_cell", kind="controller"))
        self.connect_inst([
            "aclk_n_unused", "gnd", "gnd", "gnd", "gnd", "gnd",
            "tie_low_unused", "clk", "cs", "dclk_unused", "eclk",
            "pulse_h", "pulse_l", "pulse", "rclk", "re", "row_cs", "wclk",
            "we", "vdd", "gnd"])
        self.delay_high = self.add_inst(
            "delay_high", factory.create(module_type="ihp_control_cell", kind="delay_high"))
        self.connect_inst(["pulse", "pulse_h", "vdd", "gnd"])
        self.delay_mux = self.add_inst(
            "delay_mux", factory.create(module_type="ihp_control_cell", kind="delay_mux"))
        self.connect_inst(["pulse_h", "vdd", "pulse_l", "vdd", "gnd"])
        self.pre_nor = self.add_inst(
            "pre_nor", factory.create(module_type="ihp_control_cell", kind="nor2"))
        self.connect_inst(["rclk", "wclk", "pre_b", "vdd", "gnd"])
        self.pre_inv = self.add_inst(
            "pre_inv", factory.create(module_type="ihp_control_cell", kind="inv"))
        self.connect_inst(["pre_b", "pre_n", "vdd", "gnd"])
        self.sae_inv = self.add_inst(
            "sae_inv", factory.create(module_type="ihp_control_cell", kind="inv"))
        self.connect_inst(["rclk", "sae", "vdd", "gnd"])
        if not OPTS.netlist_only:
            self.create_layout()

    def signal_via(self, point, lower, upper):
        # Foundry signal access is 0.26 wide (0.035 enclosure of a 0.19
        # cut).  Generic OpenRAM min-area contacts are too wide here.  Tall
        # landing pads meet 0.144 um^2 without widening adjacent pin tracks.
        point = vector(point)
        metals = ("m1", "m2", "m3", "m4", "m5")
        first, last = metals.index(lower), metals.index(upper)
        for index in range(first, last):
            self.add_rect(f"via{index + 1}", point - vector(.095, .095),
                          width=.19, height=.19)
        for index in range(max(1, first), last + 1):
            self.add_rect(metals[index], point - vector(.13, .28),
                          width=.26, height=.56)

    def create_layout(self):
        self.controller.place((0, 0))
        self.delay_high.place((0, 27))
        self.delay_mux.place((23, 27))
        self.pre_nor.place((33, 32.025), mirror="MX")
        self.pre_inv.place((35.55, 32.025), mirror="MX")
        self.sae_inv.place((37.59, 32.025), mirror="MX")
        self.width = self.controller.mod.width
        self.height = 27 + self.delay_mux.mod.height

        for pin in ("clk", "cs", "re", "we", "row_cs", "eclk", "wclk", "vdd", "gnd"):
            self.copy_layout_pin(self.controller, pin)
        self.copy_layout_pin(self.pre_inv, "z", "pre_n")
        self.copy_layout_pin(self.sae_inv, "z", "sae")

        # Ground BIST at the bottom access ends, below the source M3 rails.
        self.add_path("m3", [(12.5, .355), (19.79, .355)], width=.26)
        for pin in ("bist_clk", "bist_cs", "bist_en", "bist_re", "bist_we"):
            self.add_via_stack_center((self.controller.get_pin(pin).cx(), .355),
                                      "m2", "m3", min_area=True)
        self.add_via_stack_center((12.5, .355), "m3", "m4", min_area=True)

        # Source M4 straps alternate ground and supply.  Rise from matching
        # straps on M5; the two new M4 rails feed the upper hard-cell row.
        for x, y in ((7.5, 27.525), (1.5, 31.725)):
            self.add_via_stack_center((x, 25), "m4", "m5", min_area=True)
            self.add_path("m5", [(x, 25), (x, y)], width=.6)
            self.add_via_stack_center((x, y), "m4", "m5", min_area=True)
            self.add_path("m4", [(1.3, y), (39.2, y)], width=.6)
            for feed_x in (1.3, 29.4, 35.2, 36.8, 39.2):
                self.add_via_stack_center((feed_x, y), "m1", "m4", min_area=True)

        # Select the high-delay feedback path.  Do not add metal across the
        # mux's internally strapped supply rails or its intervening signals.
        select = vector(26.98, 33.84)
        self.signal_via(select, "m2", "m3")
        self.add_path("m3", [select, (select.x, 35.925)], width=.26)
        self.add_via_stack_center((select.x, 35.925), "m1", "m3", min_area=True)

        # Access the controller on its own M3 nets, in gaps between its M4
        # power straps.  Pulse_l first escapes sideways to a different gap.
        self.signal_via((10, 11.235), "m3", "m5")
        self.signal_via((31.38, 9.55), "m2", "m5")
        self.signal_via((31.875, 9.55), "m2", "m3")
        self.add_path("m3", [(31.875, 9.55), (35.5, 9.55)], width=.26)
        self.signal_via((35.5, 9.55), "m3", "m5")
        self.signal_via((30.5, 7.035), "m3", "m5")
        self.signal_via((25.5, 6.195), "m3", "m5")

        # M5 trunks cross the foundry power grid without disturbing it.
        for x, bottom, top in ((10, 11.235, 29.7), (31.38, 9.55, 34.4),
                               (35.5, 9.55, 28.6), (30.5, 7.035, 33.3),
                               (25.5, 6.195, 32.6)):
            self.add_path("m5", [(x, bottom), (x, top)], width=.3)

        a = vector(.765, 29.7)
        self.signal_via(a, "m1", "m3")
        self.add_path("m3", [a, (10, a.y)], width=.26)
        self.signal_via((10, 29.7), "m3", "m5")
        # Pulse_h crosses pulse_l and the mux select on M4, not M3.
        z = self.delay_high.get_pin("z").center()
        self.signal_via(z, "m1", "m4")
        self.add_path("m4", [z, (z.x, 30.5), (31.38, 30.5)], width=.26)
        self.signal_via((31.38, 30.5), "m4", "m5")
        a = vector(24.94, 34.05)
        self.signal_via(a, "m2", "m4")
        self.add_path("m4", [a, (a.x, 34.4), (31.38, 34.4)], width=.26)
        self.signal_via((31.38, 34.4), "m4", "m5")
        z = vector(24.77, 30.9)
        self.signal_via(z, "m1", "m3")
        self.add_path("m3", [z, (z.x, 28.6), (35.5, 28.6)], width=.26)
        self.signal_via((35.5, 28.6), "m3", "m5")

        # RCLK drives NOR and SAE inversion.  Use M2 for the short NOR
        # input drop so that it crosses the independent WCLK M3 track.
        a = self.pre_nor.get_pin("a").center()
        self.signal_via(a, "m1", "m2")
        self.add_path("m2", [a, (a.x, 33.3)], width=.26)
        self.signal_via((a.x, 33.3), "m2", "m3")
        a = self.sae_inv.get_pin("a").center()
        self.signal_via(a, "m1", "m3")
        self.add_path("m3", [a, (a.x, 33.3), (30.5, 33.3)], width=.26)
        self.signal_via((30.5, 33.3), "m3", "m5")
        b = self.pre_nor.get_pin("b").center()
        self.signal_via(b, "m1", "m3")
        self.add_path("m3", [b, (b.x, 32.6), (25.5, 32.6)], width=.26)
        self.signal_via((25.5, 32.6), "m3", "m5")
        z = self.pre_nor.get_pin("z").center()
        a = self.pre_inv.get_pin("a").center()
        self.signal_via(z, "m1", "m3")
        self.signal_via(a, "m1", "m3")
        self.add_path("m3", [z, (a.x, z.y), a], width=.26)
        self.add_boundary()
