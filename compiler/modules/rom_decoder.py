# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

from math import ceil, log
from openram.base import design
from openram.sram_factory import factory
from openram.base import vector
from openram import OPTS
from openram.tech import drc


class rom_decoder(design):
    def __init__(self, num_outputs, strap_spacing, name="", route_layer="li", output_layer="m2"):
        
        # word lines/ rows / inputs in the base array become the address lines / cols / inputs in the decoder
        # bit lines / cols / outputs in the base array become the word lines / rows / outputs in the decoder
        # array gets rotated 90deg so that rows/cols switch
        self.strap_spacing=strap_spacing
        self.num_outputs = num_outputs
        self.num_inputs = ceil(log(num_outputs, 2))
        self.create_decode_map()

        for i in range(2 * self.num_inputs): print(self.decode_map[i])
        
        super().__init__(name)

        b = factory.create(module_type=OPTS.bitcell)
        self.cell_height = b.height
        self.route_layer = route_layer
        self.output_layer = output_layer
        self.inv_route_layer = "m1"
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.add_pins()
        self.create_instances()
        

    def create_layout(self):
        self.place_array()
        self.place_input_inverters()
        self.create_outputs()
        self.width = self.array_inst.height
        self.height = self.array_inst.width + self.inv_inst.height
        self.connect_inputs()
        self.route_supplies()
        self.add_boundary()

    def create_decode_map(self):
        self.decode_map = []
        # create decoding map that will be the bitmap for the rom decoder
        # row/col order in the map will be switched in the placed decoder/
        for col in range(self.num_inputs):
            
            # odd cols are address
            # even cols are address bar
            col_array = []
            inv_col_array = []
            for row in range(self.num_outputs):

                addr_idx =  -col - 1

                addr = format(row, 'b')
                if col >= len(addr) :
                    bin_digit = 0
                else:
                    bin_digit = int(addr[addr_idx])

                col_array.append(bin_digit) 
                # print("addr {0}, at indx {1}, digit {2}".format(addr, addr_idx, bin_digit))

                if bin_digit == 0 : inv_col_array.append(1)
                else : inv_col_array.append(0)
                

                    
            self.decode_map.append(col_array)
            self.decode_map.append(inv_col_array)
        self.decode_map.reverse()


    def add_pins(self):
        for i in range(self.num_inputs):
            self.add_pin("in_{0}".format(i), "INPUT")

        for j in range(self.num_outputs):
            self.add_pin("out_{0}".format(j), "OUTPUT")
        self.add_pin("precharge_gate", "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def add_modules(self):

        self.inv_array = factory.create(module_type="rom_inv_array", cols=self.num_inputs)

        self.array_mod = factory.create(module_type="rom_base_array", \
                                        module_name="rom_decode_array", \
                                        cols=self.num_outputs, \
                                        rows=2 * self.num_inputs, \
                                        bitmap=self.decode_map,
                                        strap_spacing = self.strap_spacing,
                                        route_layer=self.route_layer,
                                        output_layer=self.output_layer)


    def create_instances(self):

        self.create_input_inverters()
        self.create_array_inst()
        

    def create_input_inverters(self):
        name = "pre_inv_array"
        self.inv_inst = self.add_inst(name=name, mod=self.inv_array)

        inv_pins = []

        for i in range(self.num_inputs):
            inv_pins.append("in_{0}".format(i))
            inv_pins.append("inbar_{0}".format(i))
        
        inv_pins.append("vdd")
        inv_pins.append("gnd")
        self.connect_inst(inv_pins)


    def create_array_inst(self):
        self.array_inst = self.add_inst(name="decode_array_inst", mod=self.array_mod)
        
        array_pins = []

        for j in range(self.num_outputs):
            name = "out_{0}".format(j)
            array_pins.append(name)


        for i in reversed(range(self.num_inputs)):
            array_pins.append("inbar_{0}".format(i))
            array_pins.append("in_{0}".format(i))
        array_pins.append("precharge_gate")
        array_pins.append("vdd")
        array_pins.append("gnd")
        self.connect_inst(array_pins)


    def place_input_inverters(self):
        print(self.array_inst.ll().x)
        self.inv_inst.place(vector(self.array_inst.ll().x, 0))


    def place_array(self):
        offset = vector(self.array_mod.height, self.inv_array.height + self.m1_width + self.poly_contact.width)
        self.array_inst.place(offset, rotate=90)

    def create_outputs(self):

        self.output_names = []
        self.outputs = []
        for j in range(self.num_outputs):
            name = "out_{0}".format(j)
            self.output_names.append(name)


        for bl in range(self.num_outputs):
            self.copy_layout_pin(self.array_inst, self.array_mod.bitline_names[0][bl], self.output_names[bl])
            # prechg_pin = self.array_mod.bitline_names[0][bl]
            # src_pin = self.array_inst.get_pin(prechg_pin)
            # offset = src_pin.center()
            # self.add_via_stack_center(offset, self.route_layer, self.output_layer)
            # self.outputs.append(self.add_layout_pin_rect_center(self.output_names[bl], self.output_layer, offset ))
        
    def connect_inputs(self):

        for i in range(self.num_inputs):
            wl = self.num_inputs * 2 - i * 2 - 1
            wl_bar = wl - 1
            addr_pin = self.array_inst.get_pin(self.array_mod.wordline_names[0][wl])
            addr_bar_pin = self.array_inst.get_pin(self.array_mod.wordline_names[0][wl_bar])

            inv_in_pin = self.inv_inst.get_pin("inv{}_in".format(i))
            inv_out_pin = self.inv_inst.get_pin("inv{}_out".format(i))

            addr_start = inv_in_pin.center()
            addr_end = vector(addr_start.x, addr_pin.cy())

            addr_bar_start = inv_out_pin.center()
            addr_bar_end = vector(addr_bar_start.x, addr_bar_pin.cy())
            self.add_segment_center(self.inv_route_layer, addr_start, addr_end)
            self.add_segment_center(self.inv_route_layer, addr_bar_start, addr_bar_end)

    def route_supplies(self):
        minwidth =  drc["minwidth_{}".format(self.inv_route_layer)]
        pitch = drc["{0}_to_{0}".format(self.inv_route_layer)]


        # route decode array vdd and inv array vdd together
        array_vdd = self.array_inst.get_pin("vdd")
        inv_vdd = self.inv_inst.get_pins("vdd")[-1]

        end = vector(array_vdd.cx(), inv_vdd.cy() - 0.5 * minwidth)
        self.add_segment_center("m1", array_vdd.center(), end)
        end = vector(array_vdd.cx() + 0.5 * minwidth, inv_vdd.cy())
        self.add_segment_center(self.route_layer, inv_vdd.center(), end)

        end = vector(array_vdd.cx(), inv_vdd.cy())
        self.add_via_stack_center(end, self.route_layer, "m1")
        self.add_layout_pin_rect_center("vdd", "m1", end)
        
        # route pin on inv gnd

        inv_gnd = self.inv_inst.get_pins("gnd")[0]
        array_gnd = self.array_inst.get_pins("gnd")

        # add x jog

        start = vector(array_gnd[0].cx(), inv_gnd.cy())
        self.add_via_stack_center(start, self.route_layer, "m1")
        self.add_layout_pin_rect_center("gnd", "m1", start)

        end = array_gnd[0].center()
        self.add_segment_center("m1", start, end)
        # add y jog


        width =  minwidth
        height = array_gnd[0].uy() - array_gnd[-1].uy() + minwidth

        offset = vector(-0.5 *width ,0.5 * (array_gnd[0].cy() + array_gnd[-1].cy()))



        # self.add_rect_center(self.route_layer, offset, width, height)


        start = end - vector(0, 0.5 * minwidth)
        end = vector(start.x, array_gnd[1].uy())
        # self.add_segment_center("m1", start, end)

 

