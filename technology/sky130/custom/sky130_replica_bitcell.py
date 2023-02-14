#!/usr/bin/env python3
# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California
# All rights reserved.
#

from openram import debug
from openram.base import logical_effort
from openram.modules import bitcell_base
from openram.tech import parameter, drc
from openram.tech import cell_properties as props


class sky130_replica_bitcell(bitcell_base):
    """
    A single bit cell (6T, 8T, etc.)
    This module implements the single memory cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library. """

    def __init__(self, version, name=""):
        if version == "opt1":
            cell_name = "sky130_fd_bd_sram__openram_sp_cell_opt1_replica"
        elif version == "opt1a":
            cell_name = "sky130_fd_bd_sram__openram_sp_cell_opt1a_replica"
        super().__init__(name, cell_name, prop=props.bitcell_1port)
        debug.info(2, "Create replica bitcell object")

    def get_stage_effort(self, load):
        parasitic_delay = 1
        size = 0.5 # This accounts for bitline being drained thought the access TX and internal node
        cin = 3 # Assumes always a minimum sizes inverter. Could be specified in the tech.py file.
        read_port_load = 0.5 # min size NMOS gate load
        return logical_effort('bitline', size, cin, load + read_port_load, parasitic_delay, False)

    def input_load(self):
        """Return the relative capacitance of the access transistor gates"""

        # FIXME: This applies to bitline capacitances as well.
        access_tx_cin = parameter["6T_access_size"] / drc["minwidth_tx"]
        return 2 * access_tx_cin

    def analytical_power(self, corner, load):
        """Bitcell power in nW. Only characterizes leakage."""
        from openram.tech import spice
        leakage = spice["bitcell_leakage"]
        dynamic = 0 # temporary
        total_power = self.return_power(dynamic, leakage)
        return total_power

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)
