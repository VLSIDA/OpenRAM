# See LICENSE for licensing information.
#
# Copyright (c) 2016-2023 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from openram import debug
from openram.base import design
from openram.base import logical_effort
from openram.tech import parameter, drc, spice
from openram.tech import cell_properties as props


class sense_amp(design):
    """
    This module implements the single sense amp cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    Sense amplifier to read a pair of bit-lines.
    """

    def __init__(self, name="sense_amp"):
        super().__init__(name, prop=props.sense_amp)
        debug.info(2, "Create sense_amp")

    def get_bl_names(self):
        return "bl"

    def get_br_names(self):
        return "br"

    @property
    def dout_name(self):
        return "dout"

    @property
    def en_name(self):
        return "en"

    def get_cin(self):

        # FIXME: This input load will be applied to both the s_en timing and bitline timing.

        # Input load for the bitlines which are connected to the source/drain of a TX. Not the selects.
        from openram.tech import spice
        # Default is 8x. Per Samira and Hodges-Jackson book:
        # "Column-mux transistors driven by the decoder must be sized for optimal speed"
        bitline_pmos_size = 8 # FIXME: This should be set somewhere and referenced. Probably in tech file.
        return spice["min_tx_drain_c"] * bitline_pmos_size # ff

    def get_stage_effort(self, load):
        # Delay of the sense amp will depend on the size of the amp and the output load.
        parasitic_delay = 1
        cin = (parameter["sa_inv_pmos_size"] + parameter["sa_inv_nmos_size"]) / drc("minwidth_tx")
        sa_size = parameter["sa_inv_nmos_size"] / drc("minwidth_tx")
        cc_inv_cin = cin
        return logical_effort('column_mux', sa_size, cin, load + cc_inv_cin, parasitic_delay, False)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        # Power in this module currently not defined. Returns 0 nW (leakage and dynamic).
        total_power = self.return_power()
        return total_power

    def get_enable_name(self):
        """Returns name used for enable net"""
        # FIXME: A better programmatic solution to designate pins
        enable_name = self.en_name
        debug.check(enable_name in self.pin_names, "Enable name {} not found in pin list".format(enable_name))
        return enable_name

    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)

    def is_non_inverting(self):
        """Return input to output polarity for module"""

        #FIXME: This only applied to bl/br -> dout and not s_en->dout
        return True

    def get_on_resistance(self):
        """On resistance of pinv, defined by single nmos"""
        is_nchannel = True
        stack = 1
        is_cell = False
        return self.tr_r_on(parameter["sa_inv_nmos_size"], is_nchannel, stack, is_cell)

    def get_input_capacitance(self):
        """Input cap of input, passes width of gates to gate cap function"""
        return self.gate_c(parameter["sa_inv_nmos_size"])

    def get_intrinsic_capacitance(self):
        """Get the drain capacitances of the TXs in the gate."""
        stack = 1
        mult = 1
        # Add the inverter drain Cap and the bitline TX drain Cap
        nmos_drain_c =  self.drain_c_(parameter["sa_inv_nmos_size"]*mult,
                                      stack,
                                      mult)
        pmos_drain_c =  self.drain_c_(parameter["sa_inv_pmos_size"]*mult,
                                      stack,
                                      mult)

        bitline_pmos_size = 8
        bl_pmos_drain_c =  self.drain_c_(drc("minwidth_tx")*bitline_pmos_size,
                                      stack,
                                      mult)
        return nmos_drain_c + pmos_drain_c + bl_pmos_drain_c

    def cacti_rc_delay(self, inputramptime, tf, vs1, vs2, rise, extra_param_dict):
        """ Special RC delay function used by CACTI for sense amp delay
        """
        import math

        c_senseamp = extra_param_dict['load']
        vdd = extra_param_dict['vdd']
        tau = c_senseamp/spice["sa_transconductance"]
        return tau*math.log(vdd/(0.1*vdd))
