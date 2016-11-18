from math import log
import design
from tech import drc, parameter
import debug
from ms_flop_array import ms_flop_array
from wordline_driver import wordline_driver
from contact import contact
from pinv import pinv
from nand_2 import nand_2
from nand_3 import nand_3
from nor_2 import nor_2
from replica_bitline import replica_bitline
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
        debug.info(1, "Creating %s" % self.name)

        self.num_rows = num_rows
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        """ Create layout and route between modules """
        self.create_modules()
        self.setup_layout_offsets()
        self.add_modules()
        self.add_routing()
        self.add_pin_labels()

    def create_modules(self):
        """ add all the required modules """
        c = reload(__import__(OPTS.config.ms_flop))
        self.mod_ms_flop = getattr(c, OPTS.config.ms_flop)
        self.ms_flop = self.mod_ms_flop("ms_flop")
        self.add_mod(self.ms_flop)
        self.inv = pinv(name="pinv",
                        nmos_width=drc["minwidth_tx"],
                        beta=parameter["pinv_beta"])

        self.add_mod(self.inv)
        self.nand2 = nand_2(name="nand2",
                            nmos_width=2 * drc["minwidth_tx"])
        self.add_mod(self.nand2)
        self.NAND3 = nand_3(name="NAND3",
                            nmos_width=3 * drc["minwidth_tx"])
        self.add_mod(self.NAND3)

        # Special gates: 4x Inverter
        self.inv4 = pinv(name="pinv4",
                         nmos_width=4 * drc["minwidth_tx"],
                         beta=parameter["pinv_beta"])
        self.add_mod(self.inv4)

        self.nor2 = nor_2(name="nor2",
                          nmos_width=drc["minwidth_tx"])
        self.add_mod(self.nor2)

        self.msf_control = ms_flop_array(name="msf_control",
                                         array_type="data_in",
                                         columns=3,
                                         word_size=3)
        self.add_mod(self.msf_control)

        self.replica_bitline = replica_bitline("replica_bitline",
                                               int(math.ceil(self.num_rows / 10.0)))
        self.add_mod(self.replica_bitline)

    def add_pin_labels(self):
        """ Add pins  and labels after everything is done """
        input_lst =["CSb","WEb","OEb"]
        output_lst = ["s_en", "w_en", "tri_en", "tri_en_bar", "clk_bar"]
        clk =["clk"]
        rails = ["vdd", "gnd"]
        pin_lst = input_lst + output_lst + clk + rails
        for pin in pin_lst:
            self.add_pin(pin)

        # add label of input, output and clk in metal3 layer 
        input_lst =["CSb","WEb","OEb"]
        output_lst = ["s_en", "w_en", "tri_en", "tri_en_bar", "clk_bar"]
        for pin in input_lst + output_lst + ["clk"]:
            self.add_label(text=pin,
                           layer="metal3",
                           offset=getattr(self, pin+"_position"))
        # add label of vdd and gnd manually cause non-uniformed names and layers
        self.add_label(text="vdd",
                       layer="metal1",
                       offset=self.vdd1_position)
        self.add_label(text="vdd",
                       layer="metal2",
                       offset=self.vdd2_position)
        self.add_label(text="gnd",
                       layer="metal2",
                       offset=self.gnd_position)

    def setup_layout_offsets(self):
        """ Setup layout offsets, determine the size of the busses etc """
        # This isn't for instantiating, but we use it to get the dimensions
        m1m2_via = contact(layer_stack=("metal1", "via1", "metal2"))

        # Vertical metal rail gap definition
        self.metal2_extend_contact = (m1m2_via.second_layer_height - m1m2_via.contact_width) / 2
        self.gap_between_rails = self.metal2_extend_contact + drc["metal2_to_metal2"]
        self.gap_between_rail_offset = self.gap_between_rails + drc["minwidth_metal2"]
        self.via_shift = (m1m2_via.second_layer_width - m1m2_via.first_layer_width) / 2

        # used to shift contact when connecting to NAND3 C pin down
        self.contact_shift = (m1m2_via.first_layer_width - m1m2_via.contact_width) / 2

        # Common parameters for rails
        self.rail_width = drc["minwidth_metal2"]
        self.rail_gap = 2 * drc["metal2_to_metal2"]
        self.rail_offset_gap = self.rail_width + self.rail_gap

        # First RAIL Parameters
        self.num_rails_1 = 6
        self.overall_rail_1_gap = (self.num_rails_1 + 1) * self.rail_offset_gap
        self.rail_1_x_offsets = []

        # Second RAIL Parameters
        self.num_rails_2 = 4
        self.overall_rail_2_gap = (self.num_rails_2 + 1) * self.rail_offset_gap
        self.rail_2_x_offsets = []

        # GAP between main control and REPLICA BITLINE
        self.replica_bitline_gap = self.rail_offset_gap * 2

        self.output_port_gap = 3 * drc["minwidth_metal3"]
        self.logic_height = max(self.replica_bitline.width, 4 * self.inv.height)

    def add_modules(self):
        """ Place all the modules """
        self.add_msf_control()
        self.set_msf_control_pins()
        self.add_1st_row(self.output_port_gap)
        self.add_2nd_row(self.output_port_gap + 2 * self.inv.height)

        # Height and width
        self.height = self.logic_height + self.output_port_gap
        self.width = self.offset_replica_bitline.x + self.replica_bitline.height

    def add_routing(self):
        """ Routing between modules """
        self.add_msf_control_routing()
        self.add_1st_row_routing()
        self.add_2nd_row_routing()
        self.add_vdd_routing()
        self.add_gnd_routing()
        self.add_input_routing()
        self.add_output_routing()

    def add_msf_control(self):
        """ ADD ARRAY OF MS_FLOP"""
        self.offset_msf_control = vector(0, self.logic_height + self.output_port_gap)
        self.add_inst(name="msf_control",
                      mod=self.msf_control,
                      offset=self.offset_msf_control,
                      mirror="R270")
        # don't change this order. This pins are meant for internal connection of msf array inside the control logic.
        # These pins are connecting the msf_array inside of control_logic.
        temp = ["CSb", "WEb", "OEb", "CS_bar", "CS", "WE_bar",
                "WE", "OE_bar", "OE", "clk", "vdd", "gnd"]
        self.connect_inst(temp)

    def set_msf_control_pins(self):
        # msf_control inputs
        correct = vector(0, 0.5 * drc["minwidth_metal2"])
        def translate_inputs(pt1,pt2):
            return pt1 + pt2.rotate_scale(1,-1) - correct

        # msf_control outputs
        def translate_outputs(pt1,pt2):
            return pt1 - correct + vector(self.msf_control.height,- pt2.x)

        # set CSS WE OE signal groups(in, out, bar)
        pt1 = self.offset_msf_control
        pin_set = ["CSb","WEb","OEb"]
        pt2in = self.msf_control.din_positions[0:len(pin_set)]
        pt2out = self.msf_control.dout_positions[0:len(pin_set)]
        pt2bar = self.msf_control.dout_bar_positions[0:len(pin_set)]
        for i in range(len(pin_set)):
            value = translate_inputs(pt1,pt2in[i])
            setattr(self,"msf_control_"+pin_set[i]+"_position",value)
            value = translate_outputs(pt1,pt2out[i])
            setattr(self,"msf_control_"+pin_set[i][0:2]+"_bar_position",value)
            value = translate_outputs(pt1,pt2bar[i])
            setattr(self,"msf_control_"+pin_set[i][0:2]+"_position",value)

        # clk , vdd
        base = self.offset_msf_control - vector(0.5 * drc["minwidth_metal2"], 0)
        msf_clk = self.msf_control.clk_positions[0].rotate_scale(1,-1) 
        self.msf_control_clk_position = base + msf_clk
        msf_vdd = self.msf_control.vdd_positions[0].rotate_scale(1,-1) 
        self.msf_control_vdd_position = base + msf_vdd 

        # gnd
        self.msf_control_gnd_positions = []
        for gnd_offset in self.msf_control.gnd_positions:
            offset = self.offset_msf_control + vector(self.msf_control.height, 
                                                          - gnd_offset.x)
            self.msf_control_gnd_positions.append(offset - correct)

    def add_1st_row(self,y_off):
        # inv1 with clk as gate input.
        msf_control_rotate_x = self.offset_msf_control.x + self.msf_control.height 
        self.offset_inv1 = vector(msf_control_rotate_x - self.inv4.width, y_off)
        self.add_inst(name="clk_inverter",
                      mod=self.inv4,
                      offset=self.offset_inv1)
        self.connect_inst(["clk", "clk_bar", "vdd", "gnd"])
        # set pin offset as attr
        self.inv1_A_position = self.offset_inv1 + self.inv4.A_position.scale(0,1)
        base = self.offset_inv1 + vector(self.inv4.width, 0)
        for pin in ["Z_position", "vdd_position", "gnd_position"]:
            setattr(self, "inv1_"+pin, base + getattr(self.inv4, pin).scale(0,1))

        # nor2
        self.offset_nor2 = vector(self.nor2.width + 2 * drc["minwidth_metal3"],
                                  y_off)
        self.add_inst(name="nor2",
                      mod=self.nor2,
                      offset=self.offset_nor2,
                      mirror="MY")
        self.connect_inst(["clk", "OE_bar", "tri_en", "vdd", "gnd"])
        self.set_nand2_nor2_pin("nor2",[-1,1])

        x_off = msf_control_rotate_x + self.overall_rail_1_gap
        self.nand_array_position = vector(x_off, y_off)

        # nand2_1 input: OE, clk_bar output: tri_en_bar
        self.offset_nand2 = self.nand_array_position
        self.add_inst(name="nand2_tri_en",
                      mod=self.nand2,
                      offset=self.offset_nand2)
        self.connect_inst(["OE", "clk_bar",  "tri_en_bar", "vdd", "gnd"])
        # set pin offset as attr
        self.set_nand2_nor2_pin("nand2",[1,1])

        # REPLICA BITLINE
        base_x = self.nand_array_position.x + self.NAND3.width + 3 * self.inv.width
        total_rail_gap = self.rail_offset_gap + self.overall_rail_2_gap
        x_off = base_x + total_rail_gap + self.replica_bitline_gap
        self.offset_replica_bitline = vector(x_off, y_off)
        self.add_inst(name="replica_bitline",
                      mod=self.replica_bitline,
                      offset=self.offset_replica_bitline,
                      mirror="MX",
                      rotate=90)
        self.connect_inst(["rblk", "pre_s_en", "vdd", "gnd"])

        # BUFFER INVERTERS FOR S_EN
        # inv_4 input: input: pre_s_en_bar, output: s_en
        self.offset_inv4 = vector(base_x - 2 * self.inv.width, y_off)
        self.add_inst(name="inv_s_en1",
                      mod=self.inv,
                      offset=self.offset_inv4,
                      mirror="MY")
        self.connect_inst(["pre_s_en_bar", "s_en",  "vdd", "gnd"])
        self.set_inv2345_pins(inv_name="inv4", inv_scale=[-1, 1])

        # inv_5 input: pre_s_en, output: pre_s_en_bar
        self.offset_inv5 = vector(base_x - self.inv.width, y_off)
        self.add_inst(name="inv_s_en2",
                      mod=self.inv,
                      offset=self.offset_inv5,
                      mirror="MY")
        self.connect_inst(["pre_s_en", "pre_s_en_bar",  "vdd", "gnd"])
        self.set_inv2345_pins(inv_name="inv5", inv_scale=[-1, 1])

        # set pin offset as attr
        pin_offset = self.replica_bitline.en_input_offset.rotate()
        self.replica_en_offset = self.offset_replica_bitline + pin_offset
        pin_offset = self.replica_bitline.out_offset.rotate()
        self.replica_out_offset = self.offset_replica_bitline + pin_offset

    def add_2nd_row(self, y_off):
        # Nand3_1 input: OE, clk_bar,CS output: rblk_bar
        self.offset_nand3_1 = vector(self.nand_array_position.x, y_off)
        self.add_inst(name="NAND3_rblk_bar",
                      mod=self.NAND3,
                      offset=self.offset_nand3_1,
                      mirror="MX")
        self.connect_inst(["clk_bar", "OE", "CS", "rblk_bar", "vdd", "gnd"])
        # set pin offset as attr
        self.set_Nand3_pins(nand_name = "nand3_1",nand_scale = [0,-1])

        # Nand3_2 input: WE, clk_bar,CS output: w_en_bar
        self.offset_nand3_2 = vector(self.nand_array_position.x, y_off)
        self.add_inst(name="NAND3_w_en_bar",
                      mod=self.NAND3,
                      offset=self.offset_nand3_2,
                      mirror="RO")
        self.connect_inst(["clk_bar", "WE", "CS", "w_en_bar", "vdd", "gnd"])
        # set pin offset as attr
        self.set_Nand3_pins(nand_name = "nand3_2",nand_scale = [0,1])

        # connect nand2 and nand3 to inv
        nand3_to_inv_connection_height = self.NAND3.Z_position.y- self.inv.A_position.y+ drc["minwidth_metal1"]
        self.add_rect(layer="metal1",
                      offset=self.nand3_1_Z_position,
                      width=drc["minwidth_metal1"],
                      height=nand3_to_inv_connection_height)
        self.add_rect(layer="metal1",
                      offset=self.nand3_2_Z_position + vector(0,drc["minwidth_metal1"]),
                      width=drc["minwidth_metal1"],
                      height=-nand3_to_inv_connection_height)

        # inv_2 input: rblk_bar, output: rblk
        x_off = self.nand_array_position.x + self.NAND3.width
        self.offset_inv2 = vector(x_off, y_off)
        self.add_inst(name="inv_rblk",
                      mod=self.inv,
                      offset=self.offset_inv2,
                      mirror="MX")
        self.connect_inst(["rblk_bar", "rblk",  "vdd", "gnd"])
        # set pin offset as attr
        self.set_inv2345_pins(inv_name="inv2", inv_scale=[1,-1])

        # inv_3 input: w_en_bar, output: pre_w_en
        self.offset_inv3 = self.offset_inv2 
        self.add_inst(name="inv_w_en",
                      mod=self.inv,
                      offset=self.offset_inv3,
                      mirror="RO")
        self.connect_inst(["w_en_bar", "pre_w_en",  "vdd", "gnd"])
        # set pin offset as attr
        self.set_inv2345_pins(inv_name="inv3", inv_scale=[1, 1])

        # BUFFER INVERTERS FOR W_EN
        x_off = self.nand_array_position.x + self.NAND3.width + self.inv.width
        self.offset_inv6 = vector(x_off, y_off)
        self.add_inst(name="inv_w_en1",
                      mod=self.inv,
                      offset=self.offset_inv6,
                      mirror="RO")
        self.connect_inst(["pre_w_en", "pre_w_en1",  "vdd", "gnd"])

        x_off = self.nand_array_position.x + self.NAND3.width + 2 * self.inv.width
        self.offset_inv7 = [x_off,  y_off]
        self.add_inst(name="inv_w_en2",
                      mod=self.inv,
                      offset=self.offset_inv7,
                      mirror="RO")
        self.connect_inst(["pre_w_en1", "w_en",  "vdd", "gnd"])
        # set pin offset as attr
        self.inv7_Z_position = self.offset_inv7 + vector(self.inv.width,
                                                         self.inv.Z_position[1])

    def set_nand2_nor2_pin(self,mod,scale):
        offset = getattr (self, "offset_"+mod)
        for pin in ["A","B"]:
            pin_xy = getattr(getattr(self, mod), pin+"_position")
            setattr(self, mod+"_1_"+pin+"_position", offset + pin_xy.scale(0,1))
        base = offset + vector(getattr(self, mod).width,0).scale(scale[0],0)
        for pin in ["Z","vdd","gnd"]:
            pin_xy = getattr(getattr(self, mod), pin+"_position")
            setattr(self, mod+"_1_"+pin+"_position", base + pin_xy.scale(0,1))

    def set_Nand3_pins(self,nand_name,nand_scale):
        base = getattr(self, "offset_"+nand_name)
        extra = vector(0, drc["minwidth_metal1"]* (1 - nand_scale[1]) *0.5) 
        off1 = base - extra
        off2 = base - extra + vector(self.NAND3.width, 0)
        self.set_Nand3_pins_sub(nand_name,["A","B","C"],off1,[0,nand_scale[1]])
        self.set_Nand3_pins_sub(nand_name,["Z","vdd","gnd"],off2,[0,nand_scale[1]])

    def set_Nand3_pins_sub(self,nand_name,pin_lst,base,nand_scale):
        for pin in pin_lst:
            pin_xy = getattr(self.NAND3, pin+"_position").scale(0,nand_scale[1])
            setattr(self, nand_name+"_"+pin+"_position", base + pin_xy)

    def set_inv2345_pins(self,inv_name,inv_scale):
        base_xy = getattr(self, "offset_"+inv_name)
        correct= vector(0, (1-inv_scale[1]) * 0.5 * drc["minwidth_metal1"])
        # pin A
        pin_xy = vector(0, self.inv4.A_position.y).scale(0,inv_scale[1])
        setattr(self, inv_name+"_A_position", base_xy + pin_xy - correct)
        # Z, vdd, gnd
        for pin in ["Z_position", "vdd_position", "gnd_position"]:
            pin_xy = getattr(self.inv, pin).scale(0,inv_scale[1])
            rotated_pin_xy = vector(self.inv.width * inv_scale[0], 0) + pin_xy 
            setattr(self, inv_name+"_"+pin, base_xy + rotated_pin_xy - correct)

    def add_msf_control_routing(self):
        # FIRST RAIL : MSF_CONTROL OUTPUT RAIL
        rail1_start = vector(self.msf_control_WE_position.x, 
                             self.output_port_gap)
        for i in range(self.num_rails_1):
            correct = vector((i+1) * self.rail_offset_gap, 0)
            offset = rail1_start + correct
            self.add_rect(layer="metal2",
                          offset=offset,
                          width=drc["minwidth_metal2"],
                          height=self.logic_height)
            self.rail_1_x_offsets.append(offset.x)

        rail2_start_x = (self.nand_array_position.x + self.NAND3.width 
                             + 3 * self.inv.width + self.rail_offset_gap)
        for i in range(self.num_rails_2):
            offset = vector(rail2_start_x + i * self.rail_offset_gap,
                            self.output_port_gap)
            self.add_rect(layer="metal2",
                          offset=offset,
                          width=drc["minwidth_metal2"],
                          height=self.logic_height)
            self.rail_2_x_offsets.append(offset.x)

    def add_1st_row_routing(self):
        # First rail routing left
        left_side = []
        for pin in ["OE_bar","OE","CS","WE"]:
            left_side.append(getattr(self,"msf_control_"+pin+"_position"))
        line_indices = [1, 2, 3, 4]
        for i in range(len(left_side)):
            offset = left_side[i]
            line_x_offset = self.rail_1_x_offsets[line_indices[i]]
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=line_x_offset - offset.x + drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])
            correct1 = vector(self.gap_between_rails, - self.via_shift)
            correct2 = vector(self.contact_shift + drc["minwidth_metal2"],0)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=offset + correct1 - correct2,
                         rotate=90)
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=vector(line_x_offset, offset[1]) + correct1,
                         rotate=90)
        # First rail routing Right
        right_side = []
        right_side.append(self.nand2_1_A_position)
        right_side.append(self.nand2_1_B_position)
        for size in ["1","2"]:
            for pin in ["A","B","C"]:
                right_side.append(getattr(self,"nand3_"+size+"_"+pin+"_position"))

        line_indices = [2, 5, 5, 2, 3, 5, 4, 3]
        for i in range(len(right_side)):
            offset = right_side[i]
            line_x_offset = self.rail_1_x_offsets[line_indices[i]]
            base = vector(line_x_offset, offset[1])
            self.add_rect(layer="metal1",
                          offset=base,
                          width=offset.x - line_x_offset,
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=base + correct1,
                         rotate=90)

        # OE_bar [Bus # 1] to nor2 B input
        layer_stack = ("metal1", "via1", "metal2")
        start = self.nor2_1_B_position
        mid1 = vector(self.nor2_1_B_position.x+ 2 * drc["minwidth_metal2"], 
                      start.y)
        mid2 = vector(mid1.x, 
                      self.nor2_1_gnd_position.y- 2 * drc["minwidth_metal1"])
        mid3 = vector(self.rail_1_x_offsets[1] + 0.5 * drc["minwidth_metal2"], 
                      mid2.y)
        end = [mid3.x, self.output_port_gap]
        self.add_wire(layer_stack, [start, mid1, mid2, mid3, end])

        layer_stack = ("metal1")
        start = self.inv1_Z_position+ vector(0, + 0.5 * drc["minwidth_metal1"])
        mid1 = start + vector(drc["minwidth_metal2"], 0)
        mid2 = vector(mid1.x, 
                      self.nand2_1_B_position.y + 0.5 * drc["minwidth_metal1"])
        end = [self.nand2_1_B_position.x, mid2.y]
        self.add_path(layer_stack, [start, mid1, mid2, end])

    def add_2nd_row_routing(self):
        # Second rail routing
        left_side = []
        left_side.append(self.inv2_Z_position)
        left_side.append(self.inv7_Z_position)
        left_side.append(self.inv5_A_position)
        line_indices = [1, 0, 2]
        #line_indices = [1,2]
        for i in range(len(left_side)):
            offset = left_side[i]
            line_x_offset = self.rail_2_x_offsets[line_indices[i]]
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=line_x_offset - offset.x+ drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[line_x_offset + self.gap_between_rails,
                                 offset.y- self.via_shift],
                         rotate=90)

        # Replica bitline (rblk to replica bitline input)
        layer_stack = ("metal1", "via1", "metal2")
        start = vector(self.rail_2_x_offsets[1] + 0.5 * drc["minwidth_metal2"],
                       self.output_port_gap)
        mid1 = vector(start.x, 0.5 * drc["minwidth_metal1"])
        end = vector(self.replica_en_offset.x, mid1.y)

        self.add_wire(layer_stack, [start, mid1,  end])

        height = self.replica_en_offset.y- end.y+ 0.5 * drc["minwidth_metal1"]

        self.add_rect(layer="metal1",
                      offset=end - vector([0.5 * drc["minwidth_metal1"]] * 2),
                      width=drc["minwidth_metal1"],
                      height=height)

        # Replica bitline (replica bitline output to the buffer [inv4,inv5])
        start = [self.rail_2_x_offsets[2], self.replica_out_offset[1]]
        end = self.replica_out_offset - vector(0.5 * drc["minwidth_metal1"],0)
        self.add_rect(layer="metal3",
                      offset=start, 
                      width=self.replica_out_offset.x- self.rail_2_x_offsets[2],
                      height=drc["minwidth_metal3"])
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=start)
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=end)

    def add_vdd_routing(self):
        """ VDD routing between modules """
        vdd_rail_index = self.num_rails_2 - 1
        rail_2_x = self.rail_2_x_offsets[vdd_rail_index]

        # Connection between nor2 vdd to nand3 vdd
        self.add_rect(layer="metal1",
                      offset=self.nor2_1_vdd_position,
                      width=rail_2_x + drc["minwidth_metal2"],
                      height=drc["minwidth_metal1"])

        # Connection between top AND_Array vdd to the last line on rail2
        self.add_rect(layer="metal1",
                      offset=self.nand3_2_vdd_position,
                      width=(rail_2_x + drc["minwidth_metal2"]
                                 - self.nand3_2_vdd_position.x),
                      height=drc["minwidth_metal1"])

        # Connection in horizontal metal2 vdd rail
        base = vector(rail_2_x + self.gap_between_rails,
                      - self.via_shift)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=base + self.nand2_1_vdd_position.scale(0, 1),
                     rotate=90)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=base + self.nand3_2_vdd_position.scale(0, 1),
                     rotate=90)

        # Connection of msf_vdd to inv1 vdd
        self.add_rect(layer="metal1",
                      offset=[self.msf_control_vdd_position.x,
                              self.inv1_vdd_position[1]],
                      width=drc["minwidth_metal1"],
                      height=self.msf_control_vdd_position.y- self.inv1_vdd_position[1])

        vdd_offset = vector(self.replica_bitline.height,3 * drc["minwidth_metal1"])

        self.vdd1_position = vdd_offset + self.offset_replica_bitline 
        self.vdd2_position = vector(rail_2_x, self.output_port_gap)

    def add_gnd_routing(self):
        """ GND routing """
        self.gnd_position = self.offset_replica_bitline

        # Connection of msf_control gnds to the metal2 gnd rail
        for gnd_offset in self.msf_control_gnd_positions:
            self.add_rect(layer="metal2",
                          offset=gnd_offset,
                          width=(self.rail_1_x_offsets[0] - gnd_offset.x
                                     + drc["minwidth_metal2"]),
                          height=drc["minwidth_metal2"])

        # Connect msf_control gnd to nand3 gnd
        self.add_rect(layer="metal1",
                      offset=self.nor2_1_gnd_position,
                      width=self.offset_replica_bitline.x,
                      height=drc["minwidth_metal1"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.rail_1_x_offsets[0] + self.gap_between_rails,
                             self.nor2_1_gnd_position.y- self.via_shift],
                     rotate=90)

        # nand3 gnd to replica bitline gnd
        self.add_rect(layer="metal1",
                      offset=self.nand3_2_gnd_position,
                      width=(self.offset_replica_bitline.x
                                 - self.nand3_2_gnd_position.x),
                      height=drc["minwidth_metal1"])

    def add_input_routing(self):
        """ Input pin routing """
        # WEb, CEb, OEb assign from msf_control pin
        self.WEb_position = self.msf_control_WEb_position
        self.CSb_position = self.msf_control_CSb_position
        self.OEb_position = self.msf_control_OEb_position

        # Clk
        clk_y = self.inv1_vdd_position.y+ 6 * drc["minwidth_metal1"]
        self.clk_position = vector(0, clk_y)

        # clk port to inv1 A
        layer_stack = ("metal1", "via1", "metal2")
        start = self.inv1_A_position + vector(0, 0.5 * drc["minwidth_metal1"])
        mid1 = vector(self.inv1_A_position.x- 2 * drc["minwidth_metal2"],
                      start.y)
        mid2 = vector(mid1.x, clk_y)
        self.clk_position = vector(0, mid2[1])

        self.add_wire(layer_stack, [start, mid1, mid2, self.clk_position])


        # clk line to msf_control_clk
        self.add_rect(layer="metal1",
                      offset=[self.msf_control_clk_position.x,
                              self.clk_position[1]],
                      width=drc["minwidth_metal1"],
                      height=(self.msf_control_clk_position.y
                                  - self.clk_position[1]))

        # clk connection to nor2 A input
        start = self.inv1_A_position + vector(- 2 * drc["minwidth_metal2"],
                                              0.5 * drc["minwidth_metal1"])
        mid1 = start - vector(3 * drc["minwidth_metal2"], 0)
        mid2 = [mid1.x, self.nor2_1_A_position.y]

        self.add_path("metal1", [start, mid1, mid2, self.nor2_1_A_position])

        correct = vector(0, 0.5 * drc["minwidth_metal1"])

        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=self.clk_position + correct,
                     rotate=270)
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.clk_position + correct,
                     rotate=270)

    def add_output_routing(self):
        """ Output pin routing """
        # clk_bar
        self.clk_bar_position = vector(self.rail_1_x_offsets[self.num_rails_1 - 1],
                                       0)
        self.add_rect(layer="metal2",
                      offset=self.clk_bar_position,
                      width=drc["minwidth_metal2"],
                      height=self.output_port_gap)
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.clk_bar_position)


        # tri_en
        correct = vector (0, 0.5 * drc["minwidth_metal1"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=self.nor2_1_Z_position + correct,
                     rotate=270)
        self.add_rect(layer="metal2",
                      offset=self.nor2_1_Z_position.scale(1, 0),
                      width=drc["minwidth_metal2"],
                      height=self.nor2_1_Z_position.y + correct.y)
        self.add_via(layers=("metal2", "via2", "metal3"),
                     offset=self.nor2_1_Z_position.scale(1, 0))
        self.tri_en_position = vector(self.nor2_1_Z_position.x, 0)

        # tri_en_bar
        correct = vector(drc["minwidth_metal2"], 0)
        self.tri_en_bar_position = self.nand2_1_Z_position.scale(1, 0) - correct
        self.add_via(layers=("metal1", "via1", "metal2"),
                      offset=self.nand2_1_Z_position - correct)
        self.add_rect(layer="metal2",
                      offset=self.tri_en_bar_position,
                      width=drc["minwidth_metal2"],
                      height=self.nand2_1_Z_position.y+ drc["minwidth_metal1"])
        self.add_via(layers=("metal2", "via2", "metal3"),
                      offset=self.tri_en_bar_position)

        # w_en
        self.w_en_position = vector(self.rail_2_x_offsets[0], 0)
        self.add_rect(layer="metal2",
                      offset=self.w_en_position,
                      width=drc["minwidth_metal2"],
                      height=self.output_port_gap)
        self.add_via(layers=("metal2", "via2", "metal3"),
                      offset=self.w_en_position)

        # s_en
        self.s_en_position = self.inv4_Z_position.scale(1,0)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=self.inv4_Z_position)
        self.add_rect(layer="metal2",
                      offset=self.s_en_position,
                      width=drc["minwidth_metal2"],
                      height=self.inv4_Z_position.y+ drc["minwidth_metal1"])
        self.add_via(layers=("metal2", "via2", "metal3"),
                      offset=self.s_en_position)
