
from math import ceil, log, sqrt
from openram.base import vector
from openram.base import design
from openram import OPTS
from openram.sram_factory import factory
from openram.tech import drc, layer

class rom_base_bank(design):

    """
    Rom data bank with row and column decoder + control logic

    word size is in bytes
    """

    def __init__(self, strap_spacing=0, data_file=None, name="", word_size=2) -> None:

        self.word_size = word_size * 8
        self.read_binary(word_size=word_size, data_file=data_file)

        self.num_outputs = self.rows
        self.num_inputs = ceil(log(self.rows, 2))
        self.col_bits = ceil(log(self.words_per_row, 2))
        self.row_bits = self.num_inputs
        
        # self.data = [[0, 1, 0, 1], [1, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 0]]
        self.strap_spacing = strap_spacing
        if "li" in layer:
            self.route_layer = "li"
        else:
            self.route_layer = "m1"
        self.bus_layer = "m2"
        self.interconnect_layer = "m1"

        super().__init__(name=name)
        self.setup_layout_constants()
        self.create_netlist()
        self.create_layout()
    """
    Reads a hexadecimal file from a given directory to be used as the data written to the ROM
    endian is either "big" or "little"
    word_size is the number of bytes per word
    sets the row and column size based on the size of binary input, tries to keep array as square as possible, 
    """

    def read_binary(self, data_file, word_size=2, endian="big"):
        
        hex_file = open(data_file, 'r')
        hex_data = hex_file.read()
        bin_data = list("{0:08b}".format(int(hex_data, 16)))
        bin_data = [int(x) for x in bin_data]

        # data size in bytes
        data_size = len(bin_data) / 8 
        num_words = int(data_size / word_size)

        bytes_per_col = sqrt(num_words)

        self.words_per_row = int(ceil(bytes_per_col /(2*word_size)))

        bits_per_row = self.words_per_row * word_size * 8

        chunked_data = []

        for i in range(0, len(bin_data), bits_per_row):
            word = bin_data[i:i + bits_per_row]
            if len(word) < bits_per_row:
                word = [0] * (bits_per_row - len(word)) + word
            chunked_data.append(word)

        if endian == "big":
            chunked_data.reverse()

        self.data = chunked_data
        self.cols = bits_per_row
        self.rows = int(num_words / (self.words_per_row))
        # print("hex: {0}, binary: {1}, chunked: {2}".format(hex_data, bin_data, chunked_data))

        
    def create_netlist(self):
        self.add_modules()
        # self.add_pins()
        self.create_instances()
        
    def create_layout(self):
        self.place_instances()
        # self.channel_route()
        self.route_decode_outputs()
        self.route_control()

        # self.route_supplies()
        self.height = self.array_inst.height
        self.width = self.array_inst.width
        self.add_boundary()


    def setup_layout_constants(self):
        self.route_layer_width = drc["minwidth_{}".format(self.route_layer)]
        self.route_layer_pitch = drc["{0}_to_{0}".format(self.route_layer)]
        self.bus_layer_width = drc["minwidth_{}".format(self.bus_layer)]
        self.bus_layer_pitch = drc["{0}_to_{0}".format(self.bus_layer)]
        self.interconnect_layer_width = drc["minwidth_{}".format(self.interconnect_layer)]
        self.interconnect_layer_pitch = drc["{0}_to_{0}".format(self.interconnect_layer)]

    def add_pins(self):
        
        self.add_pin("READ", "INPUT")
        self.add_pin("CS", "INPUT")

        for i in range(self.num_inputs):
            self.add_pin("addr_{}".format(i), "INPUT")


        out_pins = []
        for j in range(self.rows):
            out_pins.append("rom_out_{}".format(j))
        self.add_pin_list(out_pins, "OUTPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def add_modules(self):
        self.array = factory.create(module_type="rom_base_array", cols=self.cols, rows=self.rows, strap_spacing=self.strap_spacing, bitmap=self.data, route_layer=self.route_layer, pitch_match=True) 
        self.decode_array = factory.create(module_name="rom_row_decode", module_type="rom_decoder", num_outputs=self.rows, strap_spacing=self.strap_spacing, route_layer=self.route_layer, cols=self.cols)
        self.control_logic = factory.create(module_type="rom_control_logic", num_outputs=(self.rows + self.cols) / 2, height=self.decode_array.buf_inst.height)
        self.column_mux = factory.create(module_type="rom_column_mux_array", columns=self.cols, word_size=self.word_size, bitline_layer=self.route_layer)
        
        self.column_decode = factory.create(module_name="rom_column_decode", module_type="rom_decoder", num_outputs=self.words_per_row, strap_spacing=self.strap_spacing, route_layer=self.route_layer, cols=1)

    def create_instances(self):
        gnd = ["gnd"]
        vdd = ["vdd"]
        prechrg = ["precharge"]
        array_pins = []
        decode_pins = []

        for bl in range(self.cols):
            name = "bl_{}".format(bl)
            array_pins.append(name)
        for wl in range(self.rows):
            name = "wl_{}".format(wl)
            array_pins.append(wl)
        
        array_pins.append("precharge")
        array_pins.append("vdd")
        array_pins.append("gnd")


        for addr in range(self.row_bits):
            name = "row_addr_{}".format(addr)
            decode_pins.append(name)
        for wl in range(self.rows):
            name = "wl_{}".format(wl)
            decode_pins.append(name)

        decode_pins.append("precharge")
        decode_pins.append("vdd")
        decode_pins.append("gnd")


        bitlines = ["bl_{}".format(bl) for bl in range(self.cols)]
        select_lines = ["word_sel_{}".format(word) for word in range(self.words_per_row)]
        bitline_out = ["rom_out_{}".format(bl) for bl in range(self.word_size)]
        addr_lsb = ["col_addr_{}".format(addr) for addr in range(self.col_bits)]
        col_mux_pins = bitlines + select_lines + bitline_out + gnd

        col_decode_pins = addr_lsb + select_lines + prechrg + vdd + gnd
        self.array_inst = self.add_inst(name="rom_bit_array", mod=self.array)
        self.connect_inst(array_pins)

        self.decode_inst = self.add_inst(name="rom_row_decoder", mod=self.decode_array)
        self.connect_inst(decode_pins)

        self.control_inst = self.add_inst(name="rom_control", mod=self.control_logic)
        self.connect_inst(["READ", "CS", "precharge", "vdd", "gnd"])

        self.mux_inst = self.add_inst(name="rom_column_mux", mod=self.column_mux)
        self.connect_inst(col_mux_pins)

        self.col_decode_inst = self.add_inst(name="rom_column_decoder", mod=self.column_decode)
        self.connect_inst(col_decode_pins)


        
    def place_instances(self):
        self.place_row_decoder()
        self.place_data_array()
        self.place_control_logic()
        self.place_col_decoder()
        self.place_col_mux()


    def place_row_decoder(self):
        self.decode_offset = vector(0, self.control_inst.height)
        self.decode_inst.place(offset=self.decode_offset)
    
    def place_data_array(self):
        # We approximate the correct position for the array
        array_x = self.decode_inst.width + (2) * ( self.route_layer_width + self.route_layer_pitch ) 
        array_y = self.decode_array.buf_inst.height - self.array.precharge_inst.cy() - self.array.zero_cell.height * 0.5
        self.array_offset = vector(array_x ,array_y)
        self.array_inst.place(offset=self.array_offset)

        # now move array to correct alignment with decoder
        array_align = self.decode_inst.get_pin("wl_0").cy() - self.array_inst.get_pin("wl_0_0").cy()
        self.array_inst.place(offset=(self.array_offset + vector(0, array_align)))
    
    def place_control_logic(self):
        self.control_offset = vector(0,0)
        self.control_inst.place(offset=self.control_offset)

    def place_col_decoder(self):
        self.col_decode_offset = vector(self.control_logic.width * 1.3, 0)
        self.col_decode_inst.place(offset=self.col_decode_offset)

    def place_col_mux(self):

        self.mux_offset = vector(self.decode_inst.width, 0)
        self.mux_inst.place(offset=self.mux_offset)
        
        

    def create_wl_bus(self):
        bus_x = self.decode_inst.width + ( drc["minwidth_{}".format(self.bus_layer)] + 1.5 * drc["{0}_to_{0}".format(self.bus_layer)] )
        bus_y = self.array_inst.by() + self.bus_layer_pitch + self.bus_layer_width
        self.wl_interconnects = []

        for wl in range(self.rows):
            self.wl_interconnects.append("wl_interconnect_{}".format(wl))
        
        self.wl_bus = self.create_vertical_bus(self.bus_layer, vector(bus_x, bus_y), self.wl_interconnects, self.decode_inst.uy() - self.array_inst.by() )

    def route_decode_outputs(self):

        route_pins = [self.array_inst.get_pin("wl_0_{}".format(wl)) for wl in range(self.rows)]
        decode_pins = [self.decode_inst.get_pin("wl_{}".format(wl)) for wl in range(self.rows)]
        route_pins.extend(decode_pins)
        self.connect_row_pins(self.interconnect_layer, route_pins, round=True)

        # for wl in range(self.rows):
        #     decode_output = self.decode_array.output_names[wl]
        #     decode_out_pin = self.decode_inst.get_pin(decode_output)

        #     array_wl = self.array.wordline_names[0][wl]
        #     array_wl_pin = self.array_inst.get_pin(array_wl)


        #     # wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

        #     start = decode_out_pin.center()
        #     end = vector(array_wl_pin.cx(), start.y)

        #     self.add_segment_center(self.bus_layer, start, end)
        #     self.add_via_stack_center(array_wl_pin.center(), self.bus_layer, self.interconnect_layer )


    def route_array_inputs(self):

        for wl in range(self.rows):
            array_wl = self.array.wordline_names[0][wl]
            array_wl_pin = self.array_inst.get_pin(array_wl)

            wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

            end = array_wl_pin.center()
            start = vector(wl_bus_wire.cx(), end.y)

            self.add_segment_center(self.interconnect_layer, start, end)
            self.add_via_stack_center(start, self.route_layer, self.interconnect_layer )

    def channel_route(self):
        route_nets = []
        for wl in range(self.rows):
            array_wl = self.array.wordline_names[0][wl]
            
            array_wl_pin = self.array_inst.get_pin(array_wl)

            decode_output = self.decode_array.output_names[wl]
            decode_out_pin = self.decode_inst.get_pin(decode_output)

            route_nets.append([array_wl_pin, decode_out_pin])

        array_prechrg = self.array_inst.get_pin("precharge")
        decode_prechrg = self.decode_inst.get_pin("precharge")
        route_nets.append([array_prechrg, decode_prechrg])

        channel_start = vector(decode_out_pin.cx(), self.decode_array.array_inst.by())

        channel = self.create_vertical_channel_route(netlist=route_nets, offset=channel_start, layer_stack=self.m1_stack, directions="nonpref")

        
    def route_control(self):

        prechrg_control = self.control_inst.get_pin("prechrg")
        decode_prechrg = self.decode_inst.get_pin("precharge")
        array_prechrg = self.array_inst.get_pin("precharge")

        end = vector(decode_prechrg.cx() - 0.5 * self.interconnect_layer_width, prechrg_control.cy())

        self.add_segment_center(self.interconnect_layer, prechrg_control.center(), end)

        start = end + vector(0.5 * self.interconnect_layer_width, 0)
        self.add_segment_center(self.interconnect_layer, start, decode_prechrg.center())

        
        

    def route_supplies(self):
        gnd_start = vector(self.array_inst.get_pins("gnd")[0].cx(),0)

        decode_gnd = self.decode_inst.get_pin("gnd")
        decode_vdd = self.decode_inst.get_pin("vdd")
        array_vdd = self.array_inst.get_pin("vdd")

        # self.add_segment_center("m1", gnd_start, decode_gnd.center())


        self.add_power_pin("gnd", decode_vdd.center())
        self.add_power_pin("vdd", decode_gnd.center())

        vdd_start = vector(array_vdd.lx() + 0.5 * self.via1_space, array_vdd.cy())
        end = vector(decode_vdd.lx(), vdd_start.y)

        self.add_segment_center(self.interconnect_layer, vdd_start, end)
        self.add_via_stack_center(vdd_start, "m1", self.interconnect_layer)

        vdd_start = vector(decode_vdd.cx(), vdd_start.y)

        self.add_segment_center(self.interconnect_layer, vdd_start, decode_vdd.center())

        


        



