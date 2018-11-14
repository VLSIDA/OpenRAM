from math import log
import design
from tech import drc, parameter
import debug
import contact
from pinv import pinv
from pnand2 import pnand2
from pnand3 import pnand3
from pinvbuf import pinvbuf
from dff_inv import dff_inv
from dff_inv_array import dff_inv_array
import math
from vector import vector
from globals import OPTS
import logical_effort

class control_logic(design.design):
    """
    Dynamically generated Control logic for the total SRAM circuit.
    """

    def __init__(self, num_rows, words_per_row, sram=None, port_type="rw"):
        """ Constructor """
        name = "control_logic_" + port_type
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(name))
        
        self.num_rows = num_rows
        self.words_per_row = words_per_row
        self.port_type = port_type
        
        #This is needed to resize the delay chain. Likely to be changed at some point.
        self.sram=sram
        #self.sram=None #disable re-sizing for debugging
        self.wl_timing_tolerance = 1 #Determines how much larger the sen delay should be. Accounts for possible error in model.
        self.parasitic_inv_delay = 0 #Keeping 0 for now until further testing.
        
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
        self.create_modules()
        
    def create_layout(self):
        """ Create layout and route between modules """
        self.route_rails()
        self.place_modules()
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
        
        dff = dff_inv() 
        dff_height = dff.height
        
        self.ctrl_dff_array = dff_inv_array(rows=self.num_control_signals,columns=1)
        self.add_mod(self.ctrl_dff_array)
        
        self.nand2 = pnand2(height=dff_height)
        self.add_mod(self.nand2)
        self.nand3 = pnand3(height=dff_height)
        self.add_mod(self.nand3)

        # Special gates: inverters for buffering
        # Size the clock for the number of rows (fanout)
        clock_driver_size = max(1,int(self.num_rows/4))
        self.clkbuf = pinvbuf(clock_driver_size,height=dff_height)
        self.add_mod(self.clkbuf)
        self.inv = self.inv1 = pinv(size=1, height=dff_height)
        self.add_mod(self.inv1)
        self.inv2 = pinv(size=4, height=dff_height)
        self.add_mod(self.inv2)
        self.inv8 = pinv(size=16, height=dff_height)
        self.add_mod(self.inv8)

        if (self.port_type == "rw") or (self.port_type == "r"):
            from importlib import reload
            c = reload(__import__(OPTS.replica_bitline))
            replica_bitline = getattr(c, OPTS.replica_bitline)
            
            delay_stages_heuristic, delay_fanout_heuristic = self.get_heuristic_delay_chain_size()
            bitcell_loads = int(math.ceil(self.num_rows / 2.0))
            self.replica_bitline = replica_bitline(delay_stages_heuristic, delay_fanout_heuristic, bitcell_loads, name="replica_bitline_"+self.port_type)
            
            if self.sram != None and not self.is_sen_timing_okay():
                #Resize the delay chain (by instantiating a new rbl) if the analytical timing failed.
                delay_stages, delay_fanout = self.get_dynamic_delay_chain_size(delay_stages_heuristic, delay_fanout_heuristic)
                self.replica_bitline = replica_bitline(delay_stages, delay_fanout, bitcell_loads, name="replica_bitline_resized_"+self.port_type)
            
            self.add_mod(self.replica_bitline)

    def get_heuristic_delay_chain_size(self):
        """Use a basic heuristic to determine the size of the delay chain used for the Sense Amp Enable """
        # FIXME: These should be tuned according to the additional size parameters
        delay_fanout = 3 # This can be anything >=2
        # Delay stages Must be non-inverting
        if self.words_per_row >= 8:
            delay_stages = 8
        elif self.words_per_row == 4:
            delay_stages = 6
        else:
            delay_stages = 4
        return (delay_stages, delay_fanout)
        
    def is_sen_timing_okay(self):
        self.wl_delay = self.get_delay_to_wl()
        self.sen_delay = self.get_delay_to_sen()
        
        #The sen delay must always be bigger than than the wl delay. This decides how much larger the sen delay must be before 
        #a re-size is warranted.
        
        if self.wl_delay*self.wl_timing_tolerance >= self.sen_delay:
            return False
        else:
            return True
            
    def get_dynamic_delay_chain_size(self, previous_stages, previous_fanout):
        """Determine the size of the delay chain used for the Sense Amp Enable using path delays"""
        previous_delay_chain_delay = (previous_fanout+1+self.parasitic_inv_delay)*previous_stages
        debug.info(2, "Previous delay chain produced {} delay units".format(previous_delay_chain_delay))
        
        delay_fanout = 3 # This can be anything >=2
        #The delay chain uses minimum sized inverters. There are (fanout+1)*stages inverters and each
        #inverter adds 1 unit of delay (due to minimum size). This also depends on the pinv value
        required_delay = self.wl_delay*self.wl_timing_tolerance - (self.sen_delay-previous_delay_chain_delay)
        debug.check(required_delay > 0, "Cannot size delay chain to have negative delay")
        delay_stages = int(required_delay/(delay_fanout+1+self.parasitic_inv_delay))
        if delay_stages%2 == 1: #force an even number of stages. 
            delay_stages+=1
            #Fanout can be varied as well but is a little more complicated but potentially optimal.
        debug.info(1, "Setting delay chain to {} stages with {} fanout to match {} delay".format(delay_stages, delay_fanout, required_delay))
        return (delay_stages, delay_fanout)
        
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
            self.internal_bus_list = ["clk_buf", "clk_buf_bar", "we", "cs"]
        else:
            self.internal_bus_list = ["clk_buf", "clk_buf_bar", "cs"]
        # leave space for the bus plus one extra space
        self.internal_bus_width = (len(self.internal_bus_list)+1)*self.m2_pitch 
        
        # Outputs to the bank
        if self.port_type == "r":
            self.output_list = ["s_en"]
        elif self.port_type == "w":
            self.output_list = ["w_en"]
        else:
            self.output_list = ["s_en", "w_en"]
        self.output_list.append("clk_buf_bar")
        self.output_list.append("clk_buf")
        
        self.supply_list = ["vdd", "gnd"]

    
    def route_rails(self):
        """ Add the input signal inverted tracks """
        height = 4*self.inv1.height - self.m2_pitch
        offset = vector(self.ctrl_dff_array.width,0)
        
        self.rail_offsets = self.create_vertical_bus("metal2", self.m2_pitch, offset, self.internal_bus_list, height)
            
            
    def create_modules(self):
        """ Create all the modules """
        self.create_dffs()
        self.create_clk_row()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.create_we_row()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.create_rbl_in_row()
            self.create_sen_row()
            self.create_rbl()


    def place_modules(self):
        """ Place all the modules """
        # Keep track of all right-most instances to determine row boundary
        # and add the vdd/gnd pins
        self.row_end_inst = []

        # Add the control flops on the left of the bus
        self.place_dffs()

        row = 0
        # Add the logic on the right of the bus
        self.place_clk_row(row=row) # clk is a double-high cell
        row += 2
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.place_we_row(row=row)
            pre_height = self.w_en_inst.uy()
            control_center_y = self.w_en_inst.by()
            row += 1
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.place_rbl_in_row(row=row)
            self.place_sen_row(row=row+1)
            self.place_rbl(row=row+2)
            pre_height = self.rbl_inst.uy()
            control_center_y = self.rbl_inst.by()

        # This offset is used for placement of the control logic in the SRAM level.
        self.control_logic_center = vector(self.ctrl_dff_inst.rx(), control_center_y)

        # Extra pitch on top and right
        self.height = pre_height + self.m3_pitch
        # Max of modules or logic rows
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.width = max(self.rbl_inst.rx(), max([inst.rx() for inst in self.row_end_inst])) + self.m2_pitch
        else:
            self.width = max([inst.rx() for inst in self.row_end_inst]) + self.m2_pitch

    def route_all(self):
        """ Routing between modules """
        self.route_dffs()
        if (self.port_type == "rw") or (self.port_type == "w"):
            self.route_wen()
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.route_rbl_in()
            self.route_sen()
        self.route_clk()
        self.route_supply()


    def create_rbl(self):
        """ Create the replica bitline """
        self.rbl_inst=self.add_inst(name="replica_bitline",
                                    mod=self.replica_bitline)
        self.connect_inst(["rbl_in", "pre_s_en", "vdd", "gnd"])

    def place_rbl(self,row):
        """ Place the replica bitline """
        y_off = row * self.inv1.height + 2*self.m1_pitch

        # Add the RBL above the rows
        # Add to the right of the control rows and routing channel
        self.replica_bitline_offset = vector(0, y_off)
        self.rbl_inst.place(self.replica_bitline_offset)
        
        
    def create_clk_row(self):
        """ Create the multistage clock buffer  """
        self.clkbuf_inst = self.add_inst(name="clkbuf",
                                         mod=self.clkbuf)
        self.connect_inst(["clk","clk_buf_bar","clk_buf","vdd","gnd"])

    def place_clk_row(self,row):
        """ Place the multistage clock buffer below the control flops """
        x_off = self.ctrl_dff_array.width + self.internal_bus_width
        (y_off,mirror)=self.get_offset(row)
        clkbuf_offset = vector(x_off,y_off)
        self.clkbuf_inst.place(clkbuf_offset)
        self.row_end_inst.append(self.clkbuf_inst)
        

    def create_rbl_in_row(self):
        self.rbl_in_bar_inst=self.add_inst(name="nand2_rbl_in_bar",
                                         mod=self.nand2)
        self.connect_inst(["clk_buf_bar", "cs", "rbl_in_bar", "vdd", "gnd"])

        # input: rbl_in_bar, output: rbl_in
        self.rbl_in_inst=self.add_inst(name="inv_rbl_in",
                                       mod=self.inv1)
        self.connect_inst(["rbl_in_bar", "rbl_in",  "vdd", "gnd"])
        

    def place_rbl_in_row(self,row):
        x_off = self.ctrl_dff_array.width + self.internal_bus_width 
        (y_off,mirror)=self.get_offset(row)


        self.rbl_in_bar_offset = vector(x_off, y_off)
        self.rbl_in_bar_inst.place(offset=self.rbl_in_bar_offset,
                                   mirror=mirror)
        x_off += self.nand2.width

        self.rbl_in_offset = vector(x_off, y_off)
        self.rbl_in_inst.place(offset=self.rbl_in_offset,
                               mirror=mirror)
        self.row_end_inst.append(self.rbl_in_inst)
        
    def create_sen_row(self):
        """ Create the sense enable buffer. """
        # input: pre_s_en, output: pre_s_en_bar
        self.pre_s_en_bar_inst=self.add_inst(name="inv_pre_s_en_bar",
                                             mod=self.inv2)
        self.connect_inst(["pre_s_en", "pre_s_en_bar",  "vdd", "gnd"])

        # BUFFER INVERTERS FOR S_EN
        # input: input: pre_s_en_bar, output: s_en
        self.s_en_inst=self.add_inst(name="inv_s_en",
                                     mod=self.inv8)
        self.connect_inst(["pre_s_en_bar", "s_en",  "vdd", "gnd"])
        
    def place_sen_row(self,row):
        """ 
        The sense enable buffer gets placed to the far right of the 
        row. 
        """
        x_off = self.ctrl_dff_array.width + self.internal_bus_width 
        (y_off,mirror)=self.get_offset(row)

        self.pre_s_en_bar_offset = vector(x_off, y_off)
        self.pre_s_en_bar_inst.place(offset=self.pre_s_en_bar_offset,
                                     mirror=mirror)
        x_off += self.inv2.width
        
        self.s_en_offset = vector(x_off, y_off)
        self.s_en_inst.place(offset=self.s_en_offset,
                             mirror=mirror)
        self.row_end_inst.append(self.s_en_inst)
        
        
    def route_dffs(self):
        """ Route the input inverters """

        if self.port_type == "r":
            control_inputs = ["cs"]
        else:
            control_inputs = ["cs", "we"]
        dff_out_map = zip(["dout_bar_{}".format(i) for i in range(2*self.num_control_signals - 1)], control_inputs)
        self.connect_vertical_bus(dff_out_map, self.ctrl_dff_inst, self.rail_offsets)
        
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
        
        
    def create_dffs(self):
        """ Add the three input DFFs (with inverters) """
        self.ctrl_dff_inst=self.add_inst(name="ctrl_dffs",
                                         mod=self.ctrl_dff_array)
        self.connect_inst(self.input_list + self.dff_output_list + ["clk_buf"] + self.supply_list)

    def place_dffs(self):
        """ Place the input DFFs (with inverters) """
        self.ctrl_dff_inst.place(vector(0,0))
        

    def get_offset(self,row):
        """ Compute the y-offset and mirroring """
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"

        return (y_off,mirror)

    def create_we_row(self):
        # input: WE, CS output: w_en_bar
        if self.port_type == "rw":
            nand_mod = self.nand3
            temp = ["clk_buf_bar", "cs", "we", "w_en_bar", "vdd", "gnd"]
        else:
            nand_mod = self.nand2
            temp = ["clk_buf_bar", "cs", "w_en_bar", "vdd", "gnd"]
        
        self.w_en_bar_inst = self.add_inst(name="nand3_w_en_bar",
                                           mod=nand_mod)
        self.connect_inst(temp)

        # input: w_en_bar, output: pre_w_en
        self.pre_w_en_inst = self.add_inst(name="inv_pre_w_en",
                                           mod=self.inv1)
        self.connect_inst(["w_en_bar", "pre_w_en", "vdd", "gnd"])
        
        # BUFFER INVERTERS FOR W_EN
        self.pre_w_en_bar_inst = self.add_inst(name="inv_pre_w_en_bar",
                                               mod=self.inv2)
        self.connect_inst(["pre_w_en", "pre_w_en_bar", "vdd", "gnd"])

        self.w_en_inst = self.add_inst(name="inv_w_en2",
                                       mod=self.inv8)
        self.connect_inst(["pre_w_en_bar", "w_en", "vdd", "gnd"])


    def place_we_row(self,row):
        x_off = self.ctrl_dff_inst.width + self.internal_bus_width
        (y_off,mirror)=self.get_offset(row)
            
        w_en_bar_offset = vector(x_off, y_off)
        self.w_en_bar_inst.place(offset=w_en_bar_offset,
                                 mirror=mirror)
        if self.port_type == "rw":
            x_off += self.nand3.width
        else:
            x_off += self.nand2.width

        pre_w_en_offset = vector(x_off, y_off)
        self.pre_w_en_inst.place(offset=pre_w_en_offset,
                                 mirror=mirror)
        x_off += self.inv1.width
        
        pre_w_en_bar_offset = vector(x_off, y_off)
        self.pre_w_en_bar_inst.place(offset=pre_w_en_bar_offset,
                                     mirror=mirror)
        x_off += self.inv2.width

        w_en_offset = vector(x_off,  y_off)
        self.w_en_inst.place(offset=w_en_offset,
                             mirror=mirror)
        x_off += self.inv8.width

        self.row_end_inst.append(self.w_en_inst)
        

    def route_rbl_in(self):
        """ Connect the logic for the rbl_in generation """
        rbl_in_map = zip(["A", "B"], ["clk_buf_bar", "cs"])
        self.connect_vertical_bus(rbl_in_map, self.rbl_in_bar_inst, self.rail_offsets)  
        
        # Connect the NAND3 output to the inverter
        # The pins are assumed to extend all the way to the cell edge
        rbl_in_bar_pos = self.rbl_in_bar_inst.get_pin("Z").center()
        inv_in_pos = self.rbl_in_inst.get_pin("A").center()
        mid1 = vector(inv_in_pos.x,rbl_in_bar_pos.y)
        self.add_path("metal1",[rbl_in_bar_pos,mid1,inv_in_pos])

        # Connect the output to the RBL
        rbl_out_pos = self.rbl_in_inst.get_pin("Z").center()
        rbl_in_pos = self.rbl_inst.get_pin("en").center()
        mid1 = vector(rbl_in_pos.x,rbl_out_pos.y)
        self.add_wire(("metal3","via2","metal2"),[rbl_out_pos,mid1,rbl_in_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rbl_out_pos,
                            rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=rbl_out_pos,
                            rotate=90)

                      
    def connect_rail_from_right(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).center()
        rail_pos = vector(self.rail_offsets[rail].x, in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rail_pos,
                            rotate=90)

    def connect_rail_from_right_m2m3(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).center()
        rail_pos = vector(self.rail_offsets[rail].x, in_pos.y)
        self.add_wire(("metal3","via2","metal2"),[in_pos, rail_pos])
        # Bring it up to M2 for M2/M3 routing
        self.add_via_center(layers=("metal1","via1","metal2"),
                     offset=in_pos,
                     rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                     offset=in_pos,
                     rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=rail_pos,
                            rotate=90)
        
        
    def connect_rail_from_left(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).lc()
        rail_pos = vector(self.rail_offsets[rail].x, in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                     offset=rail_pos,
                     rotate=90)

    def connect_rail_from_left_m2m3(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).lc()
        rail_pos = vector(self.rail_offsets[rail].x, in_pos.y)
        self.add_wire(("metal3","via2","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal2","via2","metal3"),
                     offset=in_pos,
                     rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                     offset=rail_pos,
                     rotate=90)
        
        
    def route_wen(self):
        if self.port_type == "rw":
            wen_map = zip(["A", "B", "C"], ["clk_buf_bar", "cs", "we"])
        else:
            wen_map = zip(["A", "B"], ["clk_buf_bar", "cs"])
        self.connect_vertical_bus(wen_map, self.w_en_bar_inst, self.rail_offsets)  

        # Connect the NAND3 output to the inverter
        # The pins are assumed to extend all the way to the cell edge
        w_en_bar_pos = self.w_en_bar_inst.get_pin("Z").center()
        inv_in_pos = self.pre_w_en_inst.get_pin("A").center()
        mid1 = vector(inv_in_pos.x,w_en_bar_pos.y)
        self.add_path("metal1",[w_en_bar_pos,mid1,inv_in_pos])
        
        self.add_path("metal1",[self.pre_w_en_inst.get_pin("Z").center(), self.pre_w_en_bar_inst.get_pin("A").center()])
        self.add_path("metal1",[self.pre_w_en_bar_inst.get_pin("Z").center(), self.w_en_inst.get_pin("A").center()])                      

        self.connect_output(self.w_en_inst, "Z", "w_en")
        
    def route_sen(self):
        rbl_out_pos = self.rbl_inst.get_pin("out").bc()
        in_pos = self.pre_s_en_bar_inst.get_pin("A").lc()
        mid1 = vector(rbl_out_pos.x,in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[rbl_out_pos,mid1,in_pos])                
        #s_en_pos = self.s_en.get_pin("Z").lc()

        self.add_path("metal1",[self.pre_s_en_bar_inst.get_pin("Z").center(), self.s_en_inst.get_pin("A").center()])

        self.connect_output(self.s_en_inst, "Z", "s_en")
        
    def route_clk(self):
        """ Route the clk and clk_buf_bar signal internally """

        clk_pin = self.clkbuf_inst.get_pin("A")
        self.add_layout_pin_segment_center(text="clk",
                                           layer="metal2",
                                           start=clk_pin.bc(),
                                           end=clk_pin.bc().scale(1,0))

        clkbuf_map = zip(["Z", "Zb"], ["clk_buf", "clk_buf_bar"])
        self.connect_vertical_bus(clkbuf_map, self.clkbuf_inst, self.rail_offsets, ("metal3", "via2", "metal2"))  

        # self.connect_rail_from_right_m2m3(self.clkbuf_inst, "Z", "clk_buf")
        # self.connect_rail_from_right_m2m3(self.clkbuf_inst, "Zb", "clk_buf_bar")
        self.connect_output(self.clkbuf_inst, "Z", "clk_buf")
        self.connect_output(self.clkbuf_inst, "Zb", "clk_buf_bar")
        
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
                           
    def get_delay_to_wl(self):
        """Get the delay (in delay units) of the clk to a wordline in the bitcell array"""
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        stage_efforts = self.determine_wordline_stage_efforts()
        clk_to_wl_delay = logical_effort.calculate_relative_delay(stage_efforts, self.parasitic_inv_delay)
        debug.info(1, "Clock to wordline delay is {} delay units".format(clk_to_wl_delay))
        return clk_to_wl_delay
        
    def determine_wordline_stage_efforts(self):
        """Follows the clock signal to the clk_buf signal to the wordline signal for the total path efforts"""
        stage_effort_list = []
        #Calculate the load on clk_buf within the module and add it to external load
        internal_cout = self.ctrl_dff_array.get_clk_cin()
        external_cout = self.sram.get_clk_cin()
        #First stage is the clock buffer
        stage_effort_list += self.clkbuf.determine_clk_buf_stage_efforts(internal_cout+external_cout)
        
        #Then ask the sram for the other path delays (from the bank)
        stage_effort_list += self.sram.determine_wordline_stage_efforts()
        
        return stage_effort_list
        
    def get_delay_to_sen(self):
        """Get the delay (in delay units) of the clk to a sense amp enable. 
           This does not incorporate the delay of the replica bitline.
        """
        debug.check(self.sram.all_mods_except_control_done, "Cannot calculate sense amp enable delay unless all module have been added.")
        stage_efforts = self.determine_sa_enable_stage_efforts()
        clk_to_sen_delay = logical_effort.calculate_relative_delay(stage_efforts, self.parasitic_inv_delay)
        debug.info(1, "Clock to s_en delay is {} delay units".format(clk_to_sen_delay))
        return clk_to_sen_delay   
          
    def determine_sa_enable_stage_efforts(self):
        """Follows the clock signal to the sense amp enable signal adding each stages stage effort to a list"""
        stage_effort_list = []
        #Calculate the load on clk_buf_bar
        int_clk_buf_cout = self.get_clk_buf_bar_cin()
        ext_clk_buf_cout = self.sram.get_clk_bar_cin()
        
        #First stage is the clock buffer
        stage1 = self.clkbuf.determine_clk_buf_bar_stage_efforts(int_clk_buf_cout+ext_clk_buf_cout)
        stage_effort_list += stage1
        
        #nand2 stage
        stage2_cout = self.inv1.get_cin()
        stage2 = self.nand2.get_effort_stage(stage2_cout)
        stage_effort_list.append(stage2)
        
        #inverter stage
        stage3_cout = self.replica_bitline.get_en_cin()
        stage3 = self.inv1.get_effort_stage(stage3_cout)
        stage_effort_list.append(stage3)
        
        #Replica bitline stage
        stage4_cout = self.inv2.get_cin()
        stage4 = self.replica_bitline.determine_sen_stage_efforts(stage4_cout)
        stage_effort_list += stage4
        
        #inverter (inv2) stage
        stage5_cout = self.inv8.get_cin()
        stage5 = self.inv2.get_effort_stage(stage5_cout)
        stage_effort_list.append(stage5)
        
        #inverter (inv8) stage, s_en output
        clk_sen_cout = self.sram.get_sen_cin()
        stage6 = self.inv8.get_effort_stage(clk_sen_cout)
        stage_effort_list.append(stage6)
        return stage_effort_list    
       
    def get_clk_buf_bar_cin(self):
        """Get the relative capacitance off the clk_buf_bar signal internal to the control logic"""
        we_nand_cin = self.nand2.get_cin()
        if self.port_type == "rw":
            nand_mod = self.nand3
        else:
            nand_mod = self.nand2
        sen_nand_cin = nand_mod.get_cin()
        return we_nand_cin + sen_nand_cin