# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import sys
from tech import drc, parameter
import debug
import design
import contact
from pinv import pinv
from pnand2 import pnand2
from pnor2 import pnor2
from vector import vector
from sram_factory import factory
from globals import OPTS

class bank_select(design.design):
    """Create a bank select signal that is combined with an array of
        NOR+INV gates to gate the control signals in case of multiple
        banks are created in upper level SRAM module
    """

    def __init__(self, name="bank_select", port="rw"):
        design.design.__init__(self, name)

        self.port = port
        
        self.create_netlist()
        if not OPTS.netlist_only:
            self.create_layout()

    def create_netlist(self):
        self.add_pins()
        self.add_modules()
        self.create_instances()
        
    def create_layout(self):
        self.calculate_module_offsets()
        self.place_instances()
        self.route_instances()

        self.add_boundary()
        self.DRC_LVS()


    def add_pins(self):
        
        # Number of control lines in the bus
        if self.port == "rw":
            self.num_control_lines = 4
        else:
            self.num_control_lines = 3
        # The order of the control signals on the control bus:
        # FIXME: Update for multiport (these names are not right)
        self.input_control_signals = ["clk_buf", "clk_buf_bar"]
        if (self.port == "rw") or (self.port == "w"):
            self.input_control_signals.append("w_en")
        if (self.port == "rw") or (self.port == "r"):
            self.input_control_signals.append("s_en")
        # These will be outputs of the gaters if this is multibank
        self.control_signals = ["gated_"+str for str in self.input_control_signals]

        self.add_pin_list(self.input_control_signals, "INPUT")
        self.add_pin("bank_sel")
        self.add_pin_list(self.control_signals, "OUTPUT")
        self.add_pin("vdd","POWER")  
        self.add_pin("gnd","GROUND")  

    def add_modules(self):
        """ Create modules for later instantiation """
        self.bitcell = factory.create(module_type="bitcell")
        
        height = self.bitcell.height + drc("poly_to_active")

        # 1x Inverter
        self.inv_sel = factory.create(module_type="pinv", height=height)
        self.add_mod(self.inv_sel)

        # 4x Inverter
        self.inv4x = factory.create(module_type="pinv", height=height, size=4)
        self.add_mod(self.inv4x)

        self.nor2 = factory.create(module_type="pnor2", height=height)
        self.add_mod(self.nor2)
        
        self.inv4x_nor = factory.create(module_type="pinv", height=height, size=4)
        self.add_mod(self.inv4x_nor)

        self.nand2 = factory.create(module_type="pnand2", height=height)
        self.add_mod(self.nand2)

    def calculate_module_offsets(self):
        
        self.xoffset_nand =  self.inv4x.width + 2*self.m2_pitch + drc("pwell_to_nwell")
        self.xoffset_nor =  self.inv4x.width + 2*self.m2_pitch + drc("pwell_to_nwell")
        self.xoffset_inv = max(self.xoffset_nand + self.nand2.width, self.xoffset_nor + self.nor2.width) 
        self.xoffset_bank_sel_inv = 0 
        self.xoffset_inputs = 0

        self.yoffset_maxpoint = self.num_control_lines * self.inv4x.height
        # Include the M1 pitches for the supply rails and spacing
        self.height = self.yoffset_maxpoint + 2*self.m1_pitch
        self.width = self.xoffset_inv + self.inv4x.width
        
    def create_instances(self):
        
        self.bank_sel_inv=self.add_inst(name="bank_sel_inv", 
                                        mod=self.inv_sel)
        self.connect_inst(["bank_sel", "bank_sel_bar", "vdd", "gnd"])

        self.logic_inst = []
        self.inv_inst = []
        for i in range(self.num_control_lines):
            input_name = self.input_control_signals[i]
            gated_name = self.control_signals[i]
            name_nand = "nand_{}".format(input_name)
            name_nor = "nor_{}".format(input_name)
            name_inv = "inv_{}".format(input_name)

            # These require OR (nor2+inv) gates since they are active low.
            # (writes occur on clk low)
            if input_name in ("clk_buf"):
                
                self.logic_inst.append(self.add_inst(name=name_nor, 
                                         mod=self.nor2))
                self.connect_inst([input_name,
                                   "bank_sel_bar",
                                   gated_name+"_temp_bar",
                                   "vdd",
                                   "gnd"])
                
                # They all get inverters on the output
                self.inv_inst.append(self.add_inst(name=name_inv, 
                                                   mod=self.inv4x_nor))
                self.connect_inst([gated_name+"_temp_bar",
                                   gated_name,
                                   "vdd",
                                   "gnd"])
                
            # the rest are AND (nand2+inv) gates
            else:
                self.logic_inst.append(self.add_inst(name=name_nand, 
                                                     mod=self.nand2))
                self.connect_inst([input_name,
                                   "bank_sel",
                                   gated_name+"_temp_bar",
                                   "vdd",
                                   "gnd"])

                # They all get inverters on the output
                self.inv_inst.append(self.add_inst(name=name_inv, 
                                                   mod=self.inv4x))
                self.connect_inst([gated_name+"_temp_bar",
                                   gated_name,
                                   "vdd",
                                   "gnd"])

    def place_instances(self):
        
        # bank select inverter
        self.bank_select_inv_position = vector(self.xoffset_bank_sel_inv, 0)

        # bank select inverter (must be made unique if more than one OR)
        self.bank_sel_inv.place(vector(self.xoffset_bank_sel_inv, 0))

        for i in range(self.num_control_lines):

            logic_inst = self.logic_inst[i]
            inv_inst = self.inv_inst[i]
            
            input_name = self.input_control_signals[i]

            if i == 0:
                y_offset = 0
            else:
                y_offset = self.inv4x_nor.height + self.inv4x.height * (i-1)
            
            if i%2:
                y_offset += self.inv4x.height
                mirror = "MX"
            else:
                mirror = ""
            
            # These require OR (nor2+inv) gates since they are active low.
            # (writes occur on clk low)
            if input_name in ("clk_buf"):
                
                logic_inst.place(offset=[self.xoffset_nor, y_offset],
                                 mirror=mirror)
                
            # the rest are AND (nand2+inv) gates
            else:
                logic_inst.place(offset=[self.xoffset_nand, y_offset],
                                 mirror=mirror)

            # They all get inverters on the output
            inv_inst.place(offset=[self.xoffset_inv, y_offset],
                           mirror=mirror)
            

    def route_instances(self):
        
        # bank_sel is vertical wire
        bank_sel_inv_pin = self.bank_sel_inv.get_pin("A")
        xoffset_bank_sel = bank_sel_inv_pin.lx()
        bank_sel_line_pos = vector(xoffset_bank_sel, 0)
        bank_sel_line_end = vector(xoffset_bank_sel, self.yoffset_maxpoint)
        self.add_path("metal2", [bank_sel_line_pos, bank_sel_line_end])
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=bank_sel_inv_pin.lc())

        # Route the pin to the left edge as well
        bank_sel_pin_pos=vector(0, 0)
        bank_sel_pin_end=vector(bank_sel_line_pos.x, bank_sel_pin_pos.y)
        self.add_layout_pin_segment_center(text="bank_sel",
                                           layer="metal3",
                                           start=bank_sel_pin_pos,
                                           end=bank_sel_pin_end)
        self.add_via_center(layers=("metal2","via2","metal3"),
                            offset=bank_sel_pin_end,
                            directions=("H","H"))

        # bank_sel_bar is vertical wire
        bank_sel_bar_pin = self.bank_sel_inv.get_pin("Z")
        xoffset_bank_sel_bar = bank_sel_bar_pin.rx()
        self.add_label_pin(text="bank_sel_bar",
                           layer="metal2",  
                           offset=vector(xoffset_bank_sel_bar, 0), 
                           height=self.inv4x.height)
        self.add_via_center(layers=("metal1","via1","metal2"),
                            offset=bank_sel_bar_pin.rc())
            
            
        for i in range(self.num_control_lines):

            logic_inst = self.logic_inst[i]
            inv_inst = self.inv_inst[i]
            
            input_name = self.input_control_signals[i]
            gated_name = self.control_signals[i]            
            if input_name in ("clk_buf"):
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
                                directions=("H","H"))

            
            # Connect the logic A input to the input pin
            logic_pos = logic_inst.get_pin("A").lc()
            input_pos = vector(0,logic_pos.y)
            self.add_via_center(layers=("metal1", "via1", "metal2"),
                                offset=logic_pos,
                                directions=("H","H"))
            self.add_via_center(layers=("metal2", "via2", "metal3"),
                                offset=logic_pos,
                                directions=("H","H"))
            self.add_layout_pin_segment_center(text=input_name,
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


        # Find the x offsets for where the vias/pins should be placed
        a_xoffset = self.logic_inst[0].lx()
        b_xoffset = self.inv_inst[0].lx()
        for num in range(self.num_control_lines):
            # Route both supplies
            for n in ["vdd", "gnd"]:
                supply_pin = self.inv_inst[num].get_pin(n)
                supply_offset = supply_pin.ll().scale(0,1)
                self.add_rect(layer="metal1",
                              offset=supply_offset,
                              width=self.width)

                # Add pins in two locations
                for xoffset in [a_xoffset, b_xoffset]:
                    pin_pos = vector(xoffset, supply_pin.cy())
                    self.add_via_center(layers=("metal1", "via1", "metal2"),
                                        offset=pin_pos,
                                        directions=("H","H"))
                    self.add_via_center(layers=("metal2", "via2", "metal3"),
                                        offset=pin_pos,
                                        directions=("H","H"))
                    self.add_layout_pin_rect_center(text=n,
                                                    layer="metal3",
                                                    offset=pin_pos)
            
            # Add vdd/gnd supply rails
            gnd_pin = inv_inst.get_pin("gnd")
            left_gnd_pos = vector(0, gnd_pin.cy())
            self.add_layout_pin_segment_center(text="gnd",
                                               layer="metal1",
                                               start=left_gnd_pos,
                                               end=gnd_pin.rc())
            
            vdd_pin = inv_inst.get_pin("vdd")
            left_vdd_pos = vector(0, vdd_pin.cy())
            self.add_layout_pin_segment_center(text="vdd",
                                               layer="metal1",
                                               start=left_vdd_pos,
                                               end=vdd_pin.rc())
