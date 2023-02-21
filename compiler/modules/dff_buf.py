# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer
from openram import OPTS


class dff_buf(design):
    """
    This is a simple buffered DFF. The output is buffered
    with two inverters, of variable size, to provide q
    and qbar. This is to enable driving large fanout loads.
    """
    unique_id = 1

    def __init__(self, inv1_size=2, inv2_size=4, name=""):
        if name=="":
            name = "dff_buf_{0}".format(dff_buf.unique_id)
            dff_buf.unique_id += 1
        super().__init__(name)
        debug.info(1, "Creating {}".format(self.name))
        self.add_comment("inv1: {0} inv2: {1}".format(inv1_size, inv2_size))

        # This is specifically for SCMOS where the DFF vdd/gnd rails are more than min width.
        # This causes a DRC in the pinv which assumes min width rails. This ensures the output
        # contact does not violate spacing to the rail in the NMOS.
        debug.check(inv1_size>=2, "Inverter must be greater than two for rail spacing DRC rules.")
        debug.check(inv2_size>=2, "Inverter must be greater than two for rail spacing DRC rules.")

        self.inv1_size=inv1_size
        self.inv2_size=inv2_size

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()

    def create_layout(self):
        self.place_instances()
        self.width = self.inv2_inst.rx()
        self.height = self.dff.height
        self.route_wires()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_modules(self):
        self.dff = factory.create(module_type="dff")

        self.inv1 = factory.create(module_type="pinv",
                                   size=self.inv1_size,
                                   height=self.dff.height)

        self.inv2 = factory.create(module_type="pinv",
                                   size=self.inv2_size,
                                   height=self.dff.height)

    def add_pins(self):
        self.add_pin_list(["D", "Q", "Qb", "clk", "vdd", "gnd"],
                          ["INPUT", "OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"])

    def create_instances(self):
        self.dff_inst=self.add_inst(name="dff_buf_dff",
                                    mod=self.dff)

        self.connect_inst(["D", "qint", "clk", "vdd", "gnd"])

        self.inv1_inst=self.add_inst(name="dff_buf_inv1",
                                     mod=self.inv1)
        self.connect_inst(["qint", "Qb", "vdd", "gnd"])

        self.inv2_inst=self.add_inst(name="dff_buf_inv2",
                                     mod=self.inv2)
        self.connect_inst(["Qb", "Q", "vdd", "gnd"])

    def place_instances(self):
        # Add the DFF
        self.dff_inst.place(vector(0, 0))

        # Add INV1 to the right
        # The INV needs well spacing because the DFF is likely from a library
        # with different well construction rules
        well_spacing = 0
        try:
            well_spacing = max(well_spacing, self.nwell_space)
        except AttributeError:
            pass
        try:
            well_spacing = max(well_spacing, self.pwell_space)
        except AttributeError:
            pass
        try:
            well_spacing = max(well_spacing, self.pwell_to_nwell)
        except AttributeError:
            pass

        well_spacing += 2 * self.well_extend_active

        self.inv1_inst.place(vector(self.dff_inst.rx() + well_spacing, 0))

        # Add INV2 to the right
        self.inv2_inst.place(vector(self.inv1_inst.rx(), 0))

    def route_wires(self):
        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"

        # Route dff q to inv1 a
        q_pin = self.dff_inst.get_pin("Q")
        a1_pin = self.inv1_inst.get_pin("A")
        mid1 = vector(a1_pin.cx(), q_pin.cy())
        self.add_path(q_pin.layer, [q_pin.center(), mid1, a1_pin.center()], width=q_pin.height())
        self.add_via_stack_center(from_layer=a1_pin.layer,
                                  to_layer=q_pin.layer,
                                  offset=a1_pin.center())

        # Route inv1 z to inv2 a
        z1_pin = self.inv1_inst.get_pin("Z")
        a2_pin = self.inv2_inst.get_pin("A")
        self.mid_qb_pos = vector(0.5 * (z1_pin.cx() + a2_pin.cx()), z1_pin.cy())
        self.add_zjog(z1_pin.layer, z1_pin.center(), a2_pin.center())

    def add_layout_pins(self):

        # Continous vdd rail along with label.
        vdd_pin=self.dff_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer=vdd_pin.layer,
                            offset=vdd_pin.ll(),
                            width=self.width,
                            height=vdd_pin.height())

        # Continous gnd rail along with label.
        gnd_pin=self.dff_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer=gnd_pin.layer,
                            offset=gnd_pin.ll(),
                            width=self.width,
                            height=vdd_pin.height())

        clk_pin = self.dff_inst.get_pin("clk")
        self.add_layout_pin(text="clk",
                            layer=clk_pin.layer,
                            offset=clk_pin.ll(),
                            width=clk_pin.width(),
                            height=clk_pin.height())

        din_pin = self.dff_inst.get_pin("D")
        self.add_layout_pin(text="D",
                            layer=din_pin.layer,
                            offset=din_pin.ll(),
                            width=din_pin.width(),
                            height=din_pin.height())

        dout_pin = self.inv2_inst.get_pin("Z")
        mid_pos = dout_pin.center() + vector(self.m2_nonpref_pitch, 0)
        q_pos = mid_pos - vector(0, 2 * self.m2_nonpref_pitch)
        self.add_layout_pin_rect_center(text="Q",
                                        layer="m2",
                                        offset=q_pos)
        self.add_path(self.route_layer, [dout_pin.center(), mid_pos, q_pos])
        self.add_via_stack_center(from_layer=dout_pin.layer,
                                  to_layer="m2",
                                  offset=q_pos)

        qb_pos = self.mid_qb_pos + vector(0, 2 * self.m2_nonpref_pitch)
        self.add_layout_pin_rect_center(text="Qb",
                                        layer="m2",
                                        offset=qb_pos)
        self.add_path(self.route_layer, [self.mid_qb_pos, qb_pos])
        a2_pin = self.inv2_inst.get_pin("A")
        self.add_via_stack_center(from_layer=a2_pin.layer,
                                  to_layer="m2",
                                  offset=qb_pos)
