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
from openram.tech import drc, layer
from openram.tech import layer_properties as layer_props
from openram import OPTS


class wordline_driver_array(design):
    """
    Creates a Wordline Driver
    Generates the wordline-driver to drive the bitcell
    """

    def __init__(self, name, rows, cols):
        super().__init__(name)
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
        self.offset_x_coordinates(vector(-2*self.m4_pitch, 0))

        # Leave a well gap to separate the bitcell array well from this well
        well_gap = 2 * drc("pwell_to_nwell") + drc("nwell_enclose_active")
        self.width = self.wld_inst[-1].rx() + well_gap
        self.height = self.wld_inst[-1].uy()

        self.add_boundary()
        self.route_supplies()
        self.DRC_LVS()

    def add_pins(self):
        # inputs to wordline_driver.
        for i in range(self.rows):
            self.add_pin("in_{0}".format(i), "INPUT")
        # Outputs from wordline_driver.
        for i in range(self.rows):
            self.add_pin("wl_{0}".format(i), "OUTPUT")
        self.add_pin("en", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):

        self.wl_driver = factory.create(module_type="wordline_driver",
                                        cols=self.cols)

    def route_supplies(self):
        """
        Add vertical power rails.
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
            name_and = "wl_driver_and{}".format(row)

            # add and2
            self.wld_inst.append(self.add_inst(name=name_and,
                                                mod=self.wl_driver))
            self.connect_inst(["in_{0}".format(row),
                               "en",
                               "wl_{0}".format(row),
                               "vdd", "gnd"])

    def place_drivers(self):

        for row in range(self.rows):
            if (row % 2):
                y_offset = self.wl_driver.height * (row + 1)
                inst_mirror = "MX"
            else:
                y_offset = self.wl_driver.height * row
                inst_mirror = "R0"

            and2_offset = [self.wl_driver.width, y_offset]

            # add and2
            self.wld_inst[row].place(offset=and2_offset,
                                     mirror=inst_mirror)

    def route_layout(self):
        """ Route all of the signals """

        # Wordline enable connection
        en_pin = self.wld_inst[0].get_pin("B")
        en_bottom_pos = vector(en_pin.cx(), 0)
        en_top_pos = vector(en_pin.cx(), self.wld_inst[-1].uy())
        en_pin = self.add_layout_pin_segment_center(text="en",
                                                    layer="m2",
                                                    start=en_bottom_pos,
                                                    end=en_top_pos)

        for row in range(self.rows):
            and_inst = self.wld_inst[row]

            # Drop a via
            b_pin = and_inst.get_pin("B")
            self.add_via_stack_center(from_layer=b_pin.layer,
                                      to_layer="m2",
                                      offset=b_pin.center())

            # connect the decoder input pin to and2 A
            self.copy_layout_pin(and_inst, "A", "in_{0}".format(row))

            # output each WL on the right
            wl_offset = and_inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="wl_{0}".format(row),
                                               layer=self.route_layer,
                                               start=wl_offset,
                                               end=wl_offset - vector(self.m1_width, 0))
