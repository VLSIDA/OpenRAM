from tech import drc
import debug
import design
from vector import vector
from hierarchical_predecode import hierarchical_predecode

class hierarchical_predecode2x4(hierarchical_predecode):
    """
    Pre 2x4 decoder used in hierarchical_decoder.
    """

    def __init__(self, nmos_width, cellname):
        hierarchical_predecode.__init__(self, nmos_width, cellname, 2)

        self.add_pins()
        self.create_modules()
        self.setup_constrains()
        self.create_layout()
        self.route()

    def create_layout(self):
        self.create_rails()
        self.add_inv2x4()
        self.add_output_inverters()
        connections =[["A[0]", "A[1]", "Z[3]", "vdd", "gnd"],
                      ["B[0]", "A[1]", "Z[2]", "vdd", "gnd"],
                      ["A[0]", "B[1]", "Z[1]", "vdd", "gnd"],
                      ["B[0]", "B[1]", "Z[0]", "vdd", "gnd"]]
        self.add_nand(connections)

    def add_inv2x4(self):
        self.A_positions = []
        for inv_2x4 in range(self.number_of_inputs):
            name = "Xpre2x4_inv[{0}]".format(inv_2x4)
            if (inv_2x4 % 2 == 0):
                y_off = inv_2x4 * (self.inv.height)
                offset = vector(self.x_off_inv_1, y_off)
                mirror = "R0"
                A_off = self.inv.A_position.scale(0, 1)
            else:
                y_off = (inv_2x4 + 1) * (self.inv.height)
                offset = vector(self.x_off_inv_1, y_off)
                mirror="MX"
                A_off = vector(0, - self.inv.A_position.y - drc["minwidth_metal1"])
            self.A_positions.append(offset + A_off)
            self.add_inst(name=name,
                          mod=self.inv,
                          offset=offset,
                          mirror=mirror)
            self.connect_inst(["A[{0}]".format(inv_2x4),
                               "B[{0}]".format(inv_2x4),
                               "vdd", "gnd"])

    def route_input_inverters(self):
        # All conections of the inputs inverters [Inputs, outputs, vdd, gnd]
        output_shift = 2 * drc["minwidth_metal1"]
        for inv_rout in range(self.number_of_inputs):
            if (inv_rout % 2 == 0):
                y_dir= 1
            else:
                y_dir= -1
            base = vector(self.x_off_inv_1, 
                         (1-y_dir) * (self.inv.height - 0.5 * drc["minwidth_metal1"]))
            inv_out_offset = base + self.inv.Z_position.scale(1,y_dir)
            inv_in_offset = base + self.inv.A_position.scale(1,y_dir)
            inv_vdd_offset = base + self.inv.vdd_position.scale(1,y_dir)
            inv_gnd_offset = base + self.inv.gnd_position.scale(1,y_dir)
            out_y_mirrored = inv_vdd_offset[1] + output_shift + drc["minwidth_metal1"]
            out_offset = [inv_out_offset[0],
                          inv_out_offset[1] * (1 + y_dir) / 2
                              + out_y_mirrored * (1 - y_dir) / 2]  
            # output connection
            correct = y_dir * (output_shift + drc["minwidth_metal1"])
            off_via = [self.rails_x_offset[inv_rout + 4] + self.gap_between_rails,
                       inv_vdd_offset[1] - self.via_shift - correct]
            self.add_rect(layer="metal1",
                          offset=out_offset,
                          width=drc["minwidth_metal1"],
                          height=(inv_vdd_offset[1] - inv_out_offset[1]) * y_dir - output_shift)
            self.add_rect(layer="metal1",
                          offset=[inv_out_offset[0],
                                  inv_vdd_offset[1] - correct],
                          width=self.rails_x_offset[inv_rout + 4] - inv_out_offset[0] + drc["minwidth_metal2"],
                          height=drc["minwidth_metal1"])
            self.add_via(layers = ("metal1", "via1", "metal2"),
                         offset=off_via,
                         rotate=90)
            self.route_input_inverters_input(inv_rout,inv_in_offset)
            self.route_input_inverters_vdd(inv_vdd_offset)
            self.route_input_inverters_gnd(inv_gnd_offset)

    def route_nand_to_rails(self):
        # This 2D array defines the connection mapping 
        nand2_input_line_combination = [[4, 5], [6, 5], [4, 7], [6, 7]]
        for k in range(self.number_of_outputs):
            # create x offset list         
            x_index = nand2_input_line_combination[k]
            line_x_offset = [self.rails_x_offset[x_index[0]],
                             self.rails_x_offset[x_index[1]]]
            # create y offset list
            if (k % 2 == 0):
                y_off = k * (self.nand.height)
                direct = 1
            else:
                y_off = (k + 1) * (self.nand.height) - drc["minwidth_metal1"]
                direct = - 1
            list_connect = [y_off + direct * self.nand.A_position.y, 
                            y_off + direct * self.nand.B_position.y]
            # connect based on the two list
            for connect in list_connect:
                x_offset = line_x_offset[list_connect.index(connect)]
                self.add_rect(layer="metal1",
                              offset=[x_offset, connect],
                              width=self.x_off_nand - x_offset, 
                              height=drc["minwidth_metal1"])
                self.add_via(layers = ("metal1", "via1", "metal2"),
                             offset=[x_offset + self.gap_between_rails,
                                     connect - self.via_shift],
                             rotate=90)
                # Extended of the top NAND2 to the left hand side input rails
                if(k == self.number_of_outputs - 1):
                    x_offset = self.rails_x_offset[list_connect.index(connect)]
                    self.add_rect(layer="metal1",
                                  offset=[x_offset, connect],
                                  width=self.x_off_nand - x_offset,
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers = ("metal1", "via1", "metal2"),
                                 offset=[x_offset + self.gap_between_rails,
                                         connect - self.via_shift],
                                 rotate=90)

    def route_vdd_gnd_from_rails_to_gates(self):
        for k in range(self.number_of_outputs):
            power_line_index = 3 - (k%2)
            yoffset = k * self.inv.height -  0.5 * drc["minwidth_metal1"]
            self.add_rect(layer="metal1",
                          offset=[self.rails_x_offset[power_line_index],
                                  yoffset],
                          width=self.x_off_nand - self.rails_x_offset[power_line_index],
                          height=drc["minwidth_metal1"])
            self.add_via(layers = ("metal1", "via1", "metal2"),
                         offset=[self.rails_x_offset[power_line_index] + self.gap_between_rails,
                                 yoffset - self.via_shift],
                         rotate=90)
            
        yoffset = (self.number_of_outputs * self.inv.height 
                        - 0.5 * drc["minwidth_metal1"])
        self.add_rect(layer="metal1",
                      offset=[self.rails_x_offset[3], yoffset],
                      width=self.x_off_nand - self.rails_x_offset[3],
                      height=drc["minwidth_metal1"])
        self.add_rect(layer="metal1",
                      offset=[self.rails_x_offset[3], self.rail_height],
                      width=drc["minwidth_metal1"],
                      height=yoffset - self.rail_height)
        self.add_via(layers = ("metal1", "via1", "metal2"),
                     offset=[self.rails_x_offset[3] + self.gap_between_rails,
                             self.rail_height - self.via_shift],
                     rotate=90)
