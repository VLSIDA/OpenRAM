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


class bitcell(bitcell_base.bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)  This module implements the
    single memory cell used in the design. It is a hand-made cell, so
    the layout and netlist should be available in the technology
    library.
    """

    name = "cell_6t"
    pin_names = [
        props.bitcell.cell_6t.pin.bl,
        props.bitcell.cell_6t.pin.br,
        props.bitcell.cell_6t.pin.wl,
        props.bitcell.cell_6t.pin.vdd,
        props.bitcell.cell_6t.pin.gnd,
    ]


    # If we have a split WL bitcell, if not be backwards
    # compatible in the tech file
    type_list = ["OUTPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
    storage_nets = ['Q', 'Q_bar']

    cell_size_layer = "boundary"

    def __init__(self, name=""):
        if not name:
            name = self.name

        bitcell_base.bitcell_base.__init__(self, name)
        debug.info(2, "Create bitcell")

        (width, height) = utils.get_libcell_size(name,
                                                 GDS["unit"],
                                                 layer[self.cell_size_layer])
        pin_map = utils.get_libcell_pins(self.pin_names,
                                         name,
                                         GDS["unit"])

        self.width = width
        self.height = height
        self.pin_map = pin_map
        self.add_pin_types(self.type_list)
        self.nets_match = self.do_nets_exist(self.storage_nets)

    def get_all_wl_names(self):
        """ Creates a list of all wordline pin names """
        row_pins = [props.bitcell.cell_6t.pin.wl]
        return row_pins

    def get_all_bitline_names(self):
        """ Creates a list of all bitline pin names (both bl and br) """
        pin = props.bitcell.cell_6t.pin
        column_pins = [pin.bl, pin.br]
        return column_pins

    def get_all_bl_names(self):
        """ Creates a list of all bl pins names """
        return [props.bitcell.cell_6t.pin.bl]

    def get_all_br_names(self):
        """ Creates a list of all br pins names """
        return [props.bitcell.cell_6t.pin.br]

    def get_bl_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_6t.pin.bl

    def get_br_name(self, port=0):
        """Get bl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_6t.pin.br

    def get_wl_name(self, port=0):
        """Get wl name"""
        debug.check(port == 0, "One port for bitcell only.")
        return props.bitcell.cell_6t.pin.wl

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        self.add_graph_edges(graph, port_nets)
