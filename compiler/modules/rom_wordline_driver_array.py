# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
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

    def __init__(self, name, rows, fanout, invert_outputs=False, tap_spacing=4, flip_io=False):
        design.__init__(self, name)
        debug.info(1, "Creating {0}".format(self.name))
        self.add_comment("rows: {0} Buffer size of: {1}".format(rows, fanout))

        self.rows = rows
        self.fanout = fanout
        self.invert_outputs=invert_outputs
        self.tap_spacing = tap_spacing
        self.flip_io = flip_io
        if OPTS.tech_name == "sky130":
            self.supply_layer = "m1"
        else:
            self.supply_layer = "m2"

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
        if self.tap_spacing != 0:
            self.place_taps()
        self.add_boundary()

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
        self.tap = factory.create(module_type="rom_poly_tap", add_tap = True)

        if self.invert_outputs:
            self.wl_driver = factory.create(module_type="pinv_dec",
                                            size=self.fanout,
                                            height=b.height,
                                            add_wells=False,
                                            flip_io=self.flip_io)
                
        else:
            self.wl_driver = factory.create(module_type="pbuf_dec",
                                            size=self.fanout,
                                            height=b.height,
                                            add_wells=False)

    def route_supplies(self):
        """
        Add a pin for each row of vdd/gnd which
        are must-connects next level up.
        """

        if layer_props.wordline_driver.vertical_supply:
            # self.route_vertical_pins("vdd", self.wld_inst)
            # self.route_vertical_pins("gnd", self.wld_inst)
            self.route_vertical_pins("vdd", [self], layer=self.supply_layer)
            self.route_vertical_pins("gnd", [self], layer=self.supply_layer)
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
        y_offset = 0
        for row in range(self.rows):
            if self.tap_spacing != 0 and row % self.tap_spacing == 0:
                y_offset += self.tap.pitch_offset
            offset = [0, y_offset]

            self.wld_inst[row].place(offset=offset)
            y_offset += self.wld_inst[row].height

        self.width = self.wl_driver.width
        self.height = self.wl_driver.height * self.rows

    def route_layout(self):
        """ Route all of the signals """
        route_width = drc["minwidth_{}".format(self.route_layer)]
        for row in range(self.rows):
            if self.flip_io:
                row_num = self.rows - row - 1
            else:
                row_num = row
            inst = self.wld_inst[row_num]
            self.copy_layout_pin(inst, "vdd")
            self.copy_layout_pin(inst, "gnd")

            self.copy_layout_pin(inst, "A", "in_{0}".format(row))

            out_pin = inst.get_pin("Z")
            # output each WL on the right
            if self.flip_io:
                wl_offset = out_pin.lc() - vector(1.6 * route_width, 0)
                
            else:
                wl_offset = out_pin.rc() - vector( 0.5 * route_width, 0)

            end = vector(wl_offset.x, \
                         self.get_pin("in_{}".format(row)).cy() + 0.5 * route_width)
            self.add_segment_center(layer=self.route_layer,
                                               start=wl_offset,
                                               end=end)
            if self.flip_io:
                self.add_segment_center(layer=self.route_layer,
                                        start=out_pin.lc(),
                                        end=vector(wl_offset.x - 0.5 * route_width, out_pin.cy()))

            self.add_layout_pin_rect_center(text="out_{}".format(row), layer=self.route_layer, offset=end - vector(0, 0.5 * route_width))

    def place_taps(self):

        for wl in range(0 , self.rows, self.tap_spacing):
            driver = self.wld_inst[wl]

            source_pin1 = driver.get_pins("vdd")[0]
            gnd_pin1 = driver.get_pins("gnd")[0]

            left_edge = driver.get_pin("Z").cy() - 0.5 * self.contact_width - self.active_enclose_contact - self.active_space - 0.5 * self.active_contact.width

            contact_pos = vector(source_pin1.cx(), left_edge)
            self.place_tap(contact_pos, "n")

            contact_pos = vector( gnd_pin1.cx(), left_edge)
            self.place_tap(contact_pos, "p")

            if not self.invert_outputs:
                source_pin2 = driver.get_pins("vdd")[1]
                gnd_pin2 = driver.get_pins("gnd")[1]
                contact_pos = vector(source_pin2.cx(), left_edge)
                self.place_tap(contact_pos, "n")

                contact_pos = vector( gnd_pin2.cx(), left_edge)
                self.place_tap(contact_pos, "p")

    def place_tap(self, offset, well_type):
        self.add_via_center(layers=self.active_stack,
                    offset=offset,
                    implant_type=well_type,
                    well_type=well_type,
                    directions="nonpref")
        self.add_via_stack_center(offset=offset,
                                from_layer=self.active_stack[2],
                                to_layer=self.supply_layer)
        if well_type == "p":
            pin = "gnd"
        else:
            pin = "vdd"
        self.add_layout_pin_rect_center(text=pin, layer=self.supply_layer, offset=offset)