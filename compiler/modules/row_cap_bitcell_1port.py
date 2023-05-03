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


class row_cap_bitcell_1port(bitcell_base):
    """
    Row end cap cell.
    """

    def __init__(self, name="row_cap_bitcell_1port"):
        bitcell_base.__init__(self, name, prop=props.row_cap_1port)
        debug.info(2, "Create row_cap bitcell 1 port object")

        self.no_instances = True

    def build_graph(self, graph, inst_name, port_nets):
        """
        Adds edges based on inputs/outputs.
        Overrides base class function.
        """
        pass
