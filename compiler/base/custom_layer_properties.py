# See LICENSE for licensing information.
#
# Copyright (c) 2016-2020 Regents of the University of California and The Board
# of Regents for the Oklahoma Agricultural and Mechanical College
# (acting for and on behalf of Oklahoma State University)
# All rights reserved.
#
from design import design


class _bank:
    def __init__(self, stack, pitch):
        # bank
        # column address route: stack, pitch
        # m1_stack, m2_pitch (default)
        # m2_stack, m3_pitch (sky130)
        self.stack = stack
        self.pitch = pitch
    

class _hierarchical_decoder:
    def __init__(self,
                 bus_layer,
                 bus_directions,
                 bus_pitch,
                 bus_space,
                 input_layer,
                 output_layer,
                 output_layer_pitch,
                 vertical_supply):
        # hierarchical_decoder
        # bus_layer, bus_directions, bus_pitch, bus_space, input_layer, output_layer, output_layer_pitch
        # m2, pref, m2_pitch, m2_space, m1, m3, m3_pitch
        # m1, nonpref, m1_pitch, m2_space, m2, li, li_pitch (sky130)
        # 
        # vertical vdd/gnd
        # special jog

        # hierarchical_predecode
        # bus_layer, bus_directions, bus_pitch, bus_space, input_layer, output_layer, output_layer_pitch
        # m2, pref, m2_pitch, m2_space, m1, m1, m1_pitch
        # m1, nonpref, m1_pitch, 1`.5*m1_space, m2, li, li_pitch (sky130)
        #
        # vertical vdd/gnd
        # special jogging
        self.bus_layer = bus_layer
        self.bus_directinos = bus_directions
        self.bus_pitch = bus_pitch
        self.bus_sapce = bus_space
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.vertical_supply = vertical_supply

        
class _column_mux_array:
    def __init__(self,
                 select_layer,
                 select_pitch,
                 bitline_layer):
        # column_mux_array
        # sel_layer, sel_pitch, bitline_layer
        # m1, m2_pitch, m2
        # m3, m3_pitch, m1 (sky130)
        self.select_layer = select_layer
        self.select_pitch= select_pitch
        self.bitline_layer = bitline_layer

        
class _port_address:
    def __init__(self,
                 supply_offset):
        # port_adress
        # special supply offset
        self.supply_offset = supply_offset

        
class _port_data:
    def __init__(self,
                 enable_layer):
        # port_data
        # connect bitlines instead of chanel route

        # sense_amp_array
        # en_layer
        # m1
        # m3 (sky130)
    
        # precharge_array
        # en_bar_layer
        # m1
        # m3 (sky130)
        self.enable_layer = enable_layer


class _replica_column:
    def __init__(self,
                 even_rows):
        # replica_column
        # even row check (sky130)
        self.even_rows = even_rows
        
        
class _wordline_buffer_array:
    def __init__(self,
                 vertical_supply):
        # wordline_buffer_array
        # vertical vdd/gnd (sky130)
        self.vertical_supply = vertical_supply


class _wordline_driver_array:
    def __init__(self,
                 vertical_supply):
        # wordline_driver_array
        # vertical vdd/gnd (sky130)
        self.vertical_supply = vertical_supply
        
        
class layer_properties():
    """
    This contains meta information about the module routing layers. These
    can be overriden in the tech.py file.
    """
    def __init__(self):
        self.names = {}

        self._bank = _bank(stack=design.m1_stack,
                           pitch=design.m2_pitch)

    @property
    def bank(self):
        return self._bank
                 
    @property
    def column_mux_array(self):
        return self._column_mux_array

    @property
    def hierarchical_decoder(self):
        return self._hierarcical_decoder

    @property
    def port_address(self):
        return self._port_address

    @property
    def port_data(self):
        return self._port_data

    @property
    def replica_column(self):
        return self._replica_column

    @property
    def wordline_buffer_array(self):
        return self._wordline_buffer_array

    @property
    def wordline_driver_array(self):
        return self._wordline_driver_array
    
