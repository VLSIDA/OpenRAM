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
from tech import GDS, layer, parameter, drc
from tech import cell_properties as props
from globals import OPTS
import logical_effort


class sense_amp(design.design):
    """
    This module implements the single sense amp cell used in the design. It
    is a hand-made cell, so the layout and netlist should be available in
    the technology library.
    Sense amplifier to read a pair of bit-lines.
    """
    pin_names = [props.sense_amp.pin.bl,
                 props.sense_amp.pin.br,
                 props.sense_amp.pin.dout,
                 props.sense_amp.pin.en,
                 props.sense_amp.pin.vdd,
                 props.sense_amp.pin.gnd]
    type_list = ["INPUT", "INPUT", "OUTPUT", "INPUT", "POWER", "GROUND"]
    if not OPTS.netlist_only:
        (width, height) = utils.get_libcell_size("sense_amp", GDS["unit"], layer["boundary"])
        pin_map = utils.get_libcell_pins(pin_names, "sense_amp", GDS["unit"])
    else:
        (width, height) = (0, 0)
        pin_map = []

    def get_bl_names(self):
        return props.sense_amp.pin.bl

    def get_br_names(self):
        return props.sense_amp.pin.br

    @property
    def dout_name(self):
        return props.sense_amp.pin.dout

    @property
    def en_name(self):
        return props.sense_amp.pin.en

    def __init__(self, name):
        super().__init__(name)
        debug.info(2, "Create sense_amp")

        self.width = sense_amp.width
        self.height = sense_amp.height
        self.pin_map = sense_amp.pin_map
        self.add_pin_types(self.type_list)
        
    def get_cin(self):
    
        # FIXME: This input load will be applied to both the s_en timing and bitline timing.
        
        # Input load for the bitlines which are connected to the source/drain of a TX. Not the selects.
        from tech import spice
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
        return logical_effort.logical_effort('column_mux', sa_size, cin, load + cc_inv_cin, parasitic_delay, False)

    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        # Power in this module currently not defined. Returns 0 nW (leakage and dynamic).
        total_power = self.return_power()
        return total_power

    def get_en_cin(self):
        """Get the relative capacitance of sense amp enable gate cin"""
        pmos_cin = parameter["sa_en_pmos_size"] / drc("minwidth_tx")
        nmos_cin = parameter["sa_en_nmos_size"] / drc("minwidth_tx")
        # sen is connected to 2 pmos isolation TX and 1 nmos per sense amp.
        return 2 * pmos_cin + nmos_cin
    
    def get_enable_name(self):
        """Returns name used for enable net"""
        # FIXME: A better programmatic solution to designate pins
        enable_name = self.en_name
        debug.check(enable_name in self.pin_names, "Enable name {} not found in pin list".format(enable_name))
        return enable_name
    
    def build_graph(self, graph, inst_name, port_nets):
        """Adds edges based on inputs/outputs. Overrides base class function."""
        self.add_graph_edges(graph, port_nets)
