import sys
from tech import drc, parameter
import debug
import design
import contact
from pinv import pinv
from pnand2 import pnand2
from pnor2 import pnor2
from vector import vector
from globals import OPTS

class bank_select(design.design):
    """Create a bank select signal that is combined with an array of
        NOR+INV gates to gate the control signals in case of multiple
        banks are created in upper level SRAM module
    """

    def __init__(self, name="bank_select"):
        design.design.__init__(self, name)

        # Number of control lines in the bus
        self.num_control_lines = 6
        # The order of the control signals on the control bus:
        self.input_control_signals = ["clk_buf", "tri_en_bar", "tri_en", "clk_bar", "w_en", "s_en"]
        # These will be outputs of the gaters if this is multibank
        self.control_signals = ["gated_"+str for str in self.input_control_signals]
            
        for i in range(self.num_control_lines):
            input_name = self.input_control_signals[i]
            self.add_pin(input_name)
        for i in range(self.num_control_lines):
            gated_name = self.control_signals[i]
            self.add_pin(gated_name)

        self.create_modules()
        self.calculate_module_offsets()
        self.add_modules()
        self.route_modules()

        self.DRC_LVS()

    def create_modules(self):
        """ Create modules for later instantiation """
        # 1x Inverter
        self.inv = pinv()
        self.add_mod(self.inv)

        # 4x Inverter
        self.inv4x = pinv(4)
        self.add_mod(self.inv4x)

        self.nor2 = pnor2()
        self.add_mod(self.nor2)

        self.nand2 = pnand2()
        self.add_mod(self.nand2)

    def calculate_module_offsets(self):
        
        # M1/M2 routing pitch is based on contacted pitch
        self.m1_pitch = contact.m1m2.height + max(self.m1_space,self.m2_space)
        self.m2_pitch = contact.m2m3.height + max(self.m2_space,self.m3_space)

        # left of gnd rail is the "bus start"
        self.xoffset_nand =  self.inv4x.width + 2*self.m2_pitch + drc["pwell_to_nwell"]
        self.xoffset_nor =  self.inv4x.width + 2*self.m2_pitch + drc["pwell_to_nwell"]
        self.xoffset_inv = max(self.xoffset_nand + self.nand2.width, self.xoffset_nor + self.nor2.width) 
        self.xoffset_bank_sel_inv = 0 
        self.xoffset_inputs = 0

        # Above the bottom rails (plus a pitch to allow vias)
        self.yoffset_minpoint = self.m1_pitch
        self.yoffset_maxpoint = self.num_control_lines * self.inv.height
        
    def add_modules(self):
        
        # bank select inverter
        self.bank_select_inv_position = vector(self.xoffset_bank_sel_inv, 
                                               self.yoffset_minpoint)
        # bank select inverter (must be made unique if more than one OR)
        self.bank_sel_inv=self.add_inst(name="bank_sel_inv", 
                                        mod=self.inv, 
                                        offset=[self.xoffset_bank_sel_inv, self.yoffset_minpoint])
        self.connect_inst(["bank_sel", "bank_sel_bar", "vdd", "gnd"])

        self.logic_inst = []
        self.inv_inst = []
        for i in range(self.num_control_lines):
            input_name = self.input_control_signals[i]
            gated_name = self.control_signals[i]
            name_nand = "nand_{}".format(input_name)
            name_nor = "nor_{}".format(input_name)
            name_inv = "inv_{}".format(input_name)

            y_offset = self.yoffset_minpoint + self.inv.height * i
            if i%2:
                y_offset += self.inv.height
                mirror = "MX"
            else:
                mirror = ""
            
            # These require OR (nor2+inv) gates since they are active low.
            # (writes occur on clk low)
            if input_name in ("clk_buf", "tri_en_bar"):
                
                self.logic_inst.append(self.add_inst(name=name_nor, 
                                         mod=self.nor2, 
                                         offset=[self.xoffset_nor, y_offset],
                                         mirror=mirror))
                self.connect_inst([input_name,
                                   "bank_sel_bar",
                                   gated_name+"_temp_bar",
                                   "vdd",
                                   "gnd"])

                
            # the rest are AND (nand2+inv) gates
            else:
                self.logic_inst.append(self.add_inst(name=name_nand, 
                                                     mod=self.nand2, 
                                                     offset=[self.xoffset_nand, y_offset],
                                                     mirror=mirror))
                bank_sel_signal = "bank_sel"
                self.connect_inst([input_name,
                                   "bank_sel",
                                   gated_name+"_temp_bar",
                                   "vdd",
                                   "gnd"])

            # They all get inverters on the output
            self.inv_inst.append(self.add_inst(name=name_inv, 
                                               mod=self.inv4x, 
                                               offset=[self.xoffset_inv, y_offset],
                                               mirror=mirror))
            self.connect_inst([gated_name+"_temp_bar",
                               gated_name,
                               "vdd",
                               "gnd"])


    def route_modules(self):
        
        # bank_sel is vertical wire
        bank_sel_inv_pin = self.bank_sel_inv.get_pin("A")
        xoffset_bank_sel = bank_sel_inv_pin.lx()
        bank_sel_line_pos = vector(xoffset_bank_sel, self.yoffset_minpoint)
        bank_sel_line_end = vector(xoffset_bank_sel, self.yoffset_maxpoint)
        self.add_path("metal2", [bank_sel_line_pos, bank_sel_line_end])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=bank_sel_inv_pin.lc())

        # Route the pin to the left edge as well
        bank_sel_pin_pos=vector(0, self.yoffset_minpoint)
        bank_sel_pin_end=vector(bank_sel_line_pos.x, bank_sel_pin_pos.y)
        self.add_layout_pin_center_segment(text="bank_sel",
                                           layer="metal3",
                                           start=bank_sel_pin_pos,
                                           end=bank_sel_pin_end)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=bank_sel_pin_end,
                            rotate=90)

        # bank_sel_bar is vertical wire
        bank_sel_bar_pin = self.bank_sel_inv.get_pin("Z")
        xoffset_bank_sel_bar = bank_sel_bar_pin.rx()
        self.add_label_pin(text="bank_sel_bar",
                           layer="metal2",  
                           offset=vector(xoffset_bank_sel_bar, self.yoffset_minpoint), 
                           height=2*self.inv.height)
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=bank_sel_bar_pin.rc())
            
            
        for i in range(self.num_control_lines):

            logic_inst = self.logic_inst[i]
            inv_inst = self.inv_inst[i]
            
            input_name = self.input_control_signals[i]
            gated_name = self.control_signals[i]            
            if input_name in ("clk_buf", "tri_en_bar"):
                xoffset_bank_signal = xoffset_bank_sel_bar
            else:
                xoffset_bank_signal = xoffset_bank_sel
                
            # Connect the logic output to inverter input
            pre = logic_inst.get_pin("Z").lc()
            out_position = logic_inst.get_pin("Z").rc() + vector(0.5*self.m1_width,0)
            in_position = inv_inst.get_pin("A").lc() + vector(0.5*self.m1_width,0)
            post = inv_inst.get_pin("A").rc()
            self.add_path("metal1", [pre, out_position, in_position, post])
            
            
            # Connect the logic B input to bank_sel/bank_sel_bar
            logic_pos = logic_inst.get_pin("B").lc() - vector(0.5*contact.m1m2.height,0)
            input_pos = vector(xoffset_bank_signal, logic_pos.y)
            self.add_path("metal2",[logic_pos, input_pos])
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=logic_pos,
                                rotate=90)

            
            # Connect the logic A input to the input pin
            logic_pos = logic_inst.get_pin("A").lc()
            input_pos = vector(0,logic_pos.y)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=logic_pos,
                                rotate=90)
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=logic_pos,
                                rotate=90)
            self.add_layout_pin_center_segment(text=input_name,
                                               layer="metal3",
                                               start=input_pos,
                                               end=logic_pos)

            # Add output pins
            out_pin = inv_inst.get_pin("Z")
            self.add_layout_pin(text=gated_name,
                                layer=out_pin.layer,
                                offset=out_pin.ll(),
                                width=inv_inst.rx() - out_pin.lx(),
                                height=out_pin.height())
            
            # Add vdd/gnd supply rails
            gnd_pin = inv_inst.get_pin("gnd")
            left_gnd_pos = vector(0, gnd_pin.cy())
            self.add_layout_pin_center_segment(text="gnd",
                                               layer="metal1",
                                               start=left_gnd_pos,
                                               end=gnd_pin.rc())
            
            vdd_pin = inv_inst.get_pin("vdd")
            left_vdd_pos = vector(0, vdd_pin.cy())
            self.add_layout_pin_center_segment(text="vdd",
                                               layer="metal1",
                                               start=left_vdd_pos,
                                               end=vdd_pin.rc())
