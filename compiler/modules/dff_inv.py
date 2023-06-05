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
from openram import OPTS


class dff_inv(design):
    """
    This is a simple DFF with an inverted output. Some DFFs
    do not have Qbar, so this will create it.
    """
    unique_id = 1

    def __init__(self, inv_size=2, name=""):

        if name=="":
            name = "dff_inv_{0}".format(dff_inv.unique_id)
            dff_inv.unique_id += 1
        super().__init__(name)
        debug.info(1, "Creating {}".format(self.name))
        self.add_comment("inv: {0}".format(inv_size))

        self.inv_size = inv_size

        # This is specifically for SCMOS where the DFF vdd/gnd rails are more than min width.
        # This causes a DRC in the pinv which assumes min width rails. This ensures the output
        # contact does not violate spacing to the rail in the NMOS.
        debug.check(inv_size>=2, "Inverter must be greater than two for rail spacing DRC rules.")

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_modules()

    def create_layout(self):
        self.width = self.dff.width + self.inv1.width
        self.height = self.dff.height

        self.place_modules()
        self.add_wires()
        self.add_layout_pins()

        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        self.add_pin("D")
        self.add_pin("Q")
        self.add_pin("Qb")
        self.add_pin("clk")
        self.add_pin("vdd")
        self.add_pin("gnd")

    def add_modules(self):
        self.dff = dff_inv.dff_inv(self.inv_size)

        self.inv1 = factory.create(module_type="pinv",
                                   size=self.inv_size,
                                   height=self.dff.height)

    def create_modules(self):
        self.dff_inst=self.add_inst(name="dff_inv_dff",
                                    mod=self.dff)
        self.connect_inst(["D", "Q", "clk", "vdd", "gnd"])

        self.inv1_inst=self.add_inst(name="dff_inv_inv1",
                                     mod=self.inv1)
        self.connect_inst(["Q", "Qb",  "vdd", "gnd"])

    def place_modules(self):
        # Place the DFF
        self.dff_inst.place(vector(0,0))

        # Place the INV1 to the right
        self.inv1_inst.place(vector(self.dff_inst.rx(),0))


    def add_wires(self):
        # Route dff q to inv1 a
        q_pin = self.dff_inst.get_pin("Q")
        a1_pin = self.inv1_inst.get_pin("A")
        mid_x_offset = 0.5*(a1_pin.cx() + q_pin.cx())
        mid1 = vector(mid_x_offset, q_pin.cy())
        mid2 = vector(mid_x_offset, a1_pin.cy())
        self.add_path("m3",
                      [q_pin.center(), mid1, mid2, a1_pin.center()])
        self.add_via_center(layers=self.m2_stack,
                            offset=q_pin.center())
        self.add_via_center(layers=self.m2_stack,
                            offset=a1_pin.center())
        self.add_via_center(layers=self.m1_stack,
                            offset=a1_pin.center())


    def add_layout_pins(self):

        # Continous vdd rail along with label.
        vdd_pin=self.dff_inst.get_pin("vdd")
        self.add_layout_pin(text="vdd",
                            layer="m1",
                            offset=vdd_pin.ll(),
                            width=self.width,
                            height=vdd_pin.height())

        # Continous gnd rail along with label.
        gnd_pin=self.dff_inst.get_pin("gnd")
        self.add_layout_pin(text="gnd",
                            layer="m1",
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

        dout_pin = self.dff_inst.get_pin("Q")
        self.add_layout_pin_rect_center(text="Q",
                                        layer=dout_pin.layer,
                                        offset=dout_pin.center())

        dout_pin = self.inv1_inst.get_pin("Z")
        self.add_layout_pin_rect_center(text="Qb",
                                        layer="m2",
                                        offset=dout_pin.center())
        self.add_via_center(layers=self.m1_stack,
                            offset=dout_pin.center())
