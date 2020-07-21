# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
import debug
import utils
from tech import GDS, layer
from tech import cell_properties as props
import bitcell_base


class bitcell_1w_1r(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    pin_names = [props.bitcell.cell_1w1r.pin.bl0,
                 props.bitcell.cell_1w1r.pin.br0,
                 props.bitcell.cell_1w1r.pin.bl1,
                 props.bitcell.cell_1w1r.pin.br1,
                 props.bitcell.cell_1w1r.pin.wl0,
                 props.bitcell.cell_1w1r.pin.wl1,
                 props.bitcell.cell_1w1r.pin.vdd,
                 props.bitcell.cell_1w1r.pin.gnd]
    type_list = ["OUTPUT", "OUTPUT", "INPUT", "INPUT",
                 "INPUT", "INPUT", "POWER", "GROUND"]
    storage_nets = ['Q', 'Q_bar']
    (width, height) = utils.get_libcell_size("cell_1w_1r",
                                             GDS["unit"],
                                             layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "cell_1w_1r", GDS["unit"])

    def __init__(self, name=""):
        # Ignore the name argument
        bitcell_base.bitcell_base.__init__(self, "cell_1w_1r")
        debug.info(2, "Create bitcell with 1W and 1R Port")

        self.width = bitcell_1w_1r.width
        self.height = bitcell_1w_1r.height
        self.pin_map = bitcell_1w_1r.pin_map
        self.add_pin_types(self.type_list)
        self.nets_match = self.do_nets_exist(self.storage_nets)

        pin_names = bitcell_1w_1r.pin_names
        self.bl_names = [pin_names[0], pin_names[2]]
        self.br_names = [pin_names[1], pin_names[3]]
        self.wl_names = [pin_names[4], pin_names[5]]


    def get_bitcell_pins(self, col, row):
        """
        Creates a list of connections in the bitcell,
        indexed by column and row, for instance use in bitcell_array
        """
        pin_name = props.bitcell.cell_1w1r.pin
        bitcell_pins = ["{0}_{1}".format(pin_name.bl0, col),
                        "{0}_{1}".format(pin_name.br0, col),
                        "{0}_{1}".format(pin_name.bl1, col),
                        "{0}_{1}".format(pin_name.br1, col),
                        "{0}_{1}".format(pin_name.wl0, row),
                        "{0}_{1}".format(pin_name.wl1, row),
                        "vdd",
                        "gnd"]
        return bitcell_pins

    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        return [props.bitcell.cell_1w1r.pin.wl0,
                props.bitcell.cell_1w1r.pin.wl1]

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        return [props.bitcell.cell_1w1r.pin.bl0,
                props.bitcell.cell_1w1r.pin.br0,
                props.bitcell.cell_1w1r.pin.bl1,
                props.bitcell.cell_1w1r.pin.br1]

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return [props.bitcell.cell_1w1r.pin.bl0,
                props.bitcell.cell_1w1r.pin.bl1]

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return [props.bitcell.cell_1w1r.pin.br0,
                props.bitcell.cell_1w1r.pin.br1]

    def get_read_bl_names(self):
        """ Creates a list of bl pin names associated with read ports """
        return [props.bitcell.cell_1w1r.pin.bl0,
                props.bitcell.cell_1w1r.pin.bl1]

    def get_read_br_names(self):
        """ Creates a list of br pin names associated with read ports """
        return [props.bitcell.cell_1w1r.pin.br0,
                props.bitcell.cell_1w1r.pin.br1]

    def get_write_bl_names(self):
        """ Creates a list of bl pin names associated with write ports """
        return [props.bitcell.cell_1w1r.pin.bl0]

    def get_write_br_names(self):
        """ Creates a list of br pin names asscociated with write ports"""
        return [props.bitcell.cell_1w1r.pin.br1]

    def get_bl_name(self, port=0):
        """Get bl name by port"""
        return self.bl_names[port]

    def get_br_name(self, port=0):
        """Get bl name by port"""
        return self.br_names[port]

    def get_wl_name(self, port=0):
        """Get wl name by port"""
        debug.check(port < 2, "Two ports for bitcell_1rw_1r only.")
        return self.wl_names[port]

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges to graph. Multiport bitcell timing graph is too complex
           to use the add_graph_edges function."""
        pin_dict = {pin: port for pin, port in zip(self.pins, port_nets)}
        pins = props.bitcell.cell_1w1r.pin
        # Edges hardcoded here. Essentially wl->bl/br for both ports.
        # Port 0 edges
        graph.add_edge(pin_dict[pins.wl1], pin_dict[pins.bl1], self)
        graph.add_edge(pin_dict[pins.wl1], pin_dict[pins.br1], self)
        # Port 1 is a write port, so its timing is not considered here.
