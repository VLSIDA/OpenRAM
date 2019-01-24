from math import log
import design
from tech import drc, parameter
import debug
import contact
from sram_factory import factory
import math
from vector import vector
from globals import OPTS
import logical_effort

class control_logic(design.design):
    """
    Dynamically generated Control logic for the total SRAM circuit.
    """

    def __init__(self, num_rows, words_per_row, word_size, sram=None, port_type="rw"):
        """ Constructor """
        name = "control_logic_" + port_type
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(name))
        
        self.sram=sram
        self.num_rows = num_rows
        self.words_per_row = words_per_row
        self.word_size = word_size
        self.port_type = port_type

        self.num_cols = word_size*words_per_row
        self.num_words = num_rows * words_per_row
        
        self.enable_delay_chain_resizing = False
        
        #self.sram=None #disable re-sizing for debugging, FIXME: resizing is not working, needs to be adjusted for new control logic.
        self.wl_timing_tolerance = 1 #Determines how much larger the sen delay should be. Accounts for possible error in model.
        self.parasitic_inv_delay = parameter["min_inv_para_delay"] #Keeping 0 for now until further testing.
        
        if self.port_type == "rw":
            self.num_control_signals = 2
        else:
            self.num_control_signals = 1
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.setup_signal_busses()
        self.add_pins()
        self.add_modules()
        self.create_instances()
        
    def create_layout(self):
        """ Create layout and route between modules """
        self.place_instances()
        self.route_all()
        #self.add_lvs_correspondence_points()
        self.DRC_LVS()


    def add_pins(self):
        """ Add the pins to the control logic module. """
        for pin in self.input_list + ["clk"]:
            self.add_pin(pin,"INPUT")
        for pin in self.output_list:
            self.add_pin(pin,"OUTPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

    def add_modules(self):
        """ Add all the required modules """
        
        dff = factory.create(module_type="dff_buf")
        dff_height = dff.height
        
        self.ctrl_dff_array = factory.create(module_type="dff_buf_array",
                                             rows=self.num_control_signals,
                                             columns=1)
                                             
        self.add_mod(self.ctrl_dff_array)
        
        self.and2 = factory.create(module_type="pand2",
                                   size=4,
                                   height=dff_height)
        self.add_mod(self.and2)
        
        # Special gates: inverters for buffering
        # clk_buf drives a flop for every address and control bit
        clock_fanout = math.log(self.num_words,2) + math.log(self.words_per_row,2)+1 + self.num_control_signals
        self.clkbuf = factory.create(module_type="pdriver",
                                     fanout=clock_fanout,
                                     height=dff_height)
        
        self.add_mod(self.clkbuf)

        # wl_en drives every row in the bank
        self.wl_en_driver = factory.create(module_type="pdriver",
                                           fanout=self.num_rows,
                                           height=dff_height)
        self.add_mod(self.wl_en_driver)

        # w_en drives every write driver
        self.w_en_driver = factory.create(module_type="pdriver",
                                          fanout=self.word_size+8,
                                          height=dff_height)
        self.add_mod(self.w_en_driver)

        # s_en drives every sense amp
        self.s_en_driver = factory.create(module_type="pdriver",
                                          fanout=self.word_size,
                                          height=dff_height)
        self.add_mod(self.s_en_driver)

        # used to generate inverted signals with low fanout 
        self.inv = factory.create(module_type="pinv",
                                              size=1,
                                              height=dff_height)
        self.add_mod(self.inv)

        # p_en_bar drives every column in the bicell array
        self.p_en_bar_driver = factory.create(module_type="pdriver",
                                              neg_polarity=True,
                                              fanout=self.num_cols,
                                              height=dff_height)
        self.add_mod(self.p_en_bar_driver)
        
        if (self.port_type == "rw") or (self.port_type == "r"):
            delay_stages_heuristic, delay_fanout_heuristic = self.get_heuristic_delay_chain_size()
            bitcell_loads = int(math.ceil(self.num_rows / 2.0))
            self.replica_bitline = factory.create(module_type="replica_bitline",
                                                  delay_fanout_list=[delay_fanout_heuristic]*delay_stages_heuristic,
                                                  bitcell_loads=bitcell_loads)

            
            if self.sram != None:
                self.set_sen_wl_delays()
            
            if self.sram != None and self.enable_delay_chain_resizing and not self.does_sen_total_timing_match(): #check condition based on resizing method
                #This resizes to match fall and rise delays, can make the delay chain weird sizes.
                # stage_list = self.get_dynamic_delay_fanout_list(delay_stages_heuristic, delay_fanout_heuristic)
                # self.replica_bitline = replica_bitline(stage_list, bitcell_loads, name="replica_bitline_resized_"+self.port_type)
                
                #This resizes based on total delay. 
                delay_stages, delay_fanout = self.get_dynamic_delay_chain_size(delay_stages_heuristic, delay_fanout_heuristic)
                self.replica_bitline = factory.create(module_type="replica_bitline",
                                                      delay_fanout_list=[delay_fanout]*delay_stages,
                                                      bitcell_loads=bitcell_loads)

                self.sen_delay_rise,self.sen_delay_fall = self.get_delays_to_sen() #get the new timing
                
            self.add_mod(self.replica_bitline)

    def get_heuristic_delay_chain_size(self):
        """Use a basic heuristic to determine the size of the delay chain used for the Sense Amp Enable """
        # FIXME: These should be tuned according to the additional size parameters
        delay_fanout = 3 # This can be anything >=2
        # Delay stages Must be non-inverting
        if self.words_per_row >= 4:
            delay_stages = 8
        elif self.words_per_row == 2:
            delay_stages = 6
        else:
            delay_stages = 4
            
        return (delay_stages, delay_fanout)
        
    def set_sen_wl_delays(self):
        """Set delays for wordline and sense amp enable"""
        self.wl_delay_rise,self.wl_delay_fall = self.get_delays_to_wl()
        self.sen_delay_rise,self.sen_delay_fall = self.get_delays_to_sen()
        self.wl_delay = self.wl_delay_rise+self.wl_delay_fall
        self.sen_delay = self.sen_delay_rise+self.sen_delay_fall
        
    def does_sen_rise_fall_timing_match(self):
        """Compare the relative rise/fall delays of the sense amp enable and wordline"""
        self.set_sen_wl_delays()
        #This is not necessarily more reliable than total delay in some cases.
        if (self.wl_delay_rise*self.wl_timing_tolerance >= self.sen_delay_rise or 
            self.wl_delay_fall*self.wl_timing_tolerance >= self.sen_delay_fall):
            return False
        else:
            return True
    
    def does_sen_total_timing_match(self):
        """Compare the total delays of the sense amp enable and wordline"""
        self.set_sen_wl_delays()
        #The sen delay must always be bigger than than the wl delay. This decides how much larger the sen delay must be before 
        #a re-size is warranted.
        if self.wl_delay*self.wl_timing_tolerance >= self.sen_delay:
            return False
        else:
            return True      
          
    def get_dynamic_delay_chain_size(self, previous_stages, previous_fanout):
        """Determine the size of the delay chain used for the Sense Amp Enable using path delays"""
        from math import ceil
        previous_delay_chain_delay = (previous_fanout+1+self.parasitic_inv_delay)*previous_stages
        debug.info(2, "Previous delay chain produced {} delay units".format(previous_delay_chain_delay))
        
        delay_fanout = 3 # This can be anything >=2
        #The delay chain uses minimum sized inverters. There are (fanout+1)*stages inverters and each
        #inverter adds 1 unit of delay (due to minimum size). This also depends on the pinv value
        required_delay = self.wl_delay*self.wl_timing_tolerance - (self.sen_delay-previous_delay_chain_delay)
        debug.check(required_delay > 0, "Cannot size delay chain to have negative delay")
        delay_stages = ceil(required_delay/(delay_fanout+1+self.parasitic_inv_delay))
        if delay_stages%2 == 1: #force an even number of stages. 
            delay_stages+=1
            #Fanout can be varied as well but is a little more complicated but potentially optimal.
        debug.info(1, "Setting delay chain to {} stages with {} fanout to match {} delay".format(delay_stages, delay_fanout, required_delay))
        return (delay_stages, delay_fanout)
    
    def get_dynamic_delay_fanout_list(self, previous_stages, previous_fanout):
        """Determine the size of the delay chain used for the Sense Amp Enable using path delays"""
        
        previous_delay_chain_delay = (previous_fanout+1+self.parasitic_inv_delay)*previous_stages
        debug.info(2, "Previous delay chain produced {} delay units".format(previous_delay_chain_delay))
        
        fanout_rise = fanout_fall = 2 # This can be anything >=2
        #The delay chain uses minimum sized inverters. There are (fanout+1)*stages inverters and each
        #inverter adds 1 unit of delay (due to minimum size). This also depends on the pinv value
        required_delay_fall = self.wl_delay_fall*self.wl_timing_tolerance - (self.sen_delay_fall-previous_delay_chain_delay/2)
        required_delay_rise = self.wl_delay_rise*self.wl_timing_tolerance - (self.sen_delay_rise-previous_delay_chain_delay/2)
        debug.info(2,"Required delays from chain: fall={}, rise={}".format(required_delay_fall,required_delay_rise))
        
        #The stages need to be equal (or at least a even number of stages with matching rise/fall delays)
        while True:
            stages_fall = self.calculate_stages_with_fixed_fanout(required_delay_fall,fanout_fall)
            stages_rise = self.calculate_stages_with_fixed_fanout(required_delay_rise,fanout_rise)
            debug.info(1,"Fall stages={}, rise stages={}".format(stages_fall,stages_rise))
            if stages_fall == stages_rise: 
                break
            elif abs(stages_fall-stages_rise) == 1:
                break
            #There should also be a condition to make sure the fanout does not get too large.    
            #Otherwise, increase the fanout of delay with the most stages, calculate new stages
            elif stages_fall>stages_rise:
                fanout_fall+=1
            else:
                fanout_rise+=1
        
        total_stages = max(stages_fall,stages_rise)*2
        debug.info(1, "New Delay chain: stages={}, fanout_rise={}, fanout_fall={}".format(total_stages, fanout_rise, fanout_fall))
        
        #Creates interleaved fanout list of rise/fall delays. Assumes fall is the first stage.
        stage_list = [fanout_fall if i%2==0 else fanout_rise for i in range(total_stages)]
        return stage_list
    
    def calculate_stages_with_fixed_fanout(self, required_delay, fanout):
        from math import ceil
        #Delay being negative is not an error. It implies that any amount of stages would have a negative effect on the overall delay
        if required_delay <= 3+self.parasitic_inv_delay: #3 is the minimum delay per stage (with pinv=0).
            return 1
        delay_stages = ceil(required_delay/(fanout+1+self.parasitic_inv_delay))
        return delay_stages
    
    def calculate_stage_list(self, total_stages, fanout_rise, fanout_fall):
        """Produces a list of fanouts which determine the size of the delay chain. List length is the number of stages.
           Assumes the first stage is falling.
        """
        stage_list = []
        for i in range(total_stages):
            if i%2 == 0:
                stage_list.append()
                
    def setup_signal_busses(self):
        """ Setup bus names, determine the size of the busses etc """

        # List of input control signals
        if self.port_type == "rw":
            self.input_list = ["csb", "web"]
        else:
            self.input_list = ["csb"]
            
        if self.port_type == "rw":
            self.dff_output_list = ["cs_bar", "cs", "we_bar", "we"]
        else:
            self.dff_output_list = ["cs_bar", "cs"]
        
        # list of output control signals (for making a vertical bus)
        if self.port_type == "rw":
            self.internal_bus_list = ["gated_clk_bar", "gated_clk_buf", "we", "clk_buf", "we_bar", "cs"]
        elif self.port_type == "r":
            self.internal_bus_list = ["gated_clk_bar", "gated_clk_buf", "clk_buf", "cs_bar", "cs"]
        else:
            self.internal_bus_list = ["gated_clk_bar", "gated_clk_buf", "clk_buf", "cs"]
        # leave space for the bus plus one extra space
        self.internal_bus_width = (len(self.internal_bus_list)+1)*self.m2_pitch 
        
        # Outputs to the bank
        if self.port_type == "rw":
            self.output_list = ["s_en", "w_en", "p_en_bar"]
        elif self.port_type == "r":
            self.output_list = ["s_en", "p_en_bar"]
        else:
            self.output_list = ["w_en"]
        self.output_list.append("wl_en")
        self.output_list.append("clk_buf")
        
        self.supply_list = ["vdd", "gnd"]

    
    def route_rails(self):
        """ Add the input signal inverted tracks """
        height = self.control_logic_center.y - self.m2_pitch
        offset = vector(self.ctrl_dff_array.width,0)
        
        self.rail_offsets = self.create_vertical_bus("metal2", self.m2_pitch, offset, self.internal_bus_list, height)
            
            
    def create_instances(self):
        """ Create all the instances """
        self.create_dffs()
        self.create_clk_buf_row()
        self.create_gated_clk_bar_row()
        self.create_gated_clk_buf_row()
        self.create_wlen_row()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.create_wen_row()
        if self.port_type == "rw": 
            self.create_rbl_in_row()
        if (self.port_type == "rw") or (self.port_type == "r"): 
            self.create_pen_row()            
            self.create_sen_row()
            self.create_rbl()


    def place_instances(self):
        """ Place all the instances """
        # Keep track of all right-most instances to determine row boundary
        # and add the vdd/gnd pins
        self.row_end_inst = []

        # Add the control flops on the left of the bus
        self.place_dffs()

        # All of the control logic is placed to the right of the DFFs and bus
        self.control_x_offset = self.ctrl_dff_array.width + self.internal_bus_width
        
        row = 0
        # Add the logic on the right of the bus
        self.place_clk_buf_row(row) 
        row += 1
        self.place_gated_clk_bar_row(row) 
        row += 1
        self.place_gated_clk_buf_row(row) 
        row += 1
        self.place_wlen_row(row) 
        row += 1
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.place_wen_row(row)
            height = self.w_en_inst.uy()
            control_center_y = self.w_en_inst.uy()
            row += 1
        if self.port_type == "rw": 
            self.place_rbl_in_row(row)
            row += 1
        if (self.port_type == "rw") or (self.port_type == "r"):            
            self.place_pen_row(row)
            row += 1
            self.place_sen_row(row)
            row += 1
            self.place_rbl(row)
            height = self.rbl_inst.uy()
            control_center_y = self.rbl_inst.by()

        # This offset is used for placement of the control logic in the SRAM level.
        self.control_logic_center = vector(self.ctrl_dff_inst.rx(), control_center_y)

        # Extra pitch on top and right
        self.height = height + 2*self.m1_pitch
        # Max of modules or logic rows
        self.width = max([inst.rx() for inst in self.row_end_inst])
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.width = max(self.rbl_inst.rx() , self.width)
        self.width += self.m2_pitch

    def route_all(self):
        """ Routing between modules """
        self.route_rails()
        self.route_dffs()
        self.route_wlen()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.route_wen()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.route_rbl_in()
            self.route_pen()
            self.route_sen()
        self.route_clk_buf()
        self.route_gated_clk_bar()
        self.route_gated_clk_buf()
        self.route_supply()


    def create_rbl(self):
        """ Create the replica bitline """
        if self.port_type == "r":
            input_name = "gated_clk_bar"
        else:
            input_name = "rbl_in"
        self.rbl_inst=self.add_inst(name="replica_bitline",
                                    mod=self.replica_bitline)
        self.connect_inst([input_name, "pre_s_en", "vdd", "gnd"])

    def place_rbl(self,row):
        """ Place the replica bitline """
        y_off = row * self.and2.height + 2*self.m1_pitch

        # Add the RBL above the rows
        # Add to the right of the control rows and routing channel
        offset = vector(0, y_off)
        self.rbl_inst.place(offset)
        
        
    def create_clk_buf_row(self):
        """ Create the multistage and gated clock buffer  """
        self.clkbuf_inst = self.add_inst(name="clkbuf",
                                         mod=self.clkbuf)
        self.connect_inst(["clk","clk_buf","vdd","gnd"])
        
    def place_clk_buf_row(self,row):
        """ Place the multistage clock buffer below the control flops """
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)
        
        offset = vector(x_off,y_off)
        self.clkbuf_inst.place(offset, mirror)
        
        self.row_end_inst.append(self.clkbuf_inst)

    def route_clk_buf(self):
        clk_pin = self.clkbuf_inst.get_pin("A")
        clk_pos = clk_pin.center()
        self.add_layout_pin_segment_center(text="clk",
                                           layer="metal2",
                                           start=clk_pos,
                                           end=clk_pos.scale(1,0))
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=clk_pos)


        clkbuf_map = zip(["Z"], ["clk_buf"])
        self.connect_vertical_bus(clkbuf_map, self.clkbuf_inst, self.rail_offsets, ("metal3", "via2", "metal2"))  
        # The pin is on M1, so we need another via as well
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=self.clkbuf_inst.get_pin("Z").center())
        

        self.connect_output(self.clkbuf_inst, "Z", "clk_buf")

    def create_gated_clk_bar_row(self):
        self.clk_bar_inst = self.add_inst(name="inv_clk_bar",
                                            mod=self.inv)
        self.connect_inst(["clk_buf","clk_bar","vdd","gnd"])
        
        self.gated_clk_bar_inst = self.add_inst(name="and2_gated_clk_bar",
                                                mod=self.and2)
        self.connect_inst(["cs","clk_bar","gated_clk_bar","vdd","gnd"])

    def place_gated_clk_bar_row(self,row):
        """ Place the gated clk logic below the control flops """
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)
        
        offset = vector(x_off,y_off)
        self.clk_bar_inst.place(offset, mirror)
        
        x_off += self.inv.width
        
        offset = vector(x_off,y_off)
        self.gated_clk_bar_inst.place(offset, mirror)
        
        self.row_end_inst.append(self.gated_clk_bar_inst)

    def route_gated_clk_bar(self):
        clkbuf_map = zip(["A"], ["clk_buf"])
        self.connect_vertical_bus(clkbuf_map, self.clk_bar_inst, self.rail_offsets)  
        
        out_pos = self.clk_bar_inst.get_pin("Z").center()
        in_pos = self.gated_clk_bar_inst.get_pin("B").center()
        mid1 = vector(in_pos.x,out_pos.y)
        self.add_path("metal1",[out_pos, mid1, in_pos])

        # This is the second gate over, so it needs to be on M3
        clkbuf_map = zip(["A"], ["cs"])
        self.connect_vertical_bus(clkbuf_map, self.gated_clk_bar_inst, self.rail_offsets, ("metal3", "via2", "metal2"))  
        # The pin is on M1, so we need another via as well
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=self.gated_clk_bar_inst.get_pin("A").center())


        # This is the second gate over, so it needs to be on M3
        clkbuf_map = zip(["Z"], ["gated_clk_bar"])
        self.connect_vertical_bus(clkbuf_map, self.gated_clk_bar_inst, self.rail_offsets, ("metal3", "via2", "metal2"))  
        # The pin is on M1, so we need another via as well
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=self.gated_clk_bar_inst.get_pin("Z").center())

    def create_gated_clk_buf_row(self):
        self.gated_clk_buf_inst = self.add_inst(name="and2_gated_clk_buf",
                                                mod=self.and2)
        self.connect_inst(["clk_buf", "cs","gated_clk_buf","vdd","gnd"])

    def place_gated_clk_buf_row(self,row):
        """ Place the gated clk logic below the control flops """
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)
        
        offset = vector(x_off,y_off)
        self.gated_clk_buf_inst.place(offset, mirror)
        
        self.row_end_inst.append(self.gated_clk_buf_inst)
        
    def route_gated_clk_buf(self):
        clkbuf_map = zip(["A", "B"], ["clk_buf", "cs"])
        self.connect_vertical_bus(clkbuf_map, self.gated_clk_buf_inst, self.rail_offsets)  

        
        clkbuf_map = zip(["Z"], ["gated_clk_buf"])
        self.connect_vertical_bus(clkbuf_map, self.gated_clk_buf_inst, self.rail_offsets, ("metal3", "via2", "metal2"))  
        # The pin is on M1, so we need another via as well
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=self.gated_clk_buf_inst.get_pin("Z").center())
        
    def create_wlen_row(self):
        # input pre_p_en, output: wl_en
        self.wl_en_inst=self.add_inst(name="buf_wl_en",
                                      mod=self.wl_en_driver)
        self.connect_inst(["gated_clk_bar", "wl_en", "vdd", "gnd"])

    def place_wlen_row(self, row):
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)
        
        offset = vector(x_off, y_off)
        self.wl_en_inst.place(offset, mirror)

        self.row_end_inst.append(self.wl_en_inst)

    def route_wlen(self):
        wlen_map = zip(["A"], ["gated_clk_bar"])
        self.connect_vertical_bus(wlen_map, self.wl_en_inst, self.rail_offsets)  
        self.connect_output(self.wl_en_inst, "Z", "wl_en")

    def create_rbl_in_row(self):
        
        # input: gated_clk_bar, we_bar, output: rbl_in
        self.rbl_in_inst=self.add_inst(name="and2_rbl_in",
                                         mod=self.and2)
        self.connect_inst(["gated_clk_bar", "we_bar", "rbl_in", "vdd", "gnd"])

    def place_rbl_in_row(self,row):
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)

        offset = vector(x_off, y_off)
        self.rbl_in_inst.place(offset, mirror)

        self.row_end_inst.append(self.rbl_in_inst)

    def route_rbl_in(self):
        """ Connect the logic for the rbl_in generation """

        if self.port_type == "rw":
            input_name = "we_bar"
            # Connect the NAND gate inputs to the bus
            rbl_in_map = zip(["A", "B"], ["gated_clk_bar", "we_bar"])
            self.connect_vertical_bus(rbl_in_map, self.rbl_in_inst, self.rail_offsets)  
        
            
        # Connect the output of the precharge enable to the RBL input
        if self.port_type == "rw":
            out_pos = self.rbl_in_inst.get_pin("Z").center()
        else:
            out_pos = vector(self.rail_offsets["gated_clk_bar"].x, self.rbl_inst.by()-3*self.m2_pitch)
        in_pos = self.rbl_inst.get_pin("en").center()
        mid1 = vector(in_pos.x,out_pos.y)
        self.add_wire(("metal3","via2","metal2"),[out_pos, mid1, in_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=out_pos,
                            rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=out_pos,
                            rotate=90)
        
    def create_pen_row(self):
        if self.port_type == "rw":
            # input: gated_clk_bar, we_bar, output: pre_p_en
            self.pre_p_en_inst=self.add_inst(name="and2_pre_p_en",
                                             mod=self.and2)
            self.connect_inst(["gated_clk_buf", "we_bar", "pre_p_en", "vdd", "gnd"])
            input_name = "pre_p_en"
        else:
            input_name = "gated_clk_buf"

        # input: pre_p_en, output: p_en_bar
        self.p_en_bar_inst=self.add_inst(name="inv_p_en_bar",
                                         mod=self.p_en_bar_driver)
        self.connect_inst([input_name, "p_en_bar", "vdd", "gnd"])
        
        
    def place_pen_row(self,row):
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)
        
        if self.port_type == "rw":
            offset = vector(x_off, y_off)
            self.pre_p_en_inst.place(offset, mirror)

            x_off += self.and2.width
        
        offset = vector(x_off,y_off)
        self.p_en_bar_inst.place(offset, mirror)

        self.row_end_inst.append(self.p_en_bar_inst)

    def route_pen(self):
        if self.port_type == "rw":
            # Connect the NAND gate inputs to the bus
            pre_p_en_in_map = zip(["A", "B"], ["gated_clk_buf", "we_bar"])
            self.connect_vertical_bus(pre_p_en_in_map, self.pre_p_en_inst, self.rail_offsets)  

            out_pos = self.pre_p_en_inst.get_pin("Z").center()
            in_pos = self.p_en_bar_inst.get_pin("A").lc()
            mid1 = vector(out_pos.x,in_pos.y)
            self.add_wire(("metal1","via1","metal2"),[out_pos,mid1,in_pos])                
        else:
            in_map = zip(["A"], ["gated_clk_buf"])
            self.connect_vertical_bus(in_map, self.p_en_bar_inst, self.rail_offsets)  
        
        self.connect_output(self.p_en_bar_inst, "Z", "p_en_bar")
        
    def create_sen_row(self):
        """ Create the sense enable buffer. """
        # BUFFER FOR S_EN
        # input: pre_s_en, output: s_en
        self.s_en_inst=self.add_inst(name="buf_s_en",
                                     mod=self.s_en_driver)
        self.connect_inst(["pre_s_en", "s_en",  "vdd", "gnd"])
        
    def place_sen_row(self,row):
        """ 
        The sense enable buffer gets placed to the far right of the 
        row. 
        """
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)

        offset = vector(x_off, y_off)
        self.s_en_inst.place(offset, mirror)
        
        self.row_end_inst.append(self.s_en_inst)

        
    def route_sen(self):
        
        out_pos = self.rbl_inst.get_pin("out").bc()
        in_pos = self.s_en_inst.get_pin("A").lc()
        mid1 = vector(out_pos.x,in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[out_pos, mid1,in_pos])                

        self.connect_output(self.s_en_inst, "Z", "s_en")
        
        
    def create_wen_row(self):
        # input: we (or cs) output: w_en
        if self.port_type == "rw":
            input_name = "we"
        else:
            # No we for write-only reports, so use cs
            input_name = "cs"
            
        # BUFFER FOR W_EN
        self.w_en_inst = self.add_inst(name="buf_w_en_buf",
                                       mod=self.w_en_driver)
        self.connect_inst([input_name, "w_en", "vdd", "gnd"])


    def place_wen_row(self,row):
        x_off = self.ctrl_dff_inst.width + self.internal_bus_width
        (y_off,mirror)=self.get_offset(row)
            
        offset = vector(x_off, y_off)
        self.w_en_inst.place(offset, mirror)
        
        self.row_end_inst.append(self.w_en_inst)
        
    def route_wen(self):
        
        if self.port_type == "rw":
            input_name = "we"
        else:
            # No we for write-only reports, so use cs
            input_name = "cs"
            
        wen_map = zip(["A"], [input_name])
        self.connect_vertical_bus(wen_map, self.w_en_inst, self.rail_offsets)  

        self.connect_output(self.w_en_inst, "Z", "w_en")
        
    def create_dffs(self):
        self.ctrl_dff_inst=self.add_inst(name="ctrl_dffs",
                                         mod=self.ctrl_dff_array)
        self.connect_inst(self.input_list + self.dff_output_list + ["clk_buf"] + self.supply_list)

    def place_dffs(self):
        self.ctrl_dff_inst.place(vector(0,0))
        
    def route_dffs(self):
        if self.port_type == "rw":
            dff_out_map = zip(["dout_bar_0", "dout_bar_1", "dout_1"], ["cs", "we", "we_bar"])            
        elif self.port_type == "r":
            dff_out_map = zip(["dout_bar_0", "dout_0"], ["cs", "cs_bar"])            
        else:
            dff_out_map = zip(["dout_bar_0"], ["cs"])
        self.connect_vertical_bus(dff_out_map, self.ctrl_dff_inst, self.rail_offsets, ("metal3", "via2", "metal2"))
        
        # Connect the clock rail to the other clock rail
        in_pos = self.ctrl_dff_inst.get_pin("clk").uc()
        mid_pos = in_pos + vector(0,2*self.m2_pitch)
        rail_pos = vector(self.rail_offsets["clk_buf"].x, mid_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, mid_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rail_pos,
                            rotate=90)

        self.copy_layout_pin(self.ctrl_dff_inst, "din_0", "csb")
        if (self.port_type == "rw"):
            self.copy_layout_pin(self.ctrl_dff_inst, "din_1", "web")
        
    def get_offset(self,row):
        """ Compute the y-offset and mirroring """
        y_off = row*self.and2.height
        if row % 2:
            y_off += self.and2.height
            mirror="MX"
        else:
            mirror="R0"

        return (y_off,mirror)

                      
    def connect_output(self, inst, pin_name, out_name):
        """ Create an output pin on the right side from the pin of a given instance. """
        
        out_pin = inst.get_pin(pin_name)
        right_pos=out_pin.center() + vector(self.width-out_pin.cx(),0)
        self.add_layout_pin_segment_center(text=out_name,
                                           layer="metal1",
                                           start=out_pin.center(),
                                           end=right_pos)



    def route_supply(self):
        """ Add vdd and gnd to the instance cells """

        max_row_x_loc = max([inst.rx() for inst in self.row_end_inst])        
        for inst in self.row_end_inst:
            pins = inst.get_pins("vdd")
            for pin in pins:
                if pin.layer == "metal1":
                    row_loc = pin.rc()
                    pin_loc = vector(max_row_x_loc, pin.rc().y)
                    self.add_power_pin("vdd", pin_loc)
                    self.add_path("metal1", [row_loc, pin_loc])

            pins = inst.get_pins("gnd")
            for pin in pins:
                if pin.layer == "metal1":
                    row_loc = pin.rc()
                    pin_loc = vector(max_row_x_loc, pin.rc().y)
                    self.add_power_pin("gnd", pin_loc)
                    self.add_path("metal1", [row_loc, pin_loc])
            
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.copy_layout_pin(self.rbl_inst,"gnd")
            self.copy_layout_pin(self.rbl_inst,"vdd")        

        self.copy_layout_pin(self.ctrl_dff_inst,"gnd")
        self.copy_layout_pin(self.ctrl_dff_inst,"vdd")        
        
            

    def add_lvs_correspondence_points(self):
        """ This adds some points for easier debugging if LVS goes wrong. 
        These should probably be turned off by default though, since extraction
        will show these as ports in the extracted netlist.
        """
        # pin=self.clk_inv1.get_pin("Z")
        # self.add_label_pin(text="clk1_bar",
        #                    layer="metal1",
        #                    offset=pin.ll(),
        #                    height=pin.height(),
        #                    width=pin.width())

        # pin=self.clk_inv2.get_pin("Z")
        # self.add_label_pin(text="clk2",
        #                    layer="metal1",
        #                    offset=pin.ll(),
        #                    height=pin.height(),
        #                    width=pin.width())

        pin=self.rbl_inst.get_pin("out")
        self.add_label_pin(text="out",
                           layer=pin.layer,
                           offset=pin.ll(),
                           height=pin.height(),
                           width=pin.width())
                           

    def get_delays_to_wl(self):
        """Get the delay (in delay units) of the clk to a wordline in the bitcell array"""
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        stage_efforts = self.determine_wordline_stage_efforts()
        clk_to_wl_rise,clk_to_wl_fall = logical_effort.calculate_relative_rise_fall_delays(stage_efforts, self.parasitic_inv_delay)
        total_delay = clk_to_wl_rise + clk_to_wl_fall 
        debug.info(1, "Clock to wl delay is rise={:.3f}, fall={:.3f}, total={:.3f} in delay units".format(clk_to_wl_rise, clk_to_wl_fall,total_delay))
        return clk_to_wl_rise,clk_to_wl_fall 
     
        
    def determine_wordline_stage_efforts(self):
        """Follows the gated_clk_bar -> wl_en -> wordline signal for the total path efforts"""
        stage_effort_list = []
        
        #Initial direction of gated_clk_bar signal for this path
        is_clk_bar_rise = True
        
        #Calculate the load on wl_en within the module and add it to external load
        external_cout = self.sram.get_wl_en_cin()
        #First stage is the clock buffer
        stage_effort_list += self.clkbuf.get_stage_efforts(external_cout, is_clk_bar_rise)
        last_stage_is_rise = stage_effort_list[-1].is_rise
        
        #Then ask the sram for the other path delays (from the bank)
        stage_effort_list += self.sram.determine_wordline_stage_efforts(last_stage_is_rise)
        
        return stage_effort_list
        
    def get_delays_to_sen(self):
        """Get the delay (in delay units) of the clk to a sense amp enable. 
           This does not incorporate the delay of the replica bitline.
        """
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        stage_efforts = self.determine_sa_enable_stage_efforts()
        clk_to_sen_rise, clk_to_sen_fall = logical_effort.calculate_relative_rise_fall_delays(stage_efforts, self.parasitic_inv_delay)
        total_delay = clk_to_sen_rise + clk_to_sen_fall 
        debug.info(1, "Clock to s_en delay is rise={:.3f}, fall={:.3f}, total={:.3f} in delay units".format(clk_to_sen_rise, clk_to_sen_fall,total_delay))
        return clk_to_sen_rise, clk_to_sen_fall   
          
    def determine_sa_enable_stage_efforts(self):
        """Follows the gated_clk_bar signal to the sense amp enable signal adding each stages stage effort to a list"""
        stage_effort_list = []
        #Calculate the load on clk_buf_bar
        ext_clk_buf_cout = self.sram.get_clk_bar_cin()
        
        #Initial direction of clock signal for this path
        last_stage_rise = True
        
        #First stage, gated_clk_bar -(and2)-> rbl_in. Only for RW ports.
        if self.port_type == "rw":
            stage1_cout = self.replica_bitline.get_en_cin()
            stage_effort_list += self.and2.get_stage_efforts(stage1_cout, last_stage_rise)
            last_stage_rise = stage_effort_list[-1].is_rise
        
        #Replica bitline stage, rbl_in -(rbl)-> pre_s_en
        stage2_cout = self.s_en_driver.get_cin()
        stage_effort_list += self.replica_bitline.determine_sen_stage_efforts(stage2_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        #buffer stage, pre_s_en -(buffer)-> s_en
        stage3_cout = self.sram.get_sen_cin()
        stage_effort_list += self.s_en_driver.get_stage_efforts(stage3_cout, last_stage_rise)
        last_stage_rise = stage_effort_list[-1].is_rise
        
        return stage_effort_list    
       
