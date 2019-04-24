import design
import debug
import utils
from tech import GDS,layer,drc,parameter

class replica_bitcell_1w_1r(design.design):
    """
    A single bit cell which is forced to store a 0.
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    pin_names = ["bl0", "br0", "bl1", "br1", "wl0", "wl1", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("replica_cell_1w_1r", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "replica_cell_1w_1r", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument        
        design.design.__init__(self, "replica_cell_1w_1r")
        debug.info(2, "Create replica bitcell 1w+1r object")

        self.width = replica_bitcell_1w_1r.width
        self.height = replica_bitcell_1w_1r.height
        self.pin_map = replica_bitcell_1w_1r.pin_map

    def get_wl_cin(self):
        """Return the relative capacitance of the access transistor gates"""
        #This is a handmade cell so the value must be entered in the tech.py file or estimated.
        #Calculated in the tech file by summing the widths of all the related gates and dividing by the minimum width.
        #FIXME: sizing is not accurate with the handmade cell. Change once cell widths are fixed.
        access_tx_cin = parameter["6T_access_size"]/drc["minwidth_tx"]
        return 2*access_tx_cin

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges to graph. Handmade cells must implement this manually."""
        #The bitcell has 8 net ports hard-coded in self.pin_names. The edges
        #are based on the hard-coded name positions.
        # The edges added are: wl0->bl0, wl0->br0, wl1->bl1, wl1->br1.
        # Internal nodes of the handmade cell not considered, only ports. vdd/gnd ignored for graph.
        graph.add_edge(port_nets[4],port_nets[0])
        graph.add_edge(port_nets[4],port_nets[1])    
        graph.add_edge(port_nets[5],port_nets[2])
        graph.add_edge(port_nets[5],port_nets[3]) 