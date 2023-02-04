
from math import ceil, log, sqrt
from openram.base import vector
from openram.base import design
from openram import OPTS, debug
from openram.sram_factory import factory
from openram.tech import drc, layer

class rom_base_bank(design):

    """
    Rom data bank with row and column decoder + control logic

    word size is in bytes
    """

    def __init__(self, strap_spacing=0, data_file=None, name="", word_size=2):
        super().__init__(name=name)
        self.word_size = word_size * 8
        self.read_binary(word_size=word_size, data_file=data_file)

        self.num_outputs = self.rows
        self.num_inputs = ceil(log(self.rows, 2))
        self.col_bits = ceil(log(self.words_per_row, 2))
        self.row_bits = self.num_inputs
        
        # self.data = [[0, 1, 0, 1], [1, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 0]]
        self.strap_spacing = strap_spacing
        self.tap_spacing = 8
        self.interconnect_layer = "m1"
        self.bitline_layer = "m1"
        self.wordline_layer = "m2"

        
        if "li" in layer:
            self.route_stack = self.m1_stack
        else:
            self.route_stack = self.m2_stack
        self.route_layer = self.route_stack[0]
        self.setup_layout_constants()
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()
    """
    Reads a hexadecimal file from a given directory to be used as the data written to the ROM
    endian is either "big" or "little"
    word_size is the number of bytes per word
    sets the row and column size based on the size of binary input, tries to keep array as square as possible, 
    """

    def read_binary(self, data_file, word_size=2, endian="big"):
        # Read data as hexidecimal text file
        hex_file = open(data_file, 'r')
        hex_data = hex_file.read()

        # Convert from hex into an int
        data_int = int(hex_data, 16)
        # Then from int into a right aligned, zero padded string
        bin_string = bin(data_int)[2:].zfill(len(hex_data) * 4)

        # Then turn the string into a list of ints
        bin_data = list(bin_string)
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
        debug.info(1, "Read rom binary: length {0} bytes, {1} words, set number of cols to {2}, rows to {3}, with {4} words per row".format(data_size, num_words, self.cols, self.rows, self.words_per_row))

        # print("hex: {0}, binary: {1}, chunked: {2}".format(hex_data, bin_data, chunked_data))

        
    def create_netlist(self):
        self.add_modules()
        self.add_pins()


        
    def create_layout(self):
        print("Creating ROM bank instances")
        self.create_instances()
        print("Placing ROM bank instances")
        self.place_instances()

        print("Routing decoders to array")
        self.route_decode_outputs()

        print("Routing precharge signal")
        self.route_precharge()

        print("Routing clock signal")
        self.route_clock()
        self.route_array_outputs()
        self.place_top_level_pins()
        self.route_supplies()
        self.route_output_buffers()
        self.height = self.array_inst.height
        self.width = self.array_inst.width
        self.add_boundary()


    def setup_layout_constants(self):
        self.route_layer_width = drc["minwidth_{}".format(self.route_stack[0])]
        self.route_layer_pitch = drc["{0}_to_{0}".format(self.route_stack[0])]

        self.interconnect_layer_width = drc["minwidth_{}".format(self.interconnect_layer)]
        self.interconnect_layer_pitch = drc["{0}_to_{0}".format(self.interconnect_layer)]

    def add_pins(self):
        
        self.add_pin("clk", "INPUT")
        self.add_pin("CS", "INPUT")

        for i in range(self.row_bits + self.col_bits):
            self.add_pin("addr_{}".format(i), "INPUT")

        out_pins = []
        for j in range(self.word_size):
            out_pins.append("rom_out_{}".format(j))
        self.add_pin_list(out_pins, "OUTPUT")

        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")


    def add_modules(self):

        print("Creating bank modules")
        self.array = factory.create(module_type="rom_base_array", 
                                    cols=self.cols, 
                                    rows=self.rows, 
                                    strap_spacing=self.strap_spacing, 
                                    bitmap=self.data, 
                                    bitline_layer=self.bitline_layer,
                                    wordline_layer=self.wordline_layer,
                                    pitch_match=True,
                                    tap_spacing=self.tap_spacing) 
        
        
        self.decode_array = factory.create(module_name="rom_row_decode", 
                                           module_type="rom_decoder", 
                                           num_outputs=self.rows, 
                                           strap_spacing=self.strap_spacing, 
                                           route_layer=self.route_layer, 
                                           cols=self.cols)

        
        self.column_mux = factory.create(module_type="rom_column_mux_array", 
                                         columns=self.cols,
                                         word_size=self.word_size,
                                         tap_spacing=self.strap_spacing,
                                         bitline_layer=self.interconnect_layer,
                                         input_layer=self.bitline_layer)
        
        self.column_decode = factory.create(module_name="rom_column_decode",
                                            module_type="rom_decoder", 
                                            num_outputs=self.words_per_row, 
                                            strap_spacing=self.strap_spacing, 
                                            route_layer=self.route_layer, 
                                            cols=1,
                                            invert_outputs=True )

        self.control_logic = factory.create(module_type="rom_control_logic", 
                                            num_outputs=(self.rows + self.cols + self.words_per_row) * 0.5, 
                                            clk_fanout=(self.col_bits + self.row_bits) * 2,
                                            height=self.column_decode.height )
        
        self.output_buffer = factory.create(module_type="rom_wordline_driver_array",
                                            module_name="rom_output_buffer",
                                            rows=self.word_size,
                                            cols=4)


    def create_instances(self):
        gnd = ["gnd"]
        vdd = ["vdd"]
        prechrg = ["precharge"]
        clk = ["clk_int"]

        bitlines = ["bl_{}".format(bl) for bl in range(self.cols)]
        wordlines = ["wl_{}".format(wl) for wl in range(self.rows)]

        addr_msb = ["addr_{}".format(addr + self.col_bits) for addr in range(self.row_bits)]
        addr_lsb = ["addr_{}".format(addr) for addr in range(self.col_bits)]

        select_lines = ["word_sel_{}".format(word) for word in range(self.words_per_row)]

        pre_buf_outputs = ["rom_out_prebuf_{}".format(bit) for bit in range(self.word_size)]
        outputs = ["rom_out_{}".format(bl) for bl in range(self.word_size)]
    

        array_pins = bitlines + wordlines + prechrg + vdd + gnd

        row_decode_pins = addr_msb + wordlines + prechrg + clk + vdd + gnd
        col_decode_pins = addr_lsb + select_lines + prechrg + clk + vdd + gnd

        col_mux_pins = bitlines + select_lines + pre_buf_outputs + gnd

        output_buffer_pins = pre_buf_outputs + outputs + vdd + gnd

        self.array_inst = self.add_inst(name="rom_bit_array", mod=self.array)
        self.connect_inst(array_pins)

        self.decode_inst = self.add_inst(name="rom_row_decoder", mod=self.decode_array)
        self.connect_inst(row_decode_pins)

        self.control_inst = self.add_inst(name="rom_control", mod=self.control_logic)
        self.connect_inst(["clk", "CS", "precharge", "clk_int", "vdd", "gnd"])

        self.mux_inst = self.add_inst(name="rom_column_mux", mod=self.column_mux)
        self.connect_inst(col_mux_pins)

        self.col_decode_inst = self.add_inst(name="rom_column_decoder", mod=self.column_decode)
        self.connect_inst(col_decode_pins)

        self.output_buf_inst = self.add_inst(name="rom_output_buffer", mod=self.output_buffer)
        self.connect_inst(output_buffer_pins)


        
    def place_instances(self):
        self.place_row_decoder()
        self.place_data_array()
        self.place_col_mux()
        self.place_col_decoder()
        self.place_control_logic()
        self.place_output_buffer()


    def place_row_decoder(self):
        self.decode_offset = vector(0, self.control_inst.height - self.decode_array.control_array.height)
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


        self.control_offset = vector(self.control_inst.width + self.decode_array.control_array.width + 2 * (self.route_layer_pitch + self.route_layer_width), self.col_decode_inst.by() + self.control_logic.height)
        self.control_inst.place(offset=self.control_offset, mirror="XY")

    def place_col_decoder(self):
        col_decode_y = self.mux_inst.get_pin("sel_0").cy() - self.col_decode_inst.get_pin("wl_0").cy() 
        self.col_decode_offset = vector(self.decode_inst.width - self.col_decode_inst.width, col_decode_y)
        self.col_decode_inst.place(offset=self.col_decode_offset)

    def place_col_mux(self):
        mux_y_offset = self.array_inst.by() - self.mux_inst.height - 5 * self.route_layer_pitch

        mux_x_offset = self.array_inst.get_pin("bl_0_0").cx() - self.mux_inst.get_pin("bl_0").cx()
        self.mux_offset = vector(mux_x_offset, mux_y_offset)
        self.mux_inst.place(offset=self.mux_offset)
        
    def place_output_buffer(self):
        output_x = self.col_decode_inst.rx() + self.output_buf_inst.height 
        output_y = self.col_decode_inst.by() + self.output_buf_inst.width
        self.output_buf_offset = vector(output_x, output_y)
        self.output_buf_inst.place(offset=self.output_buf_offset, rotate=270)
        
    # def create_wl_bus(self):
    #     bus_x = self.decode_inst.width + ( drc["minwidth_{}".format(self.bus_layer)] + 1.5 * drc["{0}_to_{0}".format(self.bus_layer)] )
    #     bus_y = self.array_inst.by() + self.bus_layer_pitch + self.bus_layer_width
    #     self.wl_interconnects = []

    #     for wl in range(self.rows):
    #         self.wl_interconnects.append("wl_interconnect_{}".format(wl))
        
    #     self.wl_bus = self.create_vertical_bus(self.bus_layer, vector(bus_x, bus_y), self.wl_interconnects, self.decode_inst.uy() - self.array_inst.by() )

    def route_decode_outputs(self):
        # for the row decoder
        route_pins = [self.array_inst.get_pin("wl_0_{}".format(wl)) for wl in range(self.rows)]
        decode_pins = [self.decode_inst.get_pin("wl_{}".format(wl)) for wl in range(self.rows)]
        route_pins.extend(decode_pins)
        self.connect_row_pins(self.interconnect_layer, route_pins, round=True)


        # then for the column decoder
        col_decode_pins = [self.col_decode_inst.get_pin("wl_{}".format(wl)) for wl in range(self.words_per_row)]
        sel_pins = [self.mux_inst.get_pin("sel_{}".format(wl)) for wl in range(self.words_per_row)]
        sel_pins.extend(col_decode_pins)
        self.connect_row_pins(self.wordline_layer, sel_pins, round=True)



    def route_array_inputs(self):

        for wl in range(self.rows):
            array_wl = self.array.wordline_names[0][wl]
            array_wl_pin = self.array_inst.get_pin(array_wl)

            wl_bus_wire = self.wl_bus[self.wl_interconnects[wl]]

            end = array_wl_pin.center()
            start = vector(wl_bus_wire.cx(), end.y)

            self.add_segment_center(self.interconnect_layer, start, end)
            self.add_via_stack_center(start, self.route_layer, self.interconnect_layer )

        
    def route_precharge(self):

        prechrg_control = self.control_inst.get_pin("prechrg")
        row_decode_prechrg = self.decode_inst.get_pin("precharge")
        col_decode_prechrg = self.col_decode_inst.get_pin("precharge")
        array_prechrg = self.array_inst.get_pin("precharge")


        # Route precharge signal to the row decoder
        end = vector(row_decode_prechrg.cx() - 0.5 * self.interconnect_layer_width, prechrg_control.cy())

        self.add_segment_center(self.interconnect_layer, prechrg_control.center(), end)

        start = end + vector(0.5 * self.interconnect_layer_width, 0)
        self.add_segment_center(self.interconnect_layer, start, row_decode_prechrg.center())

        self.add_via_stack_center(from_layer=self.route_stack[0],
                                  to_layer=prechrg_control.layer,
                                  offset=prechrg_control.center())

        # Route precharge to col decoder
        start = row_decode_prechrg.center() - vector(0, self.route_layer_pitch + 2 * self.route_layer_width)
        mid = vector(col_decode_prechrg.cx(), start.y)
        end = vector(col_decode_prechrg.cx(), 0.5 * (self.col_decode_inst.uy() + mid.y) )
        self.add_path(self.route_stack[0], [start, mid, end])

        self.add_via_stack_center(from_layer=self.route_stack[0],
                                  to_layer=col_decode_prechrg.layer,
                                  offset=end)
        self.add_segment_center(col_decode_prechrg.layer, end, col_decode_prechrg.center())     

        # Route precharge to main array
        end = vector(col_decode_prechrg.cx(), array_prechrg.cy())
        self.add_segment_center(self.route_stack[0], array_prechrg.center(), end) 


    def route_clock(self):
        clk_out = self.control_inst.get_pin("clk_out")
        row_decode_clk = self.decode_inst.get_pin("clk")
        col_decode_clk = self.col_decode_inst.get_pin("clk")
        self.add_via_stack_center(from_layer=self.route_stack[2],
                                  to_layer=clk_out.layer,
                                  offset=clk_out.center())
        
        # Route clock to row decoder 
        end = row_decode_clk.rc() + vector( 2 * self.route_layer_pitch + self.route_layer_width, 0)
        self.add_path(self.route_stack[2], [clk_out.center(), end])

        self.add_via_stack_center(from_layer=self.route_stack[2],
                                  to_layer=row_decode_clk.layer,
                                  offset=end)

        self.add_segment_center(row_decode_clk.layer, end, row_decode_clk.rc())

        # Route clock to column decoder
        end = col_decode_clk.lc() - vector( 2 * self.route_layer_pitch + self.route_layer_width, 0)
        self.add_path(self.route_stack[2], [clk_out.center(), end])

        self.add_via_stack_center(from_layer=self.route_stack[2],
                                  to_layer=row_decode_clk.layer,
                                  offset=end)

        self.add_segment_center(col_decode_clk.layer, end, col_decode_clk.lc())




    def route_array_outputs(self):
        for i in range(self.cols):
            bl_out = self.array_inst.get_pin("bl_0_{}".format(i)).center()

            bl_mux = self.mux_inst.get_pin("bl_{}".format(i)).center()

            self.add_path(self.array.bitline_layer, [bl_out, bl_mux])


    def route_output_buffers(self):
        mux = self.mux_inst
        buf = self.output_buf_inst
        route_nets = [ [mux.get_pin("bl_out_{}".format(bit)), buf.get_pin("in_{}".format(bit))] for bit in range(self.word_size)]

        channel_ll = vector( route_nets[0][0].cx(), route_nets[0][1].cy() + self.m1_pitch * 3)
        self.create_horizontal_channel_route(netlist=route_nets, offset=channel_ll, layer_stack=self.m1_stack)
        # for bit in range(self.word_size):
        #     mux_pin = self.mux_inst.get_pin("bl_out_{}".format(bit))
        #     buf_pin = self.output_buf_inst.get_pin("in_{}".format(bit))
        #     mux_out = vector(mux_pin.cx(), mux_pin.by())
        #     buf_in = buf_pin.center()

        #     mid1 = vector(mux_out.x, buf_in.y + bit * self.m2_pitch)
        #     mid2 = vector(buf_in.x, mid1.y)
        #     print("start: {0}, mid: {1}, stop: {2}".format(mux_out, mid1, buf_in))
        #     self.add_path(layer="m2", coordinates=[mux_out, mid1, mid2, buf_in])


            
    def place_top_level_pins(self):
        self.copy_layout_pin(self.control_inst, "CS")
        self.copy_layout_pin(self.control_inst, "clk_in", "clk")

        for i in range(self.word_size):
            self.copy_layout_pin(self.output_buf_inst, "out_{}".format(i), "rom_out_{}".format(i))
        for lsb in range(self.col_bits):
            name = "addr_{}".format(lsb)
            self.copy_layout_pin(self.col_decode_inst, "A{}".format(lsb), name)

        for msb in range(self.col_bits, self.row_bits + self.col_bits):
            name = "addr_{}".format(msb)
            pin_num = msb - self.col_bits            
            self.copy_layout_pin(self.decode_inst, "A{}".format(pin_num), name)
            
        


    def route_supplies(self):

        for inst in self.insts:
            if not inst.mod.name.__contains__("contact"):
                self.copy_layout_pin(inst, "vdd")
                self.copy_layout_pin(inst, "gnd")
        # gnd_start = vector(self.array_inst.get_pins("gnd")[0].cx(),0)

        # decode_gnd = self.decode_inst.get_pin("gnd")
        # decode_vdd = self.decode_inst.get_pin("vdd")
        # array_vdd = self.array_inst.get_pin("vdd")

        # # self.add_segment_center("m1", gnd_start, decode_gnd.center())


        # self.add_power_pin("gnd", decode_vdd.center())
        # self.add_power_pin("vdd", decode_gnd.center())

        # vdd_start = vector(array_vdd.lx() + 0.5 * self.via1_space, array_vdd.cy())
        # end = vector(decode_vdd.lx(), vdd_start.y)

        # self.add_segment_center(self.interconnect_layer, vdd_start, end)
        # self.add_via_stack_center(vdd_start, "m1", self.interconnect_layer)

        # vdd_start = vector(decode_vdd.cx(), vdd_start.y)

        # self.add_segment_center(self.interconnect_layer, vdd_start, decode_vdd.center())

        


        



