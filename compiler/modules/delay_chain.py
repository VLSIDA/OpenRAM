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


class delay_chain(design):
    """
    Generate a delay chain with the given number of stages and fanout.
    Input is a list contains the electrical effort (fanout) of each stage.
    Usually, this will be constant, but it could have varied fanout.
    """

    def __init__(self, name, fanout_list):
        """init function"""
        super().__init__(name)
        debug.info(1, "creating delay chain {0}".format(str(fanout_list)))
        self.add_comment("fanouts: {0}".format(str(fanout_list)))

        # Two fanouts are needed so that we can route the vdd/gnd connections
        for f in fanout_list:
            debug.check(f>=2, "Must have >=2 fanouts for each stage.")

        # number of inverters including any fanout loads.
        self.fanout_list = fanout_list
        self.rows = len(self.fanout_list)

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_inverters()

    def create_layout(self):
        # Each stage is a a row
        self.height = self.rows * self.inv.height
        # The width is determined by the largest fanout plus the driver
        self.width = (max(self.fanout_list) + 1) * self.inv.width

        self.place_inverters()
        self.route_inverters()
        self.route_supplies()
        self.add_layout_pins()
        self.add_boundary()
        self.DRC_LVS()

    def add_pins(self):
        """ Add the pins of the delay chain"""
        self.add_pin("in", "INPUT")
        self.add_pin("out", "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):

        self.dff = factory.create(module_type="dff_buf")
        dff_height = self.dff.height

        self.inv = factory.create(module_type="pinv",
                                  height=dff_height)

    def create_inverters(self):
        """ Create the inverters and connect them based on the stage list """
        self.driver_inst_list = []
        self.load_inst_map = {}
        for stage_num, fanout_size in zip(range(self.rows), self.fanout_list):
            # Add the inverter
            cur_driver=self.add_inst(name="dinv{}".format(stage_num),
                                     mod=self.inv)
            # keep track of the inverter instances so we can use them to get the pins
            self.driver_inst_list.append(cur_driver)

            # Hook up the driver
            if stage_num + 1 == self.rows:
                stageout_name = "out"
            else:
                stageout_name = "dout_{}".format(stage_num + 1)
            if stage_num == 0:
                stagein_name = "in"
            else:
                stagein_name = "dout_{}".format(stage_num)
            self.connect_inst([stagein_name, stageout_name, "vdd", "gnd"])

            # Now add the dummy loads to the right
            self.load_inst_map[cur_driver]=[]
            for i in range(fanout_size):
                cur_load=self.add_inst(name="dload_{0}_{1}".format(stage_num, i),
                                      mod=self.inv)
                # Fanout stage is always driven by driver and output is disconnected
                disconnect_name = "n_{0}_{1}".format(stage_num, i)
                self.connect_inst([stageout_name, disconnect_name, "vdd", "gnd"])

                # Keep track of all the loads to connect their inputs as a load
                self.load_inst_map[cur_driver].append(cur_load)

    def place_inverters(self):
        """ Place the inverters and connect them based on the stage list """
        for stage_num, fanout_size in zip(range(self.rows), self.fanout_list):
            if stage_num % 2:
                inv_mirror = "MX"
                inv_offset = vector(0, (stage_num + 1) * self.inv.height)
            else:
                inv_mirror = "R0"
                inv_offset = vector(0, stage_num * self.inv.height)

            # Add the inverter
            cur_driver=self.driver_inst_list[stage_num]
            cur_driver.place(offset=inv_offset,
                             mirror=inv_mirror)

            # Now add the dummy loads to the right
            load_list = self.load_inst_map[cur_driver]
            for i in range(fanout_size):
                inv_offset += vector(self.inv.width, 0)
                load_list[i].place(offset=inv_offset,
                                   mirror=inv_mirror)

    def add_route(self, pin1, pin2):
        """ This guarantees that we route from the top to bottom row correctly. """
        pin1_pos = pin1.center()
        pin2_pos = pin2.center()
        if pin1_pos.y == pin2_pos.y:
            self.add_path("m2", [pin1_pos, pin2_pos])
        else:
            mid_point = vector(pin2_pos.x, 0.5 * (pin1_pos.y + pin2_pos.y))
            # Written this way to guarantee it goes right first if we are switching rows
            self.add_path("m2", [pin1_pos, vector(pin1_pos.x, mid_point.y), mid_point, vector(mid_point.x, pin2_pos.y), pin2_pos])

    def route_inverters(self):
        """ Add metal routing for each of the fanout stages """

        for i in range(len(self.driver_inst_list)):
            inv = self.driver_inst_list[i]
            for load in self.load_inst_map[inv]:
                # Drop a via on each A pin
                a_pin = load.get_pin("A")
                self.add_via_stack_center(from_layer=a_pin.layer,
                                          to_layer="m3",
                                          offset=a_pin.center())

            # Route an M3 horizontal wire to the furthest
            z_pin = inv.get_pin("Z")
            a_pin = inv.get_pin("A")
            a_max = self.load_inst_map[inv][-1].get_pin("A")
            self.add_via_stack_center(from_layer=a_pin.layer,
                                      to_layer="m2",
                                      offset=a_pin.center())
            self.add_via_stack_center(from_layer=z_pin.layer,
                                      to_layer="m3",
                                      offset=z_pin.center())
            self.add_path("m3", [z_pin.center(), a_max.center()])

            # Route Z to the A of the next stage
            if i + 1 < len(self.driver_inst_list):
                z_pin = inv.get_pin("Z")
                next_inv = self.driver_inst_list[i + 1]
                next_a_pin = next_inv.get_pin("A")
                y_mid = (z_pin.cy() + next_a_pin.cy()) / 2
                mid1_point = vector(z_pin.cx(), y_mid)
                mid2_point = vector(next_a_pin.cx(), y_mid)
                self.add_path("m2", [z_pin.center(), mid1_point, mid2_point, next_a_pin.center()])

    def route_supplies(self):
        # These pins get routed in one cell from the left/right
        # because the input signal gets routed on M3 and can interfere with the delay input.
        self.route_vertical_pins("vdd", self.driver_inst_list, xside="rx")
        right_load_insts = [self.load_inst_map[x][-1] for x in self.driver_inst_list]
        self.route_vertical_pins("gnd", right_load_insts, xside="lx")

    def add_layout_pins(self):

        # input is A pin of first inverter
        # It gets routed to the left a bit to prevent pin access errors
        # due to the output pin when going up to M3
        a_pin = self.driver_inst_list[0].get_pin("A")
        mid_loc = vector(a_pin.cx() - self.m3_pitch, a_pin.cy())
        self.add_via_stack_center(from_layer=a_pin.layer,
                                        to_layer="m2",
                                        offset=mid_loc)
        self.add_path(a_pin.layer, [a_pin.center(), mid_loc])

        self.add_layout_pin_rect_center(text="in",
                                        layer="m2",
                                        offset=mid_loc)

        # output is A pin of last load/fanout inverter
        last_driver_inst = self.driver_inst_list[-1]
        a_pin = self.load_inst_map[last_driver_inst][-1].get_pin("A")
        self.add_via_stack_center(from_layer=a_pin.layer,
                                  to_layer="m1",
                                  offset=a_pin.center())
        self.add_layout_pin_rect_center(text="out",
                                        layer="m1",
                                        offset=a_pin.center())
