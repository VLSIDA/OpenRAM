import debug
import design
import utils
from tech import GDS,layer

class write_driver(design.design):
    """
    Tristate write driver to be active during write operations only.       
    This module implements the write driver cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    """

    pin_names = ["din", "bl", "br", "en", "gnd", "vdd"]
    (width,height) = utils.get_libcell_size("write_driver", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "write_driver", GDS["unit"])

    def __init__(self, name):
        design.design.__init__(self, name)
        debug.info(2, "Create write_driver")

        self.width = write_driver.width
        self.height = write_driver.height
        self.pin_map = write_driver.pin_map


    def get_w_en_cin(self):
        """Get the relative capacitance of a single input"""
        # This is approximated from SCMOS. It has roughly 5 3x transistor gates.
        return 5*3

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges to graph. Handmade cells must implement this manually."""
        #The cell has 6 net ports hard-coded in self.pin_names. The edges
        #are based on the hard-coded name positions.
        # The edges added are: din->bl, din->br, en->bl, en->br
        # A liberal amount of edges were added, may be reduced later for complexity.
        # Internal nodes of the handmade cell not considered, only ports. vdd/gnd ignored for graph.
        graph.add_edge(port_nets[0],port_nets[1])
        graph.add_edge(port_nets[0],port_nets[2])
        graph.add_edge(port_nets[3],port_nets[1])
        graph.add_edge(port_nets[3],port_nets[2])