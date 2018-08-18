import sys
from tech import drc, parameter
import debug
import design
import math
from math import log,sqrt,ceil
import contact
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

    def __init__(self, word_size, num_words, words_per_row, num_banks=1, name=""):

        mod_list = ["bitcell", "decoder", "ms_flop_array", "wordline_driver",
                    "bitcell_array",   "sense_amp_array",    "precharge_array",
                    "column_mux_array", "write_driver_array", 
                    "dff", "bank_select"]
        from importlib import reload
        for mod_name in mod_list:
            config_mod_name = getattr(OPTS, mod_name)
            class_file = reload(__import__(config_mod_name))
            mod_class = getattr(class_file , config_mod_name)
            setattr (self, "mod_"+mod_name, mod_class)

        if name == "":
            name = "bank_{0}_{1}".format(word_size, num_words)
        design.design.__init__(self, name)
        debug.info(2, "create sram of size {0} with {1} words".format(word_size,num_words))

        self.word_size = word_size
        self.num_words = num_words
        self.words_per_row = words_per_row
        self.num_banks = num_banks
        
        self.total_write = OPTS.rw_ports + OPTS.w_ports
        self.total_read = OPTS.rw_ports + OPTS.r_ports
        self.total_ports = OPTS.rw_ports + OPTS.w_ports + OPTS.r_ports

        # The local control signals are gated when we have bank select logic,
        # so this prefix will be added to all of the input signals to create
        # the internal gated signals.
        if self.num_banks>1:
            self.prefix="gated_"
        else:
            self.prefix=""
        
        self.compute_sizes()
        self.add_pins()
        self.create_modules()
        self.add_modules()
        self.setup_layout_constraints()

        # FIXME: Move this to the add modules function
        self.add_bank_select()
        
        self.route_layout()
        

        # Can remove the following, but it helps for debug!
        #self.add_lvs_correspondence_points() 

        # Remember the bank center for further placement
        self.bank_center=self.offset_all_coordinates().scale(-1,-1)
        
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for Bank module"""
        for k in range(self.total_read):
            for i in range(self.word_size):
                self.add_pin("dout{0}[{1}]".format(k,i),"OUT")
        for k in range(self.total_write):
            for i in range(self.word_size):
                self.add_pin("din{0}[{1}]".format(k,i),"IN")
        for k in range(self.total_ports):
            for i in range(self.addr_size):
                self.add_pin("addr{0}[{1}]".format(k,i),"INPUT")

        # For more than one bank, we have a bank select and name
        # the signals gated_*.
        if self.num_banks > 1:
            self.add_pin("bank_sel","INPUT")
        for k in range(self.total_read):
            self.add_pin("s_en{0}".format(k), "INPUT")
        for k in range(self.total_write):
            self.add_pin("w_en{0}".format(k), "INPUT")
        for pin in ["clk_buf_bar","clk_buf"]:
            self.add_pin(pin,"INPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_central_bus()
        self.route_precharge_to_bitcell_array()
        self.route_col_mux_to_bitcell_array()
        self.route_sense_amp_to_col_mux_or_bitcell_array()
        self.route_sense_amp_out()
        self.route_wordline_driver()
        self.route_write_driver()        
        self.route_row_decoder()
        self.route_column_address_lines()
        self.route_control_lines()
        if self.num_banks > 1:
            self.route_bank_select()            
        
        self.route_vdd_gnd()
        
    def add_modules(self):
        """ Add modules. The order should not matter! """

        # Above the bitcell array
        self.add_bitcell_array()
        self.add_precharge_array()
        
        # Below the bitcell array
        self.add_column_mux_array()
        self.add_sense_amp_array()
        self.add_write_driver_array()

        # To the left of the bitcell array
        self.add_row_decoder()
        self.add_wordline_driver()
        self.add_column_decoder()
        

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
        self.input_control_signals = ["clk_buf", "clk_buf_bar", "w_en0", "s_en0"]

        # These will be outputs of the gaters if this is multibank, if not, normal signals.
        if self.num_banks > 1:
            self.control_signals = ["gated_"+str for str in self.input_control_signals]
        else:
            self.control_signals = self.input_control_signals
        # The central bus is the column address (one hot) and row address (binary)
        if self.col_addr_size>0:
            self.num_col_addr_lines = 2**self.col_addr_size
        else:
            self.num_col_addr_lines = 0            

        # The width of this bus is needed to place other modules (e.g. decoder)
        # A width on each side too
        self.central_bus_width = self.m2_pitch * self.num_control_lines + 2*self.m2_width

        # A space for wells or jogging m2
        self.m2_gap = max(2*drc["pwell_to_nwell"] + drc["well_enclosure_active"],
                          2*self.m2_pitch)


    def create_modules(self):
        """ Create all the modules using the class loader """
        self.bitcell = self.mod_bitcell()
        
        self.bitcell_array = self.mod_bitcell_array(cols=self.num_cols,
                                                    rows=self.num_rows)
        self.add_mod(self.bitcell_array)
        
        # create arrays of bitline and bitline_bar names for read, write, or all ports
        self.read_bl_list = self.bitcell.list_read_column_pins()
        self.read_br_list = self.bitcell.list_read_bar_column_pins()
        
        self.write_bl_list = self.bitcell.list_write_column_pins()
        self.write_br_list = self.bitcell.list_write_bar_column_pins()
        
        self.total_bl_list = self.bitcell.list_column_pins()
        self.total_br_list = self.bitcell.list_column_bar_pins()
        
        self.total_wl_list = self.bitcell.list_row_pins()

        self.precharge_array = [None] * self.total_read
        for k in range(self.total_read):
            self.precharge_array[k] = self.mod_precharge_array(columns=self.num_cols, bitcell_bl=self.read_bl_list[k], bitcell_br=self.read_br_list[k])
            self.add_mod(self.precharge_array[k])

        if self.col_addr_size > 0:
            self.column_mux_array = self.mod_column_mux_array(columns=self.num_cols, 
                                                              word_size=self.word_size)
            self.add_mod(self.column_mux_array)


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
        

    def add_bitcell_array(self):
        """ Adding Bitcell Array """

        self.bitcell_array_inst=self.add_inst(name="bitcell_array", 
                                              mod=self.bitcell_array,
                                              offset=vector(0,0))

        temp = []
        bl_list = self.bitcell.list_all_column_pins()
        wl_list = self.bitcell.list_row_pins()
        for col in range(self.num_cols):
            for bitline in bl_list:
                temp.append(bitline+"[{0}]".format(col))
        for row in range(self.num_rows):
            for wordline in wl_list:
                    temp.append(wordline+"[{0}]".format(row))
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)


    def add_precharge_array(self):
        """ Adding Precharge """

        self.precharge_array_inst = [None] * self.total_read
        
        for k in range(self.total_read):
            # The wells must be far enough apart
            # The enclosure is for the well and the spacing is to the bitcell wells
            y_offset = self.bitcell_array.height + self.m2_gap
            self.precharge_array_inst[k]=self.add_inst(name="precharge_array{}".format(k),
                                                       mod=self.precharge_array[k], 
                                                       offset=vector(0,y_offset))
            temp = []
            for i in range(self.num_cols):
                temp.append(self.read_bl_list[k]+"[{0}]".format(i))
                temp.append(self.read_br_list[k]+"[{0}]".format(i))
            temp.extend([self.prefix+"clk_buf_bar", "vdd"])
            self.connect_inst(temp)

    def add_column_mux_array(self):
        """ Adding Column Mux when words_per_row > 1 . """

        if self.col_addr_size > 0:
            self.column_mux_height = self.column_mux_array.height + self.m2_gap
        else:
            self.column_mux_height = 0
            return

        self.col_mux_array_inst = [None] * self.total_ports
        
        for k in range(self.total_ports):
            y_offset = self.column_mux_height 
            self.col_mux_array_inst[k]=self.add_inst(name="column_mux_array{}".format(k),
                                                     mod=self.column_mux_array,
                                                     offset=vector(0,y_offset).scale(-1,-1))
            temp = []
            for i in range(self.num_cols):
                temp.append(self.total_bl_list[k]+"[{0}]".format(i))
                temp.append(self.total_br_list[k]+"[{0}]".format(i))
            for h in range(self.words_per_row):
                    temp.append("sel{0}[{1}]".format(k,h))
            for j in range(self.word_size):
                temp.append(self.total_bl_list[k]+"_out[{0}]".format(j))
                temp.append(self.total_br_list[k]+"_out[{0}]".format(j))
            temp.append("gnd")
            self.connect_inst(temp)

    def add_sense_amp_array(self):
        """ Adding Sense amp  """

        self.sense_amp_array_inst = [None] * self.total_read
        
        for k in range(self.total_read):
            y_offset = self.column_mux_height + self.sense_amp_array.height + self.m2_gap
            self.sense_amp_array_inst[k]=self.add_inst(name="sense_amp_array{}".format(k),
                                                       mod=self.sense_amp_array,
                                                       offset=vector(0,y_offset).scale(-1,-1))
            temp = []
            for i in range(self.word_size):
                temp.append("dout{0}[{1}]".format(k,i))
                if self.words_per_row == 1:
                    temp.append(self.read_bl_list[k]+"[{0}]".format(i))
                    temp.append(self.read_br_list[k]+"[{0}]".format(i))
                else:
                    temp.append(self.read_bl_list[k]+"_out[{0}]".format(i))
                    temp.append(self.read_br_list[k]+"_out[{0}]".format(i))
                    
            temp.extend([self.prefix+"s_en{0}".format(k), "vdd", "gnd"])
            self.connect_inst(temp)

    def add_write_driver_array(self):
        """ Adding Write Driver  """

        self.write_driver_array_inst = [None] * self.total_write
        
        for k in range(self.total_write):
            y_offset = self.sense_amp_array.height + self.column_mux_height \
                + self.m2_gap + self.write_driver_array.height 
            self.write_driver_array_inst[k]=self.add_inst(name="write_driver_array{}".format(k), 
                                                          mod=self.write_driver_array, 
                                                          offset=vector(0,y_offset).scale(-1,-1))

            temp = []
            for i in range(self.word_size):
                temp.append("din{0}[{1}]".format(k,i))
            for i in range(self.word_size):            
                if (self.words_per_row == 1):            
                    temp.append(self.write_bl_list[k]+"[{0}]".format(i))
                    temp.append(self.write_br_list[k]+"[{0}]".format(i))
                else:
                    temp.append(self.write_bl_list[k]+"_out[{0}]".format(i))
                    temp.append(self.write_br_list[k]+"_out[{0}]".format(i))
            temp.extend([self.prefix+"w_en{0}".format(k), "vdd", "gnd"])
            self.connect_inst(temp)


    def add_row_decoder(self):
        """  Add the hierarchical row decoder  """

        # The address and control bus will be in between decoder and the main memory array 
        # This bus will route address bits to the decoder input and column mux inputs. 
        # The wires are actually routed after we placed the stuff on both sides.
        # The predecoder is below the x-axis and the main decoder is above the x-axis
        # The address flop and decoder are aligned in the x coord.
        
        self.row_decoder_inst = [None] * self.total_ports
        
        for k in range(self.total_ports):
            x_offset = -(self.row_decoder.width + self.central_bus_width + self.wordline_driver.width)
            self.row_decoder_inst[k]=self.add_inst(name="row_decoder{}".format(k), 
                                                   mod=self.row_decoder, 
                                                   offset=vector(x_offset,0))

            temp = []
            for i in range(self.row_addr_size):
                temp.append("addr{0}[{1}]".format(k,i+self.col_addr_size))
            for j in range(self.num_rows):
                temp.append("dec_out{0}[{1}]".format(k,j))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)

    def add_wordline_driver(self):
        """ Wordline Driver """

        self.wordline_driver_inst = [None] * self.total_ports
        
        for k in range(self.total_ports):
            # The wordline driver is placed to the right of the main decoder width.
            x_offset = -(self.central_bus_width + self.wordline_driver.width) + self.m2_pitch
            self.wordline_driver_inst[k]=self.add_inst(name="wordline_driver{}".format(k), 
                                                       mod=self.wordline_driver, 
                                                       offset=vector(x_offset,0))

            temp = []
            for i in range(self.num_rows):
                temp.append("dec_out{0}[{1}]".format(k,i))
            for i in range(self.num_rows):
                temp.append(self.total_wl_list[k]+"[{0}]".format(i))
            temp.append(self.prefix+"clk_buf")
            temp.append("vdd")
            temp.append("gnd")
            self.connect_inst(temp)

        
    def add_column_decoder_module(self):
        """ 
        Create a 2:4 or 3:8 column address decoder.
        """
        
        self.col_decoder_inst = [None] * self.total_ports
        
        for k in range(self.total_ports):
            # Place the col decoder right aligned with row decoder
            x_off = -(self.central_bus_width + self.wordline_driver.width + self.col_decoder.width)
            y_off = -(self.col_decoder.height + 2*drc["well_to_well"])
            self.col_decoder_inst[k]=self.add_inst(name="col_address_decoder{}".format(k), 
                                                   mod=self.col_decoder, 
                                                   offset=vector(x_off,y_off))

            temp = []
            for i in range(self.col_addr_size):
                temp.append("addr{0}[{1}]".format(k,i))
            for j in range(self.num_col_addr_lines):
                temp.append("sel{0}[{1}]".format(k,j))
            temp.extend(["vdd", "gnd"])
            self.connect_inst(temp)
        
    def add_column_decoder(self):
        """ 
        Create a decoder to decode column select lines. This could be an inverter/buffer for 1:2,
        2:4 decoder, or 3:8 decoder.
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
        
        self.add_column_decoder_module()


    def add_bank_select(self):
        """ Instantiate the bank select logic. """

        if not self.num_banks > 1:
            return
        
        x_off = -(self.row_decoder.width + self.central_bus_width + self.wordline_driver.width)
        if self.col_addr_size > 0:
            y_off = min(self.col_decoder_inst[0].by(), self.col_mux_array_inst[0].by())
        else:
            y_off = self.row_decoder_inst[0].by()
        y_off -= (self.bank_select.height + drc["well_to_well"])
        self.bank_select_pos = vector(x_off,y_off)
        self.bank_select_inst = self.add_inst(name="bank_select",
                                              mod=self.bank_select,
                                              offset=self.bank_select_pos)

        temp = []
        temp.extend(self.input_control_signals)
        temp.append("bank_sel")
        temp.extend(self.control_signals)
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def route_vdd_gnd(self):
        """ Propagate all vdd/gnd pins up to this level for all modules """

        # These are the instances that every bank has
        top_instances = [self.bitcell_array_inst,
                         self.precharge_array_inst[0],
                         self.sense_amp_array_inst[0],
                         self.write_driver_array_inst[0],
                         self.row_decoder_inst[0],
                         self.wordline_driver_inst[0]]
        # Add these if we use the part...
        if self.col_addr_size > 0:
            top_instances.append(self.col_decoder_inst[0])
            top_instances.append(self.col_mux_array_inst[0])
            
        if self.num_banks > 1:
            top_instances.append(self.bank_select_inst)

        
        for inst in top_instances:
            # Column mux has no vdd
            if self.col_addr_size==0 or (self.col_addr_size>0 and inst != self.col_mux_array_inst[0]):
                self.copy_layout_pin(inst, "vdd")
            # Precharge has no gnd
            if inst != self.precharge_array_inst[0]:
                self.copy_layout_pin(inst, "gnd")
        
    def route_bank_select(self):
        """ Route the bank select logic. """
        for input_name in self.input_control_signals+["bank_sel"]:
            self.copy_layout_pin(self.bank_select_inst, input_name)

        for gated_name in self.control_signals:
            # Connect the inverter output to the central bus
            out_pos = self.bank_select_inst.get_pin(gated_name).rc()
            bus_pos = vector(self.bus_xoffset[gated_name].x, out_pos.y)
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
        
    
    def setup_layout_constraints(self):
        """ After the modules are instantiated, find the dimensions for the
        control bus, power ring, etc. """

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
        self.max_y_offset = self.precharge_array_inst[0].uy() + 3*self.m1_width
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
        control_bus_offset = vector(-self.m2_pitch * self.num_control_lines - self.m2_width, self.min_y_offset)
        control_bus_length = self.max_y_offset - self.min_y_offset
        self.bus_xoffset = self.create_bus(layer="metal2",
                                           pitch=self.m2_pitch,
                                           offset=control_bus_offset,
                                           names=self.control_signals,
                                           length=control_bus_length,
                                           vertical=True,
                                           make_pins=(self.num_banks==1))



    def route_precharge_to_bitcell_array(self):
        """ Routing of BL and BR between pre-charge and bitcell array """
        
        for k in range(self.total_read):
            for i in range(self.num_cols):
                precharge_bl = self.precharge_array_inst[k].get_pin("bl[{}]".format(i)).bc()
                precharge_br = self.precharge_array_inst[k].get_pin("br[{}]".format(i)).bc()
                bitcell_bl = self.bitcell_array_inst.get_pin(self.read_bl_list[k]+"[{}]".format(i)).uc()
                bitcell_br = self.bitcell_array_inst.get_pin(self.read_br_list[k]+"[{}]".format(i)).uc()

                yoffset = 0.5*(precharge_bl.y+bitcell_bl.y)
                self.add_path("metal2",[precharge_bl, vector(precharge_bl.x,yoffset),
                                        vector(bitcell_bl.x,yoffset), bitcell_bl])
                self.add_path("metal2",[precharge_br, vector(precharge_br.x,yoffset),
                                        vector(bitcell_br.x,yoffset), bitcell_br])


    def route_col_mux_to_bitcell_array(self):
        """ Routing of BL and BR between col mux and bitcell array """

        # Only do this if we have a column mux!
        if self.col_addr_size==0:
            return
        
        for k in range(self.total_ports):
            for i in range(self.num_cols):
                col_mux_bl = self.col_mux_array_inst[k].get_pin("bl[{}]".format(i)).uc()
                col_mux_br = self.col_mux_array_inst[k].get_pin("br[{}]".format(i)).uc()
                bitcell_bl = self.bitcell_array_inst.get_pin(self.total_bl_list[k]+"[{}]".format(i)).bc()
                bitcell_br = self.bitcell_array_inst.get_pin(self.total_br_list[k]+"[{}]".format(i)).bc()

                yoffset = 0.5*(col_mux_bl.y+bitcell_bl.y)
                self.add_path("metal2",[col_mux_bl, vector(col_mux_bl.x,yoffset),
                                        vector(bitcell_bl.x,yoffset), bitcell_bl])
                self.add_path("metal2",[col_mux_br, vector(col_mux_br.x,yoffset),
                                        vector(bitcell_br.x,yoffset), bitcell_br])
        
    def route_sense_amp_to_col_mux_or_bitcell_array(self):
        """ Routing of BL and BR between sense_amp and column mux or bitcell array """

        for k in range(self.total_read):
            for i in range(self.word_size):
                sense_amp_bl = self.sense_amp_array_inst[k].get_pin("bl[{}]".format(i)).uc()
                sense_amp_br = self.sense_amp_array_inst[k].get_pin("br[{}]".format(i)).uc()

                if self.col_addr_size>0:
                    # Sense amp is connected to the col mux
                    connect_bl = self.col_mux_array_inst[k].get_pin("bl_out[{}]".format(i)).bc()
                    connect_br = self.col_mux_array_inst[k].get_pin("br_out[{}]".format(i)).bc()
                else:
                    # Sense amp is directly connected to the bitcell array
                    connect_bl = self.bitcell_array_inst.get_pin(self.read_bl_list[k]+"[{}]".format(i)).bc()
                    connect_br = self.bitcell_array_inst.get_pin(self.read_br_list[k]+"[{}]".format(i)).bc()
                
                    
                yoffset = 0.5*(sense_amp_bl.y+connect_bl.y)
                self.add_path("metal2",[sense_amp_bl, vector(sense_amp_bl.x,yoffset),
                                        vector(connect_bl.x,yoffset), connect_bl])
                self.add_path("metal2",[sense_amp_br, vector(sense_amp_br.x,yoffset),
                                        vector(connect_br.x,yoffset), connect_br])
            
            
    def route_sense_amp_out(self):
        """ Add pins for the sense amp output """
        for i in range(self.word_size):
            data_pin = self.sense_amp_array_inst[0].get_pin("data[{}]".format(i))
            self.add_layout_pin_rect_center(text="dout0[{}]".format(i),
                                            layer=data_pin.layer, 
                                            offset=data_pin.center(),
                                            height=data_pin.height(),
                                            width=data_pin.width()),
        

    def route_row_decoder(self):
        """ Routes the row decoder inputs and supplies """

        # Create inputs for the row address lines
        for i in range(self.row_addr_size):
            addr_idx = i + self.col_addr_size
            decoder_name = "addr[{}]".format(i)
            addr_name = "addr0[{}]".format(addr_idx)
            self.copy_layout_pin(self.row_decoder_inst[0], decoder_name, addr_name)
            
            
    def route_write_driver(self):
        """ Connecting write driver   """
        
        for i in range(self.word_size):
            data_name = "data[{}]".format(i)            
            din_name = "din0[{}]".format(i)
            self.copy_layout_pin(self.write_driver_array_inst[0], data_name, din_name)
                        

    
    def route_wordline_driver(self):
        """ Connecting Wordline driver output to Bitcell WL connection  """

        for k in range(self.total_read):
            # we don't care about bends after connecting to the input pin, so let the path code decide.
            for i in range(self.num_rows):
                # The pre/post is to access the pin from "outside" the cell to avoid DRCs
                decoder_out_pos = self.row_decoder_inst[k].get_pin("decode[{}]".format(i)).rc()
                driver_in_pos = self.wordline_driver_inst[k].get_pin("in[{}]".format(i)).lc()
                mid1 = decoder_out_pos.scale(0.5,1)+driver_in_pos.scale(0.5,0)
                mid2 = decoder_out_pos.scale(0.5,0)+driver_in_pos.scale(0.5,1)
                self.add_path("metal1", [decoder_out_pos, mid1, mid2, driver_in_pos])

                # The mid guarantees we exit the input cell to the right.
                driver_wl_pos = self.wordline_driver_inst[k].get_pin("wl[{}]".format(i)).rc()
                bitcell_wl_pos = self.bitcell_array_inst.get_pin(self.total_wl_list[k]+"[{}]".format(i)).lc()
                mid1 = driver_wl_pos.scale(0.5,1)+bitcell_wl_pos.scale(0.5,0)
                mid2 = driver_wl_pos.scale(0.5,0)+bitcell_wl_pos.scale(0.5,1)
                self.add_path("metal1", [driver_wl_pos, mid1, mid2, bitcell_wl_pos])

        

    def route_column_address_lines(self):
        """ Connecting the select lines of column mux to the address bus """
        if not self.col_addr_size>0:
            return

        

        if self.col_addr_size == 1:
            
            # Connect to sel[0] and sel[1]
            decode_names = ["Zb", "Z"]
            
            # The Address LSB
            self.copy_layout_pin(self.col_decoder_inst[0], "A", "addr0[0]") 
            
        elif self.col_addr_size > 1:
            decode_names = []
            for i in range(self.num_col_addr_lines):
                decode_names.append("out[{}]".format(i))

            for i in range(self.col_addr_size):
                decoder_name = "in[{}]".format(i)
                addr_name = "addr0[{}]".format(i)
                self.copy_layout_pin(self.col_decoder_inst[0], decoder_name, addr_name)
                

        # This will do a quick "river route" on two layers.
        # When above the top select line it will offset "inward" again to prevent conflicts.
        # This could be done on a single layer, but we follow preferred direction rules for later routing.
        top_y_offset = self.col_mux_array_inst[0].get_pin("sel[{}]".format(self.num_col_addr_lines-1)).cy()
        for (decode_name,i) in zip(decode_names,range(self.num_col_addr_lines)):
            mux_name = "sel[{}]".format(i)
            mux_addr_pos = self.col_mux_array_inst[0].get_pin(mux_name).lc()
            
            decode_out_pos = self.col_decoder_inst[0].get_pin(decode_name).center()

            # To get to the edge of the decoder and one track out
            delta_offset = self.col_decoder_inst[0].rx() - decode_out_pos.x + self.m2_pitch
            if decode_out_pos.y > top_y_offset:
                mid1_pos = vector(decode_out_pos.x + delta_offset + i*self.m2_pitch,decode_out_pos.y)
            else:
                mid1_pos = vector(decode_out_pos.x + delta_offset + (self.num_col_addr_lines-i)*self.m2_pitch,decode_out_pos.y)
            mid2_pos = vector(mid1_pos.x,mux_addr_pos.y)
            #self.add_wire(("metal1","via1","metal2"),[decode_out_pos, mid1_pos, mid2_pos, mux_addr_pos])
            self.add_path("metal1",[decode_out_pos, mid1_pos, mid2_pos, mux_addr_pos])
            

            


    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # Add the wordline names
        for i in range(self.num_rows):
            wl_name = "wl[{}]".format(i)
            wl_pin = self.bitcell_array_inst.get_pin(wl_name)
            self.add_label(text=wl_name,
                           layer="metal1",  
                           offset=wl_pin.center())
        
        # Add the bitline names
        for i in range(self.num_cols):
            bl_name = "bl[{}]".format(i)
            br_name = "br[{}]".format(i)
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
        #     data_name = "data[{}]".format(i)
        #     data_pin = self.sense_amp_array_inst.get_pin(data_name)
        #     self.add_label(text="sa_out[{}]".format(i),
        #                    layer="metal2",  
        #                    offset=data_pin.center())

        # Add labels on the decoder
        for i in range(self.word_size):
            data_name = "dec_out[{}]".format(i)
            pin_name = "in[{}]".format(i)            
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
        connection = []
        connection.append((self.prefix+"clk_buf_bar", self.precharge_array_inst[0].get_pin("en").lc()))
        connection.append((self.prefix+"w_en0", self.write_driver_array_inst[0].get_pin("en").lc()))
        connection.append((self.prefix+"s_en0", self.sense_amp_array_inst[0].get_pin("en").lc()))
  
        for (control_signal, pin_pos) in connection:
            control_pos = vector(self.bus_xoffset[control_signal].x ,pin_pos.y)
            self.add_path("metal1", [control_pos, pin_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=control_pos,
                                rotate=90)

        # clk to wordline_driver
        control_signal = self.prefix+"clk_buf"
        pin_pos = self.wordline_driver_inst[0].get_pin("en").uc()
        mid_pos = pin_pos + vector(0,self.m1_pitch)
        control_x_offset = self.bus_xoffset[control_signal].x
        control_pos = vector(control_x_offset + self.m1_width, mid_pos.y)
        self.add_wire(("metal1","via1","metal2"),[pin_pos, mid_pos, control_pos])
        control_via_pos = vector(control_x_offset, mid_pos.y)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=control_via_pos,
                            rotate=90)
        

        
    def analytical_delay(self, slew, load):
        """ return  analytical delay of the bank"""
        decoder_delay = self.row_decoder.analytical_delay(slew, self.wordline_driver.input_load())

        word_driver_delay = self.wordline_driver.analytical_delay(decoder_delay.slew, self.bitcell_array.input_load())

        bitcell_array_delay = self.bitcell_array.analytical_delay(word_driver_delay.slew)

        bl_t_data_out_delay = self.sense_amp_array.analytical_delay(bitcell_array_delay.slew,
                                                                    self.bitcell_array.output_load())
        # output load of bitcell_array is set to be only small part of bl for sense amp.

        result = decoder_delay + word_driver_delay + bitcell_array_delay + bl_t_data_out_delay 
        return result
        
