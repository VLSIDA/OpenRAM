# See LICENSE for licensing information.
#
# Copyright (c) 2016-2024 Regents of the University of California, Santa Cruz
# All rights reserved.
#
from openram import debug
from openram.base.vector import vector
from openram import OPTS
from .graph import graph
from .graph_shape import graph_shape
from .router import router

class supply_placer(router):

    def __init__(self, layers, design, bbox=None, pin_type=None, ext_vdd_name="vccd1", ext_gnd_name="vssd1", moat_pins=None):

        # `router` is the base router class
        router.__init__(self, layers, design, bbox)

        # Side supply pin type
        # (can be "top", "bottom", "right", "left", and "ring")
        self.pin_type = pin_type
        # New pins are the side supply pins
        self.new_pins = {}
        # external power name of the whole macro
        self.ext_vdd_name = ext_vdd_name
        self.ext_gnd_name = ext_gnd_name
        # instances
        self.insts = self.design.insts
        # moat pins
        self.moat_pins = moat_pins
        # store a graphshape of intermediate points(if shift)/source points(if no shift) when connecting moat_pins to outside
        # trick: since in the creation of dnwell, these pins are "ordered" added, so they'are also ordered here
        # order inside list: left -> right or bottom -> up
        self.moat_pins_left = []
        self.moat_pins_right = []
        self.moat_pins_top = []
        self.moat_pins_bottom = []
        # io pins
        self.io_pins_left = []
        self.io_pins_right = []
        self.io_pins_top = []
        self.io_pins_bottom = []


    def route_outside(self, vdd_name="vdd", gnd_name="gnd", io_pin_names=None):
        # only connect supply with inside submodules, not connecting to the power ring
        debug.info(1, "Running router for {} and {}...".format(vdd_name, gnd_name))

        # Save pin names
        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

        # Prepare gdsMill to find pins and blockages
        self.prepare_gds_reader()

        # Find vdd/gnd pins of bank, to be routed
        self.find_pins_inside(vdd_name)
        self.find_pins_inside(gnd_name)
        self.route_moat(io_pin_names)
        # Find blockages and vias
        self.find_blockages()
        self.find_vias()

        # Convert blockages and vias if they overlap a pin
        self.convert_vias()
        self.convert_blockages()

        # Add vdd and gnd pins as blockages as well
        # NOTE: This is done to make vdd and gnd pins DRC-safe
        for pin in self.all_pins:
            self.blockages.append(self.inflate_shape(pin))

        # Prepare the selected moat pins
        selected_moat_pins = self.prepare_selected_moat_pins()
        # Route vdd and gnd
        routed_count = 0
        routed_max = len(self.pins[vdd_name]) + len(self.pins[gnd_name]) + len(self.moat_pins) + len(self.new_pins["gnd"])
        for pin_name in [vdd_name, gnd_name]:
            if pin_name == gnd_name: # otherwise will not recognaize the moat blocakge
                self.prepare_gds_reader()
                # Find blockages and vias
                self.find_blockages()
                self.find_vias()

                # Convert blockages and vias if they overlap a pin
                self.convert_vias()
                self.convert_blockages()

            pins = self.pins[pin_name]
            # Route closest pins according to the minimum spanning tree
            for source, target in self.get_mst_with_ring(list(pins), selected_moat_pins, pin_name):
                # Create the graph
                g = graph(self)
                g.create_graph(source, target)
                # Find the shortest path from source to target
                path = g.find_shortest_path()
                # If no path is found, throw an error
                if path is None:
                    self.write_debug_gds(gds_name="{}error.gds".format(OPTS.openram_temp), g=g, source=source, target=target)
                    debug.error("Couldn't route from {} to {}.".format(source, target), -1)
                # Create the path shapes on layout
                new_wires, new_vias = self.add_path(path)
                # Find the recently added shapes
                self.find_blockages(pin_name, new_wires)
                self.find_vias(new_vias)
                # Report routed count
                routed_count += 1
                debug.info(2, "Routed {} of {} supply pins".format(routed_count, routed_max))
        # finsih
        self.replace_layout_pins()


    def route_inside(self, vdd_name="vdd", gnd_name="gnd"):
        # only connect supply with inside submodules, not connecting to the power ring
        debug.info(1, "Running router for {} and {}...".format(vdd_name, gnd_name))

        # Save pin names
        self.vdd_name = vdd_name
        self.gnd_name = gnd_name

        # Prepare gdsMill to find pins and blockages
        self.prepare_gds_reader()

        # Find vdd/gnd pins of bank, to be routed
        self.find_pins_inside(vdd_name)
        self.find_pins_inside(gnd_name)

        # Find blockages and vias
        self.find_blockages()
        self.find_vias()

        # Convert blockages and vias if they overlap a pin
        self.convert_vias()
        self.convert_blockages()

        # Add vdd and gnd pins as blockages as well
        # NOTE: This is done to make vdd and gnd pins DRC-safe
        for pin in self.all_pins:
            self.blockages.append(self.inflate_shape(pin))

        # Route vdd and gnd
        routed_count = 0
        routed_max = len(self.pins[vdd_name]) + len(self.pins[gnd_name])
        for pin_name in [vdd_name, gnd_name]:
            pins = self.pins[pin_name]
            # Route closest pins according to the minimum spanning tree
            for source, target in self.get_mst_pairs(list(pins)):
                # Create the graph
                g = graph(self)
                g.create_graph(source, target)
                # Find the shortest path from source to target
                path = g.find_shortest_path()
                # If no path is found, throw an error
                if path is None:
                    self.write_debug_gds(gds_name="{}error.gds".format(OPTS.openram_temp), g=g, source=source, target=target)
                    debug.error("Couldn't route from {} to {}.".format(source, target), -1)
                # Create the path shapes on layout
                new_wires, new_vias = self.add_path(path)
                # Find the recently added shapes
                self.find_blockages(pin_name, new_wires)
                self.find_vias(new_vias)
                # Report routed count
                routed_count += 1
                debug.info(2, "Routed {} of {} supply pins".format(routed_count, routed_max))
        # finsih
        self.replace_layout_pins()


    def route_moat(self, io_pin_names):
        # route the vdd pins at the moat
        # io_pin_names is a list
        # the moat vdd shape will also be created and stored in the list
        for moat_pin in self.moat_pins:
            self.check_overlap(moat_pin, io_pin_names)


    def replace_layout_pins(self):
        # clear all the inside "vdd " "gnd" at sram module level
        # Copy the pin shape(s) to rectangles
        for pin_name in ["vdd", "gnd"]:
            # Copy the pin shape(s) to rectangles
            for pin in self.design.get_pins(pin_name):
                self.design.add_rect(pin.layer,
                                     pin.ll(),
                                     pin.width(),
                                     pin.height())

            # Remove the pin shape(s)
            self.design.remove_layout_pin(pin_name)

        # Get new pins, change the name of ring to extern supply name
        # vccd1 ring
        pins = self.get_new_pins("vdd")
        for pin in pins:
            self.design.add_layout_pin(self.ext_vdd_name,
                                       pin.layer,
                                       pin.ll(),
                                       pin.width(),
                                       pin.height())
        # vssd1 ring
        pins = self.get_new_pins("gnd")
        for pin in pins:
            self.design.add_layout_pin(self.ext_gnd_name,
                                       pin.layer,
                                       pin.ll(),
                                       pin.width(),
                                       pin.height())


    def prepare_selected_moat_pins(self):
        """ Selcet the possibe moat pins, feed into the MST, where will decide which of these pin should be connected to which pin """
        if len(self.design.all_ports) > 1:
            # in order to save runtime
            # top    -> moat pins all
            # bottom -> moat pins all
            # left   -> moat pins near control logic
            # right  -> moat pins near control logic
            # expected connection for control logic

            # for port 0 -> left
            start_y = self.design.control_logic_insts[0].by()# bottom edge y value
            end_y = self.design.control_logic_insts[0].uy()# up edge y value
            # filter the pin in the range
            filtered_moat_pins_left = [pin for pin in self.moat_pins_left if start_y <= pin.center().y <= end_y]

            # for port 1 -> right
            start_y = self.design.control_logic_insts[1].by()# bottom edge y value
            end_y = self.design.control_logic_insts[1].uy()# up edge y value
            # filter the pin in the range
            filtered_moat_pins_right = [pin for pin in self.moat_pins_right if start_y <= pin.center().y <= end_y]
            # return the selected moat pins
            selected_moat_pins = []
            selected_moat_pins.extend(filtered_moat_pins_left)
            selected_moat_pins.extend(self.moat_pins_bottom)
            selected_moat_pins.extend(filtered_moat_pins_right)
            selected_moat_pins.extend(self.moat_pins_top)
            return selected_moat_pins

        else: # only 1 port
            # in order to save runtime
            # top    -> moat pins all
            # bottom -> moat pins all
            # left   -> moat pins near control logic
            # right  -> moat pins all
            start_y = self.design.control_logic_insts[0].by()# bottom edge y value
            end_y = self.design.control_logic_insts[0].uy()# up edge y value
            # filter the pin in the range
            filtered_moat_pins_left = [pin for pin in self.moat_pins_left if start_y <= pin.center().y <= end_y]
            # return the selected moat pins
            selected_moat_pins = []
            selected_moat_pins.extend(filtered_moat_pins_left)
            selected_moat_pins.extend(self.moat_pins_bottom)
            selected_moat_pins.extend(self.moat_pins_right)
            selected_moat_pins.extend(self.moat_pins_top)
            return selected_moat_pins


    def check_overlap(self, moat_pin, io_pin_names):
        # use all the IO pins(at correspoding edge) to check overlap, check 1 moat vdd pin, give the corresponding target/source position as list, and connect them
        add_distance = 0
        direction = 1
        self.prepare_io_pins(io_pin_names)
        # judge the edge of moat vdd
        edge = self.get_closest_edge(moat_pin)
        source_center = moat_pin.center()
        if edge == "bottom":
            add_distance = self.via2_via3_pitch # if shift, need to fulfill via2-via3 spacing, top/bottom only
            pin_too_close = any(abs(io_pin.center().x - source_center.x) < (self.track_width + 0.1) for io_pin in self.io_pins_bottom)
            tmp_center = vector(source_center.x, source_center.y)
            while pin_too_close:
                tmp_center = vector(source_center.x, source_center.y)
                add_distance = add_distance + 0.1
                if direction == 1: # right shift
                    tmp_center = vector((tmp_center.x + add_distance), tmp_center.y)
                else: # left shift
                    tmp_center = vector((tmp_center.x - add_distance), tmp_center.y)
                pin_too_close = any(abs(io_pin.center().x - tmp_center.x) < (self.track_width + 0.1) for io_pin in self.io_pins_bottom)
                direction = - direction
            # the nearst vdd ring
            vdd_ring = self.new_pins["vdd"][1] # order in list -> "top", "bottom", "right", "left"]
            # bottom ring's y position at it's top
            target_egde_y = vdd_ring.center().y + 0.5 * vdd_ring.height()
            if tmp_center == source_center: # no overlap
                # no jog, direct return the source/target center position
                # the target center position, should consider enought space for via
                target_point = vector(tmp_center.x, (target_egde_y - 0.5 * self.track_wire))
                source_point = vector(tmp_center.x, tmp_center.y)
                point_list = [source_point, target_point]
                self.add_wire(point_list, vertical=True)
                # store the shape of moat pins, need for route later
                ll = vector(source_point.x - 0.5 * self.track_wire, source_point.y - 0.5 * self.track_wire)
                ur = vector(source_point.x + 0.5 * self.track_wire, source_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m4")
                self.moat_pins_bottom.append(moat_pin_route)
            else: # need jog
                # shift the center
                # add rectangle at same layer (original)
                intermediate_point = vector(tmp_center.x, tmp_center.y)
                source_point = vector(source_center.x, source_center.y)
                target_point = vector(tmp_center.x, (target_egde_y - 0.5 * self.track_wire))
                point_list = [source_point, intermediate_point, target_point]
                self.add_wire(point_list, vertical=True)
                # store the shape of moat pins, need for route later
                ll = vector(intermediate_point.x - 0.5 * self.track_wire, intermediate_point.y - 0.5 * self.track_wire)
                ur = vector(intermediate_point.x + 0.5 * self.track_wire, intermediate_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m4")
                self.moat_pins_bottom.append(moat_pin_route)
        elif edge == "top":
            add_distance = self.via2_via3_pitch # if shift, need to fulfill via2-via3 spacing, top/bottom only
            pin_too_close = any(abs(io_pin.center().x - source_center.x) < (self.track_width + 0.1) for io_pin in self.io_pins_top)
            tmp_center = vector(source_center.x, source_center.y)
            while pin_too_close:
                tmp_center = vector(source_center.x, source_center.y)
                add_distance = add_distance + 0.1
                if direction == 1: # right shift
                    tmp_center = vector((tmp_center.x + add_distance), tmp_center.y)
                else: # left shift
                    tmp_center = vector((tmp_center.x - add_distance), tmp_center.y)
                pin_too_close = any(abs(io_pin.center().x - tmp_center.x) < (self.track_width + 0.1) for io_pin in self.io_pins_top)
                direction = - direction
            # the nearst vdd ring
            vdd_ring = self.new_pins["vdd"][0] # order in list -> "top", "bottom", "right", "left"]
            # top ring's y position at it's bottom
            target_egde_y = vdd_ring.center().y - 0.5 * vdd_ring.height()
            if tmp_center == source_center: # no overlap
                # no jog, direct return the source/target center position
                # the target center position, should consider enought space for via
                target_point = vector(tmp_center.x, (target_egde_y + 0.5 * self.track_wire))
                source_point = vector(tmp_center.x, tmp_center.y)
                point_list = [source_point, target_point]
                self.add_wire(point_list, vertical=True)
                # store the shape of moat pins, need for route later
                ll = vector(source_point.x - 0.5 * self.track_wire, source_point.y - 0.5 * self.track_wire)
                ur = vector(source_point.x + 0.5 * self.track_wire, source_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m4")
                self.moat_pins_top.append(moat_pin_route)
            else: # need jog
                # shift the center
                # add rectangle at same layer (original)
                intermediate_point = vector(tmp_center.x, tmp_center.y)
                source_point = vector(source_center.x, source_center.y)
                target_point = vector(tmp_center.x, (target_egde_y + 0.5 * self.track_wire))
                point_list = [source_point, intermediate_point, target_point]
                self.add_wire(point_list, vertical=True)
                # store the shape of moat pins, need for route later
                ll = vector(intermediate_point.x - 0.5 * self.track_wire, intermediate_point.y - 0.5 * self.track_wire)
                ur = vector(intermediate_point.x + 0.5 * self.track_wire, intermediate_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m4")
                self.moat_pins_top.append(moat_pin_route)
        elif edge == "left":
            pin_too_close = any(abs(io_pin.center().y - source_center.y) < (self.track_width + 0.1) for io_pin in self.io_pins_left)
            tmp_center = vector(source_center.x, source_center.y)
            while pin_too_close:
                tmp_center = vector(source_center.x, source_center.y)
                add_distance = add_distance + 0.1
                if direction == 1: # up shift
                    tmp_center = vector(tmp_center.x, (tmp_center.y + add_distance))
                else: # down shift
                    tmp_center = vector(tmp_center.x, (tmp_center.y - add_distance))
                pin_too_close = any(abs(io_pin.center().y - tmp_center.y) < (self.track_width + 0.1) for io_pin in self.io_pins_left)
                direction = - direction
            # the nearst vdd ring
            vdd_ring = self.new_pins["vdd"][3] # order in list -> "top", "bottom", "right", "left"]
            # left ring's x position at it's right
            target_egde_x = vdd_ring.center().x + 0.5 * vdd_ring.width()
            if tmp_center == source_center: # no overlap
                # no jog, direct return the source/target center position
                # the target center position, should consider enought space for via
                target_point = vector((target_egde_x - 0.5 * self.track_wire), tmp_center.y)
                source_point = vector(tmp_center.x, tmp_center.y)
                point_list = [source_point, target_point]
                self.add_wire(point_list, vertical=False)
                # store the shape of moat pins, need for route later
                ll = vector(source_point.x - 0.5 * self.track_wire, source_point.y - 0.5 * self.track_wire)
                ur = vector(source_point.x + 0.5 * self.track_wire, source_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m3")
                self.moat_pins_left.append(moat_pin_route)
            else: # need jog
                # shift the center
                # add rectangle at same layer (original)
                intermediate_point = vector(tmp_center.x, tmp_center.y)
                source_point = vector(source_center.x, source_center.y)
                target_point = vector((target_egde_x - 0.5 * self.track_wire), tmp_center.y)
                point_list = [source_point, intermediate_point, target_point]
                self.add_wire(point_list, vertical=False)
                # store the shape of moat pins, need for route later
                ll = vector(intermediate_point.x - 0.5 * self.track_wire, intermediate_point.y - 0.5 * self.track_wire)
                ur = vector(intermediate_point.x + 0.5 * self.track_wire, intermediate_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m3")
                self.moat_pins_left.append(moat_pin_route)
        else: #right
            pin_too_close = any(abs(io_pin.center().y - source_center.y) < (self.track_width + 0.1) for io_pin in self.io_pins_right)
            tmp_center = vector(source_center.x, source_center.y)
            while pin_too_close:
                tmp_center = vector(source_center.x, source_center.y)
                add_distance = add_distance + 0.1
                if direction == 1: # up shift
                    tmp_center = vector(tmp_center.x, (tmp_center.y + add_distance))
                else: # down shift
                    tmp_center = vector(tmp_center.x, (tmp_center.y - add_distance))
                pin_too_close = any(abs(io_pin.center().y - tmp_center.y) < (self.track_width + 0.1) for io_pin in self.io_pins_right)
                direction = - direction
            # the nearst vdd ring
            vdd_ring = self.new_pins["vdd"][2] # order in list -> "top", "bottom", "right", "left"]
            # right ring's y position at it's left
            target_egde_x = vdd_ring.center().x - 0.5 * vdd_ring.width()
            if tmp_center == source_center: # no overlap
                # no jog, direct return the source/target center position
                # the target center position, should consider enought space for via
                target_point = vector((target_egde_x + 0.5 * self.track_wire), tmp_center.y)
                source_point = vector(tmp_center.x, tmp_center.y)
                point_list = [source_point, target_point]
                self.add_wire(point_list, vertical=False)
                # store the shape of moat pins, need for route later
                ll = vector(source_point.x - 0.5 * self.track_wire, source_point.y - 0.5 * self.track_wire)
                ur = vector(source_point.x + 0.5 * self.track_wire, source_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m3")
                self.moat_pins_right.append(moat_pin_route)
            else: # need jog
                # shift the center
                # add rectangle at same layer (original)
                intermediate_point = vector(tmp_center.x, tmp_center.y)
                source_point = vector(source_center.x, source_center.y)
                target_point = vector((target_egde_x + 0.5 * self.track_wire) ,tmp_center.y)
                point_list = [source_point, intermediate_point, target_point]
                self.add_wire(point_list, vertical=False)
                # store the shape of moat pins, need for route later
                ll = vector(intermediate_point.x - 0.5 * self.track_wire, intermediate_point.y - 0.5 * self.track_wire)
                ur = vector(intermediate_point.x + 0.5 * self.track_wire, intermediate_point.y + 0.5 * self.track_wire)
                rect = [ll, ur]
                moat_pin_route = graph_shape("vdd", rect, "m3")
                self.moat_pins_right.append(moat_pin_route)


    def add_wire(self, point_list, vertical=False):
        if vertical == True: # m4 line, need start via3(m3 -> m4), end via3(m3 -> m4)
            if len(point_list) == 2: # direct connect
                # start via
                self.add_via(point=point_list[0],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[0],
                             from_layer="m4",
                             to_layer="m4") # shape
                # connection
                self.add_line(point_1=point_list[0],
                              point_2=point_list[1],
                              layer="m4")
                # end via
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[1],
                             from_layer="m4",
                             to_layer="m4") # shape
            elif len(point_list) == 3: # need intermediate point
                # jog
                self.add_line(point_1=point_list[0],
                              point_2=point_list[1],
                              layer="m3")
                # start_via
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m3") # shape
                # connection
                self.add_line(point_1=point_list[1],
                              point_2=point_list[2],
                              layer="m4")
                # end via
                self.add_via(point=point_list[2],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[2],
                             from_layer="m4",
                             to_layer="m4") # shape
        else: # m3 line, need start via2(m2 -> m3), end via3(m3 -> m4)
            if len(point_list) == 2: # direct connect
                # start via
                self.add_via(point=point_list[0],
                             from_layer="m2",
                             to_layer="m3")
                self.add_via(point=point_list[0],
                             from_layer="m3",
                             to_layer="m3") # shape
                # connection
                self.add_line(point_1=point_list[0],
                              point_2=point_list[1],
                              layer="m3")
                # end via
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m3") # shape
            elif len(point_list) == 3: # need intermediate point
                # jog
                self.add_line(point_1=point_list[0],
                              point_2=point_list[1],
                              layer="m2")
                # start_via
                self.add_via(point=point_list[1],
                             from_layer="m2",
                             to_layer="m3")
                self.add_via(point=point_list[1],
                             from_layer="m3",
                             to_layer="m3") # shape
                # connection
                self.add_line(point_1=point_list[1],
                              point_2=point_list[2],
                              layer="m3")
                # end via
                self.add_via(point=point_list[2],
                             from_layer="m3",
                             to_layer="m4")
                self.add_via(point=point_list[2],
                             from_layer="m3",
                             to_layer="m3") # shape


    def add_line(self, point_1, point_2, layer="m3"): # "m2", "m3", "m4"
        self.design.add_path(layer, [point_1, point_2], self.track_wire)


    def add_via(self, point, from_layer="m3", to_layer="m4"):
        # via could be via2(m2 -> m3), via3(m3 -> m4)
        # or a shape at same layer
        if from_layer == to_layer:
            self.design.add_rect_center(layer=from_layer,
                                        offset=point,
                                        width=self.track_wire,
                                        height=self.track_wire)
        else:
            self.design.add_via_stack_center(from_layer=from_layer,
                                             to_layer=to_layer,
                                             offset=point)


    def prepare_io_pins(self, io_pin_names):
        # io_pin_names is a list
        # find all the io pins
        for pin_name in io_pin_names:
            self.find_pins(pin_name)# pin now in self.pins
            io_pin = next(iter(self.pins[pin_name]))
            self.find_closest_edge(io_pin)


    def get_closest_edge(self, pin):
        """ Return a point's the closest edge and the edge's axis direction. Here we use to find the edge of moat vdd """

        ll, ur = self.bbox
        point = pin.center()
        debug.warning("moat pin center -> {0}".format(point))
        # Snap the pin to the perimeter and break the iteration
        ll_diff_x = abs(point.x - ll.x)
        ll_diff_y = abs(point.y - ll.y)
        ur_diff_x = abs(point.x - ur.x)
        ur_diff_y = abs(point.y - ur.y)
        min_diff = min(ll_diff_x, ll_diff_y, ur_diff_x, ur_diff_y)

        if min_diff == ll_diff_x:
            return "left"
        if min_diff == ll_diff_y:
            return "bottom"
        if min_diff == ur_diff_x:
            return "right"
        return "top"


    def find_closest_edge(self, pin):
        """ Use to find the edge, where the io pin locats """

        ll, ur = self.bbox
        #debug.warning("pin -> {0}".format(pin))
        point = pin.center()
        # Snap the pin to the perimeter and break the iteration
        ll_diff_x = abs(point.x - ll.x)
        ll_diff_y = abs(point.y - ll.y)
        ur_diff_x = abs(point.x - ur.x)
        ur_diff_y = abs(point.y - ur.y)
        min_diff = min(ll_diff_x, ll_diff_y, ur_diff_x, ur_diff_y)

        if min_diff == ll_diff_x:
            self.io_pins_left.append(pin)
        elif min_diff == ll_diff_y:
            self.io_pins_bottom.append(pin)
        elif min_diff == ur_diff_x:
            self.io_pins_right.append(pin)
        else:
            self.io_pins_top.append(pin)


    def add_side_pin(self, pin_name, side, num_vias=3, num_fake_pins=4):
        """ Add supply pin to one side of the layout. """

        ll, ur = self.bbox
        vertical = side in ["left", "right"]
        inner = pin_name == "vdd"

        # Calculate wires' wideness
        wideness = self.track_wire * num_vias + self.track_space * (num_vias - 1)

        # Calculate the offset for the inner ring
        if inner:
            margin = wideness * 2
        else:
            margin = 0

        # Calculate the lower left coordinate
        if side == "top":
            offset = vector(ll.x + margin, ur.y - wideness - margin)
        elif side == "bottom":
            offset = vector(ll.x + margin, ll.y + margin)
        elif side == "left":
            offset = vector(ll.x + margin, ll.y + margin)
        elif side == "right":
            offset = vector(ur.x - wideness - margin, ll.y + margin)

        # Calculate width and height
        shape = ur - ll
        if vertical:
            shape_width = wideness
            shape_height = shape.y
        else:
            shape_width = shape.x
            shape_height = wideness
        if inner:
            if vertical:
                shape_height -= margin * 2
            else:
                shape_width -= margin * 2

        # Add this new pin
        layer = self.get_layer(int(vertical))
        pin = self.design.add_layout_pin(text=pin_name,
                                         layer=layer,
                                         offset=offset,
                                         width=shape_width,
                                         height=shape_height)

        return pin


    def add_ring_pin(self, pin_name, num_vias=3, num_fake_pins=4):
        """ Add the supply ring to the layout. """

        # Add side pins
        new_pins = []
        for side in ["top", "bottom", "right", "left"]:
            new_shape = self.add_side_pin(pin_name, side, num_vias, num_fake_pins)
            ll, ur = new_shape.rect
            rect = [ll, ur]
            layer = self.get_layer(side in ["left", "right"])
            new_pin = graph_shape(name=pin_name,
                                  rect=rect,
                                  layer_name_pp=layer)
            new_pins.append(new_pin)

        # Add vias to the corners
        shift = self.track_wire + self.track_space
        half_wide = self.track_wire / 2
        for i in range(4):
            ll, ur = new_pins[i].rect
            if i % 2:
                top_left = vector(ur.x - (num_vias - 1) * shift - half_wide, ll.y + (num_vias - 1) * shift + half_wide)
            else:
                top_left = vector(ll.x + half_wide, ur.y - half_wide)
            for j in range(num_vias):
                for k in range(num_vias):
                    offset = vector(top_left.x + j * shift, top_left.y - k * shift)
                    self.design.add_via_center(layers=self.layers,
                                               offset=offset)

        # Save side pins for routing
        self.new_pins[pin_name] = new_pins
        for pin in new_pins:
            self.blockages.append(self.inflate_shape(pin))


    def get_mst_pairs(self, pins):
        """
        Return the pin pairs from the minimum spanning tree in a graph that
        connects all pins together.
        """

        pin_count = len(pins)

        # Create an adjacency matrix that connects all pins
        edges = [[0] * pin_count for i in range(pin_count)]
        for i in range(pin_count):
            for j in range(pin_count):
                # Skip if they're the same pin
                if i == j:
                    continue
                # Skip if both pins are fake
                if pins[i] in self.fake_pins and pins[j] in self.fake_pins:
                    continue
                edges[i][j] = pins[i].distance(pins[j])

        pin_connected = [False] * pin_count
        pin_connected[0] = True

        # Add the minimum cost edge in each iteration (Prim's)
        mst_pairs = []
        for i in range(pin_count - 1):
            min_cost = float("inf")
            s = 0
            t = 0
            # Iterate over already connected pins
            for m in range(pin_count):
                # Skip if not connected
                if not pin_connected[m]:
                    continue
                # Iterate over this pin's neighbors
                for n in range(pin_count):
                    # Skip if already connected or isn't a neighbor
                    if pin_connected[n] or edges[m][n] == 0:
                        continue
                    # Choose this edge if it's better the the current one
                    if edges[m][n] < min_cost:
                        min_cost = edges[m][n]
                        s = m
                        t = n
            pin_connected[t] = True
            mst_pairs.append((pins[s], pins[t]))

        return mst_pairs


    def get_mst_with_ring(self, pins, ring_pins, pin_name="vdd"):
        """
        Extend the MST logic to connect internal pins to the nearest external ring pins.
        """
        # Prepare the pins that are allowed to connect to the moat pins.
        # Specical handle gnd ring
        candidate_pins = []
        max_distance = 20#13
        if pin_name == "gnd":
            ring_pins = []
            ring_pins = self.new_pins[pin_name]
        for pin in pins:
            # Special handle vdd/gnd in 1port sram(1rw), only at bank top-right is allowed
            if len(self.design.all_ports) == 1:
                # check if pin is inside bank area
                if (self.design.bank_inst.lx() < pin.center().x < self.design.bank_inst.rx()) and (self.design.bank_inst.by() < pin.center().y < self.design.bank_inst.uy()):
                    # add pin at top-right as candidate, not care the distance
                    if (pin.center().x > self.design.bank_inst.rx() - 14) and (pin.center().y > self.design.bank_inst.uy() - 14):
                        candidate_pins.append(pin)
                        continue
                    else:# pin in the other area of bank, do not care
                        continue
            # 2 port situation, or the other pins outer bank in 1port situation
            for ring_pin in ring_pins:
                dist = pin.distance(ring_pin)
                if max_distance is None or dist <= max_distance:
                    candidate_pins.append(pin)
                    break

        # Compute the MST for internal pins
        mst_pairs = self.get_mst_pairs(pins)

        # Connect each internal pin to the nearest external ring pin
        used_ring_pins = set()
        internal_to_ring_pairs = []
        for pin in candidate_pins:
            min_distance = float("inf")
            nearest_ring_pin = None

            for ring_pin in ring_pins:
                if pin_name == "vdd" and ring_pin in used_ring_pins:
                    continue

                dist = pin.distance(ring_pin)
                if dist < min_distance:
                    min_distance = dist
                    nearest_ring_pin = ring_pin

            # Add the connection to the nearest ring pin
            if nearest_ring_pin:
                internal_to_ring_pairs.append((pin, nearest_ring_pin))
                # Mark the ring pin as used if the pin is VDD
                if pin_name == "vdd":
                    used_ring_pins.add(nearest_ring_pin)

        # Combine internal MST pairs and external connections
        full_connections = mst_pairs + internal_to_ring_pairs

        return full_connections


    def get_new_pins(self, name):
        """ Return the new supply pins added by this router. """

        return self.new_pins[name]