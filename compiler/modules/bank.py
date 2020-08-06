# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import design
from sram_factory import factory
from math import log, ceil
from tech import drc, layer
from vector import vector
from globals import OPTS


class bank(design.design):
    """
    Dynamically generated a single bank including bitcell array,
    hierarchical_decoder, precharge, (optional column_mux and column decoder),
    write driver and sense amplifiers.
    This can create up to two ports in any combination: rw, w, r.
    """

    def __init__(self, sram_config, name=""):

        self.sram_config = sram_config
        sram_config.set_local_config(self)
        if self.write_size:
            self.num_wmasks = int(self.word_size / self.write_size)
        else:
            self.num_wmasks = 0
        
        if not self.num_spare_cols:
            self.num_spare_cols = 0
                
        if name == "":
            name = "bank_{0}_{1}".format(self.word_size, self.num_words)
        super().__init__(name)
        debug.info(2, "create sram of size {0} with {1} words".format(self.word_size,
                                                                      self.num_words))
        
        # The local control signals are gated when we have bank select logic,
        # so this prefix will be added to all of the input signals to create
        # the internal gated signals.
        if self.num_banks>1:
            self.prefix="gated_"
        else:
            self.prefix=""

        self.create_netlist()
        if not OPTS.netlist_only:
            debug.check(len(self.all_ports)<=2,
                        "Bank layout cannot handle more than two ports.")
            self.create_layout()
            self.add_boundary()

    def create_netlist(self):

        self.compute_sizes()
        self.add_modules()
        self.add_pins() # Must create the replica bitcell array first
        self.create_instances()
        
    def create_layout(self):
        self.place_instances()
        self.setup_routing_constraints()
        self.route_layout()
        
        # Can remove the following, but it helps for debug!
        # self.add_lvs_correspondence_points()

        # Remember the bank center for further placement
        self.bank_array_ll = self.offset_all_coordinates().scale(-1, -1)
        self.bank_array_ur = self.bitcell_array_inst.ur()
        self.bank_array_ul = self.bitcell_array_inst.ul()

        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for Bank module"""
        for port in self.read_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("dout{0}_{1}".format(port, bit), "OUTPUT")
        for port in self.all_ports:
            self.add_pin(self.bitcell_array.get_rbl_bl_name(self.port_rbl_map[port]), "OUTPUT")
        for port in self.write_ports:
            for bit in range(self.word_size + self.num_spare_cols):
                self.add_pin("din{0}_{1}".format(port, bit), "INPUT")
        for port in self.all_ports:
            for bit in range(self.addr_size):
                self.add_pin("addr{0}_{1}".format(port, bit), "INPUT")

        # For more than one bank, we have a bank select and name
        # the signals gated_*.
        if self.num_banks > 1:
            for port in self.all_ports:
                self.add_pin("bank_sel{}".format(port), "INPUT")
        for port in self.read_ports:
            self.add_pin("s_en{0}".format(port), "INPUT")
        for port in self.all_ports:
            self.add_pin("p_en_bar{0}".format(port), "INPUT")
        for port in self.write_ports:
            self.add_pin("w_en{0}".format(port), "INPUT")
            for bit in range(self.num_wmasks):
                self.add_pin("bank_wmask{0}_{1}".format(port, bit), "INPUT")
            for bit in range(self.num_spare_cols):
                self.add_pin("bank_spare_wen{0}_{1}".format(port, bit), "INPUT")
        for port in self.all_ports:
            self.add_pin("wl_en{0}".format(port), "INPUT")
        self.add_pin("vdd", "POWER")
        self.add_pin("gnd", "GROUND")
        
    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_central_bus()
        
        for port in self.all_ports:
            self.route_bitlines(port)
            self.route_rbl(port)
            self.route_port_address(port)
            self.route_column_address_lines(port)
            self.route_control_lines(port)
            if self.num_banks > 1:
                self.route_bank_select(port)
        
        self.route_supplies()

    def route_rbl(self, port):
        """ Route the rbl_bl and rbl_wl """

        # Connect the rbl to the port data pin
        bl_pin = self.port_data_inst[port].get_pin("rbl_bl")
        if port % 2:
            pin_pos = bl_pin.uc()
            pin_offset = pin_pos + vector(0, self.m3_pitch)
            left_right_offset = vector(self.max_x_offset, pin_offset.y)
        else:
            pin_pos = bl_pin.bc()
            pin_offset = pin_pos - vector(0, self.m3_pitch)
            left_right_offset = vector(self.min_x_offset, pin_offset.y)
        self.add_via_stack_center(from_layer=bl_pin.layer,
                                  to_layer="m3",
                                  offset=pin_offset)
        self.add_path(bl_pin.layer, [pin_offset, pin_pos])
        self.add_layout_pin_segment_center(text="rbl_bl{0}".format(port),
                                           layer="m3",
                                           start=left_right_offset,
                                           end=pin_offset)
            
    def route_bitlines(self, port):
        """ Route the bitlines depending on the port type rw, w, or r. """

        if port in self.write_ports:
            self.route_port_data_in(port)
        if port in self.read_ports:
            self.route_port_data_out(port)
        self.route_port_data_to_bitcell_array(port)
        
    def create_instances(self):
        """ Create the instances of the netlist. """

        self.create_bitcell_array()
        self.create_port_data()
        self.create_port_address()
        self.create_column_decoder()
        self.create_bank_select()

    def compute_instance_offsets(self):
        """
        Compute the empty instance offsets for port0 and port1 (if needed)
        """

        self.port_data_offsets = [None] * len(self.all_ports)
        self.port_address_offsets = [None] * len(self.all_ports)

        self.column_decoder_offsets = [None] * len(self.all_ports)
        self.bank_select_offsets = [None] * len(self.all_ports)

        # The center point for these cells are the upper-right corner of
        # the bitcell array.
        # The port address decoder/driver logic is placed on the right and mirrored on Y-axis.
        # The port data write/sense/precharge/mux is placed on the top and mirrored on the X-axis.
        self.bitcell_array_top = self.bitcell_array.height
        self.bitcell_array_right = self.bitcell_array.width
        
        # These are the offsets of the main array (excluding dummy and replica rows/cols)
        self.main_bitcell_array_top = self.bitcell_array.bitcell_array_inst.uy()
        # Just past the dummy column
        self.main_bitcell_array_left = self.bitcell_array.bitcell_array_inst.lx()
        # Just past the dummy row and replica row
        self.main_bitcell_array_bottom = self.bitcell_array.bitcell_array_inst.by()
        
        self.compute_instance_port0_offsets()
        if len(self.all_ports)==2:
            self.compute_instance_port1_offsets()
        
    def compute_instance_port0_offsets(self):
        """
        Compute the instance offsets for port0 on the left/bottom of the bank.
        """

        port = 0
        
        # UPPER RIGHT QUADRANT
        # Bitcell array is placed at (0,0)
        self.bitcell_array_offset = vector(0, 0)

        # LOWER RIGHT QUADRANT
        # Below the bitcell array
        self.port_data_offsets[port] = vector(self.main_bitcell_array_left - self.bitcell_array.cell.width, 0)

        # UPPER LEFT QUADRANT
        # To the left of the bitcell array above the predecoders and control logic
        x_offset = self.m2_gap + self.port_address.width
        self.port_address_offsets[port] = vector(-x_offset,
                                                 self.main_bitcell_array_bottom)
        self.predecoder_height = self.port_address.predecoder_height + self.port_address_offsets[port].y

        # LOWER LEFT QUADRANT
        # Place the col decoder left aligned with wordline driver
        # This is also placed so that it's supply rails do not align with the SRAM-level
        # control logic to allow control signals to easily pass over in M3
        # by placing 1 1/4 a cell pitch down because both power connections and inputs/outputs
        # may be routed in M3 or M4
        x_offset = self.central_bus_width[port] + self.port_address.wordline_driver.width
        if self.col_addr_size > 0:
            x_offset += self.column_decoder.width + self.col_addr_bus_width
            y_offset = 1.25 * self.dff.height + self.column_decoder.height
        else:
            y_offset = 0
        self.column_decoder_offsets[port] = vector(-x_offset, -y_offset)

        # Bank select gets placed below the column decoder (x_offset doesn't change)
        if self.col_addr_size > 0:
            y_offset = min(self.column_decoder_offsets[port].y, self.port_data[port].column_mux_offset.y)
        else:
            y_offset = self.port_address_offsets[port].y
        if self.num_banks > 1:
            y_offset += self.bank_select.height + drc("well_to_well")
        self.bank_select_offsets[port] = vector(-x_offset, -y_offset)

    def compute_instance_port1_offsets(self):
        """
        Compute the instance offsets for port1 on the right/top of the bank.
        """

        port=1
        
        # LOWER LEFT QUADRANT
        # Bitcell array is placed at (0,0)

        # UPPER LEFT QUADRANT
        # Above the bitcell array
        self.port_data_offsets[port] = vector(self.main_bitcell_array_left, self.bitcell_array_top)
            
        # LOWER RIGHT QUADRANT
        # To the left of the bitcell array
        x_offset = self.bitcell_array_right + self.port_address.width + self.m2_gap
        self.port_address_offsets[port] = vector(x_offset,
                                                 self.main_bitcell_array_bottom)

        # UPPER RIGHT QUADRANT
        # Place the col decoder right aligned with wordline driver
        # Above the bitcell array with a well spacing
        # This is also placed so that it's supply rails do not align with the SRAM-level
        # control logic to allow control signals to easily pass over in M3
        # by placing 1 1/4 a cell pitch down because both power connections and inputs/outputs
        # may be routed in M3 or M4
        x_offset = self.bitcell_array_right  + self.central_bus_width[port] + self.port_address.wordline_driver.width
        if self.col_addr_size > 0:
            x_offset += self.column_decoder.width + self.col_addr_bus_width
            y_offset = self.bitcell_array_top + 1.25 * self.dff.height + self.column_decoder.height
        else:
            y_offset = self.bitcell_array_top
        self.column_decoder_offsets[port] = vector(x_offset, y_offset)

        # Bank select gets placed above the column decoder (x_offset doesn't change)
        if self.col_addr_size > 0:
            y_offset = max(self.column_decoder_offsets[port].y + self.column_decoder.height,
                           self.port_data[port].column_mux_offset.y + self.port_data[port].column_mux_array.height)
        else:
            y_offset = self.port_address_offsets[port].y
        self.bank_select_offsets[port] = vector(x_offset, y_offset)
        
    def place_instances(self):
        """ Place the instances. """

        self.compute_instance_offsets()
        
        self.place_bitcell_array(self.bitcell_array_offset)

        self.place_port_data(self.port_data_offsets)

        self.place_port_address(self.port_address_offsets)

        self.place_column_decoder(self.column_decoder_offsets)
        self.place_bank_select(self.bank_select_offsets)
 
    def compute_sizes(self):
        """  Computes the required sizes to create the bank """

        self.num_cols = int(self.words_per_row * self.word_size)
        self.num_rows_temp = int(self.num_words / self.words_per_row)
        self.num_rows = self.num_rows_temp + self.num_spare_rows

        self.row_addr_size = ceil(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.addr_size = self.col_addr_size + self.row_addr_size

        debug.check(self.num_rows_temp * self.num_cols==self.word_size * self.num_words,
                    "Invalid bank sizes.")
        debug.check(self.addr_size==self.col_addr_size + self.row_addr_size,
                    "Invalid address break down.")

        # The order of the control signals on the control bus:
        self.input_control_signals = []
        port_num = 0
        for port in range(OPTS.num_rw_ports):
            self.input_control_signals.append(["s_en{}".format(port_num), "w_en{}".format(port_num), "p_en_bar{}".format(port_num), "wl_en{}".format(port_num)])
            port_num += 1
        for port in range(OPTS.num_w_ports):
            self.input_control_signals.append(["w_en{}".format(port_num), "p_en_bar{}".format(port_num), "wl_en{}".format(port_num)])
            port_num += 1
        for port in range(OPTS.num_r_ports):
            self.input_control_signals.append(["s_en{}".format(port_num), "p_en_bar{}".format(port_num), "wl_en{}".format(port_num)])
            port_num += 1

        # Number of control lines in the bus for each port
        self.num_control_lines = [len(x) for x in self.input_control_signals]

        # The width of this bus is needed to place other modules (e.g. decoder) for each port
        self.central_bus_width = [self.m3_pitch * x + self.m3_width for x in self.num_control_lines]

        # These will be outputs of the gaters if this is multibank, if not, normal signals.
        self.control_signals = []
        for port in self.all_ports:
            if self.num_banks > 1:
                self.control_signals.append(["gated_" + str for str in self.input_control_signals[port]])
            else:
                self.control_signals.append(self.input_control_signals[port])
                    

        # The central bus is the column address (one hot) and row address (binary)
        if self.col_addr_size>0:
            self.num_col_addr_lines = 2**self.col_addr_size
        else:
            self.num_col_addr_lines = 0
        self.col_addr_bus_width = self.m2_pitch * self.num_col_addr_lines

        # A space for wells or jogging m2
        self.m2_gap = max(2 * drc("pwell_to_nwell") + drc("nwell_enclose_active"),
                          3 * self.m2_pitch)

    def add_modules(self):
        """ Add all the modules using the class loader """
        
        # create arrays of bitline and bitline_bar names for read, write, or all ports
        self.bitcell = factory.create(module_type="bitcell")
        self.bl_names = self.bitcell.get_all_bl_names()
        self.br_names = self.bitcell.get_all_br_names()
        self.wl_names = self.bitcell.get_all_wl_names()
        self.bitline_names = self.bitcell.get_all_bitline_names()

        self.port_data = []
        for port in self.all_ports:
            temp_pre = factory.create(module_type="port_data",
                                      sram_config=self.sram_config,
                                      port=port)
            self.port_data.append(temp_pre)
            self.add_mod(self.port_data[port])

        self.port_address = factory.create(module_type="port_address",
                                           cols=self.num_cols + self.num_spare_cols,
                                           rows=self.num_rows)
        self.add_mod(self.port_address)

        self.port_rbl_map = self.all_ports
        self.num_rbl = len(self.all_ports)
                
        self.bitcell_array = factory.create(module_type="replica_bitcell_array",
                                            cols=self.num_cols + self.num_spare_cols,
                                            rows=self.num_rows,
                                            left_rbl=1,
                                            right_rbl=1 if len(self.all_ports)>1 else 0,
                                            bitcell_ports=self.all_ports)
        self.add_mod(self.bitcell_array)

        if(self.num_banks > 1):
            self.bank_select = factory.create(module_type="bank_select")
            self.add_mod(self.bank_select)
        
    def create_bitcell_array(self):
        """ Creating Bitcell Array """

        self.bitcell_array_inst=self.add_inst(name="replica_bitcell_array",
                                              mod=self.bitcell_array)
                    
        temp = []
        for col in range(self.num_cols + self.num_spare_cols):
            for bitline in self.bitline_names:
                temp.append("{0}_{1}".format(bitline, col))
        for rbl in range(self.num_rbl):
            rbl_bl_name=self.bitcell_array.get_rbl_bl_name(rbl)
            temp.append(rbl_bl_name)
            rbl_br_name=self.bitcell_array.get_rbl_br_name(rbl)
            temp.append(rbl_br_name)
        for row in range(self.num_rows):
            for wordline in self.wl_names:
                temp.append("{0}_{1}".format(wordline, row))
        for port in self.all_ports:
            temp.append("wl_en{0}".format(port))
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)
        
    def place_bitcell_array(self, offset):
        """ Placing Bitcell Array """
        self.bitcell_array_inst.place(offset)

    def create_port_data(self):
        """ Creating Port Data """

        self.port_data_inst = [None] * len(self.all_ports)
        for port in self.all_ports:
            self.port_data_inst[port]=self.add_inst(name="port_data{}".format(port),
                                                    mod=self.port_data[port])

            temp = []
            rbl_bl_name=self.bitcell_array.get_rbl_bl_name(self.port_rbl_map[port])
            rbl_br_name=self.bitcell_array.get_rbl_br_name(self.port_rbl_map[port])
            temp.append(rbl_bl_name)
            temp.append(rbl_br_name)
            for col in range(self.num_cols + self.num_spare_cols):
                temp.append("{0}_{1}".format(self.bl_names[port], col))
                temp.append("{0}_{1}".format(self.br_names[port], col))
            if port in self.read_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    temp.append("dout{0}_{1}".format(port, bit))
            if port in self.write_ports:
                for bit in range(self.word_size + self.num_spare_cols):
                    temp.append("din{0}_{1}".format(port, bit))
            # Will be empty if no col addr lines
            sel_names = ["sel{0}_{1}".format(port, x) for x in range(self.num_col_addr_lines)]
            temp.extend(sel_names)
            if port in self.read_ports:
                temp.append("s_en{0}".format(port))
            temp.append("p_en_bar{0}".format(port))
            if port in self.write_ports:
                temp.append("w_en{0}".format(port))
                for bit in range(self.num_wmasks):
                    temp.append("bank_wmask{0}_{1}".format(port, bit))
                for bit in range(self.num_spare_cols):
                    temp.append("bank_spare_wen{0}_{1}".format(port, bit))
            temp.extend(["vdd", "gnd"])
            
            self.connect_inst(temp)

    def place_port_data(self, offsets):
        """ Placing Port Data """
        
        for port in self.all_ports:
            # Top one is unflipped, bottom is flipped along X direction
            if port % 2 == 1:
                mirror = "R0"
            else:
                mirror = "MX"
            self.port_data_inst[port].place(offset=offsets[port], mirror=mirror)

    def create_port_address(self):
        """  Create the hierarchical row decoder  """
        
        self.port_address_inst = [None] * len(self.all_ports)
        for port in self.all_ports:
            self.port_address_inst[port] = self.add_inst(name="port_address{}".format(port),
                                                         mod=self.port_address)

            temp = []
            for bit in range(self.row_addr_size):
                temp.append("addr{0}_{1}".format(port, bit + self.col_addr_size))
            temp.append("wl_en{0}".format(port))
            for row in range(self.num_rows):
                temp.append("{0}_{1}".format(self.wl_names[port], row))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)
            
    def place_port_address(self, offsets):
        """  Place the hierarchical row decoder  """

        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place row decoder array.")
        
        # The address and control bus will be in between decoder and the main memory array
        # This bus will route address bits to the decoder input and column mux inputs.
        # The wires are actually routed after we placed the stuff on both sides.
        # The predecoder is below the x-axis and the main decoder is above the x-axis
        # The address flop and decoder are aligned in the x coord.
        
        for port in self.all_ports:
            if port % 2:
                mirror = "MY"
            else:
                mirror = "R0"
            self.port_address_inst[port].place(offset=offsets[port], mirror=mirror)
        
    def create_column_decoder(self):
        """
        Create a 2:4 or 3:8 column address decoder.
        """

        self.dff =factory.create(module_type="dff")
        
        if self.col_addr_size == 0:
            return
        elif self.col_addr_size == 1:
            self.column_decoder = factory.create(module_type="pinvbuf",
                                                 height=self.dff.height)
        elif self.col_addr_size == 2:
            self.column_decoder = factory.create(module_type="hierarchical_predecode2x4",
                                                 height=self.dff.height)

        elif self.col_addr_size == 3:
            self.column_decoder = factory.create(module_type="hierarchical_predecode3x8",
                                                 height=self.dff.height)
        else:
            # No error checking before?
            debug.error("Invalid column decoder?", -1)
        self.add_mod(self.column_decoder)
            
        self.column_decoder_inst = [None] * len(self.all_ports)
        for port in self.all_ports:
            self.column_decoder_inst[port] = self.add_inst(name="col_address_decoder{}".format(port),
                                                           mod=self.column_decoder)

            temp = []
            for bit in range(self.col_addr_size):
                temp.append("addr{0}_{1}".format(port, bit))
            for bit in range(self.num_col_addr_lines):
                temp.append("sel{0}_{1}".format(port, bit))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)
            
    def place_column_decoder(self, offsets):
        """
        Place a 2:4 or 3:8 column address decoder.
        """
        if self.col_addr_size == 0:
            return
        
        debug.check(len(offsets)>=len(self.all_ports),
                    "Insufficient offsets to place column decoder.")

        for port in self.all_ports:
            if port % 2 == 1:
                mirror = "XY"
            else:
                mirror = "R0"
            self.column_decoder_inst[port].place(offset=offsets[port], mirror=mirror)
            
    def create_bank_select(self):
        """ Create the bank select logic. """

        if not self.num_banks > 1:
            return

        self.bank_select_inst = [None] * len(self.all_ports)
        for port in self.all_ports:
            self.bank_select_inst[port] = self.add_inst(name="bank_select{}".format(port),
                                                        mod=self.bank_select)
            
            temp = []
            temp.extend(self.input_control_signals[port])
            temp.append("bank_sel{}".format(port))
            temp.extend(self.control_signals[port])
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)

    def place_bank_select(self, offsets):
        """ Place the bank select logic. """

        if not self.num_banks > 1:
            return

        debug.check(len(offsets)>=len(self.all_ports),
                    "Insufficient offsets to place bank select logic.")

        for port in self.all_ports:
            self.bank_select_inst[port].place(offsets[port])
        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        # Copy only the power pins already on the power layer
        # (this won't add vias to internal bitcell pins, for example)
        for inst in self.insts:
            self.copy_power_pins(inst, "vdd", add_vias=False)
            self.copy_power_pins(inst, "gnd", add_vias=False)

        # If we use the pinvbuf as the decoder, we need to add power pins.
        # Other decoders already have them.
        if self.col_addr_size == 1:
            for port in self.all_ports:
                inst = self.column_decoder_inst[port]
                for pin_name in ["vdd", "gnd"]:
                    pin_list = inst.get_pins(pin_name)
                    for pin in pin_list:
                        self.add_power_pin(pin_name,
                                           pin.center(),
                                           start_layer=pin.layer)

    def route_bank_select(self, port):
        """ Route the bank select logic. """
        
        if self.port_id[port] == "rw":
            bank_sel_signals = ["clk_buf", "w_en", "s_en", "p_en_bar", "bank_sel"]
            gated_bank_sel_signals = ["gated_clk_buf", "gated_w_en", "gated_s_en", "gated_p_en_bar"]
        elif self.port_id[port] == "w":
            bank_sel_signals = ["clk_buf", "w_en", "p_en_bar", "bank_sel"]
            gated_bank_sel_signals = ["gated_clk_buf", "gated_w_en", "gated_p_en_bar"]
        else:
            bank_sel_signals = ["clk_buf", "s_en", "p_en_bar", "bank_sel"]
            gated_bank_sel_signals = ["gated_clk_buf", "gated_s_en", "gated_p_en_bar"]
        
        copy_control_signals = self.input_control_signals[port] + ["bank_sel{}".format(port)]
        for signal in range(len(copy_control_signals)):
            self.copy_layout_pin(self.bank_select_inst[port], bank_sel_signals[signal], copy_control_signals[signal])
    
        for signal in range(len(gated_bank_sel_signals)):
            # Connect the inverter output to the central bus
            out_pos = self.bank_select_inst[port].get_pin(gated_bank_sel_signals[signal]).rc()
            name = self.control_signals[port][signal]
            bus_pos = vector(self.bus_pins[port][name].cx(), out_pos.y)
            self.add_path("m3", [out_pos, bus_pos])
            self.add_via_center(layers=self.m2_stack,
                                offset=bus_pos)
            self.add_via_center(layers=self.m1_stack,
                                offset=out_pos)
            self.add_via_center(layers=self.m2_stack,
                                offset=out_pos)
    
    def setup_routing_constraints(self):
        """
        After the modules are instantiated, find the dimensions for the
        control bus, power ring, etc.
        """

        self.max_y_offset = max([x.uy() for x in self.insts]) + 3 * self.m1_width
        self.min_y_offset = min([x.by() for x in self.insts])
        
        self.max_x_offset = max([x.rx() for x in self.insts]) + 3 * self.m1_width
        self.min_x_offset = min([x.lx() for x in self.insts])

        # # Create the core bbox for the power rings
        ur = vector(self.max_x_offset, self.max_y_offset)
        ll = vector(self.min_x_offset, self.min_y_offset)
        self.core_bbox = [ll, ur]
        
        self.height = ur.y - ll.y
        self.width = ur.x - ll.x

    def route_central_bus(self):
        """ Create the address, supply, and control signal central bus lines. """

        # Overall central bus width. It includes all the column mux lines,
        # and control lines.

        self.bus_pins = [None] * len(self.all_ports)
        # Port 0
        # The bank is at (0,0), so this is to the left of the y-axis.
        # 2 pitches on the right for vias/jogs to access the inputs
        control_bus_offset = vector(-self.m3_pitch * self.num_control_lines[0] - self.m3_pitch, self.min_y_offset)
        # The control bus is routed up to two pitches below the bitcell array
        control_bus_length = self.main_bitcell_array_bottom - self.min_y_offset - 2 * self.m1_pitch
        self.bus_pins[0] = self.create_bus(layer="m2",
                                           offset=control_bus_offset,
                                           names=self.control_signals[0],
                                           length=control_bus_length,
                                           vertical=True,
                                           make_pins=(self.num_banks==1),
                                           pitch=self.m3_pitch)
        
        # Port 1
        if len(self.all_ports)==2:
            # The other control bus is routed up to two pitches above the bitcell array
            control_bus_length = self.max_y_offset - self.main_bitcell_array_top - 2 * self.m1_pitch
            control_bus_offset = vector(self.bitcell_array_right + self.m3_pitch,
                                        self.max_y_offset - control_bus_length)
            # The bus for the right port is reversed so that the rbl_wl is closest to the array
            self.bus_pins[1] = self.create_bus(layer="m2",
                                               offset=control_bus_offset,
                                               names=list(reversed(self.control_signals[1])),
                                               length=control_bus_length,
                                               vertical=True,
                                               make_pins=(self.num_banks==1),
                                               pitch=self.m3_pitch)

    def route_port_data_to_bitcell_array(self, port):
        """ Routing of BL and BR between port data and bitcell array """

        # Connect the regular bitlines
        inst2 = self.port_data_inst[port]
        inst1 = self.bitcell_array_inst
        inst1_bl_name = self.bl_names[port] + "_{}"
        inst1_br_name = self.br_names[port] + "_{}"

        inst2_bl_name = inst2.mod.get_bl_names() + "_{}"
        inst2_br_name = inst2.mod.get_br_names() + "_{}"
        
        self.connect_bitlines(inst1=inst1,
                              inst2=inst2,
                              num_bits=self.num_cols,
                              inst1_bl_name=inst1_bl_name,
                              inst1_br_name=inst1_br_name,
                              inst2_bl_name=inst2_bl_name,
                              inst2_br_name=inst2_br_name)
        
        # connect spare bitlines
        for i in range(self.num_spare_cols):
            self.connect_bitline(inst1, inst2, inst1_bl_name.format(self.num_cols+i), "spare" + inst2_bl_name.format(i))
            self.connect_bitline(inst1, inst2, inst1_br_name.format(self.num_cols+i), "spare" + inst2_br_name.format(i))

        # Connect the replica bitlines
        rbl_bl_name=self.bitcell_array.get_rbl_bl_name(self.port_rbl_map[port])
        rbl_br_name=self.bitcell_array.get_rbl_br_name(self.port_rbl_map[port])
        self.connect_bitline(inst1, inst2, rbl_bl_name, "rbl_bl")
        self.connect_bitline(inst1, inst2, rbl_br_name, "rbl_br")
        
    def route_port_data_out(self, port):
        """ Add pins for the port data out """

        for bit in range(self.word_size + self.num_spare_cols):
            data_pin = self.port_data_inst[port].get_pin("dout_{0}".format(bit))
            self.add_layout_pin_rect_center(text="dout{0}_{1}".format(port, bit),
                                            layer=data_pin.layer,
                                            offset=data_pin.center(),
                                            height=data_pin.height(),
                                            width=data_pin.width())
                
    def route_port_address_in(self, port):
        """ Routes the row decoder inputs and supplies """

        # Create inputs for the row address lines
        for row in range(self.row_addr_size):
            addr_idx = row + self.col_addr_size
            decoder_name = "addr_{}".format(row)
            addr_name = "addr{0}_{1}".format(port, addr_idx)
            self.copy_layout_pin(self.port_address_inst[port], decoder_name, addr_name)

    def route_port_data_in(self, port):
        """ Connecting port data in   """

        for row in range(self.word_size + self.num_spare_cols):
            data_name = "din_{}".format(row)
            din_name = "din{0}_{1}".format(port, row)
            self.copy_layout_pin(self.port_data_inst[port], data_name, din_name)

        if self.write_size:
            for row in range(self.num_wmasks):
                wmask_name = "bank_wmask_{}".format(row)
                bank_wmask_name = "bank_wmask{0}_{1}".format(port, row)
                self.copy_layout_pin(self.port_data_inst[port], wmask_name, bank_wmask_name)
        
        for col in range(self.num_spare_cols):
            sparecol_name = "bank_spare_wen{}".format(col)
            bank_sparecol_name = "bank_spare_wen{0}_{1}".format(port, col)
            self.copy_layout_pin(self.port_data_inst[port], sparecol_name, bank_sparecol_name)
            
    def channel_route_bitlines(self, inst1, inst2, num_bits,
                               inst1_bl_name="bl_{}", inst1_br_name="br_{}",
                               inst2_bl_name="bl_{}", inst2_br_name="br_{}"):
        """
        Route the bl and br of two modules using the channel router.
        """
        
        # determine top and bottom automatically.
        # since they don't overlap, we can just check the bottom y coordinate.
        if inst1.by() < inst2.by():
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst1, inst1_bl_name, inst1_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst2, inst2_bl_name, inst2_br_name)
        else:
            (bottom_inst, bottom_bl_name, bottom_br_name) = (inst2, inst2_bl_name, inst2_br_name)
            (top_inst, top_bl_name, top_br_name) = (inst1, inst1_bl_name, inst1_br_name)

        # Channel route each mux separately since we don't minimize the number
        # of tracks in teh channel router yet. If we did, we could route all the bits at once!
        offset = bottom_inst.ul() + vector(0, self.m1_pitch)
        for bit in range(num_bits):
            bottom_names = [bottom_inst.get_pin(bottom_bl_name.format(bit)), bottom_inst.get_pin(bottom_br_name.format(bit))]
            top_names = [top_inst.get_pin(top_bl_name.format(bit)), top_inst.get_pin(top_br_name.format(bit))]
            route_map = list(zip(bottom_names, top_names))
            self.create_horizontal_channel_route(route_map, offset, self.m1_stack)
            
    def connect_bitline(self, inst1, inst2, inst1_name, inst2_name):
        """
        Connect two pins of two modules.
        This assumes that they have sufficient space to create a jog
        in the middle between the two modules (if needed).
        """
        
        # determine top and bottom automatically.
        # since they don't overlap, we can just check the bottom y coordinate.
        if inst1.by() < inst2.by():
            (bottom_inst, bottom_name) = (inst1, inst1_name)
            (top_inst, top_name) = (inst2, inst2_name)
        else:
            (bottom_inst, bottom_name) = (inst2, inst2_name)
            (top_inst, top_name) = (inst1, inst1_name)

        bottom_pin = bottom_inst.get_pin(bottom_name)
        top_pin = top_inst.get_pin(top_name)
        debug.check(bottom_pin.layer == top_pin.layer, "Pin layers do not match.")
        
        bottom_loc = bottom_pin.uc()
        top_loc = top_pin.bc()
        
        yoffset = 0.5 * (top_loc.y + bottom_loc.y)
        self.add_path(top_pin.layer,
                      [bottom_loc,
                       vector(bottom_loc.x, yoffset),
                       vector(top_loc.x, yoffset),
                       top_loc])
        
    def connect_bitlines(self, inst1, inst2, num_bits,
                         inst1_bl_name, inst1_br_name,
                         inst2_bl_name, inst2_br_name):
        """
        Connect the bl and br of two modules.
        """

        for col in range(num_bits):
            self.connect_bitline(inst1, inst2, inst1_bl_name.format(col), inst2_bl_name.format(col))
            self.connect_bitline(inst1, inst2, inst1_br_name.format(col), inst2_br_name.format(col))

    def route_port_address(self, port):
        """ Connect Wordline driver to bitcell array wordline """

        self.route_port_address_in(port)
        
        if port % 2:
            self.route_port_address_right(port)
        else:
            self.route_port_address_left(port)
            
    def route_port_address_left(self, port):
        """ Connecting Wordline driver output to Bitcell WL connection  """

        for row in range(self.num_rows):
            # The mid guarantees we exit the input cell to the right.
            driver_wl_pin = self.port_address_inst[port].get_pin("wl_{}".format(row))
            driver_wl_pos = driver_wl_pin.rc()
            bitcell_wl_pin = self.bitcell_array_inst.get_pin(self.wl_names[port] + "_{}".format(row))
            bitcell_wl_pos = bitcell_wl_pin.lc()
            mid1 = driver_wl_pos.scale(0, 1) + vector(0.5 * self.port_address_inst[port].rx() + 0.5 * self.bitcell_array_inst.lx(), 0)
            mid2 = mid1.scale(1, 0) + bitcell_wl_pos.scale(0.5, 1)
            self.add_path(driver_wl_pin.layer, [driver_wl_pos, mid1, mid2, bitcell_wl_pos])
            self.add_via_stack_center(from_layer=driver_wl_pin.layer,
                                      to_layer=bitcell_wl_pin.layer,
                                      offset=bitcell_wl_pos,
                                      directions=("H", "H"))

    def route_port_address_right(self, port):
        """ Connecting Wordline driver output to Bitcell WL connection  """

        for row in range(self.num_rows):
            # The mid guarantees we exit the input cell to the right.
            driver_wl_pin = self.port_address_inst[port].get_pin("wl_{}".format(row))
            driver_wl_pos = driver_wl_pin.lc()
            bitcell_wl_pin = self.bitcell_array_inst.get_pin(self.wl_names[port] + "_{}".format(row))
            bitcell_wl_pos = bitcell_wl_pin.rc()
            mid1 = driver_wl_pos.scale(0, 1) + vector(0.5 * self.port_address_inst[port].lx() + 0.5 * self.bitcell_array_inst.rx(), 0)
            mid2 = mid1.scale(1, 0) + bitcell_wl_pos.scale(0, 1)
            self.add_path(driver_wl_pin.layer, [driver_wl_pos, mid1, mid2, bitcell_wl_pos])
            self.add_via_stack_center(from_layer=driver_wl_pin.layer,
                                      to_layer=bitcell_wl_pin.layer,
                                      offset=bitcell_wl_pos,
                                      directions=("H", "H"))

    def route_column_address_lines(self, port):
        """ Connecting the select lines of column mux to the address bus """
        if not self.col_addr_size>0:
            return

        if OPTS.tech_name == "sky130":
            stack = self.m2_stack
            pitch = self.m3_pitch
        else:
            stack = self.m1_stack
            pitch = self.m2_pitch
        
        if self.col_addr_size == 1:
            
            # Connect to sel[0] and sel[1]
            decode_names = ["Zb", "Z"]
            
            # The Address LSB
            self.copy_layout_pin(self.column_decoder_inst[port], "A", "addr{}_0".format(port))
                
        elif self.col_addr_size > 1:
            decode_names = []
            for i in range(self.num_col_addr_lines):
                decode_names.append("out_{}".format(i))

            for i in range(self.col_addr_size):
                decoder_name = "in_{}".format(i)
                addr_name = "addr{0}_{1}".format(port, i)
                self.copy_layout_pin(self.column_decoder_inst[port], decoder_name, addr_name)

        if port % 2:
            offset = self.column_decoder_inst[port].ll() - vector((self.num_col_addr_lines + 1) * pitch, 0)
        else:
            offset = self.column_decoder_inst[port].lr() + vector(pitch, 0)

        decode_pins = [self.column_decoder_inst[port].get_pin(x) for x in decode_names]
        
        sel_names = ["sel_{}".format(x) for x in range(self.num_col_addr_lines)]
        column_mux_pins = [self.port_data_inst[port].get_pin(x) for x in sel_names]
        
        route_map = list(zip(decode_pins, column_mux_pins))
        self.create_vertical_channel_route(route_map,
                                           offset,
                                           stack)

    def add_lvs_correspondence_points(self):
        """
        This adds some points for easier debugging if LVS goes wrong.
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # Add the wordline names
        for i in range(self.num_rows):
            wl_name = "wl_{}".format(i)
            wl_pin = self.bitcell_array_inst.get_pin(wl_name)
            self.add_label(text=wl_name,
                           layer="m1",
                           offset=wl_pin.center())
        
        # Add the bitline names
        for i in range(self.num_cols):
            bl_name = "bl_{}".format(i)
            br_name = "br_{}".format(i)
            bl_pin = self.bitcell_array_inst.get_pin(bl_name)
            br_pin = self.bitcell_array_inst.get_pin(br_name)
            self.add_label(text=bl_name,
                           layer="m2",
                           offset=bl_pin.center())
            self.add_label(text=br_name,
                           layer="m2",
                           offset=br_pin.center())

        # # Add the data output names to the sense amp output
        # for i in range(self.word_size):
        #     data_name = "data_{}".format(i)
        #     data_pin = self.sense_amp_array_inst.get_pin(data_name)
        #     self.add_label(text="sa_out_{}".format(i),
        #                    layer="m2",
        #                    offset=data_pin.center())

        # Add labels on the decoder
        for port in self.write_ports:
            for i in range(self.word_size):
                data_name = "dec_out_{}".format(i)
                pin_name = "in_{}".format(i)
                data_pin = self.wordline_driver_inst[port].get_pin(pin_name)
                self.add_label(text=data_name,
                               layer="m1",
                               offset=data_pin.center())
            
    def route_control_lines(self, port):
        """ Route the control lines of the entire bank """
        
        # Make a list of tuples that we will connect.
        # From control signal to the module pin
        # Connection from the central bus to the main control block crosses
        # pre-decoder and this connection is in metal3
        connection = []
        connection.append((self.prefix + "p_en_bar{}".format(port),
                           self.port_data_inst[port].get_pin("p_en_bar")))

        rbl_wl_name = self.bitcell_array.get_rbl_wl_name(self.port_rbl_map[port])
        connection.append((self.prefix + "wl_en{}".format(port),
                           self.bitcell_array_inst.get_pin(rbl_wl_name)))
            
        if port in self.write_ports:
            connection.append((self.prefix + "w_en{}".format(port),
                               self.port_data_inst[port].get_pin("w_en")))
                
        if port in self.read_ports:
            connection.append((self.prefix + "s_en{}".format(port),
                               self.port_data_inst[port].get_pin("s_en")))

        for (control_signal, pin) in connection:
            control_pin = self.bus_pins[port][control_signal]
            control_pos = vector(control_pin.cx(), pin.cy())
            # If the y doesn't overlap the bus, add a segment
            if pin.cy() < control_pin.by():
                self.add_path("m2", [control_pos, control_pin.bc()])
            elif pin.cy() > control_pin.uy():
                self.add_path("m2", [control_pos, control_pin.uc()])
            self.add_path(pin.layer, [control_pos, pin.center()])
            self.add_via_stack_center(from_layer=pin.layer,
                                      to_layer="m2",
                                      offset=control_pos)

        # clk to wordline_driver
        control_signal = self.prefix + "wl_en{}".format(port)
        if port % 2:
            pin_pos = self.port_address_inst[port].get_pin("wl_en").uc()
            mid_pos = pin_pos + vector(0, 2 * self.m2_gap) # to route down to the top of the bus
        else:
            pin_pos = self.port_address_inst[port].get_pin("wl_en").bc()
            mid_pos = pin_pos - vector(0, 2 * self.m2_gap) # to route down to the top of the bus
        control_x_offset = self.bus_pins[port][control_signal].cx()
        control_pos = vector(control_x_offset, mid_pos.y)
        self.add_wire(self.m1_stack, [pin_pos, mid_pos, control_pos])
        self.add_via_center(layers=self.m1_stack,
                            offset=control_pos)
 
    def determine_wordline_stage_efforts(self, external_cout, inp_is_rise=True):
        """Get the all the stage efforts for each stage in the path within the bank clk_buf to a wordline"""
        # Decoder is assumed to have settled before the negative edge of the clock.
        # Delay model relies on this assumption
        stage_effort_list = []
        wordline_cout = self.bitcell_array.get_wordline_cin() + external_cout
        stage_effort_list += self.port_address.wordline_driver.determine_wordline_stage_efforts(wordline_cout,
                                                                                                inp_is_rise)
        
        return stage_effort_list
        
    def get_wl_en_cin(self):
        """Get the relative capacitance of all the clk connections in the bank"""
        # wl_en only used in the wordline driver.
        return self.port_address.wordline_driver.get_wl_en_cin()

    def get_w_en_cin(self):
        """Get the relative capacitance of all the clk connections in the bank"""
        # wl_en only used in the wordline driver.
        port = self.write_ports[0]
        return self.port_data[port].write_driver.get_w_en_cin()
    
    def get_clk_bar_cin(self):
        """Get the relative capacitance of all the clk_bar connections in the bank"""
        # Current bank only uses clock bar (clk_buf_bar) as an enable for the precharge array.
        
        # Precharges are the all the same in Mulitport, one is picked
        port = self.read_ports[0]
        return self.port_data[port].precharge_array.get_en_cin()

    def get_sen_cin(self):
        """Get the relative capacitance of all the sense amp enable connections in the bank"""
        # Current bank only uses sen as an enable for the sense amps.
        port = self.read_ports[0]
        return self.port_data[port].sense_amp_array.get_en_cin()
        
    def graph_exclude_precharge(self):
        """Precharge adds a loop between bitlines, can be excluded to reduce complexity"""
        for port in self.read_ports:
            if self.port_data[port]:
                self.port_data[port].graph_exclude_precharge()
                
    def get_cell_name(self, inst_name, row, col):
        """Gets the spice name of the target bitcell."""
        return self.bitcell_array_inst.mod.get_cell_name(inst_name + '.x' + self.bitcell_array_inst.name,
                                                         row,
                                                         col)

