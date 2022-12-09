
import math
from base import vector
from base import design
from globals import OPTS
from sram_factory import factory
import tech
from tech import drc

class rom_base_bank(design):

    def __init__(self, strap_spacing=0, data_file=None, name="") -> None:
        self.rows = 4
        self.cols = 4
        self.num_inputs = 2
        self.data = [[0, 1, 0, 1], [1, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 0]]
        self.strap_spacing = strap_spacing
        self.route_layer = "li"
        self.bus_layer = "m1"
        self.interconnect_layer = "m2"


        
        super().__init__(name=name)
        self.setup_layout_constants()
        self.create_netlist()
        self.create_layout()

    def create_netlist(self):
        self.add_modules()
        self.create_instances()
        
    def create_layout(self):
        self.place_instances()
        self.create_wl_bus()
        self.route_decode_outputs()
        self.route_array_inputs()

        self.route_supplies()
        self.height = self.array_inst.height
        self.width = self.array_inst.width
        self.add_boundary()


    def setup_layout_constants(self):
        self.route_layer_width = drc["minwidth_{}".format(self.route_layer)]
        self.route_layer_pitch = drc["{0}_to_{0}".format(self.route_layer)]
        self.bus_layer_width = drc["minwidth_{}".format(self.bus_layer)]
        self.bus_layer_pitch = drc["{0}_to_{0}".format(self.bus_layer)]
        

    def add_modules(self):
        self.array = factory.create(module_type="rom_base_array", cols=self.cols, rows=self.rows, strap_spacing=self.strap_spacing, bitmap=self.data, route_layer=self.route_layer) 
        self.decode_array = factory.create(module_type="rom_decoder", num_outputs=self.rows, strap_spacing=self.strap_spacing, route_layer=self.route_layer)

        

    def create_instances(self):
        array_pins = []
        decode_pins = []

        for bl in range(self.cols):
            name = "bl_{}".format(bl)
            array_pins.append(name)
        for wl in range(self.rows):
            name = "wl_{}".format(wl)
            array_pins.append(wl)
        
        array_pins.append("array_precharge")
        array_pins.append("vdd")
        array_pins.append("gnd")


        for addr in range(self.num_inputs):
            name = "addr_{}".format(addr)
            decode_pins.append(name)
        for wl in range(self.rows):
            name = "wl_{}".format(wl)
            decode_pins.append(name)

        decode_pins.append("decode_precharge")
        decode_pins.append("vdd")
        decode_pins.append("gnd")


        self.array_inst = self.add_inst(name="rom_bit_array", mod=self.array)
        self.connect_inst(array_pins)

        self.decode_inst = self.add_inst(name="rom_decoder", mod=self.decode_array)
        self.connect_inst(decode_pins)


        
    def place_instances(self):
        
        array_x = self.decode_inst.width + (self.rows + 2) * ( self.route_layer_width + self.route_layer_pitch ) 
        array_y = self.array.height 
        
        self.array_offset = vector(array_x ,array_y)
        self.decode_offset = vector(0, 0)

        self.array_inst.place(offset=self.array_offset, mirror="MX")

        self.decode_inst.place(offset=self.decode_offset)

    def create_wl_bus(self):
        bus_x = self.decode_inst.width + ( drc["minwidth_{}".format(self.bus_layer)] + 1.5 * drc["{0}_to_{0}".format(self.bus_layer)] )
        bus_y = self.array_inst.by() + self.bus_layer_pitch + self.bus_layer_width
        self.wl_interconnects = []

        for wl in range(self.rows):
            self.wl_interconnects.append("wl_interconnect_{}".format(wl))
        
        self.wl_bus = self.create_vertical_bus(self.bus_layer, vector(bus_x, bus_y), self.wl_interconnects, self.decode_inst.uy() - self.array_inst.by() )

    def route_decode_outputs(self):

        for wl in range(self.rows):
            decode_output = self.decode_array.output_names[wl]
            decode_out_pin = self.decode_inst.get_pin(decode_output)

            wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

            start = decode_out_pin.center()
            end = vector(wl_bus_wire.cx(), start.y)

            self.add_segment_center(self.interconnect_layer, start, end)
            self.add_via_stack_center(end, self.route_layer, self.interconnect_layer )


    def route_array_inputs(self):

        for wl in range(self.rows):
            array_wl = self.array.wordline_names[0][wl]
            array_wl_pin = self.array_inst.get_pin(array_wl)

            wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

            end = array_wl_pin.center()
            start = vector(wl_bus_wire.cx(), end.y)

            self.add_segment_center(self.interconnect_layer, start, end)
            self.add_via_stack_center(start, self.route_layer, self.interconnect_layer )


    def route_supplies(self):
        gnd_start = vector(self.array_inst.get_pins("gnd")[0].cx(),0)
        print()
        print(self.decode_inst.get_pin("gnd").center())
        decode_gnd = self.decode_inst.get_pin("gnd")
        decode_vdd = self.decode_inst.get_pin("vdd")
        array_vdd = self.array_inst.get_pin("vdd")

        self.add_segment_center("m1", gnd_start, decode_gnd.center())

        

        self.add_power_pin("gnd", decode_vdd.center())
        self.add_power_pin("vdd", decode_gnd.center())

        vdd_start = vector(array_vdd.lx() + 0.5 * self.via1_space, array_vdd.cy())
        end = vector(decode_vdd.lx(), vdd_start.y)

        self.add_segment_center(self.interconnect_layer, vdd_start, end)
        self.add_via_stack_center(vdd_start, "m1", self.interconnect_layer)

        vdd_start = vector(decode_vdd.cx(), vdd_start.y)

        self.add_segment_center(self.interconnect_layer, vdd_start, decode_vdd.center())

        


        



