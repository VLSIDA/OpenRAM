# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import design
import debug
import utils
from tech import GDS,layer,parameter,drc
import logical_effort

class bitcell_1rw_1r(design.design):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    pin_names = ["bl0", "br0", "bl1", "br1", "wl0", "wl1", "vdd", "gnd"]
    type_list = ["OUTPUT", "OUTPUT", "OUTPUT", "OUTPUT", "INPUT", "INPUT", "POWER", "GROUND"] 
    storage_nets = ['Q', 'Q_bar']
    (width,height) = utils.get_libcell_size("cell_1rw_1r", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "cell_1rw_1r", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        design.design.__init__(self, "cell_1rw_1r")
        debug.info(2, "Create bitcell with 1RW and 1R Port")

        self.width = bitcell_1rw_1r.width
        self.height = bitcell_1rw_1r.height
        self.pin_map = bitcell_1rw_1r.pin_map
        self.add_pin_types(self.type_list)
        self.nets_match = self.do_nets_exist(self.storage_nets)
        
    def get_stage_effort(self, load):
        parasitic_delay = 1
        size = 0.5 #This accounts for bitline being drained thought the access TX and internal node
        cin = 3 #Assumes always a minimum sizes inverter. Could be specified in the tech.py file.
        read_port_load = 0.5 #min size NMOS gate load
        return logical_effort.logical_effort('bitline', size, cin, load+read_port_load, parasitic_delay, False)
   
    def get_bitcell_pins(self, col, row):
        """ Creates a list of connections in the bitcell, indexed by column and row, for instance use in bitcell_array """
        bitcell_pins = ["bl0_{0}".format(col),
                        "br0_{0}".format(col),
                        "bl1_{0}".format(col),
                        "br1_{0}".format(col),
                        "wl0_{0}".format(row),
                        "wl1_{0}".format(row),
                        "vdd",
                        "gnd"]
        return bitcell_pins
    
    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = ["wl0", "wl1"]    
        return row_pins
    
    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        column_pins = ["bl0", "br0", "bl1", "br1"]
        return column_pins
    
    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        column_pins = ["bl0", "bl1"]
        return column_pins
        
    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        column_pins = ["br0", "br1"]
        return column_pins
        
    def get_read_bl_names(self):
        """ Creates a list of bl pin names associated with read ports """
        column_pins = ["bl0", "bl1"]
        return column_pins
    
    def get_read_br_names(self):
        """ Creates a list of br pin names associated with read ports """
        column_pins = ["br0", "br1"]
        return column_pins
        
    def get_write_bl_names(self):
        """ Creates a list of bl pin names associated with write ports """
        column_pins = ["bl0"]
        return column_pins
    
    def get_write_br_names(self):
        """ Creates a list of br pin names asscociated with write ports"""
        column_pins = ["br0"]
        return column_pins
    
    def get_bl_name(self, port=0):
        """Get bl name by port"""
        debug.check(port<2,"Two ports for bitcell_1rw_1r only.")
        return "bl{}".format(port)
    
    def get_br_name(self, port=0):
        """Get bl name by port"""
        debug.check(port<2,"Two ports for bitcell_1rw_1r only.")
        return "br{}".format(port)

    def get_wl_name(self, port=0):
        """Get wl name by port"""
        debug.check(port<2,"Two ports for bitcell_1rw_1r only.")
        return "wl{}".format(port)
    
    def analytical_power(self, corner, load):
        """Bitcell power in nW. Only characterizes leakage."""
        from tech import spice
        leakage = spice["bitcell_leakage"]
        dynamic = 0 #temporary
        total_power = self.return_power(dynamic, leakage)
        return total_power

    def input_load(self):
        """Return the relative capacitance of the access transistor gates"""
        
        # FIXME: This applies to bitline capacitances as well.
        # FIXME: sizing is not accurate with the handmade cell. Change once cell widths are fixed.
        access_tx_cin = parameter["6T_access_size"]/drc["minwidth_tx"]
        return 2*access_tx_cin
        
    def get_storage_net_names(self):
        """Returns names of storage nodes in bitcell in  [non-inverting, inverting] format."""
        #Checks that they do exist
        if self.nets_match:
            return self.storage_nets
        else:
            debug.info(1,"Storage nodes={} not found in spice file.".format(self.storage_nets))
            return None    
        
    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges to graph. Multiport bitcell timing graph is too complex
           to use the add_graph_edges function."""
        pin_dict = {pin:port for pin,port in zip(self.pins, port_nets)} 
        #Edges hardcoded here. Essentially wl->bl/br for both ports.
        # Port 0 edges
        graph.add_edge(pin_dict["wl0"], pin_dict["bl0"], self)   
        graph.add_edge(pin_dict["wl0"], pin_dict["br0"], self)   
        # Port 1 edges
        graph.add_edge(pin_dict["wl1"], pin_dict["bl1"], self)   
        graph.add_edge(pin_dict["wl1"], pin_dict["br1"], self)   
