from math import log
import design
from tech import drc, parameter
import debug
import contact
from pinv import pinv
from pnand2 import pnand2
from pnand3 import pnand3
from pinvbuf import pinvbuf
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
        self.create_modules()
        self.add_rails()
        self.add_modules()
        self.add_routing()


        
    def create_modules(self):
        """ add all the required modules """
        for pin in self.input_list + ["clk"]:
            self.add_pin(pin,"INPUT")
        for pin in self.output_list:
            self.add_pin(pin,"OUTPUT")
        self.add_pin("vdd","POWER")
        self.add_pin("gnd","GROUND")

        self.nand2 = pnand2()
        self.add_mod(self.nand2)
        self.nand3 = pnand3()
        self.add_mod(self.nand3)

        # Special gates: inverters for buffering
        self.clkbuf = pinvbuf(4,16)
        self.add_mod(self.clkbuf)
        self.inv = self.inv1 = pinv(1)
        self.add_mod(self.inv1)
        self.inv2 = pinv(2)
        self.add_mod(self.inv2)
        self.inv8 = pinv(8)
        self.add_mod(self.inv8)

        c = reload(__import__(OPTS.replica_bitline))
        replica_bitline = getattr(c, OPTS.replica_bitline)
        # FIXME: These should be tuned according to the size!
        delay_stages = 4 # This should be even so that the delay line is inverting!
        delay_fanout = 3
        bitcell_loads = int(math.ceil(self.num_rows / 5.0))
        self.replica_bitline = replica_bitline(delay_stages, delay_fanout, bitcell_loads)
        self.add_mod(self.replica_bitline)


    def setup_layout_offsets(self):
        """ Setup layout offsets, determine the size of the busses etc """
        # These aren't for instantiating, but we use them to get the dimensions
        #self.poly_contact_offset = vector(0.5*contact.poly.width,0.5*contact.poly.height)

        # M1/M2 routing pitch is based on contacted pitch
        self.m1_pitch = max(contact.m1m2.width,contact.m1m2.height) + max(drc["metal1_to_metal1"],drc["metal2_to_metal2"])
        self.m2_pitch = max(contact.m2m3.width,contact.m2m3.height) + max(drc["metal2_to_metal2"],drc["metal3_to_metal3"])

        # Have the cell gap leave enough room to route an M2 wire.
        # Some cells may have pwell/nwell spacing problems too when the wells are different heights.
        #self.cell_gap = max(self.m2_pitch,drc["pwell_to_nwell"])

        self.input_list =["web","csb","oeb"]
        self.input_width = len(self.input_list)*self.m2_pitch        
        self.input_bar_list = ["clk_buf_bar", "we", "cs", "oe"]
        self.input_bar_width = len(self.input_bar_list)*self.m2_pitch
        self.output_list = ["s_en", "w_en", "tri_en", "tri_en_bar", "clk_buf_bar", "clk_buf"]
        self.supply_list = ["vdd", "gnd"]
        self.rail_width = len(self.input_list)*len(self.output_list)*self.m2_pitch
        self.rail_x_offsets = {}

        # GAP between main control and replica bitline
        #self.replica_bitline_gap = 2*self.m2_pitch
    
    def add_rails(self):
        """ Add the input signal tracks and their inverted tracks """
        height = 4*self.inv1.height - self.m2_pitch
        for i in range(len(self.input_list)):
            name = self.input_list[i]
            offset = vector(i*self.m2_pitch,0)
            self.add_layout_pin(text=name,
                                layer="metal2",
                                offset=offset,
                                width=drc["minwidth_metal2"],
                                height=height)
            self.rail_x_offsets[name]=offset.x + 0.5*drc["minwidth_metal2"] # center offset
            
        height = 6*self.inv1.height - self.m2_pitch
        for i in range(len(self.input_bar_list)):
            name = self.input_bar_list[i]
            offset = vector(i*self.m2_pitch + self.input_width + self.inv1.width, 0)
            # just for LVS correspondence...
            self.add_label_pin(text=name,
                               layer="metal2",
                               offset=offset,
                               width=drc["minwidth_metal2"],
                               height=height)
            self.rail_x_offsets[name]=offset.x + 0.5*drc["minwidth_metal2"] # center offset
            
            
    def add_modules(self):
        """ Place all the modules """
        self.add_input_inv()
        
        self.add_clk_buffer(row=0)
        self.add_we_row(row=2)
        self.add_trien_row(row=3)
        self.add_trien_bar_row(row=4)
        self.add_rblk_row(row=5)
        self.add_sen_row(row=6)
        self.add_rbl(row=7)
        

        self.add_lvs_correspondence_points()

        self.height = self.rbl_inst.uy()
        # Find max of logic rows
        max_row = max(self.row_rblk_end_x, self.row_trien_end_x, self.row_trien_bar_end_x,
                      self.row_sen_end_x, self.row_we_end_x, self.row_we_end_x)
        # Max of modules or logic rows
        self.width = max(self.clkbuf.rx(), self.rbl_inst.rx(), max_row)
        


    def add_routing(self):
        """ Routing between modules """
        self.route_input_inv()
        self.route_trien()
        self.route_trien_bar()
        self.route_rblk()
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
        self.connect_inst(["rblk", "pre_s_en", "vdd", "gnd"])
        
        
    def add_clk_buffer(self,row):
        """ Add the multistage clock buffer below the control flops """
        x_off = self.input_width + self.inv1.width + self.input_bar_width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.clkbuf.height
            mirror="MX"
        else:
            mirror="R0"

        clkbuf_offset = vector(x_off,y_off)
        self.clkbuf = self.add_inst(name="clkbuf",
                                    mod=self.clkbuf,
                                    offset=clkbuf_offset)

        self.connect_inst(["clk","clk_buf_bar","clk_buf","vdd","gnd"])
        
        

    def add_rblk_row(self,row):
        x_off = self.input_width + self.inv1.width + self.input_bar_width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"


        # input: OE, clk_buf_bar,CS output: rblk_bar
        self.rblk_bar_offset = vector(x_off, y_off)
        self.rblk_bar=self.add_inst(name="nand3_rblk_bar",
                                    mod=self.nand3,
                                    offset=self.rblk_bar_offset,
                                    mirror=mirror)
        self.connect_inst(["clk_buf_bar", "oe", "cs", "rblk_bar", "vdd", "gnd"])
        x_off += self.nand3.width

        # input: rblk_bar, output: rblk
        self.rblk_offset = vector(x_off, y_off)
        self.rblk=self.add_inst(name="inv_rblk",
                                mod=self.inv1,
                                offset=self.rblk_offset,
                                mirror=mirror)
        self.connect_inst(["rblk_bar", "rblk",  "vdd", "gnd"])
        x_off += self.inv1.width
        
        self.row_rblk_end_x = x_off

    def add_sen_row(self,row):
        """ The sense enable buffer gets placed to the far right of the 
        row. """
        x_off = self.replica_bitline.width - self.inv8.width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"
        
        # BUFFER INVERTERS FOR S_EN
        # input: input: pre_s_en_bar, output: s_en
        self.s_en_offset = vector(x_off, y_off)
        self.s_en=self.add_inst(name="inv_s_en",
                                mod=self.inv8,
                                offset=self.s_en_offset,
                                mirror=mirror)
        self.connect_inst(["pre_s_en_bar", "s_en",  "vdd", "gnd"])
        x_off -= self.inv2.width
        # input: pre_s_en, output: pre_s_en_bar
        self.pre_s_en_bar_offset = vector(x_off, y_off)
        self.pre_s_en_bar=self.add_inst(name="inv_pre_s_en_bar",
                                        mod=self.inv2,
                                        offset=self.pre_s_en_bar_offset,
                                        mirror=mirror)
        self.connect_inst(["pre_s_en", "pre_s_en_bar",  "vdd", "gnd"])

        self.row_sen_end_x = self.replica_bitline.width

    def add_trien_row(self, row):
        x_off = self.input_width + self.inv1.width + self.input_bar_width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"
        
        
        x_off += self.nand2.width
 
        # BUFFER INVERTERS FOR TRI_EN
        self.tri_en_offset = vector(x_off, y_off)
        self.tri_en=self.add_inst(name="inv_tri_en1",
                                  mod=self.inv2,
                                  offset=self.tri_en_offset,
                                  mirror=mirror)
        self.connect_inst(["pre_tri_en_bar", "pre_tri_en1",  "vdd", "gnd"])
        x_off += self.inv2.width
        
        self.tri_en_buf1_offset = vector(x_off, y_off)
        self.tri_en_buf1=self.add_inst(name="tri_en_buf1",
                                       mod=self.inv2,
                                       offset=self.tri_en_buf1_offset,
                                       mirror=mirror)
        self.connect_inst(["pre_tri_en1", "pre_tri_en_bar1",  "vdd", "gnd"])
        x_off += self.inv2.width

        self.tri_en_buf2_offset = vector(x_off,  y_off)
        self.tri_en_buf2=self.add_inst(name="tri_en_buf2",
                                   mod=self.inv8,
                                   offset=self.tri_en_buf2_offset,
                                   mirror=mirror)
        self.connect_inst(["pre_tri_en_bar1", "tri_en",  "vdd", "gnd"])
        x_off += self.inv8.width

        #x_off += self.inv1.width + self.cell_gap
        
        
        
        self.row_trien_end_x = x_off


    def add_trien_bar_row(self, row):
        x_off = self.input_width + self.inv1.width + self.input_bar_width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"

 
        # input: OE, clk_buf_bar output: tri_en_bar
        self.tri_en_bar_offset = vector(x_off,y_off)
        self.tri_en_bar=self.add_inst(name="nand2_tri_en",
                                      mod=self.nand2,
                                      offset=self.tri_en_bar_offset,
                                      mirror=mirror)
        self.connect_inst(["clk_buf_bar", "oe",  "pre_tri_en_bar", "vdd", "gnd"])
        x_off += self.nand2.width 

        # BUFFER INVERTERS FOR TRI_EN
        self.tri_en_bar_buf1_offset = vector(x_off, y_off)
        self.tri_en_bar_buf1=self.add_inst(name="tri_en_bar_buf1",
                                           mod=self.inv2,
                                           offset=self.tri_en_bar_buf1_offset,
                                           mirror=mirror)
        self.connect_inst(["pre_tri_en_bar", "pre_tri_en2",  "vdd", "gnd"])
        x_off += self.inv2.width

        self.tri_en_bar_buf2_offset = vector(x_off,  y_off)
        self.tri_en_bar_buf2=self.add_inst(name="tri_en_bar_buf2",
                                           mod=self.inv8,
                                           offset=self.tri_en_bar_buf2_offset,
                                           mirror=mirror)
        self.connect_inst(["pre_tri_en2", "tri_en_bar",  "vdd", "gnd"])
        x_off += self.inv8.width
        
        #x_off += self.inv1.width + self.cell_gap
        
        
        
        self.row_trien_bar_end_x = x_off

    def route_input_inv(self):
        """ Route the input inverters """
        self.connect_rail_from_left(self.cs_inv,"A","csb")
        self.connect_rail_from_left(self.we_inv,"A","web")
        self.connect_rail_from_left(self.oe_inv,"A","oeb")

        self.connect_rail_from_right(self.cs_inv,"Z","cs")
        self.connect_rail_from_right(self.we_inv,"Z","we")
        self.connect_rail_from_right(self.oe_inv,"Z","oe")
        
        
    def add_input_inv(self):
        """ Add the three input inverters """
        y_off = 0
        mirror = "R0"
        
        # input: csb output: cs
        self.cs_inv_offset = vector(self.input_width, y_off)
        self.cs_inv=self.add_inst(name="cs_inv",
                                   mod=self.inv1,
                                   offset=self.cs_inv_offset,
                                   mirror=mirror)
        self.connect_inst(["csb", "cs", "vdd", "gnd"])
        y_off += 2*self.inv1.height
        mirror = "MX"
        
        # input: oeb  output: oe
        self.oe_inv_offset = vector(self.input_width, y_off)
        self.oe_inv=self.add_inst(name="oe_inv",
                                  mod=self.inv1,
                                  offset=self.oe_inv_offset,
                                  mirror=mirror)
        self.connect_inst(["oeb", "oe", "vdd", "gnd"])

        # Skip a row to prevent via conflict
        y_off += 2*self.inv1.height
        mirror = "MX"

        # input: web output: we
        self.we_inv_offset = vector(self.input_width, y_off)
        self.we_inv=self.add_inst(name="we_inv",
                                   mod=self.inv1,
                                   offset=self.we_inv_offset,
                                   mirror=mirror)
        self.connect_inst(["web", "we", "vdd", "gnd"])

        
    def add_we_row(self,row):
        x_off = self.input_width + self.inv1.width + self.input_bar_width
        y_off = row*self.inv1.height
        if row % 2:
            y_off += self.inv1.height
            mirror="MX"
        else:
            mirror="R0"

            
        # input: WE, clk_buf_bar, CS output: w_en_bar
        self.w_en_bar_offset = vector(x_off, y_off)
        self.w_en_bar=self.add_inst(name="nand3_w_en_bar",
                                    mod=self.nand3,
                                    offset=self.w_en_bar_offset,
                                    mirror=mirror)
        self.connect_inst(["clk_buf_bar", "cs", "we", "w_en_bar", "vdd", "gnd"])
        x_off += self.nand3.width

        # input: w_en_bar, output: pre_w_en
        self.pre_w_en_offset = vector(x_off, y_off)
        self.pre_w_en=self.add_inst(name="inv_pre_w_en",
                                    mod=self.inv1,
                                    offset=self.pre_w_en_offset,
                                    mirror=mirror)

        self.connect_inst(["w_en_bar", "pre_w_en",  "vdd", "gnd"])
        x_off += self.inv1.width
        
        # BUFFER INVERTERS FOR W_EN
        self.pre_w_en_bar_offset = vector(x_off, y_off)
        self.pre_w_en_bar=self.add_inst(name="inv_pre_w_en_bar",
                                        mod=self.inv2,
                                        offset=self.pre_w_en_bar_offset,
                                        mirror=mirror)
        self.connect_inst(["pre_w_en", "pre_w_en_bar",  "vdd", "gnd"])
        x_off += self.inv2.width

        self.w_en_offset = vector(x_off,  y_off)
        self.w_en=self.add_inst(name="inv_w_en2",
                                mod=self.inv8,
                                offset=self.w_en_offset,
                                mirror=mirror)
        self.connect_inst(["pre_w_en_bar", "w_en",  "vdd", "gnd"])
        x_off += self.inv8.width

        self.row_we_end_x = x_off


    def route_rblk(self):
        """ Connect the logic for the rblk generation """
        self.connect_rail_from_left(self.rblk_bar,"A","clk_buf_bar")
        self.connect_rail_from_left(self.rblk_bar,"B","oe")
        self.connect_rail_from_left(self.rblk_bar,"C","cs")

        # Connect the NAND3 output to the inverter
        # The pins are assumed to extend all the way to the cell edge
        rblk_bar_pos = self.rblk_bar.get_pin("Z").center()
        inv_in_pos = self.rblk.get_pin("A").center()
        mid1 = vector(inv_in_pos.x,rblk_bar_pos.y)
        self.add_path("metal1",[rblk_bar_pos,mid1,inv_in_pos])

        # Connect the output to the RBL
        rblk_pos = self.rblk.get_pin("Z").center()
        rbl_in_pos = self.rbl_inst.get_pin("en").center()
        mid1 = vector(rbl_in_pos.x,rblk_pos.y)
        self.add_wire(("metal3","via2","metal2"),[rblk_pos,mid1,rbl_in_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rblk_pos,
                            rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=rblk_pos,
                            rotate=90)

        
                      
    def connect_rail_from_right(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).center()
        rail_pos = vector(self.rail_x_offsets[rail], in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=rail_pos,
                            rotate=90)

    def connect_rail_from_right_m2m3(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).center()
        rail_pos = vector(self.rail_x_offsets[rail], in_pos.y)
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
        rail_pos = vector(self.rail_x_offsets[rail], in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal1","via1","metal2"),
                     offset=rail_pos,
                     rotate=90)

    def connect_rail_from_left_m2m3(self,inst, pin, rail):
        """ Helper routine to connect an unrotated/mirrored oriented instance to the rails """
        in_pos = inst.get_pin(pin).lc()
        rail_pos = vector(self.rail_x_offsets[rail], in_pos.y)
        self.add_wire(("metal3","via2","metal2"),[in_pos, rail_pos])
        self.add_via_center(layers=("metal2","via2","metal3"),
                     offset=in_pos,
                     rotate=90)
        self.add_via_center(layers=("metal2","via2","metal3"),
                     offset=rail_pos,
                     rotate=90)
        
        
    def route_wen(self):
        self.connect_rail_from_left(self.w_en_bar,"A","clk_buf_bar")
        self.connect_rail_from_left(self.w_en_bar,"B","cs")
        self.connect_rail_from_left(self.w_en_bar,"C","we")

        # Connect the NAND3 output to the inverter
        # The pins are assumed to extend all the way to the cell edge
        w_en_bar_pos = self.w_en_bar.get_pin("Z").center()
        inv_in_pos = self.pre_w_en.get_pin("A").center()
        mid1 = vector(inv_in_pos.x,w_en_bar_pos.y)
        self.add_path("metal1",[w_en_bar_pos,mid1,inv_in_pos])
        
        self.add_path("metal1",[self.pre_w_en.get_pin("Z").center(), self.pre_w_en_bar.get_pin("A").center()])
        self.add_path("metal1",[self.pre_w_en_bar.get_pin("Z").center(), self.w_en.get_pin("A").center()])                      

        self.connect_output(self.w_en, "Z", "w_en")
        
    def route_trien(self):

        # Connect the NAND2 output to the buffer
        tri_en_bar_pos = self.tri_en_bar.get_pin("Z").center()
        inv_in_pos = self.tri_en.get_pin("A").center()
        mid1 = vector(tri_en_bar_pos.x,inv_in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[tri_en_bar_pos,mid1,inv_in_pos])
        
        # Connect the INV output to the buffer
        tri_en_pos = self.tri_en.get_pin("Z").center()
        inv_in_pos = self.tri_en_buf1.get_pin("A").center()
        mid_xoffset = 0.5*(tri_en_pos.x + inv_in_pos.x)
        mid1 = vector(mid_xoffset,tri_en_pos.y)
        mid2 = vector(mid_xoffset,inv_in_pos.y)        
        self.add_path("metal1",[tri_en_pos,mid1,mid2,inv_in_pos])
        
        self.add_path("metal1",[self.tri_en_buf1.get_pin("Z").center(), self.tri_en_buf2.get_pin("A").center()])                      
        
        self.connect_output(self.tri_en_buf2, "Z", "tri_en")
        
    def route_trien_bar(self):
        
        self.connect_rail_from_left(self.tri_en_bar,"A","clk_buf_bar")
        self.connect_rail_from_left(self.tri_en_bar,"B","oe")

        # Connect the NAND2 output to the buffer
        tri_en_bar_pos = self.tri_en_bar.get_pin("Z").center()
        inv_in_pos = self.tri_en_bar_buf1.get_pin("A").center()
        mid_xoffset = 0.5*(tri_en_bar_pos.x + inv_in_pos.x)
        mid1 = vector(mid_xoffset,tri_en_bar_pos.y)
        mid2 = vector(mid_xoffset,inv_in_pos.y)        
        self.add_path("metal1",[tri_en_bar_pos,mid1,mid2,inv_in_pos])

        self.add_path("metal1",[self.tri_en_bar_buf1.get_pin("Z").center(), self.tri_en_bar_buf2.get_pin("A").center()])                      
        
        self.connect_output(self.tri_en_bar_buf2, "Z", "tri_en_bar")
        

    def route_sen(self):
        rbl_out_pos = self.rbl_inst.get_pin("out").bc()
        in_pos = self.pre_s_en_bar.get_pin("A").lc()
        mid1 = vector(rbl_out_pos.x,in_pos.y)
        self.add_wire(("metal1","via1","metal2"),[rbl_out_pos,mid1,in_pos])                
        #s_en_pos = self.s_en.get_pin("Z").lc()

        self.add_path("metal1",[self.pre_s_en_bar.get_pin("Z").center(), self.s_en.get_pin("A").center()])

        self.connect_output(self.s_en, "Z", "s_en")
        
    def route_clk(self):
        """ Route the clk and clk_buf_bar signal internally """

        clk_pin = self.clkbuf.get_pin("A")
        self.add_layout_pin_center_segment(text="clk",
                                           layer="metal2",
                                           start=clk_pin.bc(),
                                           end=clk_pin.bc().scale(1,0))

        self.connect_rail_from_right_m2m3(self.clkbuf, "Zb", "clk_buf_bar")
        self.connect_output(self.clkbuf, "Z", "clk_buf")
        self.connect_output(self.clkbuf, "Zb", "clk_buf_bar")
        
    def connect_output(self, inst, pin_name, out_name):
        """ Create an output pin on the right side from the pin of a given instance. """
        out_pin = inst.get_pin(pin_name)
        right_pos=out_pin.center() + vector(self.width-out_pin.cx(),0)
        self.add_layout_pin_center_segment(text=out_name,
                                           layer="metal1",
                                           start=out_pin.center(),
                                           end=right_pos)



    def route_supply(self):
        """ Route the vdd and gnd for the rows of logic. """

        rows_start = 0
        rows_end = self.width
        well_width = drc["minwidth_well"]
        
        for i in range(7):
            if i%2:
                name = "vdd"
                well_type = "nwell"
            else:
                name = "gnd"
                well_type = "pwell"

            yoffset = i*self.inv1.height

            self.add_layout_pin_center_segment(text=name,
                                               layer="metal1",
                                               start=vector(rows_start,yoffset),
                                               end=vector(rows_end,yoffset))
        
            # # also add a well +- around the rail
            # well_offset = vector(rows_start,yoffset-0.5*well_width)
            # self.add_rect(layer=well_type,
            #               offset=well_offset,
            #               width=rows_end-rows_start,
            #               height=well_width)
            # self.add_rect(layer="vtg",
            #               offset=well_offset,
            #               width=rows_end-rows_start,
            #               height=well_width)

        for vdd_pin in self.rbl_inst.get_pins("vdd"):
            if vdd_pin.layer != "metal1":
                continue
            left = vdd_pin.lc().scale(0,1)
            right = left + vector(rows_end,0)
            self.add_layout_pin_center_segment(text="vdd",
                                               layer="metal1",
                                               start=left,
                                               end=right)

        for gnd_pin in self.rbl_inst.get_pins("gnd"):
            if gnd_pin.layer != "metal1":
                continue
            left = gnd_pin.lc().scale(0,1)
            right = left + vector(rows_end,0)
            self.add_layout_pin_center_segment(text="gnd",
                                               layer="metal1",
                                               start=left,
                                               end=right)


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
        
        
