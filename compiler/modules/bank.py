import sys
from tech import drc, parameter
import debug
import design
import math
from math import log,sqrt,ceil
import contact
import pgates
from pinv import pinv
from pnand2 import pnand2
from pnor2 import pnor2
from vector import vector
from pinvbuf import pinvbuf

from globals import OPTS

class bank(design.design):
    """
    Dynamically generated a single bank including bitcell array,
    hierarchical_decoder, precharge, (optional column_mux and column decoder), 
    write driver and sense amplifiers.
    """

    def __init__(self, sram_config, name=""):

        sram_config.set_local_config(self)
        
        if name == "":
            name = "bank_{0}_{1}".format(self.word_size, self.num_words)
        design.design.__init__(self, name)
        debug.info(2, "create sram of size {0} with {1} words".format(self.word_size,self.num_words))

        
        # The local control signals are gated when we have bank select logic,
        # so this prefix will be added to all of the input signals to create
        # the internal gated signals.
        if self.num_banks>1:
            self.prefix="gated_"
        else:
            self.prefix=""

        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()


    def create_netlist(self):
        self.compute_sizes()
        self.add_pins()
        self.add_modules()
        self.create_modules()

        
    def create_layout(self):
        self.place_modules()
        self.setup_routing_constraints()
        self.route_layout()
        
        # Can remove the following, but it helps for debug!
        #self.add_lvs_correspondence_points() 

        # Remember the bank center for further placement
        self.bank_center=self.offset_all_coordinates().scale(-1,-1)
        
        self.DRC_LVS()
 
 
    def add_pins(self):
        """ Adding pins for Bank module"""
        for port in self.read_ports:
            for bit in range(self.word_size):
                self.add_pin("dout{0}_{1}".format(port,bit),"OUT")
        for port in self.write_ports:
            for bit in range(self.word_size):
                self.add_pin("din{0}_{1}".format(port,bit),"IN")
        for port in self.all_ports:
            for bit in range(self.addr_size):
                self.add_pin("addr{0}_{1}".format(port,bit),"INPUT")

        # For more than one bank, we have a bank select and name
        # the signals gated_*.
        if self.num_banks > 1:
            for port in self.all_ports:
                self.add_pin("bank_sel{}".format(port),"INPUT")
        for port in self.read_ports:
            self.add_pin("s_en{0}".format(port), "INPUT")
        for port in self.write_ports:
            self.add_pin("w_en{0}".format(port), "INPUT")
        for port in self.all_ports:
            self.add_pin("clk_buf_bar{0}".format(port),"INPUT")
            self.add_pin("clk_buf{0}".format(port),"INPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

        
    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_central_bus()
        self.route_precharge_to_bitcell_array()
        self.route_col_mux_to_precharge_array()
        self.route_sense_amp_to_col_mux_or_precharge_array()
        self.route_write_driver_to_sense_amp()
        self.route_sense_amp_out()
        self.route_wordline_driver()
        self.route_write_driver()        
        self.route_row_decoder()
        self.route_column_address_lines()
        self.route_control_lines()
        if self.num_banks > 1:
            self.route_bank_select()            
        
        self.route_supplies()
        
    def create_modules(self):
        """ Add modules. The order should not matter! """

        # Above the bitcell array
        self.create_bitcell_array()
        self.create_precharge_array()
        
        # Below the bitcell array
        self.create_column_mux_array()
        self.create_sense_amp_array()
        self.create_write_driver_array()

        # To the left of the bitcell array
        self.create_row_decoder()
        self.create_wordline_driver()
        self.create_column_decoder()

        self.create_bank_select()

    def compute_module_offsets(self):
        """
        Compute the module offsets.
        """
        
        # UPPER RIGHT QUADRANT
        # Bitcell array is placed at (0,0)
        self.bitcell_array_offset = vector(0,0)

        # LOWER RIGHT QUADRANT
        # Below the bitcell array
        y_offset = self.precharge_array[0].height + self.m2_gap
        self.precharge_offset = vector(0,-y_offset)
        if self.col_addr_size > 0:
            y_offset += self.column_mux_array[0].height + self.m2_gap
        self.column_mux_offset = vector(0,-y_offset)
        y_offset += self.sense_amp_array.height + self.m2_gap
        self.sense_amp_offset = vector(0,-y_offset)                                
        y_offset += self.write_driver_array.height + self.m2_gap
        self.write_driver_offset = vector(0,-y_offset)

        # UPPER LEFT QUADRANT
        # To the left of the bitcell array
        # The wordline driver is placed to the right of the main decoder width.
        x_offset = self.central_bus_width + self.wordline_driver.width - self.m2_pitch
        self.wordline_driver_offset = vector(-x_offset,0)
        x_offset += self.row_decoder.width + self.m2_pitch
        self.row_decoder_offset = vector(-x_offset,0)

        # LOWER LEFT QUADRANT
        # Place the col decoder right aligned with row decoder (x_offset doesn't change)
        # Below the bitcell array
        if self.col_addr_size > 0:
            y_offset = self.col_decoder.height
        else:
            y_offset = 0
        y_offset += 2*drc("well_to_well")
        self.column_decoder_offset = vector(-x_offset,-y_offset)

        # Bank select gets placed below the column decoder (x_offset doesn't change)
        if self.col_addr_size > 0:
            y_offset = min(self.column_decoder_offset.y, self.column_mux_offset.y)
        else:
            y_offset = self.row_decoder_offset.y
        if self.num_banks > 1:
            y_offset += self.bank_select.height + drc("well_to_well")
        self.bank_select_offset = vector(-x_offset,-y_offset)
        
    def place_modules(self):
        """ Place the modules. """

        self.compute_module_offsets()
        
        # UPPER RIGHT QUADRANT
        self.place_bitcell_array(self.bitcell_array_offset)

        # LOWER RIGHT QUADRANT
        self.place_precharge_array([self.precharge_offset]*len(self.read_ports))
        self.place_column_mux_array([self.column_mux_offset]*len(self.all_ports))
        self.place_sense_amp_array([self.sense_amp_offset]*len(self.read_ports))
        self.place_write_driver_array([self.write_driver_offset]*len(self.write_ports))

        # UPPER LEFT QUADRANT
        self.place_row_decoder([self.row_decoder_offset]*len(self.all_ports))
        self.place_wordline_driver([self.wordline_driver_offset]*len(self.all_ports))

        # LOWER LEFT QUADRANT
        self.place_column_decoder([self.column_decoder_offset]*len(self.all_ports))
        self.place_bank_select([self.bank_select_offset]*len(self.all_ports))
 
 
    def compute_sizes(self):
        """  Computes the required sizes to create the bank """

        self.num_cols = int(self.words_per_row*self.word_size)
        self.num_rows = int(self.num_words / self.words_per_row)

        self.row_addr_size = int(log(self.num_rows, 2))
        self.col_addr_size = int(log(self.words_per_row, 2))
        self.addr_size = self.col_addr_size + self.row_addr_size

        debug.check(self.num_rows*self.num_cols==self.word_size*self.num_words,"Invalid bank sizes.")
        debug.check(self.addr_size==self.col_addr_size + self.row_addr_size,"Invalid address break down.")

        # Width for the vdd/gnd rails
        self.supply_rail_width = 4*self.m2_width
        # FIXME: This spacing should be width dependent...
        self.supply_rail_pitch = self.supply_rail_width + 4*self.m2_space
        
        # Number of control lines in the bus
        self.num_control_lines = 4
        # The order of the control signals on the control bus:
        self.input_control_signals = []
        port_num = 0
        for port in range(OPTS.num_rw_ports):
            self.input_control_signals.append(["clk_buf{}".format(port_num), "clk_buf_bar{}".format(port_num), "w_en{}".format(port_num), "s_en{}".format(port_num)])
            port_num += 1
        for port in range(OPTS.num_w_ports):
            self.input_control_signals.append(["clk_buf{}".format(port_num), "clk_buf_bar{}".format(port_num), "w_en{}".format(port_num)])
            port_num += 1
        for port in range(OPTS.num_r_ports):
            self.input_control_signals.append(["clk_buf{}".format(port_num), "clk_buf_bar{}".format(port_num), "s_en{}".format(port_num)])
            port_num += 1

        # These will be outputs of the gaters if this is multibank, if not, normal signals.
        self.control_signals = []
        for port in self.all_ports:
            if self.num_banks > 1:
                self.control_signals.append(["gated_"+str for str in self.input_control_signals[port]])
            else:
                self.control_signals.append(self.input_control_signals[port])
        # The central bus is the column address (one hot) and row address (binary)
        if self.col_addr_size>0:
            self.num_col_addr_lines = 2**self.col_addr_size
        else:
            self.num_col_addr_lines = 0            

        # The width of this bus is needed to place other modules (e.g. decoder)
        # A width on each side too
        self.central_bus_width = self.m2_pitch * self.num_control_lines + 2*self.m2_width

        # A space for wells or jogging m2
        self.m2_gap = max(2*drc("pwell_to_nwell") + drc("well_enclosure_active"),
                          2*self.m2_pitch)


    def add_modules(self):
        """ Create all the modules using the class loader """
        
        mod_list = ["bitcell", "decoder", "wordline_driver",
                    "bitcell_array",   "sense_amp_array",    "precharge_array",
                    "column_mux_array", "write_driver_array", 
                    "dff", "bank_select"]
        from importlib import reload
        for mod_name in mod_list:
            config_mod_name = getattr(OPTS, mod_name)
            class_file = reload(__import__(config_mod_name))
            mod_class = getattr(class_file , config_mod_name)
            setattr (self, "mod_"+mod_name, mod_class)

        
        self.bitcell = self.mod_bitcell()
        
        self.bitcell_array = self.mod_bitcell_array(cols=self.num_cols,
                                                    rows=self.num_rows)
        self.add_mod(self.bitcell_array)
        
        # create arrays of bitline and bitline_bar names for read, write, or all ports
        self.bl_names = self.bitcell.list_all_bl_names()
        self.br_names = self.bitcell.list_all_br_names()
        
        self.wl_names = self.bitcell.list_all_wl_names()
        self.bitline_names = self.bitcell.list_all_bitline_names()

        self.precharge_array = []
        for port in self.all_ports:
            if port in self.read_ports:
                self.precharge_array.append(self.mod_precharge_array(columns=self.num_cols, bitcell_bl=self.bl_names[port], bitcell_br=self.br_names[port]))
                self.add_mod(self.precharge_array[port])
            else:
                self.precharge_array.append(None)

        if self.col_addr_size > 0:
            self.column_mux_array = []
            for port in self.all_ports:
                self.column_mux_array.append(self.mod_column_mux_array(columns=self.num_cols, 
                                                                       word_size=self.word_size,
                                                                       bitcell_bl=self.bl_names[port],
                                                                       bitcell_br=self.br_names[port]))
                self.add_mod(self.column_mux_array[port])


        self.sense_amp_array = self.mod_sense_amp_array(word_size=self.word_size, 
                                                        words_per_row=self.words_per_row)
        self.add_mod(self.sense_amp_array)

        self.write_driver_array = self.mod_write_driver_array(columns=self.num_cols,
                                                              word_size=self.word_size)
        self.add_mod(self.write_driver_array)

        self.row_decoder = self.mod_decoder(rows=self.num_rows)
        self.add_mod(self.row_decoder)
        
        self.wordline_driver = self.mod_wordline_driver(rows=self.num_rows)
        self.add_mod(self.wordline_driver)

        self.inv = pinv()
        self.add_mod(self.inv)

        if(self.num_banks > 1):
            self.bank_select = self.mod_bank_select()
            self.add_mod(self.bank_select)
        

    def create_bitcell_array(self):
        """ Creating Bitcell Array """

        self.bitcell_array_inst=self.add_inst(name="bitcell_array", 
                                              mod=self.bitcell_array)
                    

        temp = []
        for col in range(self.num_cols):
            for bitline in self.bitline_names:
                temp.append(bitline+"_{0}".format(col))
        for row in range(self.num_rows):
            for wordline in self.wl_names:
                    temp.append(wordline+"_{0}".format(row))
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

        
    def place_bitcell_array(self, offset):
        """ Placing Bitcell Array """
        self.bitcell_array_inst.place(offset)

        
    def create_precharge_array(self):
        """ Creating Precharge """

        self.precharge_array_inst = []
        for port in self.read_ports:
            self.precharge_array_inst.append(self.add_inst(name="precharge_array{}".format(port),
                                                           mod=self.precharge_array[port]))
            temp = []
            for i in range(self.num_cols):
                temp.append(self.bl_names[port]+"_{0}".format(i))
                temp.append(self.br_names[port]+"_{0}".format(i))
            temp.extend([self.prefix+"clk_buf_bar{0}".format(port), "vdd"])
            self.connect_inst(temp)

            
    def place_precharge_array(self, offsets):
        """ Placing Precharge """
        
        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place precharge array.")

        # FIXME: place for multiport
        for port in self.read_ports:
            self.precharge_array_inst[port].place(offsets[port])

            
    def create_column_mux_array(self):
        """ Creating Column Mux when words_per_row > 1 . """
        self.col_mux_array_inst = []
        
        if self.col_addr_size == 0:
            return

        for port in self.all_ports:
            self.col_mux_array_inst.append(self.add_inst(name="column_mux_array{}".format(port),
                                                         mod=self.column_mux_array[port]))

            temp = []
            for col in range(self.num_cols):
                temp.append(self.bl_names[port]+"_{0}".format(col))
                temp.append(self.br_names[port]+"_{0}".format(col))
            for word in range(self.words_per_row):
                    temp.append("sel{0}_{1}".format(port,word))
            for bit in range(self.word_size):
                temp.append(self.bl_names[port]+"_out_{0}".format(bit))
                temp.append(self.br_names[port]+"_out_{0}".format(bit))
            temp.append("gnd")
            self.connect_inst(temp)


            
    def place_column_mux_array(self, offsets):
        """ Placing Column Mux when words_per_row > 1 . """
        if self.col_addr_size == 0:
            return

        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place column mux array.")
        
        for port in self.all_ports:
            self.col_mux_array_inst[port].place(offsets[port])

            
    def create_sense_amp_array(self):
        """ Creating Sense amp  """

        self.sense_amp_array_inst = []
        for port in self.read_ports:
            self.sense_amp_array_inst.append(self.add_inst(name="sense_amp_array{}".format(port),
                                                           mod=self.sense_amp_array))

            temp = []
            for bit in range(self.word_size):
                temp.append("dout{0}_{1}".format(port,bit))
                if self.words_per_row == 1:
                    temp.append(self.bl_names[port]+"_{0}".format(bit))
                    temp.append(self.br_names[port]+"_{0}".format(bit))
                else:
                    temp.append(self.bl_names[port]+"_out_{0}".format(bit))
                    temp.append(self.br_names[port]+"_out_{0}".format(bit))
                    
            temp.extend([self.prefix+"s_en{}".format(port), "vdd", "gnd"])
            self.connect_inst(temp)

            
    def place_sense_amp_array(self, offsets):
        """ Placing Sense amp  """
        
        debug.check(len(offsets)>=len(self.read_ports), "Insufficient offsets to place sense amp array.")

        # FIXME: place for multiport
        for port in self.read_ports:
            self.sense_amp_array_inst[port].place(offsets[port])

            
    def create_write_driver_array(self):
        """ Creating Write Driver  """

        self.write_driver_array_inst = []
        for port in self.all_ports:
            if port in self.write_ports:
                self.write_driver_array_inst.append(self.add_inst(name="write_driver_array{}".format(port), 
                                                                  mod=self.write_driver_array))
            else:
                self.write_driver_array_inst.append(None)

            temp = []
            for bit in range(self.word_size):
                temp.append("din{0}_{1}".format(port,bit))
            for bit in range(self.word_size):            
                if (self.words_per_row == 1):            
                    temp.append(self.bl_names[port]+"_{0}".format(bit))
                    temp.append(self.br_names[port]+"_{0}".format(bit))
                else:
                    temp.append(self.bl_names[port]+"_out_{0}".format(bit))
                    temp.append(self.br_names[port]+"_out_{0}".format(bit))
            temp.extend([self.prefix+"w_en{0}".format(port), "vdd", "gnd"])
            self.connect_inst(temp)

            
    def place_write_driver_array(self, offsets):
        """ Placing Write Driver  """

        debug.check(len(offsets)>=len(self.write_ports), "Insufficient offsets to place write driver array.")

        for port in self.write_ports:
            self.write_driver_array_inst[port].place(offsets[port])
            

    def create_row_decoder(self):
        """  Create the hierarchical row decoder  """
        
        self.row_decoder_inst = []
        for port in self.all_ports:
            self.row_decoder_inst.append(self.add_inst(name="row_decoder{}".format(port), 
                                                       mod=self.row_decoder))

            temp = []
            for bit in range(self.row_addr_size):
                temp.append("addr{0}_{1}".format(port,bit+self.col_addr_size))
            for row in range(self.num_rows):
                temp.append("dec_out{0}_{1}".format(port,row))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)

            
    def place_row_decoder(self, offsets):
        """  Place the hierarchical row decoder  """

        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place row decoder array.")
        
        # The address and control bus will be in between decoder and the main memory array 
        # This bus will route address bits to the decoder input and column mux inputs. 
        # The wires are actually routed after we placed the stuff on both sides.
        # The predecoder is below the x-axis and the main decoder is above the x-axis
        # The address flop and decoder are aligned in the x coord.
        
        # FIXME: place for multiport
        for port in self.all_ports:
            self.row_decoder_inst[port].place(offsets[port])

            
    def create_wordline_driver(self):
        """ Create the Wordline Driver """

        self.wordline_driver_inst = []
        for port in self.all_ports:
            self.wordline_driver_inst.append(self.add_inst(name="wordline_driver{}".format(port), 
                                                           mod=self.wordline_driver))

            temp = []
            for row in range(self.num_rows):
                temp.append("dec_out{0}_{1}".format(port,row))
            for row in range(self.num_rows):
                temp.append(self.wl_names[port]+"_{0}".format(row))
            temp.append(self.prefix+"clk_buf{0}".format(port))
            temp.append("vdd")
            temp.append("gnd")
            self.connect_inst(temp)

            
    def place_wordline_driver(self, offsets):
        """ Place the Wordline Driver """

        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place wordline driver array.")
        
        for port in self.all_ports:
            self.wordline_driver_inst[port].place(offsets[port])

        
    def create_column_decoder(self):
        """ 
        Create a 2:4 or 3:8 column address decoder.
        """
        
        if self.col_addr_size == 0:
            return
        elif self.col_addr_size == 1:
            self.col_decoder = pinvbuf(height=self.mod_dff.height)
            self.add_mod(self.col_decoder)
        elif self.col_addr_size == 2:
            self.col_decoder = self.row_decoder.pre2_4
        elif self.col_addr_size == 3:
            self.col_decoder = self.row_decoder.pre3_8
        else:
            # No error checking before?
            debug.error("Invalid column decoder?",-1)

        self.col_decoder_inst = []
        for port in self.all_ports:
            self.col_decoder_inst.append(self.add_inst(name="col_address_decoder{}".format(port), 
                                                       mod=self.col_decoder))

            temp = []
            for bit in range(self.col_addr_size):
                temp.append("addr{0}_{1}".format(port,bit))
            for bit in range(self.num_col_addr_lines):
                temp.append("sel{0}_{1}".format(port,bit))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)

            
    def place_column_decoder(self, offsets):
        """ 
        Place a 2:4 or 3:8 column address decoder.
        """
        if self.col_addr_size == 0:
            return
        
        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place column decoder.")        

        for port in self.all_ports:
            self.col_decoder_inst[port].place(offsets[port])


            
    def create_bank_select(self):
        """ Create the bank select logic. """

        if not self.num_banks > 1:
            return

        self.bank_select_inst = []
        for port in self.all_ports:
            self.bank_select_inst.append(self.add_inst(name="bank_select{}".format(port),
                                                       mod=self.bank_select))
            
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

        debug.check(len(offsets)>=len(self.all_ports), "Insufficient offsets to place bank select logic.")                

        for port in self.all_ports:
            self.bank_select_inst[port].place(offsets[port])

        
    def route_supplies(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """
        for inst in self.insts:
            self.copy_power_pins(inst,"vdd")
            self.copy_power_pins(inst,"gnd")

    def route_bank_select(self):
        """ Route the bank select logic. """
        
        for port in self.all_ports:
            if self.port_id[port] == "rw":
                bank_sel_signals = ["clk_buf", "clk_buf_bar", "w_en", "s_en", "bank_sel"]
                gated_bank_sel_signals = ["gated_clk_buf", "gated_clk_buf_bar", "gated_w_en", "gated_s_en"]
            elif self.port_id[port] == "w":
                bank_sel_signals = ["clk_buf", "clk_buf_bar", "w_en", "bank_sel"]
                gated_bank_sel_signals = ["gated_clk_buf", "gated_clk_buf_bar", "gated_w_en"]
            else:
                bank_sel_signals = ["clk_buf", "clk_buf_bar", "s_en", "bank_sel"]
                gated_bank_sel_signals = ["gated_clk_buf", "gated_clk_buf_bar", "gated_s_en"]
        
            copy_control_signals = self.input_control_signals[port]+["bank_sel{}".format(port)]
            for signal in range(len(copy_control_signals)):
                self.copy_layout_pin(self.bank_select_inst[port], bank_sel_signals[signal], copy_control_signals[signal])
    
            for signal in range(len(gated_bank_sel_signals)):
                # Connect the inverter output to the central bus
                out_pos = self.bank_select_inst[port].get_pin(gated_bank_sel_signals[signal]).rc()
                name = self.control_signals[port][signal]
                bus_pos = vector(self.bus_xoffset[name].x, out_pos.y)
                self.add_path("metal3",[out_pos, bus_pos])
                self.add_via_center(layers=("metal2", "via2", "metal3"),
                                    offset=bus_pos,
                                    rotate=90)
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=out_pos,
                                    rotate=90)
                self.add_via_center(layers=("metal2", "via2", "metal3"),
                                    offset=out_pos,
                                    rotate=90)
        
    
    def setup_routing_constraints(self):
        """ 
        After the modules are instantiated, find the dimensions for the
        control bus, power ring, etc. 
        """
        # FIXME: calculate for multiport
        
        #The minimum point is either the bottom of the address flops,
        #the column decoder (if there is one).
        write_driver_min_y_offset = self.write_driver_array_inst[0].by() - 3*self.m2_pitch        
        row_decoder_min_y_offset = self.row_decoder_inst[0].by()
        
        if self.col_addr_size > 0:
            col_decoder_min_y_offset = self.col_decoder_inst[0].by()
        else:
            col_decoder_min_y_offset = row_decoder_min_y_offset
        
        if self.num_banks>1:
            # The control gating logic is below the decoder
            # Min of the control gating logic and write driver.
            self.min_y_offset = min(col_decoder_min_y_offset - self.bank_select.height, write_driver_min_y_offset)
        else:
            # Just the min of the decoder logic logic and write driver.
            self.min_y_offset = min(col_decoder_min_y_offset, write_driver_min_y_offset)

        # The max point is always the top of the precharge bitlines
        # Add a vdd and gnd power rail above the array
        # FIXME: Update multiport
        self.max_y_offset = self.bitcell_array_inst.ur().y + 3*self.m1_width
        self.max_x_offset = self.bitcell_array_inst.ur().x + 3*self.m1_width
        self.min_x_offset = self.row_decoder_inst[0].lx()

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
        # The bank is at (0,0), so this is to the left of the y-axis.
        # 2 pitches on the right for vias/jogs to access the inputs 
        for port in self.all_ports:
            control_bus_offset = vector(-self.m2_pitch * self.num_control_lines - self.m2_width, self.min_y_offset)
            control_bus_length = self.max_y_offset - self.min_y_offset
            self.bus_xoffset = self.create_bus(layer="metal2",
                                               pitch=self.m2_pitch,
                                               offset=control_bus_offset,
                                               names=self.control_signals[port],
                                               length=control_bus_length,
                                               vertical=True,
                                               make_pins=(self.num_banks==1))


    def route_precharge_to_bitcell_array(self):
        """ Routing of BL and BR between pre-charge and bitcell array """

        # FIXME: Update for multiport
        for port in self.read_ports:
            for col in range(self.num_cols):
                precharge_bl = self.precharge_array_inst[port].get_pin("bl_{}".format(col)).uc()
                precharge_br = self.precharge_array_inst[port].get_pin("br_{}".format(col)).uc()
                bitcell_bl = self.bitcell_array_inst.get_pin(self.bl_names[port]+"_{}".format(col)).bc()
                bitcell_br = self.bitcell_array_inst.get_pin(self.br_names[port]+"_{}".format(col)).bc()

                yoffset = 0.5*(precharge_bl.y+bitcell_bl.y)
                self.add_path("metal2",[precharge_bl, vector(precharge_bl.x,yoffset),
                                        vector(bitcell_bl.x,yoffset), bitcell_bl])
                self.add_path("metal2",[precharge_br, vector(precharge_br.x,yoffset),
                                        vector(bitcell_br.x,yoffset), bitcell_br])


    def route_col_mux_to_precharge_array(self):
        """ Routing of BL and BR between col mux and precharge array """

        # Only do this if we have a column mux!
        if self.col_addr_size==0:
            return
        
        # FIXME: Update for multiport
        for port in self.all_ports:
            bottom_inst = self.col_mux_array_inst[port]
            top_inst = self.precharge_array_inst[port]
            self.connect_bitlines(top_inst, bottom_inst, self.num_cols)


                                        
    def route_sense_amp_to_col_mux_or_precharge_array(self):
        """ Routing of BL and BR between sense_amp and column mux or precharge array """

        for port in self.read_ports:
            bottom_inst = self.sense_amp_array_inst[port]
            
            if self.col_addr_size>0:
                # Sense amp is connected to the col mux
                top_inst = self.col_mux_array_inst[port]
                top_bl = "bl_out_{}"
                top_br = "br_out_{}"
            else:
                # Sense amp is directly connected to the precharge array
                top_inst = self.precharge_array_inst[port]
                top_bl = "bl_{}"
                top_br = "br_{}"
                
            self.connect_bitlines(top_inst, bottom_inst, self.word_size,
                                  top_bl_name=top_bl, top_br_name=top_br)

    def route_write_driver_to_sense_amp(self):
        """ Routing of BL and BR between write driver and sense amp """

        for port in self.write_ports:
            bottom_inst = self.write_driver_array_inst[port]
            top_inst = self.sense_amp_array_inst[port]
            self.connect_bitlines(top_inst, bottom_inst, self.word_size)

                

    def route_sense_amp_out(self):
        """ Add pins for the sense amp output """

        # FIXME: Update for multiport
        for port in self.read_ports:
            for bit in range(self.word_size):
                data_pin = self.sense_amp_array_inst[port].get_pin("data_{}".format(bit))
                self.add_layout_pin_rect_center(text="dout{0}_{1}".format(self.read_ports[port],bit),
                                                layer=data_pin.layer, 
                                                offset=data_pin.center(),
                                                height=data_pin.height(),
                                                width=data_pin.width())


    def route_row_decoder(self):
        """ Routes the row decoder inputs and supplies """

        # FIXME: Update for multiport
        # Create inputs for the row address lines
        for port in self.all_ports:
            for row in range(self.row_addr_size):
                addr_idx = row + self.col_addr_size
                decoder_name = "addr_{}".format(row)
                addr_name = "addr{0}_{1}".format(port,addr_idx)
                self.copy_layout_pin(self.row_decoder_inst[port], decoder_name, addr_name)
            
            
    def route_write_driver(self):
        """ Connecting write driver   """
        for port in self.all_ports:
            for row in range(self.word_size):
                data_name = "data_{}".format(row)
                din_name = "din{0}_{1}".format(port,row)
                self.copy_layout_pin(self.write_driver_array_inst[port], data_name, din_name)

    def connect_bitlines(self, top_inst, bottom_inst, num_items,
                         top_bl_name="bl_{}", top_br_name="br_{}", bottom_bl_name="bl_{}", bottom_br_name="br_{}"):
        """
        Connect the bl and br of two modules.
        This assumes that they have sufficient space to create a jog
        in the middle between the two modules (if needed)
        """
        for col in range(num_items):
            bottom_bl = bottom_inst.get_pin(bottom_bl_name.format(col)).uc()
            bottom_br = bottom_inst.get_pin(bottom_br_name.format(col)).uc()
            top_bl = top_inst.get_pin(top_bl_name.format(col)).bc()
            top_br = top_inst.get_pin(top_br_name.format(col)).bc()

            yoffset = 0.5*(top_bl.y+bottom_bl.y)
            self.add_path("metal2",[bottom_bl, vector(bottom_bl.x,yoffset),
                                    vector(top_bl.x,yoffset), top_bl])
            self.add_path("metal2",[bottom_br, vector(bottom_br.x,yoffset),
                                    vector(top_br.x,yoffset), top_br])
        
    
    def route_wordline_driver(self):
        """ Connecting Wordline driver output to Bitcell WL connection  """
        for port in self.all_ports:
            for row in range(self.num_rows):
                # The pre/post is to access the pin from "outside" the cell to avoid DRCs
                decoder_out_pos = self.row_decoder_inst[port].get_pin("decode_{}".format(row)).rc()
                driver_in_pos = self.wordline_driver_inst[port].get_pin("in_{}".format(row)).lc()
                mid1 = decoder_out_pos.scale(0.5,1)+driver_in_pos.scale(0.5,0)
                mid2 = decoder_out_pos.scale(0.5,0)+driver_in_pos.scale(0.5,1)
                self.add_path("metal1", [decoder_out_pos, mid1, mid2, driver_in_pos])

                # The mid guarantees we exit the input cell to the right.
                driver_wl_pos = self.wordline_driver_inst[port].get_pin("wl_{}".format(row)).rc()
                bitcell_wl_pos = self.bitcell_array_inst.get_pin(self.wl_names[port]+"_{}".format(row)).lc()
                mid1 = driver_wl_pos.scale(0.5,1)+bitcell_wl_pos.scale(0.5,0)
                mid2 = driver_wl_pos.scale(0.5,0)+bitcell_wl_pos.scale(0.5,1)
                self.add_path("metal1", [driver_wl_pos, mid1, mid2, bitcell_wl_pos])
        

    def route_column_address_lines(self):
        """ Connecting the select lines of column mux to the address bus """
        if not self.col_addr_size>0:
            return

        for port in self.all_ports:
            if self.col_addr_size == 1:
                
                # Connect to sel[0] and sel[1]
                decode_names = ["Zb", "Z"]
                
                # The Address LSB
                self.copy_layout_pin(self.col_decoder_inst[port], "A", "addr{}_0".format(port)) 
                
            elif self.col_addr_size > 1:
                decode_names = []
                for i in range(self.num_col_addr_lines):
                    decode_names.append("out_{}".format(i))

                for i in range(self.col_addr_size):
                    decoder_name = "in_{}".format(i)
                    addr_name = "addr{0}_{1}".format(port,i)
                    self.copy_layout_pin(self.col_decoder_inst[port], decoder_name, addr_name)

            offset = self.col_decoder_inst[port].lr() + vector(self.m2_pitch, 0)

            sel_names = ["sel_{}".format(x) for x in range(self.num_col_addr_lines)]

            route_map = list(zip(decode_names, sel_names))
            decode_pins = {key: self.col_decoder_inst[port].get_pin(key) for key in decode_names }
            col_mux_pins = {key: self.col_mux_array_inst[port].get_pin(key) for key in sel_names }
            # Combine the dff and bank pins into a single dictionary of pin name to pin.
            all_pins = {**decode_pins, **col_mux_pins}
            self.create_vertical_channel_route(route_map, all_pins, offset)


    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # Add the wordline names
        for i in range(self.num_rows):
            wl_name = "wl_{}".format(i)
            wl_pin = self.bitcell_array_inst.get_pin(wl_name)
            self.add_label(text=wl_name,
                           layer="metal1",  
                           offset=wl_pin.center())
        
        # Add the bitline names
        for i in range(self.num_cols):
            bl_name = "bl_{}".format(i)
            br_name = "br_{}".format(i)
            bl_pin = self.bitcell_array_inst.get_pin(bl_name)
            br_pin = self.bitcell_array_inst.get_pin(br_name)
            self.add_label(text=bl_name,
                           layer="metal2",  
                           offset=bl_pin.center())
            self.add_label(text=br_name,
                           layer="metal2",  
                           offset=br_pin.center())

        # # Add the data output names to the sense amp output     
        # for i in range(self.word_size):
        #     data_name = "data_{}".format(i)
        #     data_pin = self.sense_amp_array_inst.get_pin(data_name)
        #     self.add_label(text="sa_out_{}".format(i),
        #                    layer="metal2",  
        #                    offset=data_pin.center())

        # Add labels on the decoder
        for i in range(self.word_size):
            data_name = "dec_out_{}".format(i)
            pin_name = "in_{}".format(i)            
            data_pin = self.wordline_driver_inst[0].get_pin(pin_name)
            self.add_label(text=data_name,
                           layer="metal1",  
                           offset=data_pin.center())
            
            
    def route_control_lines(self):
        """ Route the control lines of the entire bank """
        
        # Make a list of tuples that we will connect.
        # From control signal to the module pin 
        # Connection from the central bus to the main control block crosses
        # pre-decoder and this connection is in metal3
        write_inst = 0
        read_inst = 0
        
        # Control lines for RW ports
        for port in self.all_ports:
            connection = []
            if port in self.read_ports:
                connection.append((self.prefix+"clk_buf_bar{}".format(port), self.precharge_array_inst[port].get_pin("en").lc()))
                
            if port in self.write_ports:
                connection.append((self.prefix+"w_en{}".format(port), self.write_driver_array_inst[port].get_pin("en").lc()))
                
            if port in self.read_ports:
                connection.append((self.prefix+"s_en{}".format(port), self.sense_amp_array_inst[port].get_pin("en").lc()))
      
            for (control_signal, pin_pos) in connection:
                control_pos = vector(self.bus_xoffset[control_signal].x ,pin_pos.y)
                self.add_path("metal1", [control_pos, pin_pos])
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=control_pos,
                                    rotate=90)

            # clk to wordline_driver
            control_signal = self.prefix+"clk_buf{}".format(port)
            pin_pos = self.wordline_driver_inst[port].get_pin("en").uc()
            mid_pos = pin_pos + vector(0,self.m1_pitch)
            control_x_offset = self.bus_xoffset[control_signal].x
            control_pos = vector(control_x_offset + self.m1_width, mid_pos.y)
            self.add_wire(("metal1","via1","metal2"),[pin_pos, mid_pos, control_pos])
            control_via_pos = vector(control_x_offset, mid_pos.y)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=control_via_pos,
                                rotate=90)

        
    def analytical_delay(self, vdd, slew, load):
        """ return  analytical delay of the bank"""
        results = []
        
        decoder_delay = self.row_decoder.analytical_delay(slew, self.wordline_driver.input_load())

        word_driver_delay = self.wordline_driver.analytical_delay(decoder_delay.slew, self.bitcell_array.input_load())

        #FIXME: Array delay is the same for every port.
        bitcell_array_delay = self.bitcell_array.analytical_delay(word_driver_delay.slew)

        #This also essentially creates the same delay for each port. Good structure, no substance
        for port in self.all_ports:
            if self.words_per_row > 1:
                column_mux_delay = self.column_mux_array[port].analytical_delay(vdd, bitcell_array_delay.slew,
                                                                         self.sense_amp_array.input_load())
            else:
                column_mux_delay = self.return_delay(delay = 0.0, slew=word_driver_delay.slew)
                
            bl_t_data_out_delay = self.sense_amp_array.analytical_delay(column_mux_delay.slew,
                                                                        self.bitcell_array.output_load())
            # output load of bitcell_array is set to be only small part of bl for sense amp.
            results.append(decoder_delay + word_driver_delay + bitcell_array_delay + column_mux_delay + bl_t_data_out_delay) 

        return results
        
