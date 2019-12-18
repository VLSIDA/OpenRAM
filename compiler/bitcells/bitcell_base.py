# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

import debug
import design
from globals import OPTS
import logical_effort
from tech import parameter, drc


class bitcell_base(design.design):
    """
    Base bitcell parameters to be over-riden.
    """
    def __init__(self, name):
        design.design.__init__(self, name)

    def get_stage_effort(self, load):
        parasitic_delay = 1
        # This accounts for bitline being drained
        # thought the access TX and internal node
        size = 0.5
        # Assumes always a minimum sizes inverter.
        # Could be specified in the tech.py file.
        cin = 3
        # min size NMOS gate load
        read_port_load = 0.5

        return logical_effort.logical_effort('bitline',
                                             size,
                                             cin,
                                             load + read_port_load,
                                             parasitic_delay,
                                             False)

    def analytical_power(self, corner, load):
        """Bitcell power in nW. Only characterizes leakage."""
        from tech import spice
        leakage = spice["bitcell_leakage"]
        # FIXME
        dynamic = 0
        total_power = self.return_power(dynamic, leakage)
        return total_power

    def input_load(self):
        """ Return the relative capacitance of the access transistor gates """
        
        # FIXME: This applies to bitline capacitances as well.
        # FIXME: sizing is not accurate with the handmade cell.
        # Change once cell widths are fixed.
        access_tx_cin = parameter["6T_access_size"] / drc["minwidth_tx"]
        return 2 * access_tx_cin
        
    def get_wl_cin(self):
        """Return the relative capacitance of the access transistor gates"""
        # This is a handmade cell so the value must be entered
        # in the tech.py file or estimated.
        # Calculated in the tech file by summing the widths of all
        # the related gates and dividing by the minimum width.
        # FIXME: sizing is not accurate with the handmade cell.
        # Change once cell widths are fixed.
        access_tx_cin = parameter["6T_access_size"] / drc["minwidth_tx"]
        return 2 * access_tx_cin

    def get_storage_net_names(self):
        """
        Returns names of storage nodes in bitcell in
        [non-inverting, inverting] format.
        """
        # Checks that they do exist
        if self.nets_match:
            return self.storage_nets
        else:
            fmt_str = "Storage nodes={} not found in spice file."
            debug.info(1, fmt_str.format(self.storage_nets))
            return None

    def get_storage_net_offset(self):
        """
        Gets the location of the storage net labels to add top level 
        labels for pex simulation.
        """
        #TODO: use getTexts to support custom bitcells
        # If we generated the bitcell, we already know where Q and Q_bar are
        #if OPTS.bitcell is not "pbitcell":
        #    self.storage_net_offsets = []
        #    for net in get_storage_net_names:
        #        if net is "Q" or "Q_bar":
        #            for text in self.getTexts("metal1"):
        #               self.storage_net_offsets.append(text.offsetInMicrons)
        return(self.storage_net_offsets)

    def get_normalized_storage_net_offset(self):               
        """
        Convert storage net offset to be relative to the bottom left corner
        of the bitcell. This is useful for making sense of offsets outside 
        of the bitcell.
        """     

        Q_x = self.storage_net_offsets[0][0] - self.leftmost_xpos
        Q_y = self.storage_net_offsets[0][1] - self.botmost_ypos
        Q_bar_x = self.storage_net_offsets[1][0] - self.leftmost_xpos
        Q_bar_y = self.storage_net_offsets[1][1] - self.botmost_ypos

        normalized_storage_net_offset = [[Q_x,Q_y],[Q_bar_x,Q_bar_y]]

        return normalized_storage_net_offset


    def build_graph(self, graph, inst_name, port_nets):
        """
        By default, bitcells won't be part of the graph.

        """
        return
