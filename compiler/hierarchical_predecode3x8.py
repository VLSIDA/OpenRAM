from tech import drc
import debug
import design
from nand_3 import nand_3
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

    def create_nand(self):
        self.nand = nand_3(name="a_nand_3",
                           nmos_width=self.nmos_width,
                           height=self.bitcell_height)

    def set_rail_height(self):        
        self.rail_height = (self.number_of_outputs * self.nand.height 
                                - 1.5 * drc["minwidth_metal2"])
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

    def set_height(self):
        self.height = 8 * self.nand.height

    def cal_input_inverters_output(self,setup,output_shift,inv_rout):
        y_dir,inv_in_offset,inv_out_offset,inv_vdd_offset,inv_gnd_offset = setup
        correct = y_dir * (output_shift + drc["minwidth_metal1"])

        out_offset = inv_out_offset + vector(0, output_shift + correct)
        vertical1 = out_offset
        vertical2 = (vertical1.scale(1, 0) + inv_vdd_offset.scale(0, 1) 
                         + vector(0, - correct))
        horizontal1 = vertical1
        horizontal2 = vector(self.rails_x_offset[inv_rout + 5]  + drc["minwidth_metal2"],
                       vertical2.y) 
        return [[vertical1,vertical2],[horizontal1,horizontal2]]

    def set_output_shift(self):
        return 1.5 * drc["minwidth_metal1"]

    def get_nand_input_line_combination(self):
        combination = [[5, 6, 7], [5, 6, 10], 
                       [5, 9, 7], [5, 9, 10], 
                       [8, 6, 7], [8, 6, 10], 
                       [8, 9, 7], [8, 9, 10]]
        return combination

    def create_y_offsets(self,k):
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
        return yoffset_nand_in, correct

    def get_via_correct(self):
        return vector(0, self.via_shift+self.contact_shift)  

    def get_vertical_metal(self):
        return "metal2"

    def get_via_y(self):
        yoffset = (self.number_of_outputs * self.inv.height 
                       - 0.5 * drc["minwidth_metal1"])
        return yoffset
