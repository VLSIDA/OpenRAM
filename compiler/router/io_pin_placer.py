# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram.base.vector3d import vector3d
from openram import OPTS
from .graph import graph
from .graph_shape import graph_shape
from .router import router
import re

class io_pin_placer(router):

    def __init__(self, layers, design, bbox=None):

        # `router` is the base router class
        router.__init__(self, layers, design, bbox)

        # New pins are the side supply pins
        self.new_pins = {}

        # added_io_pins
        self.io_pins_added_left = []
        self.io_pins_added_right = []
        self.io_pins_added_up = []
        self.io_pins_added_down = []

        # fake_pins, use for rename
        self.io_pins_fake =[]


    def get_closest_edge(self, point):
        """ Return a point's the closest edge and the edge's axis direction. """

        ll, ur = self.bbox

        # Snap the pin to the perimeter and break the iteration
        ll_diff_x = abs(point.x - ll.x)
        ll_diff_y = abs(point.y - ll.y)
        ur_diff_x = abs(point.x - ur.x)
        ur_diff_y = abs(point.y - ur.y)
        min_diff = min(ll_diff_x, ll_diff_y, ur_diff_x, ur_diff_y)

        if min_diff == ll_diff_x:
            return "left", True
        if min_diff == ll_diff_y:
            return "bottom", False
        if min_diff == ur_diff_x:
            return "right", True
        return "top", False


    def initial_position(self, pins): # pins is list []
        """ Set the IO pin center at the perimeter """
        pattern_clk = r'^clk'
        pattern_addr0 = r'^addr0'
        pattern_addr1 = r'^addr1'
        pattern_dout0 = r'^dout0'
        pattern_dout1 = r'^dout1'
        pattern_din = r'^din'
        pattern_wmask = r'^wmask'
        pattern_spare_wen = r'^spare_wen'
        pattern_web = r'^web'
        pattern_csb = r'^csb'
        for pin in pins:
            c = pin.center()
            # Find the closest edge
            edge, vertical = self.get_closest_edge(c)
            if re.match(pattern_clk, pin.name):# clk, should be placed at vertical edge
                if edge == "bottom" or edge == "left":#clk0
                    edge = "left"
                elif edge == "top" or edge == "right":#clk1
                    edge = "right"
                vertical = True
                self.store_position(pin, edge, vertical)
            if re.match(pattern_addr0, pin.name): # all the addr0[] should be placed at left edge
                if edge == "top" or edge == "left":
                    edge = "left"
                    vertical = True
                elif edge == "bottom": # but for big sram, addr0[] may have pins at bottom, which is allowed
                    vertical = False
                self.store_position(pin, edge, vertical)
            if re.match(pattern_addr1, pin.name): # all the addr1[] should be placed at right edge
                if edge == "bottom" or edge == "right":
                    edge = "right"
                    vertical = True
                elif edge == "top": # but for big sram, addr1[] may have pins at top, which is allowed
                    vertical = False
                self.store_position(pin, edge, vertical)
            if re.match(pattern_din, pin.name): # din
                self.store_position(pin, edge, vertical)
            if re.match(pattern_wmask, pin.name): # wmask
                self.store_position(pin, edge, vertical)
            if re.match(pattern_spare_wen, pin.name): # spare_wen
                self.store_position(pin, edge, vertical)
            if re.match(pattern_csb, pin.name):# csb
                self.store_position(pin, edge, vertical)
            if re.match(pattern_web, pin.name): # web
                self.store_position(pin, edge, vertical)
        # special handle the dout pins, if r/rw ports
        for pin in pins:
            if re.match(pattern_dout0, pin.name):
                edge = "bottom"
                vertical = False
                self.store_dout_position(pin, edge, vertical)
            if re.match(pattern_dout1, pin.name):
                edge = "top"
                vertical = False
                self.store_dout_position(pin, edge, vertical)


    def check_overlap(self, pin_position, edge):
        """ Return the suggested position to aviod overlap """
        ll, ur = self.bbox
        c = pin_position # original source pin center
        offset = 0.95 + 0.19 # FIX: this is the magic number to overcome the ovetflow problem at the boundary, may need a method
        add_distance = 0

        if edge == "bottom":
            fake_center = vector(c.x, ll.y - self.track_wire * 2 + offset)
            pin_to_close = any(abs(pin_added.center().x - fake_center.x) < (0.4 + self.half_wire * 4)for pin_added in self.io_pins_added_down)
            via_to_close = False
            # if cannot direct place below the source pin, need move towards right, and ensure the min. distance between vias
            while pin_to_close or via_to_close:
                debug.warning("overlap, changing position")
                add_distance = add_distance + 0.1
                fake_center = vector(c.x + add_distance, ll.y - self.track_wire * 2 + offset)
                pin_to_close = any(abs(pin_added.center().x - fake_center.x) < (0.4 + self.half_wire * 4)for pin_added in self.io_pins_added_down)
                via_to_close = abs(fake_center.x - c.x) < 0.6
        if edge == "top":
            fake_center = vector(c.x, ur.y + self.track_wire * 2 - offset)
            pin_to_close = any(abs(pin_added.center().x - fake_center.x) < (0.4 + self.half_wire * 4)for pin_added in self.io_pins_added_up)
            via_to_close = False
            # if cannot direct place below the source pin, need move towards right, and ensure the min. distance between vias
            while pin_to_close or via_to_close:
                debug.warning("overlap, changing position")
                add_distance = add_distance + 0.1
                fake_center = vector(c.x + add_distance, ur.y + self.track_wire * 2 - offset)
                pin_to_close = any(abs(pin_added.center().x - fake_center.x) < (0.4 + self.half_wire * 4)for pin_added in self.io_pins_added_up)
                via_to_close = abs(fake_center.x - c.x) < 0.6

        return fake_center


    def store_dout_position(self, pin, edge, vertical):
        pin_position = pin.center()
        pin_position = self.check_overlap(pin_position, edge)
        # store the center position, rect, layer of fake pin, here make sure the pin in the gds will be big enough
        layer = self.get_layer(int(not vertical))
        half_wire_vector = vector([self.half_wire] * 2)
        nll = pin_position - half_wire_vector - half_wire_vector
        nur = pin_position + half_wire_vector + half_wire_vector
        rect = [nll, nur]
        #fake_pin = [pin.name() + "_" + "fake", pin_position, rect, layer]
        fake_pin = graph_shape(name=pin.name + "_" + "fake",
                          rect=rect,
                          layer_name_pp=layer)

        if edge == "left":
            self.io_pins_added_left.append(fake_pin)
        elif edge == "bottom":
            self.io_pins_added_down.append(fake_pin)
        elif edge == "right":
            self.io_pins_added_right.append(fake_pin)
        elif edge == "top":
            self.io_pins_added_up.append(fake_pin)

        self.io_pins_fake.append(fake_pin)
        debug.warning("pin added: {0}".format(fake_pin))


    def store_position(self, pin, edge, vertical): # also need to store the source pin
        ll, ur = self.bbox
        c = pin.center()
        pattern_clk = r'^clk'
        pattern_csb = r'^csb'
        offset = 0.95 + 0.19 # FIX: this is the magic number to overcome the ovetflow problem at the boundary, may need a method
        if edge == "left":
            fake_center = vector(ll.x - self.track_wire * 2 + offset, c.y)
            if re.match(pattern_clk, pin.name): # clk0 need to be higher at left edge, 0.32 is magic number
                fake_center = vector(ll.x - self.track_wire * 2 + offset, c.y + 0.32)
            if re.match(pattern_csb, pin.name): # csb0 need to be lower at left edge, 0.32 is magic number
                fake_center = vector(ll.x - self.track_wire * 2 + offset, c.y - 0.32)
        if edge == "bottom":
            fake_center = vector(c.x, ll.y - self.track_wire * 2 + offset)
        if edge == "right":
            fake_center = vector(ur.x + self.track_wire * 2 - offset, c.y)
            if re.match(pattern_clk, pin.name): # clk1 need to be lower at right edge, 0.32 is magic number
                fake_center = vector(ur.x + self.track_wire * 2 - offset, c.y - 0.32)
            if re.match(pattern_csb, pin.name): # csb0 need to be higher at right edge, 0.32 is magic number
                fake_center = vector(ur.x + self.track_wire * 2 - offset, c.y + 0.32)
        if edge == "top":
            fake_center = vector(c.x, ur.y + self.track_wire * 2 - offset)
        # store the center position, rect, layer of fake pin, here make sure the pin in the gds will be big enough
        layer = self.get_layer(int(not vertical))
        half_wire_vector = vector([self.half_wire] * 2)
        nll = fake_center - half_wire_vector - half_wire_vector
        nur = fake_center + half_wire_vector + half_wire_vector
        rect = [nll, nur]
        #fake_pin = [pin.name() + "_" + "fake", fake_center, rect, layer]
        fake_pin = graph_shape(name=pin.name + "_" + "fake",
                          rect=rect,
                          layer_name_pp=layer)

        if edge == "left":
            self.io_pins_added_left.append(fake_pin)
        elif edge == "bottom":
            self.io_pins_added_down.append(fake_pin)
        elif edge == "right":
            self.io_pins_added_right.append(fake_pin)
        elif edge == "top":
            self.io_pins_added_up.append(fake_pin)

        self.io_pins_fake.append(fake_pin)
        debug.warning("pin added: {0}".format(fake_pin))


    def add_io_pins(self, pin_names):
        """ Add IO pins on the edges WITHOUT routing them. """
        debug.info(1, "Adding IO pins on the perimeter...")

        # Prepare GDS reader (if necessary for pin/blockage identification)
        self.prepare_gds_reader()

        # Find pins to be added (without routing)
        for name in pin_names:
            self.find_pins(name)# this will add the pins to the self.pins

        # inital position
        pin_list = []
        for name in self.pins:
            pin = next(iter(self.pins[name]))
            pin_list.append(pin)

        self.initial_position(pin_list)

        # Change IO pin names, which means "internal name" will be used, and internal io pins will not have label such as "dout0[0]"
        self.replace_layout_pins(pin_names)


    def add_io_pins_connected(self, pin_names):
        """ Add IO pins on the edges WITH routing them. """
        debug.info(1, "Adding IO pins on the perimeter...")

        # Prepare GDS reader (if necessary for pin/blockage identification)
        self.prepare_gds_reader()

        # Find pins to be added (without routing)
        for name in pin_names:
            self.find_pins(name)# this will add the pins to the self.pins
            debug.warning("the pins in pin_name -> {0}".format(name))

        # inital position
        pin_list = []
        for name in self.pins:
            pin = next(iter(self.pins[name]))
            pin_list.append(pin)
            debug.warning("the pins in self.pins -> {0}".format(name))

        self.initial_position(pin_list)

        # add fake io pins at the perimeter, which will be used for routing
        for fake_pin in self.io_pins_fake:
            self.design.add_layout_pin(text=fake_pin.name,
                                       layer=fake_pin.layer,
                                       offset=fake_pin.ll(),
                                       width=fake_pin.width(),
                                       height=fake_pin.height())

        # connect the source_pin and io_pin(target)
        self.connect_pins(pin_names)

        # remove the fake pin before change the name, in order to avoid possible problem
        for fake_pin in self.io_pins_fake:
            self.remove_io_pins(fake_pin.name)

        # Change IO pin names, which means "internal name" will be used, and internal io pins will not have label such as "dout0[0]"
        self.replace_layout_pins(pin_names)


    def connect_pins(self, pin_names): # pin_names should be a list
        """ Add IO pins on the edges, and connect them to the internal one, not-graph like process """
        debug.info(1, "connecting to io pins...")
        pattern_dout = r'^dout'
        for pin_name in pin_names:
            # get pin pairs ready
            source_pin = next(iter(self.pins[pin_name]))
            for fake_pin in self.io_pins_fake:
                if pin_name + "_" + "fake" == fake_pin.name:
                    target_pin = fake_pin
                    break
            # special hanlde dout pins
            if re.match(pattern_dout, pin_name):
                number_str = re.findall(r'\[(\d+)\]', pin_name)
                if number_str:
                    number = int(number_str[0])
                    if number % 2 == 0:
                        is_up = True
                    else:
                        is_up = False
                point_list = self.decide_point(source_pin, target_pin, is_up)
                self.add_wire(point_list)
            # other pins
            else:
                debug.warning("source{0}".format(source_pin.center()))
                debug.warning("target{0}".format(target_pin.center()))
                point_list = self.decide_point(source_pin, target_pin)
                debug.warning("point_list->{0}".format(point_list))
                self.add_wire(point_list)


    def add_wire(self, point_list):
        if len(point_list) == 2:
            # direct connect
            self.add_line(point_list[0], point_list[1])
        elif len(point_list) == 4:
            # intermediate points
            self.add_line(point_list[0], point_list[1])
            self.add_via(point_list[1])
            self.add_line(point_list[1], point_list[2])
            self.add_via(point_list[2])
            self.add_line(point_list[2], point_list[3])


    def add_line(self, point_1, point_2):
        if round(point_1.y, 3) == round(point_2.y, 3):
            # horizontal m3
            self.design.add_path(self.get_layer(False), [point_1, point_2])
        else:
            # vertical m4
            self.design.add_path(self.get_layer(True), [point_1, point_2])


    def add_via(self, point):
        # currently only m3-m4 vias are supported in this method
        # usd in order to make "z" shape routing only
        self.design.add_via_stack_center(from_layer=self.get_layer(False),
                                         to_layer=self.get_layer(True),
                                         offset=point)


    def add_start_via(self, point):
        # currently only m3-m4 vias are supported in this method
        # used in source_pin only
        self.design.add_via_stack_center(from_layer=self.get_layer(False),
                                         to_layer=self.get_layer(True),
                                         offset=point)


    def add_big_plate(self, layer, offset, width, height):
        # add rectagle at internal source pin, which avoid jog/non-preferred routing, but could implement shift-routing
        # used in source_pin only
        # offset->vertor(...), it is bottom-left position
        self.design.add_rect(layer=layer,
                             offset=offset,
                             width=width,
                             height=height)


    def decide_point(self, source_pin, target_pin, is_up=False):
        ll, ur = self.bbox
        offset = 0.95 + 0.19 # FIX: this is the magic number to overcome the ovetflow problem at the boundary, may need a method
        pattern_clk = r'^clk'
        pattern_csb = r'^csb'
        # internal -> left
        if round(target_pin.center().x, 3) == round(ll.x - self.track_wire * 2 + offset, 3):
            # special handle clk0
            if re.match(pattern_clk, source_pin.name):
                return [vector(source_pin.rc().x, source_pin.rc().y + 0.32), target_pin.lc()]# 0.32 should be same in initial_position
            # special handel csb0
            elif re.match(pattern_csb, source_pin.name):
                return [vector(source_pin.rc().x, source_pin.rc().y - 0.32), target_pin.lc()]# 0.32 should be same in initial_position
            else:
                # direct connect possible
                return [source_pin.rc(), target_pin.lc()] # FIX: not sure if shape overlap in met3 allowed, but seems OK
        # internal -> right
        if round(target_pin.center().x, 3) == round(ur.x + self.track_wire * 2 - offset, 3):
            # special handel clk1
            if re.match(pattern_clk, source_pin.name):
                return [vector(source_pin.lc().x, source_pin.lc().y - 0.32), target_pin.rc()]# 0.32 should be same in initial_position
            # special handle csb0
            elif re.match(pattern_csb, source_pin.name):
                return [vector(source_pin.lc().x, source_pin.lc().y + 0.32), target_pin.rc()]# 0.32 should be same in initial_position
            else:
                # direct connect possible
                return [source_pin.lc(), target_pin.rc()]
        # internal -> top, need to add start_via m3->m4
        if round(target_pin.center().y, 3) == round(ur.y + self.track_wire * 2 - offset, 3):
            self.add_start_via(source_pin.center())
            if round(target_pin.center().x, 3) == round(source_pin.center().x, 3):
                # direct connect possible
                return [source_pin.bc(), target_pin.uc()]
            else:
            # need intermediate point
                #via_basic_y = self.design.bank.height + 3 # 3 is magic number, make sure out of bank area
                via_basic_y = self.design.bank_inst.uy() + 3 * self.design.m3_pitch
                is_up = not is_up# Be attention, for channel at the top, the is_up should be inverted! Otherwise will cause overlap!
                if is_up:
                    #via_basic_y = via_basic_y + 0.5
                    via_basic_y = via_basic_y + self.design.m3_pitch
                else:
                    #via_basic_y = via_basic_y - 0.5
                    via_basic_y = via_basic_y - self.design.m3_pitch
                point_1 = vector(source_pin.center().x, via_basic_y)
                point_2 = vector(target_pin.center().x, via_basic_y)
                return [source_pin.bc(), point_1, point_2, target_pin.uc()]
        # internal -> bottom, need to add start_via m3->m4
        if round(target_pin.center().y, 3) == round(ll.y - self.track_wire * 2 + offset, 3):
            self.add_start_via(source_pin.center())
            if round(target_pin.center().x, 3) == round(source_pin.center().x, 3):
                # direct connect possible
                return [source_pin.uc(), target_pin.bc()]
            else:
            # need intermediate point
                #via_basic_y = ll.y + 22 # 22 is magic number, make sure out of dff area
                via_basic_y = self.design.data_dff_insts[0].uy() + 3 * self.design.m3_pitch
                if is_up:
                    #via_basic_y = via_basic_y + 0.5
                    via_basic_y = via_basic_y + self.design.m3_pitch
                else:
                    #via_basic_y = via_basic_y - 0.5
                    via_basic_y = via_basic_y - self.design.m3_pitch
                point_1 = vector(source_pin.center().x, via_basic_y)
                point_2 = vector(target_pin.center().x, via_basic_y)
                return [source_pin.uc(), point_1, point_2, target_pin.bc()]


    def remove_io_pins(self, pin_name):
        # remove io pin in gds, so we could reroute
        self.design.remove_layout_pin(pin_name)


    def replace_layout_pins(self, pin_names):
        """ Change the IO pin names with new ones around the perimeter. """
        for pin_name in pin_names:
            perimeter_pin_name = pin_name + "_" + "fake"
            for pin in self.io_pins_fake:
                if pin.name == perimeter_pin_name:
                    perimeter_pin = pin
                    self.design.replace_layout_pin(pin_name, perimeter_pin)
                    break





