# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
import math
from vector import vector
from sram_factory import factory
from globals import OPTS


class hierarchical_predecode(design.design):
    """
    Pre 2x4 and 3x8 and TBD 4x16 decoder shared code.
    """
    def __init__(self, name, input_number, height=None):
        self.number_of_inputs = input_number

        b = factory.create(module_type="bitcell")
        if not height:
            self.cell_height = b.height
            self.column_decoder = False
        else:
            self.cell_height = height
        # If we are pitch matched to the bitcell, it's a predecoder
        # otherwise it's a column decoder (out of pgates)
        self.column_decoder = (height != b.height)
            
        self.number_of_outputs = int(math.pow(2, self.number_of_inputs))
        super().__init__(name)
    
    def add_pins(self):
        for k in range(self.number_of_inputs):
            self.add_pin("in_{0}".format(k), "INPUT")
        for i in range(self.number_of_outputs):
            self.add_pin("out_{0}".format(i), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        """ Add the INV and AND gate modules """

        debug.check(self.number_of_inputs < 4,
                    "Invalid number of predecode inputs: {}".format(self.number_of_inputs))
            
        if self.column_decoder:
            and_type = "pand{}".format(self.number_of_inputs)
            inv_type = "pinv"
        else:
            and_type = "and{}_dec".format(self.number_of_inputs)
            inv_type = "inv_dec"
        self.and_mod = factory.create(module_type=and_type,
                                      height=self.cell_height)
        self.add_mod(self.and_mod)

        # This uses the pinv_dec parameterized cell
        self.inv = factory.create(module_type=inv_type,
                                  height=self.cell_height,
                                  size=1)
        self.add_mod(self.inv)

    def create_layout(self):
        """ The general organization is from left to right:
        1) a set of M2 rails for input signals
        2) a set of inverters to invert input signals
        3) a set of M2 rails for the vdd, gnd, inverted inputs, inputs
        4) a set of AND gates for inversion
        """
        self.setup_layout_constraints()
        self.route_rails()
        self.place_input_inverters()
        self.place_and_array()
        self.route()
        self.add_boundary()
        self.DRC_LVS()
        
    def setup_layout_constraints(self):

        # Inputs to cells are on input layer
        # Outputs from cells are on output layer
        if OPTS.tech_name == "sky130":
            self.bus_layer = "m1"
            self.bus_directions = "nonpref"
            self.bus_pitch = self.m1_pitch
            self.bus_space = 1.5 * self.m1_space
            self.input_layer = "m2"
            self.output_layer = "li"
            self.output_layer_pitch = self.li_pitch
        else:
            self.bus_layer = "m2"
            self.bus_directions = "pref"
            self.bus_pitch = self.m2_pitch
            self.bus_space = self.m2_space
            # This requires a special jog to ensure to conflicts with the output layers
            self.input_layer = "m1"
            self.output_layer = "m1"
            self.output_layer_pitch = self.m1_pitch
            
        self.height = self.number_of_outputs * self.and_mod.height

        # x offset for input inverters
        # +1 input for spacing for supply rail contacts
        self.x_off_inv_1 = (self.number_of_inputs + 1) * self.bus_pitch + self.bus_pitch

        # x offset to AND decoder includes the left rails, mid rails and inverters, plus two extra bus pitches
        self.x_off_and = self.x_off_inv_1 + self.inv.width + (2 * self.number_of_inputs + 2) * self.bus_pitch

        # x offset to output inverters
        self.width = self.x_off_and + self.and_mod.width

    def route_rails(self):
        """ Create all of the rails for the inputs and vdd/gnd/inputs_bar/inputs """
        input_names = ["in_{}".format(x) for x in range(self.number_of_inputs)]
        # Offsets for the perimeter spacing to other modules
        # This uses m3 pitch to leave space for power routes
        offset = vector(self.bus_pitch, self.bus_pitch)
        self.input_rails = self.create_vertical_bus(layer=self.bus_layer,
                                                    offset=offset,
                                                    names=input_names,
                                                    length=self.height - 2 * self.bus_pitch)

        invert_names = ["Abar_{}".format(x) for x in range(self.number_of_inputs)]
        non_invert_names = ["A_{}".format(x) for x in range(self.number_of_inputs)]
        decode_names = invert_names + non_invert_names
        offset = vector(self.x_off_inv_1 + self.inv.width + self.bus_pitch, self.bus_pitch)
        self.decode_rails = self.create_vertical_bus(layer=self.bus_layer,
                                                     offset=offset,
                                                     names=decode_names,
                                                     length=self.height - 2 * self.bus_pitch)

    def create_input_inverters(self):
        """ Create the input inverters to invert input signals for the decode stage. """
        self.inv_inst = []
        for inv_num in range(self.number_of_inputs):
            name = "pre_inv_{0}".format(inv_num)
            self.inv_inst.append(self.add_inst(name=name,
                                               mod=self.inv))
            self.connect_inst(["in_{0}".format(inv_num),
                               "inbar_{0}".format(inv_num),
                               "vdd", "gnd"])

    def place_input_inverters(self):
        """ Place the input inverters to invert input signals for the decode stage. """
        for inv_num in range(self.number_of_inputs):
            
            if (inv_num % 2 == 0):
                y_off = inv_num * (self.inv.height)
                mirror = "R0"
            else:
                y_off = (inv_num + 1) * (self.inv.height)
                mirror="MX"
            offset = vector(self.x_off_inv_1, y_off)
            self.inv_inst[inv_num].place(offset=offset,
                                         mirror=mirror)
            
    def create_and_array(self, connections):
        """ Create the AND stage for the decodes """
        self.and_inst = []
        for and_input in range(self.number_of_outputs):
            inout = str(self.number_of_inputs) + "x" + str(self.number_of_outputs)
            name = "Xpre{0}_and_{1}".format(inout, and_input)
            self.and_inst.append(self.add_inst(name=name,
                                               mod=self.and_mod))
            self.connect_inst(connections[and_input])

    def place_and_array(self):
        """ Place the AND stage for the decodes """
        for and_input in range(self.number_of_outputs):
            # inout = str(self.number_of_inputs) + "x" + str(self.number_of_outputs)
            if (and_input % 2 == 0):
                y_off = and_input * self.and_mod.height
                mirror = "R0"
            else:
                y_off = (and_input + 1) * self.and_mod.height
                mirror = "MX"
            offset = vector(self.x_off_and, y_off)
            self.and_inst[and_input].place(offset=offset,
                                           mirror=mirror)

    def route(self):
        self.route_input_inverters()
        self.route_inputs_to_rails()
        self.route_and_to_rails()
        self.route_output_and()
        self.route_vdd_gnd()

    def route_inputs_to_rails(self):
        """ Route the uninverted inputs to the second set of rails """

        top_and_gate = self.and_inst[-1]
        for num in range(self.number_of_inputs):
            if num == 0:
                pin = top_and_gate.get_pin("A")
            elif num == 1:
                pin = top_and_gate.get_pin("B")
            elif num == 2:
                pin = top_and_gate.get_pin("C")
            elif num == 3:
                pin = top_and_gate.get_pin("D")
            else:
                debug.error("Too many inputs for predecoder.", -1)
            y_offset = pin.cy()
            in_pin = "in_{}".format(num)
            a_pin = "A_{}".format(num)
            in_pos = vector(self.input_rails[in_pin].cx(), y_offset)
            a_pos = vector(self.decode_rails[a_pin].cx(), y_offset)
            self.add_path(self.input_layer, [in_pos, a_pos])
            self.add_via_stack_center(from_layer=self.input_layer,
                                      to_layer=self.bus_layer,
                                      offset=[self.input_rails[in_pin].cx(), y_offset])
            self.add_via_stack_center(from_layer=self.input_layer,
                                      to_layer=self.bus_layer,
                                      offset=[self.decode_rails[a_pin].cx(), y_offset])

    def route_output_and(self):
        """
        Route all conections of the outputs and gates
        """
        for num in range(self.number_of_outputs):

            z_pin = self.and_inst[num].get_pin("Z")
            self.add_layout_pin(text="out_{}".format(num),
                                layer=z_pin.layer,
                                offset=z_pin.ll(),
                                height=z_pin.height(),
                                width=z_pin.width())
    
    def route_input_inverters(self):
        """
        Route all conections of the inputs inverters [Inputs, outputs, vdd, gnd]
        """
        for inv_num in range(self.number_of_inputs):
            out_pin = "Abar_{}".format(inv_num)
            in_pin = "in_{}".format(inv_num)

            inv_out_pin = self.inv_inst[inv_num].get_pin("Z")
            
            # add output so that it is just below the vdd or gnd rail
            # since this is where the p/n devices are and there are no
            # pins in the and gates.
            inv_out_pos = inv_out_pin.rc()
            y_offset = (inv_num + 1) * self.inv.height - self.output_layer_pitch
            right_pos = inv_out_pos + vector(self.inv.width - self.inv.get_pin("Z").rx(), 0)
            rail_pos = vector(self.decode_rails[out_pin].cx(), y_offset)
            self.add_path(self.output_layer, [inv_out_pos, right_pos, vector(right_pos.x, y_offset), rail_pos])
                
            self.add_via_stack_center(from_layer=inv_out_pin.layer,
                                      to_layer=self.output_layer,
                                      offset=inv_out_pos)
            self.add_via_stack_center(from_layer=self.output_layer,
                                      to_layer=self.bus_layer,
                                      offset=rail_pos,
                                      directions=self.bus_directions)
            
            # route input
            pin = self.inv_inst[inv_num].get_pin("A")
            inv_in_pos = pin.center()
            in_pos = vector(self.input_rails[in_pin].cx(), inv_in_pos.y)
            self.add_path(self.input_layer, [in_pos, inv_in_pos])
            self.add_via_stack_center(from_layer=pin.layer,
                                      to_layer=self.input_layer,
                                      offset=inv_in_pos)
            via=self.add_via_stack_center(from_layer=self.input_layer,
                                          to_layer=self.bus_layer,
                                          offset=in_pos)
            # Create the input pin at this location on the rail
            self.add_layout_pin_rect_center(text=in_pin,
                                            layer=self.bus_layer,
                                            offset=in_pos,
                                            height=via.mod.second_layer_height,
                                            width=via.mod.second_layer_width)
            
    def route_and_to_rails(self):
        # This 2D array defines the connection mapping
        and_input_line_combination = self.get_and_input_line_combination()
        for k in range(self.number_of_outputs):
            # create x offset list
            index_lst= and_input_line_combination[k]

            if self.number_of_inputs == 2:
                gate_lst = ["A", "B"]
            else:
                gate_lst = ["A", "B", "C"]

            # this will connect pins A,B or A,B,C
            for rail_pin, gate_pin in zip(index_lst, gate_lst):
                pin = self.and_inst[k].get_pin(gate_pin)
                pin_pos = pin.center()
                rail_pos = vector(self.decode_rails[rail_pin].cx(), pin_pos.y)
                self.add_path(self.input_layer, [rail_pos, pin_pos])
                self.add_via_stack_center(from_layer=self.input_layer,
                                          to_layer=self.bus_layer,
                                          offset=rail_pos,
                                          directions=self.bus_directions)
                if gate_pin == "A":
                    direction = None
                else:
                    direction = ("H", "H")
                    
                self.add_via_stack_center(from_layer=pin.layer,
                                          to_layer=self.input_layer,
                                          offset=pin_pos,
                                          directions=direction)

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # In sky130, we use hand-made decoder cells with vertical power
        if OPTS.tech_name == "sky130" and not self.column_decoder:
            for n in ["vdd", "gnd"]:
                # This makes a wire from top to bottom for both inv and and gates
                for i in [self.inv_inst, self.and_inst]:
                    bot_pins = i[0].get_pins(n)
                    top_pins = i[-1].get_pins(n)
                    for (bot_pin, top_pin) in zip(bot_pins, top_pins):
                        self.add_rect(layer=bot_pin.layer,
                                      offset=vector(bot_pin.lx(), self.bus_pitch),
                                      width=bot_pin.width(),
                                      height=top_pin.uy() - self.bus_pitch)
                # This adds power vias at the top of each cell
                # (except the last to keep them inside the boundary)
                for i in self.inv_inst[:-1:2] + self.and_inst[:-1:2]:
                    pins = i.get_pins(n)
                    for pin in pins:
                        self.add_power_pin(name=n,
                                           loc=pin.uc(),
                                           start_layer=pin.layer)
                        self.add_power_pin(name=n,
                                           loc=pin.uc(),
                                           start_layer=pin.layer)
                    
        # In other techs, we are using standard cell decoder cells with horizontal power
        else:
            for num in range(0, self.number_of_outputs):

                # Route both supplies
                for n in ["vdd", "gnd"]:
                    and_pins = self.and_inst[num].get_pins(n)
                    for and_pin in and_pins:
                        self.add_segment_center(layer=and_pin.layer,
                                                start=vector(0, and_pin.cy()),
                                                end=vector(self.width, and_pin.cy()))

                        # Add pins in two locations
                        for xoffset in [self.inv_inst[0].lx() - self.bus_space,
                                        self.and_inst[0].lx() - self.bus_space]:
                            pin_pos = vector(xoffset, and_pin.cy())
                            self.add_power_pin(name=n,
                                               loc=pin_pos,
                                               start_layer=and_pin.layer)
            


