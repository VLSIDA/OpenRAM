from tech import drc
import debug
import design
from nand_2 import nand_2
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

    def create_nand(self):
        self.nand = nand_2(name="a_nand_2",
                           nmos_width=self.nmos_width,
                           height=self.bitcell_height)

    def set_rail_height(self):
        self.rail_height = (self.number_of_outputs * self.nand.height 
                                 - (self.number_of_outputs - 1) * drc["minwidth_metal2"])

    def create_layout(self):
        self.create_rails()
        self.add_inv2x4()
        self.add_output_inverters()
        connections =[["A[0]", "A[1]", "Z[3]", "vdd", "gnd"],
                      ["B[0]", "A[1]", "Z[2]", "vdd", "gnd"],
                      ["A[0]", "B[1]", "Z[1]", "vdd", "gnd"],
                      ["B[0]", "B[1]", "Z[0]", "vdd", "gnd"]]
        self.add_nand(connections)

    def set_height(self):
        self.height = 4 * self.nand.height

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

    def cal_input_inverters_output(self,setup,output_shift,inv_rout):
        y_dir,inv_in_offset,inv_out_offset,inv_vdd_offset,inv_gnd_offset = setup
        correct = y_dir * (output_shift + drc["minwidth_metal1"])
        out_offset = vector(inv_out_offset)
        if y_dir == -1:
            out_offset.y = inv_vdd_offset.y + output_shift + drc["minwidth_metal1"]

        vertical1 = out_offset
        vertical2 = vertical1 + vector(0,
                                       (inv_vdd_offset.y - inv_out_offset.y) * y_dir 
                                           - output_shift)
        horizontal1 = vector(inv_out_offset.x,
                             inv_vdd_offset.y - correct)
        horizontal2 = horizontal1 + vector(self.rails_x_offset[inv_rout + 4] - inv_out_offset.x+ drc["minwidth_metal2"],
                                           0)
        return [[vertical1,vertical2],[horizontal1,horizontal2]]

    def set_output_shift(self):
        return 2 * drc["minwidth_metal1"]

    def get_nand_input_line_combination(self):
        combination = [[4, 5], [6, 5], [4, 7], [6, 7]]
        return combination 

    def create_y_offsets(self,k):
        # create y offset list
        if (k % 2 == 0):
            y_off = k * (self.nand.height)
            direct = 1
        else:
            y_off = (k + 1) * (self.nand.height) - drc["minwidth_metal1"]
            direct = - 1
        correct =[0,0]
        yoffset_nand_in = [y_off + direct * self.nand.A_position.y, 
                           y_off + direct * self.nand.B_position.y]
        return yoffset_nand_in, correct

    def get_via_correct(self):
        return vector(0, self.via_shift)  

    def get_vertical_metal(self):
        return "metal1"

    def get_via_y(self):
        return self.rail_height
