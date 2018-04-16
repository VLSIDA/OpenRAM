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

        mod_list = ["tri_gate", "bitcell", "decoder", "ms_flop_array", "wordline_driver",
                    "bitcell_array",   "sense_amp_array",    "precharge_array",
                    "column_mux_array", "write_driver_array", "tri_gate_array",
                    "bank_select"]
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
        self.add_lvs_correspondence_points() 

        self.offset_all_coordinates()
        
        self.DRC_LVS()

    def add_pins(self):
        """ Adding pins for Bank module"""
        for i in range(self.word_size):
            self.add_pin("DOUT[{0}]".format(i),"OUT")
        for i in range(self.word_size):
            self.add_pin("DIN[{0}]".format(i),"IN")
        for i in range(self.addr_size):
            self.add_pin("A[{0}]".format(i),"INPUT")

        # For more than one bank, we have a bank select and name
        # the signals gated_*.
        if self.num_banks > 1:
            self.add_pin("bank_sel","INPUT")
        for pin in ["s_en","w_en","tri_en_bar","tri_en",
                    "clk_buf_bar","clk_buf"]:
            self.add_pin(pin,"INPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

    def route_layout(self):
        """ Create routing amoung the modules """
        self.route_central_bus()
        self.route_precharge_to_bitcell_array()
        self.route_sense_amp_to_trigate()
        self.route_tri_gate_out()
        self.route_wordline_driver()
        self.route_row_decoder()
        self.route_column_address_lines()
        self.route_control_lines()
        self.add_control_pins()
        if self.num_banks > 1:
            self.route_bank_select()            
        
        self.route_vdd_gnd()
        #self.route_vdd_supply()
        #self.route_gnd_supply()
        
    def add_modules(self):
        """ Add modules. The order should not matter! """

        # Above the bitcell array
        self.add_bitcell_array()
        self.add_precharge_array()
        
        # Below the bitcell array
        if self.col_addr_size > 0:
            # The m2 width is because the 6T cell may have vias on the boundary edge for
            # overlapping when making the array
            self.column_mux_height = self.column_mux_array.height + 0.5*self.m2_width
            self.add_column_mux_array()
        else:
            self.column_mux_height = 0
        self.add_sense_amp_array()
        self.add_write_driver_array()
        self.add_tri_gate_array()

        # To the left of the bitcell array
        self.add_row_decoder()
        self.add_wordline_driver()
        self.add_column_decoder()

        

    def compute_sizes(self):
        """  Computes the required sizes to create the bank """

        self.num_cols = self.words_per_row*self.word_size
        self.num_rows = self.num_words / self.words_per_row

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
        self.num_control_lines = 6
        # The order of the control signals on the control bus:
        self.input_control_signals = ["clk_buf", "tri_en_bar", "tri_en", "clk_buf_bar", "w_en", "s_en"]
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

        # M1/M2 routing pitch is based on contacted pitch
        self.m1_pitch = contact.m1m2.height + max(self.m1_space,self.m2_space)
        self.m2_pitch = contact.m2m3.height + max(self.m2_space,self.m3_space)

        # The width of this bus is needed to place other modules (e.g. decoder)
        # A width on each side too
        self.central_bus_width = self.m2_pitch * self.num_control_lines + 2*self.m2_width




    def create_modules(self):
        """ Create all the modules using the class loader """
        self.tri = self.mod_tri_gate()
        self.bitcell = self.mod_bitcell()
        
        self.bitcell_array = self.mod_bitcell_array(cols=self.num_cols,
                                                    rows=self.num_rows)
        self.add_mod(self.bitcell_array)

        self.precharge_array = self.mod_precharge_array(columns=self.num_cols)
        self.add_mod(self.precharge_array)

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
        
        self.tri_gate_array = self.mod_tri_gate_array(columns=self.num_cols, 
                                                      word_size=self.word_size)
        self.add_mod(self.tri_gate_array)

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
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for j in range(self.num_rows):
            temp.append("wl[{0}]".format(j))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

            

    def add_precharge_array(self):
        """ Adding Precharge """

        # The wells must be far enough apart
        # The enclosure is for the well and the spacing is to the bitcell wells
        y_offset = self.bitcell_array.height + 2*drc["pwell_to_nwell"] + drc["well_enclosure_active"]
        self.precharge_array_inst=self.add_inst(name="precharge_array",
                                                mod=self.precharge_array, 
                                                offset=vector(0,y_offset))
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        temp.extend([self.prefix+"clk_buf_bar", "vdd"])
        self.connect_inst(temp)

    def add_column_mux_array(self):
        """ Adding Column Mux when words_per_row > 1 . """

        y_offset = self.column_mux_height
        self.col_mux_array_inst=self.add_inst(name="column_mux_array",
                                              mod=self.column_mux_array,
                                              offset=vector(0,y_offset).scale(-1,-1))
        temp = []
        for i in range(self.num_cols):
            temp.append("bl[{0}]".format(i))
            temp.append("br[{0}]".format(i))
        for k in range(self.words_per_row):
                temp.append("sel[{0}]".format(k))
        for j in range(self.word_size):
            temp.append("bl_out[{0}]".format(j))
            temp.append("br_out[{0}]".format(j))
        temp.append("gnd")
        self.connect_inst(temp)

    def add_sense_amp_array(self):
        """ Adding Sense amp  """

        y_offset = self.column_mux_height + self.sense_amp_array.height
        self.sense_amp_array_inst=self.add_inst(name="sense_amp_array",
                                                mod=self.sense_amp_array,
                                                offset=vector(0,y_offset).scale(-1,-1))
        temp = []
        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
            if self.words_per_row == 1:
                temp.append("bl[{0}]".format(i))
                temp.append("br[{0}]".format(i))
            else:
                temp.append("bl_out[{0}]".format(i))
                temp.append("br_out[{0}]".format(i))
                
        temp.extend([self.prefix+"s_en", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_write_driver_array(self):
        """ Adding Write Driver  """

        y_offset = self.sense_amp_array.height + self.column_mux_height + self.write_driver_array.height
        self.write_driver_array_inst=self.add_inst(name="write_driver_array", 
                                                   mod=self.write_driver_array, 
                                                   offset=vector(0,y_offset).scale(-1,-1))

        temp = []
        for i in range(self.word_size):
            temp.append("DIN[{0}]".format(i))
        for i in range(self.word_size):            
            if (self.words_per_row == 1):            
                temp.append("bl[{0}]".format(i))
                temp.append("br[{0}]".format(i))
            else:
                temp.append("bl_out[{0}]".format(i))
                temp.append("br_out[{0}]".format(i))
        temp.extend([self.prefix+"w_en", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_tri_gate_array(self):
        """ data tri gate to drive the data bus """
        y_offset = self.sense_amp_array.height+self.column_mux_height \
                   + self.write_driver_array.height + self.tri_gate_array.height
        self.tri_gate_array_inst=self.add_inst(name="tri_gate_array", 
                                              mod=self.tri_gate_array, 
                                               offset=vector(0,y_offset).scale(-1,-1))
                  
        temp = []
        for i in range(self.word_size):
            temp.append("data_out[{0}]".format(i))
        for i in range(self.word_size):
            temp.append("DOUT[{0}]".format(i))
        temp.extend([self.prefix+"tri_en", self.prefix+"tri_en_bar", "vdd", "gnd"])
        self.connect_inst(temp)

    def add_row_decoder(self):
        """  Add the hierarchical row decoder  """

        
        # The address and control bus will be in between decoder and the main memory array 
        # This bus will route address bits to the decoder input and column mux inputs. 
        # The wires are actually routed after we placed the stuff on both sides.
        # The predecoder is below the x-axis and the main decoder is above the x-axis
        # The address flop and decoder are aligned in the x coord.
        
        x_offset = -(self.row_decoder.width + self.central_bus_width + self.wordline_driver.width)
        self.row_decoder_inst=self.add_inst(name="row_decoder", 
                                            mod=self.row_decoder, 
                                            offset=vector(x_offset,0))

        temp = []
        for i in range(self.row_addr_size):
            temp.append("A[{0}]".format(i+self.col_addr_size))
        for j in range(self.num_rows):
            temp.append("dec_out[{0}]".format(j))
        temp.extend(["vdd", "gnd"])
        self.connect_inst(temp)

    def add_wordline_driver(self):
        """ Wordline Driver """

        # The wordline driver is placed to the right of the main decoder width.
        x_offset = -(self.central_bus_width + self.wordline_driver.width) + self.m2_pitch
        self.wordline_driver_inst=self.add_inst(name="wordline_driver", 
                                                mod=self.wordline_driver, 
                                                offset=vector(x_offset,0))

        temp = []
        for i in range(self.num_rows):
            temp.append("dec_out[{0}]".format(i))
        for i in range(self.num_rows):
            temp.append("wl[{0}]".format(i))
        temp.append(self.prefix+"clk_buf")
        temp.append("vdd")
        temp.append("gnd")
        self.connect_inst(temp)

        
    def add_column_decoder_module(self):
        """ 
        Create a 2:4 or 3:8 column address decoder.
        """
        # Place the col decoder aligned left to row decoder
        x_off = -(self.row_decoder.width + self.central_bus_width + self.wordline_driver.width)
        y_off = -(self.col_decoder.height + 2*drc["well_to_well"])
        self.col_decoder_inst=self.add_inst(name="col_address_decoder", 
                                            mod=self.col_decoder, 
                                            offset=vector(x_off,y_off))

        temp = []
        for i in range(self.col_addr_size):
            temp.append("A[{0}]".format(i))
        for j in range(self.num_col_addr_lines):
            temp.append("sel[{0}]".format(j))
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
            self.col_decoder = pinvbuf()
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
        # extra space to allow vias
        y_off = self.min_point + 2*self.supply_rail_pitch + self.m1_space
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
                         self.precharge_array_inst,
                         self.sense_amp_array_inst,
                         self.write_driver_array_inst,
                         self.tri_gate_array_inst,
                         self.row_decoder_inst,
                         self.wordline_driver_inst]
        # Add these if we use the part...
        if self.col_addr_size > 0:
            top_instances.append(self.col_decoder_inst)
            top_instances.append(self.col_mux_array_inst)
            
        if self.num_banks > 1:
            top_instances.append(self.bank_select_inst)

        
        for inst in top_instances:
            # These copy all pins if more thanone
            self.copy_layout_pin(inst, "vdd")
            # Precharge has no gnd
            if inst != self.precharge_array_inst:
                self.copy_layout_pin(inst, "gnd")
        
    def route_bank_select(self):
        """ Route the bank select logic. """
        for input_name in self.input_control_signals+["bank_sel"]:
            in_pos = self.bank_select_inst.get_pin(input_name).lc()
            self.add_layout_pin_segment_center(text=input_name,
                                               layer="metal3",
                                               start=vector(self.left_gnd_x_offset,in_pos.y),
                                               end=in_pos)

        for gated_name in self.control_signals:
            # Connect the inverter output to the central bus
            out_pos = self.bank_select_inst.get_pin(gated_name).rc()
            bus_pos = vector(self.bus_xoffset[gated_name], out_pos.y)
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
        #the column decoder (if there is one) or the tristate output
        #driver.
        # Leave room for the output below the tri gate.
        tri_gate_min_y_offset = self.tri_gate_array_inst.by() - 3*self.m2_pitch
        row_decoder_min_y_offset = self.row_decoder_inst.by()
        if self.col_addr_size > 0:
            col_decoder_min_y_offset = self.col_decoder_inst.by()
        else:
            col_decoder_min_y_offset = row_decoder_min_y_offset
        
        if self.num_banks>1:
            # The control gating logic is below the decoder
            # Min of the control gating logic and tri gate.
            self.min_y_offset = min(col_decoder_min_y_offset - self.bank_select.height, tri_gate_min_y_offset)
        else:
            # Just the min of the decoder logic logic and tri gate.            
            self.min_y_offset = min(col_decoder_min_y_offset, tri_gate_min_y_offset)

        # The max point is always the top of the precharge bitlines
        # Add a vdd and gnd power rail above the array
        self.max_y_offset = self.precharge_array_inst.uy() + 3*self.m1_width
        self.max_x_offset = self.bitcell_array_inst.ur().x + 3*self.m1_width
        self.min_x_offset = self.row_decoder_inst.lx() 
        
        # Create the core bbox for the power rings
        ur = vector(self.max_x_offset, self.max_y_offset)
        ll = vector(self.min_x_offset, self.min_y_offset)
        self.core_bbox = [ll, ur]
        self.add_power_ring(self.core_bbox)
        
        # Compute the vertical rail positions for later use
        self.right_gnd_x_offset = self.right_gnd_x_center - 0.5*self.supply_rail_pitch
        self.right_vdd_x_offset = self.right_gnd_x_offset + self.supply_rail_pitch
        self.left_vdd_x_offset =  self.left_gnd_x_center - 0.5*self.supply_rail_pitch
        self.left_gnd_x_offset = self.left_vdd_x_offset - self.supply_rail_pitch
        
        # Have the pins go below the vdd and gnd power rail at the bottom
        self.min_y_offset -= 2*self.supply_rail_pitch

        self.height = ur.y - ll.y + 4*self.supply_rail_pitch
        self.width = ur.x - ll.x + 4*self.supply_rail_pitch
        
        
        

    def route_central_bus(self):
        """ Create the address, supply, and control signal central bus lines. """

        # Overall central bus width. It includes all the column mux lines,
        # and control lines.
        # The bank is at (0,0), so this is to the left of the y-axis.
        # 2 pitches on the right for vias/jogs to access the inputs 
        control_bus_x_offset = -self.m2_pitch * self.num_control_lines - self.m2_width
        
        # Track the bus offsets for other modules to access
        self.bus_xoffset = {}

        # Control lines 
        for i in range(self.num_control_lines):
            x_offset = control_bus_x_offset + i*self.m2_pitch 
            # Make the xoffset map the center of the rail
            self.bus_xoffset[self.control_signals[i]]=x_offset + 0.5*self.m2_width
            # Pins are added later if this is a single bank, so just add rectangle now
            self.add_rect(layer="metal2",  
                          offset=vector(x_offset, self.min_y_offset), 
                          width=self.m2_width, 
                          height=self.max_y_offset-self.min_y_offset)



    def route_precharge_to_bitcell_array(self):
        """ Routing of BL and BR between pre-charge and bitcell array """

        for i in range(self.num_cols):
            precharge_bl = self.precharge_array_inst.get_pin("bl[{}]".format(i)).bc()
            precharge_br = self.precharge_array_inst.get_pin("br[{}]".format(i)).bc()
            bitcell_bl = self.bitcell_array_inst.get_pin("bl[{}]".format(i)).uc()
            bitcell_br = self.bitcell_array_inst.get_pin("br[{}]".format(i)).uc()

            self.add_path("metal2",[precharge_bl,bitcell_bl])
            self.add_path("metal2",[precharge_br,bitcell_br])

    def route_sense_amp_to_trigate(self):
        """ Routing of sense amp output to tri_gate input """

        for i in range(self.word_size):
            # Connection of data_out of sense amp to data_in 
            tri_gate_in = self.tri_gate_array_inst.get_pin("in[{}]".format(i)).uc()
            sa_data_out = self.sense_amp_array_inst.get_pin("data[{}]".format(i)).bc()
            
            self.add_path("metal2",[sa_data_out,tri_gate_in])
            # # if we need a bend or not
            # if tri_gate_in.x-sa_data_out.x>self.m2_pitch:
            #     # We'll connect to the bottom of the SA pin
            #     bendX = sa_data_out.x
            # else:
            #     # We'll connect to the left of the SA pin
            #     sa_data_out = self.sense_amp_array_inst.get_pin("data[{}]".format(i)).lc()
            #     bendX = tri_gate_in.x - 3*self.m3_width

            # bendY = tri_gate_in.y - 2*self.m2_width

            # # Connection point of M2 and M3 paths, below the tri gate and
            # # to the left of the tri gate input
            # bend = vector(bendX, bendY)

            # # Connect an M2 path to the gate
            # mid3 = [tri_gate_in.x, bendY] # guarantee down then left
            # self.add_path("metal2", [bend, mid3, tri_gate_in])

            # # connect up then right to sense amp
            # mid1 = vector(bendX,sa_data_out.y)
            # self.add_path("metal3", [bend, mid1, sa_data_out])


            # offset = bend - vector([0.5*drc["minwidth_metal3"]] * 2)
            # self.add_via(("metal2", "via2", "metal3"),offset)

    def route_tri_gate_out(self):
        """ Metal 3 routing of tri_gate output data """
        for i in range(self.word_size):
            data_pin = self.tri_gate_array_inst.get_pin("out[{}]".format(i))
            self.add_layout_pin_rect_center(text="DATA[{}]".format(i),
                                            layer="metal2", 
                                            offset=data_pin.center(),
                                            height=data_pin.height(),
                                            width=data_pin.width()),


    def route_row_decoder(self):
        """ Routes the row decoder inputs and supplies """

        # Create inputs for the row address lines
        for i in range(self.row_addr_size):
            addr_idx = i + self.col_addr_size
            decoder_name = "A[{}]".format(i)
            addr_name = "A[{}]".format(addr_idx)
            self.copy_layout_pin(self.row_decoder_inst, decoder_name, addr_name)
            
            
                        

    
    def route_wordline_driver(self):
        """ Connecting Wordline driver output to Bitcell WL connection  """
        
        # we don't care about bends after connecting to the input pin, so let the path code decide.
        for i in range(self.num_rows):
            # The pre/post is to access the pin from "outside" the cell to avoid DRCs
            decoder_out_pos = self.row_decoder_inst.get_pin("decode[{}]".format(i)).rc()
            driver_in_pos = self.wordline_driver_inst.get_pin("in[{}]".format(i)).lc()
            mid1 = decoder_out_pos.scale(0.5,1)+driver_in_pos.scale(0.5,0)
            mid2 = decoder_out_pos.scale(0.5,0)+driver_in_pos.scale(0.5,1)
            self.add_path("metal1", [decoder_out_pos, mid1, mid2, driver_in_pos])

            # The mid guarantees we exit the input cell to the right.
            driver_wl_pos = self.wordline_driver_inst.get_pin("wl[{}]".format(i)).rc()
            bitcell_wl_pos = self.bitcell_array_inst.get_pin("wl[{}]".format(i)).lc()
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
            self.copy_layout_pin(self.col_decoder_inst, "A", "A[0]") 
            
        elif self.col_addr_size > 1:
            decode_names = []
            for i in range(self.num_col_addr_lines):
                decode_names.append("out[{}]".format(i))

            for i in range(self.col_addr_size):
                decoder_name = "in[{}]".format(i)
                addr_name = "A[{}]".format(i)
                self.copy_layout_pin(self.col_decoder_inst, decoder_name, addr_name)
                

        # This will do a quick "river route" on two layers.
        # When above the top select line it will offset "inward" again to prevent conflicts.
        # This could be done on a single layer, but we follow preferred direction rules for later routing.
        top_y_offset = self.col_mux_array_inst.get_pin("sel[{}]".format(self.num_col_addr_lines-1)).cy()
        for (decode_name,i) in zip(decode_names,range(self.num_col_addr_lines)):
            mux_name = "sel[{}]".format(i)
            mux_addr_pos = self.col_mux_array_inst.get_pin(mux_name).lc()
            
            decode_out_pos = self.col_decoder_inst.get_pin(decode_name).center()

            # To get to the edge of the decoder and one track out
            delta_offset = self.col_decoder_inst.rx() - decode_out_pos.x + self.m2_pitch
            if decode_out_pos.y > top_y_offset:
                mid1_pos = vector(decode_out_pos.x + delta_offset + i*self.m2_pitch,decode_out_pos.y)
            else:
                mid1_pos = vector(decode_out_pos.x + delta_offset + (self.num_col_addr_lines-i)*self.m2_pitch,decode_out_pos.y)
            mid2_pos = vector(mid1_pos.x,mux_addr_pos.y)
            self.add_wire(("metal1","via1","metal2"),[decode_out_pos, mid1_pos, mid2_pos, mux_addr_pos])
            

            


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
                           offset=wl_pin.ll())
        
        # Add the bitline names
        for i in range(self.num_cols):
            bl_name = "bl[{}]".format(i)
            br_name = "br[{}]".format(i)
            bl_pin = self.bitcell_array_inst.get_pin(bl_name)
            br_pin = self.bitcell_array_inst.get_pin(br_name)
            self.add_label(text=bl_name,
                           layer="metal2",  
                           offset=bl_pin.ll())
            self.add_label(text=br_name,
                           layer="metal2",  
                           offset=br_pin.ll())

        # Add the data output names to the sense amp output     
        for i in range(self.word_size):
            data_name = "data[{}]".format(i)
            data_pin = self.sense_amp_array_inst.get_pin(data_name)
            self.add_label(text="data_out[{}]".format(i),
                           layer="metal3",  
                           offset=data_pin.ll())
            
            
    def route_control_lines(self):
        """ Route the control lines of the entire bank """
        
        # Make a list of tuples that we will connect.
        # From control signal to the module pin 
        # Connection from the central bus to the main control block crosses
        # pre-decoder and this connection is in metal3
        connection = []
        connection.append((self.prefix+"tri_en_bar", self.tri_gate_array_inst.get_pin("en_bar").lc()))
        connection.append((self.prefix+"tri_en", self.tri_gate_array_inst.get_pin("en").lc()))
        connection.append((self.prefix+"clk_buf_bar", self.precharge_array_inst.get_pin("en").lc()))
        connection.append((self.prefix+"w_en", self.write_driver_array_inst.get_pin("en").lc()))
        connection.append((self.prefix+"s_en", self.sense_amp_array_inst.get_pin("en").lc()))
  
        for (control_signal, pin_pos) in connection:
            control_pos = vector(self.bus_xoffset[control_signal], pin_pos.y)
            self.add_path("metal1", [control_pos, pin_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=control_pos,
                                rotate=90)

        # clk to wordline_driver
        control_signal = self.prefix+"clk_buf"
        pin_pos = self.wordline_driver_inst.get_pin("en").uc()
        mid_pos = pin_pos + vector(0,self.m1_pitch)
        control_x_offset = self.bus_xoffset[control_signal]
        control_pos = vector(control_x_offset + self.m1_width, mid_pos.y)
        self.add_wire(("metal1","via1","metal2"),[pin_pos, mid_pos, control_pos])
        control_via_pos = vector(control_x_offset, mid_pos.y)
        self.add_via_center(layers=("metal1", "via1", "metal2"),
                            offset=control_via_pos,
                            rotate=90)
        

    def route_vdd_supply(self):
        """ Route vdd for the precharge, sense amp, write_driver, data FF, tristate """

        # Route the vdd rails to the RIGHT
        modules = [self.precharge_array_inst, self.sense_amp_array_inst,
                   self.write_driver_array_inst, 
                   self.tri_gate_array_inst]
        for inst in modules:
            for vdd_pin in inst.get_pins("vdd"):
                self.add_rect(layer="metal1", 
                              offset=vdd_pin.ll(), 
                              width=self.right_vdd_x_center, 
                              height=vdd_pin.height())
                via_position = vector(self.right_vdd_x_center, vdd_pin.cy())
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=via_position,
                                    size = (1,self.supply_vias),
                                    rotate=90)
                        
        # Route the vdd rails to the LEFT
        for vdd_pin in self.wordline_driver_inst.get_pins("vdd"):
            vdd_pos = vdd_pin.rc()
            left_rail_pos = vector(self.left_vdd_x_center, vdd_pos.y)
            right_rail_pos = vector(self.right_vdd_x_center, vdd_pos.y)
            self.add_path("metal1", [left_rail_pos, right_rail_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=left_rail_pos,
                                size = (1,self.supply_vias),
                                rotate=90)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=right_rail_pos,
                                size = (1,self.supply_vias),
                                rotate=90)

        if self.num_banks>1:
            for vdd_pin in self.bank_select_inst.get_pins("vdd"):
                vdd_pos = vdd_pin.rc()
                left_rail_pos = vector(self.left_vdd_x_center, vdd_pos.y)
                self.add_path("metal1", [left_rail_pos, vdd_pos])
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_rail_pos,
                                    size = (1,self.supply_vias),
                                    rotate=90)
            

    def route_gnd_supply(self):
        """ Route gnd rails"""
        # Route the gnd rails to the RIGHT
        # precharge is connected by abutment
        modules = [ self.tri_gate_array_inst, self.sense_amp_array_inst, self.write_driver_array_inst]
        for inst in modules:
            for gnd_pin in inst.get_pins("gnd"):
                if gnd_pin.layer != "metal1":
                    continue
                # route to the right hand side of the big rail to reduce via overlaps
                pin_pos = gnd_pin.lc()
                gnd_offset = vector(self.right_gnd_x_offset + self.supply_rail_width, pin_pos.y)
                self.add_path("metal1", [pin_pos, gnd_offset])
                via_position = vector(self.right_gnd_x_center, gnd_pin.cy())
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=via_position,
                                    size = (1,self.supply_vias),
                                    rotate=90)

        # Route the gnd rails to the LEFT
        modules = [self.wordline_driver_inst]
        if self.num_banks>1:
            modules.append(self.bank_select_inst)
        for inst in modules:
            for gnd_pin in inst.get_pins("gnd"):
                gnd_pos = gnd_pin.rc()
                left_rail_pos = vector(self.left_gnd_x_center, gnd_pos.y)
                self.add_path("metal1", [left_rail_pos, gnd_pos])
                self.add_via_center(layers=("metal1", "via1", "metal2"),
                                    offset=left_rail_pos,
                                    size = (1,self.supply_vias),
                                    rotate=90)

    def add_control_pins(self):
        """ Add the control signal input pins """

        for ctrl in self.control_signals:
            # xoffsets are the center of the rail
            x_offset = self.bus_xoffset[ctrl] - 0.5*self.m2_width
            if self.num_banks > 1:
                # it's not an input pin if we have multiple banks
                self.add_label_pin(text=ctrl,
                                    layer="metal2",  
                                    offset=vector(x_offset, self.min_y_offset), 
                                    width=self.m2_width, 
                                    height=self.max_y_offset-self.min_y_offset)
            else:
                self.add_layout_pin(text=ctrl,
                                    layer="metal2",  
                                    offset=vector(x_offset, self.min_y_offset), 
                                    width=self.m2_width, 
                                    height=self.max_y_offset-self.min_y_offset)


    def connect_rail_from_right(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pin = inst.get_pin(pin).lc()
        rail_pos = vector(self.rail_1_x_offsets[rail], in_pin.y)
        self.add_wire(("metal3","via2","metal2"),[in_pin, rail_pos, rail_pos - vector(0,self.m2_pitch)])
        # Bring it up to M2 for M2/M3 routing
        self.add_via(layers=("metal1","via1","metal2"),
                     offset=in_pin + contact.m1m2.offset,
                     rotate=90)
        self.add_via(layers=("metal2","via2","metal3"),
                     offset=in_pin + self.m2m3_via_offset,
                     rotate=90)
        
        
    def connect_rail_from_left(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pin = inst.get_pin(pin).rc()
        rail_pos = vector(self.rail_1_x_offsets[rail], in_pin.y)
        self.add_wire(("metal3","via2","metal2"),[in_pin, rail_pos, rail_pos - vector(0,self.m2_pitch)])
        self.add_via(layers=("metal1","via1","metal2"),
                     offset=in_pin + contact.m1m2.offset,
                     rotate=90)
        self.add_via(layers=("metal2","via2","metal3"),
                     offset=in_pin + self.m2m3_via_offset,
                     rotate=90)
        
    def analytical_delay(self, slew, load):
        """ return  analytical delay of the bank"""
        msf_addr_delay = self.msf_address.analytical_delay(slew, self.row_decoder.input_load())

        decoder_delay = self.row_decoder.analytical_delay(msf_addr_delay.slew, self.wordline_driver.input_load())

        word_driver_delay = self.wordline_driver.analytical_delay(decoder_delay.slew, self.bitcell_array.input_load())

        bitcell_array_delay = self.bitcell_array.analytical_delay(word_driver_delay.slew)

        bl_t_data_out_delay = self.sense_amp_array.analytical_delay(bitcell_array_delay.slew,
                                                                    self.bitcell_array.output_load())
        # output load of bitcell_array is set to be only small part of bl for sense amp.

        data_t_DATA_delay = self.tri_gate_array.analytical_delay(bl_t_data_out_delay.slew, load)

        result = msf_addr_delay + decoder_delay + word_driver_delay \
                 + bitcell_array_delay + bl_t_data_out_delay + data_t_DATA_delay
        return result
        
