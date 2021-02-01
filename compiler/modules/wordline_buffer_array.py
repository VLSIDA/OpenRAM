# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from tech import layer
from vector import vector
from sram_factory import factory
from globals import OPTS
from tech import layer_properties as layer_props


class wordline_buffer_array(design.design):
    """
    Creates a Wordline Buffer/Inverter array
    """

    def __init__(self, name, rows, cols):
        design.design.__init__(self, name)
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
        self.route_vdd_gnd()
        self.offset_all_coordinates()
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
        b = factory.create(module_type=OPTS.bitcell)

        self.wl_driver = factory.create(module_type="inv_dec",
                                        size=self.cols,
                                        height=b.height)
        self.add_mod(self.wl_driver)

    def route_vdd_gnd(self):
        """
        Add a pin for each row of vdd/gnd which
        are must-connects next level up.
        """
        if layer_props.wordline_driver.vertical_supply:
            for name in ["vdd", "gnd"]:
                supply_pins = self.wld_inst[0].get_pins(name)
                for pin in supply_pins:
                    self.add_layout_pin_segment_center(text=name,
                                                       layer=pin.layer,
                                                       start=pin.bc(),
                                                       end=vector(pin.cx(), self.height))
        else:
            # Find the x offsets for where the vias/pins should be placed
            xoffset_list = [self.wld_inst[0].rx()]
            for num in range(self.rows):
                # this will result in duplicate polygons for rails, but who cares

                # use the inverter offset even though it will be the and's too
                (gate_offset, y_dir) = self.get_gate_offset(0,
                                                            self.wl_driver.height,
                                                            num)
                # Route both supplies
                for name in ["vdd", "gnd"]:
                    supply_pin = self.wld_inst[num].get_pin(name)

                    # Add pins in two locations
                    for xoffset in xoffset_list:
                        pin_pos = vector(xoffset, supply_pin.cy())
                        self.copy_power_pin(supply_pin, loc=pin_pos)

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
            if (row % 2):
                y_offset = self.wl_driver.height * row
                inst_mirror = "R0"
            else:
                y_offset = self.wl_driver.height * (row + 1)
                inst_mirror = "MX"

            offset = [0, y_offset]

            self.wld_inst[row].place(offset=offset,
                                     mirror=inst_mirror)

        self.width = self.wl_driver.width
        self.height = self.wl_driver.height * self.rows

    def route_layout(self):
        """ Route all of the signals """

        for row in range(self.rows):
            inst = self.wld_inst[row]

            self.copy_layout_pin(inst, "A", "in_{0}".format(row))

            # output each WL on the right
            wl_offset = inst.get_pin("Z").rc()
            self.add_layout_pin_segment_center(text="out_{0}".format(row),
                                               layer=self.route_layer,
                                               start=wl_offset,
                                               end=wl_offset - vector(self.m1_width, 0))
