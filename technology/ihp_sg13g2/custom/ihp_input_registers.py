"""Rising-edge input capture using unchanged foundry negative-edge flops.

One shared clock inverter avoids one inverter per captured bit. The
single-bit form also supplies the positive-edge DFF characterization view.
"""

from openram import OPTS
from openram.base import design
from openram.sram_factory import factory


class ihp_input_registers(design):
    def __init__(self, name, bits=1):
        if bits < 1:
            raise ValueError("Input registers require at least one bit")
        super().__init__(name)
        self.bits = bits
        self.data_names = ["D"] if bits == 1 else [f"D_{i}" for i in range(bits)]
        self.output_names = ["Q"] if bits == 1 else [f"Q_{i}" for i in range(bits)]
        for pin in self.data_names:
            self.add_pin(pin, "INPUT")
        for pin in self.output_names:
            self.add_pin(pin, "OUTPUT")
        self.add_pin("clk", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        self.add_pin_names({})  # Composite pins already use the characterization names.
        self.inverter = factory.create(module_type="ihp_control_cell", kind="inv")
        self.flop = factory.create(module_type="ihp_control_cell", kind="dff")
        self.clock_inst = self.add_inst("clock_inverter", self.inverter)
        self.connect_inst(["clk", "clk_n", "vdd", "gnd"])
        self.flop_insts = []
        for bit in range(bits):
            self.flop_insts.append(self.add_inst(f"capture_{bit}", self.flop))
            self.connect_inst(["clk_n", self.data_names[bit], self.output_names[bit], "vdd", "gnd"])
        if not OPTS.netlist_only:
            self.create_layout()
        if bits == 1:
            # setup_hold includes a DFF's standalone SPICE file. This is a
            # generated composite, not a library file in the technology tree.
            self.sp_file = OPTS.openram_temp + self.cell_name + ".sp"
            self.sp_write(self.sp_file)

    def create_layout(self):
        # The source library has a 0.51 um overlap beyond its site pitch.
        # Aligning these one-row cells makes their M1 power rails abut.
        inv_pitch = self.inverter.width - .51
        flop_pitch = self.flop.width - .51
        self.clock_inst.place((0, 0))
        self.width = inv_pitch + self.bits * flop_pitch + .51
        self.height = self.flop.height + 1
        self.copy_layout_pin(self.clock_inst, "a", "clk")
        clock_pins = [self.clock_inst.get_pin("z")]
        for bit, inst in enumerate(self.flop_insts):
            inst.place((inv_pitch + bit * flop_pitch, 0))
            self.copy_layout_pin(inst, "d", self.data_names[bit])
            self.copy_layout_pin(inst, "q", self.output_names[bit])
            clock_pins.append(inst.get_pin("clk_n"))
        bus_y = self.flop.height + .5
        for index, pin in enumerate(clock_pins):
            # The inverter's narrow output is beside its input at mid-height.
            # Its upper extension has space for a legal via landing pad.
            point = (pin.cx(), pin.uy() - .3) if index == 0 else pin.center()
            self.add_via_stack_center(point, pin.layer, "m3", min_area=True)
            self.add_path("m3", [point, (pin.cx(), bus_y)], width=.3)
        self.add_path("m3", [(clock_pins[0].cx(), bus_y),
                             (clock_pins[-1].cx(), bus_y)], width=.3)
        for pin, y in (("gnd", 0), ("vdd", 4.2)):
            # One continuous rail per supply also supports generic callers
            # that require a single pin rather than an iterator of shapes.
            self.add_layout_pin(pin, "m1", (.51, y),
                                width=self.width - 1.02, height=.6)
        self.add_boundary()
