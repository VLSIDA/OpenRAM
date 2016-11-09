import debug
import design
import math
from tech import drc
from contact import contact
from nand_2 import nand_2
from nand_3 import nand_3
from pinv import pinv
from vector import vector
from globals import OPTS


class hierarchical_predecode(design.design):
    """
    Pre 2x4 and 3x8 decoder shared code.
    """
    def __init__(self, nmos_width, cellname, input_number):
        design.design.__init__(self, cellname)

        c = reload(__import__(OPTS.config.bitcell))
        self.mod_bitcell = getattr(c, OPTS.config.bitcell)
        self.bitcell_height = self.mod_bitcell.chars["height"]

        self.nmos_width = nmos_width
        self.number_of_inputs = input_number
        self.number_of_outputs = int(math.pow(2, self.number_of_inputs))
    
    def add_pins(self):
        for k in range(self.number_of_inputs):
            self.add_pin("A[{0}]".format(k))
        for i in range(self.number_of_outputs):
            self.add_pin("out[{0}]".format(i))
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_modules(self):
        layer_stack = ("metal1", "via1", "metal2")
        self.m1m2_via = contact(layer_stack=layer_stack) 
        self.inv = pinv(name="a_inv_1",
                        nmos_width=drc["minwidth_tx"],
                        beta=2,
                        height=self.bitcell_height)
        self.add_mod(self.inv)
        if self.number_of_inputs ==2:
            self.nand = nand_2(name="a_nand_2",
                                nmos_width=self.nmos_width,
                                height=self.bitcell_height)
        elif self.number_of_inputs ==3:
            self.nand = nand_3(name="a_nand_3",
                                nmos_width=self.nmos_width,
                                height=self.bitcell_height)
        self.add_mod(self.nand)

    def set_up_constrain(self):
        self.via_shift = (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) / 2
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height - self.m1m2_via.contact_width) / 2
        self.via_shift = (self.m1m2_via.second_layer_width
                              - self.m1m2_via.first_layer_width) / 2
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height 
                                          - self.m1m2_via.contact_width) / 2

        self.gap_between_rails = (self.metal2_extend_contact 
                                 + drc["metal2_to_metal2"])
        self.gap_between_rail_offset = (self.gap_between_rails 
                                       + drc["minwidth_metal2"])

    def setup_constrains(self):
        self.via_shift = (self.m1m2_via.second_layer_width - self.m1m2_via.first_layer_width) / 2
        self.metal2_extend_contact = (self.m1m2_via.second_layer_height - self.m1m2_via.contact_width) / 2

        # Contact shift used connecting NAND3 inputs to the rail
        self.contact_shift = (self.m1m2_via.first_layer_width - self.m1m2_via.contact_width) / 2

        self.gap_between_rails = self.metal2_extend_contact + drc["metal2_to_metal2"]
        self.gap_between_rail_offset = self.gap_between_rails + drc["minwidth_metal2"]          

        self.rails_x_offset = []
        if self.number_of_inputs == 2:
            self.rail_height = (self.number_of_outputs * self.nand.height 
                                     - (self.number_of_outputs - 1) * drc["minwidth_metal2"])
        elif self.number_of_inputs == 3:
            self.rail_height = (self.number_of_outputs * self.nand.height 
                                        - 1.5 * drc["minwidth_metal2"])
        # Creating the left hand side metal2 rails for input connections
        for hrail_1 in range(self.number_of_inputs):
            xoffset_1 = (self.metal2_extend_contact 
                             + (hrail_1 * self.gap_between_rail_offset))
            self.rails_x_offset.append(xoffset_1)
        # x offset for Xpre2x4_inv
        self.x_off_inv_1 = self.rails_x_offset[-1] + self.gap_between_rail_offset
        # Creating the right hand side metal2 rails for output connections
        for hrail_2 in range(2 * self.number_of_inputs + 2):
            xoffset_2 = self.x_off_inv_1 + self.inv.width + self.gap_between_rails + (hrail_2 * self.gap_between_rail_offset)
            self.rails_x_offset.append(xoffset_2)
        self.xoffset_2=self.rails_x_offset[-1]

        self.x_off_nand = self.xoffset_2 + self.gap_between_rail_offset
        self.x_off_inv_2 = self.x_off_nand + self.nand.width
        self.update_size()

    def update_size(self):
        self.width = self.x_off_inv_2 + self.inv.width
        if self.number_of_inputs ==2:
            self.height = 4 * self.nand.height
        elif self.number_of_inputs ==3:
            self.height = 8 * self.nand.height
        self.size = vector(self.width, self.height)
        correct =vector(0, 0.5 * drc["minwidth_metal1"])
        self.vdd_position = self.size - correct - vector(0, self.inv.height)
        self.gnd_position = self.size - correct 

    def create_rails(self):
        for x_off in self.rails_x_offset:
            self.add_rect(layer="metal2",
                          offset=[x_off, 0], 
                          width=drc["minwidth_metal2"],
                          height=self.rail_height)

    def add_output_inverters(self):
        self.decode_out_positions = []
        for inv_2x4 in range(self.number_of_outputs):
            name = "Xpre2x4_nand_inv[{0}]".format(inv_2x4)
            if (inv_2x4 % 2 == 0):
                y_factor = inv_2x4 
                mirror = "R0"
                correct = self.inv.Z_position       
            else:
                y_factor =inv_2x4 + 1
                mirror = "MX"   
                correct = self.inv.Z_position.scale(1,-1) - vector(0, 
                                                                   drc["minwidth_metal1"])
            base = vector(self.x_off_inv_2, self.inv.height * y_factor)   
            self.add_inst(name=name,
                          mod=self.inv,
                          offset=base,
                          mirror=mirror)
            self.connect_inst(["Z[{0}]".format(inv_2x4),
                               "out[{0}]".format(inv_2x4),
                               "vdd", "gnd"])
            output_inv_out_offset = base + correct
            self.decode_out_positions.append(output_inv_out_offset)

    def add_nand(self,connections):
        for nand_input in range(self.number_of_outputs):
            if self.number_of_inputs ==2:
                name = "Xpre2x4_nand[{0}]".format(nand_input)
            elif self.number_of_inputs ==3:
                name = "Xpre3x8_nand[{0}]".format(nand_input)
            if (nand_input % 2 == 0):
                y_off = nand_input * (self.nand.height)
                mirror = "R0"
                offset = [self.x_off_nand + self.nand.width,
                          y_off + self.nand.Z_position[1]]
            else:
                y_off = (nand_input + 1) * (self.nand.height)
                mirror = "MX"
                offset =[self.x_off_nand + self.nand.width,
                         y_off - self.nand.Z_position[1] - drc["minwidth_metal1"]]
            self.add_inst(name=name,
                          mod=self.nand,
                          offset=[self.x_off_nand, y_off],
                          mirror=mirror)
            self.add_rect(layer="metal1",
                          offset=offset,
                          width=drc["minwidth_metal1"],
                          height=drc["minwidth_metal1"])
            self.connect_inst(connections[nand_input])

    def route(self):
        # route sub funtions need to be redfined in sub class
        self.route_input_inverters()
        self.route_nand_to_rails()
        self.route_vdd_gnd_from_rails_to_gates()

    def route_input_inverters_input(self,inv_rout,inv_in_offset):
        self.add_rect(layer="metal1",
                      offset=[self.rails_x_offset[inv_rout],
                              inv_in_offset[1]],
                      width=inv_in_offset[0] - self.rails_x_offset[inv_rout] + drc["minwidth_metal2"],
                      height=drc["minwidth_metal1"])
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.rails_x_offset[inv_rout] + self.gap_between_rails,
                             inv_in_offset[1] - self.via_shift],
                     rotate=90)

    def route_input_inverters_vdd(self,inv_vdd_offset):
        self.add_rect(layer="metal1",
                      offset=inv_vdd_offset,
                      width=self.rails_x_offset[self.number_of_inputs] - inv_vdd_offset[0] + drc["minwidth_metal2"],
                      height=drc["minwidth_metal1"])

    def route_input_inverters_gnd(self,inv_gnd_offset):
        self.add_rect(layer="metal1",
                      offset=inv_gnd_offset,
                      width=self.rails_x_offset[self.number_of_inputs+1] - inv_gnd_offset[0] + drc["minwidth_metal2"],
                      height=drc["minwidth_metal1"])
