import debug
import design
import math
from tech import drc
from contact import contact
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
        # create_nand redefine in sub class based on number of inputs
        self.create_nand()
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
        # set_rail_height redefine in sub class
        self.set_rail_height()
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
        self.set_height()
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
            inout = str(self.number_of_inputs)+"x"+str(self.number_of_outputs)
            name = "Xpre"+inout+"_nand[{0}]".format(nand_input)
            if (nand_input % 2 == 0):
                y_off = nand_input * (self.nand.height)
                mirror = "R0"
                offset = [self.x_off_nand + self.nand.width,
                          y_off + self.nand.Z_position.y]
            else:
                y_off = (nand_input + 1) * (self.nand.height)
                mirror = "MX"
                offset =[self.x_off_nand + self.nand.width,
                         y_off - self.nand.Z_position.y - drc["minwidth_metal1"]]
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
        self.route_input_inverters()
        self.route_nand_to_rails()
        self.route_vdd_gnd_from_rails_to_gates()

    def route_input_inverters(self):
        # All conections of the inputs inverters [Inputs, outputs, vdd, gnd]
        output_shift = self.set_output_shift()
        for inv_rout in range(self.number_of_inputs):
            setup = self.setup_route_input_inverter(inv_rout,output_shift)
            y_dir,inv_in_offset,inv_out_offset,inv_vdd_offset,inv_gnd_offset = setup
            #add output
            correct = y_dir * (output_shift + drc["minwidth_metal1"])
            output_metal = self.cal_input_inverters_output(setup,output_shift,inv_rout)
            offset1,offset2=output_metal[0]
            offset3,offset4=output_metal[1]
            self.add_rect(layer="metal1",
                          offset=offset1,
                          width=drc["minwidth_metal1"],
                          height=offset2.y - offset1.y)
            self.add_rect(layer="metal1",
                          offset=offset3,
                          width=offset4.x - offset3.x,
                          height=drc["minwidth_metal1"])
            off_via = [self.rails_x_offset[inv_rout + self.number_of_inputs+2] + self.gap_between_rails,
                       inv_vdd_offset.y- self.via_shift - correct]
            self.add_via(layers = ("metal1", "via1", "metal2"),
                         offset=off_via,
                         rotate=90)
            #route input
            self.add_rect(layer="metal1",
                          offset=[self.rails_x_offset[inv_rout],
                                  inv_in_offset.y],
                          width=inv_in_offset.x - self.rails_x_offset[inv_rout] + drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.rails_x_offset[inv_rout] + self.gap_between_rails,
                                 inv_in_offset.y - self.via_shift],
                         rotate=90)
            # route vdd
            self.add_rect(layer="metal1",
                          offset=inv_vdd_offset,
                          width=self.rails_x_offset[self.number_of_inputs] - inv_vdd_offset.x + drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])
            # route gnd
            self.add_rect(layer="metal1",
                          offset=inv_gnd_offset,
                          width=self.rails_x_offset[self.number_of_inputs+1] - inv_gnd_offset.x + drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])

    def setup_route_input_inverter(self, inv_rout, output_shift):
        # add Inputs, vdd, gnd of the inputs inverters 
        if (inv_rout % 2 == 0):
            base_offset=[self.x_off_inv_1, inv_rout * self.inv.height ]
            y_dir = 1
        else:
            base_offset=[self.x_off_inv_1, 2 * self.inv.height - drc["minwidth_metal1"]]
            y_dir = -1
        inv_out_offset = base_offset+self.inv.Z_position.scale(1,y_dir)
        inv_in_offset = base_offset+self.inv.A_position.scale(1,y_dir)
        inv_vdd_offset = base_offset+self.inv.vdd_position.scale(1,y_dir)
        inv_gnd_offset = base_offset+self.inv.gnd_position.scale(1,y_dir)
        #return info to create output of the input inverter
        return [y_dir,inv_in_offset,inv_out_offset,inv_vdd_offset,inv_gnd_offset]

    def route_nand_to_rails(self):
        # This 2D array defines the connection mapping 
        nand_input_line_combination = self.get_nand_input_line_combination()
        for k in range(self.number_of_outputs):
            # create x offset list         
            index_lst= nand_input_line_combination[k]
            line_x_offset = []
            for index in index_lst:
                line_x_offset.append(self.rails_x_offset[index])
            # create y offset list
            yoffset_nand_in, correct= self.create_y_offsets(k)
            # connect based on the two list
            for i in range(self.number_of_inputs):
                x_offset = line_x_offset[i]
                y_offset = yoffset_nand_in[i]
                # Connecting the i-th input of Nand3 gate
                self.add_rect(layer="metal1",
                              offset=[x_offset, y_offset],
                              width=self.x_off_nand - x_offset,
                              height=drc["minwidth_metal1"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[x_offset+ self.gap_between_rails,
                                     y_offset - self.via_shift - correct[i]],
                             rotate=90) 
                # Extended of the top NAND2 to the left hand side input rails
                if(k == self.number_of_outputs - 1):
                    x_offset = self.rails_x_offset[i]
                    self.add_rect(layer="metal1",
                                  offset=[x_offset, y_offset],
                                  width=self.x_off_nand - x_offset,
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers = ("metal1", "via1", "metal2"),
                                 offset=[x_offset + self.gap_between_rails,
                                         y_offset - self.via_shift],
                                 rotate=90)

    def route_vdd_gnd_from_rails_to_gates(self):
        via_correct = self.get_via_correct()
        for k in range(self.number_of_outputs):
            power_line_index = self.number_of_inputs + 1 - (k%2)
            yoffset = k * self.inv.height -  0.5 * drc["minwidth_metal1"]
            self.add_rect(layer="metal1",
                          offset=[self.rails_x_offset[power_line_index],
                                  yoffset],
                          width=self.x_off_nand - self.rails_x_offset[power_line_index],
                          height=drc["minwidth_metal1"])
            self.add_via(layers = ("metal1", "via1", "metal2"),
                         offset=[self.rails_x_offset[power_line_index] + self.gap_between_rails,
                                 yoffset - via_correct.y],
                         rotate=90)

        yoffset = (self.number_of_outputs * self.inv.height 
                       - 0.5 * drc["minwidth_metal1"])
        v_metal = self.get_vertical_metal()
        via_y = self.get_via_y()
        index = self.number_of_inputs + 1
        self.add_rect(layer="metal1",
                      offset=[self.rails_x_offset[index], yoffset],
                      width=self.x_off_nand - self.rails_x_offset[index],
                      height=drc["minwidth_metal1"])
        self.add_rect(layer=v_metal,
                      offset=[self.rails_x_offset[index], self.rail_height],
                      width=drc["minwidth_"+v_metal],
                      height=yoffset - self.rail_height)
        self.add_via(layers = ("metal1", "via1", "metal2"),
                     offset=[self.rails_x_offset[index] + self.gap_between_rails,
                             via_y] - via_correct,
                     rotate=90)
