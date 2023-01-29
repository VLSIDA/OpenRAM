# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.tech import cell_properties as props
from .bitcell_base import bitcell_base


class bitcell_2port(bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    def __init__(self, name):
        super().__init__(name, prop=props.bitcell_2port)
        debug.info(2, "Create bitcell with 2 ports")

        self.bl_names = ["bl0", "bl1"]
        self.br_names = ["br0", "br1"]
        self.wl_names = ["wl0", "wl1"]

    def get_bitcell_pins(self, col, row):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
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
        return self.wl_names

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        return ["bl0", "br0", "bl1", "br1"]

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return ["bl0", "bl1"]

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return ["br0", "br1"]

    def get_read_bl_names(self):
        """ Creates a list of bl pin names associated with read ports """
        return ["bl0", "bl1"]

    def get_read_br_names(self):
        """ Creates a list of br pin names associated with read ports """
        return ["br0", "br1"]

    def get_write_bl_names(self):
        """ Creates a list of bl pin names associated with write ports """
        return ["bl0"]

    def get_write_br_names(self):
        """ Creates a list of br pin names asscociated with write ports"""
        return ["br1"]

    def get_bl_name(self, port=0):
        """Get bl name by port"""
        debug.check(port < 2, "Two ports for bitcell_2port only.")
        return self.bl_names[port]

    def get_br_name(self, port=0):
        """Get bl name by port"""
        debug.check(port < 2, "Two ports for bitcell_2port only.")
        return self.br_names[port]

    def get_wl_name(self, port=0):
        """Get wl name by port"""
        debug.check(port < 2, "Two ports for bitcell_2port only.")
        return self.wl_names[port]

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges to graph. Multiport bitcell timing graph is too complex
           to use the add_graph_edges function."""
        pin_dict = {pin: port for pin, port in zip(self.get_original_pin_names(), port_nets)}
        # Edges hardcoded here. Essentially wl->bl/br for both ports.
        # Port 0 edges
        graph.add_edge(pin_dict["wl0"], pin_dict["bl0"], self)
        graph.add_edge(pin_dict["wl0"], pin_dict["br0"], self)
        # Port 1 edges
        graph.add_edge(pin_dict["wl1"], pin_dict["bl1"], self)
        graph.add_edge(pin_dict["wl1"], pin_dict["br1"], self)
