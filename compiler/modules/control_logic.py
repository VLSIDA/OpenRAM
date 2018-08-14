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

class control_logic(design.design):
    """
    Dynamically generated Control logic for the total SRAM circuit.
    """

    def __init__(self, num_rows):
        """ Constructor """
        design.design.__init__(self, "control_logic")
        debug.info(1, "Creating {}".format(self.name))

        self.num_rows = num_rows
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        """ Create layout and route between modules """
        self.setup_layout_offsets()
        self.add_pins()
        self.create_modules()
        self.add_rails()
        self.add_modules()
        self.add_routing()


    def add_pins(self):
        """ Add the pins to the control logic module. """
        for pin in self.input_list + ["clk"]:
            self.add_pin(pin,"INPUT")
        for pin in self.output_list:
            self.add_pin(pin,"OUTPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

    def create_modules(self):
        """ add all the required modules """
        
        dff = dff_inv() 
        dff_height = dff.height
        
        self.ctrl_dff_array = dff_inv_array(rows=2,columns=1)
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

        from importlib import reload
        c = reload(__import__(OPTS.replica_bitline))
        replica_bitline = getattr(c, OPTS.replica_bitline)
        # FIXME: These should be tuned according to the size!
        delay_stages = 4 # Must be non-inverting
        delay_fanout = 3 # This can be anything >=2
        bitcell_loads = int(math.ceil(self.num_rows / 5.0))
        self.replica_bitline = replica_bitline(delay_stages, delay_fanout, bitcell_loads)
        self.add_mod(self.replica_bitline)


    def setup_layout_offsets(self):
        """ Setup layout offsets, determine the size of the busses etc """
        # These aren't for instantiating, but we use them to get the dimensions
        #self.poly_contact_offset = vector(0.5*contact.poly.width,0.5*contact.poly.height)

        # Have the cell gap leave enough room to route an M2 wire.
        # Some cells may have pwell/nwell spacing problems too when the wells are different heights.
        #self.cell_gap = max(self.m2_pitch,drc["pwell_to_nwell"])

        # List of input control signals
        self.input_list =["csb","web"]
        self.dff_output_list =["cs_bar", "cs", "we_bar", "we"]        
        # list of output control signals (for making a vertical bus)
        self.internal_bus_list = ["clk_buf", "clk_buf_bar", "we", "cs"]
        # leave space for the bus plus one extra space
        self.internal_bus_width = (len(self.internal_bus_list)+1)*self.m2_pitch 
        # Outputs to the bank
        self.output_list = ["s_en", "w_en", "clk_buf_bar", "clk_buf"]
        self.supply_list = ["vdd", "gnd"]

    
    def add_rails(self):
        """ Add the input signal inverted tracks """
        height = 4*self.inv1.height - self.m2_pitch
        offset = vector(self.ctrl_dff_array.width,0)
        
        self.rail_offsets = self.create_vertical_bus("metal2", self.m2_pitch, offset, self.internal_bus_list, height)
            
            
    def add_modules(self):
        """ Place all the modules """
        # Keep track of all right-most instances to determine row boundary
        # and add the vdd/gnd pins
        self.row_end_inst = []


        # Add the control flops on the left of the bus
        self.add_dffs()

        # Add the logic on the right of the bus
        self.add_clk_row(row=0) # clk is a double-high cell
        self.add_we_row(row=2)
        # self.add_trien_row(row=3)
        # self.add_trien_bar_row(row=4)
        self.add_rbl_in_row(row=3)
        self.add_sen_row(row=4)
        self.add_rbl(row=5)
        

        self.add_lvs_correspondence_points()

        # This offset is used for placement of the control logic in
        # the SRAM level.
        self.control_logic_center = vector(self.ctrl_dff_inst.rx(), self.rbl_inst.by())

        # Extra pitch on top and right
        self.height = self.rbl_inst.uy() + self.m3_pitch
        # Max of modules or logic rows
        self.width = max(self.rbl_inst.rx(), max([inst.rx() for inst in self.row_end_inst])) + self.m2_pitch


    def add_routing(self):
        """ Routing between modules """
        self.route_dffs()
        #self.route_trien()
        #self.route_trien_bar()
        self.route_rbl_in()
        self.route_wen()
        self.route_sen()
        self.route_clk()
        self.route_supply()


    def add_rbl(self,row):
        """ Add the replica bitline """
        y_off = row * self.inv1.height + 2*self.m1_pitch

        # Add the RBL above the rows
        # Add to the right of the control rows and routing channel
        self.replica_bitline_offset = vector(0, y_off)
        self.rbl_inst=self.add_inst(name="replica_bitline",
                                    mod=self.replica_bitline,
                                    offset=self.replica_bitline_offset)
        self.connect_inst(["rbl_in", "pre_s_en", "vdd", "gnd"])
        
        
    def add_clk_row(self,row):
        """ Add the multistage clock buffer below the control flops """
        x_off = self.ctrl_dff_array.width + self.internal_bus_width
        (y_off,mirror)=self.get_offset(row)

        clkbuf_offset = vector(x_off,y_off)
        self.clkbuf_inst = self.add_inst(name="clkbuf",
                                         mod=self.clkbuf,
                                         offset=clkbuf_offset)

        self.connect_inst(["clk","clk_buf_bar","clk_buf","vdd","gnd"])

        self.row_end_inst.append(self.clkbuf_inst)
        

    def add_rbl_in_row(self,row):
        x_off = self.ctrl_dff_array.width + self.internal_bus_width 
        (y_off,mirror)=self.get_offset(row)


        # input: clk_buf_bar,CS output: rbl_in_bar
        self.rbl_in_bar_offset = vector(x_off, y_off)
        self.rbl_in_bar_inst=self.add_inst(name="nand3_rbl_in_bar",
                                         mod=self.nand2,
                                         offset=self.rbl_in_bar_offset,
                                         mirror=mirror)
        self.connect_inst(["clk_buf_bar", "cs", "rbl_in_bar", "vdd", "gnd"])
        x_off += self.nand2.width

        # input: rbl_in_bar, output: rbl_in
        self.rbl_in_offset = vector(x_off, y_off)
        self.rbl_in_inst=self.add_inst(name="inv_rbl_in",
                                       mod=self.inv1,
                                       offset=self.rbl_in_offset,
                                       mirror=mirror)
        self.connect_inst(["rbl_in_bar", "rbl_in",  "vdd", "gnd"])
        
        self.row_end_inst.append(self.rbl_in_inst)
        
    def add_sen_row(self,row):
        """ The sense enable buffer gets placed to the far right of the 
        row. """
        x_off = self.ctrl_dff_array.width + self.internal_bus_width 
        (y_off,mirror)=self.get_offset(row)

        # input: pre_s_en, output: pre_s_en_bar
        self.pre_s_en_bar_offset = vector(x_off, y_off)
        self.pre_s_en_bar_inst=self.add_inst(name="inv_pre_s_en_bar",
                                             mod=self.inv2,
                                             offset=self.pre_s_en_bar_offset,
                                             mirror=mirror)
        self.connect_inst(["pre_s_en", "pre_s_en_bar",  "vdd", "gnd"])

        x_off += self.inv2.width
        
        # BUFFER INVERTERS FOR S_EN
        # input: input: pre_s_en_bar, output: s_en
        self.s_en_offset = vector(x_off, y_off)
        self.s_en_inst=self.add_inst(name="inv_s_en",
                                     mod=self.inv8,
                                     offset=self.s_en_offset,
                                     mirror=mirror)
        self.connect_inst(["pre_s_en_bar", "s_en",  "vdd", "gnd"])
        

        self.row_end_inst.append(self.s_en_inst)
        
        
    def route_dffs(self):
        """ Route the input inverters """

        dff_out_map = zip(["dout_bar[{}]".format(i) for i in range(3)], ["cs", "we"])
        self.connect_vertical_bus(dff_out_map, self.ctrl_dff_inst, self.rail_offsets)
        
        # Connect the clock rail to the other clock rail
        in_pos = self.ctrl_dff_inst.get_pin("clk").uc()
        mid_pos = in_pos + vector(0,self.m2_pitch)
        rail_pos = vector(self.rail_offsets["clk_buf"].x, mid_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, mid_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rail_pos,
                            rotate=90)

        self.copy_layout_pin(self.ctrl_dff_inst, "din[0]", "csb")
        self.copy_layout_pin(self.ctrl_dff_inst, "din[1]", "web")
        
        
    def add_dffs(self):
        """ Add the three input DFFs (with inverters) """
        self.ctrl_dff_inst=self.add_inst(name="ctrl_dffs",
                                         mod=self.ctrl_dff_array,
                                         offset=vector(0,0))

        self.connect_inst(self.input_list + self.dff_output_list + ["clk_buf"] + self.supply_list)


    def get_offset(self,row):
        """ Compute the y-offset and mirroring """
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"

        return (y_off,mirror)

    def add_we_row(self,row):
        x_off = self.ctrl_dff_inst.width + self.internal_bus_width
        (y_off,mirror)=self.get_offset(row)
            
        # input: WE, CS output: w_en_bar
        w_en_bar_offset = vector(x_off, y_off)
        self.w_en_bar_inst=self.add_inst(name="nand3_w_en_bar",
                                         mod=self.nand3,
                                         offset=w_en_bar_offset,
                                         mirror=mirror)
        self.connect_inst(["clk_buf_bar", "cs", "we", "w_en_bar", "vdd", "gnd"])
        x_off += self.nand3.width

        # input: w_en_bar, output: pre_w_en
        pre_w_en_offset = vector(x_off, y_off)
        self.pre_w_en_inst=self.add_inst(name="inv_pre_w_en",
                                         mod=self.inv1,
                                         offset=pre_w_en_offset,
                                         mirror=mirror)

        self.connect_inst(["w_en_bar", "pre_w_en",  "vdd", "gnd"])
        x_off += self.inv1.width
        
        # BUFFER INVERTERS FOR W_EN
        pre_w_en_bar_offset = vector(x_off, y_off)
        self.pre_w_en_bar_inst=self.add_inst(name="inv_pre_w_en_bar",
                                             mod=self.inv2,
                                             offset=pre_w_en_bar_offset,
                                             mirror=mirror)
        self.connect_inst(["pre_w_en", "pre_w_en_bar",  "vdd", "gnd"])
        x_off += self.inv2.width

        w_en_offset = vector(x_off,  y_off)
        self.w_en_inst=self.add_inst(name="inv_w_en2",
                                     mod=self.inv8,
                                     offset=w_en_offset,
                                     mirror=mirror)
        self.connect_inst(["pre_w_en_bar", "w_en",  "vdd", "gnd"])
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
        wen_map = zip(["A", "B", "C"], ["clk_buf_bar", "cs", "we"])
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
        
        
