# See LICENSE for licensing information.
#
# Copyright (c) 2016-2022 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design, drc
from openram.base import vector
from openram.sram_factory import factory
from openram.tech import layer
from openram.tech import layer_properties as layer_props
from openram import OPTS


class rom_wordline_driver_array(design):
    """
    Creates a Wordline Buffer/Inverter array
    """

    def __init__(self, name, rows, cols):
        design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("rows: {0} cols: {1}".format(rows, cols))

        self.rows = rows
        self.cols = cols

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_drivers()

    def create_layout(self):
        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"
        self.place_drivers()
        self.route_layout()
        self.route_supplies()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.rows):
            self.add_pin("in_{0}".format(i), "INPUT")
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("out_{0}".format(i), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        b = factory.create(module_type="rom_base_cell")

        self.wl_driver = factory.create(module_type="pbuf_dec",
                                        size=self.cols,
                                        height=b.height,
                                        add_wells=False)

    def route_supplies(self):
        """
        Add a pin for each row of vdd/gnd which
        are must-connects next level up.
        """
        if layer_props.wordline_driver.vertical_supply:
            self.route_vertical_pins("vdd", self.wld_inst)
            self.route_vertical_pins("gnd", self.wld_inst)
        else:
            self.route_vertical_pins("vdd", self.wld_inst, xside="rx",)
            self.route_vertical_pins("gnd", self.wld_inst, xside="lx",)

    def create_drivers(self):
        self.wld_inst = []
        for row in range(self.rows):
            self.wld_inst.append(self.add_inst(name="wld{0}".format(row),
                                               mod=self.wl_driver))
            self.connect_inst(["in_{0}".format(row),
                               "out_{0}".format(row),
                               "vdd", "gnd"])

    def place_drivers(self):

        for row in range(self.rows):
            # These are flipped since we always start with an RBL on the bottom
            y_offset = self.wl_driver.height * row

            offset = [0, y_offset]

            self.wld_inst[row].place(offset=offset)

        self.width = self.wl_driver.width
        self.height = self.wl_driver.height * self.rows

    def route_layout(self):
        """ Route all of the signals """
        route_width = drc["minwidth_{}".format(self.route_layer)]
        for row in range(self.rows):
            inst = self.wld_inst[row]

            self.copy_layout_pin(inst, "A", "in_{0}".format(row))

            # output each WL on the right
            wl_offset = inst.get_pin("Z").rc() - vector( 0.5 * route_width, 0)

            end = vector(wl_offset.x, \
                         self.get_pin("in_{}".format(row)).cy() + 0.5 * route_width)
            self.add_segment_center(layer=self.route_layer,
                                               start=wl_offset,
                                               end=end)

            self.add_layout_pin_rect_center(text="out_{}".format(row), layer=self.route_layer, offset=end - vector(0, 0.5 * route_width))
