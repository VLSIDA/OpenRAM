# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from tech import drc, layer
from vector import vector
from sram_factory import factory
from globals import OPTS
from tech import layer_properties as layer_props


class wordline_driver_array(design.design):
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
        self.offset_x_coordinates()
        self.add_boundary()
        self.route_vdd_gnd()
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

    def route_vdd_gnd(self):
        """
        Add vertical power rails.
        """
        if layer_props.wordline_driver.vertical_supply:
            self.route_vertical_pins("vdd", insts=self.wld_inst)
            self.route_vertical_pins("gnd", insts=self.wld_inst)
        else:
            self.route_vertical_pins("vdd", insts=self.wld_inst, side="left")
            self.route_vertical_pins("gnd", insts=self.wld_inst, side="right")

            # Widen the rails to cover any gap
            for num in range(self.rows):
                for name in ["vdd", "gnd"]:
                    supply_pin = self.wld_inst[num].get_pin(name)
                    self.add_segment_center(layer=supply_pin.layer,
                                            start=vector(0, supply_pin.cy()),
                                            end=vector(self.width, supply_pin.cy()))


    def create_drivers(self):
        self.wld_inst = []
        for row in range(self.rows):
            name_and = "wl_driver_and{}".format(row)

            # add and2
            self.wld_inst.append(self.add_inst(name=name_and,
                                                mod=self.wl_driver))
            self.connect_inst(["en",
                               "in_{0}".format(row),
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

        # Leave a well gap to separate the bitcell array well from this well
        well_gap = 2 * drc("pwell_to_nwell") + drc("nwell_enclose_active")
        self.width = self.wl_driver.width + well_gap
        self.height = self.wl_driver.height * self.rows

    def route_layout(self):
        """ Route all of the signals """

        # Wordline enable connection
        en_pin = self.wld_inst[0].get_pin("A")
        en_bottom_pos = vector(en_pin.cx(), 0)
        en_top_pos = vector(en_pin.cx(), self.height)
        en_pin = self.add_layout_pin_segment_center(text="en",
                                                    layer="m2",
                                                    start=en_bottom_pos,
                                                    end=en_top_pos) 

        for row in range(self.rows):
            and_inst = self.wld_inst[row]

            # Drop a via
            b_pin = and_inst.get_pin("A")
            self.add_via_stack_center(from_layer=b_pin.layer,
                                      to_layer="m2",
                                      offset=b_pin.center())

            # connect the decoder input pin to and2 A
            self.copy_layout_pin(and_inst, "B", "in_{0}".format(row))

            # output each WL on the right
            wl_offset = and_inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="wl_{0}".format(row),
                                               layer=self.route_layer,
                                               start=wl_offset,
                                               end=wl_offset - vector(self.m1_width, 0))
