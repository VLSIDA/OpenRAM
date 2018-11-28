from math import log
import design
from tech import drc, parameter
import debug
import contact
from pinv import pinv
from pbuf import pbuf
from pand2 import pand2
from pnand2 import pnand2
from pinvbuf import pinvbuf
from dff_buf import dff_buf
from dff_buf_array import dff_buf_array
import math
from vector import vector
from globals import OPTS

class control_logic(design.design):
    """
    Dynamically generated Control logic for the total SRAM circuit.
    """

    def __init__(self, num_rows, words_per_row, port_type="rw"):
        """ Constructor """
        name = "control_logic_" + port_type
        design.design.__init__(self, name)
        debug.info(1, "Creating {}".format(name))
        
        self.num_rows = num_rows
        self.words_per_row = words_per_row
        self.port_type = port_type
        
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
        
        dff = dff_buf() 
        dff_height = dff.height
        
        self.ctrl_dff_array = dff_buf_array(rows=self.num_control_signals,columns=1)
        self.add_mod(self.ctrl_dff_array)
        
        self.and2 = pand2(size=4,height=dff_height)
        self.add_mod(self.and2)
        
        # Special gates: inverters for buffering
        # Size the clock for the number of rows (fanout)
        clock_driver_size = max(1,int(self.num_rows/4))
        self.clkbuf = pbuf(size=clock_driver_size, height=dff_height)
        self.add_mod(self.clkbuf)

        self.buf16 = pbuf(size=16, height=dff_height)
        self.add_mod(self.buf16)

        self.buf8 = pbuf(size=8, height=dff_height)
        self.add_mod(self.buf8)
        
        self.inv = self.inv1 = pinv(size=1, height=dff_height)
        self.add_mod(self.inv1)
        
        self.inv8 = pinv(size=8, height=dff_height)
        self.add_mod(self.inv8)
        
        # self.inv2 = pinv(size=4, height=dff_height)
        # self.add_mod(self.inv2)
        #self.inv16 = pinv(size=16, height=dff_height)
        #self.add_mod(self.inv16)

        if (self.port_type == "rw") or (self.port_type == "r"):
            from importlib import reload
            c = reload(__import__(OPTS.replica_bitline))
            replica_bitline = getattr(c, OPTS.replica_bitline)
            
            delay_stages, delay_fanout = self.get_delay_chain_size()
            bitcell_loads = int(math.ceil(self.num_rows / 2.0))
            self.replica_bitline = replica_bitline(delay_stages, delay_fanout, bitcell_loads, name="replica_bitline_"+self.port_type)
            self.add_mod(self.replica_bitline)

    def get_delay_chain_size(self):
        """Determine the size of the delay chain used for the Sense Amp Enable """
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
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.create_rbl_in_row()
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
        if (self.port_type == "rw") or (self.port_type == "r"):
            self.place_rbl_in_row(row)
            row += 1
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
        self.rbl_inst=self.add_inst(name="replica_bitline",
                                    mod=self.replica_bitline)
        self.connect_inst(["rbl_in", "pre_s_en", "vdd", "gnd"])

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
                                      mod=self.buf16)
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

        if self.port_type == "rw":
            input_name = "we_bar"
        else:
            input_name = "cs_bar"
        
        # input: gated_clk_bar, we_bar, output: rbl_in
        self.rbl_in_inst=self.add_inst(name="and2_rbl_in",
                                         mod=self.and2)
        self.connect_inst(["gated_clk_bar", input_name, "rbl_in", "vdd", "gnd"])

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
        else:
            input_name = "cs_bar"
            
        # Connect the NAND gate inputs to the bus
        rbl_in_map = zip(["A", "B"], ["gated_clk_bar", input_name])
        self.connect_vertical_bus(rbl_in_map, self.rbl_in_inst, self.rail_offsets)  
        
        # Connect the output of the precharge enable to the RBL input
        out_pos = self.rbl_in_inst.get_pin("Z").center()
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
            input_name = "we_bar"
        else:
            # No we for read-only reports, so use cs
            input_name = "cs_bar"

        # input: gated_clk_bar, we_bar, output: pre_p_en
        self.pre_p_en_inst=self.add_inst(name="and2_pre_p_en",
                                         mod=self.and2)
        self.connect_inst(["gated_clk_buf", input_name, "pre_p_en", "vdd", "gnd"])
        
        # input: pre_p_en, output: p_en_bar
        self.p_en_bar_inst=self.add_inst(name="inv_p_en_bar",
                                         mod=self.inv8)
        self.connect_inst(["pre_p_en", "p_en_bar", "vdd", "gnd"])
        
        
    def place_pen_row(self,row):
        x_off = self.control_x_offset
        (y_off,mirror)=self.get_offset(row)

        offset = vector(x_off, y_off)
        self.pre_p_en_inst.place(offset, mirror)

        x_off += self.and2.width
        
        offset = vector(x_off,y_off)
        self.p_en_bar_inst.place(offset, mirror)

        self.row_end_inst.append(self.pre_p_en_inst)

    def route_pen(self):
        if self.port_type == "rw":
            input_name = "we_bar"
        else:
            # No we for read-only reports, so use cs
            input_name = "cs_bar"
            
        # Connect the NAND gate inputs to the bus
        pre_p_en_in_map = zip(["A", "B"], ["gated_clk_buf", input_name])
        self.connect_vertical_bus(pre_p_en_in_map, self.pre_p_en_inst, self.rail_offsets)  
        
        out_pos = self.pre_p_en_inst.get_pin("Z").center()
        in_pos = self.p_en_bar_inst.get_pin("A").lc()
        mid1 = vector(out_pos.x,in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[out_pos,mid1,in_pos])                
        
        self.connect_output(self.p_en_bar_inst, "Z", "p_en_bar")
        
    def create_sen_row(self):
        """ Create the sense enable buffer. """
        # BUFFER FOR S_EN
        # input: pre_s_en, output: s_en
        self.s_en_inst=self.add_inst(name="buf_s_en",
                                     mod=self.buf8)
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
                                       mod=self.buf8)
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
        
        
