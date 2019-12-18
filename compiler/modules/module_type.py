# See LICENSE for licensing information.
#
# Copyright (c) 2016-2019 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#

class ModuleType():
    """
    This is a class that maps cell names to python classes implementing them.
    """
    def __init__(self):
        self.names = {}
        self.names['contact']                       = 'contact'
        self.names['precharge']                     = 'precharge'
        self.names['pinv']                          = 'pinv'
        self.names['dff_buf']                       = 'dff_buf'
        self.names['sense_amp']                     = 'sense_amp'
        self.names['bitcell']                       = 'bitcell'
        self.names['port_data']                     = 'port_data'
        self.names['port_address']                  = 'port_address'
        self.names['replica_bitcell_array']         = 'replica_bitcell_array'
        self.names['bank_select']                   = 'bank_select'
        self.names['dff']                           = 'dff'
        self.names['pinvbuf']                       = 'pinvbuf'
        self.names['hierarchical_predecode2x4']     = 'hierarchical_predecode2x4'
        self.names['hierarchical_predecode3x8']     = 'hierarchical_predecode3x8'
        self.names['replica_bitcell']               = 'replica_bitcell'
        self.names['dummy_bitcell']                 = 'dummy_bitcell'
        self.names['bitcell']                       = 'bitcell'
        self.names['pnor2']                         = 'pnor2'
        self.names['pnand2']                        = 'pnand2'
        self.names['precharge_array']               = 'precharge_array'
        self.names['sense_amp_array']               = 'sense_amp_array'
        self.names['column_mux_array']              = 'column_mux_array'
        self.names['write_driver_array']            = 'write_driver_array'
        self.names['write_mask_and_array']          = 'write_mask_and_array'
        self.names['pand2']                         = 'pand2'
        self.names['write_driver']                  = 'write_driver'
        self.names['dff_buf_array']                 = 'dff_buf_array'
        self.names['pdriver']                       = 'pdriver'
        self.names['pand3']                         = 'pand3'
        self.names['delay_chain']                   = 'delay_chain'
        self.names['decoder']                       = 'decoder'
        self.names['wordline_driver']               = 'wordline_driver'
        self.names['tri_gate']                      = 'tri_gate'
        self.names['tri_gate_array']                = 'tri_gate_array'
        self.names['bitcell_array']                 = 'bitcell_array'
        self.names['replica_column']                = 'replica_column'
        self.names['dummy_array']                   = 'dummy_array'
        self.names['single_level_column_mux_array'] = 'single_level_column_mux_array'
        self.names['single_level_column_mux']       = 'single_level_column_mux'
        self.names['sram']                          = 'sram'
        self.names['ptx']                           = 'ptx'
        self.names['hierarchical_decoder']          = 'hierarchical_decoder'
        self.names['pbuf']                          = 'pbuf'
        self.names['control_logic']                 = 'control_logic'
        self.names['bank']                          = 'bank'
        self.names['pbitcell']                      = 'pbitcell'
        self.names['pnand3']                        = 'pnand3'
        self.names['pwrite_driver']                 = 'pwrite_driver'
        self.names['ptristate_inv']                 = 'ptristate_inv'
        self.names['ptristate_buf']                 = 'ptristate_buf'
        self.names['dff_array']                     = 'dff_array'

    def __setitem__(self, b, c):
        self.names[b] = c

    def __getitem__(self, b):
        if b not in self.names.keys():
            raise KeyError
        
        return self.names[b]
        
