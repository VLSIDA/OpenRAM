from tech import drc
import debug
import design
from vector import vector
from hierarchical_predecode import hierarchical_predecode

class hierarchical_predecode3x8(hierarchical_predecode):
    """
    Pre 3x8 decoder used in hierarchical_decoder.
    """
    def __init__(self):
        hierarchical_predecode.__init__(self, 3)

        self.add_pins()
        self.create_modules()
        self.setup_constraints()
        self.create_layout()
        self.DRC_LVS()

    def create_layout(self):
        """ The general organization is from left to right:
        1) a set of M2 rails for input signals
        2) a set of inverters to invert input signals
        3) a set of M2 rails for the vdd, gnd, inverted inputs, inputs
        4) a set of NAND gates for inversion
        """
        self.create_rails()
        self.add_input_inverters()
        self.add_output_inverters()
        connections=[["inbar[0]", "inbar[1]", "inbar[2]", "Z[0]", "vdd", "gnd"],
                     ["in[0]",    "inbar[1]", "inbar[2]", "Z[1]", "vdd", "gnd"],            
                     ["inbar[0]", "in[1]",    "inbar[2]", "Z[2]", "vdd", "gnd"],
                     ["in[0]",    "in[1]",    "inbar[2]", "Z[3]", "vdd", "gnd"],            
                     ["inbar[0]", "inbar[1]", "in[2]",    "Z[4]", "vdd", "gnd"],
                     ["in[0]",    "inbar[1]", "in[2]",    "Z[5]", "vdd", "gnd"],
                     ["inbar[0]", "in[1]",    "in[2]",    "Z[6]", "vdd", "gnd"],
                     ["in[0]",    "in[1]",    "in[2]",    "Z[7]", "vdd", "gnd"]]
        self.add_nand(connections)
        self.route()

    def get_nand_input_line_combination(self):
        """ These are the decoder connections of the NAND gates to the A,B,C pins """
        combination = [["Abar[0]", "Abar[1]", "Abar[2]"],
                       ["A[0]",    "Abar[1]", "Abar[2]"],
                       ["Abar[0]", "A[1]",    "Abar[2]"],
                       ["A[0]",    "A[1]",    "Abar[2]"],
                       ["Abar[0]", "Abar[1]", "A[2]"], 
                       ["A[0]",    "Abar[1]", "A[2]"], 
                       ["Abar[0]", "A[1]",    "A[2]"], 
                       ["A[0]",    "A[1]",    "A[2]"]]
        return combination


    def analytical_delay(self, slew, load = 0.0 ):
        # A -> Abar
        a_t_b_delay = self.inv.analytical_delay(slew=slew, load=self.nand.input_load())

        # Abar -> z
        b_t_z_delay = self.nand.analytical_delay(slew=a_t_b_delay.slew, load=self.inv.input_load())

        # Z -> out
        a_t_out_delay = self.inv.analytical_delay(slew=b_t_z_delay.slew, load=load)

        return a_t_b_delay + b_t_z_delay + a_t_out_delay


    def input_load(self):
        return self.nand.input_load()
