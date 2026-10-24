"""Unresized foundry control/interface cells from the SRAM macro hierarchy."""

from openram.base import design
from openram.drc.custom_cell_properties import cell


class ihp_control_cell(design):
    def __init__(self, name, kind):
        ports, outputs = {
            "controller": (
                "aclk_n bist_clk bist_cs bist_en bist_re bist_we tie_low clk cs dclk eclk pulse_h pulse_l pulse rclk re row_cs wclk we",
                "aclk_n tie_low dclk eclk pulse rclk row_cs wclk"),
            "delay_high": ("a z", "z"),
            "delay_mux": ("a sel z", "z"),
            "inv": ("a z", "z"),
            "and2": ("a b z", "z"),
            "nor2": ("a b z", "z"),
            "dff": ("clk_n d q", "q"),
        }[kind]
        pins = ports.split() + ["vdd", "gnd"]
        types = ["OUTPUT" if p in outputs.split() else "INPUT" for p in ports.split()]
        super().__init__(name, cell_name="ihp_" + kind,
                         prop=cell(pins, types + ["POWER", "GROUND"]))
