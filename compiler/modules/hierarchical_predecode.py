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
import contact
from vector import vector
from sram_factory import factory
from tech import cell_properties


class hierarchical_predecode(design.design):
    """
    Pre 2x4 and 3x8 decoder shared code.
    """
    def __init__(self, name, input_number, height=None):
        self.number_of_inputs = input_number

        if not height:
            b = factory.create(module_type="bitcell")
            try:
                self.cell_multiple = cell_properties.bitcell.decoder_bitcell_multiple
            except AttributeError:
                self.cell_multiple = 1
            self.cell_height = self.cell_multiple * b.height
        else:
            self.cell_height = height
        
        self.number_of_outputs = int(math.pow(2, self.number_of_inputs))
        design.design.__init__(self, name)
    
    def add_pins(self):
        for k in range(self.number_of_inputs):
            self.add_pin("in_{0}".format(k), "INPUT")
        for i in range(self.number_of_outputs):
            self.add_pin("out_{0}".format(i), "OUTPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")

    def add_modules(self):
        """ Add the INV and AND gate modules """
        
        self.inv = factory.create(module_type="pinv",
                                  height=self.cell_height)
        self.add_mod(self.inv)
        
        self.add_and(self.number_of_inputs)
        self.add_mod(self.and_mod)

    def add_and(self, inputs):
        """ Create the NAND for the predecode input stage """
        if inputs==2:
            self.and_mod = factory.create(module_type="pand2",
                                          height=self.cell_height)
        elif inputs==3:
            self.and_mod = factory.create(module_type="pand3",
                                          height=self.cell_height)
        else:
            debug.error("Invalid number of predecode inputs: {}".format(inputs), -1)
            
    def setup_layout_constraints(self):

        self.height = self.number_of_outputs * self.and_mod.height

        # x offset for input inverters
        self.x_off_inv_1 = self.number_of_inputs * self.m2_pitch + self.m2_space

        # x offset to AND decoder includes the left rails, mid rails and inverters, plus two extra m2 pitches
        self.x_off_and = self.x_off_inv_1 + self.inv.width + (2 * self.number_of_inputs + 2) * self.m2_pitch

        # x offset to output inverters
        self.width = self.x_off_and + self.and_mod.width

    def route_rails(self):
        """ Create all of the rails for the inputs and vdd/gnd/inputs_bar/inputs """
        input_names = ["in_{}".format(x) for x in range(self.number_of_inputs)]
        offset = vector(0.5 * self.m2_width, self.m3_pitch)
        self.input_rails = self.create_vertical_pin_bus(layer="m2",
                                                        offset=offset,
                                                        names=input_names,
                                                        length=self.height - 2 * self.m1_pitch)

        invert_names = ["Abar_{}".format(x) for x in range(self.number_of_inputs)]
        non_invert_names = ["A_{}".format(x) for x in range(self.number_of_inputs)]
        decode_names = invert_names + non_invert_names
        offset = vector(self.x_off_inv_1 + self.inv.width + 2 * self.m2_pitch, self.m3_pitch)
        self.decode_rails = self.create_vertical_bus(layer="m2",
                                                     offset=offset,
                                                     names=decode_names,
                                                     length=self.height - 2 * self.m1_pitch)

    def create_input_inverters(self):
        """ Create the input inverters to invert input signals for the decode stage. """
        self.in_inst = []
        for inv_num in range(self.number_of_inputs):
            name = "pre_inv_{0}".format(inv_num)
            self.in_inst.append(self.add_inst(name=name,
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
            self.in_inst[inv_num].place(offset=offset,
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
        for num in range(self.number_of_inputs):
            # route one signal next to each vdd/gnd rail since this is
            # typically where the p/n devices are and there are no
            # pins in the and gates.
            y_offset = (num + self.number_of_inputs) * self.inv.height + contact.m2_via.width + self.m2_space
            in_pin = "in_{}".format(num)
            a_pin = "A_{}".format(num)
            in_pos = vector(self.input_rails[in_pin].x, y_offset)
            a_pos = vector(self.decode_rails[a_pin].x, y_offset)
            self.add_path("m1", [in_pos, a_pos])
            self.add_via_stack_center(from_layer="m1",
                                      to_layer="m2",
                                      offset=[self.input_rails[in_pin].x, y_offset])
            self.add_via_stack_center(from_layer="m1",
                                      to_layer="m2",
                                      offset=[self.decode_rails[a_pin].x, y_offset])

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
            
            # add output so that it is just below the vdd or gnd rail
            # since this is where the p/n devices are and there are no
            # pins in the and gates.
            y_offset = (inv_num + 1) * self.inv.height - 3 * self.m1_space
            inv_out_pin = self.in_inst[inv_num].get_pin("Z")
            inv_out_pos = inv_out_pin.rc()
            right_pos = inv_out_pos + vector(self.inv.width - self.inv.get_pin("Z").lx(), 0)
            rail_pos = vector(self.decode_rails[out_pin].x, y_offset)
            self.add_path(inv_out_pin.layer, [inv_out_pos, right_pos, vector(right_pos.x, y_offset), rail_pos])
            self.add_via_stack_center(from_layer=inv_out_pin.layer,
                                      to_layer="m2",
                                      offset=rail_pos)
            
            # route input
            pin = self.in_inst[inv_num].get_pin("A")
            inv_in_pos = pin.lc()
            in_pos = vector(self.input_rails[in_pin].x, inv_in_pos.y)
            self.add_path("m1", [in_pos, inv_in_pos])
            self.add_via_stack_center(from_layer=pin.layer,
                                      to_layer="m1",
                                      offset=inv_in_pos)
            self.add_via_stack_center(from_layer="m1",
                                      to_layer="m2",
                                      offset=in_pos)
            
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
                rail_pos = vector(self.decode_rails[rail_pin].x, pin_pos.y)
                self.add_path("m1", [rail_pos, pin_pos])
                self.add_via_stack_center(from_layer="m1",
                                          to_layer="m2",
                                          offset=rail_pos)
                if gate_pin == "A":
                    direction = None
                else:
                    direction = ("H", "H")
                    
                self.add_via_stack_center(from_layer=pin.layer,
                                          to_layer="m1",
                                          offset=pin_pos,
                                          directions=direction)

    def route_vdd_gnd(self):
        """ Add a pin for each row of vdd/gnd which are must-connects next level up. """

        # Find the x offsets for where the vias/pins should be placed
        in_xoffset = self.in_inst[0].rx() + self.m1_space
        # out_xoffset = self.and_inst[0].cx() + self.m1_space
        for num in range(0, self.number_of_outputs):
            # this will result in duplicate polygons for rails, but who cares
            
            # Route both supplies
            for n in ["vdd", "gnd"]:
                and_pin = self.and_inst[num].get_pin(n)
                supply_offset = and_pin.ll().scale(0, 1)
                self.add_rect(layer=and_pin.layer,
                              offset=supply_offset,
                              width=self.and_inst[num].rx())

                # Add pins in two locations
                for xoffset in [in_xoffset]:
                    pin_pos = vector(xoffset, and_pin.cy())
                    self.add_power_pin(name=n,
                                       loc=pin_pos,
                                       start_layer=and_pin.layer)
            


