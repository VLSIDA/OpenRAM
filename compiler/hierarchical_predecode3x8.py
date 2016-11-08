from tech import drc
import debug
import design
from vector import vector
from hierarchical_predecode import hierarchical_predecode


class hierarchical_predecode3x8(hierarchical_predecode):
    """
    Pre 3x8 decoder used in hierarchical_decoder.
    """
    def __init__(self, nmos_width, cellname):
        hierarchical_predecode.__init__(self, nmos_width, cellname, 3)

        self.add_pins()
        self.create_modules()
        self.setup_constrains()
        self.create_layout()
        self.route()

    def create_layout(self):
        self.create_rails()
        self.add_output_inverters()
        connections=[["A[0]", "A[1]", "A[2]", "Z[7]", "vdd", "gnd"],
                     ["A[0]", "A[1]", "B[2]", "Z[6]", "vdd", "gnd"],
                     ["A[0]", "B[1]", "A[2]", "Z[5]", "vdd", "gnd"],
                     ["A[0]", "B[1]", "B[2]", "Z[4]", "vdd", "gnd"],
                     ["B[0]", "A[1]", "A[2]", "Z[3]", "vdd", "gnd"],
                     ["B[0]", "A[1]", "B[2]", "Z[2]", "vdd", "gnd"],
                     ["B[0]", "B[1]", "A[2]", "Z[1]", "vdd", "gnd"],
                     ["B[0]", "B[1]", "B[2]", "Z[0]", "vdd", "gnd"]]
        self.add_nand(connections)

    def route_input_inverters(self):
        # All conections of the inputs inverters [Inputs, outputs, vdd, gnd]
        for inv_rout in range(self.number_of_inputs):
            output_shift = 1.5 * drc["minwidth_metal1"]

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
            # output connection
            correct = y_dir * (output_shift + drc["minwidth_metal1"])
            off_via = [self.rails_x_offset[inv_rout + 5] + self.gap_between_rails,
                       inv_vdd_offset[1] - self.via_shift - correct]
            path1 = vector(inv_out_offset[0] + 0.5*drc["minwidth_metal1"],
                           inv_out_offset[1]- 1.5*drc["minwidth_metal1"] - correct)
            path2 = vector(path1.x,
                           inv_vdd_offset[1] + 0.5 * drc["minwidth_metal1"] - correct)
            path3 = vector(self.rails_x_offset[inv_rout + 5]  + drc["minwidth_metal2"],
                           path2.y) 
            self.add_path("metal1", [path1,path2,path3])           
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=off_via,
                         rotate=90)
            self.route_input_inverters_input(inv_rout,inv_in_offset)
            self.route_input_inverters_vdd(inv_vdd_offset)
            self.route_input_inverters_gnd(inv_gnd_offset)

    def route_nand_to_rails(self):
        # This 2D array defines the connection mapping of the Nand3 gates to
        # the rail
        nand3_input_line_combination = [[5, 6, 7], [5, 6, 10], 
                                        [5, 9, 7], [5, 9, 10], 
                                        [8, 6, 7], [8, 6, 10], 
                                        [8, 9, 7], [8, 9, 10]]
        for k in range(self.number_of_outputs):
            index_lst = nand3_input_line_combination[k]
            line_x_offset = []
            for index in index_lst:
                line_x_offset.append(self.rails_x_offset[index])

            if (k % 2 == 0):
                y_off = k * (self.nand.height)
                y_dir =1
                correct = [0,0,self.contact_shift]
            else:
                y_off = 2 * self.inv.height - drc["minwidth_metal1"] + (k - 1) * (self.nand.height)
                y_dir = -1
                correct = [0,self.contact_shift,0]
            yoffset_nand_in = [y_off +  y_dir*self.nand.A_position[1],
                               y_off +  y_dir*self.nand.B_position[1],
                               y_off +  y_dir*self.nand.C_position[1]]

            for i in range(self.number_of_inputs):
                # Connecting the i-th input of Nand3 gate
                self.add_rect(layer="metal1",
                              offset=[line_x_offset[i], yoffset_nand_in[i]],
                              width=self.x_off_nand - line_x_offset[i],
                              height=drc["minwidth_metal1"])
                self.add_via(layers=("metal1", "via1", "metal2"),
                             offset=[line_x_offset[i]+ self.gap_between_rails,
                                     yoffset_nand_in[i] - self.via_shift - correct[i]],
                             rotate=90)    
            #Extended of the top NAND2 to the left hand side input rails
            if(k == self.number_of_outputs - 1):
                for i in range(self.number_of_inputs):
                    self.add_rect(layer="metal1",
                                  offset=[self.rails_x_offset[i], yoffset_nand_in[i]],
                                  width=self.x_off_nand - self.rails_x_offset[i],
                                  height=drc["minwidth_metal1"])
                    self.add_via(layers=("metal1", "via1", "metal2"),
                                 offset=[self.rails_x_offset[i] + self.gap_between_rails,
                                         yoffset_nand_in[i] - self.via_shift],
                                 rotate=90)

    def route_vdd_gnd_from_rails_to_gates(self):
        for k in range(self.number_of_outputs):
            power_line_index = 4 - (k%2)
            yoffset = k * self.inv.height - 0.5 * drc["minwidth_metal1"]
            self.add_rect(layer="metal1",
                          offset=[self.rails_x_offset[power_line_index], yoffset],
                          width=self.x_off_nand - self.rails_x_offset[power_line_index],
                          height=drc["minwidth_metal1"])
            self.add_via(layers=("metal1", "via1", "metal2"),
                         offset=[self.rails_x_offset[power_line_index] + self.gap_between_rails,
                                 yoffset - self.via_shift - self.contact_shift],
                         rotate=90)

        yoffset = (self.number_of_outputs * self.inv.height 
                       - 0.5 * drc["minwidth_metal1"])
        self.add_rect(layer="metal1",
                      offset=[self.rails_x_offset[4], yoffset],
                      width=self.x_off_nand - self.rails_x_offset[4],
                      height=drc["minwidth_metal1"])

        self.add_rect(layer="metal2",
                      offset=[self.rails_x_offset[4], self.rail_height],
                      width=drc["minwidth_metal2"],
                      height=yoffset - self.rail_height)
        self.add_via(layers=("metal1", "via1", "metal2"),
                     offset=[self.rails_x_offset[4] + self.gap_between_rails - self.via_shift,
                             yoffset - self.via_shift - self.contact_shift],
                     rotate=90)
