import debug
import design
import utils
from tech import GDS,layer

class tri_gate(design.design):
    """
    This module implements the tri gate cell used in the design for
    bit-line isolation. It is a hand-made cell, so the layout and
    netlist should be available in the technology library.  
    """

    pin_names = ["in", "out", "en", "en_bar", "gnd", "vdd"]
    (width,height) = utils.get_libcell_size("tri_gate", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "tri_gate", GDS["unit"])

    unique_id = 1
    
    def __init__(self, name=""):
        if name=="":
            name = "tri{0}".format(tri_gate.unique_id)
            tri_gate.unique_id += 1
        design.design.__init__(self, name)
        debug.info(2, "Create tri_gate")

        self.width = tri_gate.width
        self.height = tri_gate.height
        self.pin_map = tri_gate.pin_map

    def analytical_delay(self, corner, slew, load=0.0):
        from tech import spice
        r = spice["min_tx_r"]
        c_para = spice["min_tx_drain_c"]
        return self.cal_delay_with_rc(corner, r = r, c =  c_para+load, slew = slew)
        
    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        #Power in this module currently not defined. Returns 0 nW (leakage and dynamic).
        total_power = self.return_power() 
        return total_power

    def input_load(self):
        return 9*spice["min_tx_gate_c"]

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges to graph. Handmade cells must implement this manually."""
        #The cell has 6 net ports hard-coded in self.pin_names. The edges
        #are based on the hard-coded name positions.
        # The edges added are: en->out, en_bar->out, in->out.
        # A liberal amount of edges were added, may be reduced later for complexity.
        # Internal nodes of the handmade cell not considered, only ports. vdd/gnd ignored for graph.
        graph.add_edge(port_nets[0],port_nets[1])
        graph.add_edge(port_nets[2],port_nets[1])
        graph.add_edge(port_nets[3],port_nets[1])